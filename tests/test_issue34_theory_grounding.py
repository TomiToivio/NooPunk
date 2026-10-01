# -*- coding: utf-8 -*-
"""Regression tests for issue #34: theory-grounded character systems framework.

These are STRUCTURE guards, in the style of ``test_issue32_rules_reset.py``. They
assert that every element the issue required to be *written into the rulebook and
the source registry* is actually there, and that the issue's guardrails hold.

They deliberately do NOT constrain mechanics. Issue #34 states the only
mechanical consequence is the four-group division itself and forbids inventing
the individual statistics, so a test here may never require a stat name.

What is protected here:

* the rulebook states the theoretical-grounding principle, and the source
  registry is reachable from it;
* the four groups are named and their theoretical treatment exists;
* the source citation required by the issue is present;
* the required five-part treatment is present for the Luhmannian rule
  (source / what it argues / NoöPunk interpretation / disagreement or extension /
  mechanical consequence) with the parts kept separable;
* the Cybernetic domain is never attributed to Luhmann;
* the disagreement with a strict reading of Luhmann is recorded, not erased;
* the speculative metaphysical layer is labelled as speculation;
* the nested-participation table is present and marks only the Psychic row as
  metaphysical;
* "Social" is not collapsed into charisma and "Cybernetic" is not collapsed into
  programming skill;
* no individual statistic has been invented into the four groups.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = "RULEBOOK.md"
REGISTRY = "docs/THEORETICAL_SOURCES.md"
MEMO = "docs/RULES_RESET_MEMO.md"

#: The four groups, as the issue names them.
GROUPS = ("physical", "social", "psychic", "cybernetic")

#: The keyword entry this issue makes the first major treatment.
ENTRY_ANCHOR = "luhmannian-four-system-character-architecture"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalised(relative: str) -> str:
    """Lowercased, whitespace-collapsed, markdown emphasis stripped."""
    text = re.sub(r"[>*_`]", " ", read(relative))
    return " ".join(text.split()).lower()


def flat(relative: str) -> str:
    return normalised(relative)


class TheoreticalGroundingPrincipleTests(unittest.TestCase):
    """The issue requires the principle itself to be in the rulebook."""

    def test_rulebook_states_the_grounding_principle(self) -> None:
        text = flat(RULEBOOK)
        self.assertIn("theoretical source", text)
        self.assertIn("every canonical rule", text)

    def test_rulebook_links_the_source_registry(self) -> None:
        self.assertIn(REGISTRY, read(RULEBOOK))

    def test_registry_exists_and_states_its_purpose(self) -> None:
        self.assertTrue((ROOT / REGISTRY).exists(), f"{REGISTRY} is missing")
        text = flat(REGISTRY)
        self.assertIn("source", text)
        self.assertIn("noöpunk interpretation", text)

    def test_registry_separates_source_from_interpretation(self) -> None:
        """The issue requires the parts to be distinguishable, not blended."""
        text = flat(REGISTRY)
        self.assertIn("what the source itself argues", text)
        self.assertIn("where noöpunk disagrees", text)
        self.assertIn("mechanical consequence", text)

    def test_registry_names_the_required_citation(self) -> None:
        text = read(REGISTRY)
        self.assertIn("Unlocking Luhmann", text)
        self.assertIn("10.14361/9783839456743", text)
        self.assertIn("Bielefeld University Press", text)

    def test_registry_keeps_quotations_short(self) -> None:
        """Normal scholarly practice: short quotations, otherwise paraphrase."""
        quotes = re.findall(r"^>\s*(.+)$", read(REGISTRY), re.M)
        self.assertTrue(quotes, "the entry should carry the source's own wording")
        # A long block quotation would mean the entry is reproducing the source
        # rather than citing it. 100 words is generous for a keyword definition.
        for quote in quotes:
            with self.subTest(quote=quote[:40]):
                self.assertLess(
                    len(quote.split()), 100, "quotation is too long; paraphrase instead"
                )


class FourGroupArchitectureTests(unittest.TestCase):
    """Section 5 must name all four groups and carry their theoretical treatment."""

    def test_rulebook_names_all_four_groups(self) -> None:
        text = flat(RULEBOOK)
        for group in GROUPS:
            with self.subTest(group=group):
                self.assertIn(group, text)

    def test_rulebook_section_five_carries_the_treatment(self) -> None:
        text = read(RULEBOOK)
        section = text[text.index("## 5. Characters"):text.index("## 6. ")]
        for heading in (
            "Theoretical architecture of the four groups",
            "Source.",
            "NoöPunk's reading.",
            "Our extension.",
            "Where NoöPunk disagrees.",
            "Nested participation.",
            "Psychic as fundamental.",
            "Mechanical consequence.",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, section)

    def test_rulebook_points_at_the_registry_entry(self) -> None:
        text = read(RULEBOOK)
        self.assertIn(ENTRY_ANCHOR, text)


class GuardrailTests(unittest.TestCase):
    """The issue's negative constraints. These are the ones a rewrite erases."""

    def test_cybernetic_is_not_attributed_to_luhmann(self) -> None:
        """The fourth domain is NoöPunk's, and the documents must say so."""
        for doc in (RULEBOOK, REGISTRY):
            with self.subTest(doc=doc):
                text = flat(doc)
                self.assertRegex(
                    text,
                    r"not attributed to\s*luhmann|noöpunk extension|noopunk extension",
                    f"{doc} does not mark Cybernetic as NoöPunk's own extension",
                )

    def test_the_disagreement_with_luhmann_is_recorded(self) -> None:
        """Entanglement: NoöPunk does not adopt a clean ontological separation.

        Checks the *body* of the disagreement section, not just its heading --
        matching the heading alone let a rewrite that emptied the section pass.
        """
        text = read(REGISTRY)
        section = text[text.index("### Where NoöPunk disagrees"):text.index("### Nested participation")]
        body = " ".join(section.split()).lower()
        self.assertIn("entangled", body)
        self.assertIn("not", body)
        # The section must carry an actual claim about the systems' relation,
        # not merely announce that a disagreement exists.
        self.assertRegex(body, r"coupled|interpenetrat|mutually constitutive|separate in the fiction")

    def test_speculative_metaphysics_is_labelled(self) -> None:
        """Panpsychism must not be presented as settled science."""
        text = flat(REGISTRY)
        self.assertRegex(text, r"not established science|setting metaphysics")
        self.assertIn("panpsychism", text)

    def test_only_the_psychic_row_is_metaphysical(self) -> None:
        text = read(REGISTRY)
        table = text[text.index("### Nested participation"):text.index("### Speculative extension")]
        rows = [line for line in table.splitlines() if line.startswith("|")]
        body = [r for r in rows if "---" not in r and "Larger system" not in r]
        self.assertEqual(len(body), 4, "nested participation needs one row per group")
        flagged = [r for r in body if "metaphysic" in r.lower()]
        self.assertEqual(len(flagged), 1, "exactly one nested row is metaphysical")
        self.assertIn("psychic", flagged[0].lower())

    def test_social_is_not_collapsed_into_charisma(self) -> None:
        text = flat(RULEBOOK)
        self.assertRegex(text, r"communication systems|not charisma|not a measure of personality")

    def test_cybernetic_is_not_collapsed_into_programming_skill(self) -> None:
        """Checked against the paragraph that makes the claim, not the whole file.

        Searching the whole rulebook let a rewrite of this paragraph pass,
        because the phrase also occurs in the four-group summary list.
        """
        text = read(RULEBOOK)
        start = text.index("**Cybernetic is a domain, not a programming skill.**")
        paragraph = " ".join(text[start:text.index("\n\n", start)].split()).lower()
        self.assertRegex(
            paragraph,
            r"not.{0,12}(reduced to|a programming)",
            "the Cybernetic paragraph no longer refuses the skill reading",
        )
        self.assertRegex(paragraph, r"machine and network systems|participation in machine")

    def test_physical_terminology_note_exists(self) -> None:
        text = flat(REGISTRY)
        self.assertIn("game-design simplification", text)

    def test_individual_statistics_were_not_invented(self) -> None:
        """#34: "Do not invent the individual stats inside the four groups yet."

        The six legacy attributes are explicitly retained as legacy; anything
        else presented as a *canonical attribute list entry* in the theoretical
        treatment would be an invention.
        """
        text = read(RULEBOOK)
        section = text[text.index("## 5. Characters"):text.index("### 5.1")]
        self.assertIsNone(
            re.search(r"\*\*(Strength|Agility|Wits|Luck|Presence|Resolve) \(", section),
            "the theoretical treatment invented a new attribute",
        )
        self.assertIn("not yet finalized", section)

    def test_no_other_rpg_was_imported_as_the_chassis(self) -> None:
        """#34: "Do not import another RPG chassis to fill gaps.\""""
        text = read(RULEBOOK)
        section = text[text.index("## 5. Characters"):text.index("### 5.1")]
        lowered = section.lower()
        for game in ("cyberpunk 2020", "shadowrun", "eclipse phase", "the sprawl", "cy_borg"):
            with self.subTest(game=game):
                self.assertNotIn(f"{game} as the chassis", lowered)


class SpeculativeLayerStaysModularTests(unittest.TestCase):
    """The metaphysics is a later layer; it must not be welded into the core."""

    def test_memo_already_places_the_metaphysics_as_coupling(self) -> None:
        text = flat(MEMO)
        self.assertIn("coupling", text)
        self.assertIn("noösphere", text)

    def test_psychic_fundamentality_is_marked_as_direction_not_rule(self) -> None:
        text = flat(REGISTRY)
        self.assertIn("fundamental", text)
        self.assertRegex(text, r"no mechanics at\s*this stage|carries no mechanics")


if __name__ == "__main__":
    unittest.main()
