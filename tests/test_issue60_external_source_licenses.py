"""Structure guard for the external source license audit (issue #60).

Issue #60 lists a set of external rules references, data repositories and conversion
documents, and requires that "External repositories, fan conversions and third-party data
sources must be checked individually before material is copied into NoöPunk." The audit
records that check. This guard protects the PROPERTIES a later session could silently
drift, not the individual findings, which are dated observations that legitimately change
when a license changes.

What is protected:

* the audit document and its machine-readable record both exist and are discoverable from
  the sources document that issue #60's first implementation already added;
* every source issue #60 names is accounted for, by URL or by name -- a source quietly
  dropped from the audit is the failure mode, because the audit is what a later importer
  would trust;
* every source carries a decision, and the decision vocabulary is closed -- an entry
  cannot invent a permissive-sounding verdict;
* **no source is marked importable without a license** -- the one rule that turns the
  audit from documentation into a gate;
* the blocked verification is recorded as blocked rather than as a licence finding, so a
  fetch failure never silently becomes "no license, fine to use";
* **nothing is recorded as imported**, because the audit exists to keep the initial kernel
  a reimplementation rather than a copy;
* the published PDF is explicitly not redistributed, and no PDF is committed;
* the ShareAlike and NonCommercial consequences survive, since they are the clauses that
  actually constrain the codebase.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = "docs/sources/EXTERNAL_SOURCE_LICENSES.md"
AUDIT_JSON = "data/sources/external_sources.json"
SOURCES_DOC = "docs/sources/EP2_HOME_BREW_SOURCES.md"

#: The decision vocabulary. An entry MUST use one of these; the point is that
#: "unclear", "unverified" and "not-present" cannot be laundered into "fine".
DECISIONS = {
    "importable-ep-derived",
    "unclear-do-not-import",
    "unverified-do-not-import",
    "not-present",
}

#: (label used in the audit's document, needles that must appear in the matching JSON entry)
#: Every external source issue #60 names, plus the author's thread addition.
REQUIRED_SOURCES = (
    ("EP2 online rules", "eclipsephase.github.io"),
    ("Quick-Start", "QuickStartRules"),
    ("Artemystra", "Artemystra/eclipsephase"),
    ("eclipse-phase-2-tools", "ralfbiedert/eclipse-phase-2-tools"),
    ("Eclipse Helper", "eclipsehelper"),
    ("PbtA", "eclipse-phase-apocalypse"),
    ("EP1 PDF index", "robboyle.wordpress.com"),
)

#: (label, needle) for the document, where the wording legitimately differs.
REQUIRED_DOC_TERMS = (
    ("EP2 online rules", "EP2 online rules"),
    ("Quick-Start", "Quick-Start"),
    ("Artemystra", "Artemystra"),
    ("eclipse-phase-2-tools", "eclipse-phase-2-tools"),
    ("Eclipse Helper", "Eclipse Helper"),
    ("PbtA", "PbtA"),
    ("EP1 PDF index", "Boyle"),
)


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _records() -> dict:
    return json.loads(_text(AUDIT_JSON))


class AuditExistsTests(unittest.TestCase):
    def test_audit_document_exists(self) -> None:
        self.assertTrue((ROOT / AUDIT_DOC).exists(), f"{AUDIT_DOC} is missing")

    def test_machine_readable_record_exists(self) -> None:
        self.assertTrue((ROOT / AUDIT_JSON).exists(), f"{AUDIT_JSON} is missing")

    def test_record_is_valid_json_with_the_repository_data_conventions(self) -> None:
        data = _records()
        self.assertIn("format", data)
        self.assertIn("version", data)
        self.assertIsInstance(data.get("sources"), list)
        self.assertTrue(data["sources"], "the audit records no sources at all")

    def test_the_existing_sources_document_points_at_the_audit(self) -> None:
        """The sibling document that #60 added says the check is pending; it must now link
        to the check, or a reader stops at 'not yet checked' and duplicates the work."""
        text = _text(SOURCES_DOC)
        self.assertIn("EXTERNAL_SOURCE_LICENSES.md", text)


class CoverageTests(unittest.TestCase):
    def test_every_source_issue_60_names_appears_in_the_record(self) -> None:
        blob = json.dumps(_records())
        for label, needle in REQUIRED_SOURCES:
            with self.subTest(source=label):
                self.assertIn(needle, blob, f"{label} is missing from the audit record")

    def test_every_source_issue_60_names_appears_in_the_document(self) -> None:
        text = _text(AUDIT_DOC)
        for label, needle in REQUIRED_DOC_TERMS:
            with self.subTest(source=label):
                self.assertIn(needle, text, f"{label} is missing from the audit document")

    def test_the_attached_conversions_are_recorded_as_absent(self) -> None:
        """The four attachments named by the issue are not on disk. Saying so is the
        finding; a later session must not assume they were reviewed and passed."""
        blob = json.dumps(_records())
        self.assertIn("attached-fate-and-nco-conversions", blob)
        entry = next(s for s in _records()["sources"]
                     if s["id"] == "attached-fate-and-nco-conversions")
        self.assertEqual(entry["importable"], "not-present")


class DecisionTests(unittest.TestCase):
    def test_every_source_carries_a_decision_from_the_closed_vocabulary(self) -> None:
        for entry in _records()["sources"]:
            with self.subTest(source=entry.get("id")):
                self.assertIn(entry.get("importable"), DECISIONS)

    def test_no_source_is_importable_without_a_license(self) -> None:
        """The gate rule: a positive decision requires a stated license."""
        for entry in _records()["sources"]:
            if entry.get("importable") == "importable-ep-derived":
                with self.subTest(source=entry["id"]):
                    self.assertTrue(entry.get("license"),
                                    f"{entry['id']} is importable but states no license")
                    self.assertNotIn("NONE", str(entry.get("license")).upper())
                    self.assertNotIn("UNVERIFIED", str(entry.get("license")).upper())

    def test_the_unlicensed_repositories_are_not_importable(self) -> None:
        by_id = {s["id"]: s for s in _records()["sources"]}
        self.assertEqual(by_id["ralfbiedert-eclipse-phase-2-tools"]["importable"],
                         "unclear-do-not-import")
        self.assertNotEqual(by_id["eclipsehelper"]["importable"], "importable-ep-derived")

    def test_the_blocked_verification_is_recorded_as_blocked(self) -> None:
        """A 403 is not evidence of permissiveness. It must stay 'unverified'."""
        by_id = {s["id"]: s for s in _records()["sources"]}
        self.assertEqual(by_id["pbtA-conversion"]["importable"], "unverified-do-not-import")

    def test_the_governing_license_and_attribution_line_are_recorded(self) -> None:
        basis = _records()["license_basis"]
        self.assertIn("CC BY-NC-SA", basis["statement"])
        self.assertIn("eclipsephase.com", basis["url"])
        self.assertIn("Posthuman Studios", basis["attribution_line"])


class ImportBoundaryTests(unittest.TestCase):
    def test_the_audit_records_that_nothing_has_been_imported(self) -> None:
        imports = _records()["current_imports"]
        self.assertTrue(imports["summary"].startswith("None"),
                        "the audit claims an import; the initial kernel is a reimplementation")

    def test_no_pdf_is_committed_anywhere_in_the_repository(self) -> None:
        """The issue forbids committing third-party-hosted PDFs."""
        offenders = [p.as_posix() for p in ROOT.rglob("*.pdf")
                     if ".git/" not in p.as_posix()]
        self.assertEqual(offenders, [], f"PDFs must not be committed: {offenders}")

    def test_the_redistributed_pdf_is_marked_not_redistributable(self) -> None:
        by_id = {s["id"]: s for s in _records()["sources"]}
        self.assertIs(by_id["ep2-quickstart-rules"]["redistributable_pdf"], False)
        self.assertIs(by_id["ep1-pdf-links"]["redistributable_pdf"], False)

    def test_the_ep_derived_boundary_is_stated(self) -> None:
        boundary = _records()["boundary"]
        self.assertEqual(set(boundary["ep_derived_code_paths"]),
                         {"src/eclipse_phase_homebrew/",
                          "src/concordia_runtime/ep2_adapter.py"})

    def test_no_ep_derived_path_is_claimed_as_original(self) -> None:
        """The audit must not describe an EP-derived path as NoöPunk-original."""
        boundary = _records()["boundary"]
        self.assertIn("separate", boundary["noopunk_original"].lower())


class ConsequenceTests(unittest.TestCase):
    """The clauses that actually constrain the codebase, not just the paperwork."""

    def test_the_sharealike_consequence_survives(self) -> None:
        text = _text(AUDIT_DOC)
        self.assertRegex(text, r"(?i)sharealike")

    def test_the_noncommercial_consequence_survives(self) -> None:
        text = _text(AUDIT_DOC)
        self.assertRegex(text, r"(?i)noncommercial")

    def test_the_attribution_requirement_names_the_studio_and_url(self) -> None:
        text = _text(AUDIT_DOC)
        self.assertIn("Posthuman Studios", text)
        self.assertIn("eclipsephase.com", text)

    def test_the_document_states_that_nothing_has_been_imported(self) -> None:
        text = _text(AUDIT_DOC)
        self.assertRegex(text, r"(?i)nothing has been imported|no third-party")

    def test_the_document_is_a_license_finding_not_a_rules_summary(self) -> None:
        """Scoped claim check: the audit must not carry EP mechanics. If a later session
        grows it with rule content it becomes EP-derived prose by the back door."""
        text = _text(AUDIT_DOC)
        for mechanic in ("33/66 rule implementation", "roll-under formula",
                         "insight pool maximum"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
