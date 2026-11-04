"""The Goal tag through the reference console (#1119): the same facts on paper, in a save, and in play.

The console is the thin interface the issue asks for "if already available": four verbs, no rules. The
lifecycle lives in `rules.goals`, the XP level comes from `cwn_advancement`, and this file only checks
that the seam actually carries the state — including a save written before goals existed.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from console.play import run_command
from console.session import CaseSession, load_session, save_session
from rules.investigation import Investigator, load_case_graph

CASE = ROOT / "data" / "scenarios" / "lakkahaltia" / "case_graph.json"


def make_session() -> CaseSession:
    graph = load_case_graph(CASE)
    return CaseSession.start(graph, Investigator(name="Romppainen", ratings={"Notice": 1}), seed=7)


def run(session: CaseSession, line: str) -> str:
    return run_command(session, line)[1]


class ConsoleVerbTests(unittest.TestCase):
    def test_the_short_goal_lifecycle_runs_through_four_verbs(self):
        session = make_session()
        self.assertIn("goal-1", run(session, "goal romppainen short Arrest Roy Batty"))
        self.assertIn("completed", run(
            session, "progress goal-1 completed case:lakkahaltia custody established"))
        self.assertIn("awarded 1 XP", run(session, "award goal-1 case:lakkahaltia"))
        self.assertIn("no active goals", run(session, "goals"))
        self.assertEqual(session.goals_view()["xp"]["romppainen"], 1)

    def test_the_paper_line_is_what_the_console_prints(self):
        session = make_session()
        run(session, "goal romppainen medium Get a Promotion")
        printed = run(session, "goals")
        self.assertIn("Goal: Get a Promotion | owner: romppainen | horizon: medium "
                      "| status: in progress", printed)

    def test_a_faction_goal_is_refused_character_xp_and_says_why(self):
        session = make_session()
        run(session, "goal faction:unsa medium Secure a mandate")
        run(session, "progress goal-1 completed board:2026-11-04")
        refused = run(session, "award goal-1 board:2026-11-04")
        self.assertIn("refused", refused)
        self.assertIn("faction rewards are assets", refused)
        self.assertEqual(session.goals_view()["xp"]["unsa"], 0)

    def test_a_second_award_for_the_same_event_is_refused(self):
        session = make_session()
        run(session, "goal romppainen short Arrest Roy Batty")
        run(session, "progress goal-1 completed case:1")
        run(session, "award goal-1 case:1")
        self.assertIn("already been paid", run(session, "award goal-1 case:1"))

    def test_a_bad_horizon_is_refused_rather_than_guessed(self):
        session = make_session()
        self.assertIn("refused", run(session, "goal romppainen epic Prevent Extinction"))

    def test_the_goal_verbs_are_offered_to_an_agent_too(self):
        from console.agent import VERBS

        for verb in ("goal", "goals", "progress", "award"):
            self.assertIn(verb, VERBS)


class SaveTests(unittest.TestCase):
    def test_goals_survive_a_save_and_a_load(self):
        session = make_session()
        run(session, "goal romppainen short Arrest Roy Batty")
        run(session, "progress goal-1 completed case:1 custody")
        run(session, "award goal-1 case:1")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            save_session(session, path)
            restored = load_session(load_case_graph(CASE), path)
        self.assertEqual(restored.goals.to_dict(), session.goals.to_dict())
        self.assertEqual(restored.goals.paper("goal-1"), session.goals.paper("goal-1"))
        self.assertEqual(restored.goals_view()["xp"]["romppainen"], 1)

    def test_a_save_written_before_goals_existed_still_loads(self):
        session = make_session()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "old.json"
            save_session(session, path)
            data = json.loads(path.read_text(encoding="utf-8"))
            data.pop("goals", None)          # exactly what a v1 save looks like
            path.write_text(json.dumps(data), encoding="utf-8")
            restored = load_session(load_case_graph(CASE), path)
        self.assertEqual(restored.goals_view()["active"], [])
        self.assertEqual(restored.goals.to_dict()["goals"], [])

    def test_goals_do_not_disturb_the_case_state(self):
        plain, goaly = make_session(), make_session()
        run(goaly, "goal romppainen short Arrest Roy Batty")
        run(goaly, "progress goal-1 completed case:1")
        for key in ("scene", "discovered", "evidence", "theory", "concluded"):
            self.assertEqual(plain.to_dict()[key], goaly.to_dict()[key],
                             f"a goal tag must not touch {key}")


if __name__ == "__main__":
    unittest.main()
