"""Focused tests for the canonical NoöPunk attribute and skill-check rules.

These pin the **ported** canon: RULEBOOK.md §4's 2d6 engine, not the withdrawn 3d6
engine. They replace an earlier version of this file that asserted the superseded
3d6 ladder (Easiest/Easier/Easy/Normal/Hard/Impossible at 3/6/9/12/15/18), which
RULEBOOK §4 and §17.1 retired as canon.

Attribute *generation* still uses 3d6 per attribute (§5.2) and is tested as such.
"""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from concordia_runtime import resolve_structured_check

from rules import (
    ATTRIBUTE_DEFINITIONS,
    ATTRIBUTE_IDS,
    CHECK_DICE,
    DIFFICULTIES,
    DIFFICULTY_LADDER,
    SKILL_LEVEL_MAX,
    SKILL_LEVEL_MIN,
    TOP_DIFFICULTY,
    UNSKILLED_PENALTY,
    AttributeSet,
    SkillAccess,
    compare_opposed,
    difficulty_for,
    generate_human_attributes,
    human_modifier,
    resolve_check,
    roll_2d6,
    roll_3d6,
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

    def test_attribute_meanings_match_author_specification(self) -> None:
        self.assertEqual(
            {item["id"]: item["description"] for item in ATTRIBUTE_DEFINITIONS},
            {
                "FIT": "Your health, fitness and constitution.",
                "REF": "Your dexterity, agility and coordination.",
                "INT": "How smart, educated and knowledgeable you are.",
                "CHA": "Your social skills, attractiveness and leadership skills.",
                "CYB": "Your cyborg side; how technical you are; your proficiency in cyberspace, programming and cybernetics.",
                "PSY": "Your consciousness, intuition, empathy and psionics. Used in astral projection and for psionics.",
            },
        )

    # -- retained from the pre-port canon, unchanged by §17.1 --------------- #

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

    # -- the ported 2d6 engine --------------------------------------------- #

    def test_skill_check_engine_is_2d6(self) -> None:
        self.assertEqual(CHECK_DICE, "2d6")
        dice = FixedDice([6, 6])
        self.assertEqual(roll_2d6(dice), 12)
        dice = FixedDice([1, 1])
        self.assertEqual(roll_2d6(dice), 2)
        # The generation roll is a different thing and stays 3d6.
        dice = FixedDice([1, 1, 1])
        self.assertEqual(roll_3d6(dice), 3)

    def test_canonical_difficulty_ladder(self) -> None:
        self.assertEqual(DIFFICULTY_LADDER, (6, 8, 10, 12, 14))
        self.assertEqual(sorted(int(k) for k in DIFFICULTIES), list(DIFFICULTY_LADDER))
        self.assertEqual(TOP_DIFFICULTY, 14)

    def test_withdrawn_ladder_names_are_not_retained_as_aliases(self) -> None:
        """§4: the old names must not silently keep meaning their old numbers."""
        for retired in ("Easiest", "Easier", "Easy", "Normal", "Hard", "Impossible"):
            with self.subTest(name=retired):
                self.assertNotIn(retired, DIFFICULTIES)
        # In particular the old numbers themselves are gone as rungs.
        for old_number in (3, 9, 15, 18):
            with self.subTest(number=old_number):
                self.assertNotIn(str(old_number), DIFFICULTIES)

    def test_difficulty_six_keeps_its_number_but_changed_meaning(self) -> None:
        """§4 is explicit: 6 was the second-easiest rung and is now the top of 'not worth rolling'."""
        self.assertIn("6", DIFFICULTIES)
        self.assertIn("still beyond ordinary routine", DIFFICULTIES["6"])
        self.assertNotIn("Easiest", DIFFICULTIES["6"])

    def test_skill_level_adds_to_the_total(self) -> None:
        base = resolve_check(attribute_modifier=1, target=10, dice_total=7, skill_level=0)
        level_two = resolve_check(attribute_modifier=1, target=10, dice_total=7, skill_level=2)
        self.assertEqual(base.total, 8)
        self.assertEqual(level_two.total, 10)
        self.assertFalse(base.success)
        self.assertTrue(level_two.success)

    def test_skill_level_range_is_zero_to_four(self) -> None:
        self.assertEqual((SKILL_LEVEL_MIN, SKILL_LEVEL_MAX), (0, 4))
        self.assertEqual(resolve_check(attribute_modifier=0, target=6, dice_total=6, skill_level=4).total, 10)
        for bad in (-1, 5):
            with self.subTest(level=bad):
                with self.assertRaises(ValueError):
                    resolve_check(attribute_modifier=0, target=6, dice_total=6, skill_level=bad)

    def test_unskilled_is_not_level_zero(self) -> None:
        """§5.3: unskilled sits outside the numbered levels and takes -1 (§4.2)."""
        self.assertEqual(UNSKILLED_PENALTY, -1)
        unskilled = resolve_check(attribute_modifier=0, target=8, dice_total=6, has_skill=False)
        level_zero = resolve_check(attribute_modifier=0, target=8, dice_total=6, skill_level=0)
        self.assertEqual(unskilled.unskilled_modifier, -1)
        self.assertEqual(unskilled.total, 5)
        self.assertEqual(unskilled.skill_level, 0)
        self.assertEqual(level_zero.unskilled_modifier, 0)
        self.assertEqual(level_zero.total, 6)
        # The two must not be conflated.
        self.assertNotEqual(unskilled.total, level_zero.total)

    def test_meeting_difficulty_succeeds_and_below_fails(self) -> None:
        self.assertTrue(resolve_check(attribute_modifier=0, target=10, dice_total=10).success)
        self.assertFalse(resolve_check(attribute_modifier=0, target=11, dice_total=10).success)

    def test_no_automatic_failure_on_two_or_success_on_twelve(self) -> None:
        """§4: a 2 or a 12 is only ever a die result; no critical rule exists."""
        # A natural 2 can still succeed with enough skill and attribute.
        low = resolve_check(attribute_modifier=3, target=6, dice_total=2, skill_level=4)
        self.assertTrue(low.success)
        # A natural 12 can still fail against a high target.
        high = resolve_check(attribute_modifier=-3, target=14, dice_total=12, skill_level=0)
        self.assertFalse(high.success)

    def test_positive_and_negative_extra_modifiers(self) -> None:
        positive = resolve_check(attribute_modifier=1, target=12, dice_total=7, extra_modifiers=(2,))
        negative = resolve_check(attribute_modifier=1, target=12, dice_total=12, extra_modifiers=(-2,))
        self.assertEqual(positive.total, 10)
        self.assertFalse(positive.success)
        self.assertEqual(negative.total, 11)
        self.assertFalse(negative.success)

    def test_check_roll_outside_2d6_bounds_is_rejected(self) -> None:
        for bad in (1, 13):
            with self.subTest(roll=bad):
                with self.assertRaises(ValueError):
                    resolve_check(attribute_modifier=0, target=6, dice_total=bad)

    def test_trained_only_attempt_is_blocked_without_skill(self) -> None:
        result = resolve_check(
            attribute_modifier=3,
            target=6,
            skill_access=SkillAccess.TRAINED_ONLY,
            has_skill=False,
            dice_total=12,
            extra_modifiers=(100,),
        )
        self.assertFalse(result.attempted)
        self.assertIsNone(result.total)
        self.assertIsNone(result.success)
        self.assertEqual(result.blocked_reason, "trained_only_without_skill")

    def test_aid_bonus_is_capped_at_one(self) -> None:
        """§4.3: multiple helpers may roll but the total aid bonus is capped at +1."""
        one = resolve_check(attribute_modifier=0, target=8, dice_total=6, aid_bonus=1)
        many = resolve_check(attribute_modifier=0, target=8, dice_total=6, aid_bonus=5)
        self.assertEqual(one.total, 7)
        self.assertEqual(many.total, 7)

    def test_difficulty_for_reports_the_ladder_and_the_floor(self) -> None:
        self.assertIn("Relatively simple", difficulty_for(6))
        self.assertIn("Extreme", difficulty_for(14))
        # Above the top rung the rulebook writes "14+"; no sixth rung is invented.
        self.assertIn("above the 14 rung", difficulty_for(16))
        self.assertIn("not worth a roll", difficulty_for(4))

    # -- opposed checks ---------------------------------------------------- #

    def test_opposed_higher_total_wins(self) -> None:
        self.assertEqual(compare_opposed(12, 9).winner, "left")
        self.assertEqual(compare_opposed(9, 12).winner, "right")

    def test_opposed_tie_is_won_by_a_player_character(self) -> None:
        """§4.1."""
        left_pc = compare_opposed(12, 12, left_is_player_character=True)
        right_pc = compare_opposed(12, 12, right_is_player_character=True)
        self.assertEqual(left_pc.winner, "left")
        self.assertFalse(left_pc.unresolved_tie)
        self.assertEqual(left_pc.decided_by, "player_character_tie")
        self.assertEqual(right_pc.winner, "right")

    def test_opposed_tie_without_a_player_character_stays_unresolved(self) -> None:
        """§4.1 declines to define a general tie procedure; inventing one is a defect."""
        tie = compare_opposed(12, 12)
        self.assertIsNone(tie.winner)
        self.assertTrue(tie.unresolved_tie)
        self.assertEqual(tie.decided_by, "unresolved_tie")
        both_pcs = compare_opposed(12, 12, left_is_player_character=True, right_is_player_character=True)
        self.assertIsNone(both_pcs.winner)
        self.assertTrue(both_pcs.unresolved_tie)

    # -- cross-runtime parity ---------------------------------------------- #

    def test_attribute_model_allows_future_values_outside_human_range(self) -> None:
        attributes = AttributeSet({"FIT": 4, "REF": -4, "INT": 0, "CHA": 0, "CYB": 7, "PSY": -9})
        self.assertEqual(attributes["FIT"], 4)
        self.assertEqual(attributes["REF"], -4)
        self.assertEqual(attributes["CYB"], 7)
        self.assertEqual(attributes["PSY"], -9)

    def test_concordia_structured_check_matches_shared_resolution(self) -> None:
        attributes = AttributeSet({"FIT": 1, "REF": 0, "INT": 0, "CHA": 0, "CYB": 0, "PSY": 0})
        shared = resolve_check(
            attribute_modifier=attributes["FIT"],
            target=10,
            dice_total=7,
            skill_level=2,
            extra_modifiers=(-1,),
        )
        concordia = resolve_structured_check(
            attributes=attributes,
            attribute_id="FIT",
            target=10,
            dice_total=7,
            skill_level=2,
            extra_modifiers=(-1,),
        )
        self.assertEqual(concordia["dice_total"], shared.dice_total)
        self.assertEqual(concordia["total"], shared.total)
        self.assertEqual(concordia["success"], shared.success)
        self.assertEqual(concordia["skill_level"], 2)

    def test_godot_adapter_reads_shared_canon_and_uses_2d6(self) -> None:
        source = (ROOT / "src" / "godot" / "core_rules.gd").read_text(encoding="utf-8")
        self.assertIn("res://data/rules/core.json", source)
        self.assertIn("func difficulty_names()", source)
        self.assertIn("dice_total_override", source)
        self.assertIn("total >= target", source)
        self.assertIn("func roll_2d6", source)
        self.assertIn("human_3d6_generation", source)
        self.assertIn("player_character_tie", source)
        # The withdrawn 3d6 check engine must not survive in the adapter.
        self.assertNotIn("A 3d6 check roll", source)
        self.assertNotIn('canon["human_3d6_modifier"]', source)
        for attribute_id in ATTRIBUTE_IDS:
            self.assertNotIn('"' + attribute_id + '":', source)

    def test_no_runtime_still_reads_the_superseded_tables(self) -> None:
        """The port's whole point: the withdrawn keys must be gone from every runtime."""
        for relative in ("src/rules/core.py", "src/godot/core_rules.gd"):
            with self.subTest(file=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertNotIn("human_3d6_modifier", text)
                self.assertNotIn("A 3d6 check roll", text)
        # The superseded key must be gone as a *key*, not merely mentioned in prose:
        # check the parsed data rather than the file text.
        import json
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        self.assertNotIn("_superseded_note", canon)
        self.assertNotIn("human_3d6_modifier", canon)
        self.assertEqual(canon["skill_check"]["dice"], "2d6")
        self.assertEqual(canon["_canon_revision"], "2d6-port")


if __name__ == "__main__":
    unittest.main()
