from __future__ import annotations

import unittest

from src.rules.tags import (
    EntityState,
    SystemDomain,
    SystemState,
    Tag,
    TagCategory,
    absent_system,
    present_system,
    stack_relevant_tags,
)


class Issue51TagModelTests(unittest.TestCase):
    def test_attributes_are_tags(self) -> None:
        tag = Tag("REF", 2, TagCategory.ATTRIBUTE, SystemDomain.PHYSICAL)
        self.assertTrue(tag.is_attribute)
        self.assertTrue(tag.is_normal_human_attribute_value)

    def test_transhuman_attribute_values_are_representable(self) -> None:
        tag = Tag("prototype_attribute", 4, TagCategory.ATTRIBUTE, SystemDomain.PHYSICAL)
        self.assertFalse(tag.is_normal_human_attribute_value)
        self.assertEqual(tag.rating, 4)

    def test_relevant_tags_stack(self) -> None:
        tags = (
            Tag("REF", 1, TagCategory.ATTRIBUTE, SystemDomain.PHYSICAL),
            Tag("Pistol", 2, TagCategory.SKILL, SystemDomain.PHYSICAL),
            Tag("Smartlink", 1, TagCategory.CYBERWARE, SystemDomain.CYBERNETIC),
            Tag("Ambush position", 1, TagCategory.ENVIRONMENT),
            Tag("Injured arm", -1, TagCategory.INJURY, SystemDomain.PHYSICAL),
        )
        result = stack_relevant_tags(tags)
        self.assertEqual(result.total, 4)
        self.assertEqual(result.tags, tags)

    def test_absent_system_is_distinct_from_low_attribute(self) -> None:
        absent = absent_system(SystemDomain.PSYCHIC)
        weak = present_system(
            SystemDomain.PHYSICAL,
            Tag("prototype_attribute", -3, TagCategory.ATTRIBUTE, SystemDomain.PHYSICAL),
        )
        self.assertFalse(absent.present)
        self.assertTrue(weak.present)
        self.assertEqual(weak.attribute_tags()[0].rating, -3)

    def test_absent_system_cannot_hold_active_tags(self) -> None:
        with self.assertRaises(ValueError):
            SystemState(
                SystemDomain.PSYCHIC,
                present=False,
                tags=(Tag("INT", 0, TagCategory.ATTRIBUTE, SystemDomain.PSYCHIC),),
            )

    def test_entity_defines_all_four_systems(self) -> None:
        entity = EntityState(
            entity_id="nonconscious_ai",
            systems={
                SystemDomain.PHYSICAL: absent_system(SystemDomain.PHYSICAL),
                SystemDomain.SOCIAL: present_system(SystemDomain.SOCIAL),
                SystemDomain.PSYCHIC: absent_system(SystemDomain.PSYCHIC),
                SystemDomain.CYBERNETIC: present_system(SystemDomain.CYBERNETIC),
            },
        )
        self.assertFalse(entity.system_present(SystemDomain.PSYCHIC))
        self.assertTrue(entity.system_present(SystemDomain.CYBERNETIC))

    def test_mismatched_system_tag_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            present_system(
                SystemDomain.SOCIAL,
                Tag("prototype_attribute", 1, TagCategory.ATTRIBUTE, SystemDomain.PHYSICAL),
            )


if __name__ == "__main__":
    unittest.main()
