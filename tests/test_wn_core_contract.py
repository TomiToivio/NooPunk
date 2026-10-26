"""The contract and the kernel must agree.

`src/rules/wn_core.py` is the implementation; `data/rules/wn_core.json` is the readable contract that states
the same numbers. Two sources of truth is exactly how a band drifts — one gets edited, the other does not, and
the documentation keeps describing the old arithmetic. These tests compare them instead of trusting either.

They also pin the *shape* of the core to the Without Number baseline adopted by #620, so a later edit to one
number fails here rather than in a session six weeks from now.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import unittest  # noqa: E402

from rules import wn_core  # noqa: E402

CONTRACT = json.loads((ROOT / "data" / "rules" / "wn_core.json").read_text(encoding="utf-8"))


class ContractAgreesWithKernelTests(unittest.TestCase):
    def test_every_attribute_score_maps_to_the_documented_modifier(self) -> None:
        table = {int(k): v for k, v in CONTRACT["stats"]["modifier_table"].items()}
        for score in range(CONTRACT["stats"]["min"], CONTRACT["stats"]["max"] + 1):
            with self.subTest(score=score):
                self.assertEqual(wn_core.attribute_modifier(score), table[score])

    def test_the_attribute_bounds_match(self) -> None:
        self.assertEqual(wn_core.ATTRIBUTE_MIN, CONTRACT["stats"]["min"])
        self.assertEqual(wn_core.ATTRIBUTE_MAX, CONTRACT["stats"]["max"])

    def test_the_difficulty_ladder_matches(self) -> None:
        documented = {int(k): v for k, v in CONTRACT["skill_check"]["difficulties"].items()}
        kernel = {
            wn_core.DIFFICULTY_SIMPLE: "Simple",
            wn_core.DIFFICULTY_SIGNIFICANT: "Significant",
            wn_core.DIFFICULTY_EXPERT: "Expert",
            wn_core.DIFFICULTY_MASTER: "Master",
            wn_core.DIFFICULTY_EXTREME: "Extreme",
        }
        self.assertEqual(kernel, documented)

    def test_the_check_dice_match(self) -> None:
        self.assertEqual(wn_core.SKILL_CHECK_DICE, CONTRACT["skill_check"]["dice_count"])
        self.assertEqual(wn_core.SKILL_CHECK_FACES, CONTRACT["skill_check"]["dice_sides"])

    def test_the_situational_and_aid_bounds_match(self) -> None:
        self.assertEqual(wn_core.SITUATIONAL_MIN, CONTRACT["modifiers"]["situational_min"])
        self.assertEqual(wn_core.SITUATIONAL_MAX, CONTRACT["modifiers"]["situational_max"])
        self.assertEqual(wn_core.AID_BONUS_MAX, CONTRACT["modifiers"]["aid_bonus_max"])

    def test_the_base_modifier_cap_matches(self) -> None:
        self.assertEqual(wn_core.MODIFIER_CAP, CONTRACT["stats"]["base_modifier_cap"])


class KernelBehaviourTests(unittest.TestCase):
    """The arithmetic the contract describes, asserted through the kernel with exact dice."""

    def test_two_d6_plus_modifier_plus_skill(self) -> None:
        result = wn_core.skill_check(
            attribute_score=14, skill_level=2, difficulty=10, dice=(5, 3)
        )
        self.assertEqual(result.attribute_modifier, 1)
        # 5 + 3 + 1 (modifier) + 2 (skill)
        self.assertEqual(sum(result.dice) + result.attribute_modifier + result.skill_level, 11)

    def test_situational_is_clamped_not_trusted(self) -> None:
        high = wn_core.skill_check(attribute_score=10, skill_level=1, difficulty=8,
                                   situational=99, dice=(1, 1))
        self.assertEqual(high.situational, CONTRACT["modifiers"]["situational_max"])
        low = wn_core.skill_check(attribute_score=10, skill_level=1, difficulty=8,
                                  situational=-99, dice=(6, 6))
        self.assertEqual(low.situational, CONTRACT["modifiers"]["situational_min"])

    def test_a_negative_skill_level_is_refused(self) -> None:
        with self.assertRaises(wn_core.WnError):
            wn_core.skill_check(attribute_score=10, skill_level=-1, difficulty=8, dice=(3, 3))

    def test_a_bad_die_face_is_refused(self) -> None:
        for bad in ((0, 3), (7, 3)):
            with self.subTest(dice=bad):
                with self.assertRaises(Exception):
                    wn_core.skill_check(attribute_score=10, skill_level=1, difficulty=8, dice=bad)

    def test_a_seed_replays_and_a_different_seed_does_not(self) -> None:
        import random

        def rolls(seed: int) -> list[tuple[int, int]]:
            return [
                tuple(wn_core.skill_check(attribute_score=10, skill_level=1, difficulty=8,
                                          rng=random.Random(seed)).dice)
                for _ in range(4)
            ]

        self.assertEqual(rolls(42), rolls(42))
        self.assertNotEqual(rolls(42), rolls(43))


if __name__ == "__main__":
    unittest.main()
