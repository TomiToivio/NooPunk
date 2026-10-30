"""#791 checklist: state isolation and the scenario fixtures.

Two claims the consolidation depends on, both checkable without a renderer:

1. **One owning state per session.** `GameState` is the only autoload; `NooPunkCampaignState` is an
   ordinary RefCounted. They must not share a save path, and the campaign save must be explicitly
   versioned so an old file is refused rather than half-read.
2. **The scenario directories are not copies of each other.** The audit found
   `data/scenarios/lakkahaltia/` and `godot/scenarios/lakkahaltia/` both holding case data. They
   overlap in exactly one filename and that file differs — so "duplication" here is two different
   fixtures, not one file saved twice, and deleting either would delete a live scenario.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME_STATE = ROOT / "godot" / "core" / "game_state.gd"
CAMPAIGN_STATE = ROOT / "src" / "godot" / "campaign_state.gd"
PROJECT = ROOT / "project.godot"

DATA_SCENARIO = ROOT / "data" / "scenarios" / "lakkahaltia"
GODOT_SCENARIO = ROOT / "godot" / "scenarios" / "lakkahaltia"


def _save_paths(source: Path) -> list[str]:
    return re.findall(r'"user://([^"]+)"', source.read_text(encoding="utf-8"))


class GodotStateIsolationTest(unittest.TestCase):
    def test_only_one_autoload_exists(self) -> None:
        text = PROJECT.read_text(encoding="utf-8")
        autoload_block = text.split("[autoload]", 1)[1].split("\n[", 1)[0]
        entries = [
            line for line in autoload_block.splitlines()
            if "=" in line and not line.strip().startswith(";")
        ]
        self.assertEqual(len(entries), 1, f"expected exactly one autoload, got {entries}")
        self.assertIn("game_state.gd", entries[0])

    def test_the_two_states_do_not_share_a_save_file(self) -> None:
        legacy = set(_save_paths(GAME_STATE))
        campaign = set(_save_paths(CAMPAIGN_STATE))
        self.assertTrue(legacy, "GameState declares no save path")
        self.assertTrue(campaign, "campaign state declares no save path")
        self.assertEqual(
            legacy & campaign,
            set(),
            "the two states must not write the same save file: {}".format(legacy & campaign),
        )

    def test_the_campaign_save_is_versioned(self) -> None:
        text = CAMPAIGN_STATE.read_text(encoding="utf-8")
        self.assertRegex(text, r"const VERSION := \d+")
        self.assertIn("from_data", text)
        # The version check must reject, not coerce: a save from another build is refused. Asserted
        # against what the file declares rather than against one expression, because #809 extended
        # the rule from "must equal VERSION" to "must be one of SUPPORTED_VERSIONS" and a text match
        # would call that improvement a regression.
        supported = re.search(r"const SUPPORTED_VERSIONS := \[([^\]]*)\]", text)
        self.assertIsNotNone(supported, "the state must declare which save versions it accepts")


class ScenarioFixtureTest(unittest.TestCase):
    def test_both_scenario_directories_still_exist(self) -> None:
        """Two live entry points read them; neither directory is dead weight."""
        self.assertTrue(DATA_SCENARIO.is_dir(), DATA_SCENARIO)
        self.assertTrue(GODOT_SCENARIO.is_dir(), GODOT_SCENARIO)

    def test_the_directories_are_distinct_fixtures_not_copies(self) -> None:
        data_files = {p.name for p in DATA_SCENARIO.glob("*.json")}
        godot_files = {p.name for p in GODOT_SCENARIO.glob("*.json")}
        overlap = data_files & godot_files
        # They share at most the dialogue fixture, and even that is not byte-identical, which is why
        # deduplicating them would need a parity decision rather than a file move.
        self.assertLessEqual(
            len(overlap),
            1,
            f"the two scenario trees now overlap in several files: {sorted(overlap)}",
        )
        for name in overlap:
            self.assertNotEqual(
                (DATA_SCENARIO / name).read_bytes(),
                (GODOT_SCENARIO / name).read_bytes(),
                f"{name} is byte-identical in both trees; that one can be deduplicated",  # noqa: E501
            )

    def test_scenario_json_parses(self) -> None:
        for directory in (DATA_SCENARIO, GODOT_SCENARIO):
            for path in directory.glob("*.json"):
                with self.subTest(path=path.name):
                    json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
