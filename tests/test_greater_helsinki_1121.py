"""Regression tests for the #1121 Helsinki operational register."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.world.greater_helsinki_1121 import (
    HelsinkiCanonError,
    claims_for,
    get_zone,
    load_register,
    zone_lookup_by_category,
)


class GreaterHelsinkiTests(unittest.TestCase):
    def test_merged_municipality_and_four_governance_levels(self):
        register = load_register()
        self.assertEqual(register["municipality"]["id"], "helsinki_2045")
        self.assertEqual(
            [level["level"] for level in register["governance"]],
            ["municipal", "national", "eu", "global_xrisk"],
        )
        self.assertEqual(
            [[agency["id"] for agency in level["agencies"]] for level in register["governance"]],
            [["helsingin_poliisi"], ["suomen_poliisi", "suomen_puolustusvoimat"],
             ["europol", "eurodef"], ["unsa"]],
        )

    def test_economic_and_diplomatic_are_not_interchangeable(self):
        self.assertEqual(
            {zone["id"] for zone in zone_lookup_by_category("economic")},
            {"espoo_oittaa_economic", "helsinki_vantaa_economic"},
        )
        self.assertEqual(
            {zone["id"] for zone in zone_lookup_by_category("diplomatic")},
            {"villinki_orion_diplomatic", "vallisaari_confederacy_diplomatic"},
        )
        self.assertIn("joint", get_zone("espoo_oittaa_economic")["administration"])
        self.assertIn("authorized official", get_zone("villinki_orion_diplomatic")["access"])

    def test_sirian_protection_zones_do_not_become_free_trade_zones(self):
        self.assertEqual(
            {zone["id"] for zone in zone_lookup_by_category("protection")},
            {"kajaani_sirian_protection", "lappi_sirian_protection", "karjala_sirian_protection"},
        )
        self.assertTrue(all("refugee" in zone["access"] for zone in zone_lookup_by_category("protection")))
        self.assertEqual(
            {item["status"] for item in claims_for("kajaani_sirian_protection")},
            {"setting_fact", "unresolved", "contested_history"},
        )

    def test_exclusion_zones_have_different_extent_and_evidence(self):
        self.assertEqual(get_zone("hyvinkaa_military_exclusion")["boundary_status"], "whole_area")
        self.assertEqual(
            get_zone("loviisa_military_exclusion")["boundary_status"],
            "plant_and_surroundings_only",
        )
        self.assertIn("internet", get_zone("hyvinkaa_military_exclusion")["access"])
        self.assertEqual(
            {claim["id"]: claim["status"] for claim in claims_for("hyvinkaa_military_exclusion")}[
                "hyvinkaa_borgs"
            ],
            "rumor",
        )
        self.assertEqual(
            {claim["id"]: claim["status"] for claim in claims_for("loviisa_military_exclusion")}[
                "loviisa_meltdown"
            ],
            "agency_report",
        )

    def test_no_invented_routes_or_treaty_powers(self):
        data = load_register()
        self.assertEqual(data["routes"], [])
        self.assertEqual(data["coordinates"], [])
        self.assertTrue(data["jurisdiction_policy"]["no_blanket_extraterritoriality"])
        self.assertTrue(data["jurisdiction_policy"]["no_automatic_arrest_or_search_power"])

    def test_unknown_zone_is_rejected(self):
        with self.assertRaises(HelsinkiCanonError):
            get_zone("invented_embassy")

    def test_refuse_promotion_of_rumor_or_invented_routes(self):
        original = load_register()
        for mutation in ("rumor_as_fact", "route"):
            data = json.loads(json.dumps(original))
            if mutation == "rumor_as_fact":
                next(claim for claim in data["claims"] if claim["id"] == "hyvinkaa_borgs")["status"] = "verified"
            else:
                data["routes"].append(["hyvinkaa", "loviisa"])
            with tempfile.TemporaryDirectory() as folder:
                target = Path(folder) / "world.json"
                target.write_text(json.dumps(data), encoding="utf-8")
                with self.assertRaises(HelsinkiCanonError):
                    load_register(target)


if __name__ == "__main__":
    unittest.main()
