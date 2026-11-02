"""Contract tests for independent headless frontends."""
import unittest
from portable_noopunk import Game, Action
from portable_noopunk.adapters import LocalAdapter

SEQUENCE = ("briefing", "go_library", "catalogue_record", "go_hq",
            "go_hospital", "examine_room", "interview_witness", "conclude")

class AdapterContractTests(unittest.TestCase):
    def test_same_actions_same_results(self):
        direct = Game()
        adapter = LocalAdapter(Game())
        for command in SEQUENCE:
            expected = direct.apply(Action(command))
            actual = adapter.dispatch(command)
            self.assertEqual(expected, actual)
            self.assertEqual(direct.to_json(), adapter.save())
        self.assertTrue(adapter.snapshot()["finished"])

    def test_save_round_trip_and_action_validation(self):
        adapter = LocalAdapter(Game())
        self.assertEqual(adapter.dispatch("conclude").events, ())
        adapter.dispatch("go_hospital")
        saved = adapter.save()
        restored = LocalAdapter.load(saved)
        self.assertEqual(restored.available_actions(), adapter.available_actions())
        self.assertEqual(restored.snapshot(), adapter.snapshot())
        self.assertEqual(restored.dispatch("catalogue_record").events, ())
        self.assertEqual(restored.snapshot()["clues"], [])

    def test_snapshot_is_copy(self):
        a = LocalAdapter(Game())
        snap = a.snapshot()
        snap["clues"].append("fake")
        self.assertEqual(a.snapshot()["clues"], [])

if __name__ == "__main__":
    unittest.main()
