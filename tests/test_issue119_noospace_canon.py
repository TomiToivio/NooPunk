"""Regression guard for issue #119: canonical Noöspace ontology.

This file previously defined module-level ``test_*`` functions rather than ``TestCase``
classes, so ``python -m unittest discover -s tests -p "test_*.py"`` matched the filename but
found nothing to run: the CI step reported "Ran 0 tests ... OK" and the whole Noöspace canon
was unguarded in CI. Verified by deleting every occurrence of the term from ``RULEBOOK.md``
and observing zero failures across the suite. It also had no ``__main__`` block, so running
it directly did nothing and exited 0.

The repository already documents this exact trap for ``test_world_ideology.py`` in
``.github/workflows/python-scaffold.yml`` and gives that file its own runner step. Rather
than add a second bespoke step, this guard is now a ``unittest.TestCase`` so the existing
discovery run collects it -- and the assertions become individually reported subtests.

Only the standard library is used: CI installs ``requirements.txt`` and nothing else, so no
dependency beyond ``unittest`` is safe here.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"

#: Phrases the issue makes canonical. Each is asserted as its own subtest.
REQUIRED_CANON = (
    "Noöspace is real.",
    "infinite-dimensional",
    "quantum-information Hilbert space",
    "Astral Plane",
    "Conscious Agent Network",
    "Noöspace is the domain; the Noösphere is an emergent",
    "Time/Space",
    "Self-Transforming Machine Elves",
    "The deeper Noöspace becomes, the less reliable human categories become.",
    "interdimensional Zones",
    "mode of manifestation, not ultimate species identity",
)


def rulebook() -> str:
    return RULEBOOK.read_text(encoding="utf-8")


class NoospaceCanonTests(unittest.TestCase):
    def test_the_rulebook_exists_and_mentions_noospace(self) -> None:
        """Anchor check: if the whole section is deleted, name it first."""
        self.assertIn("Noöspace", rulebook(),
                      "RULEBOOK.md no longer mentions Noöspace at all")

    def test_the_canonical_phrases_survive(self) -> None:
        text = rulebook()
        for phrase in REQUIRED_CANON:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text, f"Missing issue #119 canon phrase: {phrase}")

    def test_the_official_and_colloquial_terms_are_distinguished(self) -> None:
        """The issue's central terminology ruling: Noöspace is the technical term, the
        Astral Plane the colloquial one, and the rulebook must say they name one domain."""
        text = rulebook()
        for phrase in ("Noöspace", "Astral Plane"):
            with self.subTest(term=phrase):
                self.assertIn(phrase, text)

    def test_the_noospace_noosphere_distinction_is_stated(self) -> None:
        """Noöspace is the domain; the Noösphere is an emergent network within it. A later
        edit that collapses the two would erase the issue's core ontology."""
        self.assertIn("Noöspace is the domain; the Noösphere is an emergent", rulebook())

    def test_the_scientific_sources_are_recorded(self) -> None:
        text = rulebook()
        for name in ("Faggin", "Hoffman", "Monroe", "Campbell"):
            with self.subTest(source=name):
                self.assertIn(name, text)

    def test_the_retired_astral_partial_mapping_stays_retired(self) -> None:
        """The old wording mapped the astral only partially onto time/space. Issue #119
        replaced that with the full correspondence, so the superseded sentence must not
        return."""
        self.assertNotIn("The astral is **not identical with all of time/space**", rulebook())


if __name__ == "__main__":
    unittest.main()
