"""The console slice behind #1053 and #1054: a case that can be finished, replayed and saved.

These are code tests in the sense of AGENTS.md: they drive executable Python through the rules
module and assert behaviour (which scene is reachable, what the dice did, what a save restores).
Nothing here reads a Markdown file or matches rulebook prose.

The properties that matter, because each of them is a way a "playable slice" quietly stops being one:

* the whole case can be played to a conclusion from a script, on every scene;
* the same seed and the same commands produce the same run, byte for byte;
* a save resumes exactly where it left off -- including the dice stream;
* the console never announces that a theory is correct;
* the rules are imported from `rules.investigation`, not re-implemented behind the UI.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from console import session as session_module  # noqa: E402
from console.play import build_session, run_command  # noqa: E402
from console.session import CaseSession, SessionError  # noqa: E402
from rules import investigation  # noqa: E402
from rules.investigation import Investigator, load_case_graph  # noqa: E402

CASE = ROOT / "data" / "scenarios" / "lakkahaltia" / "case_graph.json"
WALKTHROUGH = ROOT / "docs" / "examples" / "lakkahaltia_walkthrough.txt"
SCRIPT = [line for line in WALKTHROUGH.read_text(encoding="utf-8").splitlines()
          if line.strip() and not line.strip().startswith("#")]


def make_session(seed: int = 7) -> CaseSession:
    graph = load_case_graph(CASE)
    investigator = Investigator(name="Test Investigator",
                                ratings={"Notice": 1, "Talk": 1, "Administer": 1,
                                         "Survive": 0, "Heal": 0, "Know": 0, "Connect": 0})
    return CaseSession.start(graph, investigator, seed=seed)


def play(session: CaseSession, commands) -> list[str]:
    output = []
    for command in commands:
        keep_going, text = run_command(session, command)
        output.append(text)
        if not keep_going:
            break
    return output


class PlaythroughTests(unittest.TestCase):
    def test_the_whole_case_is_playable_to_a_conclusion(self) -> None:
        session = make_session()
        play(session, SCRIPT)
        self.assertTrue(session.concluded, "the walkthrough did not conclude the case")
        self.assertTrue(session.conclusion, "no conclusion recorded")
        # The walkthrough is the whole graph, not a corner of it.
        self.assertEqual(len(set(session.visited)), len(session.graph.case.scenes))
        self.assertGreaterEqual(len(session.discovered), 8)

    def test_dice_are_actually_rolled(self) -> None:
        session = make_session()
        play(session, SCRIPT)
        rolls = [event for event in session.events if event["kind"] == "risk"]
        self.assertTrue(rolls, "the walkthrough never exercises a check")
        for roll in rolls:
            self.assertTrue(all(1 <= die <= 6 for die in roll["dice"]))
            self.assertEqual(roll["total"], sum(roll["dice"]) + roll["rank"])

    def test_same_seed_and_commands_replay_identically(self) -> None:
        first, second = make_session(seed=11), make_session(seed=11)
        play(first, SCRIPT)
        play(second, SCRIPT)
        self.assertEqual(first.to_dict(), second.to_dict())

    def test_a_different_seed_moves_the_dice_but_not_the_clues(self) -> None:
        first, second = make_session(seed=1), make_session(seed=2)
        play(first, SCRIPT)
        play(second, SCRIPT)
        self.assertEqual(first.discovered, second.discovered)
        self.assertNotEqual(
            [event for event in first.events if event["kind"] == "risk"],
            [event for event in second.events if event["kind"] == "risk"],
            "two seeds produced identical dice, so the seed is not reaching the generator")


class SaveLoadTests(unittest.TestCase):
    def test_a_save_resumes_exactly_where_it_left_off(self) -> None:
        uninterrupted = make_session(seed=5)
        play(uninterrupted, SCRIPT)

        split = make_session(seed=5)
        play(split, SCRIPT[:8])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "case-save.json"
            split.save(path)
            resumed = session_module.load_session(load_case_graph(CASE), path)
            play(resumed, SCRIPT[8:])

        self.assertEqual(resumed.to_dict(), uninterrupted.to_dict(),
                         "a resumed session diverged from the same commands without a save")

    def test_the_dice_stream_survives_a_save(self) -> None:
        split = make_session(seed=3)
        play(split, SCRIPT[:3])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "case-save.json"
            split.save(path)
            resumed = session_module.load_session(load_case_graph(CASE), path)
        first, second = split.risk(8, "Notice"), resumed.risk(8, "Notice")
        self.assertEqual(first, second)

    def test_an_unknown_state_version_is_refused(self) -> None:
        data = make_session().to_dict()
        data["state_version"] = 99
        with self.assertRaises(SessionError):
            CaseSession.from_dict(load_case_graph(CASE), data)

    def test_a_save_from_another_case_is_refused(self) -> None:
        data = make_session().to_dict()
        data["case_id"] = "some-other-case"
        with self.assertRaises(SessionError):
            CaseSession.from_dict(load_case_graph(CASE), data)

    def test_a_truncated_save_is_refused_with_a_message(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(SessionError):
                session_module.load_session(load_case_graph(CASE), path)


class RuleBoundaryTests(unittest.TestCase):
    def test_the_console_uses_the_rules_module_rather_than_a_copy(self) -> None:
        self.assertIs(session_module.discover, investigation.discover,
                      "the console must import discovery, not reimplement it")

    def test_an_unknown_scene_is_refused(self) -> None:
        session = make_session()
        with self.assertRaises(SessionError):
            session.travel("no-such-scene")

    def test_a_scene_without_a_discovered_lead_is_refused(self) -> None:
        session = make_session()
        session.discovered.clear()
        with self.assertRaises(SessionError):
            session.travel("patient_room")

    def test_reading_a_clue_that_was_not_found_is_refused(self) -> None:
        session = make_session()
        session.choose_theory("mundane_records_error")
        with self.assertRaises(SessionError):
            session.attach("mundane_records_error", "record-1601", "supports")

    def test_no_competency_means_no_sheet(self) -> None:
        graph = load_case_graph(CASE)
        with self.assertRaises(SessionError):
            CaseSession.start(graph, Investigator(name="Nobody", ratings={}))

    def test_concluding_records_the_answer_and_refuses_to_grade_it(self) -> None:
        session = make_session()
        play(session, SCRIPT)
        conclusion = session.conclusion
        self.assertFalse(conclusion["case_solved_by_program"])
        self.assertIn("does not decide the truth", conclusion["verdict"])
        self.assertTrue(investigation.hypotheses_remain_open(session.graph.hypotheses))

    def test_a_conclusion_with_no_evidence_is_still_a_legal_state(self) -> None:
        session = make_session()
        result = session.conclude("anomalous_visitor", "played blind")
        self.assertEqual(result["supports"], 0)
        self.assertTrue(session.concluded)

    def test_the_console_does_not_pull_in_a_game_engine(self) -> None:
        code = ("import sys; import console, console.play; "
                "bad = [name for name in ('evennia', 'pygame', 'concordia') if name in sys.modules]; "
                "print(','.join(bad))")
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                                cwd=str(ROOT), env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "", "the reference console imported an engine")


class CommandLineTests(unittest.TestCase):
    def test_the_scripted_cli_runs_and_saves(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "cli-save.json"
            result = subprocess.run(
                [sys.executable, "scripts/noopunk_case.py", "--seed", "7",
                 "--script", str(WALKTHROUGH), "--save", str(save)],
                capture_output=True, text=True, cwd=str(ROOT),
                env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("NoöPunk case console", result.stdout)
            self.assertIn("recorded:", result.stdout)
            self.assertTrue(save.is_file())
            data = json.loads(save.read_text(encoding="utf-8"))
            self.assertTrue(data["concluded"])

    def test_a_broken_case_file_is_a_clean_error_not_a_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            broken = Path(folder) / "case.json"
            broken.write_text('{"format": "not-a-case"}', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/noopunk_case.py", "--case", str(broken)],
                capture_output=True, text=True, cwd=str(ROOT), input="quit\n",
                env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"})
            self.assertEqual(result.returncode, 2)
            self.assertIn("cannot start", result.stderr)
            self.assertNotIn("Traceback", result.stderr)


class BuildSessionTests(unittest.TestCase):
    def test_the_default_sheet_can_traverse_the_case(self) -> None:
        class Args:
            case = str(CASE)
            load = ""
            seed = 7
            name = "Default Sheet"
            skill: list[str] = []

        session = build_session(Args())
        play(session, SCRIPT)
        self.assertTrue(session.concluded)

    def test_skills_can_be_stated_on_the_command_line(self) -> None:
        class Args:
            case = str(CASE)
            load = ""
            seed = 7
            name = "Specialist"
            skill = ["Notice=3", "Talk=2"]

        session = build_session(Args())
        self.assertEqual(session.investigator.ratings, {"Notice": 3, "Talk": 2})

    def test_rank_zero_counts_as_trained(self) -> None:
        """The Without Number baseline rates skills 0-4 and untrained is *absence*: rank 0 plays."""
        graph = load_case_graph(CASE)
        sheet = Investigator(name="Rank zero", ratings={"Notice": 0, "Talk": 0, "Administer": 0})
        session = CaseSession.start(graph, sheet, seed=1)
        self.assertIn("sign-in-sheet", session.discovered)



class SharedRuleTests(unittest.TestCase):
    """#1054: an adapter may not compute a check. These pin that the console delegates."""

    def test_the_default_attribute_is_the_plus_zero_band(self) -> None:
        roll = make_session().risk(8, "Notice")
        self.assertEqual(roll["attribute"], 10)
        self.assertEqual(roll["attribute_modifier"], 0)
        self.assertEqual(roll["total"], sum(roll["dice"]) + roll["rank"])

    def test_a_named_attribute_contributes_its_cwn_modifier(self) -> None:
        # CWN bands: 14-17 is +1, 3 is -2. Before this parameter the console silently dropped both,
        # which made every check a different rule from the one in the book.
        roll = make_session().risk(8, "Notice", attribute=14)
        self.assertEqual(roll["attribute_modifier"], 1)
        self.assertEqual(roll["total"], sum(roll["dice"]) + roll["rank"] + 1)
        weak = make_session().risk(8, "Notice", attribute=3)
        self.assertEqual(weak["attribute_modifier"], -2)
        self.assertEqual(weak["total"], sum(weak["dice"]) + weak["rank"] - 2)

    def test_an_impossible_attribute_score_is_refused_by_the_shared_rule(self) -> None:
        with self.assertRaises(Exception):
            make_session().risk(8, "Notice", attribute=19)


if __name__ == "__main__":
    unittest.main()
