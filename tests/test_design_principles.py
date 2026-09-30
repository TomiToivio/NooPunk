"""Structural guard for NoöPunk's three design balances.

The design principles are project-level invariants, so they are enforced rather
than left as prose that can drift. This test is a STRUCTURE guard, not a
behaviour guard: it asserts that the canonical document exists, that the binding
agent rules restate it, that the other documents reference it, and that none of
them contradict it by describing the rules as unspecified.

It deliberately does NOT constrain how anyone implements a rule. It only prevents
the invariants from being silently dropped.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_DOC = "docs/DESIGN_PRINCIPLES.md"

#: Documents required to point at the canonical principles document.
REFERRING_DOCS = (
    "AGENTS.md",
    "README.md",
    "docs/GODOT_ARCHITECTURE.md",
    "docs/CONCORDIA_ARCHITECTURE.md",
)

#: The three reference poles, by creative agenda.
REFERENCE_POLES = {
    "Gamism": "CY_BORG",
    "Simulationism": "Cyberpunk 2020",
    "Narrativism": "The Sprawl",
}

#: The three defining Noösphere paradigm shifts.
PARADIGM_SHIFTS = ("UFO", "Psionics", "Panpsychism")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalised(relative: str) -> str:
    """Lowercased, whitespace-collapsed text, so line wrapping cannot hide a term."""
    return " ".join(read(relative).split()).lower()


class CanonicalDocumentTests(unittest.TestCase):
    def test_canonical_principles_document_exists(self) -> None:
        self.assertTrue((ROOT / CANONICAL_DOC).exists(), f"{CANONICAL_DOC} is missing")

    def test_documents_all_three_balances(self) -> None:
        text = normalised(CANONICAL_DOC)
        for balance in ("gamism", "narrativism", "simulationism"):
            with self.subTest(balance=balance):
                self.assertIn(balance, text)
        for phrase in ("tabletop", "godot", "concordia", "cyberpunk", "noösphere"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_names_each_canonical_reference_pole(self) -> None:
        text = normalised(CANONICAL_DOC)
        for agenda, system in REFERENCE_POLES.items():
            with self.subTest(agenda=agenda):
                self.assertIn(system.lower(), text)
                self.assertIn(agenda.lower(), text)

    def test_names_the_three_noosphere_paradigm_shifts(self) -> None:
        text = normalised(CANONICAL_DOC)
        for shift in PARADIGM_SHIFTS:
            with self.subTest(shift=shift):
                self.assertIn(shift.lower(), text)
        self.assertIn("paradigm shift", text)

    def test_names_the_comparative_influences(self) -> None:
        text = normalised(CANONICAL_DOC)
        for influence in ("shadowrun", "eclipse phase"):
            with self.subTest(influence=influence):
                self.assertIn(influence, text)
        self.assertIn("not templates to copy", text)

    def test_separates_shared_from_divergent(self) -> None:
        text = normalised(CANONICAL_DOC)
        self.assertIn("shared", text)
        self.assertIn("may diverge", text)
        # both headings must actually carry content
        for section in ("### shared", "### may diverge"):
            with self.subTest(section=section):
                self.assertIn(section, text)

    def test_states_the_parity_principle(self) -> None:
        text = normalised(CANONICAL_DOC)
        self.assertIn("same world, same rules, same mechanics", text)

    def test_carries_all_eight_invariants(self) -> None:
        text = normalised(CANONICAL_DOC)
        for number in range(1, 9):
            with self.subTest(invariant=number):
                self.assertRegex(text, rf"\b{number}\. ")


class AgentRulesTests(unittest.TestCase):
    """AGENTS.md must restate the invariants as binding rules."""

    def test_agents_md_has_a_design_balance_rule(self) -> None:
        text = normalised("AGENTS.md")
        self.assertIn("three design balances", text)

    def test_agents_md_carries_all_eight_invariants(self) -> None:
        text = normalised("AGENTS.md")
        for fragment in (
            "gamism / narrativism / simulationism",
            "cy_borg",
            "cyberpunk 2020",
            "the sprawl",
            "parity",
            "diverge",
            "cyberpunk / noösphere",
            "panpsychism",
            "shadowrun",
            "eclipse phase",
            "not templates to copy",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_agents_md_links_the_canonical_document(self) -> None:
        self.assertIn(CANONICAL_DOC, read("AGENTS.md"))

    def test_agents_md_forbids_silent_redesign(self) -> None:
        text = normalised("AGENTS.md")
        self.assertIn("do not silently redesign these balances", text)


class ReferencingDocsTests(unittest.TestCase):
    """Each document must point at the single source of truth."""

    def test_every_referring_document_links_the_canonical_doc(self) -> None:
        for doc in REFERRING_DOCS:
            with self.subTest(doc=doc):
                self.assertIn(
                    "DESIGN_PRINCIPLES.md",
                    read(doc),
                    f"{doc} does not reference {CANONICAL_DOC}",
                )

    def test_no_document_contradicts_the_principles(self) -> None:
        """A doc must not still claim the rules/attributes are unspecified."""
        stale = (
            "attributes are unspecified",
            "the core resolution mechanic is unspecified",
            "core mechanic is not yet specified",
            "have not yet been specified",
        )
        for doc in REFERRING_DOCS:
            text = normalised(doc)
            for phrase in stale:
                with self.subTest(doc=doc, phrase=phrase):
                    self.assertNotIn(
                        phrase, text, f"{doc} contradicts the specified rules"
                    )

    def test_no_document_presents_a_comparative_influence_as_a_template(self) -> None:
        """A comparative influence must not be advertised as NoöPunk's base system.

        The principles record Shadowrun and Eclipse Phase as comparisons, not
        templates. The published site previously described NoöPunk as an "Eclipse
        Phase homebrew", which says the opposite; nothing checked the site, so it
        survived the first pass of the design-principles work.
        """
        for doc in REFERRING_DOCS + ("docs/index.html",):
            text = normalised(doc)
            for phrase in (
                "eclipse phase homebrew",
                "homebrew for eclipse phase",
                "based on eclipse phase",
                "shadowrun homebrew",
                "based on shadowrun",
            ):
                with self.subTest(doc=doc, phrase=phrase):
                    self.assertNotIn(
                        phrase,
                        text,
                        f"{doc} presents a comparative influence as NoöPunk's base system",
                    )

    def test_architecture_docs_state_the_parity_rule(self) -> None:
        for doc in ("docs/GODOT_ARCHITECTURE.md", "docs/CONCORDIA_ARCHITECTURE.md"):
            with self.subTest(doc=doc):
                text = normalised(doc)
                self.assertIn("design_principles.md", text)
                self.assertTrue(
                    "parity" in text or "same rules" in text or "may diverge" in text,
                    f"{doc} does not state the parity/divergence contract",
                )


class SingleSourceOfTruthTests(unittest.TestCase):
    """The principles must not be duplicated into a competing source."""

    def test_no_second_principles_document_exists(self) -> None:
        candidates = [
            p for p in (ROOT / "docs").glob("*.md")
            if re.search(r"principl|design.?principles", p.name, re.I)
        ]
        names = {p.name for p in candidates}
        self.assertEqual(
            names, {"DESIGN_PRINCIPLES.md"},
            f"expected exactly one canonical principles doc, found {sorted(names)}",
        )

    def test_no_competing_top_level_principles_doc(self) -> None:
        for name in ("DESIGN.md", "PRINCIPLES.md", "BALANCE.md", "PHILOSOPHY.md"):
            with self.subTest(name=name):
                self.assertFalse(
                    (ROOT / name).exists(),
                    f"{name} would be a competing source of truth",
                )


if __name__ == "__main__":
    unittest.main()
