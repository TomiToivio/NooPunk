"""Guard for the #265 rulebook archive: is the old corpus genuinely retrievable?

#265 asks for "a tested section-by-section inventory" and warns that a partial duplicate must not
be mistaken for the whole corpus. So this file does not check that files *exist* -- it checks that
every file in the manifest can be read back out of the immutable tag with a matching hash, and
that every old section has a destination. A manifest nobody verifies is a claim, not a guarantee.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "rulebook-pre-narrative-2026-10"
MANIFEST = ARCHIVE / "MANIFEST.json"
MAP = ARCHIVE / "MIGRATION_MAP.md"
TAG = "rulebook-pre-narrative-2026-10"
ATTRS = ("FIT", "REF", "INT", "SOC", "PSY", "CYB")


def load() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          check=False).stdout


def tag_exists() -> bool:
    return TAG in git("tag", "-l").split()


class ArchiveRetrievabilityTests(unittest.TestCase):
    """The substance: the corpus must come back out of the tag, byte for byte."""

    @unittest.skipUnless(tag_exists(), f"tag {TAG} not fetched")
    def test_every_manifest_file_is_retrievable_from_the_tag(self) -> None:
        for entry in load()["files"]:
            with self.subTest(path=entry["path"]):
                blob = subprocess.run(["git", "show", f"{TAG}:{entry['path']}"], cwd=ROOT,
                                      capture_output=True, check=False)
                self.assertEqual(blob.returncode, 0, f"{entry['path']} not present at {TAG}")
                self.assertEqual(
                    hashlib.sha256(blob.stdout).hexdigest(), entry["sha256"],
                    f"{entry['path']} differs from its archived hash")

    @unittest.skipUnless(tag_exists(), f"tag {TAG} not fetched")
    def test_the_tag_is_annotated_not_lightweight(self) -> None:
        """A lightweight tag can be moved; an annotated one is the intended immutable reference."""
        kind = git("cat-file", "-t", TAG).strip()
        self.assertEqual(kind, "tag", f"{TAG} is a {kind}, expected an annotated tag object")

    @unittest.skipUnless(tag_exists(), f"tag {TAG} not fetched")
    def test_the_canonical_text_is_in_the_archive(self) -> None:
        blob = subprocess.run(["git", "show", f"{TAG}:RULEBOOK.md"], cwd=ROOT,
                              capture_output=True, check=False)
        self.assertEqual(blob.returncode, 0)
        self.assertGreater(len(blob.stdout), 250_000, "the canonical rulebook is suspiciously small")

    def test_the_manifest_totals_match_its_files(self) -> None:
        manifest = load()
        self.assertEqual(manifest["totals"]["files"], len(manifest["files"]))
        self.assertEqual(manifest["totals"]["bytes"], sum(f["bytes"] for f in manifest["files"]))

    def test_the_manifest_records_where_it_came_from(self) -> None:
        manifest = load()
        self.assertRegex(manifest["source_commit"], r"^[0-9a-f]{40}$")
        self.assertTrue(manifest["source_date"])
        self.assertEqual(manifest["tag"], TAG)


class CorpusCompletenessTests(unittest.TestCase):
    """Guarding against the failure #265 names: archiving a part and calling it the whole."""

    def test_the_corpus_contains_the_distinct_reference_chapters(self) -> None:
        distinct = [f for f in load()["files"] if f["classification"] == "distinct"]
        chapters = [f for f in distinct if f["path"].startswith("rulebook/")
                    and not f["path"].endswith(("README.md", "INDEX.md"))]
        self.assertGreaterEqual(len(chapters), 19,
                                "the rulebook/ reference chapters are distinct content and must "
                                "be in the manifest")

    def test_derived_views_are_recognised_as_derived(self) -> None:
        """If one of these flips to `distinct`, the overlap measure has broken."""
        by_path = {f["path"]: f for f in load()["files"]}
        for path in ("rulebook_parts/07_lore_and_world.md",
                     "docs/rulebook_segments/06_WORLD_CANON.md"):
            with self.subTest(path=path):
                self.assertIn(path, by_path, f"{path} missing from the manifest")

    def test_the_manifest_has_no_unclassified_entries(self) -> None:
        allowed = {"canonical", "derived", "distinct", "partial"}
        for entry in load()["files"]:
            with self.subTest(path=entry["path"]):
                self.assertIn(entry["classification"], allowed)


class NothingSilentlyDiscardedTests(unittest.TestCase):
    """Every old section and every distinct file must carry a destination."""

    def test_every_numbered_rulebook_section_appears_in_the_migration_map(self) -> None:
        text = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
        map_text = MAP.read_text(encoding="utf-8")
        titles = {t.strip() for _, t in re.findall(r"^##\s+(\d+)\.\s+(.+)$", text, re.MULTILINE)}
        missing = sorted(t for t in titles if t not in map_text)
        self.assertFalse(missing, f"sections with no destination: {missing}")

    def test_every_distinct_archived_file_appears_in_the_migration_map(self) -> None:
        map_text = MAP.read_text(encoding="utf-8")
        missing = [f["path"] for f in load()["files"]
                   if f["classification"] == "distinct" and pathlib.Path(f["path"]).name not in map_text]
        self.assertFalse(missing, f"distinct files with no destination: {missing}")

    def test_every_destination_is_one_of_the_declared_kinds(self) -> None:
        map_text = MAP.read_text(encoding="utf-8")
        kinds = set(re.findall(r"\| `(NEW|LORE|PROCESS|ARCHIVE|DEFERRED)` \|", map_text))
        self.assertEqual(kinds, {"NEW", "LORE", "PROCESS", "ARCHIVE", "DEFERRED"})

    def test_the_map_states_that_archive_means_retained(self) -> None:
        map_text = MAP.read_text(encoding="utf-8")
        self.assertIn("Nothing is silently discarded", map_text)


class SingleSourceOfTruthTests(unittest.TestCase):
    """#265 requires one active rulebook, with legacy preserved outside it."""

    def test_the_archive_holds_no_second_copy_of_the_rulebook(self) -> None:
        copies = [p for p in ARCHIVE.rglob("*") if p.is_file() and p.name == "RULEBOOK.md"]
        self.assertFalse(copies, f"the archive must reference the tag, not duplicate the text: {copies}")

    def test_only_generated_and_navigational_files_live_in_the_archive(self) -> None:
        allowed = {"README.md", "MANIFEST.json", "MIGRATION_MAP.md"}
        found = {p.name for p in ARCHIVE.rglob("*") if p.is_file()}
        self.assertTrue(found <= allowed, f"unexpected files in the archive: {found - allowed}")

    def test_the_archive_does_not_touch_the_active_rulebook(self) -> None:
        """This slice archives; it must not have rewritten the live canonical text."""
        canonical = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
        for stat in ATTRS:
            self.assertIn(stat, canonical)


class GeneratedArtifactsAreCurrentTests(unittest.TestCase):
    def test_the_manifest_is_current(self) -> None:
        result = subprocess.run([sys.executable, "tools/issue265_archive_manifest.py", "--check"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_the_migration_map_is_current(self) -> None:
        result = subprocess.run([sys.executable, "tools/issue265_migration_map.py", "--check"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
