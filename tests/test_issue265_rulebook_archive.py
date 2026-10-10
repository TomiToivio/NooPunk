# -*- coding: utf-8 -*-
"""Issue #265 — the pre-narrative archive is complete, provable, and the new book starts clean.

The issue's acceptance criteria are that (a) the complete old content remains retrievable, (b)
nothing is silently discarded, and (c) there is one clear new authoritative entry point beginning
with the exact six attributes. These tests assert all three, plus that no legacy file was deleted.
"""
from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "archive" / "rulebook-pre-narrative-2026-10"
TAG = "rulebook-pre-narrative-2026-10"
START = ROOT / "rulebook" / "00_START_HERE.md"
MIGRATION = ARCHIVE / "MIGRATION_MAP.md"
MANIFEST = ARCHIVE / "manifest.json"

ATTRS = {"FIT": "Fitness", "REF": "Reflexes", "INT": "Intelligence",
         "SOC": "Social", "PSY": "Psyche", "CYB": "Cyber"}
DESTINATIONS = {"NEW-CORE", "DEFERRED", "LORE", "HISTORICAL", "REVIEW"}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def flat(p: Path) -> str:
    return " ".join(p.read_text(encoding="utf-8").split())


class ArchiveExistsTests(unittest.TestCase):
    def test_the_archive_exists_at_the_expected_path(self) -> None:
        self.assertTrue(ARCHIVE.is_dir(), "archive/rulebook-pre-narrative-2026-10 is missing")

    def test_it_has_a_readme_a_manifest_and_a_migration_map(self) -> None:
        for name in ("README.md", "MANIFEST.md", "MIGRATION_MAP.md", "manifest.json"):
            self.assertTrue((ARCHIVE / name).is_file(), f"{name} missing from the archive")

    def test_the_manifest_is_machine_readable_and_declares_nothing_deleted(self) -> None:
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(d["issue"], 265)
        self.assertEqual(d["tag"], TAG)
        self.assertIs(d["deleted_anything"], False)
        self.assertGreaterEqual(len(d["files"]), 30, "the inventory looks too small to be the corpus")

    def test_the_manifest_records_that_it_extends_rather_than_replaces_issue_243(self) -> None:
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(d["extends"]["issue"], 243)
        text = flat(ARCHIVE / "README.md").lower()
        self.assertIn("243", text)
        self.assertIn("does not duplicate or undo", text)


class RetrievabilityTests(unittest.TestCase):
    """Every recorded artefact must still exist, and hash to what was recorded."""

    def test_every_manifest_entry_still_exists_on_disk(self) -> None:
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
        missing = [f["source"] for f in d["files"] if not (ROOT / f["source"]).is_file()]
        self.assertEqual(missing, [], f"legacy files recorded in the manifest are gone: {missing}")

    def test_every_manifest_hash_still_matches(self) -> None:
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
        bad = [f["source"] for f in d["files"] if sha256(ROOT / f["source"]) != f["sha256"]]
        self.assertEqual(bad, [], f"content changed under the archive: {bad}")

    def test_the_root_rulebook_is_preserved_byte_for_byte(self) -> None:
        snap = ROOT / "rulebook" / "source_snapshots" / "root" / "RULEBOOK.md"
        self.assertTrue(snap.is_file())
        self.assertEqual(sha256(snap), sha256(ROOT / "RULEBOOK.md"),
                         "the #243 snapshot of the root RULEBOOK.md no longer matches the live file")

    def test_the_archive_regenerates_identically(self) -> None:
        import subprocess
        r = subprocess.run(["python3", str(ROOT / "tools" / "build_rulebook_archive.py"), "--check"],
                           cwd=str(ROOT), capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 0, f"archive out of date:\n{r.stdout}\n{r.stderr}")


class MigrationCompletenessTests(unittest.TestCase):
    """Nothing is silently discarded: every legacy unit has a recorded destination."""

    def setUp(self) -> None:
        self.map = MIGRATION.read_text(encoding="utf-8")

    def test_every_rulebook_section_heading_appears_in_the_map(self) -> None:
        headings = [ln[3:].strip() for ln in (ROOT / "RULEBOOK.md").read_text(encoding="utf-8").splitlines()
                    if ln.startswith("## ") and ln.strip() != "## Contents"]
        self.assertGreater(len(headings), 50, "expected the full section set")
        missing = [h for h in headings if h not in self.map]
        self.assertEqual(missing, [], f"legacy sections with no recorded destination: {missing}")

    def test_every_rulebook_chapter_appears_in_the_map(self) -> None:
        chapters = sorted(p.name for p in (ROOT / "rulebook").glob("[0-9]*.md")
                          if p.name != "00_START_HERE.md")
        self.assertGreater(len(chapters), 15)
        missing = [c for c in chapters if c not in self.map]
        self.assertEqual(missing, [], f"legacy chapters with no recorded destination: {missing}")

    def test_every_row_carries_a_known_destination_label(self) -> None:
        rows = re.findall(r"^\| .+? \| \*\*([A-Z-]+)\*\* \|", self.map, re.M)
        self.assertGreater(len(rows), 60, "expected a row per legacy unit")
        self.assertLessEqual(set(rows), DESTINATIONS, f"unknown destination label: {set(rows) - DESTINATIONS}")

    def test_old_numeric_rules_are_marked_historical_not_canonical(self) -> None:
        text = flat(MIGRATION).lower()
        self.assertIn("never quietly reinstated", text)
        self.assertIn("historical archive only", text)
        self.assertIn("nothing is silently discarded", text)

    def test_unsafe_destinations_are_left_for_the_author_not_guessed(self) -> None:
        text = flat(MIGRATION).lower()
        self.assertIn("needs author review", text)

    def test_no_legacy_corpus_was_deleted(self) -> None:
        for rel in ("RULEBOOK.md", "rulebook_parts", "rulebook/parts", "docs/rulebook_segments",
                    "docs/archive/RULEBOOK.md"):
            self.assertTrue((ROOT / rel).exists(), f"{rel} was deleted")


class NewRulebookStartTests(unittest.TestCase):
    """One clear authoritative entry point, opening with the exact six attributes."""

    def setUp(self) -> None:
        self.assertTrue(START.is_file(), "rulebook/00_START_HERE.md is missing")
        self.t = START.read_text(encoding="utf-8")

    def test_it_opens_with_the_exact_six_attributes(self) -> None:
        for code, name in ATTRS.items():
            self.assertIn(f"**{code}**", self.t, f"{code} missing")
            self.assertIn(f"| **{code}** | {name} |", self.t, f"{code} / {name} row missing from the table")

    def test_it_keeps_psyche_distinct_from_paranormal_psi(self) -> None:
        low = flat(START).lower()
        self.assertIn("not identical to psi", low)
        self.assertIn("psy and psi are different things", low)

    def test_it_declares_the_resolution_formula_undecided(self) -> None:
        low = flat(START).lower()
        self.assertIn("resolution formula is undecided", low)
        for engine in ("1d10", "4df", "fate", "pbta"):
            self.assertIn(engine, low)

    def test_it_retains_the_skill_catalogue_rather_than_pruning_it(self) -> None:
        low = flat(START).lower()
        self.assertIn("skills.json", low)
        self.assertIn("unchanged", low)

    def test_it_points_at_the_archive_and_the_tag(self) -> None:
        self.assertIn("archive/rulebook-pre-narrative-2026-10", self.t)
        self.assertIn(TAG, self.t)

    def test_the_readme_declares_the_new_entry_point_and_the_single_source_rule(self) -> None:
        r = flat(ROOT / "rulebook" / "README.md")
        self.assertIn("00_START_HERE.md", r)
        self.assertIn(TAG, r)
        self.assertIn("nothing has been deleted", r.lower())

    def test_it_does_not_present_a_legacy_engine_as_canon(self) -> None:
        low = flat(START).lower()
        self.assertIn("reference and history", low)
        self.assertNotIn("stat + skill + 1d10", low.replace("`", ""))


if __name__ == "__main__":
    unittest.main()
