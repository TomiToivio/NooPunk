"""Behavior tests for the live Ubiquitous Maniacs scenario adapter.

Tests exercise executable scenario/runtime integration only, not lore wording.
"""
import tempfile
import unittest
from pathlib import Path

from strategy_game.casework.session import load_session
from strategy_game.casework.ubiquitous_maniacs import CASE, CASE_ID, build_session


class UbiquitousManiacsRuntimeTests(unittest.TestCase):
    def test_playable_session_uses_current_casework(self):
        session = build_session(seed=12)
        self.assertEqual(session.spec.id, CASE_ID)
        self.assertEqual(session.campaign.cases[CASE_ID].case_id, CASE_ID)
        first = session.act("pc_leader", "inspect_register")
        self.assertTrue(first.ok)
        self.assertIn("register", session.clues)
        session.end_scene()
        self.assertTrue(session.act("harri_romppainen", "compare_traces").ok)
        self.assertTrue(session.act("laura_falk", "interview_patient").ok)
        self.assertTrue(session.assemble("finding-ward").ok)
        outcome = session.resolve("closed_by_evidence")
        self.assertIsNotNone(outcome.applied)
        self.assertTrue(session.finished)
        self.assertTrue(session.resolve("closed_by_evidence").idempotent)

    def test_save_resume_and_referral(self):
        session = build_session(seed=13)
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "case.json"
            session.act("pc_leader", "question_orderly")
            session.save(target)
            resumed = load_session(target, CASE)
            self.assertEqual(resumed.clues, session.clues)
            self.assertEqual(resumed.scene_spec.id, session.scene_spec.id)
            resumed.end_scene()
            self.assertIsNotNone(resumed.resolve("closed_by_withdrawal").applied)
            self.assertTrue(resumed.finished)


if __name__ == "__main__":
    unittest.main()
