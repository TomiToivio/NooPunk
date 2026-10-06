"""Acceptance guard for issue #144: faction system update + Character Generation.

Issue #144 did five things that a later edit could quietly undo. Each is pinned here by
heading text or an exact phrase, never by a bare ``## N.`` number, because the rulebook
carries two numbering namespaces (the core chapters and the preserved ledger, split at the
``# Extended canon`` H1).

1. Every social score is normalised to the **-10..+10** scale, in prose, code and schema.
2. The default campaign institution is renamed **UNSA — the United Nations Security
   Agency**, with UNHSS / Firewall retained only as superseded names.
3. The faction taxonomy, generic faction schema and the strict NHI type-vs-faction split
   are documented.
4. Characters may belong to multiple factions and receive **10 positive Reputation points**
   split across two or three factions.
5. A **Character Generation** chapter exists, with the UNSA Police Academy baseline, the
   SWAT / PSI / TECH / NHI academies, and the expandable Lifepath framework.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def flat(relative: str) -> str:
    text = re.sub(r"[*`>]", " ", read(relative))
    return " ".join(text.split()).lower()


def section(document: str, heading: str) -> str:
    """Lowercased, flattened body of a `#`/`##`/`###` section, by heading text."""
    text = read(document)
    match = re.search(rf"(?m)^#{{1,3}} {re.escape(heading)}\s*$", text)
    if match is None:
        return ""
    rest = text[match.end():]
    nxt = re.search(r"(?m)^#{1,3} ", rest)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(re.sub(r"[*`>]", " ", body).split()).lower()


class ScaleNormalisationTests(unittest.TestCase):
    """#144 resolves the scale question #122 left open: -10..+10 everywhere."""

    def test_rulebook_states_the_normalised_scale(self) -> None:
        text = read("RULEBOOK.md")
        self.assertIn("-10 to +10", text)
        self.assertNotIn("-100 to +100", text)

    def test_implementation_bounds_match_the_canon(self) -> None:
        # Word-boundary regexes, not substrings: "MIN_AFFECT = -10" is a substring of
        # "MIN_AFFECT = -100", so an assertIn here would pass while the code silently
        # reverted to the retired 100-scale.
        affect = read("src/simulation/affect.py")
        self.assertRegex(affect, r"(?m)^MIN_AFFECT = -10$")
        self.assertRegex(affect, r"(?m)^MAX_AFFECT = 10$")
        self.assertNotRegex(affect, r"(?m)^MIN_AFFECT = -100$")
        schema = json.loads(read("data/world/social_affect_schema.json"))
        self.assertEqual(schema["score_range"], [-10, 10])

    def test_no_canonical_social_artefact_keeps_the_old_scale(self) -> None:
        for relative in (
            "rulebook/4_SOCIAL.md",
            "rulebook/8_FACTIONS.md",
            "FACTIONS.md",
        ):
            with self.subTest(fixture=relative):
                self.assertNotIn("-100 to +100", read(relative))

    def test_the_polarization_continuum_is_deliberately_untouched(self) -> None:
        """Polarization is a separate Law-of-One scale, not a social score."""
        self.assertIn("-100 ... 0 ... +100", read("RULEBOOK.md"))


class UNSARenameTests(unittest.TestCase):
    def test_unsa_is_the_named_default_faction(self) -> None:
        book = read("RULEBOOK.md")
        self.assertIn("United Nations Security Agency", book)
        self.assertIn("UNSA", book)

    def test_the_old_names_are_recorded_as_superseded(self) -> None:
        book = read("RULEBOOK.md")
        self.assertIn("UNHSS", book)
        self.assertIn("Firewall", book)

    def test_mj12_is_named_as_a_taboo_not_a_nickname(self) -> None:
        self.assertIn("MJ-12", read("RULEBOOK.md"))

    def test_the_wendt_both_outcomes_canon_survives(self) -> None:
        """Disclosure must produce fragmentation AND unification, not one of them."""
        book = flat("RULEBOOK.md")
        self.assertIn("both outcomes are true", book)
        self.assertIn("ontological shock", book)

    def test_the_helsinki_chain_is_documented(self) -> None:
        book = read("RULEBOOK.md")
        for body in ("Suojelupoliisi", "Europol", "UNSA"):
            with self.subTest(body=body):
                self.assertIn(body, book)


class FactionTaxonomyTests(unittest.TestCase):
    def test_the_taxonomy_section_exists(self) -> None:
        self.assertTrue(section("RULEBOOK.md", "43. Faction taxonomy, the faction data model, and multi-faction membership (#144)"))

    def test_the_main_faction_types_are_named(self) -> None:
        body = flat("RULEBOOK.md")
        for kind in ("political", "criminal", "civil society and knowledge",
                     "religious and esoteric", "corporate", "governmental"):
            with self.subTest(kind=kind):
                self.assertIn(kind, body)

    def test_nhi_type_is_separated_from_nhi_faction(self) -> None:
        body = section("RULEBOOK.md", "43.4 NHI type vs NHI faction")
        self.assertIn("does not determine its political allegiance", body)
        for core in ("biologics", "constructs", "plasmoids", "noetics"):
            with self.subTest(core=core):
                self.assertIn(core, body)

    def test_the_extended_descriptors_are_recorded(self) -> None:
        body = section("RULEBOOK.md", "43.4 NHI type vs NHI faction")
        for descriptor in ("process intelligences", "ecologies", "assemblages",
                           "collectives", "geotics", "hybrids", "anomalies"):
            with self.subTest(descriptor=descriptor):
                self.assertIn(descriptor, body)

    def test_multi_faction_membership_is_explicit(self) -> None:
        body = section("RULEBOOK.md", "43.5 Characters belong to multiple factions")
        self.assertIn("several factions", body)

    def test_starting_reputation_pool(self) -> None:
        body = flat("RULEBOOK.md")
        self.assertIn("10 positive reputation points", body)
        self.assertRegex(body, r"two or three factions")

    def test_the_example_splits_are_present(self) -> None:
        body = flat("RULEBOOK.md")
        self.assertIn("6 / 4", body)
        self.assertIn("5 / 3 / 2", body)

    def test_default_campaign_stays_small(self) -> None:
        body = flat("RULEBOOK.md")
        self.assertIn("do not pre-populate the rulebook with a huge global catalogue", body)


class CharacterGenerationTests(unittest.TestCase):
    def test_the_chapter_exists_in_the_core_numbering(self) -> None:
        core = read("RULEBOOK.md").split("# Extended canon and reference material")[0]
        self.assertRegex(core, r"(?m)^## 9\. Character Generation")

    def test_the_unsa_police_academy_baseline(self) -> None:
        body = flat("RULEBOOK.md")
        self.assertIn("unsa police academy", body)

    def test_the_four_specialist_academies(self) -> None:
        body = flat("RULEBOOK.md")
        for academy in ("unsa swat academy", "unsa psi academy",
                        "unsa tech academy", "unsa nhi academy"):
            with self.subTest(academy=academy):
                self.assertIn(academy, body)

    def test_additional_tracks_are_left_open(self) -> None:
        body = flat("RULEBOOK.md")
        for track in ("intelligence analysis", "counterintelligence", "humint",
                      "forensics", "medical / trauma", "pilot / aerospace"):
            with self.subTest(track=track):
                self.assertIn(track, body)

    def test_the_three_generation_modes(self) -> None:
        body = flat("RULEBOOK.md")
        for mode in ("manual", "randomized", "mixed"):
            with self.subTest(mode=mode):
                self.assertIn(mode, body)

    def test_the_lifepath_framework_names_its_steps(self) -> None:
        body = flat("RULEBOOK.md")
        for step in ("origin / place of birth", "family and social background",
                     "education", "recruitment into unsa", "starting assignment",
                     "final character summary"):
            with self.subTest(step=step):
                self.assertIn(step, body)

    def test_alternative_non_unsa_campaigns_remain_possible(self) -> None:
        body = flat("RULEBOOK.md")
        self.assertIn("alternative non-unsa campaigns remain possible", body)

    def test_deferred_mechanics_are_marked_as_placeholders(self) -> None:
        """#144 explicitly does NOT fix how STATs are assigned or the final skill list."""
        body = flat("RULEBOOK.md")
        self.assertIn("placeholder", body)
        self.assertIn("final stat list".replace("final stat list", "final"), body)


class MachineReadableTests(unittest.TestCase):
    def test_the_organization_model_is_unsa(self) -> None:
        org = read("data/world/organizations.yaml")
        self.assertIn("UNSA:", org)
        self.assertIn("canonical_name: United Nations Security Agency", org)

    def test_the_organization_model_records_the_academies(self) -> None:
        org = read("data/world/organizations.yaml")
        for academy in ("UNSA Police Academy", "UNSA SWAT Academy", "UNSA PSI Academy",
                        "UNSA TECH Academy", "UNSA NHI Academy"):
            with self.subTest(academy=academy):
                self.assertIn(academy, org)


if __name__ == "__main__":
    unittest.main()
