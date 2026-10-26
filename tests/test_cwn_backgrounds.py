"""Tests for the Background and Contact contracts."""
import unittest

from src.rules.cwn_backgrounds import (
    ACQUAINTANCE,
    FRIEND,
    AnyCombat,
    AnySkill,
    AttributeBonus,
    Background,
    BackgroundRulesError,
    Contact,
    ContactBook,
    apply_attribute_bonus,
    grant_free_skill,
    growth_rolls,
    resolve_table_entry,
    specific_picks,
)
from src.rules.cwn_character import SkillPool

TABLE_BG = Background(
    id="bureaucrat",
    free_skill="Administer",
    learning=(AnyCombat(), AnySkill(), "Talk", "Connect", "Program"),
    growth=(AttributeBonus(1, "Any"), "Talk", AnyCombat()),
)


class FreeSkillTest(unittest.TestCase):
    def test_the_free_skill_arrives_at_level_zero(self):
        pool = SkillPool()
        self.assertEqual(grant_free_skill(TABLE_BG, pool), 0)
        self.assertEqual(pool.levels["Administer"], 0)


class SpecificPickTest(unittest.TestCase):
    def test_two_picks_from_the_learning_table(self):
        pool = SkillPool()
        grant_free_skill(TABLE_BG, pool)
        self.assertEqual(specific_picks(TABLE_BG, ["Talk", "Connect"], pool), [0, 0])

    def test_the_same_skill_may_be_picked_twice_to_reach_level_one(self):
        pool = SkillPool()
        specific_picks(TABLE_BG, ["Talk", "Talk"], pool)
        self.assertEqual(pool.levels["Talk"], 1)

    def test_a_skill_outside_the_learning_table_is_refused(self):
        with self.assertRaises(BackgroundRulesError):
            specific_picks(TABLE_BG, ["Shoot", "Talk"], SkillPool())

    def test_wrong_number_of_picks_is_refused(self):
        with self.assertRaises(BackgroundRulesError):
            specific_picks(TABLE_BG, ["Talk"], SkillPool())

    def test_any_skill_is_not_a_legal_specific_pick(self):
        # "Any Skill" is an instruction to roll, not a skill name.
        with self.assertRaises(BackgroundRulesError):
            specific_picks(TABLE_BG, ["Any Skill", "Talk"], SkillPool())


class GrowthRollTest(unittest.TestCase):
    def test_three_rolls_may_all_come_from_one_table(self):
        out = growth_rolls(TABLE_BG, [("growth", 1), ("growth", 2), ("growth", 3)])
        self.assertEqual(len(out), 3)

    def test_rolls_may_be_split_between_tables(self):
        out = growth_rolls(TABLE_BG, [("growth", 3), ("learning", 1), ("learning", 3)])
        self.assertIsInstance(out[1], AnyCombat)
        self.assertEqual(out[2].skill, "Talk")

    def test_the_wrong_number_of_rolls_is_refused(self):
        with self.assertRaises(BackgroundRulesError):
            growth_rolls(TABLE_BG, [("growth", 1)])

    def test_a_roll_past_the_end_of_a_table_is_refused_rather_than_clamped(self):
        with self.assertRaises(BackgroundRulesError):
            resolve_table_entry(TABLE_BG.growth, 9)

    def test_an_unknown_table_name_is_refused(self):
        with self.assertRaises(BackgroundRulesError):
            growth_rolls(TABLE_BG, [("spiral", 1), ("growth", 1), ("growth", 1)])


ATTRS = {"Strength": 10, "Dexterity": 10, "Constitution": 10,
         "Intelligence": 10, "Wisdom": 10, "Charisma": 10}


class AttributeBonusTest(unittest.TestCase):

    def test_a_physical_bonus_may_target_a_physical_attribute(self):
        out = apply_attribute_bonus(AttributeBonus(2, "Physical"), ATTRS, [("Strength", 2)])
        self.assertEqual(out["Strength"], 12)
        self.assertEqual(ATTRS["Strength"], 10)   # input untouched

    def test_a_bonus_may_be_split_between_two_of_the_same_kind(self):
        out = apply_attribute_bonus(AttributeBonus(2, "Physical"), ATTRS,
                                    [("Strength", 1), ("Dexterity", 1)])
        self.assertEqual((out["Strength"], out["Dexterity"]), (11, 11))

    def test_a_physical_bonus_cannot_target_a_mental_attribute(self):
        with self.assertRaises(BackgroundRulesError):
            apply_attribute_bonus(AttributeBonus(2, "Physical"), ATTRS, [("Wisdom", 2)])

    def test_any_stat_may_target_either_kind(self):
        out = apply_attribute_bonus(AttributeBonus(1, "Any"), ATTRS, [("Wisdom", 1)])
        self.assertEqual(out["Wisdom"], 11)

    def test_no_attribute_may_exceed_eighteen(self):
        with self.assertRaises(BackgroundRulesError):
            apply_attribute_bonus(AttributeBonus(2, "Physical"),
                                  dict(ATTRS, Strength=17), [("Strength", 2)])

    def test_the_whole_bonus_must_be_spent(self):
        with self.assertRaises(BackgroundRulesError):
            apply_attribute_bonus(AttributeBonus(2, "Physical"), ATTRS, [("Strength", 1)])


class ContactTest(unittest.TestCase):
    def test_two_acquaintances_are_legal(self):
        book = ContactBook([Contact("doc", ACQUAINTANCE), Contact("fixer", ACQUAINTANCE)])
        self.assertEqual(len(book.contacts), 2)

    def test_one_friend_is_legal(self):
        self.assertEqual(len(ContactBook([Contact("doc", FRIEND)]).contacts), 1)

    def test_a_mixed_start_is_refused(self):
        with self.assertRaises(BackgroundRulesError):
            ContactBook([Contact("doc", FRIEND), Contact("fixer", ACQUAINTANCE)])

    def test_three_acquaintances_are_refused(self):
        with self.assertRaises(BackgroundRulesError):
            ContactBook([Contact(a) for a in ("a", "b", "c")])

    def test_two_friends_are_refused(self):
        with self.assertRaises(BackgroundRulesError):
            ContactBook([Contact("a", FRIEND), Contact("b", FRIEND)])

    def test_an_illegal_addition_is_rolled_back(self):
        book = ContactBook([Contact("doc", FRIEND)])
        with self.assertRaises(BackgroundRulesError):
            book.add(Contact("fixer", ACQUAINTANCE))
        self.assertEqual(len(book.contacts), 1)

    def test_promoting_an_acquaintance_to_friend_is_refused_when_it_breaks_the_start(self):
        book = ContactBook([Contact("doc"), Contact("fixer")])
        with self.assertRaises(BackgroundRulesError):
            book.promote("doc")
        self.assertEqual(book.contacts[0].level, ACQUAINTANCE)

    def test_a_contact_needs_a_name(self):
        with self.assertRaises(BackgroundRulesError):
            Contact("")


if __name__ == "__main__":
    unittest.main()
