"""Tests for the Without Number core (#615).

The author's direction was *"use CWN/SWN/AWN/WWN system for everything ... we will modify later"*, so this
kernel's job is to be exactly the published chassis and nothing more. The tests below therefore assert the
**arithmetic** (modifier bands, the -1 untrained penalty, the save target, the attack comparison), not
NoöPunk flavour.

Determinism is asserted two ways: an injected seed replays identically, and explicit dice values produce an
exact total. Inputs that are out of range raise rather than clamp — a silently clamped die is how a
distribution test passes while the distribution is wrong.
"""
from __future__ import annotations

import json
import pathlib
import random
import sys
import unittest

# The test-isolation guard requires every module that imports a ``src/`` package to put ``src/``
# on sys.path itself; relying on an earlier-collected module to do it makes the file pass or fail
# by collection order.
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rules.wn_core import (  # noqa: E402
    SAVE_BASE_TARGET,
    UNSKILLED_ATTACK_PENALTY,
    UNSKILLED_CHECK_PENALTY,
    attribute_modifier,
    attack_roll,
    roll_attributes,
    saving_throw,
    skill_check,
)

CONTRACT = json.loads((ROOT / "data" / "rules" / "wn_core.json").read_text(encoding="utf-8"))


class AttributeModifierTests(unittest.TestCase):
    def test_the_published_bands(self) -> None:
        """3 -> -2, 4-7 -> -1, 8-13 -> 0, 14-17 -> +1, 18 -> +2."""
        self.assertEqual(attribute_modifier(3), -2)
        for score in (4, 5, 6, 7):
            self.assertEqual(attribute_modifier(score), -1, score)
        for score in range(8, 14):
            self.assertEqual(attribute_modifier(score), 0, score)
        for score in (14, 15, 16, 17):
            self.assertEqual(attribute_modifier(score), 1, score)
        self.assertEqual(attribute_modifier(18), 2)

    def test_the_contract_json_and_the_kernel_agree(self) -> None:
        """Two sources of truth is how a band drifts; they are compared here, not trusted."""
        table = {int(k): v for k, v in CONTRACT["stats"]["modifier_table"].items()}
        for score in range(CONTRACT["stats"]["min"], CONTRACT["stats"]["max"] + 1):
            self.assertEqual(attribute_modifier(score), table[score], score)

    def test_out_of_range_scores_raise_rather_than_clamp(self) -> None:
        for bad in (2, 19, 0, -1, 100):
            with self.subTest(score=bad):
                with self.assertRaises(ValueError):
                    attribute_modifier(bad)

    def test_a_non_integer_score_is_a_type_error(self) -> None:
        for bad in ("12", 12.0, None, True):
            with self.subTest(score=bad):
                with self.assertRaises(TypeError):
                    attribute_modifier(bad)  # type: ignore[arg-type]


class SkillCheckTests(unittest.TestCase):
    def test_exact_arithmetic_with_explicit_dice(self) -> None:
        """No RNG: the total is knowable by hand, so the assertion is exact."""
        result = skill_check(attribute_score=14, skill_level=2, difficulty=10, dice=(5, 3))
        self.assertEqual(result.dice, (5, 3))
        self.assertEqual(result.modifier, 1)          # 14 -> +1
        self.assertEqual(result.skill_level, 2)
        self.assertEqual(result.total, 5 + 3 + 1 + 2)
        self.assertTrue(result.success)

    def test_untrained_is_minus_one_and_not_a_level(self) -> None:
        result = skill_check(attribute_score=10, skill_level=None, difficulty=8, dice=(4, 4))
        self.assertTrue(result.untrained)
        self.assertEqual(result.skill_level, UNSKILLED_CHECK_PENALTY)
        self.assertEqual(result.total, 8 + 0 - 1)
        self.assertFalse(result.success, "7 against difficulty 8 must fail")

    def test_the_difficulty_ladder_matches_the_contract(self) -> None:
        ladder = {int(k): v for k, v in CONTRACT["skill_check"]["difficulties"].items()}
        self.assertEqual(sorted(ladder), [6, 8, 10, 12])
        for difficulty, label in ladder.items():
            with self.subTest(difficulty=difficulty, label=label):
                self.assertTrue(label)
                skill_check(attribute_score=10, skill_level=0, difficulty=difficulty, dice=(1, 1))

    def test_two_dice_only(self) -> None:
        for bad in ((6,), (1, 2, 3), ()):
            with self.subTest(dice=bad):
                with self.assertRaises(ValueError):
                    skill_check(attribute_score=10, skill_level=0, difficulty=8, dice=bad)  # type: ignore[arg-type]

    def test_a_face_outside_one_to_six_raises(self) -> None:
        for bad in ((0, 3), (7, 3), (-1, 2)):
            with self.subTest(dice=bad):
                with self.assertRaises(ValueError):
                    skill_check(attribute_score=10, skill_level=0, difficulty=8, dice=bad)  # type: ignore[arg-type]

    def test_an_illegal_skill_level_raises(self) -> None:
        for bad in (-1, 5, 99):
            with self.subTest(level=bad):
                with self.assertRaises(ValueError):
                    skill_check(attribute_score=10, skill_level=bad, difficulty=8, dice=(3, 3))

    def test_a_seed_replays_identically_and_a_different_seed_does_not(self) -> None:
        """If the seed were ignored, the harness would prove nothing."""
        first = [skill_check(attribute_score=10, skill_level=1, difficulty=8,
                             rng=random.Random(42)).dice for _ in range(5)]
        again = [skill_check(attribute_score=10, skill_level=1, difficulty=8,
                             rng=random.Random(42)).dice for _ in range(5)]
        other = [skill_check(attribute_score=10, skill_level=1, difficulty=8,
                             rng=random.Random(43)).dice for _ in range(5)]
        self.assertEqual(first, again)
        self.assertNotEqual(first, other)

    def test_the_total_always_lands_in_the_possible_range(self) -> None:
        """2..12 dice, -2..+2 modifier, 0..4 skill — the arithmetic cannot leave that band."""
        rng = random.Random(7)
        for _ in range(200):
            result = skill_check(attribute_score=rng.randint(3, 18), skill_level=rng.randint(0, 4),
                                 difficulty=8, rng=rng)
            self.assertGreaterEqual(result.total, 2 - 2 + 0)
            self.assertLessEqual(result.total, 12 + 2 + 4)


class SaveTests(unittest.TestCase):
    def test_physical_uses_the_better_of_str_and_con(self) -> None:
        weak = saving_throw(category="Physical", scores={"STR": 10, "CON": 10}, die=10)
        strong = saving_throw(category="Physical", scores={"STR": 18, "CON": 10}, die=10)
        self.assertEqual(weak.target, SAVE_BASE_TARGET)          # +0 -> 15
        self.assertEqual(strong.target, SAVE_BASE_TARGET - 2)    # +2 -> 13
        self.assertFalse(weak.success, "10 vs 15 fails")
        self.assertFalse(strong.success, "10 vs 13 still fails")

    def test_luck_is_flat_fifteen(self) -> None:
        result = saving_throw(category="Luck", scores={}, die=15)
        self.assertEqual(result.target, 15)
        self.assertTrue(result.success, "a 15 meets a target of 15")
        self.assertFalse(saving_throw(category="Luck", scores={}, die=14).success)

    def test_a_missing_attribute_is_an_error_not_a_zero(self) -> None:
        with self.assertRaises(ValueError):
            saving_throw(category="Evasion", scores={"INT": 10}, die=10)

    def test_an_unknown_category_raises(self) -> None:
        with self.assertRaises(ValueError):
            saving_throw(category="Sanity", scores={}, die=10)


class AttackTests(unittest.TestCase):
    def test_the_comparison_is_greater_or_equal_to_ac(self) -> None:
        self.assertTrue(attack_roll(attack_bonus=3, ac=13, die=10).hit)
        self.assertFalse(attack_roll(attack_bonus=2, ac=13, die=10).hit)

    def test_the_unskilled_penalty_is_part_of_the_bonus(self) -> None:
        """Applied once by the caller, never twice by the kernel."""
        self.assertEqual(UNSKILLED_ATTACK_PENALTY, -2)
        result = attack_roll(attack_bonus=UNSKILLED_ATTACK_PENALTY, ac=10, die=12)
        self.assertEqual(result.total, 10)

    def test_an_out_of_range_die_raises(self) -> None:
        for bad in (0, 21):
            with self.subTest(die=bad):
                with self.assertRaises(ValueError):
                    attack_roll(attack_bonus=0, ac=10, die=bad)


class GenerationTests(unittest.TestCase):
    def test_six_attributes_on_three_d6(self) -> None:
        attributes = roll_attributes(random.Random(11))
        self.assertEqual(list(attributes), ["STR", "DEX", "CON", "INT", "WIS", "CHA"])
        for stat, score in attributes.items():
            with self.subTest(stat=stat):
                self.assertGreaterEqual(score, 3)
                self.assertLessEqual(score, 18)

    def test_generation_is_seeded(self) -> None:
        self.assertEqual(roll_attributes(random.Random(5)), roll_attributes(random.Random(5)))
        self.assertNotEqual(roll_attributes(random.Random(5)), roll_attributes(random.Random(6)))

    def test_the_array_is_the_documented_one(self) -> None:
        self.assertEqual(CONTRACT["generation"]["array"], [14, 12, 11, 10, 9, 7])


if __name__ == "__main__":
    unittest.main()
