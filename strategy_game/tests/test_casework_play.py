"""The interactive play mode (``--play``): the same case, one command at a time.

What is pinned here is what the mode claims:

1. **Three endings are reachable by playing.** A script standing in for a player reaches each of the
   case's resolutions from the prompt, and each one writes its own objective into the campaign.
2. **There is no second engine.** The same seed and the same choices played at the prompt produce the
   *same session record* as the headless run — same clues, same findings, same dice in the event log,
   same persisted books. The play mode chooses; ``CaseSession`` decides.
3. **The choices are the session's.** Every action the menu offers or locks is exactly what
   :meth:`CaseSession.actions` reports, a locked one is refused without costing the turn, and an
   ambiguous seat name is reported rather than guessed.
4. **A save is a pause.** A case saved with ``quit`` mid-morning resumes into the same later rolls and
   the same ending as an uninterrupted run — seeded or not, because the save carries the dice state.
5. **Determinism and a clean exit.** The same seed and the same commands replay to an identical
   transcript; ``quit`` and end-of-input both save and return rather than tracebacking.

The headless path itself is guarded where prose is *not* at stake: the entrypoint's ``--json`` record
for a route and seed is compared with :func:`strategy_game.casework.demo.run_demo` for the same route
and seed, so the headless CLI is still exactly the demo. Byte-for-byte identity of the headless text
was verified with ``sha256sum`` against ``origin/main`` while making this change; it is deliberately
not encoded here, because AGENTS.md keeps scenario prose out of executable tests.
"""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import ClassVar
from unittest import mock

from strategy_game.casework import kallio
from strategy_game.casework.__main__ import main
from strategy_game.casework.demo import play as demo_play
from strategy_game.casework.demo import run_demo
from strategy_game.casework.play import play, render_menu
from strategy_game.casework.session import CaseSession, load_session

#: The moves the headless demo makes, as a player would type them. Seat and action tokens are
#: deliberately mixed (fragments, numbers, ``pc``) so the command syntax is exercised.
INVESTIGATE = (
    "act harri read_the_duty_log",
    "act pc take_the_liaison_aside",
    "next",
    "act falk interview_nila",
    "act harri scan_the_stack",
    "act univaara promise_protection",
    "next",
    "act sebastian read_the_stairwell",
    "act harri pull_the_mesh_log",
    "act falk search_the_landing",
    "act pc hold_the_hatch",
    "next",
    "act univaara supervise_the_reading",
    "act harri check_the_thermal_record",
    "act falk ask_her_why_she_stayed",
    "next",
    "act pc assemble_the_chain",
    "act harri pull_the_batch_signout",
    "act sebastian read_his_file",
    "act univaara brief_the_liaison_early",
    "act falk get_to_the_bay_first",
)


class _Script:
    """A stand-in for ``input``: hands out one line per prompt and then reports end of input."""

    def __init__(self, lines) -> None:
        self.lines = list(lines)
        self.prompts: list[str] = []

    def __call__(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if not self.lines:
            raise EOFError
        return self.lines.pop(0)


def _s(outcome) -> CaseSession:
    """The session of a sitting that got as far as starting one (every script here does)."""
    assert outcome.session is not None
    return outcome.session

def _play(lines, **kwargs):
    """Run the play mode with a script and capture every line it wrote."""
    transcript: list[str] = []
    outcome = play(read=_Script(lines), write=transcript.append, **kwargs)
    return outcome, transcript


class EndingsTests(unittest.TestCase):
    """A human at the prompt can reach each of the three endings."""

    #: The seeds each ending is played on. They only make the printed run show the ending it asks
    #: for; the case is fail-forward at any seed (a lost confrontation degrades to the referral).
    SEEDS: ClassVar[dict[str, int]] = {
        "resolve 1": 461,
        "resolve closed_by_evidence": 461,
        "resolve 2 pressure": 2,
        "resolve closed_by_confrontation force": 2,
        "resolve 3": 461,
    }

    def _run(self, ending, directory: str, seed: int | None = None):
        return _play(
            [*INVESTIGATE, ending],
            seed=self.SEEDS.get(ending, 461) if seed is None else seed,
            save_to=Path(directory) / "case.json",
        )

    def test_closing_on_the_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outcome, transcript = self._run("resolve closed_by_evidence", directory)
        self.assertEqual(outcome.exit_reason, "ended")
        report = _s(outcome).report()
        self.assertEqual(report["resolution"], "closed_by_evidence")
        self.assertIn(
            "Kallio raid case closed on the record", report["persisted"]["objectives"]
        )
        self.assertIn("Persisted in the campaign", "\n".join(transcript))

    def test_closing_in_the_loading_bay_with_words(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outcome, _ = self._run("resolve 2 pressure", directory)
        report = _s(outcome).report()
        self.assertEqual(report["resolution"], "closed_by_confrontation")
        self.assertIn(
            "Kallio raid case closed with a detention", report["persisted"]["objectives"]
        )
        self.assertIn("kallio-residents-wary", report["persisted"]["reputation_labels"])

    def test_closing_in_the_loading_bay_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outcome, transcript = self._run("resolve closed_by_confrontation force", directory)
        report = _s(outcome).report()
        self.assertEqual(report["resolution"], "closed_by_confrontation")
        self.assertIn("grey-sleeve-controller", report["persisted"]["resources"])
        self.assertTrue(any("opposed attack" in line for line in transcript))
        self.assertTrue(any("wound:" in line for line in transcript))

    def test_referring_it_and_walking_away(self) -> None:
        # The third ending is always available, even with the chain unassembled.
        with tempfile.TemporaryDirectory() as directory:
            outcome, _ = _play(
                ["act pc 1", "resolve 3"],
                seed=461,
                save_to=Path(directory) / "case.json",
            )
        report = _s(outcome).report()
        self.assertEqual(report["resolution"], "closed_by_withdrawal")
        self.assertIn(
            "Kallio raid case referred to Internal Affairs", report["persisted"]["objectives"]
        )

    def test_the_three_endings_write_three_different_objectives(self) -> None:
        objectives = set()
        for ending in ("resolve 1", "resolve 2 pressure", "resolve 3"):
            with tempfile.TemporaryDirectory() as directory:
                outcome, _ = self._run(ending, directory)
            objectives.add(_s(outcome).report()["persisted"]["objectives"][-1])
        self.assertEqual(len(objectives), 3)

    def test_a_confrontation_offers_the_approach_when_none_is_typed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            script = _Script([*INVESTIGATE, "resolve 2", "force"])
            outcome = play(
                read=script,
                write=lambda line: None,
                seed=2,
                save_to=Path(directory) / "case.json",
            )
        self.assertEqual(outcome.exit_reason, "ended")
        self.assertEqual(_s(outcome).report()["resolution"], "closed_by_confrontation")
        self.assertTrue(
            any("pressure (words) or force" in prompt for prompt in script.prompts), script.prompts
        )


class NoSecondEngineTests(unittest.TestCase):
    """The prompt chooses; the session decides. Nothing is reimplemented in the front end."""

    def test_a_played_case_and_a_headless_run_are_the_same_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            headless, _, _ = demo_play(
                "investigate", seed=461, save_to=Path(directory) / "headless.json"
            )
            played, _ = _play(
                [*INVESTIGATE, "resolve closed_by_evidence"],
                seed=461,
                save_to=Path(directory) / "played.json",
            )
        # The same calls on the same seed: the event log carries every roll, so an identical log is
        # the statement that the prompt did not roll anything of its own.
        self.assertEqual(_s(played).events, headless.events)
        self.assertEqual(_s(played).report(), headless.report())
        checks = [
            event["check"]
            for event in _s(played).events
            if event.get("kind") == "case_action" and event.get("check")
        ]
        self.assertEqual(len(checks), 16)  # every rolled action on this route's script
        self.assertTrue(all(check["dice"] for check in checks))

    def test_the_menu_reports_exactly_the_sessions_verdict(self) -> None:
        session = kallio.build_session(seed=461)
        session.end_scene()
        session.act("laura_falk", "interview_nila")  # one action resolved, two now unlocked
        menu = render_menu(session)
        verdicts = session.actions()
        self.assertEqual(len(verdicts), len(session.scene_spec.actions))
        labels = [session.scene_spec.action(entry["id"]).label for entry in verdicts]
        for label in labels:
            self.assertIn(label, menu)
        locked = [line.strip() for line in menu.splitlines() if line.strip().startswith("locked")]
        self.assertEqual(len(locked), sum(1 for entry in verdicts if not entry["available"]))
        for entry in verdicts:
            with self.subTest(action=entry["id"]):
                if entry["available"]:
                    self.assertIn(entry["skill"], menu.upper())
                    self.assertEqual(entry["reason"], "")
                    self.assertNotIn(f"'{entry['id']}' requires", menu)
                else:
                    # A locked action carries the session's own words, verbatim.
                    self.assertIn(entry["reason"], menu)

    def test_a_locked_action_is_refused_without_spending_the_turn(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outcome, transcript = _play(
                ["next", "act harri scan_the_stack", "act falk interview_nila", "quit"],
                seed=461,
                save_to=Path(directory) / "case.json",
            )
        self.assertTrue(any("The case refuses that" in line for line in transcript))
        # Only the interview was spent; the refusal cost nothing.
        self.assertEqual(list(_s(outcome).acted()), ["agent_1"])
        self.assertIn("stack-card", _s(outcome).clues)

    def test_an_ambiguous_seat_is_reported_rather_than_guessed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outcome, transcript = _play(
                ["act laura interview_nila", "quit"],
                seed=461,
                save_to=Path(directory) / "case.json",
            )
        joined = "\n".join(transcript)
        self.assertIn("matches", joined)
        self.assertIn("laura_falk", joined)
        self.assertIn("laura_univaara", joined)
        self.assertEqual(_s(outcome).acted(), {})

    def test_an_unknown_command_is_not_fatal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outcome, transcript = _play(
                ["dance", "act", "resolve", "quit"],
                seed=461,
                save_to=Path(directory) / "case.json",
            )
        joined = "\n".join(transcript)
        self.assertIn("Not a command", joined)
        self.assertIn("act needs a seat and an action", joined)
        self.assertIn("resolve needs an ending", joined)
        self.assertEqual(outcome.exit_reason, "quit")


class PauseAndResumeTests(unittest.TestCase):
    """A save is a pause: the case resumes into the rolls it would have had."""

    def test_a_case_saved_mid_morning_resumes_into_the_same_ending(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            uninterrupted, _ = _play(
                [*INVESTIGATE, "resolve closed_by_evidence"], seed=77, save_to=path
            )
            first, _ = _play(
                INVESTIGATE[:6], seed=77, save_to=path, resume=False
            )  # two scenes, then end of input
            self.assertFalse(_s(first).finished)
            resumed, transcript = _play(
                [*INVESTIGATE[6:], "resolve closed_by_evidence"], save_to=path
            )
        self.assertIn("Resumed from", "\n".join(transcript))
        self.assertEqual(_s(resumed).report(), _s(uninterrupted).report())
        self.assertEqual(
            _s(resumed).campaign.to_dict(), _s(uninterrupted).campaign.to_dict()
        )

    def test_an_unseeded_morning_is_reproducible_from_its_save(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            uninterrupted, _ = _play(
                [*INVESTIGATE, "resolve closed_by_evidence"], save_to=path
            )
            _play(INVESTIGATE[:9], save_to=path, resume=False)
            resumed, _ = _play([*INVESTIGATE[9:], "resolve closed_by_evidence"], save_to=path)
        self.assertEqual(_s(resumed).report(), _s(uninterrupted).report())
        self.assertEqual(_s(resumed).report()["seed"], _s(uninterrupted).report()["seed"])

    def test_the_same_seed_and_commands_replay_to_the_same_transcript(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            first, first_transcript = _play(
                [*INVESTIGATE, "resolve 2 pressure"], seed=461, save_to=path, resume=False
            )
            second, second_transcript = _play(
                [*INVESTIGATE, "resolve 2 pressure"], seed=461, save_to=path, resume=False
            )
        self.assertEqual(first_transcript, second_transcript)
        self.assertEqual(_s(first).events, _s(second).events)
        self.assertEqual(_s(first).report(), _s(second).report())

    def test_a_finished_case_reopens_as_its_ending(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            _play([*INVESTIGATE, "resolve closed_by_evidence"], seed=461, save_to=path)
            reopened, transcript = _play([], save_to=path)
        self.assertEqual(reopened.exit_reason, "ended")
        self.assertTrue(_s(reopened).finished)
        self.assertIn("Persisted in the campaign", "\n".join(transcript))
        self.assertIn("Resolution: closed_by_evidence", "\n".join(transcript))


class ExitTests(unittest.TestCase):
    """Leaving is not a crash: quit and end-of-input both save."""

    def test_quit_saves_the_morning_where_it_stopped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            outcome, transcript = _play(
                ["act harri read_the_duty_log", "act pc 2", "quit"], seed=461, save_to=path
            )
            self.assertEqual(outcome.exit_reason, "quit")
            self.assertTrue(path.exists())
            restored = load_session(path, kallio.CASE)
        self.assertEqual(restored.clues, _s(outcome).clues)
        self.assertEqual(restored.turn, _s(outcome).turn)
        self.assertIn("saved to", "\n".join(transcript))

    def test_end_of_input_saves_and_returns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            outcome, transcript = _play(["act harri 1"], seed=461, save_to=path)
            self.assertEqual(outcome.exit_reason, "eof")
            self.assertTrue(path.exists())
            restored = load_session(path, kallio.CASE)
        self.assertEqual(restored.clues, ("raid-log",))
        self.assertIn("End of input", "\n".join(transcript))

    def test_leaving_before_acting_still_writes_the_save_file(self) -> None:
        # Nothing has been autosaved yet: the file exists only because leaving saves.
        for command in ("quit",):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "case.json"
                outcome, _ = _play([command], seed=461, save_to=path)
                self.assertEqual(outcome.exit_reason, "quit")
                self.assertTrue(path.exists())
                self.assertEqual(load_session(path, kallio.CASE).clues, ())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            outcome, _ = _play([], seed=461, save_to=path)  # immediate end of input
            self.assertEqual(outcome.exit_reason, "eof")
            self.assertTrue(path.exists())
            self.assertEqual(load_session(path, kallio.CASE).turn, 0)

    def test_end_of_input_at_the_approach_prompt_also_saves(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            outcome, _ = _play([*INVESTIGATE, "resolve 2"], seed=461, save_to=path)
            self.assertEqual(outcome.exit_reason, "eof")
            self.assertFalse(_s(outcome).finished)
            restored = load_session(path, kallio.CASE)
        self.assertIn("finding-empty-sleeve", restored.findings)

    def test_a_foreign_save_is_refused_as_a_save(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            path.write_text('{"schema_version": "case-session-99"}', encoding="utf-8")
            outcome, transcript = _play(["quit"], save_to=path)
        self.assertEqual(outcome.exit_reason, "refused")
        self.assertIn("case refused", "\n".join(transcript))


class HeadlessPathTests(unittest.TestCase):
    """The headless path is still the demo, and the entrypoint still reaches both modes."""

    def test_the_headless_entrypoint_prints_the_demo_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = main(["--json", "--route", "confront", "--seed", "2", "--save", str(path)])
            printed = json.loads(buffer.getvalue())
            expected = run_demo("confront", seed=2, save_to=path)
        self.assertEqual(code, 0)
        self.assertEqual(printed, expected)

    def test_the_headless_text_run_still_reports_what_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = main(["--route", "refer", "--save", str(Path(directory) / "c.json")])
        self.assertEqual(code, 0)
        text = buffer.getvalue()
        self.assertIn("Persisted in the campaign", text)
        self.assertIn("Resolution: closed_by_withdrawal", text)

    def test_play_mode_is_reachable_from_the_module_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            buffer = io.StringIO()
            with mock.patch("sys.stdin", io.StringIO("act pc 1\nquit\n")), contextlib.redirect_stdout(
                buffer
            ):
                code = main(["--play", "--seed", "461", "--save", str(path)])
            self.assertEqual(code, 0)
            self.assertIn("What can be attempted", buffer.getvalue())
            self.assertTrue(path.exists())
            self.assertIn("raid-log", load_session(path, kallio.CASE).clues)

    def test_play_mode_refuses_json_because_it_writes_a_transcript(self) -> None:
        # One stream cannot carry both a played transcript and one JSON document.
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(["--play", "--json"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
