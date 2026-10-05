"""Focused tests for issue #111: independent NoöPunk d10 core."""

from __future__ import annotations

from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concordia_runtime import resolve_structured_check
from rules import (
    AttributeSet,
    CHECK_DICE,
    DIFFICULTIES,
    DIFFICULTY_LADDER,
    SKILL_LEVEL_MAX,
    SKILL_LEVEL_MIN,
    STAT_MAX,
    STAT_MIN,
    compare_opposed,
    resolve_check,
    roll_d10,
)


class FixedDice:
    def __init__(self, values: list[int]) -> None:
        self.values = iter(values)

    def randint(self, a: int, b: int) -> int:
        value = next(self.values)
        if value < a or value > b:
            raise AssertionError("Fixed die outside requested bounds")
        return value


class CoreRulesTests(unittest.TestCase):
    def test_system_is_independent_and_lists_multiple_influences(self) -> None:
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        self.assertTrue(canon["system_identity"]["independent"])
        self.assertGreaterEqual(len(canon["system_identity"]["influences"]), 5)
        self.assertIn("Eclipse Phase", canon["system_identity"]["not_a_conversion_of"])

    def test_stats_and_skills_are_one_to_ten(self) -> None:
        self.assertEqual((STAT_MIN, STAT_MAX), (1, 10))
        self.assertEqual((SKILL_LEVEL_MIN, SKILL_LEVEL_MAX), (1, 10))
        AttributeSet({"BODY": 1, "MIND": 10})
        for bad in (0, 11):
            with self.assertRaises(ValueError):
                AttributeSet({"BODY": bad})

    def test_final_stat_list_is_locked_and_skill_list_is_deferred(self) -> None:
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        self.assertEqual(canon["stats"]["final_list"], ["FIT", "REF", "INT", "SOC", "CYB", "PSY"])
        self.assertEqual(canon["skills"]["final_list"], "deferred")

    def test_skill_check_engine_is_1d10(self) -> None:
        self.assertEqual(CHECK_DICE, "1d10")
        self.assertEqual(roll_d10(FixedDice([1])), 1)
        self.assertEqual(roll_d10(FixedDice([10])), 10)

    def test_canonical_difficulty_ladder(self) -> None:
        self.assertEqual(DIFFICULTY_LADDER, (9, 13, 15, 17, 21, 24, 29))
        self.assertEqual(
            DIFFICULTIES,
            {9: "Simple", 13: "Everyday", 15: "Difficult", 17: "Professional",
             21: "Heroic", 24: "Incredible", 29: "Legendary"},
        )

    def test_check_is_stat_plus_skill_plus_d10(self) -> None:
        result = resolve_check(stat=6, skill=5, target=17, die=6)
        self.assertEqual(result.total, 17)
        self.assertTrue(result.success)
        fail = resolve_check(stat=6, skill=5, target=17, die=5)
        self.assertFalse(fail.success)

    def test_invalid_stat_skill_and_die_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            resolve_check(stat=0, skill=5, target=13, die=5)
        with self.assertRaises(ValueError):
            resolve_check(stat=5, skill=11, target=13, die=5)
        with self.assertRaises(ValueError):
            resolve_check(stat=5, skill=5, target=13, die=0)

    def test_opposed_higher_total_wins_and_ties_remain_open(self) -> None:
        self.assertEqual(compare_opposed(20, 18).winner, "left")
        self.assertEqual(compare_opposed(18, 20).winner, "right")
        tie = compare_opposed(20, 20)
        self.assertIsNone(tie.winner)
        self.assertTrue(tie.unresolved_tie)

    def test_concordia_uses_same_shared_resolution(self) -> None:
        stats = AttributeSet({"REF": 7})
        result = resolve_structured_check(
            attributes=stats,
            attribute_id="REF",
            target=15,
            skill_level=4,
            dice_total=4,
        )
        self.assertEqual(result["total"], 15)
        self.assertTrue(result["success"])

    def test_probability_examples_are_recorded(self) -> None:
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        probs = canon["probability_examples"]
        self.assertEqual(probs["Professional STAT 6 + Skill 5"]["17"], 0.5)
        self.assertEqual(probs["Expert STAT 7 + Skill 7"]["21"], 0.4)
        self.assertEqual(probs["Elite STAT 8 + Skill 9"]["24"], 0.4)

    def test_godot_adapter_uses_shared_d10_canon(self) -> None:
        source = (ROOT / "src" / "godot" / "core_rules.gd").read_text(encoding="utf-8")
        self.assertIn("res://data/rules/core.json", source)
        self.assertIn("func roll_d10", source)
        self.assertIn("var total := stat + skill + die", source)
        self.assertNotIn("roll_2d6", source)


if __name__ == "__main__":
    unittest.main()
