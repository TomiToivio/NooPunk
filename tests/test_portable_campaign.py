"""Headless tests; run: python -m unittest discover -s tests -p 'test_portable_campaign.py'."""
import unittest
from portable_noopunk import Game, Action

class PortableCampaignTests(unittest.TestCase):
    def test_case_and_sidequest_and_save_roundtrip(self):
        g = Game()
        self.assertIn("briefing", g.available_actions())
        g.apply(Action("go_library"))
        self.assertIn("sidequest_completed", g.apply(Action("catalogue_record")).events)
        serialized = g.to_json()
        g = Game.from_json(serialized)
        self.assertTrue(g.state.sidequest_done)
        g.apply(Action("go_hq"))
        g.apply(Action("go_hospital"))
        self.assertNotIn("case_completed", g.apply(Action("conclude")).events)
        g.apply(Action("examine_room"))
        g.apply(Action("interview_witness"))
        self.assertIn("case_completed", g.apply(Action("conclude")).events)
        self.assertTrue(Game.from_json(g.to_json()).state.finished)

    def test_repeated_actions_do_not_duplicate_clues(self):
        g = Game()
        g.apply(Action("go_hospital"))
        g.apply(Action("examine_room"))
        g.apply(Action("examine_room"))
        self.assertEqual(g.state.clues, ["anomalous_clock"])

    def test_invalid_state_rejected(self):
        with self.assertRaises(ValueError):
            Game.from_json('{"version":99}')

if __name__ == "__main__":
    unittest.main()
