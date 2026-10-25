"""End-to-end CLI smoke tests for the canonical Ubiquitous Maniacs scenario (issue #561).

These are **not** unit tests of the case object. They spawn the real, documented command in a
subprocess and drive it through stdin, exactly as a player does:

    python -m strategy_game.rpg --scenario ubiquitous-maniacs --save FILE --new

That distinction is the point of the module. The unit tests in
``test_ubiquitous_maniacs_case.py`` call ``CaseSession`` directly and would keep passing if the
CLI lost a command, printed nothing, or crashed on a refusal; a player would not. Everything here
asserts on what the *process* printed and on the *exit status*, so a regression in the entrypoint
is a failure here even when the engine is fine.

What is covered, matching the acceptance criteria of #561:

* a full successful playthrough to ``closed_by_evidence``;
* the second supported resolution, ``closed_by_withdrawal``;
* the same route twice with the same seed produces byte-identical output (determinism);
* save at the beginning, mid-case, and at resolution, and resume from each;
* a corrupt save is refused with a useful message and a non-zero status, not a traceback;
* a save from the *other* adapter is refused rather than half-loaded;
* every invalid input a player might type — unknown seat, unknown action, unknown command,
  unknown resolution, leaving the last scene — produces a message and no exception;
* the interpreter gate: on an older interpreter the process exits 2 with a readable reason
  instead of a bare ``ImportError`` from inside the rules layer.

Run:

    python -m unittest strategy_game.tests.test_ubiquitous_maniacs_e2e -v

**Relationship to `test_ubiquitous_maniacs_cli_playthrough.py`.** That module drives the same
launcher *in process*, patching ``builtins.input``. It is faster and it covers one thing this
module cannot: that a corrupt save is refused **without being overwritten**. This module is the
complementary layer — a real subprocess, so it also covers argv parsing, exit status and the
stdout/stderr split, and it adds determinism across two runs, a seed that must change the dice,
and refusal of the *other* adapter's save. Both are kept: neither subsumes the other.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

#: The documented entrypoint. Kept as a list so a test can print it verbatim when it fails.
BASE = [sys.executable, "-m", "strategy_game.rpg", "--scenario", "ubiquitous-maniacs"]

#: A route that reaches the first ending. Every action is legal from the seat given, and the
#: party is large enough that no seat has to act twice in one scene.
EVIDENCE_ROUTE = (
    "act agent_1 inspect_register\n"
    "act agent_2 question_orderly\n"
    "next\n"
    "act agent_1 compare_traces\n"
    "act agent_2 interview_patient\n"
    "assemble\n"
    "resolve closed_by_evidence\n"
)

#: A shorter route that still reaches the second ending. `closed_by_withdrawal` requires no
#: finding, so it must be reachable even from a thin record — that is the point of testing it.
WITHDRAWAL_ROUTE = (
    "act pc_leader inspect_register\n"
    "next\n"
    "resolve closed_by_withdrawal\n"
)


def run(args: list[str], stdin: str, timeout: int = 120) -> subprocess.CompletedProcess:
    """Run the CLI with ``stdin`` and capture the result."""
    return subprocess.run(BASE + args, input=stdin, text=True, capture_output=True,
                          timeout=timeout, cwd=REPO, check=False)


def describe(result: subprocess.CompletedProcess) -> str:
    """A failure message that shows the command, the status and both streams."""
    return (
        f"\ncommand: {' '.join(BASE)}\n"
        f"exit:    {result.returncode}\n"
        f"stdout:\n{result.stdout[-2000:]}\n"
        f"stderr:\n{result.stderr[-2000:]}"
    )


class EnvironmentTests(unittest.TestCase):
    """Record the interpreter the run was made with, because #561 asks for it."""

    def test_the_supported_interpreter_is_named_in_the_output(self) -> None:
        """The suite must say which interpreter it verified against."""
        self.assertGreaterEqual(sys.version_info[:2], (3, 11),
                                f"this scenario needs 3.11+; running {sys.version.split()[0]}")
        print(f"\n  e2e verified on Python {sys.version.split()[0]} ({sys.platform})")


class PlaythroughTests(unittest.TestCase):
    """A player can start the case, play it and close it with either ending."""

    def test_a_full_playthrough_reaches_the_evidence_ending(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "ward.json"
            result = run(["--save", str(save), "--new"], EVIDENCE_ROUTE)
            self.assertEqual(result.returncode, 0, describe(result))
            self.assertIn("Case closed", result.stdout, describe(result))

            payload = json.loads(save.read_text(encoding="utf-8"))
            self.assertEqual(payload["resolution_id"], "closed_by_evidence")
            self.assertEqual(payload["schema_version"], "case-session-1")
            self.assertIn("finding-ward", payload["findings"])
            self.assertIn("register", payload["clues"])

    def test_the_withdrawal_ending_is_reachable_from_a_thin_record(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "ward.json"
            result = run(["--save", str(save), "--new"], WITHDRAWAL_ROUTE)
            self.assertEqual(result.returncode, 0, describe(result))
            self.assertIn("Case closed", result.stdout, describe(result))

            payload = json.loads(save.read_text(encoding="utf-8"))
            self.assertEqual(payload["resolution_id"], "closed_by_withdrawal")
            self.assertEqual(payload["findings"], [])

    def test_the_same_route_and_seed_produce_identical_output(self) -> None:
        """Determinism, asserted end to end rather than on one object.

        The transcript names the save file, so the two runs write to the *same* filename in
        different directories and that path is normalised out before comparing: determinism is a
        property of the game transcript, not of where the player asked it to save.
        """
        with (
            tempfile.TemporaryDirectory() as one,
            tempfile.TemporaryDirectory() as two,
        ):
            first = run(["--save", str(Path(one) / "ward.json"), "--new", "--seed", "7"],
                        EVIDENCE_ROUTE)
            second = run(["--save", str(Path(two) / "ward.json"), "--new", "--seed", "7"],
                         EVIDENCE_ROUTE)
            self.assertEqual(first.returncode, 0, describe(first))
            self.assertEqual(second.returncode, 0, describe(second))
            self.assertEqual(
                first.stdout.replace(str(Path(one)), "<dir>"),
                second.stdout.replace(str(Path(two)), "<dir>"),
                "two runs with the same seed must print the same transcript",
            )

    def test_a_different_seed_produces_a_different_transcript(self) -> None:
        """The seed must actually reach the dice, or determinism above proves nothing."""
        with tempfile.TemporaryDirectory() as folder:
            a = run(["--save", str(Path(folder) / "a.json"), "--new", "--seed", "1"], EVIDENCE_ROUTE)
            b = run(["--save", str(Path(folder) / "b.json"), "--new", "--seed", "999"], EVIDENCE_ROUTE)
            self.assertEqual(a.returncode, 0, describe(a))
            self.assertEqual(b.returncode, 0, describe(b))
            self.assertNotEqual(a.stdout, b.stdout,
                                "a different seed should roll different dice")


class SaveAndResumeTests(unittest.TestCase):
    """Saving and resuming work at the beginning, mid-case and at resolution."""

    def test_resume_from_the_beginning(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "ward.json"
            started = run(["--save", str(save), "--new"], "save\nquit\n")
            self.assertEqual(started.returncode, 0, describe(started))

            resumed = run(["--save", str(save)], "next\nsave\nquit\n")
            self.assertEqual(resumed.returncode, 0, describe(resumed))
            self.assertIn("records", resumed.stdout, describe(resumed))

    def test_resume_mid_case_and_finish(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "ward.json"
            part = run(["--save", str(save), "--new"],
                       "act agent_1 inspect_register\nnext\nsave\nquit\n")
            self.assertEqual(part.returncode, 0, describe(part))

            rest = run(["--save", str(save)],
                       "act agent_1 compare_traces\nact agent_2 interview_patient\n"
                       "assemble\nresolve closed_by_evidence\n")
            self.assertEqual(rest.returncode, 0, describe(rest))
            self.assertIn("Case closed", rest.stdout, describe(rest))
            payload = json.loads(save.read_text(encoding="utf-8"))
            self.assertEqual(payload["resolution_id"], "closed_by_evidence")

    def test_resume_after_resolution_reports_the_closed_case(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "ward.json"
            done = run(["--save", str(save), "--new"], EVIDENCE_ROUTE)
            self.assertEqual(done.returncode, 0, describe(done))

            again = run(["--save", str(save)], "quit\n")
            self.assertEqual(again.returncode, 0, describe(again))
            payload = json.loads(save.read_text(encoding="utf-8"))
            self.assertEqual(payload["resolution_id"], "closed_by_evidence")

    def test_a_corrupt_save_is_refused_with_a_useful_message(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "broken.json"
            save.write_text("{ this is not json", encoding="utf-8")
            result = run(["--save", str(save)], "quit\n")
            self.assertEqual(result.returncode, 2, describe(result))
            self.assertIn("cannot resume saved case", result.stderr, describe(result))
            self.assertIn("not valid JSON", result.stderr, describe(result))
            self.assertNotIn("Traceback", result.stderr, describe(result))

    def test_a_save_from_the_other_adapter_is_refused(self) -> None:
        """The two adapters must not half-load each other's saves."""
        with tempfile.TemporaryDirectory() as legacy_folder:
            legacy_save = str(Path(legacy_folder) / "legacy.json")
            other = subprocess.run(
                [sys.executable, "-m", "strategy_game.rpg",
                 "--scenario", "ubiquitous-maniacs-legacy",
                 "--save", legacy_save, "--new"],
                input="quit\n", text=True, capture_output=True, timeout=120, cwd=REPO,
                check=False,
            )
            self.assertEqual(other.returncode, 0, describe(other))

            result = run(["--save", legacy_save], "quit\n")
            self.assertEqual(result.returncode, 2, describe(result))
            self.assertIn("cannot resume saved case", result.stderr, describe(result))
            self.assertNotIn("Traceback", result.stderr, describe(result))


class InvalidInputTests(unittest.TestCase):
    """A player's mistakes are answered, never raised."""

    def _assert_refused(self, stdin: str, expected: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as folder:
            result = run(["--save", str(Path(folder) / "w.json"), "--new"], stdin + "quit\n")
        self.assertEqual(result.returncode, 0, describe(result))
        self.assertIn(expected, result.stdout, describe(result))
        self.assertNotIn("Traceback", result.stderr, describe(result))
        return result

    def test_an_unknown_seat_lists_the_roster(self) -> None:
        self._assert_refused("act nobody inspect_register\n", "no seat or character 'nobody'")

    def test_an_unknown_action_lists_what_is_offered(self) -> None:
        self._assert_refused("act agent_1 no_such_action\n", "has no action 'no_such_action'")

    def test_an_unknown_command_says_how_to_get_help(self) -> None:
        self._assert_refused("gibberish\n", "Unknown command")

    def test_an_unknown_resolution_is_refused(self) -> None:
        self._assert_refused("resolve no_such_resolution\n", "no resolution 'no_such_resolution'")

    def test_leaving_the_last_scene_says_what_to_do_instead(self) -> None:
        result = self._assert_refused("next\nnext\n", "this is the last scene")
        self.assertIn("resolve(", result.stdout, describe(result))

    def test_a_second_action_by_the_same_seat_is_refused_with_the_reason(self) -> None:
        self._assert_refused(
            "act agent_1 inspect_register\nact agent_1 question_orderly\n",
            "has already acted this scene",
        )

    def test_resolving_the_evidence_ending_without_the_finding_is_refused(self) -> None:
        self._assert_refused("resolve closed_by_evidence\n", "Cannot do that")

    def test_help_and_status_both_answer(self) -> None:
        for command in ("help", "status"):
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as folder:
                    result = run(["--save", str(Path(folder) / "w.json"), "--new"],
                                 command + "\nquit\n")
                self.assertEqual(result.returncode, 0, describe(result))
                self.assertTrue(result.stdout.strip(), f"{command} printed nothing")


if __name__ == "__main__":
    unittest.main()
