"""Guard: `RULEBOOK.md` has TWO numbering runs, and the segmentation map must know it.

Independent of `tests/test_issue232_lossless_segments.py` and `tests/test_rulebook_split_map.py`,
which cover assembly and map shape. This file covers the thing neither does: **the source contains
two independent `## N.` runs**, so a bare section number is ambiguous, and the authored map must
disambiguate core from extended canon or the split silently mis-assigns sections.

Found while attempting this split by cutting bodies out of `RULEBOOK.md` (which failed 309 tests --
see `docs/design/RULEBOOK_STRUCTURE.md`). Reported rather than reconciled, because choosing a
canonical run and renumbering the other is an author decision under #232.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_FILE = ROOT / "data" / "rules" / "rulebook_segmentation.json"
MARKER = "# Extended canon and reference material"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def runs() -> tuple[list[int], list[int]]:
    """(core numbers, extended-canon numbers) as they literally appear in the source."""
    text = read("RULEBOOK.md")
    core, ledger = text.split(MARKER, 1)
    grab = lambda half: [int(n) for n in re.findall(r"(?m)^##\s+(\d+)\.", half)]
    return grab(core), grab(ledger)


class TwoNumberingRunsTests(unittest.TestCase):
    """The structural fact, pinned so it cannot be forgotten or silently 'tidied'."""

    def test_the_source_has_two_independent_runs(self) -> None:
        core, ledger = runs()
        self.assertEqual(core, list(range(1, 10)), "the core run drifted")
        self.assertEqual(ledger, list(range(1, 55)), "the extended-canon run drifted")
        self.assertEqual((len(core), len(ledger)), (9, 54))

    def test_the_marker_separates_them(self) -> None:
        self.assertIn(MARKER, read("RULEBOOK.md"))

    def test_a_bare_section_number_is_genuinely_ambiguous(self) -> None:
        """The finding: `§5` names two different sections. Every consumer must disambiguate."""
        text = read("RULEBOOK.md")
        core, ledger = text.split(MARKER, 1)
        core_five = re.search(r"(?m)^##\s+5\.\s*(.+)$", core)
        ledger_five = re.search(r"(?m)^##\s+5\.\s*(.+)$", ledger)
        assert core_five is not None and ledger_five is not None  # narrowing for type checkers
        self.assertNotEqual(core_five.group(1).strip(), ledger_five.group(1).strip(),
                            "§5 now names the same section twice; the ambiguity was reconciled "
                            "and docs/design/RULEBOOK_STRUCTURE.md must be updated to say so")

    def test_every_run_has_a_collision_not_just_the_first(self) -> None:
        """All of 1-9 collide, which is why the whole run needs a namespace and not one label."""
        core, ledger = runs()
        colliding = sorted(set(core) & set(ledger))
        self.assertEqual(colliding, list(range(1, 10)))


class MapDisambiguatesTheRunsTests(unittest.TestCase):
    """Verification of the authored map, not a restatement of the lossless-assembly guard."""

    def setUp(self) -> None:
        self.map = json.loads(MAP_FILE.read_text(encoding="utf-8"))

    def test_the_map_declares_both_numbering_spaces(self) -> None:
        keys = {k for part in self.map["parts"] for k in part if k in {"core", "ledger"}}
        self.assertEqual(keys, {"core", "ledger"},
                         "the map must key on both spaces; a single section list would collide")

    def test_the_map_covers_the_core_run_exactly_once(self) -> None:
        covered: list[int] = []
        for part in self.map["parts"]:
            covered += [int(n) for n in part.get("core", [])]
        self.assertEqual(sorted(covered), sorted(set(covered)), f"duplicated: {covered}")
        self.assertEqual(sorted(int(n) for n in covered), list(range(1, 10)))

    def test_the_map_covers_the_extended_canon_run_exactly_once(self) -> None:
        covered: list[int] = []
        for part in self.map["parts"]:
            covered += [int(n) for n in part.get("ledger", [])]
        self.assertEqual(sorted(covered), sorted(set(covered)), f"duplicated: {covered}")
        self.assertEqual(sorted(int(n) for n in covered), list(range(1, 55)))

    def test_the_maps_numbers_match_the_source(self) -> None:
        """If the source is renumbered, this fails rather than the map going quietly wrong."""
        core, ledger = runs()
        in_map_core = sorted(int(n) for p in self.map["parts"] for n in p.get("core", []))
        in_map_ledger = sorted(int(n) for p in self.map["parts"] for n in p.get("ledger", []))
        self.assertEqual(in_map_core, core)
        self.assertEqual(in_map_ledger, ledger)


if __name__ == "__main__":
    unittest.main()
