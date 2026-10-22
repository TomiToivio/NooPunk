"""Regression coverage for the noncanonical RPG-first playtest."""
import unittest

from strategy_game.rpg.investigation import Investigation
from strategy_game.rpg.playtest import TRIALS, run_trials


class PlaytestTest(unittest.TestCase):
    def test_three_playable_cases_are_reproducible(self):
        report = run_trials()
        self.assertEqual(report["status"], "passed")
        self.assertTrue(report["noncanonical"])
        self.assertEqual(len(report["trials"]), 3)
        self.assertEqual([x["name"] for x in report["trials"]], [x[0] for x in TRIALS])
        self.assertEqual(report, run_trials())
        for trial in report["trials"]:
            self.assertTrue(trial["saved_and_reloaded"])
            self.assertEqual(len(trial["participants"]), 5)
            self.assertEqual(len(trial["check"]["dice"]), 4)
            self.assertEqual(len(trial["events"]), 4)
            self.assertEqual(trial["events"][-1]["kind"], "investigation_choice")

    def test_runner_does_not_mutate_default_case(self):
        before = Investigation().to_dict()
        run_trials()
        self.assertEqual(Investigation().to_dict(), before)


if __name__ == "__main__":
    unittest.main()
