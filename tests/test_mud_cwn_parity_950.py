"""The MUD's CWN core agrees with the repository's Python rules, case by case (#950).

A port is only a port if it produces the same answers. This compares `mud/nopunk_mud/cwn` against `src/rules/`
on the procedures both implement — attributes, saves, skill arithmetic, hit points and strain — using fixed
inputs, so a divergence is a failing test rather than a later surprise at a table.

Written with `unittest` only: CI discovers with `unittest` and does not install pytest. It lives at the
repository root on purpose — `mud/` must stay importable without the rest of the repository, and this is the
place where the two are allowed to meet.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))
sys.path.insert(0, str(ROOT))

from nopunk_mud import cwn  # noqa: E402
from src.rules import cwn_advancement, cwn_core, wn_core  # noqa: E402

SHEETS = [
    {"Strength": 12, "Dexterity": 15, "Constitution": 9, "Intelligence": 11, "Wisdom": 13,
     "Charisma": 8},
    {"Strength": 3, "Dexterity": 18, "Constitution": 14, "Intelligence": 7, "Wisdom": 10,
     "Charisma": 17},
]
SAVE_KINDS = ["Physical", "Evasion", "Mental", "Luck"]


class AttributeParity(unittest.TestCase):
    def test_modifiers_match_for_every_legal_score(self):
        for score in range(3, 19):
            with self.subTest(score=score):
                self.assertEqual(cwn.attribute_modifier(score), wn_core.attribute_modifier(score))

    def test_illegal_scores_are_refused(self):
        for score in (2, 19):
            with self.subTest(score=score):
                with self.assertRaises(cwn.CwnError):
                    cwn.attribute_modifier(score)


class SaveParity(unittest.TestCase):
    def test_targets_match(self):
        for sheet in SHEETS:
            for kind in SAVE_KINDS:
                for level in (1, 3, 7, 10):
                    with self.subTest(kind=kind, level=level):
                        self.assertEqual(
                            cwn.save_target(kind, level=level, attributes=sheet),
                            cwn_core.save_target(kind, level=level, attributes=sheet))

    def test_throws_match_including_naturals(self):
        sheet = SHEETS[0]
        for die in (1, 2, 10, 19, 20):
            with self.subTest(die=die):
                theirs = cwn_core.saving_throw("Physical", level=2, attributes=sheet, die=die, bonus=1)
                ours = cwn.saving_throw("Physical", level=2, attributes=sheet, die=die, bonus=1)
                self.assertEqual(ours["target"], theirs.target)
                self.assertEqual(ours["success"], theirs.success)
                self.assertEqual(ours["natural"], theirs.natural)


class HitPointParity(unittest.TestCase):
    def test_dice_totals_match(self):
        cases = [(1, (1,)), (1, (3,)), (2, (6, 6)), (5, (1, 4, 2, 6, 5))]
        for level, dice in cases:
            with self.subTest(level=level, dice=dice):
                self.assertEqual(cwn.hit_points(level, 1, dice=dice),
                                 cwn_advancement.hit_points_rolled(level, 1, dice=dice))

    def test_a_wrong_number_of_dice_is_refused(self):
        with self.assertRaises(cwn.CwnError):
            cwn.hit_points(3, 0, dice=(4, 5))


class StrainParity(unittest.TestCase):
    def test_every_lifestyle_matches(self):
        for constitution in (3, 9, 14, 18):
            for lifestyle in ("squatter", "slum", "ordinary", "fine", "luxury"):
                with self.subTest(constitution=constitution, lifestyle=lifestyle):
                    self.assertEqual(cwn.strain_maximum(constitution, lifestyle=lifestyle),
                                     cwn_core.strain_maximum(constitution, lifestyle=lifestyle))


class SkillArithmetic(unittest.TestCase):
    def test_rank_zero_is_trained(self):
        self.assertEqual(cwn.skill_modifier(0), 0)
        self.assertEqual(cwn.skill_modifier(-1), -1)

    def test_check_arithmetic(self):
        sheet = SHEETS[0]
        for rank in (-1, 0, 1, 4):
            for dice in ((1, 1), (3, 4), (6, 6)):
                with self.subTest(rank=rank, dice=dice):
                    result = cwn.skill_check(rank=rank, attribute=sheet["Intelligence"],
                                             difficulty=10, dice=dice)
                    expected = (dice[0] + dice[1]
                                + (cwn.UNTRAINED_MODIFIER if rank < 0 else rank)
                                + wn_core.attribute_modifier(sheet["Intelligence"]))
                    self.assertEqual(result.total, expected)
                    self.assertEqual(result.success, expected >= 10)

    def test_circumstances_and_aid_are_capped(self):
        with self.assertRaises(cwn.CwnError):
            cwn.skill_check(rank=0, attribute=10, difficulty=10, dice=(3, 3), circumstances=3)
        with self.assertRaises(cwn.CwnError):
            cwn.skill_check(rank=0, attribute=10, difficulty=10, dice=(3, 3), aid=2)

    def test_an_unpublished_difficulty_is_refused(self):
        with self.assertRaises(cwn.CwnError):
            cwn.skill_check(rank=0, attribute=10, difficulty=11, dice=(3, 3))


class CharacterCreation(unittest.TestCase):
    def test_a_legal_sheet_builds(self):
        character = cwn.create_character("rookie", attributes=SHEETS[0],
                                          skills={"Notice": 1, "Talk": 0})
        self.assertEqual(character.name, "rookie")
        self.assertEqual(character.max_hit_points(dice=(4,)), 4)
        self.assertEqual(character.strain_capacity(), 9)

    def test_an_illegal_sheet_is_refused_not_repaired(self):
        with self.assertRaises(cwn.CwnError):
            cwn.create_character("rookie", attributes={**SHEETS[0], "Strength": 22})
        with self.assertRaises(cwn.CwnError):
            cwn.create_character("rookie", attributes={"Strength": 10})
        with self.assertRaises(cwn.CwnError):
            cwn.create_character("", attributes=SHEETS[0])
        with self.assertRaises(cwn.CwnError):
            cwn.create_character("rookie", attributes=SHEETS[0], skills={"Notice": 9})


if __name__ == "__main__":
    unittest.main()
