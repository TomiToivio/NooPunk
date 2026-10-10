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

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_DOC = "docs/archive/DESIGN_PRINCIPLES.md"

#: Documents required to point at the canonical principles document.
REFERRING_DOCS = (
    "AGENTS.md",
    "README.md",
    "docs/archive/GODOT_ARCHITECTURE.md",
    "docs/archive/CONCORDIA_ARCHITECTURE.md",
)

#: The three reference poles, by creative agenda, per the issue #200 triangle.
#: These were CY_BORG / Cyberpunk 2020 / The Sprawl before #200 realigned the corners;
#: the doc's own invariant #2 named the old trio after #203 had already rewritten §1, so
#: the pole set and the triangle contradicted each other while this guard passed on the
#: leftover sentence. See `test_the_canonical_poles_match_the_triangle`.
REFERENCE_POLES = {
    "Gamism": "Cities Without Number",
    "Simulationism": "Eclipse Phase",
    "Narrativism": "Apocalypse World",
}

#: The pole trio that issue #200 superseded. Named once, so a future rename edits one place.
SUPERSEDED_POLES = ("CY_BORG", "Cyberpunk 2020", "The Sprawl")

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

    def test_the_canonical_poles_match_the_triangle(self) -> None:
        """The pole sentence must agree with the #200 triangle, in the same doc.

        Sentence-scoped on purpose: #203 rewrote §1 to the new corners while invariant #2
        still said CY_BORG / Cyberpunk 2020 / The Sprawl, and a document-wide name check was
        satisfied by that leftover, so it could not see the contradiction.
        """
        text = read(CANONICAL_DOC)
        sentences = [s for s in re.split(r"(?<=[.;])\s+", text) if "canonical reference poles" in s]
        self.assertTrue(sentences, "no sentence declares the canonical reference poles")
        for sentence in sentences:
            for system in ("Eclipse Phase", "Apocalypse World", "Cities Without Number"):
                with self.subTest(system=system):
                    self.assertIn(system, sentence)
            for superseded in ("CY_BORG", "Cyberpunk 2020", "The Sprawl"):
                with self.subTest(superseded=superseded):
                    self.assertNotIn(superseded, sentence)

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

    def test_carries_all_nine_invariants(self) -> None:
        text = normalised(CANONICAL_DOC)
        for number in range(1, 10):
            with self.subTest(invariant=number):
                self.assertRegex(text, rf"\b{number}\. ")


class AgentRulesTests(unittest.TestCase):
    """AGENTS.md must restate the invariants as binding rules."""

    def test_agents_md_has_a_design_balance_rule(self) -> None:
        text = normalised("AGENTS.md")
        self.assertIn("three design balances", text)

    def test_agents_md_carries_all_nine_invariants(self) -> None:
        """§13 must list all nine, not just mention the rules-source rule somewhere else.

        Scoping to the §13 block matters: AGENTS.md also names the rules source in
        §15, so a document-wide substring check would pass even with invariant 9
        deleted from the invariant list.
        """
        section = re.search(
            r"(?ms)^### 13\. Preserve the three design balances.*?(?=\n### |\Z)",
            read("AGENTS.md"),
        )
        self.assertIsNotNone(section, "AGENTS.md §13 not found")
        assert section is not None
        text = " ".join(section.group(0).split()).lower()
        for fragment in (
            "gamism / narrativism / simulationism",
            # NOTE: the superseded poles (CY_BORG / Cyberpunk 2020 / The Sprawl) are
            # deliberately NOT required here. Requiring them is what kept AGENTS.md §13.2
            # pinned to them while the canonical document was required to name the #200
            # triangle, so the two could never agree. Pole CONTENT is checked by
            # test_the_agents_md_pole_sentence_agrees_with_the_canonical_document instead.
            "parity",
            "diverge",
            "cyberpunk / noösphere",
            "panpsychism",
            "shadowrun",
            "eclipse phase",
            "the veil",
            "independent rules system inspired by multiple games",
            "1–10 stat + 1–10 skill + 1d10 core",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_agents_md_invariant_list_is_numbered_one_to_nine(self) -> None:
        """The list itself, not just its content, must run 1..9."""
        section = re.search(
            r"(?ms)^### 13\. Preserve the three design balances.*?(?=\n### |\Z)",
            read("AGENTS.md"),
        )
        self.assertIsNotNone(section, "AGENTS.md §13 not found")
        assert section is not None
        numbers = re.findall(r"(?m)^(\d+)\. ", section.group(0))
        self.assertEqual(numbers, [str(n) for n in range(1, 10)])

    @staticmethod
    def _pole_sentences(relative: str) -> list[str]:
        """Sentences in `relative` that declare the canonical reference poles.

        Sentence-scoped, following test_the_canonical_poles_match_the_triangle: a
        document-wide substring check is satisfied by a leftover mention and cannot see
        a contradiction.
        """
        text = read(relative)
        return [s for s in re.split(r"(?<=[.;])\s+", text) if "canonical reference poles" in s]

    def test_the_agents_md_pole_sentence_agrees_with_the_canonical_document(self) -> None:
        """AGENTS.md §13.2 and the canonical document must not name different poles.

        AGENTS.md §13 promises this guard "fails the build if these invariants, the
        canonical document, or the documents that reference it drift out of agreement".
        It did not. The §13 fragment list *required* the superseded trio, while
        test_the_canonical_poles_match_the_triangle *forbade* it in the canonical
        document: two contradictory expectations in one file, so the disagreement was
        permanent by construction rather than merely unnoticed.

        The disagreement itself is author-owned (issue #200, PR #211), so it is not
        resolved here. What is enforced is that it stays VISIBLE: the two documents
        either agree, or the rights ledger records the standing contradiction. Reconcile
        AGENTS.md §13.2 and this test tells you to clear that record; silently edit
        either side and it fails.
        """
        agents = self._pole_sentences("AGENTS.md")
        canonical = self._pole_sentences(CANONICAL_DOC)
        self.assertTrue(agents, "AGENTS.md declares no canonical reference poles")
        self.assertTrue(canonical, f"{CANONICAL_DOC} declares no canonical reference poles")

        agents_text = " ".join(agents)
        canonical_text = " ".join(canonical)
        agents_superseded = all(pole in agents_text for pole in SUPERSEDED_POLES)
        agents_triangle = all(pole in agents_text for pole in REFERENCE_POLES.values())
        self.assertTrue(
            all(pole in canonical_text for pole in REFERENCE_POLES.values()),
            f"{CANONICAL_DOC} must name the #200 triangle poles in its pole sentence",
        )

        ledger = json.loads(read("data/sources/game_system_rights.json"))
        record = json.dumps(ledger["open_inconsistency"])

        if agents_superseded and not agents_triangle:
            # The known, author-owned disagreement. It must be RECORDED, not just present.
            self.assertIn(
                "AGENTS.md",
                ledger["open_inconsistency"].get("what_remains", ""),
                "AGENTS.md §13.2 still names the superseded poles; the rights ledger must "
                "record that standing contradiction (issue #200).",
            )
            self.assertIn("AGENTS.md", record)
        else:
            self.assertNotIn(
                "what_remains",
                ledger["open_inconsistency"],
                "AGENTS.md and the canonical document now agree on the poles -- clear the "
                "standing contradiction from data/sources/game_system_rights.json.",
            )

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
        for doc in ("docs/archive/GODOT_ARCHITECTURE.md", "docs/archive/CONCORDIA_ARCHITECTURE.md"):
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
            p for p in list((ROOT / "docs").glob("*.md"))
            + list((ROOT / "docs" / "archive").glob("*.md"))
            if re.search(r"principl|design.?principles", p.name, re.IGNORECASE)
        ]
        found = {p.relative_to(ROOT).as_posix() for p in candidates}
        self.assertEqual(
            found, {CANONICAL_DOC},
            f"expected exactly one canonical principles doc, found {sorted(found)}",
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
