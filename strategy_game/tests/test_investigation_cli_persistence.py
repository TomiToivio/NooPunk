"""Regression: a completed Fate check is durable before the next input prompt."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from strategy_game.rpg.investigation import Investigation
from strategy_game.rpg.investigation_cli import main


class InvestigationCLIPersistenceTest(unittest.TestCase):
    def test_check_saved_before_next_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_path = Path(tmp) / "case.json"
            # Simulate the process being interrupted before another choice or
            # normal EOF/quit shutdown can save the case.
            with patch("builtins.input", side_effect=[
                "check leader SAV 1 516", KeyboardInterrupt
            ]):
                with self.assertRaises(KeyboardInterrupt):
                    main(["--save", str(save_path)])
            recovered = Investigation.load(save_path)
            self.assertEqual(len(recovered.events), 1)
            self.assertEqual(recovered.events[0]["kind"], "rpg_check")
            self.assertEqual(recovered.events[0]["actor_id"], "leader")

    def test_invalid_check_does_not_create_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_path = Path(tmp) / "case.json"
            with patch("builtins.input", side_effect=[
                "check outsider SAV 1 516", KeyboardInterrupt
            ]):
                with self.assertRaises(KeyboardInterrupt):
                    main(["--save", str(save_path)])
            self.assertFalse(save_path.exists())


if __name__ == "__main__":
    unittest.main()
