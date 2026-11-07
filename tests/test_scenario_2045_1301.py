"""#1301: the scenario's invariants are data, so a later edit cannot quietly reverse them.

The design specification is prose, but six of its statements are load-bearing: if a later document flips one of them
the scenario becomes a different game. Those six live in `data/campaign/scenario_2045_1301.json` and are asserted here.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from campaign.scenario_1301 import (  # noqa: E402
    KNOWLEDGE_LADDER,
    OBJECTIVE_IDS,
    SHIFT_IDS,
    ScenarioError,
    load_scenario,
)


class TimelineTests(unittest.TestCase):
    def test_the_full_nhi_crisis_has_not_happened(self):
        scenario = load_scenario()
        self.assertTrue(scenario.crisis_has_not_happened())

    def test_a_scenario_that_moves_the_crisis_into_the_present_is_refused(self):
        payload = json.loads((ROOT / "data/campaign/scenario_2045_1301.json").read_text(encoding="utf-8"))
        payload["setting"]["nhi_crisis_occurred"] = True
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scenario.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ScenarioError):
                load_scenario(path)


class ShiftTests(unittest.TestCase):
    def test_the_three_shifts_are_mainstream_science(self):
        scenario = load_scenario()
        self.assertEqual(tuple(entry["id"] for entry in scenario.shifts), SHIFT_IDS)
        for entry in scenario.shifts:
            self.assertEqual(entry["status"], "mainstream", entry["id"])

    def test_each_shift_carries_its_own_fifty_twenty_five_twenty_five(self):
        scenario = load_scenario()
        for shift_id in SHIFT_IDS:
            segments = scenario.shift(shift_id)["segments"]
            self.assertEqual(segments, {"normies": 50, "accelerationists": 25, "doomers": 25}, shift_id)
            self.assertTrue(scenario.segments_sum_to_a_hundred(shift_id))

    def test_the_split_is_per_shift_not_one_alignment_for_a_person(self):
        """A person may be an AGI accelerationist, a PSI normie and an NHI doomer at once (#1301 §7)."""
        scenario = load_scenario()
        self.assertEqual(len(scenario.shifts), 3)
        for entry in scenario.shifts:
            self.assertIn("segments", entry, "the baseline is stored per shift, not on a character")


class ObjectiveTests(unittest.TestCase):
    def test_the_four_objectives_and_their_tensions(self):
        scenario = load_scenario()
        self.assertEqual(tuple(entry["id"] for entry in scenario.objectives), OBJECTIVE_IDS)
        for entry in scenario.objectives:
            self.assertTrue(entry["mandate"].strip() and entry["tension"].strip(), entry["id"])

    def test_profit_is_a_criticism_of_sustainability_not_a_fifth_objective(self):
        scenario = load_scenario()
        self.assertNotIn("profit", [entry["id"] for entry in scenario.objectives])
        sustainability = next(entry for entry in scenario.objectives if entry["id"] == "sustainability")
        self.assertEqual(sustainability["critics_call_it"], "Profit")


class CaseTests(unittest.TestCase):
    def test_one_case_per_shift_with_several_outcomes(self):
        scenario = load_scenario()
        for shift_id in SHIFT_IDS:
            cases = scenario.cases_for(shift_id)
            self.assertEqual(len(cases), 1, shift_id)
            self.assertGreaterEqual(len(cases[0]["outcomes"]), 3)

    def test_every_case_has_a_non_psi_path(self):
        scenario = load_scenario()
        self.assertTrue(scenario.psi_is_optional_everywhere())

    def test_a_case_that_requires_psi_is_refused(self):
        payload = json.loads((ROOT / "data/campaign/scenario_2045_1301.json").read_text(encoding="utf-8"))
        payload["cases"][1]["non_psi_path"] = False
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scenario.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ScenarioError):
                load_scenario(path)

    def test_outcomes_include_a_lawful_or_non_criminal_one(self):
        """The issue insists a registration violation is not the same as harm (#1301 §4A)."""
        for case in load_scenario().cases:
            joined = " ".join(case["outcomes"]).lower()
            self.assertTrue(
                any(word in joined for word in ("no crime", "dropped", "protected", "administrative")),
                case["id"],
            )


class CharacterTests(unittest.TestCase):
    def test_the_rookie_is_tabula_rasa_with_cyber_and_optional_psi(self):
        character = json.loads((ROOT / "data/campaign/scenario_2045_1301.json")
                               .read_text(encoding="utf-8"))["player_character"]
        self.assertEqual(character["state"], "tabula rasa")
        self.assertFalse(character["psi_required"])
        self.assertFalse(character["forced_alignment"])
        self.assertIn("regularly used", character["cyber_competence"])

    def test_the_knowledge_ladder_keeps_public_from_gm_truth(self):
        self.assertEqual(load_scenario().knowledge_ladder, KNOWLEDGE_LADDER)
        self.assertIn("classified", KNOWLEDGE_LADDER)
        self.assertIn("gm_truth", KNOWLEDGE_LADDER)


if __name__ == "__main__":
    unittest.main()
