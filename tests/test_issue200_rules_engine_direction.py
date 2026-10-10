# -*- coding: utf-8 -*-
"""Guard for the #200 rules-engine direction: the rights ledger and the direction record.

Issue #200 changes the licensing premise of the project, and its central constraint is
mechanical enough to test:

    **an entry may be marked importable-cc only when its license is compatible with a
    commercially reusable Creative Commons release.**

A NonCommercial source cannot enter such a release, and Open Game Content cannot be
relabelled Creative Commons. That rule is what this file enforces, because it is exactly the
kind of constraint that a later tidy-up would quietly relax -- a reordered classifier that
reads "CC BY-NC-SA 4.0" as "BY-SA" would turn the whole ledger into permission it does not
have. Hence `ClassifierTests` below: the guard tests its own classifier before trusting it.

It also pins the *record-only* nature of this increment: no LICENSE file, no migration claim.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "sources" / "rules_engine_rights.json"
DIRECTION = ROOT / "docs" / "design" / "ISSUE_200_DIRECTION_2026-10-10.md"
AUDIT = ROOT / "docs" / "sources" / "RULES_ENGINE_LICENSES.md"

REQUIRED_ENTRY_FIELDS = (
    "key", "name", "publisher", "role_in_noopunk", "license", "license_checked",
    "verified", "decision", "commercial_ok", "sharealike_ok", "imported_expression",
)

#: Sources #200 names that must each have an entry. A missing one is a silent gap.
REQUIRED_KEYS = (
    "fate_core_srd", "the_veil", "cwn_srd", "swn_srd", "fudge_srd", "fudge_1995_core",
    "psi_punk_srd", "eclipse_phase_2e", "transhumanitys_fate", "apocalypse_world",
    "closed_systems",
)

#: Licenses that can never enter a commercially reusable CC BY/BY-SA release.
NONCOMMERCIAL = "noncommercial"
OPEN_GAME = "ogl"
PERMISSIVE_CC = "permissive-cc"
UNVERIFIED = "unverified"


def classify(license_text: str) -> str:
    """Reduce a license string to the family that decides reuse.

    ORDER IS THE FACT: "CC BY-NC-SA" contains "BY-SA", so the NonCommercial test has to run
    first. `ClassifierTests` pins that, because getting it backwards would silently license
    NonCommercial material into the rulebook.
    """
    t = license_text.lower()
    if "nc" in t.replace("nc-", "nc ").split() or "by-nc" in t or "noncommercial" in t:
        return NONCOMMERCIAL
    if "open game license" in t or "ogl" in t:
        return OPEN_GAME
    if "cc0" in t or "public-domain" in t or "creative commons 0" in t:
        return PERMISSIVE_CC
    if "by-sa" in t or "by" in t.split() or "creative commons attribution" in t:
        return PERMISSIVE_CC
    return UNVERIFIED


def load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


class ClassifierTests(unittest.TestCase):
    """The guard tests its own classifier before the ledger is trusted."""

    def test_noncommercial_is_not_read_as_shares_alike(self):
        self.assertEqual(classify("CC BY-NC-SA 4.0"), NONCOMMERCIAL)
        self.assertEqual(classify("CC BY-NC-SA 3.0"), NONCOMMERCIAL)
        self.assertEqual(classify("CC BY-NC 4.0"), NONCOMMERCIAL)

    def test_open_game_content_is_not_creative_commons(self):
        self.assertEqual(classify("Open Game License 1.0a (designated Open Game Content)"), OPEN_GAME)

    def test_compatible_licenses_are_recognised(self):
        self.assertEqual(classify("CC0 1.0 Universal (public-domain waiver)"), PERMISSIVE_CC)
        self.assertEqual(classify("CC BY 3.0 (Unported)"), PERMISSIVE_CC)
        self.assertEqual(classify("CC BY-SA 3.0 (Unported)"), PERMISSIVE_CC)

    def test_an_unknown_license_is_not_permissive(self):
        self.assertEqual(classify("no Creative Commons grant; 'all rights reserved'"), UNVERIFIED)


class LedgerShapeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load()
        self.entries = {e["key"]: e for e in self.data["sources"]}

    def test_the_ledger_parses_and_is_the_expected_format(self):
        self.assertEqual(self.data["format"], "noopunk.sources.rules_engine_rights")
        self.assertIn("issues/200", self.data["issue"])

    def test_every_named_source_has_an_entry(self):
        missing = [k for k in REQUIRED_KEYS if k not in self.entries]
        self.assertEqual(missing, [], f"ledger is missing entries: {missing}")

    def test_every_entry_carries_the_required_fields(self):
        for key, entry in self.entries.items():
            with self.subTest(entry=key):
                for field in REQUIRED_ENTRY_FIELDS:
                    self.assertIn(field, entry, f"{key} lacks {field}")

    def test_nothing_has_been_imported(self):
        for key, entry in self.entries.items():
            with self.subTest(entry=key):
                self.assertIs(entry["imported_expression"], False)

    def test_a_date_was_recorded_for_every_check(self):
        for key, entry in self.entries.items():
            with self.subTest(entry=key):
                self.assertRegex(str(entry["license_checked"]), r"^\d{4}-\d{2}-\d{2}$")


class LicensingInvariantTests(unittest.TestCase):
    """The rule the issue exists to enforce."""

    def setUp(self) -> None:
        self.data = load()
        self.entries = {e["key"]: e for e in self.data["sources"]}
        self.vocabulary = set(self.data["decision_vocabulary"])

    def test_decisions_come_from_the_declared_vocabulary(self):
        for key, entry in self.entries.items():
            with self.subTest(entry=key):
                self.assertIn(entry["decision"], self.vocabulary)

    def test_importable_cc_entries_are_really_compatible(self):
        for key, entry in self.entries.items():
            if entry["decision"] != "importable-cc":
                continue
            with self.subTest(entry=key):
                self.assertEqual(
                    classify(entry["license"]), PERMISSIVE_CC,
                    f"{key} is marked importable-cc but its license is not compatible",
                )
                self.assertIs(entry["commercial_ok"], True, f"{key} is not commercial-safe")

    def test_noncommercial_and_ogl_sources_are_never_importable(self):
        for key, entry in self.entries.items():
            family = classify(entry["license"])
            if family in (NONCOMMERCIAL, OPEN_GAME):
                with self.subTest(entry=key):
                    self.assertNotEqual(
                        entry["decision"], "importable-cc",
                        f"{key} has a {family} license and cannot be importable-cc",
                    )

    def test_unverified_sources_are_not_importable(self):
        for key, entry in self.entries.items():
            if "NOT VERIFIED" in str(entry["verified"]) or "not verified" in str(entry["license"]).lower():
                with self.subTest(entry=key):
                    self.assertNotEqual(entry["decision"], "importable-cc", f"{key} is unverified")

    def test_the_two_noncommercial_posthuman_sources_are_principles_only(self):
        for key in ("eclipse_phase_2e", "transhumanitys_fate"):
            with self.subTest(entry=key):
                self.assertEqual(self.entries[key]["decision"], "principles-only")
                self.assertIs(self.entries[key]["commercial_ok"], False)

    def test_the_ogl_sources_are_principles_only(self):
        for key in ("fudge_srd", "psi_punk_srd"):
            with self.subTest(entry=key):
                self.assertEqual(self.entries[key]["decision"], "principles-only")

    def test_apocalypse_world_is_principles_only_not_a_grant(self):
        entry = self.entries["apocalypse_world"]
        self.assertEqual(entry["decision"], "principles-only")
        self.assertIn("no Creative Commons grant", entry["license"])

    def test_the_target_license_names_both_pathways(self):
        target = self.data["target_license"]
        self.assertEqual(target["recommended"], "CC BY-SA 4.0")
        self.assertEqual(target["alternative"], "CC BY 4.0")
        # and it must be a recommendation, not an applied relicence
        self.assertIn("NOT APPLIED", target["status"])

    def test_the_compatibility_rule_keeps_nc_and_ogl_rejected(self):
        rule = self.data["compatibility_rule"]
        for rejected in ("CC BY-NC-SA (any version)", "OGL 1.0a", "no license found", "unverified"):
            with self.subTest(rejected=rejected):
                self.assertIn(rejected, rule["rejected"])


class RecordOnlyTests(unittest.TestCase):
    """This increment records a direction; it does not migrate anything."""

    def test_no_license_file_was_added(self):
        for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
            with self.subTest(file=name):
                self.assertFalse((ROOT / name).exists(), f"{name} exists: relicensing is not an agent act")

    def test_the_direction_record_exists_and_is_self_limiting(self):
        text = " ".join(DIRECTION.read_text(encoding="utf-8").split())
        self.assertIn("RECORD ONLY", text)
        self.assertIn("does not migrate", text.lower())

    def test_the_record_names_all_three_corners_and_the_six_stats(self):
        text = " ".join(DIRECTION.read_text(encoding="utf-8").split())
        for corner in ("Simulationism", "Narrativism", "Gamism"):
            with self.subTest(corner=corner):
                self.assertIn(corner, text)
        for stat in ("FIT", "REF", "INT", "SOC", "CYB", "PSY"):
            with self.subTest(stat=stat):
                self.assertIn(stat, text)

    def test_the_record_keeps_the_core_locked(self):
        text = " ".join(DIRECTION.read_text(encoding="utf-8").split())
        self.assertIn("is **not** superseded here", text)

    def test_the_record_carries_the_two_guard_conflicts_forward(self):
        # These are the migrations that need an author ruling; forgetting them is the failure.
        text = " ".join(DIRECTION.read_text(encoding="utf-8").split())
        self.assertIn("test_design_principles.py", text)
        self.assertIn("FORBIDDEN_CHASSIS", text)

    def test_the_audit_document_exists_and_states_the_rule(self):
        text = " ".join(AUDIT.read_text(encoding="utf-8").split())
        self.assertRegex(text, r"NonCommercial term cannot enter")
        self.assertIn("cannot be relabelled", text)


if __name__ == "__main__":
    unittest.main()
