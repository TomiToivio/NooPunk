"""Tests for the Without Number kernel adopted by the 2026-10-26 author ruling.

Every value asserted here is read from the SRD, so these tests are the contract between the
repository and the source. If a band, a difficulty or a cap changes, this file is where the
change has to be argued for.
"""
import random
import unittest

from src.rules import wn_core as wn


class AttributeModifierTests(unittest.TestCase):
    """SRD 1.1.2: 3 -> -2, 4-7 -> -1, 8-13 -> 0, 14-17 -> +1, 18 -> +2."""

    def test_the_bands_are_exactly_the_srd_bands(self) -> None:
        expected = {
            3: -2, 4: -1, 5: -1, 6: -1, 7: -1,
            8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
            14: 1, 15: 1, 16: 1, 17: 1, 18: 2,
        }
        for score, modifier in expected.items():
            with self.subTest(score=score):
                self.assertEqual(wn.attribute_modifier(score), modifier)

    def test_scores_outside_3_to_18_are_refused(self) -> None:
        for score in (2, 0, -1, 19, 25):
            with self.subTest(score=score), self.assertRaises(wn.WnError):
                wn.attribute_modifier(score)

    def test_the_base_cap_is_two_in_both_directions(self) -> None:
        self.assertEqual(wn.attribute_modifier(wn.ATTRIBUTE_MIN), -2)
        self.assertEqual(wn.attribute_modifier(wn.ATTRIBUTE_MAX), 2)


class SkillCheckTests(unittest.TestCase):
    """SRD 2.3.0/2.3.1: 2d6 + attribute modifier + skill level vs difficulty."""

    def test_the_arithmetic_is_two_dice_plus_modifier_plus_skill(self) -> None:
        check = wn.skill_check(attribute_score=14, skill_level=2, difficulty=8, dice=(3, 5))
        self.assertEqual(check.dice, (3, 5))
        self.assertEqual(check.attribute_modifier, 1)
        self.assertEqual(check.total, 3 + 5 + 1 + 2)
        self.assertTrue(check.success)
        self.assertEqual(check.margin, 3)

    def test_missing_the_difficulty_by_one_is_a_failure(self) -> None:
        # 2 + 2 + 0 + 0 = 4 against a 6 is the bottom of the scale.
        check = wn.skill_check(attribute_score=8, skill_level=0, difficulty=6, dice=(1, 1))
        self.assertEqual(check.total, 2)
        self.assertFalse(check.success)

    def test_the_difficulty_bands_are_the_srd_values(self) -> None:
        self.assertEqual(
            (wn.DIFFICULTY_SIMPLE, wn.DIFFICULTY_SIGNIFICANT, wn.DIFFICULTY_EXPERT,
             wn.DIFFICULTY_MASTER, wn.DIFFICULTY_EXTREME),
            (6, 8, 10, 12, 14),
        )

    def test_a_table_rolling_real_dice_can_supply_them(self) -> None:
        check = wn.skill_check(attribute_score=10, skill_level=1, difficulty=8, dice=(6, 6))
        self.assertEqual(check.total, 12 + 0 + 1)

    def test_dice_outside_1_to_6_are_refused(self) -> None:
        for bad in ((0, 3), (7, 3), (3,)):
            with self.subTest(dice=bad), self.assertRaises(wn.WnError):
                wn.skill_check(attribute_score=10, skill_level=1, difficulty=8, dice=bad)

    def test_a_negative_skill_level_is_refused(self) -> None:
        with self.assertRaises(wn.WnError):
            wn.skill_check(attribute_score=10, skill_level=-1, difficulty=8, dice=(3, 3))


class BoundedModifierTests(unittest.TestCase):
    """SRD 2.3.1 and 2.3.3: circumstances -2..+2, aid at most +1."""

    def test_circumstances_are_clamped_to_plus_or_minus_two(self) -> None:
        self.assertEqual(wn.clamp_situational(9), 2)
        self.assertEqual(wn.clamp_situational(-9), -2)
        self.assertEqual(wn.clamp_situational(1), 1)

    def test_aid_never_exceeds_one_however_many_help(self) -> None:
        self.assertEqual(wn.clamp_aid(0), 0)
        self.assertEqual(wn.clamp_aid(1), 1)
        self.assertEqual(wn.clamp_aid(5), 1)

    def test_the_bounds_are_enforced_inside_a_check(self) -> None:
        blown_up = wn.skill_check(attribute_score=10, skill_level=1, difficulty=8,
                                  situational=9, aid=9, dice=(3, 3))
        self.assertEqual(blown_up.situational, 2)
        self.assertEqual(blown_up.aid, 1)


class DeterminismTests(unittest.TestCase):
    def test_a_seeded_roll_replays_and_different_seeds_differ(self) -> None:
        def roll(seed: int) -> tuple[int, int]:
            return wn.skill_check(attribute_score=10, skill_level=1, difficulty=8,
                                  rng=random.Random(seed)).dice

        self.assertEqual(roll(2026), roll(2026))
        self.assertGreater(len({roll(s) for s in range(30)}), 1)

    def test_the_kernel_has_no_model_or_network_dependency(self) -> None:
        import inspect
        source = inspect.getsource(wn)
        for dependency in ("openai", "anthropic", "requests", "urllib", "socket"):
            self.assertNotIn(dependency, source)


class OpposedCheckTests(unittest.TestCase):
    """SRD 2.3.4: the higher roll wins. Ties are reported, not silently invented."""

    def test_the_higher_roll_wins(self) -> None:
        self.assertEqual(wn.opposed_check(a=(6, 6), b=(1, 1)), "a")
        self.assertEqual(wn.opposed_check(a=(1, 1), b=(6, 6)), "b")

    def test_a_tie_is_reported_as_undefined(self) -> None:
        self.assertIsNone(wn.opposed_check(a=(4, 3), b=(5, 2)),
                          "the SRD gives no tie-break, so none may be invented here")


class SupersessionTests(unittest.TestCase):
    """The ruling changed the kernel; the module must say so where it can be checked."""

    def test_the_six_attributes_are_the_without_number_names(self) -> None:
        self.assertEqual(wn.ATTRIBUTES,
                         ("Strength", "Dexterity", "Constitution",
                          "Intelligence", "Wisdom", "Charisma"))

    def test_the_old_noopunk_stat_names_are_gone_from_this_kernel(self) -> None:
        for legacy in ("FIT", "REF", "INT", "SOC", "CYB", "PSY"):
            self.assertNotIn(legacy, wn.ATTRIBUTES)

    def test_the_check_is_2d6_not_1d10(self) -> None:
        self.assertEqual((wn.SKILL_CHECK_DICE, wn.SKILL_CHECK_FACES), (2, 6))


if __name__ == "__main__":
    unittest.main()
