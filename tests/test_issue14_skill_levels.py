# -*- coding: utf-8 -*-
"""Regression tests for the canonical tabletop-first skill levels from issue #14.

The tabletop rule is already canonical on main. These tests guard that definition
without creating a digital skill implementation.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"
AGENTS = ROOT / "AGENTS.md"
CORE_JSON = ROOT / "data" / "rules" / "core.json"
GODOT_ADAPTER = ROOT / "src" / "godot" / "core_rules.gd"
CONCORDIA_MECHANICS = ROOT / "src" / "concordia_runtime" / "mechanics.py"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(path: Path) -> str:
    return " ".join(_text(path).split()).lower()


class SkillLevelCanonTests(unittest.TestCase):
    def test_exact_four_skill_levels(self) -> None:
        text = _flat(RULEBOOK)
        for level, name, modifier in (
            ("0", "unskilled", "special"),
            ("1", "basic", "+1"),
            ("2", "advanced", "+2"),
            ("3", "expert", "+3"),
        ):
            with self.subTest(level=level):
                self.assertIn(f"| {level} | {name} | {modifier} |", text)

    def test_level_zero_means_no_skill(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("level 0 is the absence of the skill", text)
        self.assertIn("unskilled allowed", text)
        self.assertIn("skill required / trained-only", text)

    def test_trained_levels_have_expected_modifiers(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("1 = basic", text)
        self.assertIn("2 = advanced", text)
        self.assertIn("3 = expert", text)
        self.assertIn("+1/+2/+3", text)

    def test_check_formula_includes_skill_modifier(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn(
            "total = 3d6 + relevant attribute modifier + skill modifier + other applicable modifiers",
            text,
        )
        self.assertIn("success = total >= difficulty target", text)

    def test_unskilled_penalty_and_blocking(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("-1 unskilled modifier", text)
        self.assertIn("applied exactly once", text)
        self.assertIn("blocked before rolling", text)

    def test_issue_11_difficulty_ladder_preserved(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        self.assertEqual(
            canon["difficulties"],
            {
                "Easiest": 3,
                "Easier": 6,
                "Easy": 9,
                "Normal": 12,
                "Hard": 15,
                "Impossible": 18,
            },
        )
        self.assertEqual(canon["unskilled_penalty"], -1)
        self.assertEqual(canon["trained_only_without_skill"], "blocked")
        self.assertEqual(canon["opposed_rule"], "higher_total_wins")
        self.assertEqual(canon["opposed_tie"], "unresolved")

    def test_skill_catalog_and_progression_remain_undefined(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("skill catalog", text)
        self.assertIn("not defined", text)
        self.assertIn("advancement", text)
        self.assertIn("**unspecified.**", text)

    def test_tabletop_first_deferral_is_explicit(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("tabletop-first and not yet ported", text)
        self.assertIn("godot and concordia do not implement them yet", text)

    def test_agents_preserve_tabletop_first_scope(self) -> None:
        text = _flat(AGENTS)
        self.assertIn("four canonical skill levels", text)
        self.assertIn("a skill list or skill catalog", text)
        self.assertIn("tabletop first", text)

    def test_no_skill_level_runtime_table_or_adapter_implementation(self) -> None:
        canon_text = _flat(CORE_JSON)
        godot_text = _flat(GODOT_ADAPTER)
        concordia_text = _flat(CONCORDIA_MECHANICS)

        for term in ("basic", "advanced", "expert", "skill_levels", "skill_level"):
            with self.subTest(term=term):
                self.assertNotIn(term, canon_text)

        for term in ("skill_level", "skill levels", "basic", "advanced", "expert"):
            with self.subTest(runtime="godot", term=term):
                self.assertNotIn(term, godot_text)

        for term in ("skill_level", "skill levels", "skill modifier"):
            with self.subTest(runtime="concordia", term=term):
                self.assertNotIn(term, concordia_text)


if __name__ == "__main__":
    unittest.main()
