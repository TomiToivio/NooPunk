"""Focused tests for the canonical NoöPunk attribute and check rules."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import (
    ATTRIBUTE_IDS,
    DIFFICULTIES,
    UNSKILLED_PENALTY,
    AttributeSet,
    SkillAccess,
    compare_opposed,
    generate_human_attributes,
    human_modifier,
    resolve_check,
)


EXPECTED_MODIFIERS = {
    3: -3, 4: -2, 5: -2, 6: -1, 7: -1, 8: -1,
    9: 0, 10: 0, 11: 0, 12: 0,
    13: 1, 14: 1, 15: 1, 16: 2, 17: 2, 18: 3,
}


class FixedDice:
    def __init__(self, values: list[int]) -> None:
        self.values = iter(values)

    def randint(self, a: int, b: int) -> int:
        value = next(self.values)
        if value < a or value > b:
            raise AssertionError("Fixed die outside requested bounds")
        return value


class CoreRulesTests(unittest.TestCase):
    def test_six_attribute_identifiers(self) -> None:
        self.assertEqual(ATTRIBUTE_IDS, ("FIT", "REF", "INT", "CHA", "CYB", "PSY"))

    def test_every_human_3d6_modifier_boundary_and_value(self) -> None:
        for raw, expected in EXPECTED_MODIFIERS.items():
            with self.subTest(raw=raw):
                self.assertEqual(human_modifier(raw), expected)
        for raw in (2, 19):
            with self.assertRaises(ValueError):
                human_modifier(raw)

    def test_human_generation_preserves_raw_rolls_and_modifiers(self) -> None:
        dice = FixedDice([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6])
        generated = generate_human_attributes(dice)
        self.assertEqual(set(generated.raw_rolls), set(ATTRIBUTE_IDS))
        self.assertTrue(all(3 <= value <= 18 for value in generated.raw_rolls.values()))
        for attribute_id, raw in generated.raw_rolls.items():
            self.assertEqual(generated.modifiers[attribute_id], human_modifier(raw))

    def test_canonical_difficulties(self) -> None:
        self.assertEqual(
            DIFFICULTIES,
            {"Easiest": 3, "Easier": 6, "Easy": 9, "Hard": 12, "Harder": 15, "Hardest": 18},
        )

    def test_meeting_target_succeeds_and_below_fails(self) -> None:
        self.assertTrue(resolve_check(attribute_modifier=0, target=9, dice_total=9).success)
        self.assertFalse(resolve_check(attribute_modifier=0, target=10, dice_total=9).success)

    def test_positive_and_negative_extra_modifiers(self) -> None:
        positive = resolve_check(attribute_modifier=1, target=12, dice_total=9, extra_modifiers=(2,))
        negative = resolve_check(attribute_modifier=1, target=12, dice_total=12, extra_modifiers=(-2,))
        self.assertEqual(positive.total, 12)
        self.assertTrue(positive.success)
        self.assertEqual(negative.total, 11)
        self.assertFalse(negative.success)

    def test_unskilled_penalty_is_minus_one(self) -> None:
        self.assertEqual(UNSKILLED_PENALTY, -1)
        result = resolve_check(attribute_modifier=0, target=8, dice_total=9, has_skill=False)
        self.assertEqual(result.unskilled_modifier, -1)
        self.assertEqual(result.total, 8)
        self.assertTrue(result.success)

    def test_trained_only_attempt_is_blocked_without_skill(self) -> None:
        result = resolve_check(
            attribute_modifier=3,
            target=3,
            skill_access=SkillAccess.TRAINED_ONLY,
            has_skill=False,
            dice_total=18,
        )
        self.assertFalse(result.attempted)
        self.assertIsNone(result.total)
        self.assertIsNone(result.success)
        self.assertEqual(result.blocked_reason, "trained_only_without_skill")

    def test_opposed_higher_total_wins_and_tie_is_unresolved(self) -> None:
        self.assertEqual(compare_opposed(12, 9).winner, "left")
        self.assertEqual(compare_opposed(9, 12).winner, "right")
        tie = compare_opposed(12, 12)
        self.assertIsNone(tie.winner)
        self.assertTrue(tie.unresolved_tie)

    def test_attribute_model_allows_future_values_outside_human_range(self) -> None:
        attributes = AttributeSet({"FIT": 4, "REF": -4, "INT": 0, "CHA": 0, "CYB": 7, "PSY": -9})
        self.assertEqual(attributes["FIT"], 4)
        self.assertEqual(attributes["REF"], -4)
        self.assertEqual(attributes["CYB"], 7)
        self.assertEqual(attributes["PSY"], -9)

    def test_godot_adapter_reads_shared_canon(self) -> None:
        source = (ROOT / "src" / "godot" / "core_rules.gd").read_text(encoding="utf-8")
        self.assertIn('res://data/rules/core.json', source)
        for attribute_id in ATTRIBUTE_IDS:
            self.assertNotIn('"' + attribute_id + '":', source)


if __name__ == "__main__":
    unittest.main()
