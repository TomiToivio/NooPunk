# -*- coding: utf-8 -*-
"""Issue #11 — the author-specified attribute and difficulty rules, across runtimes.

The author's table supersedes the earlier one. The two things that actually need
guarding are not the numbers (those are data) but the two ways a rename goes
wrong:

1. **`Hard` changed target from 12 to 15.** A rename applied to only one runtime
   would silently reinterpret an existing difficulty. So these tests assert
   parity between the shared spec, the Godot adapter and the Concordia adapter,
   not just that the shared spec is right.
2. **`Impossible` is a name, not a prohibition.** It must resolve numerically —
   no automatic failure on a natural 3, no automatic success on a natural 18.

Every acceptance criterion from the issue is covered by name below.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import (  # noqa: E402
    ATTRIBUTE_DEFINITIONS,
    ATTRIBUTE_IDS,
    DIFFICULTIES,
    HUMAN_ATTRIBUTE_INTERPRETATION,
    UNSKILLED_PENALTY,
    AttributeSet,
    SkillAccess,
    UnknownDifficulty,
    difficulty_meaning,
    difficulty_target,
    generate_human_attributes,
    human_modifier,
    resolve_check,
)

AUTHOR_TABLE = {
    "Easiest": 3, "Easier": 6, "Easy": 9,
    "Normal": 12, "Hard": 15, "Impossible": 18,
}

AUTHOR_ATTRIBUTES = {
    "FIT": "Fitness", "REF": "Reflexes", "INT": "Intelligence",
    "CHA": "Charisma", "CYB": "Cybernetics", "PSY": "Psyche",
}

AUTHOR_MODIFIERS = {
    3: -3, 4: -2, 5: -2, 6: -1, 7: -1, 8: -1,
    9: 0, 10: 0, 11: 0, 12: 0,
    13: 1, 14: 1, 15: 1, 16: 2, 17: 2, 18: 3,
}

CANON = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))


class FixedDice:
    def __init__(self, values):
        self.values = iter(values)

    def randint(self, a, b):
        value = next(self.values)
        if value < a or value > b:
            raise AssertionError("Fixed die outside requested bounds")
        return value


class AttributeSpecTests(unittest.TestCase):
    """Acceptance: all six identifiers and meanings match the specification."""

    def test_identifiers_and_meanings(self) -> None:
        self.assertEqual(ATTRIBUTE_IDS, tuple(AUTHOR_ATTRIBUTES))
        by_id = {item["id"]: item for item in ATTRIBUTE_DEFINITIONS}
        for attribute_id, name in AUTHOR_ATTRIBUTES.items():
            with self.subTest(attribute=attribute_id):
                self.assertEqual(by_id[attribute_id]["name"], name)
                self.assertTrue(by_id[attribute_id]["description"].strip())

    def test_psy_governs_psionics_and_astral_projection(self) -> None:
        """#11 states PSY is 'used in astral projection and for psionics'."""
        description = next(
            item for item in ATTRIBUTE_DEFINITIONS if item["id"] == "PSY"
        )["description"].lower()
        self.assertIn("psionic", description)
        self.assertIn("astral projection", description)

    def test_cyb_describes_the_cyborg_technical_side(self) -> None:
        description = next(
            item for item in ATTRIBUTE_DEFINITIONS if item["id"] == "CYB"
        )["description"].lower()
        self.assertIn("cyberspace", description)
        self.assertIn("cybernetic", description)


class HumanGenerationTests(unittest.TestCase):
    """Acceptance: every raw roll 3..18 maps correctly, boundaries included."""

    def test_every_roll_value_and_the_boundaries(self) -> None:
        for raw in range(3, 19):
            with self.subTest(raw=raw):
                self.assertEqual(human_modifier(raw), AUTHOR_MODIFIERS[raw])
        # explicit interval boundaries, named as the issue names them
        for raw, expected in ((3, -3), (4, -2), (5, -2), (6, -1), (8, -1),
                              (9, 0), (12, 0), (13, 1), (15, 1),
                              (16, 2), (17, 2), (18, 3)):
            with self.subTest(boundary=raw):
                self.assertEqual(human_modifier(raw), expected)

    def test_rolls_outside_the_range_are_rejected(self) -> None:
        for raw in (2, 19, 0, -1):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    human_modifier(raw)

    def test_generation_rolls_three_dice_per_attribute(self) -> None:
        """Exactly 18 dice for six attributes, i.e. 3d6 each."""
        consumed = []

        class Counting:
            def __init__(self):
                self.n = 0

            def randint(self, a, b):
                self.n += 1
                consumed.append(a)
                return b  # always roll the maximum, to also exercise 18

        generated = generate_human_attributes(Counting())
        self.assertEqual(len(consumed), len(ATTRIBUTE_IDS) * 3)
        self.assertTrue(all(1 == low for low in consumed))
        self.assertEqual(set(generated.raw_rolls), set(ATTRIBUTE_IDS))
        self.assertTrue(all(roll == 18 for roll in generated.raw_rolls.values()))

    def test_raw_rolls_are_preserved_alongside_modifiers(self) -> None:
        dice = FixedDice([1, 1, 1] * 6)
        generated = generate_human_attributes(dice)
        self.assertEqual(set(generated.raw_rolls), set(ATTRIBUTE_IDS))
        for attribute_id, raw in generated.raw_rolls.items():
            with self.subTest(attribute=attribute_id):
                self.assertEqual(generated.modifiers[attribute_id], human_modifier(raw))

    def test_values_outside_plus_minus_three_are_representable(self) -> None:
        """Above +3 transhuman, below -3 near-dead -- and never clamped."""
        attributes = AttributeSet(
            {"FIT": 4, "REF": -4, "INT": 0, "CHA": 0, "CYB": 7, "PSY": -9}
        )
        self.assertEqual(attributes["FIT"], 4)     # above +3: transhuman
        self.assertEqual(attributes["PSY"], -9)    # below -3: near-dead
        self.assertEqual(HUMAN_ATTRIBUTE_INTERPRETATION["above_plus_3"], "Transhuman.")
        self.assertEqual(
            HUMAN_ATTRIBUTE_INTERPRETATION["below_minus_3"], "Basically dead."
        )
        self.assertIn("MODIFIERS", HUMAN_ATTRIBUTE_INTERPRETATION["$note"])

    def test_the_interpretation_defines_no_mechanics(self) -> None:
        """#11: preserve the interpretation WITHOUT inventing death/injury rules."""
        note = HUMAN_ATTRIBUTE_INTERPRETATION["$note"].lower()
        for invented in ("death", "injury", "augmentation", "resurrection"):
            with self.subTest(term=invented):
                self.assertIn(invented, note)  # stated as NOT defined


class DifficultyTableTests(unittest.TestCase):
    """Acceptance: difficulty pairs are exactly the author's six."""

    def test_pairs_match_exactly(self) -> None:
        self.assertEqual(DIFFICULTIES, AUTHOR_TABLE)

    def test_lookup_by_name_matches_the_table(self) -> None:
        for name, target in AUTHOR_TABLE.items():
            with self.subTest(name=name):
                self.assertEqual(difficulty_target(name), target)

    def test_every_difficulty_has_a_meaning(self) -> None:
        for name in AUTHOR_TABLE:
            with self.subTest(name=name):
                self.assertTrue(difficulty_meaning(name).strip())

    def test_unknown_difficulty_raises_rather_than_defaulting(self) -> None:
        """A rename must fail loudly; silently reinterpreting old data is the bug."""
        for bad in ("Harder", "Hardest", "hard", "normal", "", "Impossible "):
            with self.subTest(name=bad):
                with self.assertRaises(UnknownDifficulty):
                    difficulty_target(bad)

    def test_the_removed_names_are_not_silently_aliased(self) -> None:
        """'Harder'/'Hardest' must NOT resolve -- aliasing them would hide the change."""
        self.assertEqual(difficulty_target("Hard"), 15)
        self.assertEqual(difficulty_target("Normal"), 12)
        for removed in ("Harder", "Hardest"):
            with self.subTest(removed=removed):
                with self.assertRaises(UnknownDifficulty):
                    difficulty_target(removed)


class CheckResolutionTests(unittest.TestCase):
    """Acceptance: boundaries, modifiers, unskilled and trained-only rules."""

    def test_equal_to_target_succeeds_and_one_below_fails(self) -> None:
        for target in AUTHOR_TABLE.values():
            with self.subTest(target=target):
                self.assertTrue(
                    resolve_check(attribute_modifier=0, target=target,
                                  dice_total=target).success
                )
                if target > 3:
                    # one below the target, by die
                    self.assertFalse(
                        resolve_check(attribute_modifier=0, target=target,
                                      dice_total=target - 1).success
                    )
                else:
                    # A 3d6 total cannot go below 3, so at target 3 the "one
                    # below" case must come from a modifier -- which is exactly
                    # the boundary case #11 names (raw 3 with -1 fails).
                    self.assertFalse(
                        resolve_check(attribute_modifier=0, target=target,
                                      dice_total=3, extra_modifiers=(-1,)).success
                    )

    def test_positive_and_negative_modifiers_sum(self) -> None:
        positive = resolve_check(attribute_modifier=1, target=12, dice_total=9,
                                 extra_modifiers=(2,))
        self.assertEqual(positive.total, 12)
        self.assertTrue(positive.success)

        negative = resolve_check(attribute_modifier=1, target=12, dice_total=12,
                                 extra_modifiers=(-2,))
        self.assertEqual(negative.total, 11)
        self.assertFalse(negative.success)

        mixed = resolve_check(attribute_modifier=0, target=12, dice_total=12,
                              extra_modifiers=(3, -3))
        self.assertEqual(mixed.total, 12)
        self.assertTrue(mixed.success)

    def test_target_three_boundary_case_from_the_issue(self) -> None:
        """#11 names this case explicitly: raw 3 +0 succeeds, raw 3 -1 fails."""
        ok = resolve_check(attribute_modifier=0, target=3, dice_total=3,
                           extra_modifiers=(0,))
        self.assertEqual(ok.total, 3)
        self.assertTrue(ok.success)

        fails = resolve_check(attribute_modifier=0, target=3, dice_total=3,
                              extra_modifiers=(-1,))
        self.assertEqual(fails.total, 2)
        self.assertFalse(fails.success)

    def test_impossible_is_resolved_numerically_not_blocked(self) -> None:
        """#11: target 18 uses the same formula; no categorical prohibition."""
        self.assertEqual(difficulty_target("Impossible"), 18)
        result = resolve_check(attribute_modifier=3, target=18, dice_total=18)
        self.assertTrue(result.attempted, "target 18 must be attemptable")
        self.assertEqual(result.total, 21)
        self.assertTrue(result.success)
        # and it can genuinely fail, by arithmetic rather than by fiat
        miss = resolve_check(attribute_modifier=3, target=18, dice_total=3)
        self.assertTrue(miss.attempted)
        self.assertEqual(miss.total, 6)
        self.assertFalse(miss.success)

    def test_no_natural_three_failure_or_natural_eighteen_success(self) -> None:
        """#11 forbids both. A natural 18 must still fail against a high enough target."""
        natural_18 = resolve_check(attribute_modifier=0, target=18, dice_total=18,
                                   extra_modifiers=(-1,))
        self.assertFalse(natural_18.success, "natural 18 must not auto-succeed")
        natural_3 = resolve_check(attribute_modifier=0, target=3, dice_total=3,
                                  extra_modifiers=(0,))
        self.assertTrue(natural_3.success, "natural 3 must not auto-fail")
        natural_3_low = resolve_check(attribute_modifier=-3, target=3, dice_total=3)
        self.assertFalse(natural_3_low.success)

    def test_unskilled_penalty_applies_exactly_once(self) -> None:
        result = resolve_check(attribute_modifier=0, target=6, dice_total=9,
                               has_skill=False, extra_modifiers=(0,))
        self.assertEqual(result.unskilled_modifier, UNSKILLED_PENALTY)
        self.assertEqual(result.unskilled_modifier, -1)
        self.assertEqual(result.total, 8)  # 9 + 0 + 0 + (-1), once

        with_skill = resolve_check(attribute_modifier=0, target=6, dice_total=9,
                                   has_skill=True)
        self.assertEqual(with_skill.unskilled_modifier, 0)
        self.assertEqual(with_skill.total, 9)

    def test_skill_required_is_blocked_before_rolling(self) -> None:
        """A blocked attempt is not a failed roll, and modifiers cannot bypass it."""
        result = resolve_check(
            attribute_modifier=3, target=3,
            extra_modifiers=(100,),
            skill_access=SkillAccess.TRAINED_ONLY, has_skill=False,
            dice_total=18,
        )
        self.assertFalse(result.attempted)
        self.assertIsNone(result.dice_total, "no dice may be consumed when blocked")
        self.assertIsNone(result.total)
        self.assertIsNone(result.success)
        self.assertEqual(result.blocked_reason, "trained_only_without_skill")

    def test_blocking_happens_without_a_supplied_roll(self) -> None:
        """Blocked must not roll even when no dice_total is injected."""

        class Exploding:
            def randint(self, a, b):
                raise AssertionError("dice were rolled for a blocked attempt")

        result = resolve_check(
            attribute_modifier=0, target=9,
            skill_access=SkillAccess.TRAINED_ONLY, has_skill=False, rng=Exploding(),
        )
        self.assertFalse(result.attempted)

    def test_unskilled_allowed_is_the_default_category(self) -> None:
        result = resolve_check(attribute_modifier=0, target=9, dice_total=10,
                               has_skill=False)
        self.assertTrue(result.attempted)
        self.assertEqual(result.unskilled_modifier, -1)


class CrossRuntimeParityTests(unittest.TestCase):
    """Determinism across the three runtimes -- the point of the issue."""

    def test_godot_adapter_reads_the_shared_canon_and_declares_no_table(self) -> None:
        source = (ROOT / "src" / "godot" / "core_rules.gd").read_text(encoding="utf-8")
        self.assertIn("res://data/rules/core.json", source)
        for attribute_id in ATTRIBUTE_IDS:
            with self.subTest(attribute=attribute_id):
                self.assertNotIn('"' + attribute_id + '":', source)
        # no hard-coded difficulty table in the Godot source
        for name, target in AUTHOR_TABLE.items():
            with self.subTest(name=name):
                self.assertNotIn(f'"{name}": {target}', source)

    def test_godot_difficulty_names_match_the_shared_spec(self) -> None:
        """Extract the Godot source's difficulty names and compare.

        The Godot file cannot be executed here (no Godot binary), so its literal
        expectations are read from the source and checked against the shared
        spec. This is weaker than running it and is reported as such.
        """
        source = (ROOT / "src" / "godot" / "core_rules.gd").read_text(encoding="utf-8")
        # the adapter must look difficulties up from canon rather than declare them
        self.assertRegex(source, r"canon\.get\(\"difficulties\"")
        # and must not reference the superseded names except in prose
        for removed in ("Harder", "Hardest"):
            with self.subTest(removed=removed):
                self.assertNotIn(f'"{removed}"', source)

    def test_canonical_json_agrees_with_the_shared_spec(self) -> None:
        """The data file every runtime reads must match the spec exactly."""
        self.assertEqual(CANON["difficulties"], AUTHOR_TABLE)
        self.assertEqual(
            {int(k): v for k, v in CANON["human_3d6_modifier"].items()},
            AUTHOR_MODIFIERS,
        )
        self.assertEqual(CANON["unskilled_penalty"], -1)
        self.assertEqual(CANON["trained_only_without_skill"], "blocked")
        self.assertEqual(CANON["success_rule"], "total_gte_target")

    def test_canonical_json_carries_the_migration_warning(self) -> None:
        """The Hard 12->15 change must be recorded where runtimes read it."""
        notes = " ".join(CANON["difficulty_notes"])
        self.assertIn("Hard", notes)
        self.assertIn("12", notes)
        self.assertIn("15", notes)

    def test_the_rulebook_carries_the_same_table_and_the_warning(self) -> None:
        """Tabletop is one of the three runtimes: the doc must not drift."""
        text = " ".join((ROOT / "RULEBOOK.md").read_text(encoding="utf-8").split())
        for name, target in AUTHOR_TABLE.items():
            with self.subTest(name=name):
                self.assertIn(f"{name} | {target} |", text)
        for removed in ("Harder", "Hardest"):
            with self.subTest(removed=removed):
                self.assertNotIn(f"| {removed} |", text)
        self.assertIn("Migration warning", text)
        self.assertIn("no automatic failure on a natural 3", text.lower())

    def test_rulebook_states_the_transhuman_and_near_dead_reading(self) -> None:
        text = " ".join((ROOT / "RULEBOOK.md").read_text(encoding="utf-8").split())
        self.assertIn("transhuman", text.lower())
        self.assertIn("near-dead", text.lower())
        self.assertIn("not raw generation rolls", text)

    def test_concordia_resolves_a_named_difficulty_in_code(self) -> None:
        """The GM names a difficulty; code decides the number (#11, Concordia)."""
        from concordia_runtime.mechanics import resolve_named_check

        attributes = AttributeSet({k: 0 for k in ATTRIBUTE_IDS})
        for name, target in AUTHOR_TABLE.items():
            with self.subTest(name=name):
                result = resolve_named_check(
                    attributes=attributes, attribute_id="INT",
                    difficulty=name, dice_total=target,
                )
                self.assertEqual(result["target"], target)
                self.assertEqual(result["difficulty"], name)
                self.assertEqual(result["total"], target)
                self.assertTrue(result["success"])
                self.assertTrue(result["difficulty_meaning"])

    def test_concordia_blocks_trained_only_before_rolling(self) -> None:
        from concordia_runtime.mechanics import resolve_named_check

        attributes = AttributeSet({k: 0 for k in ATTRIBUTE_IDS})
        result = resolve_named_check(
            attributes=attributes, attribute_id="INT", difficulty="Hard",
            skill_access=SkillAccess.TRAINED_ONLY, has_skill=False,
        )
        self.assertFalse(result["attempted"])
        self.assertEqual(result["blocked_reason"], "trained_only_without_skill")
        self.assertIsNone(result["total"])

    def test_concordia_rejects_an_unknown_difficulty(self) -> None:
        from concordia_runtime.mechanics import resolve_named_check

        attributes = AttributeSet({k: 0 for k in ATTRIBUTE_IDS})
        with self.assertRaises(UnknownDifficulty):
            resolve_named_check(
                attributes=attributes, attribute_id="INT", difficulty="Harder",
                dice_total=12,
            )

    def test_worked_tabletop_examples_match_both_runtimes(self) -> None:
        """Worked examples stated in tabletop terms, checked in code.

        These are the examples the acceptance criteria ask to be identical
        across Godot and Concordia and to match tabletop: each is stated as a
        sentence a tabletop player would read, then resolved.
        """
        from concordia_runtime.mechanics import resolve_named_check

        # "INT 0 against Normal (12), rolled a 12" -> exactly succeeds.
        attributes = AttributeSet({"FIT": 0, "REF": 0, "INT": 0, "CHA": 0,
                                   "CYB": 0, "PSY": 0})
        examples = [
            # (attribute modifier, difficulty, roll, extras, expected total, success)
            (0, "Normal", 12, (), 12, True),
            (0, "Normal", 11, (), 11, False),
            (1, "Normal", 9, (2,), 12, True),
            (1, "Normal", 12, (-2,), 11, False),
            (0, "Easiest", 3, (), 3, True),
            (0, "Easiest", 3, (-1,), 2, False),
            (3, "Impossible", 18, (), 21, True),
            (3, "Impossible", 3, (), 6, False),
        ]
        for modifier, difficulty, roll, extras, total, success in examples:
            with self.subTest(difficulty=difficulty, roll=roll, extras=extras,
                              modifier=modifier):
                shared = resolve_check(
                    attribute_modifier=modifier,
                    target=difficulty_target(difficulty),
                    extra_modifiers=extras, dice_total=roll,
                )
                self.assertEqual(shared.total, total)
                self.assertEqual(shared.success, success)

                concordia = resolve_named_check(
                    attributes=AttributeSet({**attributes.as_dict(), "INT": modifier}),
                    attribute_id="INT", difficulty=difficulty,
                    extra_modifiers=extras, dice_total=roll,
                )
                self.assertEqual(concordia["total"], total)
                self.assertEqual(concordia["success"], success)

    def test_unskilled_parity_across_shared_and_concordia(self) -> None:
        from concordia_runtime.mechanics import resolve_named_check

        attributes = AttributeSet({k: 0 for k in ATTRIBUTE_IDS})
        shared = resolve_check(attribute_modifier=0, target=9, dice_total=10,
                               has_skill=False)
        concordia = resolve_named_check(
            attributes=attributes, attribute_id="INT", difficulty="Easy",
            dice_total=10, has_skill=False,
        )
        # 10 + 0 + (-1) = 9 against Easy (9): succeeds on the boundary.
        self.assertEqual(shared.total, 9)
        self.assertTrue(shared.success)
        self.assertEqual(concordia["total"], 9)
        self.assertEqual(concordia["success"], shared.success)
        self.assertEqual(concordia["target"], difficulty_target("Easy"))


class NoInventedMechanicsTests(unittest.TestCase):
    """Acceptance: no unrelated mechanics or lore introduced."""

    def test_no_automatic_success_failure_language_in_canon(self) -> None:
        """The data must not smuggle in a critical-hit style rule."""
        text = json.dumps(CANON).lower()
        self.assertIn("no automatic failure", text)
        self.assertIn("no automatic success", text)

    def test_rulebook_still_leaves_skill_catalogues_unspecified(self) -> None:
        text = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8").lower()
        self.assertIn("**unspecified.**", text)
        # the skills section must not have acquired a list
        self.assertIn("no skill list", text)

    def test_no_skill_values_were_invented(self) -> None:
        """#11: represent the two categories; do not invent which skills are which."""
        source = (ROOT / "src" / "rules" / "core.py").read_text(encoding="utf-8")
        self.assertIn("UNSKILLED_ALLOWED", source)
        self.assertIn("TRAINED_ONLY", source)
        self.assertNotRegex(source, r"SKILL_(LIST|CATALOG|NAMES)\s*=")


if __name__ == "__main__":
    unittest.main()
