"""Tests for canonical independent NoöPunk core rules (#111)."""
from pathlib import Path
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))

from rules import (
    AttributeSet, CHECK_DICE, DIFFICULTIES, DIFFICULTY_LADDER,
    SKILL_LEVEL_MIN, SKILL_LEVEL_MAX, STAT_MIN, STAT_MAX,
    compare_opposed, difficulty_for, resolve_check, roll_d10,
)

class FixedDice:
    def __init__(self, value:int): self.value=value
    def randint(self,a:int,b:int)->int:
        if not a <= self.value <= b: raise AssertionError("fixed die out of bounds")
        return self.value

class CoreRulesTests(unittest.TestCase):
    def test_system_is_1d10(self):
        self.assertEqual(CHECK_DICE,"1d10")
        self.assertEqual(roll_d10(FixedDice(1)),1)
        self.assertEqual(roll_d10(FixedDice(10)),10)

    def test_stat_and_skill_ranges(self):
        self.assertEqual((STAT_MIN,STAT_MAX),(1,10))
        self.assertEqual((SKILL_LEVEL_MIN,SKILL_LEVEL_MAX),(1,10))
        self.assertEqual(AttributeSet({"Physical":5})["Physical"],5)
        for bad in (0,11):
            with self.assertRaises(ValueError): AttributeSet({"X":bad})

    def test_difficulty_ladder(self):
        self.assertEqual(DIFFICULTY_LADDER,(9,13,15,17,21,24,29))
        self.assertEqual(DIFFICULTIES[17],"Professional")
        self.assertEqual(difficulty_for(29),"Legendary")

    def test_check_formula_and_meeting_dv(self):
        r=resolve_check(stat=6,skill=5,target=17,die=6)
        self.assertEqual(r.total,17)
        self.assertTrue(r.success)
        self.assertFalse(resolve_check(stat=6,skill=5,target=18,die=6).success)

    def test_rating_and_die_validation(self):
        for kwargs in (
            dict(stat=0,skill=5,target=9,die=5),
            dict(stat=5,skill=0,target=9,die=5),
            dict(stat=5,skill=5,target=9,die=0),
            dict(stat=5,skill=5,target=9,die=11),
        ):
            with self.assertRaises(ValueError): resolve_check(**kwargs)

    def test_opposed_ties_are_deliberately_unresolved(self):
        self.assertEqual(compare_opposed(20,18).winner,"left")
        self.assertEqual(compare_opposed(18,20).winner,"right")
        tie=compare_opposed(20,20)
        self.assertTrue(tie.unresolved_tie)
        self.assertIsNone(tie.winner)

    def test_machine_readable_identity(self):
        data=json.loads((ROOT/"data/rules/core.json").read_text(encoding="utf-8"))
        self.assertTrue(data["system_identity"]["independent"])
        self.assertEqual(data["skill_check"]["formula"],"STAT + Skill + 1d10")
        self.assertEqual(data["opposed"]["tie"],"deferred")
        self.assertEqual(data["criticals"],"deferred")
        self.assertEqual(data["situational_modifiers"],"deferred")

    def test_probability_pass_is_recorded(self):
        data=json.loads((ROOT/"data/rules/core.json").read_text(encoding="utf-8"))
        p=data["probability_examples"]
        self.assertEqual(p["Novice STAT 4 + Skill 1"]["9"],0.7)
        self.assertEqual(p["Professional STAT 6 + Skill 5"]["17"],0.5)
        self.assertEqual(p["Elite STAT 8 + Skill 9"]["24"],0.4)

if __name__=="__main__": unittest.main()
