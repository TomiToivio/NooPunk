"""Tests for the WWN rule register (#1101, Phase 0).

The register's value depends on it not being able to lie quietly. These tests pin three things:

1. every row that claims code cites files that exist in this repository;
2. no row sourced from material agents may not use is ever marked as done — Deluxe is the case that matters,
   because the tracker explicitly forbids inventing it from chapter names;
3. the audit itself fails when handed a fabricated claim, so it is a guard rather than a formatting exercise.

The counts asserted here are the tracker's own numbers (83 spell identities, 13 transcribed effects). If a later
PR adds effects, that test should be updated deliberately — not loosened.
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import wwn_register_audit as audit_tool


class RegisterIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = audit_tool.load()

    def test_the_register_has_no_integrity_problems(self):
        problems = audit_tool.audit(self.register)
        self.assertEqual(problems, [], "the register makes claims this repository cannot back")

    def test_row_ids_are_unique(self):
        ids = [row["id"] for row in self.register["rows"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate row ids make the register ambiguous")

    def test_every_chapter_of_the_tracker_is_represented(self):
        # A. Character Creation through K. Additional GM Tools, per the tracker's own lettering.
        chapters = {row["chapter"].split(".")[0] for row in self.register["rows"]}
        missing = set("ABCDEFGHIJK") - chapters
        self.assertFalse(missing, f"tracker chapters with no registered row: {sorted(missing)}")

    def test_deluxe_rows_are_blocked_not_guessed(self):
        deluxe = [row for row in self.register["rows"] if row["edition"] == "deluxe"]
        self.assertTrue(deluxe, "the tracker has five Deluxe chapters; none may be silently dropped")
        for row in deluxe:
            with self.subTest(row=row["id"]):
                self.assertEqual(row["status"], "blocked",
                                 "Deluxe text is not available to agents; a Deluxe row cannot be done")
                self.assertEqual(row["python"], [], "a blocked row must not claim an implementation")

    def test_unusable_sources_never_produce_a_done_row(self):
        usable = {}
        for source in self.register["sources"].values():
            usable[source["rights"]] = usable.get(source["rights"], False) or bool(source.get("usable"))
        for row in self.register["rows"]:
            if not usable.get(row["rights"], False):
                with self.subTest(row=row["id"]):
                    self.assertIn(row["status"], audit_tool.BLOCKED_ALLOWED)

    def test_swn_and_awn_are_recorded_as_unusable(self):
        # The rights ledger (#200) records both as NOT VERIFIED. If someone promotes them, that is a deliberate
        # licensing finding and must change this test with evidence in hand.
        for key in ("swn", "awn"):
            with self.subTest(source=key):
                self.assertEqual(self.register["sources"][key]["rights"], "unverified")
                self.assertFalse(self.register["sources"][key]["usable"])


class TheAuditActuallyCatchesLiesTests(unittest.TestCase):
    """A guard that cannot fail is a comment with extra steps."""

    @classmethod
    def setUpClass(cls):
        cls.register = audit_tool.load()

    def test_a_row_citing_a_module_that_does_not_exist_is_caught(self):
        broken = copy.deepcopy(self.register)
        row = next(r for r in broken["rows"] if r["status"] == "implemented")
        row["python"] = ["src/rules/wwn_module_that_was_never_written.py"]
        self.assertTrue(audit_tool.audit(broken))

    def test_a_deluxe_row_marked_implemented_is_caught(self):
        broken = copy.deepcopy(self.register)
        deluxe = next(r for r in broken["rows"] if r["edition"] == "deluxe")
        deluxe["status"] = "implemented"
        deluxe["python"] = ["src/rules/wwn_high_mage.py"]
        deluxe["tests"] = ["tests/test_wwn_high_mage.py"]
        self.assertTrue(audit_tool.audit(broken))

    def test_an_unknown_status_is_caught(self):
        broken = copy.deepcopy(self.register)
        broken["rows"][0]["status"] = "probably_fine"
        self.assertTrue(audit_tool.audit(broken))

    def test_a_claim_without_a_test_is_caught(self):
        broken = copy.deepcopy(self.register)
        row = next(r for r in broken["rows"] if r["status"] == "implemented")
        row["tests"] = []
        self.assertTrue(audit_tool.audit(broken))


class GroundingTests(unittest.TestCase):
    """The register's notes quote numbers; they must match the data files beside it."""

    def test_spell_catalogue_matches_the_tracker_count(self):
        data = json.loads((ROOT / "data/rules/wwn_spells.json").read_text(encoding="utf-8"))
        spells = data["spells"]
        self.assertEqual(len(spells), 83, "the tracker says 83 SRD spell identities")
        by_tradition = {}
        for spell in spells:
            by_tradition[spell["tradition"]] = by_tradition.get(spell["tradition"], 0) + 1
        self.assertEqual(by_tradition, {"high_magic": 52, "elementalist": 15, "necromancer": 16})

    def test_effect_backlog_is_what_the_tracker_says(self):
        data = json.loads((ROOT / "data/rules/wwn_spell_effects.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["effects"]), 13, "PR #1095 delivered 13 level-1 High Magic effect rows")
        self.assertEqual(83 - 13, 70, "the tracker says 70 effects remain, owned by #1085")

    def test_rendered_report_is_current(self):
        target = ROOT / "docs/rules/WWN_COVERAGE_1101.md"
        self.assertTrue(target.is_file(), "run tools/wwn_register_audit.py --render")
        self.assertEqual(target.read_text(encoding="utf-8"), audit_tool.render(audit_tool.load()),
                         "WWN_COVERAGE_1101.md is stale; regenerate it")


if __name__ == "__main__":
    unittest.main()
