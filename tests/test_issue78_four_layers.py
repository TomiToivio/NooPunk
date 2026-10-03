"""Structure guard for the four-layer ontology and its couplings (issue #78).

Issue #78 defines NoöPunk's four layers — Physical, Psychic, Social, Cybernetic — as a
deliberate modification of Luhmann's systems theory, and states that "much of the
interesting gameplay happens at their interfaces". This guard protects the properties a
later session could silently lose.

What is protected here:

* all four layers are named, and the Cybernetic one is presented as a NoöPunk
  extension rather than as something Luhmann claimed;
* Biological is generalised to Physical for setting purposes;
* language is NOT a separate layer -- no Linguistic layer may appear;
* Psychic and Social stay distinct layers;
* PSI is natural, never virus-derived;
* the seven structural couplings are enumerated, including the all-four case;
* the Psychic layer does not use physical distance as its metric;
* speculative theories stay marked as setting lore, not established science;
* the couplings section defines no mechanics.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = "RULEBOOK.md"
ATTRIBUTES = "rulebook/2_ATTRIBUTES.md"

#: The four layers, as the issue names them.
LAYERS = ("Physical", "Psychic", "Social", "Cybernetic")

#: The seven couplings the issue enumerates.
COUPLINGS = (
    ("Physical", "Psychic"),
    ("Psychic", "Social"),
    ("Social", "Cybernetic"),
    ("Cybernetic", "Physical"),
    ("Psychic", "Cybernetic"),
    ("Psychic", "Psychic"),
)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def flat(relative: str) -> str:
    """Whitespace-collapsed, emphasis-stripped, lowercased.

    Structural markers are stripped so a wrapped or emphasised phrase still matches, but
    the comparison characters are untouched -- they are canon text.
    """
    text = re.sub(r"[*`]", "", read(relative))
    return " ".join(text.split()).lower()


#: Documents that together carry the four-layer ontology. The layer definitions and the
#: Luhmann modifications live in the attribute stub; the couplings live in RULEBOOK.md.
LAYER_DOCS = (RULEBOOK, ATTRIBUTES)


def layer_text() -> str:
    """Flattened text of every document that defines the layers."""
    return " ".join(flat(d) for d in LAYER_DOCS)


def section(number: int) -> str:
    """The body of `## <number>. ...`, up to the next `## `."""
    body = read(RULEBOOK)
    match = re.search(rf"(?m)^## {number}\.\s", body)
    assert match, f"RULEBOOK section {number} not found"
    rest = body[match.end():]
    nxt = re.search(r"(?m)^## \d+\.\s", rest)
    return rest[: nxt.start()] if nxt else rest


class FourLayersAreDefined(unittest.TestCase):
    def test_all_four_layers_are_named(self) -> None:
        text = flat(RULEBOOK)
        for layer in LAYERS:
            with self.subTest(layer=layer):
                self.assertIn(layer.lower(), text)

    def test_the_four_layers_appear_together(self) -> None:
        """Naming them separately is not defining a four-layer ontology.

        Scoped to the layer documents as a set: the attribute stub states the division
        outright ("We divide attributes into Physical, Social, Cybernetic and Psychic"),
        so checking RULEBOOK.md alone would fail against correct content.
        """
        text = layer_text()
        self.assertRegex(
            text,
            r"physical.{0,80}psychic.{0,80}social.{0,80}cybernetic"
            r"|physical.{0,80}social.{0,80}cybernetic.{0,80}psychic",
        )

    def test_both_binding_documents_agree_on_the_four_layers(self) -> None:
        """The rulebook and the attribute stub must not drift apart."""
        for doc in (RULEBOOK, ATTRIBUTES):
            text = flat(doc)
            with self.subTest(doc=doc):
                for layer in LAYERS:
                    self.assertIn(layer.lower(), text)


class TheLuhmannModificationsAreStated(unittest.TestCase):
    def test_biological_is_generalised_to_physical(self) -> None:
        text = flat(RULEBOOK) + " " + flat(ATTRIBUTES)
        self.assertRegex(
            text,
            r"(instead of biological|rename biological|biological systems into physical"
            r"|generaliz\w* .{0,30}physical|rather than biological)",
            "the Biological -> Physical generalisation is not stated",
        )

    def test_cybernetic_is_presented_as_a_noopunk_extension(self) -> None:
        """The issue is explicit: do not attribute this to Luhmann.

        The statement lives in the attribute stub ("NoöPunk adds Cybernetic Systems"),
        so the assertion spans the layer documents rather than RULEBOOK.md alone.
        """
        text = layer_text()
        self.assertIn("cybernetic", text)
        self.assertRegex(
            text,
            r"noöpunk (extension|adds|adaptation)|fourth (type|domain|system)|adds cybernetic",
            "Cybernetic is not marked as a NoöPunk extension",
        )

    def test_luhmann_is_not_credited_with_the_cybernetic_layer(self) -> None:
        text = layer_text()
        for claim in ("luhmann's fourth", "luhmann added cybernetic",
                      "luhmann proposed cybernetic"):
            with self.subTest(claim=claim):
                self.assertNotIn(claim, text)


class NoLinguisticLayerTests(unittest.TestCase):
    """The issue is emphatic: language belongs to Social, not to its own layer."""

    def test_no_linguistic_layer_is_defined(self) -> None:
        text = flat(RULEBOOK)
        self.assertNotRegex(
            text,
            r"linguistic layer|fifth layer|separate linguistic|languistic layer",
            "a Linguistic layer appeared; language belongs to the Social layer",
        )

    def test_language_is_placed_inside_social(self) -> None:
        text = flat(RULEBOOK)
        self.assertRegex(
            text,
            r"language.{0,120}social|social.{0,120}language",
            "language is not tied to the Social layer",
        )

    def test_the_four_layers_stay_four(self) -> None:
        """A five-layer formulation would break the Luhmannian basis."""
        text = flat(RULEBOOK)
        for wrong in ("five layers", "five-layer", "four layers plus"):
            with self.subTest(wrong=wrong):
                self.assertNotIn(wrong, text)


class PsychicAndSocialStaySeparate(unittest.TestCase):
    def test_the_two_are_not_collapsed(self) -> None:
        text = flat(RULEBOOK)
        self.assertRegex(
            text,
            r"distinct but structurally coupled|remain distinct|stay distinct"
            r"|consciousness and communication",
            "Psychic and Social are not distinguished",
        )

    def test_psi_is_natural_not_virus_derived(self) -> None:
        """A signature NoöPunk rule: PSI is not an infection."""
        text = flat(RULEBOOK)
        self.assertRegex(
            text,
            r"not caused by an alien virus|natural latent psi|not.{0,30}virus"
            r"|not.{0,30}infection",
            "the natural-not-viral rule for PSI is missing",
        )
        self.assertNotRegex(
            text,
            r"psi is (caused|spread) by (an? )?(alien )?(virus|infection)",
            "PSI is described as virus-derived",
        )


def coupling_entries() -> list[str]:
    """The bolded coupling labels in §34, e.g. "Physical <-> Psychic".

    Extracted structurally rather than by substring: a document-wide search for
    "psychic ... psychic" still matches after a row is deleted, because §34.1 also
    discusses the psychic/social relation. Reading the list items is what makes a
    deleted or renamed row detectable.
    """
    body = section(34)
    entries = re.findall(r"(?m)^-\s+\*\*(.+?)\*\*\s*(?:—|--|-)", body)
    return [" ".join(e.split()) for e in entries]


class CouplingTests(unittest.TestCase):
    def test_the_couplings_section_exists(self) -> None:
        body = section(34)
        self.assertIn("coupl", body.lower())

    def test_the_coupling_list_has_the_expected_rows(self) -> None:
        """Assert the row COUNT, so deleting a row cannot pass."""
        entries = coupling_entries()
        self.assertGreaterEqual(
            len(entries), 7,
            f"§34 lists only {len(entries)} couplings; the issue enumerates seven: {entries}",
        )

    def test_every_layer_pair_is_enumerated(self) -> None:
        """Match against the extracted labels, not the whole section body."""
        entries = " | ".join(coupling_entries()).lower()
        for a, b in COUPLINGS:
            with self.subTest(pair=f"{a}<->{b}"):
                self.assertIn(
                    f"{a.lower()} ↔ {b.lower()}", entries,
                    f"the {a} <-> {b} coupling row is not present; §34 lists: {entries}",
                )

    def test_no_linguistic_layer_replaces_a_psychic_coupling(self) -> None:
        """A row renamed to Linguistic would break the four-layer basis."""
        entries = " | ".join(coupling_entries()).lower()
        self.assertNotIn("linguistic ↔", entries)

    def test_the_all_four_case_is_present(self) -> None:
        """The issue lists an all-four coupling, not only pairwise ones."""
        body = " ".join(section(34).split()).lower()
        self.assertRegex(body, r"all four", "the all-four coupling is missing")

    def test_the_interface_rationale_is_recorded(self) -> None:
        body = " ".join(section(34).split()).lower()
        self.assertRegex(
            body,
            r"interfaces?|at their interface",
            "the reason the couplings matter is not recorded",
        )

    def test_the_couplings_define_no_mechanics(self) -> None:
        """This is ontology; §16 keeps psi mechanics deferred."""
        body = section(34).lower()
        for forbidden in ("dice", "modifier", "point cost", "roll "):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, body)


class PsychicMetricTests(unittest.TestCase):
    def test_the_psychic_layer_is_not_spatial(self) -> None:
        """Scoped to §34.2.

        A document-wide check passes even when the §34.2 statement is inverted, because
        §16.2 independently says PSI is non-local. The claim under test is the one in the
        couplings section, so assert against that section.
        """
        body = " ".join(section(34).split()).lower()
        self.assertRegex(
            body,
            r"must not use physical distance|not use physical distance"
            r"|rather than kilometres|rather than kilometers",
            "§34.2 does not state that the Psychic layer is non-spatial",
        )
        # and the inverted form must be absent
        self.assertNotRegex(
            body,
            r"psychic\*\*? layer uses physical distance|uses physical distance as its fundamental",
            "§34.2 gives the Psychic layer a spatial metric",
        )


class SpeculativeStaysSpeculativeTests(unittest.TestCase):
    def test_the_setting_lore_is_marked_as_lore(self) -> None:
        """Assert the NEGATION, not merely the vocabulary.

        The bare word "fictional" appears in half a dozen places, so it passes even when
        a specific disclaimer is deleted. The guard checks that a disclaimer is present
        AND carries its negation.
        """
        text = flat(RULEBOOK)
        disclaimers = re.findall(r"([\w\s,]{0,60}(?:not a claim about|not established science|not settled descriptions))", text)
        self.assertTrue(disclaimers, "no 'not a claim about' style disclaimer exists at all")
        for d in disclaimers:
            with self.subTest(fragment=d[:50]):
                self.assertIn("not", d)

    def test_the_lore_disclaimers_are_not_stripped(self) -> None:
        """Count the distinct disclaimers.

        The three the rulebook actually carries, in their own wordings:
          * "not a claim about real human destiny"   (§16.3)
          * "do not establish NooPunk's fictional conclusions"  (§35)
          * "not as settled descriptions of the real world"     (§35)
        Asserting a count catches a stripped disclaimer that a single remaining
        occurrence would otherwise mask.
        """
        text = flat(RULEBOOK)
        patterns = (
            r"not a claim about",
            r"do not establish",
            r"not as settled descriptions",
        )
        found = [p_ for p_ in patterns if re.search(p_, text)]
        self.assertEqual(
            len(found), len(patterns),
            f"lore disclaimers stripped: {sorted(set(patterns) - set(found))}",
        )

    def test_the_interpretation_rule_survives(self) -> None:
        text = flat(RULEBOOK)
        self.assertIn("interpretation rule", text)


class RulebookHygieneTests(unittest.TestCase):
    def test_section_numbering_has_no_gaps(self) -> None:
        """The file had a §34 hole before this change; it must not reopen."""
        numbers = [int(n) for n in re.findall(r"(?m)^## (\d+)\.", read(RULEBOOK))]
        self.assertEqual(numbers, list(range(1, max(numbers) + 1)),
                         f"section numbering has a gap: {numbers}")

    def test_the_four_layers_are_written_as_a_letter_case_the_repo_uses(self) -> None:
        """NOÖPUNK carries the umlaut; an ASCII-only label is a mismatch."""
        for doc in LAYER_DOCS:
            with self.subTest(doc=doc):
                self.assertNotIn("NOOEPUNK", read(doc))


if __name__ == "__main__":
    unittest.main()
