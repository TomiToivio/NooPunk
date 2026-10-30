"""NoöPunk tag-based attributes, skills and statuses (#821).

The draft is Tomi's; these tests check the implementation honours it, and that the points the draft
leaves undecided stay undecided instead of being quietly settled in code.
"""
from __future__ import annotations

import random
import unittest

from src.rules import noopunk_tags as tags

HUMAN = {name: tags.Tag(name, tags.TagType.ATTRIBUTE, 0) for name in tags.ATTRIBUTES}


def sheet_with(**values: int) -> tags.Sheet:
    """A sheet whose attributes are all zero except the named ones."""
    attributes = {name: tags.Tag(name, tags.TagType.ATTRIBUTE, values.get(name, 0))
                  for name in tags.ATTRIBUTES}
    return tags.Sheet(attributes=attributes)


class BandTest(unittest.TestCase):
    def test_the_bands_are_the_drafts(self) -> None:
        expected = {3: -2, 4: -1, 5: -1, 6: -1, 7: -1, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                    14: 1, 15: 1, 16: 1, 17: 1, 18: 2}
        for total, value in expected.items():
            self.assertEqual(tags.modifier_for_roll(total), value, total)

    def test_only_the_modifier_is_stored(self) -> None:
        rolled = tags.generate_attribute_tags(random.Random(4))
        self.assertEqual(sorted(rolled), sorted(tags.ATTRIBUTES))
        self.assertTrue(all(-2 <= tag.value <= 2 for tag in rolled.values()))

    def test_a_total_outside_three_d_six_is_refused(self) -> None:
        for total in (2, 19):
            with self.assertRaises(ValueError):
                tags.modifier_for_roll(total)


class GenerationTest(unittest.TestCase):
    def test_generation_never_produces_the_non_human_floor(self) -> None:
        for seed in range(200):
            sheet = tags.generate_sheet(random.Random(seed))
            self.assertGreater(sheet.empathy, tags.EMPATHY_FLOOR, seed)
            self.assertTrue(sheet.pc_eligible, seed)
            self.assertFalse(sheet.is_transhuman, seed)

    def test_a_transhuman_tag_is_storable(self) -> None:
        sheet = sheet_with(Cyber=3)
        self.assertTrue(sheet.is_transhuman)
        self.assertTrue(sheet.pc_eligible)
        # The creation check refuses it by default and accepts it with the explicit flag.
        with self.assertRaises(ValueError):
            tags.validate_attribute_set(sheet.attributes)
        tags.validate_attribute_set(sheet.attributes, allow_transhuman=True)


class EmpathyBoundaryTest(unittest.TestCase):
    def test_the_floor_is_not_a_player_character(self) -> None:
        sheet = sheet_with(Empathy=-3)
        self.assertFalse(sheet.is_human)
        self.assertFalse(sheet.pc_eligible)

    def test_the_floor_is_representable(self) -> None:
        self.assertEqual(tags.Tag("Empathy", tags.TagType.ATTRIBUTE, -3).display(), "Empathy-3")

    def test_below_the_floor_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            tags.validate_attribute_set(sheet_with(Empathy=-4).attributes)


class DisplayTest(unittest.TestCase):
    def test_a_skill_rank_never_looks_like_a_bonus(self) -> None:
        self.assertEqual(tags.skill_tag("Firearms", 1).display(), "Firearms-1")
        self.assertEqual(tags.skill_tag("Firearms", 4).display(), "Firearms-4")
        self.assertEqual(tags.skill_tag("Firearms", 0).display(), "Firearms-0")

    def test_a_status_shows_its_penalty(self) -> None:
        self.assertEqual(tags.status_tag("wounded", 1).display(), "wounded-1")
        self.assertEqual(tags.status_tag("wounded", 2).display(), "wounded-2")

    def test_an_attribute_shows_its_modifier(self) -> None:
        self.assertEqual(tags.Tag("Cognition", tags.TagType.ATTRIBUTE, 2).display(), "Cognition+2")
        self.assertEqual(tags.Tag("Fitness", tags.TagType.ATTRIBUTE, -2).display(), "Fitness-2")
        self.assertEqual(tags.Tag("Agency", tags.TagType.ATTRIBUTE, 0).display(), "Agency+0")

    def test_unicode_names_survive(self) -> None:
        self.assertEqual(tags.skill_tag("Noöware", 2).display(), "Noöware-2")

    def test_a_rank_above_four_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            tags.skill_tag("Firearms", 5)

    def test_an_unknown_skill_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            tags.skill_tag("Basketweaving", 1)


class CheckTest(unittest.TestCase):
    def test_a_trained_check_adds_rank(self) -> None:
        sheet = sheet_with(Reflexes=2)
        sheet.skills["Firearms"] = tags.skill_tag("Firearms", 1)
        result = sheet.check("Reflexes", "Firearms", 7, difficulty=10)
        self.assertEqual(result["total"], 10)
        self.assertTrue(result["success"])

    def test_an_untrained_action_takes_the_penalty(self) -> None:
        result = sheet_with().check("Cognition", "Research", 7, difficulty=8)
        self.assertEqual(result["rank"], tags.UNTRAINED)
        self.assertFalse(result["success"])

    def test_talk_takes_empathy_or_agency_only(self) -> None:
        sheet = sheet_with()
        sheet.skills["Talk"] = tags.skill_tag("Talk", 1)
        self.assertTrue(sheet.check("Empathy", "Talk", 7)["ok"])
        self.assertTrue(sheet.check("Agency", "Talk", 7)["ok"])
        self.assertEqual(sheet.check("Reflexes", "Talk", 7)["reason"],
                         "contextual_skill_wrong_attribute")

    def test_an_unknown_skill_is_a_result_not_an_exception(self) -> None:
        self.assertEqual(sheet_with().check("Cognition", "Astrology", 7)["reason"], "unknown_skill")

    def test_status_penalties_apply_to_checks(self) -> None:
        sheet = sheet_with()
        sheet.skills["Firearms"] = tags.skill_tag("Firearms", 0)
        self.assertTrue(sheet.check("Reflexes", "Firearms", 8, difficulty=8)["success"])
        sheet.add_status(tags.status_tag("wounded", 2))
        self.assertFalse(sheet.check("Reflexes", "Firearms", 8, difficulty=8)["success"])


class StatusTest(unittest.TestCase):
    def test_highest_stacking_keeps_the_worst(self) -> None:
        sheet = sheet_with()
        sheet.add_status(tags.status_tag("wounded", 1))
        sheet.add_status(tags.status_tag("wounded", 2))
        self.assertEqual(sheet.status_penalty(), 2)

    def test_stack_adds_every_application(self) -> None:
        sheet = sheet_with()
        for _ in range(3):
            sheet.add_status(tags.status_tag("poisoned", 1, stacking="stack"))
        self.assertEqual(sheet.status_penalty(), 3)

    def test_the_newest_mode_governs_a_status(self) -> None:
        sheet = sheet_with()
        sheet.add_status(tags.status_tag("wounded", 1))
        sheet.add_status(tags.status_tag("wounded", 2))
        sheet.add_status(tags.status_tag("wounded", 1, stacking="stack"))
        self.assertEqual(sheet.status_penalty(), 4)

    def test_exclusive_statuses_replace_each_other(self) -> None:
        sheet = sheet_with()
        sheet.add_status(tags.status_tag("stunned", 2, stacking="replace"))
        sheet.add_status(tags.status_tag("panicked", 1, stacking="replace",
                                         exclusive_with=("stunned",)))
        self.assertEqual([tag.name for tag in sheet.statuses], ["panicked"])

    def test_scene_statuses_expire_and_permanent_ones_do_not(self) -> None:
        sheet = sheet_with()
        sheet.add_status(tags.status_tag("wounded", 1, duration="scene"))
        sheet.add_status(tags.status_tag("marked", 1, duration="permanent"))
        self.assertEqual(len(sheet.expire("scene")), 1)
        self.assertEqual([tag.name for tag in sheet.statuses], ["marked"])
        self.assertEqual(sheet.expire("permanent"), [])


class SerialisationTest(unittest.TestCase):
    def test_a_sheet_round_trips(self) -> None:
        sheet = tags.generate_sheet(random.Random(3))
        sheet.skills["Noöware"] = tags.skill_tag("Noöware", 3)
        sheet.add_status(tags.status_tag("wounded", 1))
        restored = tags.Sheet.from_dict(sheet.to_dict())
        self.assertEqual(restored.to_dict(), sheet.to_dict())
        self.assertIn("Noöware-3", restored.sheet_lines())

    def test_a_skill_cannot_be_seated_as_an_attribute(self) -> None:
        with self.assertRaises(ValueError):
            tags.Sheet(attributes={"Firearms": tags.skill_tag("Firearms", 1)})


class ConversionTest(unittest.TestCase):
    def test_multi_source_tags_need_a_ruling(self) -> None:
        proposals = {p.attribute: p for p in tags.propose_conversion(
            {"WIS": 1, "CHA": 0, "STR": 0, "CON": 1, "DEX": 1, "INT": 2})}
        self.assertTrue(proposals["Fitness"].needs_ruling)
        self.assertTrue(proposals["Cognition"].needs_ruling is False)
        self.assertEqual(proposals["Fitness"].suggestion, 1)

    def test_a_proposal_is_not_a_migration(self) -> None:
        proposal = tags.propose_conversion({"WIS": 0, "CHA": 0, "STR": 0, "CON": 0, "DEX": 0, "INT": 0})
        self.assertEqual(len(proposal), 7)
        self.assertFalse(any("saved" in str(p) for p in proposal))


if __name__ == "__main__":
    unittest.main()
