# -*- coding: utf-8 -*-
"""Protect the theory sections that a stale-branch clobber once deleted silently.

Commit ``901ba05`` ("Make Law of One authenticated...", a 65-line addition) deleted 703
lines from ``RULEBOOK.md`` — a stale-branch write that removed the four-layer ontology
(issue #78) and the theoretical bibliography. The loss was invisible to the number-keyed
guards, because a later commit reused ``## 34.`` for the glossary, so ``## 34.`` still
existed and the guards read the wrong section.

This guard pins the two sections by their **heading text**, and pins the *ordering*
relationship (they must follow the glossary, which owns ``## 34.``). A future renumber or
clobber that drops either section fails here with a clear message instead of silently
retargeting a number.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = "RULEBOOK.md"

#: Anchored by content, not by number — the number is reused across commits.
ONTOLOGY = "The four NoöPunk systems: Physical, Psychic, Social and Cybernetic"
BIBLIOGRAPHY = "Theoretical sources and inspirations"

#: Distinctive strings that must survive with each section.
ONTOLOGY_MARKERS = (
    "Luhmann's baseline",
    "Physical instead of Biological",
    "Cybernetic as a proposed fourth domain",
    "No separate Linguistic layer",
    "Structural coupling between the layers",
    "Candidate simulation representations",
)
BIBLIOGRAPHY_MARKERS = (
    "Niklas Luhmann",
    "Manuel Castells",
    "Donna Haraway",
    "Seth Lloyd",
    "Federico Faggin",
    "Alexander Wendt",
    "Interpretation rule",
)


def read() -> str:
    return (ROOT / RULEBOOK).read_text(encoding="utf-8")


def section(heading: str) -> str:
    """Body of the top-level ``##`` section whose heading text contains `heading`."""
    text = read()
    match = re.search(
        rf"(?ms)^##\s+\d+\.\s+[^\n]*{re.escape(heading)}[^\n]*\n(.*?)(?=^##\s+\d+\.|\Z)",
        text,
    )
    return match.group(1) if match else ""


class TheorySectionsSurviveTests(unittest.TestCase):
    def test_the_four_layer_ontology_section_exists(self) -> None:
        self.assertTrue(
            section(ONTOLOGY),
            f"RULEBOOK.md no longer contains the {ONTOLOGY!r} section; it was removed or "
            "renamed. If a rename is intended, update this guard deliberately.",
        )

    def test_the_theory_bibliography_section_exists(self) -> None:
        self.assertTrue(
            section(BIBLIOGRAPHY),
            f"RULEBOOK.md no longer contains the {BIBLIOGRAPHY!r} section; it was removed "
            "or renamed. If a rename is intended, update this guard deliberately.",
        )

    def test_the_ontology_keeps_its_distinctive_claims(self) -> None:
        body = section(ONTOLOGY)
        for marker in ONTOLOGY_MARKERS:
            with self.subTest(marker=marker):
                self.assertIn(marker, body)

    def test_the_bibliography_keeps_its_sources(self) -> None:
        body = section(BIBLIOGRAPHY)
        for marker in BIBLIOGRAPHY_MARKERS:
            with self.subTest(marker=marker):
                self.assertIn(marker, body)

    def test_the_glossary_still_owns_section_34(self) -> None:
        """The number was reused; a clobber must not silently overwrite the glossary."""
        self.assertIn("## 34. NoöPunk glossary", read())

    def test_no_internal_dangling_section_reference(self) -> None:
        """Every '§<n>.' a section cites must resolve to a real subsection heading."""
        text = read()
        headings = set(re.findall(r"(?m)^#{2,4}\s+(\d+(?:\.\d+)*)", text))
        for ref in sorted(set(re.findall(r"§\s*(\d+(?:\.\d+)*)", text))):
            # top-level-only refs like §33 are fine; require a subsection to exist for x.y
            if "." not in ref:
                continue
            with self.subTest(ref=ref):
                self.assertIn(
                    ref, headings,
                    f"§{ref} is cited but no heading defines it",
                )


if __name__ == "__main__":
    unittest.main()
