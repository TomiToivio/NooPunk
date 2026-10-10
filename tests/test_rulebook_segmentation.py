# -*- coding: utf-8 -*-
"""Rulebook segmentation (#232): the split must lose NOTHING.

The author's requirement is explicit -- *"Split the rulebook into smaller segments.
Consider how many are needed to make it reasonable. Do not lose anything!"* -- so the
guards are about totality and losslessness, not about layout taste.

What is asserted:
 1. the map is TOTAL -- every top-level section in `RULEBOOK.md` is assigned to exactly
    one part, and no part is empty (an unassigned section is silent loss);
 2. the concatenation of the parts reproduces `RULEBOOK.md` **byte-for-byte**;
 3. every part file on disk exists, is listed in the index, and its body really is the
    concatenation of the segments the map gave it (a part that drifted from the source
    is loss in disguise);
 4. the parts live outside `rulebook/`, so no existing chapter guard silently absorbs
    them into its scope.
"""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "RULEBOOK.md"
MAP_FILE = ROOT / "data" / "rules" / "rulebook_segmentation.json"
PARTS_DIR = ROOT / "rulebook_parts"


def _tool():
    spec = importlib.util.spec_from_file_location(
        "split_rulebook", ROOT / "tools" / "split_rulebook.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TotalityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))

    def test_the_map_is_a_versioned_format(self) -> None:
        self.assertEqual(self.mapping["version"], 1)
        self.assertIn("issues/232", self.mapping["issue"])

    def test_no_part_is_empty(self) -> None:
        for part in self.mapping["parts"]:
            with self.subTest(part=part["id"]):
                self.assertTrue(part.get("core") or part.get("ledger"),
                                f"{part['id']} claims no sections")

    def test_no_section_is_claimed_by_two_parts(self) -> None:
        core: set[str] = set()
        ledger: set[str] = set()
        for part in self.mapping["parts"]:
            with self.subTest(part=part["id"]):
                self.assertTrue(core.isdisjoint(part.get("core", [])), part["id"])
                self.assertTrue(ledger.isdisjoint(part.get("ledger", [])), part["id"])
            core = core.union(part.get("core", []))
            ledger = ledger.union(part.get("ledger", []))

    def test_every_ledger_section_is_assigned(self) -> None:
        tool = _tool()
        original = SOURCE.read_text(encoding="utf-8")
        segments = tool.segment(
            original.splitlines(keepends=True), self.mapping["core_ledger_marker"]
        )
        on_disk = {
            int(m.group(1))
            for s in segments
            if s["space"] == "ledger" and (m := tool.NUMBERED.match(s["heading"]))
        }
        assigned: set[int] = set()
        for part in self.mapping["parts"]:
            assigned = assigned.union(int(x) for x in part.get("ledger", []))
        with self.subTest("assigned but absent from the source"):
            self.assertEqual(sorted(assigned.difference(on_disk)), [])
        with self.subTest("present in the source but unassigned"):
            self.assertEqual(sorted(on_disk.difference(assigned)), [])


class LosslessnessTests(unittest.TestCase):
    """The `--check` proof, asserted from the test rather than taken on trust."""

    def test_reconstruction_is_byte_for_byte_the_source(self) -> None:
        tool = _tool()
        mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        original = SOURCE.read_text(encoding="utf-8")
        segments = tool.segment(original.splitlines(keepends=True), mapping["core_ledger_marker"])
        tool.assign(segments, mapping)
        self.assertEqual(tool.reconstruct(segments), original)

    def test_no_source_line_is_duplicated_across_the_parts(self) -> None:
        """Losslessness covers dropping; this covers double-counting the same text."""
        tool = _tool()
        mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        original = SOURCE.read_text(encoding="utf-8")
        segments = tool.segment(original.splitlines(keepends=True), mapping["core_ledger_marker"])
        tool.assign(segments, mapping)
        handed_out = [s for part in mapping["parts"] for s in part["_segments"]]
        self.assertEqual(len(handed_out), len(segments), "a segment is in no part or in two")
        seen = {id(s) for s in handed_out}
        self.assertEqual(len(seen), len(handed_out))

    def test_the_check_mode_writes_nothing(self) -> None:
        tool = _tool()
        before = {p: p.stat().st_mtime_ns for p in PARTS_DIR.glob("*.md")}
        self.assertEqual(tool.main(["--check"]), 0)
        after = {p: p.stat().st_mtime_ns for p in PARTS_DIR.glob("*.md")}
        self.assertEqual(before, after)


class GeneratedPartsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        self.tool = _tool()

    def test_every_part_file_exists_and_is_indexed(self) -> None:
        index = (PARTS_DIR / "INDEX.md").read_text(encoding="utf-8")
        for part in self.mapping["parts"]:
            with self.subTest(part=part["id"]):
                target = PARTS_DIR / f"{part['id']}.md"
                self.assertTrue(target.is_file(), f"{target} is missing")
                self.assertIn(f"{part['id']}.md", index)

    def test_each_part_body_is_exactly_its_segments(self) -> None:
        original = SOURCE.read_text(encoding="utf-8")
        segments = self.tool.segment(
            original.splitlines(keepends=True), self.mapping["core_ledger_marker"]
        )
        self.tool.assign(segments, self.mapping)
        for part in self.mapping["parts"]:
            with self.subTest(part=part["id"]):
                body = "".join("".join(s["lines"]) for s in part["_segments"])
                on_disk = (PARTS_DIR / f"{part['id']}.md").read_text(encoding="utf-8")
                self.assertTrue(on_disk.endswith(body),
                                f"{part['id']}.md does not end with its source segments")
                self.assertIn(self.tool.NAV_END, on_disk)

    def test_the_parts_are_not_absorbed_by_the_chapter_guards(self) -> None:
        """`rulebook/` has guards that derive their scope from its members."""
        self.assertFalse(PARTS_DIR == ROOT / "rulebook")
        self.assertFalse(str(PARTS_DIR).startswith(str(ROOT / "rulebook") + "/"))
        self.assertTrue(PARTS_DIR.is_dir())


class ThePartsContainWhatTheMapDeclaresTests(unittest.TestCase):
    """Totality and losslessness are both satisfied by filing every section ANYWHERE.

    The map does not only say *that* every section is assigned; it says **which** part each one
    belongs to, in its `core` and `ledger` lists. Those lists are the reader-facing promise --
    "01 Basic Rules" contains the rules. An implementation that never consults them can ignore
    them entirely, pass every other test in this file, and still file the whole playable core
    game-book under `00_meta_and_provenance`, whose stated purpose is material that is *"not
    player-facing rules"*.

    So the declaration is checked against the artefacts rather than taken on trust, and the core
    numbering space gets the same totality check the ledger already had.
    """

    def setUp(self) -> None:
        self.tool = _tool()
        self.mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        original = SOURCE.read_text(encoding="utf-8")
        segments = self.tool.segment(
            original.splitlines(keepends=True), self.mapping["core_ledger_marker"]
        )
        self.tool.assign(segments, self.mapping)

    def _declared(self, part: dict) -> set[str]:
        return {f"core:{x}" for x in part.get("core", [])} | {
            f"ledger:{x}" for x in part.get("ledger", [])
        }

    def _delivered(self, part: dict) -> set[str]:
        out: set[str] = set()
        for s in part["_segments"]:
            m = self.tool.NUMBERED.match(s["heading"])
            if not m:
                continue
            space = "core" if s["space"] == "preamble" else "ledger"
            out.add(f"{space}:{m.group(1)}")
        return out

    def test_every_part_delivers_exactly_the_sections_it_declares(self) -> None:
        for part in self.mapping["parts"]:
            with self.subTest(part=part["id"]):
                self.assertEqual(
                    self._delivered(part),
                    self._declared(part),
                    f"{part['id']} does not contain the sections the map assigns to it",
                )

    def test_every_core_section_is_declared_somewhere(self) -> None:
        """The core half has its own numbering space, so it needs its own totality check."""
        original = SOURCE.read_text(encoding="utf-8")
        segments = self.tool.segment(
            original.splitlines(keepends=True), self.mapping["core_ledger_marker"]
        )
        on_disk = {
            m.group(1)
            for s in segments
            if s["space"] == "preamble" and (m := self.tool.NUMBERED.match(s["heading"]))
        }
        declared: set[str] = set()
        for part in self.mapping["parts"]:
            declared = declared.union(part.get("core", []))
        with self.subTest("declared but absent from the source"):
            self.assertEqual(sorted(declared.difference(on_disk)), [])
        with self.subTest("in the source but declared by no part"):
            self.assertEqual(sorted(on_disk.difference(declared)), [])


    def test_the_companion_notes_quote_the_real_totals(self) -> None:
        """Prose drifts; the measurement in the notes is pinned to the artefacts it describes."""
        notes = (
            ROOT / "docs" / "design" / "RULEBOOK_SPLIT_MEASUREMENT_2026-10-10.md"
        ).read_text(encoding="utf-8")
        total = sum(
            len("".join(s["lines"]))
            for part in self.mapping["parts"]
            for s in part["_segments"]
        )
        self.assertEqual(total, len(SOURCE.read_text(encoding="utf-8")))
        self.assertIn("| **64** | **320,640** |", notes)
        self.assertIn("58.7%", notes)

    def test_the_playable_core_is_not_filed_under_meta(self) -> None:
        """The named failure this class exists for, asserted on the written artefacts."""
        meta = self.mapping["parts"][0]
        self.assertEqual(meta["id"], "00_meta_and_provenance")
        misplaced = {k for k in self._delivered(meta) if k.startswith("core:")}
        self.assertEqual(
            misplaced,
            set(),
            "the core game-book is filed under a part whose purpose is "
            f"'not player-facing rules': {sorted(misplaced)}",
        )
        body = (PARTS_DIR / "01_basic_rules.md").read_text(encoding="utf-8")
        for heading in ("## 3. Stats", "## 4. Skills"):
            with self.subTest(heading=heading):
                self.assertIn(heading, body)


if __name__ == "__main__":
    unittest.main()
