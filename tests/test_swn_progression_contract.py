"""Contract test: the `progression` block of data/rules/swn_psionics.json vs swn_progression.py.

The Godot advancement kernel reads the JSON; the Python module is the reference of record. If the
pick rule, the core-technique rank or the discipline ceiling drift apart, the engine and the rules
layer start teaching different psychics — and neither suite would notice without this file.
"""
import json
import unittest
from pathlib import Path

from src.rules import swn_progression as rules

CONTRACT = Path(__file__).resolve().parents[1] / "data" / "rules" / "swn_psionics.json"


class ProgressionContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.block = json.loads(CONTRACT.read_text(encoding="utf-8"))["progression"]

    def test_the_core_technique_is_free_at_the_recorded_rank(self) -> None:
        self.assertEqual(self.block["core_technique_at_rank"], rules.CORE_TECHNIQUE_RANK)
        self.assertTrue(self.block["core_is_free"])

    def test_one_pick_per_improvement_and_no_banking(self) -> None:
        self.assertEqual(self.block["picks_per_skill_improvement"], rules.PICKS_PER_IMPROVEMENT)
        self.assertTrue(self.block["picks_cannot_be_saved"])

    def test_the_ceiling_and_the_partial_limit_are_the_modules(self) -> None:
        self.assertEqual(self.block["max_discipline_rank"], rules.MAX_DISCIPLINE_RANK)
        self.assertEqual(
            self.block["partial_psychic_discipline_limit"], rules.PARTIAL_DISCIPLINE_LIMIT
        )

    def test_the_pick_rule_is_what_the_code_does(self) -> None:
        p = rules.PsychicTraining(rules.FULL, {"Telepathy": 0})
        with self.assertRaises(rules.PsiRulesError):
            p.learn_technique("t0", "Telepathy", 0)  # nothing improved yet, so no pick
        p.advance("Telepathy")
        with self.assertRaises(rules.PsiRulesError):
            p.advance("Telepathy")  # the open pick blocks the next improvement
        p.learn_technique("t1", "Telepathy", 1)
        p.advance("Telepathy")
        p.learn_technique("t2", "Telepathy", 1)
        self.assertTrue(p.technique_access("t2"))


if __name__ == "__main__":
    unittest.main()
