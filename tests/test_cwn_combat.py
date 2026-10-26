"""CWN attack resolution regression coverage."""
import random
import unittest

from src.rules.cwn_combat import attack_roll
from src.rules.wn_core import WnError


class CwnAttackTests(unittest.TestCase):
    def test_attack_uses_d20_not_2d6(self):
        hit = attack_roll(attribute_score=14, skill_level=1, attack_bonus=2, armor_class=15, die=11)
        self.assertEqual(hit.total, 15)
        self.assertTrue(hit.hit)
        self.assertEqual(hit.margin, 0)
        self.assertEqual(hit.die, 11)

    def test_untrained_attack_uses_minus_two_not_minus_one(self):
        result = attack_roll(attribute_score=10, skill_level=None, attack_bonus=0, armor_class=10, die=11)
        self.assertEqual(result.skill_modifier, -2)
        self.assertEqual(result.total, 9)
        self.assertFalse(result.hit)

    def test_zero_rank_is_trained(self):
        result = attack_roll(attribute_score=10, skill_level=0, attack_bonus=0, armor_class=10, die=10)
        self.assertEqual(result.skill_modifier, 0)
        self.assertTrue(result.hit)

    def test_bonus_and_ac_are_explicit(self):
        result = attack_roll(attribute_score=7, skill_level=2, attack_bonus=1,
                             armor_class=14, other_modifier=1, die=10)
        self.assertEqual(result.total, 13)
        self.assertFalse(result.hit)

    def test_seeded_attacks_replay(self):
        def sequence(seed):
            rng = random.Random(seed)
            return [attack_roll(attribute_score=10, skill_level=0, attack_bonus=0,
                                armor_class=12, rng=rng).die for _ in range(8)]
        self.assertEqual(sequence(31), sequence(31))
        self.assertNotEqual(sequence(31), sequence(32))

    def test_invalid_inputs_are_rejected(self):
        for face in (0, 21):
            with self.subTest(face=face), self.assertRaises(WnError):
                attack_roll(attribute_score=10, skill_level=0, attack_bonus=0,
                            armor_class=12, die=face)
        for skill in (-1, 5):
            with self.subTest(skill=skill), self.assertRaises(WnError):
                attack_roll(attribute_score=10, skill_level=skill, attack_bonus=0,
                            armor_class=12, die=10)
        with self.assertRaises(WnError):
            attack_roll(attribute_score=10, skill_level=0, attack_bonus=0,
                        armor_class=0, die=10)
        with self.assertRaises(WnError):
            attack_roll(attribute_score=19, skill_level=0, attack_bonus=0,
                        armor_class=10, die=10)
