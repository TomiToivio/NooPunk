"""Tests for CWN attribute generation and the starting skill pool."""
import unittest

from src.rules.cwn_character import (
    ARRAY,
    ATTRIBUTES,
    CharacterRulesError,
    SkillPool,
    assign_array,
    effective_modifier,
    roll_attributes,
    substitute_fourteen,
)


class AttributeGenerationTest(unittest.TestCase):
    def test_six_3d6_rolls_are_taken_in_order(self):
        scores = roll_attributes([1, 1, 1] + [3, 3, 3] + [6, 6, 6] + [2, 2, 2] + [4, 4, 4] + [5, 5, 5])
        self.assertEqual(scores["Strength"], 3)
        self.assertEqual(scores["Dexterity"], 9)
        self.assertEqual(scores["Constitution"], 18)
        self.assertEqual(scores["Charisma"], 15)

    def test_wrong_dice_count_is_refused(self):
        with self.assertRaises(CharacterRulesError):
            roll_attributes([1, 2, 3])

    def test_a_face_outside_one_to_six_is_refused(self):
        with self.assertRaises(CharacterRulesError):
            roll_attributes([0, 1, 1] + [1, 1, 1] * 5)

    def test_one_rolled_score_may_become_fourteen(self):
        base = {a: 10 for a in ATTRIBUTES}
        out = substitute_fourteen(base, "Wisdom")
        self.assertEqual(out["Wisdom"], 14)
        self.assertEqual(base["Wisdom"], 10)  # input untouched

    def test_substitution_happens_only_once(self):
        base = {a: 10 for a in ATTRIBUTES}
        with self.assertRaises(CharacterRulesError):
            substitute_fourteen(base, "Wisdom", already_substituted=True)

    def test_a_character_who_used_the_array_may_not_substitute(self):
        with self.assertRaises(CharacterRulesError):
            substitute_fourteen({a: 10 for a in ATTRIBUTES}, "Wisdom", array_used=True)


class ArrayTest(unittest.TestCase):
    def test_the_array_assigns_exactly_its_own_numbers(self):
        assignment = dict(zip(ATTRIBUTES, ARRAY))
        self.assertEqual(assign_array(assignment), assignment)

    def test_an_invented_spread_is_refused(self):
        with self.assertRaises(CharacterRulesError):
            assign_array(dict(zip(ATTRIBUTES, (18, 18, 18, 18, 18, 18))))

    def test_dropping_the_low_score_is_refused(self):
        with self.assertRaises(CharacterRulesError):
            assign_array(dict(zip(ATTRIBUTES, (14, 12, 11, 10, 9, 9))))


class ModifierTest(unittest.TestCase):
    def test_the_base_band_is_used_when_there_is_no_bonus(self):
        self.assertEqual(effective_modifier(3), -2)
        self.assertEqual(effective_modifier(10), 0)
        self.assertEqual(effective_modifier(18), 2)

    def test_a_bonus_cannot_push_past_plus_two(self):
        self.assertEqual(effective_modifier(18, 1), 2)

    def test_a_penalty_cannot_push_below_minus_two(self):
        self.assertEqual(effective_modifier(3, -1), -2)

    def test_an_explicit_source_may_exceed_the_band(self):
        self.assertEqual(effective_modifier(18, 1, uncapped=True), 3)


class SkillPoolTest(unittest.TestCase):
    def test_first_pick_is_level_zero_and_second_is_level_one(self):
        pool = SkillPool()
        self.assertEqual(pool.pick("Shoot"), 0)
        self.assertEqual(pool.pick("Shoot"), 1)

    def test_a_third_pick_of_the_same_skill_is_refused(self):
        pool = SkillPool()
        pool.pick("Shoot")
        pool.pick("Shoot")
        with self.assertRaises(CharacterRulesError):
            pool.pick("Shoot")

    def test_no_character_begins_above_level_one(self):
        pool = SkillPool()
        for _ in range(2):
            pool.pick("Heal")
        self.assertLessEqual(pool.levels["Heal"], 1)

    def test_a_surplus_pick_may_raise_a_different_skill_still_at_zero(self):
        pool = SkillPool()
        pool.pick("Shoot")
        pool.pick("Shoot")
        pool.pick("Heal")
        self.assertIn("Heal", pool.open_skills())
        self.assertEqual(pool.pick("Heal"), 1)

    def test_open_skills_excludes_anything_already_level_one(self):
        pool = SkillPool()
        pool.pick("Shoot")
        pool.pick("Shoot")
        self.assertEqual(pool.open_skills(), ())

    def test_a_nameless_skill_is_refused(self):
        with self.assertRaises(CharacterRulesError):
            SkillPool().pick("")


if __name__ == "__main__":
    unittest.main()
