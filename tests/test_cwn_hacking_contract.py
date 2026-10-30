"""Contract test: `data/rules/cwn_hacking.json` and `src/rules/cwn_hacking.py` agree.

The JSON is the engine-neutral contract that the Godot kernel reads; the Python module is the
rules layer of record. If a number changes on one side and not the other, the two runtimes start
playing different games and nothing else in either suite notices. This file exists only to make
that impossible.

Executable contract, not a prose guard: every assertion compares a value the code actually uses.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.rules import cwn_hacking as rules

CONTRACT = Path(__file__).resolve().parents[1] / "data" / "rules" / "cwn_hacking.json"


class HackingContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_security_ladder_is_the_same_on_both_sides(self) -> None:
        contract_ladder = {int(k): v for k, v in self.contract["security_levels"].items()}
        self.assertEqual(contract_ladder, rules.SECURITY_LEVELS)

    def test_connection_penalties_match(self) -> None:
        self.assertEqual(self.contract["connection"]["wireless_penalty"], rules.WIRELESS_PENALTY)
        self.assertEqual(self.contract["connection"]["vr_crown_penalty"], rules.VR_CROWN_PENALTY)

    def test_alert_clock_constants_match(self) -> None:
        self.assertEqual(
            self.contract["alert"]["failures_per_alert_action"], rules.FAILURES_PER_ALERT
        )
        self.assertEqual(
            self.contract["alert"]["alert_actions_to_alert"], rules.ALERT_ACTIONS_TO_ALERT
        )

    def test_cyberware_difficulty_matches_its_formula(self) -> None:
        base = self.contract["cyberware"]["base_difficulty"]
        divisor = self.contract["cyberware"]["hit_dice_divisor"]
        self.assertEqual(base, 7)
        self.assertEqual(divisor, 3)
        for level_or_hit_dice in range(1, 13):
            expected = base + -(-level_or_hit_dice // divisor)  # ceil division
            self.assertEqual(
                rules.cyberware_difficulty(level_or_hit_dice=level_or_hit_dice), expected
            )
        self.assertEqual(
            rules.cyberware_difficulty(level_or_hit_dice=1, has_operator=False),
            self.contract["cyberware"]["unoperated_drone_difficulty"],
        )

    def test_access_pool_is_the_sum_the_contract_documents(self) -> None:
        self.assertEqual(rules.access_pool(intelligence_modifier=2, program_skill=1, deck_bonus=1), 4)
        # The contract's minimum is 0; the module clamps rather than going negative.
        self.assertEqual(rules.access_pool(intelligence_modifier=-2, program_skill=0), 0)

    def test_alert_clock_reaches_alert_on_the_contract_number_of_failures(self) -> None:
        clock = rules.AlertClock()
        failures = self.contract["alert"]["failures_per_alert_action"]
        actions = self.contract["alert"]["alert_actions_to_alert"]
        for _ in range(failures * actions - 1):
            self.assertFalse(clock.record_failure())
            self.assertFalse(clock.alerted)
        self.assertTrue(clock.record_failure())

    def test_declared_situation_ranges_are_enforced_by_both_sides(self) -> None:
        modifiers = self.contract["security_modifiers"]
        self.assertEqual(tuple(modifiers["tech_quality_range"]), rules.TECH_QUALITY_RANGE)
        self.assertEqual(
            tuple(modifiers["inside_information_range"]), rules.INSIDE_INFORMATION_RANGE
        )
        # Out of range on either side is clamped, not trusted, so the two runtimes cannot diverge.
        self.assertEqual(rules.security_difficulty(9, tech_quality=9), 9 + rules.TECH_QUALITY_RANGE[1])
        self.assertEqual(
            rules.security_difficulty(9, inside_info=9), 9 - rules.INSIDE_INFORMATION_RANGE[1]
        )
        self.assertEqual(rules.security_difficulty(9, inside_info=0), 9)

    def test_security_difficulty_accepts_only_the_recorded_ladder(self) -> None:
        recorded = sorted(int(k) for k in self.contract["security_levels"])
        self.assertEqual(rules.security_difficulty(recorded[0]), recorded[0])
        with self.assertRaises(rules.HackError):
            rules.security_difficulty(6)
        self.assertEqual(
            rules.security_difficulty(recorded[0], alerted=True),
            recorded[0] + self.contract["security_modifiers"]["alerted"],
        )


if __name__ == "__main__":
    unittest.main()
