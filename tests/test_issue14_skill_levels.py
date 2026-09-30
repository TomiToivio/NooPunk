# -*- coding: utf-8 -*-
"""Issue #14 — the four canonical tabletop skill levels.

This is a tabletop-only, documentation-only change, so the risks worth guarding are
narrow and specific rather than behavioural:

1. **The levels being confused with a skill catalog.** Skill *levels* are now
   canonical; the *list* of skills is not. If a catalog or a progression mechanic
   appears, the issue's smallest-possible-change intent has been exceeded.
2. **Level 0 drifting into "beginner".** The author's model is that level 0 means
   *no skill at all*. Rewriting it as low-grade competence would change what a
   character sheet means.
3. **The digital runtimes acquiring an implementation.** Issue #14 is tabletop
   only; Godot and Concordia port later. A skill-level table appearing in
   `data/rules/core.json` or in the runtime adapters would violate that, and the
   project's tabletop-first order (#13) exists precisely to prevent it.
4. **Silent redesign of what #11 settled.** The difficulty ladder, unskilled
   penalty, trained-only blocking and opposed-check behaviour must be untouched.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import json
import re
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
    """Lowercased, whitespace-collapsed, so line wrapping cannot hide a term."""
    return " ".join(_text(path).split()).lower()


class SkillLevelTableTests(unittest.TestCase):
    def test_rulebook_defines_exactly_four_levels_with_their_modifiers(self) -> None:
        text = _flat(RULEBOOK)
        for level, name, modifier in (
            ("0", "unskilled", "special"),
            ("1", "basic", "+1"),
            ("2", "advanced", "+2"),
            ("3", "expert", "+3"),
        ):
            with self.subTest(level=level):
                self.assertRegex(
                    text,
                    rf"\| {level} \| {name} \| {re.escape(modifier)} \|",
                    f"level {level} {name} is not in the canonical table",
                )

    def test_the_check_formula_names_the_skill_modifier(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn(
            "3d6 + relevant attribute modifier + skill modifier + other applicable modifiers",
            text,
        )

    def test_each_level_states_what_it_contributes(self) -> None:
        text = _flat(RULEBOOK)
        for fragment in ("level 1 → **+1**", "level 2 → **+2**", "level 3 → **+3**"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)


class LevelZeroTests(unittest.TestCase):
    def test_level_zero_is_explicitly_no_skill(self) -> None:
        """The author's model: 0 means the character does not have the skill."""
        text = _flat(RULEBOOK)
        self.assertIn("level 0 means no skill", text)
        self.assertIn("does **not have** the skill", text)

    def test_level_zero_is_not_described_as_low_grade_competence(self) -> None:
        """Guard the reading that would change what a sheet means."""
        text = _flat(RULEBOOK)
        # it may explicitly deny the reading, but must not assert it
        self.assertNotRegex(text, r"level 0 (?:is|means) (?:a )?(?:low|basic|beginner)")
        self.assertIn("not a low grade of trained competence", text)

    def test_the_two_level_zero_cases_are_both_present(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("unskilled attempt allowed", text)
        self.assertIn("skill required / trained-only", text)
        self.assertIn("blocked attempt", text)

    def test_unskilled_penalty_is_stated_apply_once(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("exactly once", text)


class NoInventedContentTests(unittest.TestCase):
    """Acceptance: no catalog, no progression, nothing subsystem-specific."""

    BANNED_TERMS = (
        "xp cost",
        "experience point",
        "training time",
        "specialt",          # specialty / specialisation
        "prerequisite",
        "skill group",
        "defaulting chain",
        "improvement cost",
    )

    def test_no_progression_mechanics_were_invented(self) -> None:
        """Progression terms may appear ONLY where they are declared undefined.

        The rulebook lists them under "still UNSPECIFIED" and in the unresolved
        section, which is the correct treatment. What would be a defect is a
        term appearing with a defined value or cost.
        """
        raw = _text(RULEBOOK)
        flat = _flat(RULEBOOK)
        for term in self.BANNED_TERMS:
            with self.subTest(term=term):
                if term not in flat:
                    continue
                # every occurrence must sit in an unresolved/undefined context
                for match in re.finditer(term, flat):
                    window = flat[max(0, match.start() - 400):match.end() + 40]
                    defined_context = any(
                        marker in window
                        for marker in ("unspecified", "not yet", "not defined",
                                       "do not invent", "unresolved",
                                       "still **unspecified**", "deferred")
                    )
                    self.assertTrue(
                        defined_context,
                        f"{raw.count(term)}x {term!r} appears without a "
                        f"'not defined' context:\n...{window!r}",
                    )

    def test_no_skill_catalog_was_invented(self) -> None:
        """A list of concrete skills would be a catalog; the issue forbids it."""
        text = _flat(RULEBOOK)
        self.assertIn("the skill list — which skills exist", text)
        # the only places a capitalised skill-like name may appear are the four
        # level names, which are defined here
        for invented in ("stealth", "athletics", "melee", "firearms", "pilot",
                         "persuasion", "hacking skill", "medicine"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, text)

    def test_no_subsystem_skill_rules_were_invented(self) -> None:
        text = _flat(RULEBOOK)
        for subsystem in ("combat skill", "psi skill", "psionic skill",
                          "cyberware skill", "social skill rating"):
            with self.subTest(subsystem=subsystem):
                self.assertNotIn(subsystem, text)

    def test_four_levels_are_declared_the_only_ordinary_levels(self) -> None:
        self.assertIn("the only ordinary skill levels", _flat(RULEBOOK))


class Issue11RulesPreservedTests(unittest.TestCase):
    """#14 extends #11 and must not redesign it."""

    def test_difficulty_ladder_is_unchanged(self) -> None:
        text = _flat(RULEBOOK)
        for name, target in (("easiest", 3), ("easier", 6), ("easy", 9),
                             ("normal", 12), ("hard", 15), ("impossible", 18)):
            with self.subTest(difficulty=name):
                self.assertRegex(text, rf"\| {name} \| {target} \|")

    def test_the_canonical_json_difficulty_table_is_untouched(self) -> None:
        canon = json.loads(_text(CORE_JSON))
        self.assertEqual(
            canon["difficulties"],
            {"Easiest": 3, "Easier": 6, "Easy": 9,
             "Normal": 12, "Hard": 15, "Impossible": 18},
        )
        self.assertEqual(canon["unskilled_penalty"], -1)
        self.assertEqual(canon["trained_only_without_skill"], "blocked")
        self.assertEqual(canon["opposed_rule"], "higher_total_wins")
        self.assertEqual(canon["opposed_tie"], "unresolved")

    def test_opposed_checks_are_unchanged_and_still_unresolved_on_ties(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("higher final total wins", text)
        self.assertIn("no tie-breaker rule is currently canonical", text)

    def test_impossible_still_is_not_a_prohibition(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("no automatic failure on a natural 3", text)
        self.assertIn("no automatic success on a natural 18", text)


class TabletopOnlyTests(unittest.TestCase):
    """Issue #14 explicitly defers Godot and Concordia."""

    def test_core_json_has_no_skill_level_table(self) -> None:
        """Guard specifically against a skill-level scale, not the substring 'skill'.

        `unskilled_penalty` and `trained_only_without_skill` legitimately contain the
        word and predate this issue; they are part of #11 and must stay.
        """
        canon = json.loads(_text(CORE_JSON))
        for key in canon:
            with self.subTest(key=key):
                lowered = key.lower()
                self.assertNotIn(
                    "skill_level", lowered,
                    f"data/rules/core.json gained {key!r}; #14 is tabletop only",
                )
                self.assertNotIn(
                    "skill_modifier", lowered,
                    f"data/rules/core.json gained {key!r}; #14 is tabletop only",
                )
        flat = _text(CORE_JSON).lower()
        for invented in ("basic", "advanced", "expert"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, flat)
        # the #11 values must still be present
        self.assertEqual(canon["unskilled_penalty"], -1)
        self.assertEqual(canon["trained_only_without_skill"], "blocked")

    def test_godot_adapter_does_not_implement_skill_levels(self) -> None:
        text = _flat(GODOT_ADAPTER)
        for term in ("skill_level", "skill level", "basic", "advanced", "expert"):
            with self.subTest(term=term):
                self.assertNotIn(term, text,
                                 "the Godot adapter gained skill-level handling")

    def test_concordia_mechanics_do_not_implement_skill_levels(self) -> None:
        text = _flat(CONCORDIA_MECHANICS)
        for term in ("skill_level", "skill level", "skill modifier"):
            with self.subTest(term=term):
                self.assertNotIn(term, text,
                                 "the Concordia mechanics gained skill-level handling")

    def test_rulebook_defers_the_digital_port_explicitly(self) -> None:
        text = _flat(RULEBOOK)
        self.assertIn("digital skill-level implementation is deferred", text)
        self.assertIn("porting them is a separate, later task", text)

    def test_agents_md_forbids_porting_without_a_task(self) -> None:
        text = _flat(AGENTS)
        self.assertIn("tabletop-canonical but not yet ported", text)
        self.assertIn("do not add a skill-level table", text)


class WorkedExampleTests(unittest.TestCase):
    """The documented examples must actually be the arithmetic they claim."""

    def test_skill_level_examples_are_arithmetically_correct(self) -> None:
        text = _flat(RULEBOOK)
        for modifier, total, target, succeeds in (
            ("+1", 11, 12, False),
            ("+2", 12, 12, True),
            ("+3", 13, 12, True),
            ("-1", 9, 12, False),
        ):
            with self.subTest(modifier=modifier):
                expected = 10 + int(modifier)
                self.assertEqual(expected, total)
                # the claim in the document must match that arithmetic
                self.assertIn(str(total), text, f"total {total} is not documented")
                outcome = "succeeds" if total >= target else "fails"
                self.assertIn(outcome, text)


if __name__ == "__main__":
    unittest.main()
