"""Contract for the SWN register and its report (#1105).

The register is only worth having if it cannot rot: the report must be the tool's own output, every citation
must resolve to a section that exists in the extracted index, every implemented row must name evidence that
still exists, and no row may claim an implementation without one.

The Deluxe source is the author's purchased copy and is not in the repository, so the extraction is checked
against the PDF only when the file is present; otherwise the committed index is checked for internal
consistency and against the rows that cite it.
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

from swn_parity_audit import REPORT, STATUSES, EVIDENCED, build, render  # noqa: E402

REGISTER = ROOT / "data" / "rules" / "swn_traceability.json"
SECTIONS = ROOT / "data" / "rules" / "swn_sections.json"
PDF = Path(os.environ.get("SWN_DELUXE_PDF", Path.home() / "Lataukset" / "StarsWithoutNumberRevised-DeluxeEdition-011418.pdf"))


def register() -> dict:
    return json.loads(REGISTER.read_text(encoding="utf-8"))


def index() -> dict:
    return json.loads(SECTIONS.read_text(encoding="utf-8"))


class SectionIndexTests(unittest.TestCase):
    def test_the_index_covers_the_whole_book(self) -> None:
        data = index()
        # SWN prints a running head on recto pages only, so the extraction finds ~116 titled sections
        # rather than one per page; the threshold is the measured count, not a guess.
        self.assertGreaterEqual(len(data["sections"]), 110,
                                "the running-head extraction should find every titled section")
        self.assertEqual(data["source"]["isbn"], "978-1-936673-95-7")

    def test_ids_are_unique_and_ordered_by_page(self) -> None:
        sections = index()["sections"]
        ids = [s["id"] for s in sections]
        self.assertEqual(len(ids), len(set(ids)))
        pages = [s["first_page"] for s in sections]
        self.assertEqual(pages, sorted(pages))

    def test_every_section_names_a_known_chapter(self) -> None:
        data = index()
        chapters = {c["title"] for c in data["chapters"]}
        for section in data["sections"]:
            self.assertIn(section["chapter"], chapters, section["id"])

    def test_the_deluxe_chapters_are_present(self) -> None:
        """The point of the index: the Deluxe-only material is now citable, not guessed from chapter names."""
        ids = {s["id"] for s in index()["sections"]}
        self.assertGreaterEqual(len(ids), 110)
        for expected in ("psionics", "biopsionics", "factions-assets-and-turns", "cunning-assets",
                         "transhuman-campaigns", "space-magic", "true-artificial-intelligences",
                         "designing-mechs"):
            self.assertIn(expected, ids)

    def test_the_extraction_still_matches_the_pdf_when_it_is_available(self) -> None:
        if not PDF.is_file():
            self.skipTest("authorised Deluxe PDF not present; the committed index is the reference")
        result = subprocess.run([sys.executable, "tools/swn_section_index.py", "--pdf", str(PDF), "--check"],
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
                             f"{row['id']}: cited p.{row['page']}, running head says p.{section['first_page']}")

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

    def test_a_non_implemented_row_does_not_cite_modules(self) -> None:
        for row in self.data["rows"]:
            if row["status"] in EVIDENCED:
                continue
            self.assertEqual(row["modules"], [], f"{row['id']}: cites modules without claiming them")

    def test_every_gap_names_its_section_and_a_reason(self) -> None:
        """A gap row must say what is absent. "Missing" alone is a shrug, not a register entry.

        The check is deliberately about *content that a reader can act on* — the section is named and the
        note says something about it — rather than about matching a phrase list, which only teaches the
        next author to write to the test.
        """
        for row in self.data["rows"]:
            if row["status"] in {"missing", "unverified", "partial"}:
                note = row["note"]
                self.assertGreaterEqual(len(note), 25, f"{row['id']}: a gap with no explanation")
                self.assertTrue(note.rstrip().endswith("."),
                                f"{row['id']}: the note is a fragment, not a reason: {note!r}")

    def test_statuses_are_from_the_documented_vocabulary(self) -> None:
        for row in self.data["rows"]:
            self.assertIn(row["status"], STATUSES, row["id"])
        self.assertEqual(set(self.data["statuses"]), set(STATUSES))

    def test_the_source_states_its_availability_and_rights(self) -> None:
        source = self.data["source"]["swn_deluxe"]
        self.assertIn("authorised", source["availability"])
        self.assertIn("not redistributable", source["availability"])

    def test_every_section_of_the_book_is_registered(self) -> None:
        """#1105: an inventory, not a sample. A section absent from the register is a hole nobody can see."""
        missing = sorted(set(self.sections) - set(self.rows))
        self.assertEqual(missing, [], f"sections with no register row: {missing}")

    def test_the_p0_workstreams_are_present(self) -> None:
        """Psionics and Factions are the two the tracker makes P0; they cannot be quietly omitted."""
        for section in ("psionics", "biopsionics", "metapsionics", "precognition", "telekinesis",
                        "telepathy", "teleportation", "factions-assets-and-turns", "faction-actions",
                        "cunning-assets", "force-assets", "wealth-assets"):
            self.assertIn(section, self.rows, section)

    def test_psi_and_factions_do_not_claim_completeness(self) -> None:
        """The tracker warns that existing modules are not proof; a `verified` claim needs printed numbers."""
        for section in ("psionics", "factions-assets-and-turns"):
            self.assertIn(self.rows[section]["status"], {"partial", "unverified"})
            self.assertTrue(self.rows[section]["note"].strip())


class ReportFreshnessTests(unittest.TestCase):
    def test_the_report_is_the_tools_own_output(self) -> None:
        self.assertTrue(REPORT.is_file(), "run python3 tools/swn_parity_audit.py")
        self.assertEqual(REPORT.read_text(encoding="utf-8"), render(build()),
                         "docs/rules/SWN_COVERAGE_1105.md is stale; run python3 tools/swn_parity_audit.py")

    def test_the_check_mode_agrees_with_the_test(self) -> None:
        result = subprocess.run([sys.executable, "tools/swn_parity_audit.py", "--check"],
                                cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_the_report_never_claims_more_coverage_than_the_register(self) -> None:
        counts = build()["counts"]
        text = REPORT.read_text(encoding="utf-8")
        for status in STATUSES:
            self.assertIn(f"**{counts[status]}**", text)


if __name__ == "__main__":
    unittest.main()
