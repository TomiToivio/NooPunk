"""Contract for the AWN register and its report (#1109).

The AWN copy has a detailed table of contents, so the index does not have to be inferred from running heads:
`tools/awn_section_index.py` parses the contents pages and then **checks every entry against the page it
names**. That check is the difference between an inventory and a guess, and this suite keeps it honest:

* the committed index must be the tool's own output (and re-verifiable when the author's copy is present);
* every register row must cite a section that exists, at the page the contents page gives;
* a row claiming code must name a module and a test that references it;
* a row claiming a written procedure must cite a document that exists;
* every section of the book must have a row — a missing row is a gap nobody can see.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from awn_parity_audit import DOCUMENTED, EVIDENCED, REPORT, STATUSES, build, render  # noqa: E402

REGISTER = ROOT / "data" / "rules" / "awn_traceability.json"
SECTIONS = ROOT / "data" / "rules" / "awn_sections.json"
PDF = Path(os.environ.get("AWN_DELUXE_PDF",
                          Path.home() / "Lataukset" / "AshesWithoutNumber_Deluxe_061125-1.pdf"))


def register() -> dict:
    return json.loads(REGISTER.read_text(encoding="utf-8"))


def index() -> dict:
    return json.loads(SECTIONS.read_text(encoding="utf-8"))


class SectionIndexTests(unittest.TestCase):
    def test_the_index_covers_the_whole_book(self) -> None:
        data = index()
        self.assertGreaterEqual(len(data["sections"]), 125,
                                "the contents page should yield every titled section")
        self.assertEqual(data["source"]["title"], "Ashes Without Number, Deluxe Edition")

    def test_every_contents_entry_was_found_on_its_page(self) -> None:
        """The tool verifies each title against the page the contents page names; none may be unverified."""
        self.assertEqual(index()["unverified_entries"], [])

    def test_ids_are_unique_and_ordered(self) -> None:
        sections = index()["sections"]
        ids = [s["id"] for s in sections]
        self.assertEqual(len(ids), len(set(ids)))
        pages = [s["first_page"] for s in sections]
        self.assertEqual(pages, sorted(pages))

    def test_the_chapters_named_by_the_tracker_are_all_present(self) -> None:
        chapters = {c["title"] for c in index()["chapters"]}
        for expected in ("Character Creation", "The Rules of the Game", "Equipment",
                         "Enclaves and Settlements", "Creating Your Campaign",
                         "Building Encounter Sites", "Creating Adventures", "Creatures of the Wastes"):
            self.assertIn(expected, chapters)

    def test_the_extraction_still_matches_the_book_when_it_is_available(self) -> None:
        if not PDF.is_file():
            self.skipTest("authorised AWN copy not present; the committed index is the reference")
        result = subprocess.run([sys.executable, "tools/awn_section_index.py", "--pdf", str(PDF), "--check"],
                                cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class RegisterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = register()
        self.sections = {s["id"]: s for s in index()["sections"]}
        self.rows = {row["id"]: row for row in self.data["rows"]}

    def test_every_row_cites_a_real_section_and_page(self) -> None:
        for row in self.data["rows"]:
            section = self.sections.get(row["id"])
            self.assertIsNotNone(section, f"{row['id']}: not a section of the book")
            self.assertEqual(row["page"], section["first_page"],
                             f"{row['id']}: cited p.{row['page']}, contents page says p.{section['first_page']}")

    def test_every_section_of_the_book_is_registered(self) -> None:
        missing = sorted(set(self.sections) - set(self.rows))
        self.assertEqual(missing, [], f"sections with no register row: {missing}")

    def test_no_row_claims_more_than_its_evidence(self) -> None:
        matrix = build()
        self.assertEqual(matrix["problems"], {},
                         f"rows whose evidence does not verify: {matrix['problems']}")

    def test_implemented_rows_name_a_module_a_test_and_a_rulebook(self) -> None:
        for row in self.data["rows"]:
            if row["status"] not in EVIDENCED:
                continue
            self.assertTrue(row["modules"], f"{row['id']}: no module")
            self.assertTrue(row["tests"], f"{row['id']}: no test")
            self.assertTrue((ROOT / row["rulebook"]).is_file(), f"{row['id']}: rulebook anchor missing")

    def test_documented_rows_cite_a_document_that_exists(self) -> None:
        documented = [row for row in self.data["rows"] if row["status"] in DOCUMENTED]
        self.assertTrue(documented, "the cross-game mixing procedure must be registered somewhere")
        for row in documented:
            self.assertTrue((ROOT / row["rulebook"]).is_file(), row["id"])

    def test_a_non_implemented_row_does_not_cite_modules(self) -> None:
        for row in self.data["rows"]:
            if row["status"] in EVIDENCED:
                continue
            self.assertEqual(row["modules"], [], f"{row['id']}: cites modules without claiming them")

    def test_statuses_are_from_the_documented_vocabulary(self) -> None:
        for row in self.data["rows"]:
            self.assertIn(row["status"], STATUSES, row["id"])
        self.assertEqual(set(self.data["statuses"]), set(STATUSES))

    def test_the_trackers_p0_rows_are_present_and_not_overstated(self) -> None:
        """Stress, survival, cross-game mixing and enclaves are the P0 audit rows the tracker names."""
        for section in ("stress", "overland-travel-and-scouting", "hunger-thirst-and-supplies",
                        "mixing-sine-nomine-games-together", "enclave-actions", "saving-throws"):
            self.assertIn(section, self.rows, section)
        # Enclave actions are the declared #1083 gap: no row may claim them.
        self.assertEqual(self.rows["enclave-actions"]["status"], "missing")
        # Saves are CWN's, but unverified for AWN: an honest middle, not a claim.
        self.assertEqual(self.rows["saving-throws"]["status"], "unverified")

    def test_the_excluded_setting_is_recorded_as_a_decision(self) -> None:
        """The Albuquerque Death Zone is proprietary; excluding it is a decision, not an omission."""
        for section in ("the-albuquerque-death-zone", "the-cowboy"):
            self.assertEqual(self.rows[section]["status"], "not_applicable")
            self.assertIn("setting", self.rows[section]["note"].lower())

    def test_the_source_states_its_rights_and_availability(self) -> None:
        source = self.data["source"]["awn_deluxe"]
        self.assertIn("authorised", source["availability"])
        self.assertIn("not redistributable", source["availability"])
        self.assertIn("no verified open-text licence", source["rights"])


class ReportFreshnessTests(unittest.TestCase):
    def test_the_report_is_the_tools_own_output(self) -> None:
        self.assertTrue(REPORT.is_file(), "run python3 tools/awn_parity_audit.py")
        self.assertEqual(REPORT.read_text(encoding="utf-8"), render(build()),
                         "docs/rules/AWN_SECTION_COVERAGE_1109.md is stale; run tools/awn_parity_audit.py")

    def test_the_check_mode_agrees_with_the_test(self) -> None:
        result = subprocess.run([sys.executable, "tools/awn_parity_audit.py", "--check"],
                                cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
