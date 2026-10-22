"""Contract tests: both Ubiquitous Maniacs adapters use the RPG launcher."""
import unittest
from unittest.mock import patch

from strategy_game.rpg.__main__ import main


class UbiquitousEntrypointTests(unittest.TestCase):
    def test_current_casework_routing_and_arguments(self):
        with patch("strategy_game.casework.ubiquitous_maniacs_play.main", return_value=0) as runner:
            self.assertEqual(main(["--scenario", "ubiquitous-maniacs-case", "--seed", "23", "--save", "case.json", "--new"]), 0)
            runner.assert_called_once_with(["--seed", "23", "--save", "case.json", "--new"])

    def test_canonical_alias_uses_current_casework(self):
        with patch("strategy_game.casework.ubiquitous_maniacs_play.main", return_value=0) as runner:
            self.assertEqual(main(["--scenario", "ubiquitous-maniacs"]), 0)
            runner.assert_called_once_with(["--seed", str(__import__("strategy_game.rpg.run", fromlist=["DEFAULT_SEED"]).DEFAULT_SEED)])

    def test_original_two_day_adapter_remains_available(self):
        with patch("strategy_game.scenarios.ubiquitous_maniacs_cli.main", return_value=0) as runner:
            self.assertEqual(main(["--scenario", "ubiquitous-maniacs-legacy", "--save", "old.json"]), 0)
            runner.assert_called_once_with(["--save", "old.json"])


if __name__ == "__main__":
    unittest.main()
