"""Contract test: `data/rules/noopunk_tags.json` vs `src/rules/noopunk_tags.py` (#821).

The JSON is what the Godot kernel reads; the Python module is the layer of record. If they disagree,
the tabletop text, the engine and the tests describe three different games.
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from src.rules import noopunk_tags as tags

CONTRACT = json.loads(
    (Path(__file__).resolve().parents[1] / "data" / "rules" / "noopunk_tags.json").read_text(encoding="utf-8")
)


class AttributeContractTest(unittest.TestCase):
    def test_the_attribute_order_matches(self) -> None:
        self.assertEqual(tuple(CONTRACT["attributes"]["order"]), tags.ATTRIBUTES)

    def test_every_attribute_has_a_meaning(self) -> None:
        for name in tags.ATTRIBUTES:
            self.assertTrue(CONTRACT["attributes"]["meaning"].get(name), name)

    def test_the_bands_match_the_module(self) -> None:
        # The module keeps inclusive (low, high, modifier) triples; the contract keeps lower bounds.
        from_contract = [(low, value) for low, value in CONTRACT["attributes"]["generation"]["bands"]]
        from_module = [(low, modifier) for low, _high, modifier in tags.ROLL_BANDS]
        self.assertEqual(from_contract, from_module)

    def test_the_generation_is_three_d_six_and_stores_the_modifier(self) -> None:
        self.assertEqual(CONTRACT["attributes"]["generation"]["dice"], "3d6")
        self.assertEqual(CONTRACT["attributes"]["generation"]["store"], "modifier")

    def test_the_ranges_match(self) -> None:
        self.assertEqual(tuple(CONTRACT["attributes"]["human_range"]),
                         (tags.ATTRIBUTE_MIN, tags.ATTRIBUTE_MAX_HUMAN))
        self.assertEqual(CONTRACT["attributes"]["empathy_floor"]["value"], tags.EMPATHY_FLOOR)
        self.assertFalse(CONTRACT["attributes"]["empathy_floor"]["pc_eligible"])

    def test_the_storage_floor_matches(self) -> None:
        self.assertEqual(CONTRACT["attributes"]["storage_range"]["min"], tags.EMPATHY_FLOOR)


class SkillContractTest(unittest.TestCase):
    def test_every_contract_skill_exists_in_the_module(self) -> None:
        self.assertEqual(sorted(CONTRACT["skills"]["list"]), sorted(tags.SKILLS))

    def test_the_scale_and_untrained_rule_match(self) -> None:
        self.assertEqual(CONTRACT["skills"]["scale"][1], tags.SKILL_MAX)
        self.assertEqual(CONTRACT["skills"]["untrained"]["penalty"], tags.UNTRAINED)
        self.assertEqual(tuple(CONTRACT["skills"]["untrained"]["impossible_without"]),
                         tags.IMPOSSIBLE_UNTRAINED)

    def test_the_default_attributes_match(self) -> None:
        for name, entry in CONTRACT["skills"]["list"].items():
            self.assertEqual(entry["attribute"], tags.SKILLS[name]["attribute"], name)

    def test_the_cwn_relationships_match(self) -> None:
        for name, entry in CONTRACT["skills"]["list"].items():
            self.assertEqual(entry["cwn"], tags.SKILLS[name]["cwn"], name)

    def test_talk_is_one_contextual_skill(self) -> None:
        talk = CONTRACT["skills"]["list"]["Talk"]
        self.assertEqual(talk["attribute"], "contextual")
        self.assertEqual(tuple(talk["attribute_options"]), tags.SKILLS["Talk"]["options"])

    def test_strength_is_a_skill_not_an_attribute(self) -> None:
        self.assertIn("Strength", tags.SKILLS)
        self.assertNotIn("Strength", tags.ATTRIBUTES)


class TagModelContractTest(unittest.TestCase):
    def test_the_kinds_match(self) -> None:
        self.assertEqual(sorted(CONTRACT["tags"]["kinds"]),
                         sorted(kind.value for kind in tags.TagType))

    def test_the_duration_and_stacking_modes_are_the_ones_the_module_understands(self) -> None:
        self.assertIn("permanent", CONTRACT["tags"]["duration"])
        self.assertEqual(sorted(CONTRACT["tags"]["stacking"]), ["highest", "replace", "stack"])


class UndecidedTest(unittest.TestCase):
    def test_the_open_questions_are_carried(self) -> None:
        questions = CONTRACT["open_questions"]
        self.assertGreaterEqual(len(questions), 6)
        joined = " ".join(questions)
        for topic in ("impossible", "Connect", "Work", "Empathy", "migrat", "six STATs"):
            self.assertIn(topic, joined, topic)

    def test_undecided_skills_have_no_invented_attribute(self) -> None:
        for name in ("Know", "Work"):
            self.assertIsNone(CONTRACT["skills"]["list"][name]["attribute"], name)
            self.assertIsNone(tags.SKILLS[name]["attribute"], name)

    def test_migration_awaits_a_ruling(self) -> None:
        self.assertEqual(CONTRACT["migration_from_cwn"]["status"], "awaiting_author_ruling")

    def test_the_six_stat_conflict_is_recorded(self) -> None:
        self.assertTrue(any("six STATs" in question for question in CONTRACT["open_questions"]))


if __name__ == "__main__":
    unittest.main()
