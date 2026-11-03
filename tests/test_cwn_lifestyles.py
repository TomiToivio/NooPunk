"""CWN lifestyle costs, common wages and bribes — table fidelity, one source, edge cases.

Every number is pinned against the SRD's own table, so a wrong edit to the data file fails a test
instead of quietly changing what a month of rent or a bribed clerk costs. The tables live in
`data/rules/cwn/*.json`; the module is the only procedure over them, and the MUD adapter delegates to it.
"""

from __future__ import annotations

import json
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

DATA = ROOT / "data" / "rules" / "cwn"


class LifestyleCostTests(unittest.TestCase):
    def test_monthly_costs_match_the_srd(self) -> None:
        self.assertEqual(LIFESTYLE_COSTS, {
            "squatter": 0, "slum": 300, "middle_class": 1_000, "fine": 5_000, "luxury": 20_000})

    def test_the_module_reads_the_data_file_rather_than_keeping_a_copy(self) -> None:
        on_disk = {row["id"]: row["monthly_cost"] for row in
                   json.loads((DATA / "lifestyles.json").read_text(encoding="utf-8"))["levels"]}
        self.assertEqual(LIFESTYLE_COSTS, on_disk)

    def test_the_srd_middle_tier_is_the_cores_ordinary_tier(self) -> None:
        """Two vocabularies, one tier: ``middle_class`` in the SRD data, ``ordinary`` in cwn_core."""
        self.assertEqual(living_cost("middle_class"), living_cost("ordinary"))
        self.assertEqual(strain_modifier("middle_class"), 0)
        self.assertEqual(strain_modifier("squatter"), -2)
        self.assertEqual(strain_modifier("luxury"), 2)

    def test_every_cost_row_has_a_strain_row(self) -> None:
        """Money and strain are two halves of one rule; a lifestyle in one and not the other is a bug."""
        for lifestyle in LIFESTYLE_COSTS:
            self.assertIsInstance(strain_modifier(lifestyle), int, lifestyle)

    def test_an_unknown_lifestyle_is_an_error_with_the_valid_keys(self) -> None:
        with self.assertRaises(LifestyleError) as caught:
            living_cost("palace")
        self.assertIn("luxury", str(caught.exception))
        with self.assertRaises(LifestyleError):
            strain_modifier("palace")


class WageTests(unittest.TestCase):
    def test_daily_wages_match_the_srd(self) -> None:
        self.assertEqual(len(COMMON_WAGES), 18)
        self.assertEqual(wage("unskilled_street_laborer"), 10)
        self.assertEqual(wage("common_streetwalker"), 20)
        self.assertEqual(wage("street_cop_or_skilled_corp_worker"), 100)
        self.assertEqual(wage("successful_gang_boss"), 750)
        self.assertEqual(wage("oligarchic_elite_of_a_city"), 10_000)

    def test_wages_come_from_the_data_file(self) -> None:
        on_disk = json.loads((DATA / "common_wages.json").read_text(encoding="utf-8"))["wages"]
        self.assertEqual(COMMON_WAGES, on_disk)

    def test_wage_lookup_and_error(self) -> None:
        with self.assertRaises(LifestyleError):
            wage("freelance wizard")


class BribeTests(unittest.TestCase):
    def test_multiples_match_the_srd(self) -> None:
        self.assertEqual(BRIBE_MULTIPLES["look_the_other_way_minor"], (2, False))
        self.assertEqual(BRIBE_MULTIPLES["small_favour_within_authority"], (5, False))
        self.assertEqual(BRIBE_MULTIPLES["blind_eye_when_it_will_trouble"], (60, True))
        self.assertEqual(BRIBE_MULTIPLES["favour_that_might_get_them_fired"], (180, True))
        self.assertEqual(len(BRIBE_MULTIPLES), 8)

    def test_a_bribe_is_a_multiple_of_the_targets_daily_wage(self) -> None:
        clerk = wage("street_cop_or_skilled_corp_worker")   # 100 credits a day
        self.assertEqual(bribe_cost("look_the_other_way_minor", daily_wage=clerk), 200)
        self.assertEqual(bribe_cost("favour_that_might_get_them_fired", daily_wage=clerk), 18_000)
        # The SRD's point: a manager costs more than a janitor for the same favour.
        self.assertGreater(bribe_cost("small_favour_within_authority",
                                       daily_wage=wage("corp_middle_manager")),
                           bribe_cost("small_favour_within_authority",
                                      daily_wage=wage("unskilled_street_laborer")))

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


class SingleSourceTests(unittest.TestCase):
    def test_the_mud_adapter_delegates_to_this_module(self) -> None:
        from mud.nopunk_mud.cwn import economy

        self.assertEqual(economy.daily_wage("successful_gang_boss"), wage("successful_gang_boss"))
        self.assertEqual(economy.hire_cost("bodyguard", 3), 3 * wage("competent_street_bodyguard"))

    def test_the_strain_half_is_still_the_core_table(self) -> None:
        for lifestyle, expected in cwn_core.LIFESTYLE_STRAIN.items():
            self.assertEqual(strain_modifier(lifestyle), expected)


if __name__ == "__main__":
    unittest.main()
