"""Canon checks for the Greater Helsinki register (#1121)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "design" / "GREATER_HELSINKI_2045.md"
DATA = ROOT / "data" / "world" / "greater_helsinki_1121.json"
ZONES = ROOT / "design" / "ZONES.md"


class GreaterHelsinkiCanonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_the_author_document_replaced_the_empty_placeholder(self):
        self.assertIn("Canon — author decision #1121", self.doc)
        self.assertNotIn("Tomi writes below", self.doc)
        self.assertIn("Helsingin Kaupunki", self.doc)
        self.assertIn("Suomen Tasavalta", self.doc)
        self.assertIn("United Nations Security Administration", self.doc)

    def test_four_governance_levels_and_their_agencies(self):
        levels = self.data["governance_levels"]
        self.assertEqual([row["level"] for row in levels],
                         ["municipal", "national", "eu_federal", "global_exceptional"])
        agencies = {agency["id"] for row in levels for agency in row["agencies"]}
        self.assertEqual(agencies, {
            "agency.helsinki_police", "agency.finnish_police", "agency.finnish_defence",
            "agency.europol", "agency.eurodef", "agency.unsa",
        })

    def test_exactly_two_economic_and_two_diplomatic_zones(self):
        zones = self.data["extraterrestrial_zones"]
        self.assertEqual(len(zones), 4)
        self.assertEqual([zone["category"] for zone in zones].count("economic"), 2)
        self.assertEqual([zone["category"] for zone in zones].count("diplomatic"), 2)
        self.assertEqual({zone["administration"] for zone in zones if zone["category"] == "economic"},
                         {"joint_human_extraterrestrial"})
        self.assertEqual({zone["administration"] for zone in zones if zone["category"] == "diplomatic"},
                         {"orion_diplomatic", "confederacy_diplomatic"})

    def test_three_sirian_protection_zones(self):
        zones = self.data["sirian_protection_zones"]
        self.assertEqual(len(zones), 3)
        self.assertEqual({zone["region_name"] for zone in zones}, {"Kajaani", "Lappi", "Karjala"})
        self.assertTrue(all(zone["near_soviet_border"] for zone in zones))
        self.assertEqual(self.data["sirian_notes"]["fleet_handover"],
                         "given_to_finland_and_requested_scrapped")

    def test_hyvinkaa_keeps_the_mystery_and_the_internet_prohibition(self):
        zone = next(z for z in self.data["military_exclusion_zones"] if z["id"].startswith("zone.hyvinkaa"))
        self.assertTrue(zone["entire_area_excluded"])
        self.assertEqual(zone["internet_connection"], "prohibited")
        self.assertEqual(zone["central_asi_status"], "unknown")
        self.assertEqual(zone["borg_population"], "contested_rumour")
        self.assertEqual(zone["emp_nuclear_strike"], "proposed_not_settled")

    def test_loviisa_does_not_force_a_sci_fantasy_twist(self):
        zone = next(z for z in self.data["military_exclusion_zones"] if z["id"].startswith("zone.loviisa"))
        self.assertFalse(zone["entire_area_excluded"])
        self.assertTrue(zone["radiation_contained"])
        self.assertFalse(zone["compulsory_supernatural_twist"])
        self.assertEqual(zone["reactor_description"], "old Soviet reactors")

    def test_ids_are_unique_and_do_not_invent_coordinates(self):
        all_rows = self.data["governance_levels"] + self.data["extraterrestrial_zones"] + \
            self.data["sirian_protection_zones"] + self.data["military_exclusion_zones"]
        ids = [row["id"] for row in all_rows]
        self.assertEqual(len(ids), len(set(ids)))
        for row in self.data["extraterrestrial_zones"] + self.data["military_exclusion_zones"]:
            self.assertNotIn("coordinates", row)
            self.assertNotIn("boundary", row)

    def test_zones_note_points_to_the_canonical_register(self):
        text = ZONES.read_text(encoding="utf-8")
        self.assertIn("GREATER_HELSINKI_2045.md", text)


if __name__ == "__main__":
    unittest.main()
