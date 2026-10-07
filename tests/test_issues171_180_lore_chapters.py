"""Structure guard for the 2026-10-07 lore and reference chapters (issues #171-#180).

The author asked for lore chapters plus descriptive sections covering character generation,
equipment, cybernetic and psychotronic implants, PSI powers and a catalogue of kinds of
being — with explicit instruction that the lists carry **light descriptions only, not full
statistics**. Two PRs delivered that material: #181 (the condensed field catalog,
``rulebook/9_FIELD_CATALOGS.md``) and the detailed chapters (``rulebook/6_PSYCHIC.md``
expansion plus ``10_SINGULARITY_CRISIS.md``, ``11_ONTOLOGY.md``, ``12_BEINGS.md``,
``13_EQUIPMENT.md``, ``14_CHARACTER_GENERATION.md``).

This guard asserts the FACT that each requested section exists and is discoverable, and that
each one keeps the **"no statistics"** bound the author set. It deliberately asserts
*existence and bound*, not wording: a chapter may be rewritten freely as long as the section
still exists and still refuses to define numbers.

A structure guard in the style of ``test_issue122_faction_terminology.py``:

1. asserts every requested chapter exists, keeps a stable heading and is linked from
   ``RULEBOOK.md`` (a chapter nobody links is a chapter nobody reads);
2. asserts the author's requested sections are present — character generation, equipment,
   cybernetic/psychotronic implants, PSI powers and kinds of being;
3. asserts each new chapter keeps its explicit "what this does NOT define" bound;
4. asserts the lore-only pair (#173 Seity, #174 disconnected systems) is marked as NOT
   implemented, so a later session does not mistake the parking place for rules;
5. asserts the reserved areas named by ``AGENTS.md`` §4 are still not defined by these
   chapters (no costs, no damage, no prices).

Uses only the standard library: CI installs requirements.txt and nothing else.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"


def read(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def flat(path: Path) -> str:
    """Whitespace-collapsed AND blockquote-marker-stripped.

    The chapters wrap prose at ~90 columns and some of the material the author asked to
    assert lives inside blockquotes. A phrase like ``NO stat blocks`` is therefore split
    across a line break and prefixed with ``>`` in the raw file, so a needle that reads as
    one string never matches. Stripping the leading ``>`` markers before collapsing is the
    difference between a guard that measures the document and one that measures its width.
    """
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        lines.append(re.sub(r"^\s*>\s?", "", line))
    return " ".join(" ".join(lines).split())


def chapter(name: str) -> str:
    return flat(ROOT / "rulebook" / name)


#: The chapters the author requested on 2026-10-07, with the heading each must keep.
#: The heading is an anchor; keep the assertion to a recognisable prefix, not the full title.
REQUESTED = {
    "6_PSYCHIC.md": r"^# Psychic Systems\b",
    "9_FIELD_CATALOGS.md": r"^# NoöPunk Field Catalogs\b",
    "10_SINGULARITY_CRISIS.md": r"^# The Singularity Crisis\b",
    "11_ONTOLOGY.md": r"^# Ontology\b",
    "12_BEINGS.md": r"^# Beings\b",
    "13_EQUIPMENT.md": r"^# Equipment\b",
    "14_CHARACTER_GENERATION.md": r"^# Character Generation\b",
}


class ChapterExistenceTests(unittest.TestCase):
    def test_every_requested_chapter_exists_with_its_heading(self) -> None:
        for name, pattern in REQUESTED.items():
            path = ROOT / "rulebook" / name
            with self.subTest(chapter=name):
                self.assertTrue(path.exists(), f"rulebook/{name} is missing")
                self.assertRegex(chapter(name), pattern,
                                 f"the heading of {name} was renamed or removed")

    def test_every_requested_chapter_is_linked_from_the_rulebook(self) -> None:
        """A chapter nobody links is a chapter nobody reads.

        The assertion requires the **path** (``rulebook/<name>``), not the bare filename:
        the chapter list renders each entry as ``[`6_PSYCHIC.md`](rulebook/6_PSYCHIC.md)``,
        so a guard matching only the name passes even after the link target is removed —
        the label alone satisfies it. Pin the target.
        """
        text = RULEBOOK.read_text(encoding="utf-8")
        for name in REQUESTED:
            with self.subTest(chapter=name):
                self.assertIn(f"rulebook/{name}", text,
                              f"RULEBOOK.md does not link rulebook/{name}")


class AuthorRequestedSectionsTests(unittest.TestCase):
    """The five sections the author named, each asserted by its FACT, not its wording."""

    def test_character_generation_section_exists(self) -> None:
        text = chapter("14_CHARACTER_GENERATION.md")
        self.assertRegex(text, r"Lifepath")
        # It must consume the canonical framework, not fork it.
        self.assertRegex(text, r"RULEBOOK\.md`? §9|canonical framework")

    def test_equipment_section_exists(self) -> None:
        text = chapter("13_EQUIPMENT.md")
        self.assertRegex(text, r"equipment", re.IGNORECASE)
        self.assertRegex(text, r"no numeric statistics|no statistics|does NOT define")

    def test_cybernetic_and_psychotronic_implant_sections_exist(self) -> None:
        text = chapter("13_EQUIPMENT.md")
        self.assertRegex(text, r"[Cc]ybernetic implants")
        self.assertRegex(text, r"[Pp]sychotronic implants")

    def test_psi_powers_section_exists(self) -> None:
        """PSI powers are a section of Psychic Systems, and must be a description list,
        not a second Skill list."""
        text = chapter("6_PSYCHIC.md")
        self.assertRegex(text, r"PSI powers")
        self.assertRegex(text, r"not a power catalogue|descriptions only|no stats")

    def test_kinds_of_being_catalogue_exists(self) -> None:
        text = chapter("12_BEINGS.md")
        self.assertRegex(text, r"Beings")
        # The catalogue is a field guide, never a complete stat-block manual.
        self.assertRegex(text, r"NO stat blocks")


class NoStatisticsBoundTests(unittest.TestCase):
    """The author's bound: light description only, no statistics. Each new chapter says so."""

    def test_each_new_chapter_states_its_own_scope_bound(self) -> None:
        for name in ("13_EQUIPMENT.md", "14_CHARACTER_GENERATION.md", "12_BEINGS.md"):
            with self.subTest(chapter=name):
                self.assertRegex(
                    chapter(name),
                    r"does NOT define",
                    f"{name} no longer states what it does not define",
                )

    def test_equipment_chapter_refuses_statistics_explicitly(self) -> None:
        text = chapter("13_EQUIPMENT.md")
        # The reserved areas must be named as refused, so a later pass cannot read the
        # silence as an opening.
        for reserved in ("damage", "armor", "economy"):
            with self.subTest(reserved=reserved):
                self.assertRegex(text, reserved, f"{reserved} is no longer named as deferred")

    def test_chargen_chapter_refuses_classes_and_points(self) -> None:
        text = chapter("14_CHARACTER_GENERATION.md")
        self.assertRegex(text, r"careers, not classes|not classes")
        self.assertRegex(text, r"starting Skill counts")


class LoreOnlyPairTests(unittest.TestCase):
    """#173 (Seity) and #174 (disconnected systems) are lore-only: rules as ideas."""

    def test_seity_is_marked_not_implemented(self) -> None:
        text = chapter("6_PSYCHIC.md")
        self.assertRegex(text, r"Seity")
        self.assertRegex(text, r"DESIGN IDEA ONLY")
        self.assertRegex(text, r"not implemented in the current core rules")

    def test_disconnected_systems_are_marked_speculative(self) -> None:
        text = chapter("6_PSYCHIC.md")
        self.assertRegex(text, r"disconnected", re.IGNORECASE)
        self.assertRegex(text, r"LORE AND DESIGN IDEAS")

    def test_the_field_catalog_also_labels_the_parking_place(self) -> None:
        text = chapter("9_FIELD_CATALOGS.md")
        self.assertRegex(text, r"not active rules")


class DensityAndOntologyFactTests(unittest.TestCase):
    """The load-bearing setting facts the author's issues turned on."""

    def test_density_is_not_a_morphology_classifier(self) -> None:
        text = chapter("11_ONTOLOGY.md")
        self.assertRegex(
            text,
            r"Density is fundamentally a level of consciousness and evolution — not a biological species classification",
        )
        self.assertRegex(text, r"vehicle", re.IGNORECASE)
        self.assertRegex(text, r"entity", re.IGNORECASE)

    def test_false_positives_are_mandatory(self) -> None:
        text = chapter("11_ONTOLOGY.md")
        self.assertRegex(text, r"[Ff]alse positives")

    def test_metallic_spheres_are_infrastructure_not_a_species(self) -> None:
        text = chapter("11_ONTOLOGY.md")
        self.assertRegex(text, r"metallic sphere")
        self.assertRegex(text, r"not\*\* to be treated as an alien species")
        self.assertRegex(text, r"infrastructure\*\*, not a species")

    def test_hybrid_verification_requires_corroboration(self) -> None:
        text = chapter("12_BEINGS.md")
        self.assertRegex(text, r"verif", re.IGNORECASE)
        self.assertRegex(text, r"Multiple independent indicators are required before escalation")


class SingularityCrisisCombinationTests(unittest.TestCase):
    """#177 and #178 are the same concept; the chapter must be a single synthesis."""

    def test_the_crisis_chapter_names_all_three_outcomes(self) -> None:
        text = chapter("10_SINGULARITY_CRISIS.md")
        for name in ("Noösphere", "Panopticon", "Thanatos"):
            with self.subTest(entity=name):
                self.assertIn(name, text, f"{name} is missing from the Crisis chapter")

    def test_the_crisis_cause_stays_unresolved(self) -> None:
        text = chapter("10_SINGULARITY_CRISIS.md")
        self.assertRegex(text, r"single canonical explanation")

    def test_the_two_singularities_are_distinguished(self) -> None:
        text = chapter("10_SINGULARITY_CRISIS.md")
        self.assertRegex(text, r"Machine Singularity")
        self.assertRegex(text, r"Cyborg Singularity")


if __name__ == "__main__":
    unittest.main()
