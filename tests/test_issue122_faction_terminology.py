"""Structure guard for the faction-system terminology of issue #122.

Issue #122 fixes the *vocabulary* for the faction system — Contacts, Motivations, Faction
Reputation, US / FRONTIER, Affect, and the Social Network Analysis graph layers — so the
same terms mean the same thing in the rulebook, character data, faction data, NPC
generation, code and visualization. The terminology lives in ``rulebook/8_FACTIONS.md``.

A structure guard in the style of ``test_issue60_setting_canon.py``:

1. asserts the chapter exists and is discoverable from RULEBOOK.md;
2. asserts each canonical term the issue names is defined;
3. asserts the relationship shape and the seven graph layers are stated;
4. asserts the US / FRONTIER model keeps the parts that make it more than a flavour
   alignment field, and stays explicitly NOT a populism classifier;
5. asserts the score-scale conflict is **resolved by issue #144** in favor of the canonical
   -10..+10 scale across the rulebook, schema and engine.

Uses only the standard library: CI installs requirements.txt and nothing else.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "8_FACTIONS.md"
RULEBOOK = ROOT / "RULEBOOK.md"


def chapter() -> str:
    return " ".join(CHAPTER.read_text(encoding="utf-8").split())


class ChapterTests(unittest.TestCase):
    def test_the_chapter_exists(self) -> None:
        self.assertTrue(CHAPTER.exists(), "rulebook/8_FACTIONS.md is missing")

    def test_the_chapter_keeps_its_stable_heading(self) -> None:
        """The heading is the anchor every other assertion and cross-reference uses. An
        earlier version of this guard never asserted it, so renaming the chapter away left
        the guard green."""
        self.assertRegex(chapter(), r"^# Faction system terminology\b",
                         "the chapter heading was renamed or removed")

    def test_the_rulebook_points_at_the_chapter(self) -> None:
        """A chapter nobody links is a chapter nobody reads."""
        self.assertIn("rulebook/8_FACTIONS.md", RULEBOOK.read_text(encoding="utf-8"))


class TerminologyTests(unittest.TestCase):
    #: The canonical terms the issue asks to confirm, plus the object kinds under US/FRONTIER.
    TERMS = (
        "Contact", "Motivation", "Faction Reputation", "US", "FRONTIER", "Affect",
        "Goals", "Empty Signifiers", "Actors",
    )

    def test_every_canonical_term_is_defined(self) -> None:
        """Case-sensitive on the canonical capitalisation: the terms are proper nouns of the
        system, so a lower-cased or renamed variant is a real drift, not a stylistic one."""
        text = CHAPTER.read_text(encoding="utf-8")
        for term in self.TERMS:
            with self.subTest(term=term):
                self.assertIn(term, text, f"canonical term missing or renamed: {term}")

    def test_the_core_terms_are_defined_as_headings_or_definitions(self) -> None:
        """Each of the four layers the issue asks to confirm gets its own `##` heading, so a
        later edit cannot demote it to a passing mention."""
        text = CHAPTER.read_text(encoding="utf-8")
        for heading in ("## Contacts", "## Motivations", "## Faction Reputation",
                        "## Faction ideology: US and FRONTIER"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_the_relationship_shape_is_stated(self) -> None:
        self.assertRegex(chapter(), r"source, target, score, affect")

    def test_contacts_are_personal_not_group_standing(self) -> None:
        """The issue is explicit that a Contact is a personal relationship and that group
        standing is a different layer. Collapsing them would merge two graph layers."""
        self.assertRegex(chapter(), r"personal relationship")

    def test_the_default_affects_are_recorded(self) -> None:
        text = chapter()
        self.assertIn("Likes", text)
        self.assertIn("Dislikes", text)

    def test_reputation_is_directional(self) -> None:
        """Reputation is faction -> character, not the character's opinion of the faction.
        An earlier draft of the issue's model got this backwards."""
        self.assertRegex(chapter(), r"directional")

    def test_faction_membership_seeds_but_does_not_control(self) -> None:
        self.assertRegex(chapter(), r"not a personality package|not mind control|seeding rule")


class IdeologyModelTests(unittest.TestCase):
    def test_the_us_frontier_model_is_defined_as_constitutive_and_antagonistic(self) -> None:
        text = chapter()
        self.assertRegex(text, r"constitutive")
        self.assertRegex(text, r"antagonistic")

    def test_it_is_not_a_populism_classifier(self) -> None:
        """The Formula of Populism is adapted as a general faction model. The chapter must
        say so, or the term invites the reading that factions are populist by default."""
        self.assertRegex(chapter(), r"not a populism classifier")

    def test_a_frontier_is_not_merely_disagreement(self) -> None:
        """Assert the NEGATION, not the phrase. An earlier version matched only
        `[Mm]ere disagreement`, so replacing the rule with 'Mere disagreement is enough to
        mark a frontier' kept the phrase and passed."""
        text = chapter()
        self.assertRegex(
            text,
            r"[Mm]ere disagreement or dislike is not automatically a frontier",
            "the 'a frontier is not mere disagreement' rule was reworded or removed",
        )

    def test_empty_and_floating_signifiers_are_role_marked_not_inferred(self) -> None:
        self.assertRegex(chapter(), r"[Aa]mbiguity alone never")


class GraphLayerTests(unittest.TestCase):
    LAYERS = (
        "Character ↔ Character", "Character ↔ Motivation", "Character ↔ Faction",
        "Faction ↔ Actor", "Faction ↔ Goal", "Faction ↔ Empty Signifier",
        "Faction ↔ Faction",
    )

    def test_all_seven_graph_layers_are_named(self) -> None:
        text = chapter()
        for layer in self.LAYERS:
            with self.subTest(layer=layer):
                self.assertIn(layer, text)

    def test_the_layers_are_a_numbered_index_not_loose_prose(self) -> None:
        """Assert the list NUMBERS, not only the layer names.

        A name-only check passes with the `1.`–`7.` markers stripped, because every phrase
        still appears -- but the result is no longer a usable index, and the issue asks for
        an enumerated set. Proven by sabotage: removing the numbering left the guard green.
        """
        raw = CHAPTER.read_text(encoding="utf-8")
        expected = [f"{n}. **{layer}" for n, layer in enumerate(self.LAYERS, start=1)]
        for marker in expected:
            with self.subTest(marker=marker):
                self.assertIn(marker, raw, f"the graph layer list lost its numbering: {marker}")

    def test_the_layers_are_in_the_issue_s_order(self) -> None:
        """The issue lists them 1..7; a reordering that keeps all seven names would still
        satisfy a membership check, so assert the sequence too."""
        raw = CHAPTER.read_text(encoding="utf-8")
        positions = [raw.find(layer) for layer in self.LAYERS]
        self.assertNotIn(-1, positions, "a graph layer name is missing entirely")
        self.assertEqual(positions, sorted(positions),
                         "the graph layers are no longer in the issue's order")

    def test_faction_to_faction_edges_are_derived_not_stored(self) -> None:
        """The issue says rivalries are derived from US/FRONTIER overlap; a stored opinion
        field would be a second source of truth for the same fact."""
        self.assertRegex(chapter(), r"derived from")


class ScaleConflictTests(unittest.TestCase):
    """Issue #144 resolves the old #107/#122 scale conflict."""

    def test_canonical_scale_is_ten(self) -> None:
        text = chapter()
        self.assertIn("-10 to +10", text)
        self.assertNotIn("Open question: the score scale", text)

    def test_rulebook_uses_ten_scale(self) -> None:
        rulebook = RULEBOOK.read_text(encoding="utf-8")
        self.assertIn("-10 to +10", rulebook)
        self.assertNotIn("-100 to +100", rulebook)

class ScopeTests(unittest.TestCase):
    def test_the_chapter_defines_no_new_mechanics(self) -> None:
        """It fixes vocabulary. Dice, DVs and skill checks belong elsewhere."""
        text = chapter()
        for mechanic in ("skill check", "difficulty value", "1d10"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic.lower(), text.lower())

    def test_it_defers_the_open_questions_rather_than_answering_them(self) -> None:
        self.assertRegex(chapter(), r"Questions this section does not settle")


if __name__ == "__main__":
    unittest.main()
