"""NoöPunk typed tags and seven attributes (#821).

The draft is specific where it matters and silent where it is not; these tests pin the first and expose
the second rather than filling it in.
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules.noopunk_tags import (  # noqa: E402
    ATTRIBUTES,
    CONVERSION_SOURCES,
    Tag,
    TagType,
    attribute_tags,
    generate_attribute_tags,
    is_transhuman,
    modifier_for_roll,
    propose_conversion,
    roll_3d6,
    validate_attribute_set,
)


class TagTest(unittest.TestCase):
    def test_an_attribute_tag_displays_its_modifier_with_sign(self):
        self.assertEqual(Tag("Fitness", TagType.ATTRIBUTE, -2).display(), "Fitness-2")
        self.assertEqual(Tag("Agency", TagType.ATTRIBUTE, 1).display(), "Agency+1")
        self.assertEqual(Tag("Empathy", TagType.ATTRIBUTE, 0).display(), "Empathy")

    def test_a_skill_level_one_is_not_a_penalty(self):
        """`Shoot-1` means level 1. Only the type distinguishes it from a negative status."""
        skill = Tag("Shoot", TagType.SKILL, 1)
        status = Tag("wounded", TagType.STATUS, -1)
        self.assertEqual(skill.display(), "Shoot+1")
        self.assertFalse(skill.is_negative)
        self.assertTrue(status.is_negative)

    def test_unicode_names_are_allowed(self):
        tag = Tag("Noöware", TagType.SKILL, 1)
        self.assertEqual(tag.display(), "Noöware+1")

    def test_an_empty_name_is_refused(self):
        with self.assertRaises(ValueError):
            Tag("  ", TagType.STATUS, -1)

    def test_a_non_integer_value_is_refused(self):
        with self.assertRaises(ValueError):
            Tag("Fitness", TagType.ATTRIBUTE, "2")  # type: ignore[arg-type]


class RollBandTest(unittest.TestCase):
    def test_the_drafts_bands_exactly(self):
        expected = {3: -2, 4: -1, 5: -1, 6: -1, 7: -1, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                    14: 1, 15: 1, 16: 1, 17: 1, 18: 2}
        for total, modifier in expected.items():
            self.assertEqual(modifier_for_roll(total), modifier, total)

    def test_out_of_range_totals_are_refused_not_clamped(self):
        for total in (2, 19, 0):
            with self.assertRaises(ValueError):
                modifier_for_roll(total)

    def test_roll_is_three_to_eighteen(self):
        rng = random.Random(3)
        rolls = [roll_3d6(rng) for _ in range(200)]
        self.assertTrue(all(3 <= value <= 18 for value in rolls))


class GenerationTest(unittest.TestCase):
    def test_generation_produces_all_seven_attributes(self):
        tags = generate_attribute_tags(random.Random(11))
        self.assertEqual(set(attribute_tags(tags)), set(ATTRIBUTES))

    def test_the_sheet_never_carries_the_raw_roll(self):
        for tag in generate_attribute_tags(random.Random(5)).values():
            self.assertLessEqual(tag.value, 2)
            self.assertGreaterEqual(tag.value, -2)

    def test_generation_is_deterministic_for_a_seed(self):
        first = {name: tag.value for name, tag in generate_attribute_tags(random.Random(99)).items()}
        second = {name: tag.value for name, tag in generate_attribute_tags(random.Random(99)).items()}
        self.assertEqual(first, second)

    def test_validate_requires_every_attribute(self):
        tags = generate_attribute_tags(random.Random(1))
        validate_attribute_set(tags)
        partial = dict(tags)
        partial.pop("Cyber")
        with self.assertRaises(ValueError):
            validate_attribute_set(partial)

    def test_transhuman_values_are_detected_and_refused_on_a_sheet(self):
        tags = generate_attribute_tags(random.Random(2))
        tags["Cyber"] = Tag("Cyber", TagType.ATTRIBUTE, 3)
        self.assertTrue(is_transhuman(tags))
        with self.assertRaises(ValueError):
            validate_attribute_set(tags)


class ConversionTest(unittest.TestCase):
    def test_the_mapping_matches_the_draft(self):
        self.assertEqual(CONVERSION_SOURCES["Fitness"], ("STR", "CON"))
        self.assertEqual(CONVERSION_SOURCES["Reflexes"], ("DEX",))
        self.assertEqual(CONVERSION_SOURCES["Cognition"], ("INT",))
        self.assertEqual(CONVERSION_SOURCES["Cyber"], ("INT",))
        self.assertEqual(set(CONVERSION_SOURCES["Agency"]), {"WIS", "CHA"})

    def test_single_source_attributes_do_not_need_a_ruling(self):
        proposals = propose_conversion({"STR": 1, "CON": 0, "DEX": 2, "INT": 1, "WIS": 0, "CHA": -1})
        by_name = {p.attribute: p for p in proposals}
        self.assertEqual(by_name["Reflexes"].suggestion, 2)
        self.assertFalse(by_name["Reflexes"].needs_ruling)

    def test_multi_source_attributes_are_flagged_not_decided(self):
        proposals = propose_conversion({"STR": 2, "CON": -1, "DEX": 0, "INT": 0, "WIS": 1, "CHA": -2})
        by_name = {p.attribute: p for p in proposals}
        self.assertTrue(by_name["Fitness"].needs_ruling, "STR+CON cannot be merged silently")
        self.assertTrue(by_name["Agency"].needs_ruling)
        # the suggestion is a proposal, and it is documented as one
        self.assertEqual(by_name["Fitness"].suggestion, 2)

    def test_a_missing_source_is_an_error_not_a_guess(self):
        with self.assertRaises(ValueError):
            propose_conversion({"STR": 1})  # nothing for Reflexes


if __name__ == "__main__":
    unittest.main()
