"""CWN lifestyle costs, common wages and bribes (SRD 3.8) — table fidelity and edge cases.

Every number here is pinned against the Free Edition SRD's own table, so a typo in the module fails
a test instead of quietly changing what a month of rent or a bribed clerk costs.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import cwn_core  # noqa: E402
from rules.cwn_lifestyles import (  # noqa: E402
    BRIBE_MULTIPLES,
    COMMON_WAGES,
    LIFESTYLE_COSTS,
    LifestyleError,
    bribe_cost,
    bribe_needs_more_than_cash,
    living_cost,
    strain_modifier,
    wage,
)


class LifestyleCostTests(unittest.TestCase):
    def test_monthly_costs_match_the_srd(self) -> None:
        self.assertEqual(LIFESTYLE_COSTS, {
            "squatter": 0, "slum": 300, "ordinary": 1_000, "fine": 5_000, "luxury": 20_000})

    def test_the_cost_table_and_the_strain_table_share_their_keys(self) -> None:
        """Money and strain are two halves of one rule; a lifestyle in one and not the other is a bug."""
        self.assertEqual(set(LIFESTYLE_COSTS), set(cwn_core.LIFESTYLE_STRAIN))

    def test_strain_modifier_is_the_core_table_not_a_copy(self) -> None:
        for lifestyle, expected in cwn_core.LIFESTYLE_STRAIN.items():
            self.assertEqual(strain_modifier(lifestyle), expected)
        self.assertEqual(strain_modifier("squatter"), -2)
        self.assertEqual(strain_modifier("luxury"), 2)

    def test_an_unknown_lifestyle_is_an_error_with_the_valid_keys(self) -> None:
        with self.assertRaises(LifestyleError) as caught:
            living_cost("palace")
        self.assertIn("luxury", str(caught.exception))
        with self.assertRaises(LifestyleError):
            strain_modifier("palace")


class WageTests(unittest.TestCase):
    def test_daily_wages_match_the_srd(self) -> None:
        expected = {
            "unskilled_labourer": 10, "low_level_ganger": 15, "streetwalker": 20,
            "street_stall_merchant": 25, "entry_level_corp_worker": 30, "low_level_corp_lifer": 40,
            "street_tech_or_cyberdoc": 50, "street_bodyguard": 50,
            "street_cop_or_skilled_corp_worker": 100, "professional_companion": 200,
            "corp_hacker": 200, "corp_middle_manager": 250, "corp_cyberdoc": 250,
            "elite_bodyguard": 500, "gang_boss": 750, "corp_branch_manager": 1_000,
            "high_ranking_corp_exec": 5_000, "oligarchic_elite": 10_000,
        }
        self.assertEqual(COMMON_WAGES, expected)

    def test_wage_lookup_and_error(self) -> None:
        self.assertEqual(wage("gang_boss"), 750)
        with self.assertRaises(LifestyleError):
            wage("freelance wizard")


class BribeTests(unittest.TestCase):
    def test_multiples_match_the_srd(self) -> None:
        self.assertEqual(BRIBE_MULTIPLES["look_the_other_way_minor"], (2, False))
        self.assertEqual(BRIBE_MULTIPLES["small_favour_within_authority"], (5, False))
        self.assertEqual(BRIBE_MULTIPLES["blind_eye_when_it_will_trouble"], (60, True))
        self.assertEqual(BRIBE_MULTIPLES["favour_that_might_get_them_fired"], (180, True))

    def test_a_bribe_is_a_multiple_of_the_targets_daily_wage(self) -> None:
        clerk = wage("street_cop_or_skilled_corp_worker")   # $100/day
        self.assertEqual(bribe_cost("look_the_other_way_minor", daily_wage=clerk), 200)
        self.assertEqual(bribe_cost("favour_that_might_get_them_fired", daily_wage=clerk), 18_000)
        # The SRD's point: a manager costs more than a janitor for the same favour.
        janitor = wage("unskilled_labourer")
        manager = wage("corp_middle_manager")
        self.assertGreater(bribe_cost("small_favour_within_authority", daily_wage=manager),
                           bribe_cost("small_favour_within_authority", daily_wage=janitor))

    def test_serious_favours_are_flagged(self) -> None:
        self.assertFalse(bribe_needs_more_than_cash("pass_out_information"))
        self.assertTrue(bribe_needs_more_than_cash("favour_that_might_get_them_fired"))

    def test_unknown_favour_and_negative_wage_are_refused(self) -> None:
        with self.assertRaises(LifestyleError):
            bribe_cost("overthrow_the_city_council", daily_wage=100)
        with self.assertRaises(LifestyleError):
            bribe_cost("look_the_other_way_minor", daily_wage=-1)

    def test_no_bribe_is_ever_cheaper_than_the_wage_it_references(self) -> None:
        for favour, (multiple, _serious) in BRIBE_MULTIPLES.items():
            self.assertGreaterEqual(multiple, 2, favour)
            self.assertEqual(bribe_cost(favour, daily_wage=25), multiple * 25)


if __name__ == "__main__":
    unittest.main()
