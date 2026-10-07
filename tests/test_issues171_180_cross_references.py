# -*- coding: utf-8 -*-
"""Cross-file §-reference integrity for the reference chapters added by #171–#180.

Why this exists: the repo guards internal RULEBOOK references
(`test_theory_sections_survive`), and the #171–#180 guard checks that each new chapter
exists, is linked, and states its no-statistics bound. Neither checks that the
**modular chapters' own cross-references resolve**. Those chapters self-number
(`6_PSYCHIC.md` uses 6.x, `10_SINGULARITY_CRISIS.md` uses 9.x, `11_ONTOLOGY.md` uses 10.x,
…), so a reference like `§12.4` inside `13_EQUIPMENT.md` is a real pointer that can rot
silently: a heading gets renumbered during an edit and the reader is sent nowhere. The
whole set resolves today (verified), so this guard pins that state.

It asserts structure only — it does not constrain wording.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: the reference chapters the #171–#180 batch added or expanded
REFERENCE_CHAPTERS = (
    "rulebook/6_PSYCHIC.md",
    "rulebook/10_SINGULARITY_CRISIS.md",
    "rulebook/11_ONTOLOGY.md",
    "rulebook/12_BEINGS.md",
    "rulebook/13_EQUIPMENT.md",
    "rulebook/14_CHARACTER_GENERATION.md",
)

_SECTION_REF = re.compile(r"§\s*(\d+(?:\.\d+)*)")
_HEADING_NUM = re.compile(r"(?m)^#{1,6}\s+(\d+(?:\.\d+)*)")


def _universe() -> set[str]:
    """Every section number a reference may legitimately point at.

    The RULEBOOK's own headings, plus each modular chapter's self-numbered headings.
    """
    numbers = set(_HEADING_NUM.findall((ROOT / "RULEBOOK.md").read_text(encoding="utf-8")))
    for rel in REFERENCE_CHAPTERS:
        numbers |= set(_HEADING_NUM.findall((ROOT / rel).read_text(encoding="utf-8")))
    return numbers


class CrossReferenceIntegrityTests(unittest.TestCase):
    def test_every_reference_in_the_reference_chapters_resolves(self) -> None:
        """A dotted §-reference must point at a heading that exists somewhere."""
        universe = _universe()
        failures: list[str] = []
        for rel in REFERENCE_CHAPTERS:
            text = (ROOT / rel).read_text(encoding="utf-8")
            refs = sorted({r for r in _SECTION_REF.findall(text) if "." in r})
            for ref in refs:
                if ref not in universe:
                    failures.append(f"{rel}: §{ref} resolves to no heading")
        self.assertEqual(failures, [], "dangling cross-references:\n  " + "\n  ".join(failures))

    def test_the_chapters_self_number_consistently(self) -> None:
        """Each chapter must carry at least one self-numbered heading.

        A chapter that loses its numbering would silently invalidate every internal
        reference to it, so the numbering itself is pinned as a property.
        """
        for rel in REFERENCE_CHAPTERS:
            with self.subTest(chapter=rel):
                nums = _HEADING_NUM.findall((ROOT / rel).read_text(encoding="utf-8"))
                self.assertTrue(nums, f"{rel} has no self-numbered headings")

    def test_the_rulebook_links_the_reference_chapters(self) -> None:
        """A chapter the reader cannot reach from the rulebook is not canon-facing."""
        rb = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
        for rel in REFERENCE_CHAPTERS:
            with self.subTest(chapter=rel):
                self.assertIn(Path(rel).name, rb,
                              f"{Path(rel).name} is not linked from RULEBOOK.md")


if __name__ == "__main__":
    unittest.main()
