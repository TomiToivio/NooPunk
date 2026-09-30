# -*- coding: utf-8 -*-
"""Regression tests for the canonical tabletop-first skill levels from issue #14.

**Issue #22 superseded this scale.** #14 established a four-step model where level 0
meant "unskilled" and levels 1-3 gave +1/+2/+3; #22 replaced it with the
Cities-Without-Number-style **level-0..4 trained scale**, with unskilled outside the
numbered levels entirely.

These tests therefore guard two things:

1. the current canon (level-0..4, unskilled outside), so the rule cannot drift; and
2. that the withdrawn four-step model does not come back, in the documents *or* in
   the runtime adapters.

The tabletop rule is canonical on main. Nothing here creates a digital skill
implementation.
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


class SupersededScaleTests(unittest.TestCase):
    """The withdrawn #14 model must not reappear anywhere."""

    def test_old_four_step_rows_are_gone(self) -> None:
        text = _flat(RULEBOOK)
        for level, name in (("0", "unskilled"), ("1", "basic"),
                            ("2", "advanced"), ("3", "expert")):
            with self.subTest(level=level):
                self.assertNotIn(
                    f"| {level} | {name} |", text,
                    "the withdrawn #14 skill-level row is still in RULEBOOK.md",
                )

    def test_old_names_are_not_canonical_skill_levels(self) -> None:
        text = _flat(RULEBOOK)
        self.assertNotIn("1 = basic", text)
        self.assertNotIn("2 = advanced", text)
        self.assertNotIn("3 = expert", text)
        self.assertNotIn("four canonical skill levels", text)

    def test_supersession_is_stated_explicitly(self) -> None:
        """The issue requires the old rule to be marked superseded, not deleted."""
        text = _flat(RULEBOOK)
        self.assertIn("supersedes the earlier four-step skill model", text)
        self.assertIn("that model is withdrawn", text)


class CurrentScaleTests(unittest.TestCase):
    """The level-0..4 canon from #22, with unskilled outside it."""

    def test_five_trained_levels_exist(self) -> None:
        text = _flat(RULEBOOK)
        for level in ("level-0", "level-1", "level-2", "level-3", "level-4"):
            with self.subTest(level=level):
                self.assertIn(level, text)

    def test_unskilled_is_not_a_numbered_level(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("unskilled is not level-0", text)
        self.assertIn("not a numbered level at all", text)

    def test_level_modifiers_are_zero_through_four(self) -> None:
        text = _flat(RULEBOOK)
        for level, modifier in (("level-0", "+0"), ("level-1", "+1"),
                                ("level-2", "+2"), ("level-3", "+3"),
                                ("level-4", "+4")):
            with self.subTest(level=level):
                self.assertIn(f"{level}: {modifier}", text)

    def test_check_formula_still_carries_the_skill_term(self) -> None:
        text = _flat(RULEBOOK)
        # #25 converted the core check to 2d6 + skill level + attribute modifier
        self.assertIn(
            "total = 2d6 + relevant skill level + relevant attribute modifier + other applicable modifiers",
            text,
        )
        self.assertIn("success = total >= difficulty", text)


class UnskilledRulesTests(unittest.TestCase):
    """Unskilled keeps the -1 / BLOCKED behaviour; only the numbering changed."""

    def test_unskilled_penalty_and_blocking(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("-1 unskilled modifier", text)
        self.assertIn("applied exactly once", text)
        self.assertIn("blocked before rolling", text)

    def test_core_json_still_carries_the_unskilled_contract(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        self.assertEqual(canon["unskilled_penalty"], -1)
        self.assertEqual(canon["trained_only_without_skill"], "blocked")

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
        self.assertEqual(canon["opposed_rule"], "higher_total_wins")
        self.assertEqual(canon["opposed_tie"], "unresolved")


class TabletopScopeTests(unittest.TestCase):
    def test_tabletop_first_deferral_is_explicit(self) -> None:
        """#22 said "not yet ported"; #25 made the debt explicit. The guarantee
        (tabletop is canonical, the runtimes are not) is what must survive."""
        text = _flat(RULEBOOK)
        self.assertIn("port debt", text)
        self.assertIn("still implement the superseded 3d6 system", text)
        self.assertIn("this rulebook is authoritative", text)

    def test_agents_preserve_tabletop_first_scope(self) -> None:
        text = _flat(AGENTS)
        self.assertIn("level-0..4 trained skill scale", text)
        self.assertIn("tabletop first", text)

    def test_no_skill_level_runtime_table_or_adapter_implementation(self) -> None:
        """#22 is tabletop-only: no runtime may grow a skill scale."""
        canon_text = _flat(CORE_JSON)
        godot_text = _flat(GODOT_ADAPTER)
        concordia_text = _flat(CONCORDIA_MECHANICS)

        for term in ("skill_levels", "skill_level", "medical", "science"):
            with self.subTest(term=term):
                self.assertNotIn(term, canon_text)

        for term in ("skill_level", "skill levels", "medical", "science"):
            with self.subTest(runtime="godot", term=term):
                self.assertNotIn(term, godot_text)

        for term in ("skill_level", "skill levels"):
            with self.subTest(runtime="concordia", term=term):
                self.assertNotIn(term, concordia_text)


if __name__ == "__main__":
    unittest.main()
