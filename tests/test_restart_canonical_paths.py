"""The restart's canonical paths exist, stay isolated and stay empty of rules (#827).

These are guard rails, not gameplay tests: if the two canonical artefacts move, or someone quietly
imports a rule system into the empty starter, this fails.
"""
from __future__ import annotations

import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESTART = ROOT / "restart"
RULEBOOK = RESTART / "rulebook" / "RULEBOOK.md"
RULEBOOK_INDEX = RESTART / "rulebook" / "README.md"
GAME = RESTART / "game"
START_HERE = RESTART / "START_HERE.md"


class CanonicalPathTest(unittest.TestCase):
    def test_the_two_canonical_artefacts_exist(self) -> None:
        for path in (RULEBOOK, RULEBOOK_INDEX, START_HERE, GAME / "project.godot",
                     GAME / "main.tscn", GAME / "player.gd", GAME / "tests" / "smoke.gd"):
            self.assertTrue(path.exists(), path)

    def test_start_here_names_both_paths_and_the_workflow(self) -> None:
        text = START_HERE.read_text(encoding="utf-8")
        self.assertIn("restart/rulebook/RULEBOOK.md", text)
        self.assertIn("restart/game/", text)
        self.assertIn("child issue", text.lower())
        self.assertIn("--script res://tests/smoke.gd", text)

    def test_the_rulebook_says_it_is_blank_on_purpose(self) -> None:
        text = RULEBOOK.read_text(encoding="utf-8").lower()
        self.assertIn("intentionally almost empty", text)
        self.assertIn("nothing yet", text)

    def test_the_new_project_is_isolated_from_the_legacy_one(self) -> None:
        # The legacy root project must not scan the restart project.
        self.assertTrue((RESTART / ".gdignore").exists())
        legacy = (ROOT / "project.godot").read_text(encoding="utf-8")
        self.assertIn("res://scenes/main.tscn", legacy)
        self.assertNotIn("restart/game", legacy)
        restart = (GAME / "project.godot").read_text(encoding="utf-8")
        self.assertIn("res://main.tscn", restart)


class NoRulesIntroducedTest(unittest.TestCase):
    """The milestone forbids rules. A starter that grows a stat block is a scope failure."""

    FORBIDDEN = ("attribute", "strength", "dexterity", "hit_points", "hp_max", "damage",
                 "initiative", "skill_rank", "inventory", "dialogue", "quest", "strain", "psionic")

    def test_the_starter_carries_no_rule_system(self) -> None:
        sources = [GAME / "player.gd", GAME / "main.tscn", GAME / "project.godot"]
        for path in sources:
            # Comments declare what is *absent* ("no combat, no inventory"); the guard reads code and
            # config only, so prose cannot trip it and cannot hide a mechanic either.
            lines = [line for line in path.read_text(encoding="utf-8").splitlines()
                     if not line.lstrip().startswith((";", "#"))]
            text = "\n".join(lines).lower()
            for word in self.FORBIDDEN:
                self.assertNotIn(word, text, f"{path.name} mentions {word!r}")

    def test_the_rulebook_has_no_mechanical_tables(self) -> None:
        text = RULEBOOK.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"^\|.*d6.*\|", text, re.MULTILINE),
                          "an attribute or dice table has crept into the blank rulebook")

    def test_the_legacy_rulebook_is_untouched_by_the_restart(self) -> None:
        legacy = ROOT / "rulebook" / "RULEBOOK.md"
        if legacy.exists():
            self.assertNotIn("restart/rulebook", legacy.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
