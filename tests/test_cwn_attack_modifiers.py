"""Attack-roll modifiers — assertions traced to the CWN SRD attack table."""
import unittest

from src.rules import cwn_attack_modifiers as mods
from src.rules import cwn_combat


class TableTests(unittest.TestCase):
    def test_a_single_circumstance_uses_the_table_value(self) -> None:
        self.assertEqual(mods.attack_modifier("target_half_cover"), -2)
        self.assertEqual(mods.attack_modifier("target_prone_adjacent"), 2)

    def test_circumstances_stack(self) -> None:
        self.assertEqual(
            mods.attack_modifier("target_half_cover", "target_prone_not_in_melee"), -4
        )

    def test_no_circumstances_is_zero(self) -> None:
        self.assertEqual(mods.attack_modifier(), 0)

    def test_an_unknown_circumstance_is_an_error_not_a_zero(self) -> None:
        with self.assertRaises(KeyError):
            mods.attack_modifier("target_is_a_lizard")

    def test_an_impossible_circumstance_raises(self) -> None:
        with self.assertRaises(mods.AttackImpossibleError):
            mods.attack_modifier("two_handed_gun_in_melee")
        with self.assertRaises(mods.AttackImpossibleError):
            mods.attack_modifier("target_unseen_position_unknown")

    def test_an_impossible_circumstance_cannot_be_stacked_away(self) -> None:
        with self.assertRaises(mods.AttackImpossibleError):
            mods.attack_modifier("target_half_cover", "two_handed_gun_in_melee")


class InMeleeTests(unittest.TestCase):
    def test_one_handed_guns_and_thrown_weapons_take_four(self) -> None:
        self.assertEqual(mods.in_melee_penalty("one_handed"), -4)
        self.assertEqual(mods.in_melee_penalty("thrown"), -4)

    def test_two_handed_guns_cannot_fire_in_melee(self) -> None:
        with self.assertRaises(mods.AttackImpossibleError):
            mods.in_melee_penalty("two_handed")

    def test_unknown_handedness_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            mods.in_melee_penalty("shoulder-mounted")


class CompositionWithAttackRollTests(unittest.TestCase):
    def test_cover_turns_a_hit_into_a_miss(self) -> None:
        kwargs = dict(attribute_score=14, skill_level=1, attack_bonus=1, armor_class=13, die=10)
        clear = cwn_combat.attack_roll(**kwargs)
        covered = cwn_combat.attack_roll(
            **kwargs, other_modifier=mods.attack_modifier("target_almost_full_cover")
        )
        self.assertTrue(clear.hit)
        self.assertFalse(covered.hit)
        self.assertEqual(covered.total, clear.total - 4)


if __name__ == "__main__":
    unittest.main()
