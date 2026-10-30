"""Contract test: `data/rules/noopunk_tags.json` vs `src/rules/noopunk_tags.py` (#821).

The JSON is what the Godot kernel reads; the Python module is the layer of record. If they disagree,
the tabletop text, the engine and the tests are describing three different games.
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from src.rules import noopunk_tags as tags

CONTRACT = json.loads((Path(__file__).resolve().parents[1] / "data" / "rules" / "noopunk_tags.json").read_text(encoding="utf-8"))


class AttributeContractTest(unittest.TestCase):
    def test_the_attribute_order_matches(self) -> None:
        self.assertEqual(tuple(CONTRACT["attributes"]["order"]), tags.ATTRIBUTES)

    def test_every_attribute_has_a_meaning(self) -> None:
        for name in tags.ATTRIBUTES:
            self.assertTrue(CONTRACT["attributes"]["meaning"].get(name), name)

    def test_the_bands_match_the_module(self) -> None:
        self.assertEqual(tuple(tuple(b) for b in CONTRACT["attributes"]["generation"]["bands"]), tags.BANDS)

    def test_the_generation_is_three_d_six_and_stores_the_modifier(self) -> None:
        self.assertEqual(CONTRACT["attributes"]["generation"]["dice"], "3d6")
        self.assertEqual(CONTRACT["attributes"]["generation"]["store"], "modifier")

    def test_the_ranges_match(self) -> None:
        self.assertEqual(tuple(CONTRACT["attributes"]["human_range"]), (tags.HUMAN_MIN, tags.HUMAN_MAX))
        self.assertEqual(CONTRACT["attributes"]["storage_range"]["min"], tags.STORE_MIN)
        self.assertEqual(CONTRACT["attributes"]["storage_range"]["max"], tags.STORE_MAX)
        self.assertEqual(CONTRACT["attributes"]["empathy_floor"]["value"], tags.EMPATHY_FLOOR)
        self.assertFalse(CONTRACT["attributes"]["empathy_floor"]["pc_eligible"])


class SkillContractTest(unittest.TestCase):
    def test_the_skill_scale_is_zero_to_four(self) -> None:
        self.assertEqual(CONTRACT["skills"]["scale"], [0, tags.SKILL_MAX])

    def test_the_untrained_penalty_matches(self) -> None:
        self.assertEqual(CONTRACT["skills"]["untrained"]["penalty"], tags.UNTRAINED)

    def test_every_skill_is_known_to_the_module(self) -> None:
        for name in CONTRACT["skills"]["list"]:
            tags.skill_tag(name, 0)  # raises if the module disagrees with the contract

    def test_talk_is_one_contextual_skill(self) -> None:
        talk = CONTRACT["skills"]["list"]["Talk"]
        self.assertEqual(talk["attribute"], "contextual")
        self.assertEqual(talk["attribute_options"], ["Empathy", "Agency"])

    def test_renamed_skills_keep_their_cwn_alias(self) -> None:
        renamed = {"Unarmed": "Punch", "Melee": "Stab", "Firearms": "Shoot",
                   "Strength": "Exert", "Stamina": "Exert", "Hardware": "Fix",
                   "Wetware": "Heal", "Software": "Program", "Research": "Know"}
        for modern, legacy in renamed.items():
            self.assertEqual(CONTRACT["skills"]["list"][modern]["cwn"], legacy, modern)

    def test_strength_is_a_skill_not_an_attribute(self) -> None:
        self.assertIn("Strength", CONTRACT["skills"]["list"])
        self.assertNotIn("Strength", tags.ATTRIBUTES)


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

    def test_migration_awaits_a_ruling(self) -> None:
        self.assertEqual(CONTRACT["migration_from_cwn"]["status"], "awaiting_author_ruling")

    def test_the_six_stat_conflict_is_recorded(self) -> None:
        self.assertTrue(any("six STATs" in question for question in CONTRACT["open_questions"]))


if __name__ == "__main__":
    unittest.main()
