"""NoöPunk tag-based attributes, skills and statuses (#821).

The draft is Tomi's; these tests check that the implementation honours it and that the points the
draft leaves undecided stay undecided instead of being quietly settled in code.
"""
from __future__ import annotations

import random
import unittest

from src.rules import noopunk_tags as tags


class AttributeBandTest(unittest.TestCase):
    def test_the_bands_are_the_drafts(self) -> None:
        expected = {3: -2, 4: -1, 5: -1, 6: -1, 7: -1, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                    14: 1, 15: 1, 16: 1, 17: 1, 18: 2}
        for score, value in expected.items():
            self.assertEqual(tags.modifier_for_score(score), value, score)

    def test_only_the_modifier_is_stored(self) -> None:
        sheet = tags.Sheet(attributes={"Cognition": 2})
        self.assertEqual(sheet.attributes["Cognition"], 2)
        # A raw 3d6 score is not representable as an attribute tag value band beyond +2/-2.
        self.assertFalse(any(str(tag).startswith("1") for tag in sheet.sheet_lines()))

    def test_a_score_outside_three_d_six_is_refused(self) -> None:
        for score in (2, 19):
            with self.assertRaises(tags.TagError):
                tags.modifier_for_score(score)


class GenerationTest(unittest.TestCase):
    def test_all_seven_attributes_are_generated(self) -> None:
        sheet = tags.generate(random.Random(11))
        self.assertEqual(sorted(sheet.attributes), sorted(tags.ATTRIBUTES))
        self.assertEqual(len(tags.ATTRIBUTES), 7)

    def test_generation_never_produces_the_non_human_floor(self) -> None:
        for seed in range(200):
            sheet = tags.generate(random.Random(seed))
            self.assertGreater(sheet.empathy, tags.EMPATHY_FLOOR, seed)
            self.assertTrue(sheet.pc_eligible, seed)
            self.assertTrue(sheet.is_human, seed)

    def test_transhuman_is_above_plus_two(self) -> None:
        human = tags.Sheet(attributes={"Cyber": 2})
        self.assertFalse(human.is_transhuman)
        trans = tags.Sheet(attributes={"Cyber": 3})
        self.assertTrue(trans.is_transhuman)
        self.assertTrue(trans.pc_eligible)


class EmpathyBoundaryTest(unittest.TestCase):
    def test_the_floor_is_not_a_player_character(self) -> None:
        sheet = tags.Sheet(attributes={name: 0 for name in tags.ATTRIBUTES} | {"Empathy": -3})
        self.assertFalse(sheet.is_human)
        self.assertFalse(sheet.pc_eligible)

    def test_the_floor_is_representable_for_np_cs(self) -> None:
        tag = tags.attribute_tag("Empathy", -3)
        self.assertEqual(tag.display, "Empathy-3")

    def test_below_the_floor_is_not_storable(self) -> None:
        with self.assertRaises(tags.TagError):
            tags.Sheet(attributes={"Empathy": -4})


class TagDisplayTest(unittest.TestCase):
    def test_skill_rank_is_not_a_penalty(self) -> None:
        self.assertEqual(tags.skill_tag("Firearms", 1).display, "Firearms-1")
        self.assertEqual(tags.skill_tag("Firearms", 4).display, "Firearms-4")

    def test_status_shows_its_penalty(self) -> None:
        self.assertEqual(tags.status_tag("wounded", 1).display, "wounded-1")

    def test_attribute_shows_its_sign(self) -> None:
        self.assertEqual(tags.attribute_tag("Cognition", 2).display, "Cognition+2")
        self.assertEqual(tags.attribute_tag("Fitness", -2).display, "Fitness-2")
        self.assertEqual(tags.attribute_tag("Agency", 0).display, "Agency+0")

    def test_unicode_names_survive(self) -> None:
        self.assertEqual(tags.skill_tag("Noöware", 2).display, "Noöware-2")

    def test_a_skill_rank_is_capped_at_four(self) -> None:
        with self.assertRaises(tags.TagError):
            tags.skill_tag("Firearms", 5)

    def test_an_unknown_skill_is_refused(self) -> None:
        with self.assertRaises(tags.TagError):
            tags.skill_tag("Basketweaving", 1)


class CheckTest(unittest.TestCase):
    def test_a_trained_check_adds_rank(self) -> None:
        sheet = tags.Sheet(attributes={name: 0 for name in tags.ATTRIBUTES} | {"Reflexes": 2},
                           skills={"Firearms": 1})
        result = sheet.check("Reflexes", "Firearms", 7, difficulty=10)
        self.assertEqual(result["total"], 10)
        self.assertTrue(result["success"])

    def test_an_untrained_action_takes_the_penalty(self) -> None:
        result = tags.Sheet().check("Cognition", "Research", 7, difficulty=8)
        self.assertEqual(result["rank"], tags.UNTRAINED)
        self.assertFalse(result["success"])

    def test_talk_takes_empathy_or_agency(self) -> None:
        sheet = tags.Sheet(skills={"Talk": 1})
        self.assertTrue(sheet.check("Empathy", "Talk", 7)["ok"])
        self.assertTrue(sheet.check("Agency", "Talk", 7)["ok"])
        self.assertEqual(sheet.check("Reflexes", "Talk", 7)["reason"], "contextual_skill_wrong_attribute")

    def test_status_penalties_apply_to_checks(self) -> None:
        sheet = tags.Sheet(attributes={name: 0 for name in tags.ATTRIBUTES}, skills={"Firearms": 0})
        clean = sheet.check("Reflexes", "Firearms", 8, difficulty=8)
        sheet.add_status(tags.status_tag("wounded", 2))
        hurt = sheet.check("Reflexes", "Firearms", 8, difficulty=8)
        self.assertTrue(clean["success"])
        self.assertFalse(hurt["success"])

    def test_impossible_untrained_list_is_empty_until_ruled(self) -> None:
        self.assertEqual(tags.CONTRACT["skills"]["untrained"]["impossible_without"], [])


class StatusTest(unittest.TestCase):
    def test_highest_stacking_keeps_the_worst(self) -> None:
        sheet = tags.Sheet()
        sheet.add_status(tags.status_tag("wounded", 1))
        sheet.add_status(tags.status_tag("wounded", 2))
        self.assertEqual(sheet.status_penalty(), 2)

    def test_stack_adds_every_application(self) -> None:
        sheet = tags.Sheet()
        for _ in range(3):
            sheet.add_status(tags.status_tag("poisoned", 1, stacking=tags.Stacking.STACK))
        self.assertEqual(sheet.status_penalty(), 3)

    def test_the_newest_mode_governs_a_status(self) -> None:
        sheet = tags.Sheet()
        sheet.add_status(tags.status_tag("wounded", 1))
        sheet.add_status(tags.status_tag("wounded", 2))
        sheet.add_status(tags.status_tag("wounded", 1, stacking=tags.Stacking.STACK))
        self.assertEqual(sheet.status_penalty(), 4)

    def test_exclusive_statuses_replace_each_other(self) -> None:
        sheet = tags.Sheet()
        sheet.add_status(tags.status_tag("stunned", 2, stacking=tags.Stacking.REPLACE))
        sheet.add_status(tags.status_tag("panicked", 1, stacking=tags.Stacking.REPLACE,
                                         exclusive_with=("stunned",)))
        self.assertEqual([tag.name for tag in sheet.statuses], ["panicked"])

    def test_scene_statuses_expire_and_permanent_ones_do_not(self) -> None:
        sheet = tags.Sheet()
        sheet.add_status(tags.status_tag("wounded", 1, duration=tags.Duration.SCENE))
        sheet.add_status(tags.status_tag("marked", 1, duration=tags.Duration.PERMANENT))
        self.assertEqual(len(sheet.expire(tags.Duration.SCENE)), 1)
        self.assertEqual([tag.name for tag in sheet.statuses], ["marked"])
        self.assertEqual(sheet.expire(tags.Duration.PERMANENT), [])


class SerialisationTest(unittest.TestCase):
    def test_a_sheet_round_trips(self) -> None:
        sheet = tags.generate(random.Random(3))
        sheet.skills["Noöware"] = 3
        sheet.add_status(tags.status_tag("wounded", 1))
        sheet.traits.append(tags.Tag(tags.Kind.TRAIT, "Noögenetic"))
        restored = tags.Sheet.from_dict(sheet.to_dict())
        self.assertEqual(restored.to_dict(), sheet.to_dict())
        self.assertIn("Noöware-3", restored.sheet_lines())

    def test_a_save_from_another_schema_is_refused(self) -> None:
        with self.assertRaises(Exception):
            tags.Tag.from_dict({"kind": "nonsense", "name": "x"})


class MigrationTest(unittest.TestCase):
    def test_the_mapping_is_conceptual_not_a_copy(self) -> None:
        proposal = tags.migrate_from_cwn({"Intelligence": 14, "Wisdom": 9, "Charisma": 12,
                                          "Strength": 13, "Constitution": 10, "Dexterity": 12})
        # One old attribute feeds several new tags.
        self.assertEqual(proposal["derivation"]["Cognition"], ["Intelligence"])
        self.assertEqual(proposal["derivation"]["Cyber"], ["Intelligence"])
        self.assertEqual(proposal["derivation"]["Awareness"], ["Wisdom", "Charisma"])
        self.assertEqual(proposal["status"], "awaiting_author_ruling")

    def test_migration_is_a_proposal(self) -> None:
        proposal = tags.migrate_from_cwn({"Intelligence": 14})
        self.assertIn("derivation", proposal)
        self.assertNotIn("saved", proposal)


if __name__ == "__main__":
    unittest.main()
