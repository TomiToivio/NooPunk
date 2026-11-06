"""The Orion–MJ-12 base register must not claim more than its sources (#1253).

The whole risk of this dossier is a base table that quietly turns a region into a grid reference, a human
installation into a joint one, or a channeled claim into a fact. These tests are structural: provenance
tags must exist and be known, a Ra-sourced entry may not mention MJ-12, a shared entry must carry the canon
tag that makes the sharing ours, no entry may carry coordinates, and the two factions that are *not* Orion
must stay that way.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "world" / "orion_mj12_bases_1253.json"
DOC = ROOT / "docs" / "world" / "ORION_MJ12_1253.md"

TAGS = {"RA", "MJ12_LORE", "NOOPUNK", "OPEN", "HISTORICAL"}
COORDINATE_KEYS = {"coordinates", "lat", "lon", "lng", "latitude", "longitude", "grid", "grid_ref"}


class BaseRegisterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.entries = {entry["id"]: entry for entry in cls.data["entries"]}

    def test_format_and_source(self):
        self.assertEqual(self.data["format"], "noopunk.world.orion_mj12_bases")
        self.assertIn("/issues/1253", self.data["source_issue"])
        self.assertTrue(COORDINATE_KEYS and self.data["coordinates"] == "refused")

    def test_every_entry_is_complete(self):
        required = {
            "id", "label", "region", "physical_type", "operators", "era", "function", "cover",
            "public_knowledge", "jurisdiction", "status_2045", "sources", "hooks",
        }
        for entry in self.data["entries"]:
            missing = required - set(entry)
            self.assertEqual(missing, set(), f"{entry['id']} is missing {sorted(missing)}")
            self.assertTrue(entry["hooks"], f"{entry['id']} has no adventure hook")

    def test_sources_are_known_tags(self):
        for entry in self.data["entries"]:
            for source in entry["sources"]:
                head = source.split()[0]
                self.assertIn(head, TAGS, f"{entry['id']} cites an unknown provenance tag {source!r}")

    def test_ra_entries_cite_a_session_and_never_name_mj12(self):
        for entry in self.data["entries"]:
            ra_sources = [s for s in entry["sources"] if s.startswith("RA ")]
            if not ra_sources:
                continue
            for source in ra_sources:
                self.assertRegex(source, r"^RA \d", f"{entry['id']} cites Ra without a session")
            blob = json.dumps(entry).lower()
            self.assertNotIn("mj-12", blob,
                             f"{entry['id']} is a Ra claim; the source never names MJ-12")
            self.assertNotIn("mj12", blob, f"{entry['id']} is a Ra claim; the source never names MJ-12")

    def test_a_shared_site_is_marked_as_our_synthesis(self):
        """Ra describes two operators in one sea; it never says the installations are the same."""
        shared = [
            e for e in self.data["entries"]
            if "Orion" in e["operators"] and any("human" in op for op in e["operators"])
        ]
        self.assertTrue(shared, "the register should contain the one shared complex")
        for entry in shared:
            self.assertIn("NOOPUNK", entry["sources"],
                          f"{entry['id']} claims a shared site without the canon tag that makes it ours")

    def test_no_coordinates_anywhere(self):
        for entry in self.data["entries"]:
            self.assertIsNone(entry.get("coordinates"), f"{entry['id']} carries coordinates")
            for key in COORDINATE_KEYS:
                if key == "coordinates":
                    continue
                self.assertNotIn(key, entry, f"{entry['id']} smuggles in a {key}")

    def test_the_non_orion_sites_stay_non_orion(self):
        hyvinkaa = self.entries["hyvinkaa"]
        self.assertNotIn("Orion", hyvinkaa["operators"])
        self.assertIn("NOT an Orion", hyvinkaa["status_2045"])
        mars = self.entries["mars-eldrich"]
        self.assertEqual(mars["operators"], ["Eldrich Corporation"])

    def test_open_sites_are_marked_open(self):
        for site in ("dulce", "area-51", "lunar"):
            self.assertIn("OPEN", self.entries[site]["sources"], f"{site} is presented as settled")


class DossierTests(unittest.TestCase):
    def test_the_dossier_states_its_provenance_rule(self):
        text = DOC.read_text(encoding="utf-8")
        for tag in ("[RA]", "[MJ12 LORE]", "[NOÖPUNK]", "[OPEN]"):
            self.assertIn(tag, text)
        self.assertIn("not historical proof", text)

    def test_the_dossier_keeps_orion_and_mj12_distinct(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("They are **not synonyms**", text)
        self.assertIn("The source does not say \"MJ-12\"", text)

    def test_the_1981_inventory_is_not_a_2045_inventory(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("573", text)
        self.assertIn("not a\n2045 inventory", text.replace("\r", ""))

    def test_it_defers_to_the_existing_faction_source(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("NHI_FACTIONS_922.md", text)
        self.assertIn("Supersedes nothing", text)


if __name__ == "__main__":
    unittest.main()
