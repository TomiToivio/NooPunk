from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from text_game.actions import parse_command
from text_game.engine import GameEngine
from text_game.model import World
from text_game.prefall import (
    HUMAN_ID,
    MARS_ARCHIVE_ID,
    SCENARIO_PREFIX,
    SETI_ANALYST_ID,
    STARGATE_ANALYST_ID,
    prefall_world,
)


class Issue60PrefallScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = prefall_world()
        self.engine = GameEngine(self.world)

    def test_scenario_is_canonical_not_fixture_data(self) -> None:
        ids = (
            list(self.world.rooms)
            + list(self.world.items)
            + list(self.world.actors)
            + [self.world.adventure.adventure_id]
        )
        self.assertTrue(all(x.startswith(SCENARIO_PREFIX) for x in ids))
        self.assertTrue(all(not x.startswith("fixture:") for x in ids))

    def test_world_carries_author_specified_prefall_facts(self) -> None:
        text = " ".join(
            [room.description for room in self.world.rooms.values()]
            + [item.description for item in self.world.items.values()]
        ).casefold()
        for phrase in (
            "earth still exists",
            "20xx",
            "seventh detected extraterrestrial civilization",
            "five civilizations were contacted on earth",
            "sixth",
            "ancient martian ruins",
            "mars eldrich",
            "crash-retrieval",
            "zookeepers",
            "billions of years ago",
            "warp drives",
            "noetics",
            "plasmoids",
            "constructs",
            "no consensus",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_first_contact_count_is_not_inflated_by_disputed_categories(self) -> None:
        earth = next(room for room in self.world.rooms.values() if "SETI" in room.label)
        text = earth.description.casefold()
        self.assertIn("five civilizations were contacted on earth", text)
        self.assertIn("sixth", text)
        self.assertIn("seventh", text)
        dossier = next(item for item in self.world.items.values() if "classification" in item.label)
        self.assertIn("no consensus", dossier.description.casefold())

    def test_scenario_has_player_and_multiple_llm_capable_contacts(self) -> None:
        self.assertEqual(self.world.actors[HUMAN_ID].controller, "human")
        self.assertEqual(self.world.actors[SETI_ANALYST_ID].controller, "scripted")
        self.assertEqual(self.world.actors[STARGATE_ANALYST_ID].controller, "llm")
        self.assertEqual(self.world.actors[MARS_ARCHIVE_ID].controller, "llm")
        self.assertTrue(all(actor.sheet for actor in self.world.actors.values()))

    def test_character_sheet_and_seeded_roll_path_are_playable(self) -> None:
        sheet = self.engine.execute(parse_command(HUMAN_ID, "sheet"))
        self.assertIn("Sheet: Player", sheet.text)
        result = self.engine.execute(
            parse_command(HUMAN_ID, "test skill Perceive roll 40")
        )
        self.assertIn("roll 40", result.text)
        self.assertIn("success", result.text)

    def test_taking_seti_record_completes_vertical_slice(self) -> None:
        result = self.engine.execute(parse_command(HUMAN_ID, "take SETI signal record"))
        self.assertTrue(result.completed)
        self.assertEqual(self.world.adventure.completed_by, HUMAN_ID)
        self.assertIn("Adventure complete.", result.text)

    def test_world_round_trip_preserves_scenario_and_sheets(self) -> None:
        restored = World.from_dict(self.world.to_dict())
        self.assertEqual(restored.adventure.adventure_id, self.world.adventure.adventure_id)
        self.assertEqual(restored.actors[HUMAN_ID].sheet, self.world.actors[HUMAN_ID].sheet)
        self.assertEqual(
            restored.rooms[SCENARIO_PREFIX + "stargate-survey"].description,
            self.world.rooms[SCENARIO_PREFIX + "stargate-survey"].description,
        )


if __name__ == "__main__":
    unittest.main()
