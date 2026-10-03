"""Issue #74 proof-of-concept scenario tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from text_game.actions import parse_command
from text_game.engine import GameEngine
from text_game.issue74 import ANALYST_ID, HUMAN_ID, SIGNAL_ID, TECHNICIAN_ID, issue74_world


class Issue74ScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = GameEngine(world=issue74_world())

    def run_cmd(self, raw: str):
        return self.engine.execute(parse_command(HUMAN_ID, raw))

    def test_scenario_is_deliberately_bounded(self) -> None:
        self.assertEqual(len(self.engine.world.rooms), 1)
        self.assertEqual(len(self.engine.world.actors), 3)

    def test_player_has_ep2_derived_resolution_sheet(self) -> None:
        sheet = self.engine.world.actors[HUMAN_ID].sheet
        self.assertIsNotNone(sheet)
        self.assertIn("Perceive", sheet["skills"])
        self.assertIn("Interface", sheet["skills"])
        self.assertIn("Persuade", sheet["skills"])

    def test_llm_and_scripted_npcs_coexist(self) -> None:
        self.assertEqual(self.engine.world.actors[ANALYST_ID].controller, "llm")
        self.assertEqual(self.engine.world.actors[TECHNICIAN_ID].controller, "scripted")

    def test_investigation_and_mesh_checks_use_existing_kernel(self) -> None:
        investigation = self.run_cmd("test skill Perceive roll 40")
        mesh = self.run_cmd("test skill Interface roll 40")
        self.assertIn("success", investigation.text)
        self.assertIn("success", mesh.text)

    def test_social_contest_uses_existing_kernel(self) -> None:
        result = self.run_cmd("test social Persuade vs analyst roll 20")
        self.assertIn("social:", result.text)

    def test_objective_can_complete_without_llm(self) -> None:
        result = self.run_cmd("take signal-record")
        self.assertTrue(result.completed)
        self.assertIn(SIGNAL_ID, self.engine.world.actors[HUMAN_ID].inventory)


if __name__ == "__main__":
    unittest.main()
