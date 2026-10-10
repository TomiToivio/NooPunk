# -*- coding: utf-8 -*-
"""Guard for the #200 direction record — and the licence-string property the ledger needs.

Division of labour with `test_issue200_rights_ledger.py` (which guards the ledger's own shape,
its decision vocabulary and its audit inventory): this file owns things that file does not —

1. **the direction record** — the triangle, the hybrid centre, the six STATs, the reserved
   areas, and the fact that this increment *records* a direction instead of migrating one;
2. **the no-LICENSE rule** — an agent must not relicense the repository;
3. **a licence-string property over the canonical ledger**: no entry carrying a reusable
   verdict may hold a licence that is NonCommercial or OGL.

(3) needs its own classifier, and its own test, because `"CC BY-NC-SA"` **contains** `"BY-SA"`.
A classifier that tests BY-SA first reads a NonCommercial licence as permissive and the whole
ledger becomes permission it does not have. `ClassifierTests` runs before the ledger is
trusted, for exactly that reason.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "sources" / "game_system_rights.json"
DIRECTION = ROOT / "docs" / "design" / "ISSUE_200_DIRECTION_2026-10-10.md"

#: Verdicts that mean "this expression may go into the CC release".
REUSABLE_DECISIONS = {"verified-permissive", "verified-public-domain"}

NONCOMMERCIAL = "noncommercial"
OPEN_GAME = "ogl"
PERMISSIVE_CC = "permissive-cc"
UNVERIFIED = "unverified"


def classify(license_text: str) -> str:
    """Reduce a licence string to the family that decides reuse.

    ORDER IS THE FACT: "CC BY-NC-SA" contains "BY-SA", so the NonCommercial test must run
    first. `ClassifierTests` pins that.
    """
    t = license_text.lower()
    if "noncommercial" in t or "nc" in re.split(r"[^a-z]+", t) or "by-nc" in t or re.search(r"\bnc\b", t):
        return NONCOMMERCIAL
    if "open game license" in t or re.search(r"\bogl\b", t):
        return OPEN_GAME
    if "cc0" in t or "public-domain" in t or "public domain" in t:
        return PERMISSIVE_CC
    if "by-sa" in t or "creative commons attribution" in t or re.search(r"\bcc by\b", t):
        return PERMISSIVE_CC
    return UNVERIFIED


def ledger() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


class ClassifierTests(unittest.TestCase):
    """The guard tests its own classifier before the ledger is trusted."""

    def test_noncommercial_is_not_read_as_shares_alike(self):
        self.assertEqual(classify("CC BY-NC-SA 4.0"), NONCOMMERCIAL)
        self.assertEqual(classify("CC BY-NC-SA 3.0 (author-stated)"), NONCOMMERCIAL)
        self.assertEqual(classify("CC BY-NC 4.0"), NONCOMMERCIAL)

    def test_open_game_content_is_not_creative_commons(self):
        self.assertEqual(
            classify("OGL 1.0a for designated Open Game Content (author-stated)"), OPEN_GAME)

    def test_compatible_licences_are_recognised(self):
        self.assertEqual(classify("CC0 (public-domain dedication)"), PERMISSIVE_CC)
        self.assertEqual(classify("CC BY 3.0 Unported"), PERMISSIVE_CC)
        self.assertEqual(classify("CC BY-SA 3.0 (author-stated)"), PERMISSIVE_CC)

    def test_an_ungranted_licence_is_not_permissive(self):
        self.assertEqual(classify("NO CC GRANT ESTABLISHED"), UNVERIFIED)
        self.assertEqual(classify("NOT ESTABLISHED from an authoritative source"), UNVERIFIED)


class LicenceStringPropertyTests(unittest.TestCase):
    """A reusable verdict and an incompatible licence must never coexist."""

    def setUp(self) -> None:
        self.entries = ledger()["sources"]

    def test_no_reusable_entry_holds_an_incompatible_licence(self):
        for entry in self.entries:
            if entry.get("decision") not in REUSABLE_DECISIONS:
                continue
            with self.subTest(entry=entry.get("id")):
                self.assertEqual(
                    classify(str(entry.get("license", ""))), PERMISSIVE_CC,
                    f"{entry.get('id')} is marked reusable with an incompatible licence",
                )

    def test_noncommercial_and_ogl_entries_are_never_reusable(self):
        for entry in self.entries:
            family = classify(str(entry.get("license", "")))
            if family in (NONCOMMERCIAL, OPEN_GAME):
                with self.subTest(entry=entry.get("id")):
                    self.assertNotIn(
                        entry.get("decision"), REUSABLE_DECISIONS,
                        f"{entry.get('id')} carries a {family} licence but a reusable verdict",
                    )

    def test_the_ledger_still_records_the_incompatible_sources(self):
        # If these vanished, the property above would pass vacuously.
        families = {classify(str(e.get("license", ""))) for e in self.entries}
        self.assertIn(NONCOMMERCIAL, families)
        self.assertIn(OPEN_GAME, families)


class LicenceDecisionIsTheAuthorsTests(unittest.TestCase):
    def test_no_license_file_was_added(self):
        for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
            with self.subTest(file=name):
                self.assertFalse(
                    (ROOT / name).exists(),
                    f"{name} exists: relicensing is a one-way legal act, not an agent's",
                )

    def test_the_release_target_is_still_recorded_as_open(self):
        # The decision must stay visible as the author's, whichever document carries it.
        target = ledger()["target_license"]
        self.assertRegex(json.dumps(target), r"(?i)author|open|approval")


class DirectionRecordTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = flat(DIRECTION)

    def test_the_record_exists_and_is_record_only(self):
        self.assertIn("RECORD ONLY", self.text)
        self.assertIn("does not migrate", self.text.lower())

    def test_it_names_all_three_corners_and_the_hybrid_centre(self):
        for corner in ("Simulationism", "Narrativism", "Gamism"):
            with self.subTest(corner=corner):
                self.assertIn(corner, self.text)
        for centre in ("Fudge", "Psi-Punk", "Fate", "Transhumanity's Fate"):
            with self.subTest(centre=centre):
                self.assertIn(centre, self.text)

    def test_it_keeps_the_six_stats_and_the_locked_core(self):
        for stat in ("FIT", "REF", "INT", "SOC", "CYB", "PSY"):
            with self.subTest(stat=stat):
                self.assertIn(stat, self.text)
        self.assertIn("is **not** superseded here", self.text)
        self.assertIn("approved migration", self.text)

    def test_it_records_that_attributes_and_skills_stay_distinct(self):
        self.assertRegex(self.text, r"Attributes and Skills stay \*\*distinct\*\*")

    def test_it_does_not_claim_the_engine_migrated(self):
        lowered = self.text.lower()
        for forbidden in ("the engine has migrated", "the core is superseded", "relicensed"):
            with self.subTest(phrase=forbidden):
                self.assertNotIn(forbidden, lowered)

    def test_it_points_at_the_canonical_ledger_rather_than_a_second_copy(self):
        self.assertIn("game_system_rights.json", self.text)
        self.assertFalse(
            (ROOT / "data" / "sources" / "rules_engine_rights.json").exists(),
            "a second rights ledger would fork the record",
        )


if __name__ == "__main__":
    unittest.main()
