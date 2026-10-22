"""End-to-end CLI tests using the real shared NoöPunk RPG entry point."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class UnifiedUbiquitousManiacsTests(unittest.TestCase):
    def test_play_to_completion_and_resume(self):
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "campaign.json"
            cmd = [sys.executable, "-m", "strategy_game.rpg", "--scenario",
                   "ubiquitous-maniacs-legacy", "--save", str(save)]
            run = subprocess.run(cmd, input="check romppainen SAV 1 42\nread_form\nenter_chamber\nretain_record\ncontinue\nfollow_clue\n",
                                 text=True, capture_output=True, timeout=30)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("Scenario complete", run.stdout)
            payload = json.loads(save.read_text(encoding="utf-8"))
            self.assertEqual(payload["stage"], "conclusion")
            self.assertEqual(len(payload["checks"]), 1)
            resumed = subprocess.run(cmd, input="", text=True, capture_output=True, timeout=30)
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            self.assertIn("Scenario complete", resumed.stdout)

    def test_bad_choice_does_not_advance(self):
        with tempfile.TemporaryDirectory() as folder:
            save = Path(folder) / "campaign.json"
            run = subprocess.run(
                [sys.executable, "-m", "strategy_game.rpg", "--scenario", "ubiquitous-maniacs-legacy",
                 "--save", str(save)],
                input="invalid\nquit\n", text=True, capture_output=True, timeout=30)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(save.read_text(encoding="utf-8"))["stage"], "arrival")
            self.assertIn("Not available", run.stdout)


if __name__ == "__main__":
    unittest.main()
