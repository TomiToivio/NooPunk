"""The CWN traceability inventory must stay honest and resolvable (#1068).

The inventory is a claim about coverage; `tools/cwn_rule_inventory_audit.py --check` is the check. This
test runs the check and then pins the two properties that make the claim meaningful:

* nothing may *shrink* silently: every chapter and section of the Deluxe book is a row;
* a row may not claim `implemented` while naming no Python test.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "rules" / "cwn_rule_inventory.json"


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(INVENTORY.read_text(encoding="utf-8"))

    def test_the_audit_passes(self):
        completed = subprocess.run([sys.executable, str(ROOT / "tools" / "cwn_rule_inventory_audit.py"),
                                    "--check"], capture_output=True, text=True, timeout=300, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_every_row_carries_a_printed_page(self):
        for row in self.data["rows"]:
            self.assertIsInstance(row["printed_page"], int, row["id"])
            self.assertGreater(row["printed_page"], 0, row["id"])

    def test_the_book_is_covered_chapter_by_chapter(self):
        chapters = {row["chapter"] for row in self.data["rows"]}
        expected = {"Character Creation", "The Rules of the Game", "The Tools of the Trade", "Hacking",
                    "Creating Your Dystopia", "Creating and Running Missions", "Faces On the Street",
                    "The City", "Mixing Sine Nomine Games Together", "Supplemental Material"}
        self.assertEqual(chapters, expected, "a missing chapter is a missing audit")

    def test_no_untested_claim_of_coverage(self):
        for row in self.data["rows"]:
            if row["status"] == "implemented":
                self.assertTrue(row.get("tests"), f"{row['id']} claims implemented without tests")

    def test_the_supplemental_chapter_is_audited_rather_than_ignored(self):
        """The Deluxe-only material is exactly where a free-edition audit goes blind."""
        supplemental = [row for row in self.data["rows"] if row["chapter"] == "Supplemental Material"]
        self.assertGreaterEqual(len(supplemental), 10)
        statuses = {row["id"].split(":")[1]: row["status"] for row in supplemental}
        self.assertEqual(statuses["cyber-alienation"], "implemented")
        self.assertEqual(statuses["mages-spellcasting"], "implemented")
        self.assertEqual(statuses["summoners-spirits"], "partial", "Effort only; spirit statistics are content")

    def test_the_report_document_is_generated_from_the_data(self):
        document = ROOT / "docs" / "rules" / "CWN_RULE_INVENTORY.md"
        self.assertTrue(document.exists(), "run the tool with --markdown")
        text = document.read_text(encoding="utf-8")
        for row in self.data["rows"]:
            marker = f"| {row['printed_page']} |"
            self.assertIn(marker, text, "the document is stale; regenerate it from the data")


if __name__ == "__main__":
    unittest.main()
