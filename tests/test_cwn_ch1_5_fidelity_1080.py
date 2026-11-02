"""Book-fidelity checks for CWN chapters 1-5 (#1080).

The coverage matrix could say "there is a module with this name and a test that names it" — presence,
not fidelity. This test is the other half: each row of `data/rules/cwn_ch1_5_fidelity_1068.json` was
read off a printed page of the Deluxe rulebook, and here the library has to reproduce it. If a
refactor moves a number, this fails at CI instead of at a table mid-session.

Scope is deliberately the eight claims a reader can check by hand in a minute. Everything else in
chapters 1-5 stays `unverified` in the coverage report, which is the honest state: an unverified row
is not a covered row.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.rules import cwn_advancement, cwn_core, cwn_strain, wn_core

ROOT = Path(__file__).resolve().parents[1]
FIDELITY = ROOT / "data/rules/cwn_ch1_5_fidelity_1068.json"


def rows() -> dict[str, dict]:
    data = json.loads(FIDELITY.read_text(encoding="utf-8"))
    assert data["format"] == "noopunk.rules.cwn_ch1_5_fidelity"
    return {row["id"]: row for row in data["rows"]}


class AttributeBandTests(unittest.TestCase):
    """Printed p. 5. These are the CWN bands, not the WWN/SWN ones."""

    def test_every_band_matches_the_printed_table(self):
        row = rows()["attributes.modifier_bands"]
        for score, expected in row["table"].items():
            self.assertEqual(wn_core.attribute_modifier(int(score)), expected,
                             f"score {score} should modify by {expected}")


class LevelTableTests(unittest.TestCase):
    """Printed p. 24: saves 15+ falling by one per level, attack bonus +0..+5."""

    def test_save_targets_fall_by_one_per_level(self):
        row = rows()["creation.level_table.saves"]
        attributes = {name: 10 for name in
                      ("Strength", "Constitution", "Intelligence", "Dexterity",
                       "Wisdom", "Charisma")}
        for level, expected in enumerate(row["table"], start=1):
            for kind in cwn_core.SAVE_KINDS:
                self.assertEqual(
                    cwn_core.save_target(kind, level=level, attributes=attributes), expected,
                    f"level {level} {kind}")

    def test_attack_bonus_by_level(self):
        row = rows()["creation.level_table.attack_bonus"]
        for level, expected in enumerate(row["table"], start=1):
            self.assertEqual(cwn_advancement.attack_bonus(level), expected)
            self.assertEqual(cwn_advancement.attack_bonus(level, on_target=True), level,
                             "the On Target Edge is +level, not a table")

    def test_hard_to_kill_adds_two_per_die(self):
        row = rows()["creation.hit_points.hard_to_kill"]
        self.assertEqual(cwn_advancement.HARD_TO_KILL_BONUS,
                         row["table"]["hard_to_kill_bonus_per_die"])


class SkillCheckTests(unittest.TestCase):
    """Printed p. 31: 2d6 + attribute + skill, -1 untrained, difficulties 6/8/10/12/14."""

    def test_the_formula_and_the_untrained_penalty(self):
        row = rows()["rules.skill_checks.formula"]
        check = wn_core.skill_check(attribute_score=10, skill_level=0, difficulty=8, dice=(4, 4))
        self.assertEqual(row["table"]["dice"], len(check.dice))
        self.assertEqual(row["table"]["die_faces"], 6)
        self.assertEqual(check.total, 8)
        untrained = wn_core.skill_check(attribute_score=10, skill_level=None, difficulty=8,
                                        dice=(4, 4))
        self.assertTrue(untrained.untrained)
        self.assertEqual(untrained.total, 7, "a character without level-0 takes -1")
        self.assertEqual(wn_core.UNSKILLED_PENALTY, row["table"]["untrained_penalty"])

    def test_the_difficulty_bands(self):
        row = rows()["rules.skill_checks.difficulty_bands"]
        self.assertEqual(row["table"], [
            wn_core.DIFFICULTY_SIMPLE, wn_core.DIFFICULTY_SIGNIFICANT, wn_core.DIFFICULTY_EXPERT,
            wn_core.DIFFICULTY_MASTER, wn_core.DIFFICULTY_EXTREME])


class SaveCategoryTests(unittest.TestCase):
    """Printed p. 30: which attribute pair each save subtracts (Luck subtracts none)."""

    def test_the_attribute_pairs(self):
        row = rows()["rules.saving_throw.categories"]
        self.assertEqual({kind: list(pair) for kind, pair in cwn_core.SAVE_ATTRIBUTES.items()},
                         row["table"])
        # The consequence, not just the mapping: a high Strength improves Physical only.
        attributes = {"Strength": 18, "Constitution": 10, "Intelligence": 10,
                      "Dexterity": 10, "Wisdom": 10, "Charisma": 10}
        physical = cwn_core.save_target("Physical", level=1, attributes=attributes)
        mental = cwn_core.save_target("Mental", level=1, attributes=attributes)
        self.assertEqual((physical, mental), (13, 15))


class SystemStrainTests(unittest.TestCase):
    """Printed p. 40: the Strain maximum is the Constitution score."""

    def test_the_maximum_is_constitution(self):
        row = rows()["injury.system_strain.maximum"]
        constitution = row["table"]["constitution"]
        strain = cwn_strain.SystemStrain(constitution=constitution)
        self.assertEqual(strain.maximum, constitution)
        with self.assertRaises(cwn_strain.StrainError):
            cwn_strain.SystemStrain(constitution=3, permanent=4)


class ProvenanceTests(unittest.TestCase):
    def test_every_row_names_a_page_and_a_symbol_that_exists(self):
        modules = {"src/rules/wn_core.py": wn_core, "src/rules/cwn_core.py": cwn_core,
                   "src/rules/cwn_advancement.py": cwn_advancement,
                   "src/rules/cwn_strain.py": cwn_strain}
        for identifier, row in rows().items():
            self.assertGreaterEqual(row["printed_page"], 1, identifier)
            self.assertTrue(row["claim"], identifier)
            module = modules[row["module"]]
            symbol = row["symbol"]
            if symbol.endswith("*"):
                prefix = symbol.rstrip("*")
                self.assertTrue([name for name in dir(module) if name.startswith(prefix)],
                                f"{identifier}: no {prefix}* in {row['module']}")
            else:
                head = symbol.split(".")[0]
                self.assertTrue(hasattr(module, head), f"{identifier}: no {head}")

    def test_the_rows_do_not_claim_more_than_chapters_one_to_five(self):
        data = json.loads(FIDELITY.read_text(encoding="utf-8"))
        self.assertEqual(len(data["rows"]), 8)
        self.assertEqual(data["source"]["pdf_page_offset"], 4)


if __name__ == "__main__":
    unittest.main()
