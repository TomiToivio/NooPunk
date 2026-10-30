"""Contract test: data/rules/swn_psionics.json and src/rules/swn_psionics.py agree.

The JSON is what the Godot kernel reads; the Python module is the rules layer of record. Drift
between them is invisible to both suites unless something compares them, which is this file.
"""
import json
import unittest
from pathlib import Path

from src.rules import swn_psionics as rules

CONTRACT = Path(__file__).resolve().parents[1] / "data" / "rules" / "swn_psionics.json"


class PsionicsContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_the_effort_formula_is_the_same_on_both_sides(self) -> None:
        effort = self.contract["effort"]
        self.assertEqual(effort["base"], 1)
        self.assertEqual(effort["minimum"], 1)
        self.assertEqual(effort["use_best_of"], ["WIS", "CON"])
        psychic = rules.Psychic(wisdom=9, constitution=18, disciplines={"Telepathy": 1})
        self.assertEqual(psychic.capacity, 4)  # 1 + CON +2 + rank 1

    def test_the_durations_are_the_three_the_rules_use(self) -> None:
        self.assertEqual(sorted(self.contract["durations"]),
                         sorted(d.value for d in rules.Duration))

    def test_the_torching_table_matches(self) -> None:
        table = {int(k): v for k, v in self.contract["torching"]["table"].items()}
        self.assertEqual(table, rules.TORCHING_TABLE)
        self.assertEqual(self.contract["torching"]["attribute_floor"], rules.ATTRIBUTE_FLOOR)
        self.assertEqual(self.contract["torching"]["grants_effort"], rules.TORCH_GRANTED_EFFORT)
        self.assertEqual(set(self.contract["packages"]),
                         {"swn_psychic", "swn_partial_psychic"})
        self.assertIn("swn_partial_psychic", rules.RESTRICTED_PACKAGES)


if __name__ == "__main__":
    unittest.main()
