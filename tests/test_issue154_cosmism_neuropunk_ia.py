# -*- coding: utf-8 -*-
"""Regression guards for issue #154 Cosmism / Neuropunk / IA documentation."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
AUDIT = (ROOT / "docs/design/COSMISM_NEUROPUNK_IA_AUDIT.md").read_text(encoding="utf-8")


class Issue154CosmismAuditTests(unittest.TestCase):
    def test_patron_saints_lineage_is_explicit(self) -> None:
        self.assertIn("Pierre Teilhard de Chardin → Ben Goertzel → Ray Kurzweil", RULEBOOK)
        self.assertIn("patron saint of NoöPunk Cosmism", RULEBOOK)

    def test_manifesto_and_goertzel_sources_are_in_bibliography(self) -> None:
        self.assertIn("A Cosmist Manifesto: Practical Philosophy for the Posthuman Age", RULEBOOK)
        self.assertIn("Glocality of Self and Memory as a Possible Foundation for Understanding Psi", RULEBOOK)
        self.assertIn("Mindplexes: The Potential Emergence of Multiple Levels", RULEBOOK)
        self.assertIn("Toward a Formal Model of Cognitive Synergy", RULEBOOK)

    def test_neuropunk_and_ia_sources_are_in_bibliography(self) -> None:
        self.assertIn("Neuropunk Revolution. Hacking Cognitive Systems towards Cyborgs 3.0", RULEBOOK)
        self.assertIn("Augmenting Human Intellect: A Conceptual Framework", RULEBOOK)

    def test_audit_tracks_all_three_requested_domains(self) -> None:
        for heading in (
            "## 2. Cosmism checklist",
            "## 3. Goertzel papers with particularly NoöPunkish ideas",
            "## 4. Neuropunk audit",
            "## 5. Intelligence Augmentation (IA) methods audit",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, AUDIT)

    def test_audit_preserves_epistemic_guardrail(self) -> None:
        self.assertIn("not a declaration that any disputed real-world claim", AUDIT)
        self.assertIn("PSI", AUDIT)
        self.assertIn("not automatic", AUDIT.lower())


if __name__ == "__main__":
    unittest.main()
