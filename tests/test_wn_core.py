"""Issue #615 base-system contract: the *Without Number* arithmetic, exactly as the SRD (CC0) states it.

Author direction (2026-10-26): use the CWN/SWN/AWN/WWN system for stats, skills and rules as the
starting point. These tests are the contract for that base: if a later "modification" moves a band
edge, a ladder rung or the untrained penalty, one of them fails and names the change.
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from rules import wn  # noqa: E402


class CanonTests(unittest.TestCase):
    def test_the_base_system_is_versioned_and_named(self) -> None:
        self.assertEqual(wn.REVISION, "wn-2d6-cwn")
        self.assertEqual(wn.ATTRIBUTES, ("STR", "DEX", "CON", "INT", "WIS", "CHA"))
        self.assertEqual((wn.ATTRIBUTE_MIN, wn.ATTRIBUTE_MAX), (3, 18))
        self.assertEqual((wn.SKILL_MIN, wn.SKILL_MAX), (0, 4))
        self.assertEqual(wn.UNSKILLED_PENALTY, -1)
        self.assertEqual((wn.CHECK_DICE, wn.CHECK_DICE_COUNT, wn.CHECK_DICE_SIDES), ("2d6", 2, 6))


class AttributeModifierTests(unittest.TestCase):
    def test_every_score_in_the_range_maps_to_the_srd_band(self) -> None:
        expected = {3: -2}
        expected.update({score: -1 for score in range(4, 8)})
        expected.update({score: 0 for score in range(8, 14)})
        expected.update({score: 1 for score in range(14, 18)})
        expected.update({18: 2})
        for score, modifier in expected.items():
            with self.subTest(score=score):
                self.assertEqual(wn.attribute_modifier(score), modifier)

    def test_the_table_is_total_over_the_legal_range(self) -> None:
        self.assertEqual(sorted(wn.attribute_modifier(s) for s in range(3, 19))[0], -2)
        self.assertEqual(sorted(wn.attribute_modifier(s) for s in range(3, 19))[-1], 2)

    def test_scores_outside_3_to_18_are_refused(self) -> None:
        for bad in (0, 2, 19, 30):
            with self.subTest(score=bad), self.assertRaises(wn.WNError):
                wn.attribute_modifier(bad)

    def test_attribute_bonuses_are_clamped_to_the_canon_band(self) -> None:
        self.assertEqual(wn.clamp_modifier(5), wn.MODIFIER_CEILING)
        self.assertEqual(wn.clamp_modifier(-5), wn.MODIFIER_FLOOR)
        self.assertEqual(wn.attribute_total(1, 1, 1), wn.MODIFIER_CEILING)


class SkillCheckTests(unittest.TestCase):
    def test_the_arithmetic_is_dice_plus_modifier_plus_level(self) -> None:
        result = wn.resolve_skill_check(
            attribute="INT", score=14, skill_level=2, difficulty=10, dice=(3, 4)
        )
        self.assertEqual(result.dice, (3, 4))
        self.assertEqual(result.attribute_modifier, 1)
        self.assertEqual(result.total, 3 + 4 + 1 + 2)
        self.assertTrue(result.success)
        self.assertEqual(result.margin, 0)

    def test_success_is_total_greater_or_equal_to_difficulty(self) -> None:
        exact = wn.resolve_skill_check(attribute="WIS", score=8, skill_level=1, difficulty=10,
                                      dice=(5, 4))
        self.assertEqual(exact.total, 10)
        self.assertTrue(exact.success, "equalling the difficulty is a success")
        below = wn.resolve_skill_check(attribute="WIS", score=8, skill_level=1, difficulty=10,
                                       dice=(4, 4))
        self.assertFalse(below.success)
        self.assertEqual(below.margin, -1)

    def test_untrained_is_a_penalty_and_not_level_zero(self) -> None:
        trained = wn.resolve_skill_check(attribute="DEX", score=10, skill_level=0, difficulty=8,
                                         dice=(2, 3))
        untrained = wn.resolve_skill_check(attribute="DEX", score=10, skill_level=None, difficulty=8,
                                           dice=(2, 3))
        self.assertTrue(trained.untrained is False)
        self.assertTrue(untrained.untrained is True)
        self.assertEqual(untrained.total, trained.total + wn.UNSKILLED_PENALTY)

    def test_the_situational_band_is_two_points_each_way(self) -> None:
        for modifier in (wn.SITUATIONAL_MIN, 0, wn.SITUATIONAL_MAX):
            with self.subTest(modifier=modifier):
                wn.resolve_skill_check(attribute="CHA", score=11, skill_level=1, difficulty=8,
                                       dice=(3, 3), situational=modifier)
        for bad in (wn.SITUATIONAL_MIN - 1, wn.SITUATIONAL_MAX + 1):
            with self.subTest(modifier=bad), self.assertRaises(wn.WNError):
                wn.resolve_skill_check(attribute="CHA", score=11, skill_level=1, difficulty=8,
                                       dice=(3, 3), situational=bad)

    def test_skill_levels_outside_0_to_4_are_refused(self) -> None:
        for bad in (-1, 5, 9):
            with self.subTest(level=bad), self.assertRaises(wn.WNError):
                wn.resolve_skill_check(attribute="STR", score=10, skill_level=bad, difficulty=8,
                                       dice=(3, 3))

    def test_an_unknown_attribute_is_refused(self) -> None:
        with self.assertRaises(wn.WNError):
            wn.resolve_skill_check(attribute="FIT", score=10, skill_level=1, difficulty=8,
                                   dice=(3, 3))

    def test_the_dice_are_validated(self) -> None:
        with self.assertRaises(wn.WNError):
            wn.resolve_skill_check(attribute="INT", score=10, skill_level=1, difficulty=8, dice=(6,))
        with self.assertRaises(wn.WNError):
            wn.resolve_skill_check(attribute="INT", score=10, skill_level=1, difficulty=8, dice=(0, 6))
        with self.assertRaises(wn.WNError):
            wn.resolve_skill_check(attribute="INT", score=10, skill_level=1, difficulty=8, dice=(3, 7))

    def test_a_seeded_roll_replays(self) -> None:
        first = wn.resolve_skill_check(attribute="INT", score=12, skill_level=1, difficulty=9,
                                       rng=random.Random(615))
        second = wn.resolve_skill_check(attribute="INT", score=12, skill_level=1, difficulty=9,
                                        rng=random.Random(615))
        self.assertEqual(first, second)
        self.assertTrue(all(1 <= die <= 6 for die in first.dice))
        self.assertEqual(len(first.dice), 2)


class DifficultyLadderTests(unittest.TestCase):
    def test_the_ladder_is_the_srd_five_rungs(self) -> None:
        self.assertEqual(wn.DIFFICULTY_LADDER, (6, 8, 10, 12, 14))
        self.assertEqual(wn.TOP_DIFFICULTY, 14)
        for rung in wn.DIFFICULTY_LADDER:
            with self.subTest(rung=rung):
                description = wn.difficulty_for(rung)
                self.assertTrue(description, "every rung has a description")
                self.assertNotIn("No ladder rung", description)

    def test_an_off_ladder_difficulty_is_named_rather_than_rounded_silently(self) -> None:
        self.assertIn("No ladder rung", wn.difficulty_for(11))
        self.assertIn("nearest", wn.difficulty_for(11, nearest=True))


class SavingThrowTests(unittest.TestCase):
    def test_the_target_is_sixteen_minus_level_minus_the_best_listed_modifier(self) -> None:
        self.assertEqual(wn.save_target("physical", level=2, modifiers={"STR": 1, "CON": -1}), 13)
        self.assertEqual(wn.save_target("evasion", level=1, modifiers={"DEX": 2, "INT": 0}), 13)
        self.assertEqual(wn.save_target("mental", level=3, modifiers={"WIS": -2, "CHA": 1}), 12)

    def test_luck_has_no_attribute_modifiers(self) -> None:
        self.assertEqual(wn.save_target("luck", level=2, modifiers={"DEX": 2}), 14)

    def test_a_natural_one_always_fails_and_a_natural_twenty_always_succeeds(self) -> None:
        hopeless = wn.roll_save("physical", level=1, modifiers={"STR": -2}, die=1)
        self.assertFalse(hopeless.success)
        self.assertTrue(hopeless.natural)
        easy = wn.roll_save("physical", level=1, modifiers={"STR": 2}, die=20)
        self.assertTrue(easy.success)

    def test_the_die_is_validated_and_the_type_is_known(self) -> None:
        with self.assertRaises(wn.WNError):
            wn.roll_save("physical", die=21)
        with self.assertRaises(wn.WNError):
            wn.roll_save("psychic", die=10)

    def test_four_save_types_exist(self) -> None:
        self.assertEqual(wn.SAVE_TYPES, ("physical", "evasion", "mental", "luck"))


class LegacyMigrationTests(unittest.TestCase):
    def test_the_legacy_stat_stretch_is_monotonic_and_hits_both_ends(self) -> None:
        stretched = [wn.from_legacy_stat(value) for value in range(1, 11)]
        self.assertEqual(stretched[0], wn.ATTRIBUTE_MIN)
        self.assertEqual(stretched[-1], wn.ATTRIBUTE_MAX)
        self.assertEqual(stretched, sorted(stretched))
        self.assertTrue(all(wn.ATTRIBUTE_MIN <= v <= wn.ATTRIBUTE_MAX for v in stretched))

    def test_the_legacy_skill_mapping_covers_the_whole_level_scale(self) -> None:
        mapping = {value: wn.from_legacy_skill(value) for value in range(1, 11)}
        self.assertEqual(mapping[1], 0)
        self.assertEqual(mapping[10], wn.SKILL_MAX)
        self.assertEqual(mapping, {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4})

    def test_every_legacy_stat_has_a_declared_home(self) -> None:
        self.assertEqual(set(wn.LEGACY_STAT_MAP), {"FIT", "REF", "INT", "SOC", "CYB", "PSY"})
        self.assertTrue(set(wn.LEGACY_STAT_MAP.values()) <= set(wn.ATTRIBUTES))

    def test_out_of_range_legacy_values_are_refused(self) -> None:
        for bad in (0, 11):
            with self.subTest(value=bad), self.assertRaises(wn.WNError):
                wn.from_legacy_stat(bad)
            with self.subTest(value=bad), self.assertRaises(wn.WNError):
                wn.from_legacy_skill(bad)


if __name__ == "__main__":
    unittest.main()
