"""Structure guard for issue #144: faction taxonomy, −10…+10, UNSA, and Character Generation.

The issue does several separable things, so the guards are grouped the same way:

* the faction **taxonomy** exists as an expandable type list, and the campaign-scope rule that
  it must NOT become a pre-populated global catalogue is stated;
* NHI **ontology is separated from NHI faction politics**;
* the generic faction **schema**, multi-faction **membership**, and the **10-point** starting
  Reputation rule (employer granted separately) are recorded;
* social scores are **−10…+10** consistently across rulebook, chapter, schema and runtime;
* the default campaign institution is **UNSA**, with Firewall recorded as Eclipse Phase's
  organization rather than an in-world name;
* the **Character Generation** chapter exists with the Lifepath framework, the four specialist
  academies, and the explicit deferral of the random tables.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"
CHAPTER = ROOT / "rulebook" / "8_FACTIONS.md"
FACTIONS = ROOT / "FACTIONS.md"
SCHEMA = ROOT / "data" / "world" / "social_affect_schema.json"
AFFECT = ROOT / "src" / "simulation" / "affect.py"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def flat(p: Path) -> str:
    """Whitespace-collapsed, markdown-structural markers removed.

    Both rulebook and chapter are hard-wrapped, so a phrase that reads as one string is often
    split across a newline; a raw substring assertion then fails against correct content.
    """
    return " ".join(re.sub(r"[*`>]", " ", read(p)).split()).lower()


class FactionTaxonomyTests(unittest.TestCase):
    def test_the_seven_faction_types_are_defined(self) -> None:
        """Assert the numbered type HEADINGS, not a keyword that occurs elsewhere.

        "Religious" also appears in the worked-classification examples and "corporate"
        in prose, so a bare keyword check passed with the type heading deleted.
        """
        text = " ".join(re.sub(r"[*`>]", " ", read(CHAPTER)).split()).lower()
        for number, title in ((1, "political"), (2, "criminal"),
                              (3, "civil society and knowledge"), (4, "religious and esoteric"),
                              (5, "corporate"), (6, "governmental"),
                              (7, "nhi: type is not faction")):
            with self.subTest(faction_type=number):
                self.assertRegex(
                    text, rf"\b{number}\. {re.escape(title)}",
                    f"faction type {number} ({title}) heading is missing",
                )

    def test_government_uses_a_scale_field_not_a_second_system(self) -> None:
        text = flat(CHAPTER)
        for scale in ("local", "regional", "nation-state", "supranational", "planetary"):
            with self.subTest(scale=scale):
                self.assertIn(scale, text)

    def test_the_taxonomy_is_expandable_and_not_a_global_catalogue(self) -> None:
        """The issue is explicit: do not pre-populate the rulebook with dozens of factions."""
        text = flat(CHAPTER)
        self.assertIn("campaign scope", text)
        self.assertIn("added when a scenario, campaign arc or supplement needs them", text)
        self.assertRegex(text, r"not pre-populated here")


class NhiTypeIsNotFactionTests(unittest.TestCase):
    def test_the_separation_is_stated(self) -> None:
        text = flat(CHAPTER)
        self.assertIn(
            "nhi ontology and nhi politics are separate fields", text,
            "the chapter must separate NHI ontology from NHI faction politics",
        )

    def test_the_core_types_are_named(self) -> None:
        text = flat(CHAPTER)
        for core in ("biologics", "constructs", "plasmoids", "noetics"):
            with self.subTest(nhi_type=core):
                self.assertIn(core, text)

    def test_the_extended_descriptors_are_named(self) -> None:
        text = flat(CHAPTER)
        for descriptor in ("process intelligence", "ecologie", "assemblage",
                           "collective", "geotic", "hybrid", "anomal"):
            with self.subTest(descriptor=descriptor):
                self.assertIn(descriptor, text)


class FactionSchemaTests(unittest.TestCase):
    def test_the_generic_schema_fields_are_recorded(self) -> None:
        text = flat(CHAPTER)
        for field in ("name", "faction type", "scale", "ideology", "motivations",
                      "reputation", "contacts", "allies", "enemies",
                      "network position", "parent faction", "subfactions", "tags"):
            with self.subTest(field=field):
                self.assertIn(field, text)

    def test_multiple_faction_membership_is_explicit(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("belong to several factions", text)
        self.assertIn("membership is not ideological loyalty", text)
        self.assertIn("starting reputation allocation", text)

    def test_factions_states_the_multi_faction_rule_too(self) -> None:
        """Scope to the #144 paragraph: "belong to several" occurs twice in this file, so a
        document-wide check passed after the #144 sentence was deleted."""
        body = read(FACTIONS)
        start = body.find("This is one instance of the general rule")
        self.assertGreater(start, 0, "FACTIONS.md lost the #144 multi-faction paragraph")
        para = " ".join(body[start:start + 700].split()).lower()
        self.assertIn("may belong to several factions", para)
        self.assertIn("10 starting reputation points", para)
        self.assertIn("rulebook/8_factions.md", para)


class StartingReputationTests(unittest.TestCase):
    def test_the_ten_point_rule_is_recorded(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("10 positive reputation points", text)
        self.assertRegex(text, r"two or three factions")

    def test_the_canonical_examples_are_present(self) -> None:
        text = flat(CHAPTER)
        for example in ("6 / 4", "5 / 3 / 2"):
            with self.subTest(example=example):
                self.assertIn(example, text)

    def test_the_employer_is_granted_separately(self) -> None:
        text = flat(CHAPTER)
        self.assertRegex(text, r"granted separately|granted by the campaign template")

    def test_negative_reputation_is_not_bought_from_the_pool(self) -> None:
        text = flat(CHAPTER)
        self.assertRegex(text, r"negative reputation is not bought")


class ScaleIsResolvedTests(unittest.TestCase):
    """#144 resolves the scale #122 recorded as open, across all four places."""

    def test_the_chapter_states_the_resolved_one_scale(self) -> None:
        text = flat(CHAPTER)
        self.assertIn("−10…+10", text)
        self.assertIn("(resolved)", text)

    def test_the_rulebook_uses_the_resolved_scale(self) -> None:
        text = read(RULEBOOK)
        self.assertIn("-10 to +10", text)
        self.assertNotRegex(text, r"-100\s+to\s+\+100")

    def test_the_schema_and_runtime_agree(self) -> None:
        self.assertEqual(json.loads(read(SCHEMA))["score_range"], [-10, 10])
        affect = read(AFFECT)
        # \b matters: "MIN_AFFECT = -10" is a substring of "MIN_AFFECT = -100", so a plain
        # assertIn passed after the bound was reverted.
        self.assertRegex(affect, r"MIN_AFFECT\s*=\s*-10\b")
        self.assertRegex(affect, r"MAX_AFFECT\s*=\s*10\b")
        self.assertNotRegex(affect, r"MIN_AFFECT\s*=\s*-100\b")

    def test_affect_remains_available_for_specific_semantics(self) -> None:
        text = flat(CHAPTER)
        self.assertRegex(text, r"affect override|label carries the meaning")


class UnsanNamingTests(unittest.TestCase):
    def test_unsa_is_defined_with_its_full_name(self) -> None:
        text = flat(RULEBOOK)
        self.assertIn("united nations security agency (unsa)", text)

    def test_firewall_is_ep2_provenance_not_an_in_world_name(self) -> None:
        """The issue: Firewall may be acknowledged as inspiration, not as a faction name."""
        text = flat(RULEBOOK)
        self.assertRegex(text, r"firewall.*is eclipse phase's organization|"
                               r"\*firewall\* is eclipse phase")
        self.assertRegex(text, r"not\*{0,2} an in-world")

    def test_the_mj12_exception_is_stated(self) -> None:
        text = flat(RULEBOOK)
        self.assertRegex(text, r"mj-12.*not a tolerated nickname|"
                               r"\"mj-12\" is not a tolerated nickname")

    def test_the_tolerated_nicknames_are_recorded(self) -> None:
        text = flat(RULEBOOK)
        for nick in ("x-com", "x-files", "men in black"):
            with self.subTest(nickname=nick):
                self.assertIn(nick, text)

    def test_the_early_labels_are_recorded(self) -> None:
        text = flat(RULEBOOK)
        self.assertIn("un x-risk agency", text)
        self.assertIn("un nhi agency", text)

    def test_the_integration_chain_is_present(self) -> None:
        text = flat(RULEBOOK)
        for actor in ("suojelupoliisi", "europol", "unsa"):
            with self.subTest(actor=actor):
                self.assertIn(actor, text)


class DisclosureForkTests(unittest.TestCase):
    def test_both_outcomes_are_stated_as_simultaneous(self) -> None:
        text = flat(RULEBOOK)
        self.assertRegex(text, r"simultaneously|both outcomes happen")
        self.assertRegex(text, r"does not choose between them|both happen")

    def test_the_fragmentation_includes_psi_manipulation(self) -> None:
        text = flat(RULEBOOK)
        self.assertRegex(text, r"psi for influence|psi .{0,40}manipulation")

    def test_unification_is_an_emergency_response(self) -> None:
        text = flat(RULEBOOK)
        self.assertRegex(text, r"emergency|panic, war, institutional collapse")

    def test_wendt_is_named(self) -> None:
        self.assertIn("wendt", flat(RULEBOOK))


class CharacterGenerationTests(unittest.TestCase):
    def test_the_chapter_exists(self) -> None:
        text = read(RULEBOOK)
        self.assertIn("## 43. Character Generation", text)

    def test_manual_random_or_mixed_is_stated(self) -> None:
        text = flat(RULEBOOK)
        self.assertRegex(text, r"manual choice, randomization, or a mix")

    def test_the_academies_are_named(self) -> None:
        text = flat(RULEBOOK)
        for academy in ("unsa police academy", "swat academy", "psi academy",
                        "tech academy", "nhi academy"):
            with self.subTest(academy=academy):
                self.assertIn(academy, text)

    def test_the_lifepath_stages_run_to_the_end(self) -> None:
        text = flat(RULEBOOK)
        for stage in ("origin", "family", "education", "motivations",
                      "rivals", "specialist academy", "final character summary"):
            with self.subTest(stage=stage):
                self.assertIn(stage, text)

    def test_the_random_tables_are_deferred(self) -> None:
        """The issue forbids overbuilding the tables in this pass."""
        text = flat(RULEBOOK)
        self.assertIn("building out every random table is not", text,
                      "the chapter must state that building the random tables is not its job")
        self.assertIn("establishing the framework is this chapter's job", text)
        for claim in ("random tables are complete", "all random tables are done",
                      "tables are provided in full"):
            with self.subTest(claim=claim):
                self.assertNotIn(claim, text)

    def test_alternative_campaigns_remain_possible(self) -> None:
        text = flat(RULEBOOK)
        self.assertIn("alternative campaign structures", text)

    def test_it_defines_no_new_mechanics(self) -> None:
        """The chapter must not *define* mechanics — but it legitimately NAMES the systems it
        leaves deferred ("does not define advancement or XP"), so a bare keyword ban would
        fail on correct text. Assert instead that the deferral wording is present and that no
        numeric mechanic is stated.
        """
        body = read(RULEBOOK)
        start = body.find("## 43. Character Generation")
        assert start > 0
        chapter = " ".join(body[start:].split()).lower()
        self.assertRegex(chapter, r"deliberately does \*\*not\*\*|does not:")
        for forbidden in ("hit points", "damage track", "initiative order"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, chapter)
        # no dice formula and no target numbers
        self.assertNotRegex(chapter, r"\b\d+d\d+\b")
        self.assertNotRegex(chapter, r"difficulty value of \d")

    def test_the_ledger_numbering_stays_contiguous(self) -> None:
        """A new top-level section must not open a gap in the compatibility ledger."""
        core, appendix = read(RULEBOOK).split("# Extended canon and reference material", 1)
        core_numbers = [int(n) for n in re.findall(r"(?m)^## (\d+)\.", core)]
        ledger_numbers = [int(n) for n in re.findall(r"(?m)^## (\d+)\.", appendix)]
        self.assertEqual(core_numbers, list(range(1, 9)))
        self.assertEqual(ledger_numbers, list(range(1, max(ledger_numbers) + 1)))


if __name__ == "__main__":
    unittest.main()
