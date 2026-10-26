"""Behavioral tests for the first #615 Without Number rules kernel."""
import random
import unittest

from src.rules.without_number import (
    ATTRIBUTES, Character, attack_check, enter_environment, modifier,
    saving_throw, skill_check,
)


class WithoutNumberKernelTests(unittest.TestCase):
    def setUp(self):
        self.character = Character(
            dict(zip(ATTRIBUTES, (12, 14, 10, 13, 9, 8))),
            {"Program": 1, "Notice": 0, "Survive": 1, "Talk": 0},
            hit_points=6, effort_max=3,
        )

    def test_attribute_modifier_bands(self):
        for score, expected in ((3, -2), (4, -1), (7, -1),
                                (8, 0), (13, 0), (14, 1), (17, 1), (18, 2)):
            self.assertEqual(modifier(score), expected)
        with self.assertRaises(ValueError):
            modifier(19)

    def test_two_d6_skill_and_untrained(self):
        rng = random.Random(615)
        result = skill_check(self.character, "INT", "Program", 8, rng)
        self.assertEqual(result.total, result.dice + 1)
        self.assertTrue(2 <= result.dice <= 12)
        untrained = skill_check(self.character, "WIS", "Heal", rng=random.Random(615))
        self.assertEqual(untrained.total, untrained.dice - 1)

    def test_d20_combat_and_saves(self):
        attack = attack_check(2, 12, rng=random.Random(33), attribute_modifier=1)
        self.assertEqual(attack.total, attack.dice + 3)
        self.assertTrue(1 <= attack.dice <= 20)
        save = saving_throw(12, rng=random.Random(33))
        self.assertEqual(save.total, save.dice)

    def test_effort_never_overcommits(self):
        self.character.commit_effort(2)
        with self.assertRaises(ValueError):
            self.character.commit_effort(2)
        self.character.release_effort(1)
        self.assertEqual(self.character.effort_committed, 1)

    def test_genre_change_preserves_character(self):
        original = self.character
        for environment in ("urban", "crisis", "space", "noetic"):
            self.assertIs(enter_environment(original, environment), original)
        self.assertEqual(original.hit_points, 6)
        self.assertEqual(original.skills["Program"], 1)

    def test_character_rejects_bad_attributes_and_skills(self):
        with self.assertRaises(ValueError):
            Character({"INT": 12})
        with self.assertRaises(ValueError):
            Character(dict.fromkeys(ATTRIBUTES, 10), {"Fake": 4})
        with self.assertRaises(ValueError):
            Character(dict.fromkeys(ATTRIBUTES, 10), {"Program": 5})


if __name__ == "__main__":
    unittest.main()
