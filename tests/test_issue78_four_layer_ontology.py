"""Regression guard for issue #78: the four NoöPunk systems ontology.

These are STRUCTURE guards, in the style of ``test_issue34_theory_grounding.py`` and
``test_issue60_setting_canon.py``. Issue #78 asks for the **four-layer ontology** —
Physical, Psychic, Social, Cybernetic — to be written into the rulebook, with Luhmann's
original theory clearly separated from NoöPunk's extensions, and with the theory side of
each layer (Law of One, Radin, Lloyd, Orch OR, Faggin/D'Ariano, Hoffman, Wendt, Haraway,
Bratton, Gibson, Kurzweil, extended mind) recorded.

They deliberately do NOT constrain mechanics. AGENTS.md §1/§4 make inventing rules out of
scope, and #78 defines an ontology rather than a mechanic, so a test here may never require
a statistic, a dice procedure or a power. What is protected:

* the four layers exist, are named, and each carries its core question;
* Luhmann's baseline is separated from the NoöPunk extensions, and Cybernetic is never
  attributed to Luhmann;
* Physical explicitly replaces Biological, and no separate Linguistic layer is created;
* the Psychic layer's theoretical background and its speculative framing are present and
  labelled as not established science;
* the Social and Cybernetic inspirations are present;
* the structural-coupling and simulation-representation tables exist;
* the section adds no mechanics, statistics or concrete dates.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

RULEBOOK = "RULEBOOK.md"

_YEAR_RE = re.compile(r"\b20[3-9]\d\b")


def read() -> str:
    return (ROOT / RULEBOOK).read_text(encoding="utf-8")


#: The ontology section, anchored by its stable heading text rather than a section
#: number. Section numbers are reused by later commits (the glossary took 34 once
#: already), so keying on the number is what let a clobber read as "content moved".
ONTOLOGY_HEADING = "The four NoöPunk systems"


def section() -> str:
    """The raw body of the four-layer ontology section, or "" if it is missing."""
    text = read()
    match = re.search(
        rf"(?ms)^##\s+\d+\.\s+[^\n]*{re.escape(ONTOLOGY_HEADING)}[^\n]*\n(.*?)(?=^##\s+\d+\.|\Z)",
        text,
    )
    return match.group(1) if match else ""


def flat() -> str:
    """Emphasis-stripped, whitespace-collapsed, lowercased §34 body."""
    text = re.sub(r"[>*_`]", " ", section())
    return " ".join(text.split()).lower()


class FourLayerOntologyRecordedTests(unittest.TestCase):
    def test_the_section_exists_and_names_all_four_layers(self) -> None:
        self.assertIn(ONTOLOGY_HEADING, read())
        text = flat()
        for layer in ("physical", "psychic", "social", "cybernetic"):
            with self.subTest(layer=layer):
                self.assertIn(layer, text)

    def test_each_layer_has_a_core_question(self) -> None:
        text = section()
        for heading in ("#### 36.2.1 Physical", "#### 36.2.2 Psychic",
                        "#### 36.2.3 Social", "#### 36.2.4 Cybernetic"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        self.assertEqual(text.count("**Core question:**"), 4,
                         "each of the four layers must state its core question")

    def test_physical_replaces_biological_for_the_setting(self) -> None:
        text = flat()
        self.assertRegex(text, r"physical instead of biological")
        self.assertRegex(text, r"not make .{0,40}biological.{0,40}fundamental layer")
        self.assertIn("does not claim that luhmann made the substitution", text)

    def test_cybernetic_is_the_noopunk_extension_not_luhmanns(self) -> None:
        text = flat()
        self.assertRegex(text, r"noöpunk theoretical extension|noopunk theoretical extension")
        self.assertRegex(text, r"not something luhmann claimed|not attributed to luhmann")
        self.assertIn("luhmann did not treat computer systems", text)

    def test_no_separate_linguistic_layer_is_created(self) -> None:
        text = flat()
        self.assertIn("no separate linguistic layer", text)
        self.assertIn("do not create a separate linguistic layer", text)
        # ...and language is explicitly placed inside Social, not beside it
        social = flat().split("36.2.3 social", 1)[1].split("36.2.4 cybernetic", 1)[0]
        self.assertIn("language", social)


class PsychicLayerTheoryTests(unittest.TestCase):
    def test_law_of_one_fourth_density_cosmology_is_present(self) -> None:
        text = flat()
        for concept in ("fourth density", "social memory complex", "service to others",
                        "service to self", "council of saturn", "law of one"):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_psi_is_natural_and_not_viral(self) -> None:
        text = flat()
        self.assertRegex(text, r"not produced by an alien virus|not caused by an alien virus")

    def test_psi_is_a_professional_service_with_ubik(self) -> None:
        text = flat()
        self.assertIn("professional service", text)
        self.assertIn("ubik", text)

    def test_psi_and_magic_are_overlapping_vocabularies(self) -> None:
        text = flat()
        self.assertIn("different cultural vocabularies", text)
        self.assertIn("magic", text)

    def test_the_quantum_consciousness_background_is_named(self) -> None:
        text = flat()
        for author in ("lloyd", "penrose", "hameroff", "orch or", "faggin",
                       "d'ariano", "hoffman", "wendt", "radin"):
            with self.subTest(author=author):
                self.assertIn(author, text)
        self.assertIn("quantum information panpsychism", text)
        self.assertIn("conscious realism", text)

    def test_radin_entangled_minds_is_the_psi_bridge(self) -> None:
        self.assertIn("Entangled Minds", read())

    def test_the_speculative_layer_is_labelled_not_established_science(self) -> None:
        text = flat()
        self.assertRegex(
            text,
            r"not as established science|not a statement of established science|"
            r"precursor theor",
        )


class SocialAndCyberneticLayerTests(unittest.TestCase):
    def test_social_is_luhmannian_communication(self) -> None:
        text = flat()
        self.assertRegex(text, r"consist of communication|constituted by communication")

    def test_social_combines_luhmann_and_castells(self) -> None:
        text = flat()
        self.assertIn("castells", text)
        self.assertIn("networks and flows", text)

    def test_cybernetic_names_haraway_bratton_gibson_kurzweil(self) -> None:
        text = flat()
        for name in ("haraway", "cyborg manifesto", "bratton", "the stack",
                     "gibson", "kurzweil"):
            with self.subTest(name=name):
                self.assertIn(name, text)

    def test_mesh_insert_cranial_computer_muse_are_default(self) -> None:
        text = flat()
        for device in ("mesh insert", "cranial computer", "muse"):
            with self.subTest(device=device):
                self.assertIn(device, text)

    def test_collective_intelligence_and_extended_mind(self) -> None:
        text = flat()
        self.assertIn("human + llm + language + internet", text)
        self.assertIn("more important than raw computational scale", text)
        self.assertIn("extended mind", text)


class CrossLayerTests(unittest.TestCase):
    def test_structural_coupling_table_exists(self) -> None:
        text = flat()
        for coupling in ("physical ↔ psychic", "psychic ↔ social",
                         "social ↔ cybernetic", "psychic ↔ psychic"):
            with self.subTest(coupling=coupling):
                self.assertIn(coupling, text)
        self.assertIn("all four", text)

    def test_simulation_representations_are_tabulated(self) -> None:
        text = flat()
        for phrase in ("spatial map", "social / rhizomatic graph",
                       "entanglement graph or hypergraph", "autonomous software agents"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_psychic_layer_does_not_use_physical_distance(self) -> None:
        text = flat()
        self.assertRegex(
            text,
            r"not use physical distance as its fundamental metric|rather than kilometres",
        )


class AntiInventionTests(unittest.TestCase):
    """#78 records an ontology; it must not author mechanics or statistics."""

    def test_the_section_declares_it_adds_no_mechanics(self) -> None:
        text = flat()
        self.assertIn("defines no statistics", text)
        self.assertIn("adds no mechanics", text)

    def test_the_section_invents_no_dice_or_statistics(self) -> None:
        """The ONTOLOGY invents no mechanics -- excluding the status subsection.

        §35.10 is a status note recording what the separate #74 prototype does
        ("deterministic Python owns mechanics and state: legal actions, ratings,
        dice, modifiers..."). That sentence *describes* the prototype's scope; it
        is not the ontology authoring a statistic, which is what this guard is
        for. Forbidding the word anywhere in §34 therefore failed on text that
        obeys the rule, so the check is scoped to the ontology itself and §35.10
        is excluded by name.
        """
        body = section()
        marker = re.search(r"(?m)^#{3,4} 36\.10", body)
        ontology = body[: marker.start()] if marker else body
        text = " ".join(re.sub(r"[>*_`]", " ", ontology).split()).lower()
        for mechanic in ("2d6", "dice", "initiative", "hit point", "armour", "armor"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, text)
        # and the exclusion must stay meaningful: the prototype note is still there
        self.assertRegex(
            body,
            r"(?m)^#{3,4} 36\.10",
            "the §35.10 status subsection this exclusion names has moved or been removed",
        )

    def test_no_concrete_future_dates(self) -> None:
        offenders = [m.group(0) for m in _YEAR_RE.finditer(section())]
        self.assertEqual(offenders, [], f"§34 assigns concrete years: {offenders}")

    def test_it_points_at_the_modular_worldbook_chapters(self) -> None:
        text = read()
        for chapter in ("3_PHYSICAL.md", "4_SOCIAL.md", "5_CYBERNETIC.md", "6_PSYCHIC.md"):
            with self.subTest(chapter=chapter):
                self.assertIn(chapter, text)


if __name__ == "__main__":
    unittest.main()
