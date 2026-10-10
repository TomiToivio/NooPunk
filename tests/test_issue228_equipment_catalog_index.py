"""The #228 catalog index must never invent equipment statistics."""
import json
import unittest
from pathlib import Path

from src.rules.equipment_catalog_index import ROOT, SOURCES, collect_entries, search_catalog, export_catalog


class EquipmentCatalogIndexTests(unittest.TestCase):
    def test_both_authoritative_light_catalogs_are_indexed(self):
        entries = collect_entries()
        self.assertGreater(len(entries), 15)
        self.assertEqual({e.source for e in entries}, set(SOURCES))
        for item in entries:
            self.assertGreater(item.line, 0)
            self.assertTrue(item.name)
            self.assertTrue(item.description)
            actual = (ROOT / item.source).read_text(encoding="utf-8").splitlines()[item.line - 1]
            self.assertIn(item.name, actual)

    def test_a_known_existing_item_can_be_found_with_provenance(self):
        entries = search_catalog("Commlink / mesh node")
        self.assertTrue(entries)
        self.assertTrue(any(e.source == "rulebook/13_EQUIPMENT.md" for e in entries))
        self.assertTrue(all(e.line > 0 for e in entries))

    def test_search_is_case_insensitive_and_never_mutates(self):
        entries = collect_entries()
        self.assertEqual(search_catalog("FORENSIC", entries), search_catalog("forensic", entries))
        with self.assertRaises(ValueError):
            search_catalog(" ")

    def test_no_runtime_stats_generated_or_licensing_claims_added(self):
        payload = export_catalog()
        self.assertFalse(payload["numeric_stats_finalized"])
        self.assertEqual(payload["canonical_sources"], list(SOURCES))
        self.assertEqual(len(payload["entries"]), len(collect_entries()))
        self.assertNotIn("damage", payload)
        self.assertNotIn("cost", payload)
        json.dumps(payload, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
