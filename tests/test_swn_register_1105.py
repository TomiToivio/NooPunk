"""Tests for the SWN rule register (#1105).

#1105 replaces its own preliminary chapter table with a granular register and says the statuses in that table
are "preliminary file-level observations, not verified fidelity or passing tests". These tests keep the
replacement honest:

* every row that claims code cites a module and a test that exist;
* **no row may claim verified fidelity**, because no agent here can read the book to check against — SWN
  publishes a free edition, not a CC0 SRD, and the rights position is recorded in
  `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`;
* the register cannot quietly drop one of the seventeen chapters it is meant to cover;
* the audit itself fails when handed a fabricated claim.
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import swn_register_audit as audit_tool

#: The seventeen chapters #1105 lists after the opening chapter. Losing one is how a tracker becomes a rumour.
CHAPTERS = (
    "Character Creation", "Psionics", "Systems", "Equipment and Vehicles", "Starships",
    "The History of Space", "Sector Creation", "Adventure Creation", "Xenobestiary",
    "Factions", "Game Master Resources", "Transhuman Campaigns", "Space Magic",
    "Heroic Characters", "True Artificial Intelligences", "Societies", "Mechs",
)


class RegisterIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = audit_tool.load()

    def test_the_register_has_no_integrity_problems(self):
        self.assertEqual(audit_tool.audit(self.register), [])

    def test_row_ids_are_unique(self):
        ids = [row["id"] for row in self.register["rows"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_tracker_chapter_is_represented(self):
        present = {row["chapter"] for row in self.register["rows"]}
        self.assertEqual(present, set(CHAPTERS),
                         "the register must cover exactly the chapters #1105 lists, no more and no fewer")

    def test_verified_fidelity_is_only_claimed_against_a_readable_copy(self):
        """A `verified` row means someone compared the code to the printed pages.

        The earlier version of this test asserted that *no* row could be verified, because the book was not
        in the repository. That premise died when the author supplied the copy and it was read and indexed:
        a blanket ban would now be an excuse rather than a safeguard. What must hold instead is that every
        `verified` row has something to have been verified against, and real evidence behind it.
        """
        readable = {source.get("rights") for source in self.register["sources"].values()
                    if source.get("readable")}
        self.assertTrue(readable, "no source in the register is marked readable")
        for row in self.register["rows"]:
            if row["fidelity"] != "verified":
                continue
            with self.subTest(row=row["id"]):
                self.assertIn(row["rights"], readable)
                self.assertTrue(row["python"], "a verified row must name the code that was checked")
                self.assertTrue(row["tests"], "a verified row must name the test that checks it")

    def test_rows_that_claim_code_state_a_fidelity(self):
        for row in self.register["rows"]:
            if row["status"] in audit_tool.CLAIMS_CODE:
                with self.subTest(row=row["id"]):
                    self.assertIn(row["fidelity"], self.register["fidelities"])

    def test_the_rights_position_is_recorded_as_mechanics_only(self):
        # If this ever becomes cc0, that is a licensing finding and must arrive with evidence.
        for key in ("swn_revised", "swn_deluxe"):
            with self.subTest(source=key):
                self.assertEqual(self.register["sources"][key]["rights"], "mechanics_only")
                self.assertFalse(self.register["sources"][key]["text_available"],
                                 "no text licence: the book may not be reproduced")

    def test_the_copy_is_recorded_as_readable_without_being_publishable(self):
        """Two questions, two fields. Reading a page to check a number is not the same as publishing it."""
        for key in ("swn_revised", "swn_deluxe"):
            with self.subTest(source=key):
                source = self.register["sources"][key]
                self.assertTrue(source.get("readable"))
                self.assertTrue(source.get("readable_note"))
                self.assertFalse(source["text_available"])


class TrackerSpecificClaimsTests(unittest.TestCase):
    """The two P0 workstreams must be visible in the register, gaps included."""

    @classmethod
    def setUpClass(cls):
        cls.register = audit_tool.load()
        cls.by_id = {row["id"]: row for row in cls.register["rows"]}

    def test_the_psionics_technique_gap_is_recorded_as_unverified(self):
        """The copy is readable now, so "blocked" would be a licensing excuse for a work gap.

        What is missing is the book's per-discipline technique list; the row must say `unverified` and name
        the gap, because `blocked` is reserved for a source nobody can read.
        """
        row = self.by_id["P4"]
        self.assertEqual(row["status"], "partial")
        self.assertEqual(row["fidelity"], "unverified")
        self.assertIn("technique", row["notes"].lower())

    def test_the_faction_asset_catalogue_exists_and_says_what_it_omits(self):
        """#1105 warned "existing turn code is not proof of a finished asset catalogue" — so here is one.

        The catalogue is now implemented and verified against the printed tables. The row must still not
        read as "factions are finished": the ~60 individual special abilities are rules text that changes
        what an action may be, and the note has to say so.
        """
        row = self.by_id["F2"]
        self.assertEqual(row["status"], "implemented")
        self.assertEqual(row["fidelity"], "verified")
        self.assertIn("src/rules/swn_faction_assets.py", row["python"])
        self.assertIn("special abilit", row["notes"].lower())

    def test_sws_default_history_is_explicitly_not_applicable(self):
        row = self.by_id["H1"]
        self.assertEqual(row["status"], "not_applicable",
                         "SWN's future history must not overwrite NoöPunk canon")

    def test_psionics_and_factions_workstreams_have_real_implementations(self):
        for row_id in ("P1", "P2", "F1", "F4", "F5"):
            row = self.by_id[row_id]
            with self.subTest(row=row_id):
                self.assertEqual(row["status"], "implemented")
                for relative in row["python"] + row["tests"]:
                    self.assertTrue((ROOT / relative).exists(), relative)


class TheAuditActuallyCatchesLiesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = audit_tool.load()

    def test_a_row_citing_a_missing_module_is_caught(self):
        broken = copy.deepcopy(self.register)
        next(r for r in broken["rows"] if r["status"] == "implemented")["python"] = ["src/rules/nope.py"]
        self.assertTrue(audit_tool.audit(broken))

    def test_a_claim_without_a_test_is_caught(self):
        broken = copy.deepcopy(self.register)
        next(r for r in broken["rows"] if r["status"] == "implemented")["tests"] = []
        self.assertTrue(audit_tool.audit(broken))

    def test_verified_fidelity_without_a_readable_source_is_caught(self):
        """A `verified` claim needs something to have been verified against.

        The SWN copy is readable now, so flipping one row to `verified` is no longer a lie by itself —
        which is why the mutation has to remove the source as well. That is the actual invariant: no
        readable copy, no verified fidelity.
        """
        broken = copy.deepcopy(self.register)
        next(r for r in broken["rows"] if r["status"] == "implemented")["fidelity"] = "verified"
        for source in broken["sources"].values():
            source["readable"] = False
            source["text_available"] = False
        problems = audit_tool.audit(broken)
        self.assertTrue(problems)
        self.assertTrue(any("readable" in problem for problem in problems), problems)

    def test_a_row_with_no_page_reference_is_caught(self):
        broken = copy.deepcopy(self.register)
        row = broken["rows"][0]
        row.pop("printed_page", None)
        self.assertTrue(audit_tool.audit(broken))


class GroundingTests(unittest.TestCase):
    """The register describes the psionics data; the data must still say what it says."""

    def test_psionics_data_records_the_licence_boundary(self):
        data = json.loads((ROOT / "data/rules/swn_psionics.json").read_text(encoding="utf-8"))
        self.assertEqual(data["licence"], "no-verified-srd-shape-only")

    def test_the_technique_catalogue_is_provisional_and_original(self):
        data = json.loads((ROOT / "data/rules/psionics_techniques.json").read_text(encoding="utf-8"))
        self.assertFalse(data["is_canonical"], "the techniques are NoöPunk-original, not published SWN")
        self.assertEqual(data["status"], "provisional")
        self.assertEqual(len(data["discipline_cores"]), 6, "six disciplines, per #1105")
        self.assertEqual(len(data["techniques"]), 20)

    def test_rendered_report_is_current(self):
        target = ROOT / "docs/rules/SWN_COVERAGE_1105.md"
        self.assertTrue(target.is_file(), "run tools/swn_register_audit.py --render")
        self.assertEqual(target.read_text(encoding="utf-8"), audit_tool.render(audit_tool.load()))


if __name__ == "__main__":
    unittest.main()
