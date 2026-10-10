"""Guard for the #232 rulebook split.

The split must satisfy three things at once, and this file pins all three:

1. **Nothing lost.** Every section body of `RULEBOOK.md` appears verbatim in exactly one part,
   and its SHA-256 still matches the digest frozen in
   `data/rules/rulebook_split_manifest.json` at split time.
2. **Drift-proof.** Editing `RULEBOOK.md` without regenerating the parts fails here, and editing
   a part by hand fails here. The two cannot quietly disagree.
3. **Shape preserved.** `RULEBOOK.md` keeps its `## 1.`-`## 9.` core run, its contiguous `## 1.`
   -`## N.` extended-canon run, and the `# Extended canon and reference material` marker the other
   guards split on -- because hundreds of `RULEBOOK.md §N` cross-references resolve against them.

The point of 1 and 2 together is that this is the ONLY thing standing between a large mechanical
restructure and silent content loss, so it is deliberately strict about bytes rather than prose.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import split_rulebook_twelve as sr

MANIFEST = ROOT / "data" / "rules" / "rulebook_split_manifest.json"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


class NothingLostTests(unittest.TestCase):
    """The promise Tomi made explicit: 'Do not lose anything!'"""

    def test_the_manifest_exists_and_covers_every_section(self) -> None:
        data = manifest()
        self.assertEqual(data["source"], "RULEBOOK.md")
        self.assertEqual(data["section_count"], 63)
        counted = sum(len(part["sections"]) for part in data["parts"].values())
        self.assertEqual(counted, data["section_count"])

    def test_every_part_section_still_hashes_to_its_frozen_digest(self) -> None:
        """The core guarantee: a body edited in a part is caught byte-for-byte."""
        failures = []
        for part in manifest()["parts"].values():
            blocks = sr.blocks_by_heading(read(part["file"]))
            for section in part["sections"]:
                heading = section["heading"]
                if heading not in blocks:
                    failures.append(f"{part['file']}: {heading!r} missing")
                    continue
                digest = hashlib.sha256(blocks[heading].encode("utf-8")).hexdigest()
                if digest != section["body_sha256"]:
                    failures.append(f"{part['file']}: {heading!r} content changed")
        self.assertFalse(failures, failures)

    def test_the_manifest_tracks_the_current_rulebook(self) -> None:
        """Editing RULEBOOK.md without regenerating must fail, so the parts cannot go stale."""
        live = hashlib.sha256(read("RULEBOOK.md").encode("utf-8")).hexdigest()
        self.assertEqual(
            live, manifest()["source_sha256"],
            "RULEBOOK.md changed without regenerating the split: run "
            "`python3 tools/split_rulebook.py --apply` in the same commit.",
        )

    def test_no_section_body_appears_in_two_parts(self) -> None:
        """Duplication is the other way a 'split' quietly goes wrong."""
        seen: dict[str, str] = {}
        for part in manifest()["parts"].values():
            for section in part["sections"]:
                key = f"{section['kind']}:{section['number']}"
                self.assertNotIn(key, seen,
                                 f"{key} is in both {seen.get(key)} and {part['file']}")
                seen[key] = part["file"]

    def test_the_partition_is_total(self) -> None:
        """Every numbered section of the source lands somewhere; none is orphaned."""
        assigned = {(s["kind"], s["number"])
                    for part in manifest()["parts"].values() for s in part["sections"]}
        present = {(s["kind"], s["number"]) for s in sr.parse(read("RULEBOOK.md"))["sections"]
                   if s["number"] is not None}
        self.assertEqual(assigned, present,
                         f"orphaned: {sorted(present - assigned)}; phantom: {sorted(assigned - present)}")


class ShapePreservedTests(unittest.TestCase):
    """RULEBOOK.md's shape is load-bearing for other guards and for cross-references."""

    def test_the_appendix_marker_survives(self) -> None:
        self.assertIn("# Extended canon and reference material", read("RULEBOOK.md"))

    def test_the_core_run_is_still_one_to_nine(self) -> None:
        text = read("RULEBOOK.md")
        core = text.split("# Extended canon and reference material", 1)[0]
        numbers = [int(n) for n in re.findall(r"(?m)^##\s+(\d+)\.", core)]
        self.assertEqual(numbers, list(range(1, 10)))

    def test_the_extended_canon_run_is_still_contiguous(self) -> None:
        text = read("RULEBOOK.md")
        appendix = text.split("# Extended canon and reference material", 1)[1]
        numbers = [int(n) for n in re.findall(r"(?m)^##\s+(\d+)\.", appendix)]
        self.assertEqual(numbers, list(range(1, max(numbers) + 1)))

    def test_the_navigation_block_is_present_exactly_once(self) -> None:
        text = read("RULEBOOK.md")
        marker = "This rulebook is also published as navigable parts."
        self.assertEqual(text.count(marker), 1)
        self.assertIn("rulebook/00_INDEX.md", text)

    def test_no_body_was_left_behind_in_the_index_form(self) -> None:
        """Sanity: the split is by section, so the rulebook still holds its own prose."""
        self.assertGreater(len(read("RULEBOOK.md").splitlines()), 5000)


class IndexTests(unittest.TestCase):
    def test_the_index_links_every_part(self) -> None:
        index = read("rulebook/00_INDEX.md")
        for stem, part in manifest()["parts"].items():
            with self.subTest(part=stem):
                self.assertIn(f"parts/{stem}.md", index)
                self.assertIn(part["title"], index)

    def test_every_part_file_links_back_to_the_canonical_rulebook(self) -> None:
        for stem, part in manifest()["parts"].items():
            with self.subTest(part=stem):
                self.assertIn("RULEBOOK.md", read(part["file"]))

    def test_the_index_carries_every_section_heading(self) -> None:
        index = read("rulebook/00_INDEX.md")
        for section in sr.parse(read("RULEBOOK.md"))["sections"]:
            if section["number"] is None:
                continue
            with self.subTest(section=section["heading"]):
                self.assertIn(section["heading"], index)


class ToolTests(unittest.TestCase):
    def test_the_navigation_insertion_is_idempotent(self) -> None:
        text = read("RULEBOOK.md")
        again, changed = sr.ensure_navigation(text)
        self.assertFalse(changed, "running the splitter twice must not duplicate the block")
        self.assertEqual(again, text)

    def test_the_partition_map_is_a_partition(self) -> None:
        sr.validate_partition(sr.parse(read("RULEBOOK.md")))

    def test_the_parts_are_not_globbed_as_reference_chapters(self) -> None:
        """`rulebook/*.md` is globbed by another guard; parts live one level down on purpose.

        That guard requires every globbed chapter to self-number and to be linked from
        RULEBOOK.md. Putting twelve generated parts in the glob would impose both on all of
        them for no benefit -- the index is the entry point.
        """
        self.assertTrue((ROOT / "rulebook" / "parts").is_dir())
        globbed = {p.name for p in (ROOT / "rulebook").glob("*.md")}
        part_names = {p.name for p in (ROOT / "rulebook" / "parts").glob("*.md")}
        self.assertEqual(part_names & globbed, set(),
                         "a part is inside the rulebook/*.md glob and would face that guard")


if __name__ == "__main__":
    unittest.main()
