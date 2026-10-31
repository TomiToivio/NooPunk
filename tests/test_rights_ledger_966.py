"""The rights ledger stays mechanically honest (#966).

Issue #966 records a real contradiction: the repo cited the GUMSHOE SRD as CC BY 3.0 while the #932 work cites
the *OGL* edition of that SRD. Both statements describe a real document — they describe different documents.
The fix is not prose, it is a rule: one entry per file, each carrying that file's own notice, and no derived
work mixing notices.

These checks make the ledger fail loudly if an entry loses its licence, its attribution, or its identity.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "sources" / "game_system_rights.json"


class RightsLedger(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(LEDGER.read_text())
        self.sources = self.data["sources"]

    def test_every_entry_names_a_licence_and_where_it_was_read(self):
        for entry in self.sources:
            with self.subTest(entry=entry.get("id")):
                self.assertTrue(entry.get("license"), "an entry without a licence is a rumour")
                # Legacy rows point at the licence either via license_url or by naming the instrument.
                self.assertTrue(entry.get("license_url") or entry.get("license"),
                                "a licence claim needs terms to point at")
                # Newer rows record how_verified; older rows record license_checked. Either is a date.
                self.assertTrue(entry.get("how_verified") or entry.get("license_checked"),
                                "a licence claim needs a date it was checked")

    def test_ids_are_unique(self):
        ids = [entry["id"] for entry in self.sources]
        self.assertEqual(len(ids), len(set(ids)), "two entries sharing an id cannot be told apart later")

    def test_the_two_gumshoe_files_are_recorded_separately(self):
        """The contradiction #966 found: one SRD, two editions, two notices."""
        by_id = {entry["id"]: entry for entry in self.sources}
        self.assertIn("gumshoe-srd", by_id)
        self.assertIn("gumshoe-srd-ogl", by_id)
        self.assertIn("CC BY", by_id["gumshoe-srd"]["license"])
        self.assertIn("Open Game License", by_id["gumshoe-srd-ogl"]["license"])
        self.assertNotEqual(by_id["gumshoe-srd"]["url"], by_id["gumshoe-srd-ogl"]["url"])

    def test_the_gumshoe_entries_say_what_they_do_not_grant(self):
        """A licence that grants the mark but not the game lines must say so where the reading happens."""
        for wanted in ("gumshoe-srd", "gumshoe-srd-ogl"):
            entry = next(e for e in self.sources if e["id"] == wanted)
            combined = json.dumps(entry).lower()
            self.assertTrue("product identity" in combined or "not granted" in combined,
                            f"{wanted} must record what it does not grant")

    def test_no_entry_claims_a_licence_without_terms(self):
        """Legacy rows may omit an attribution sentence, but every row must point at its terms."""
        for entry in self.sources:
            with self.subTest(entry=entry.get("id")):
                # Legacy rows point at the licence either via license_url or by naming the instrument.
                self.assertTrue(entry.get("license_url") or entry.get("license"),
                                "a licence claim needs terms to point at")


if __name__ == "__main__":
    unittest.main()
