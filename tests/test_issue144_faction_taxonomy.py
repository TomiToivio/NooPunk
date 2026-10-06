"""Guard for the faction-taxonomy half of issue #144.

Issue #144 landed in two parts. The UNSA rename and the Character Generation chapter merged
first (§§38-39 and Chapter 9, PR #146). What this guard protects is the part that did **not**
land with them and is easy to lose again: the **faction-model** half of the issue — the types
the faction machinery can represent, the generic faction schema, and the strict separation of
an NHI's ontology (type) from its politics (faction).

Anchored on heading text and exact phrases, never a bare ``## N.``, because the rulebook
carries two numbering namespaces split at the ``# Extended canon`` H1.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_HEADING = "43. Faction taxonomy, schema, and NHI type vs faction (#144)"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def flat(relative: str) -> str:
    return " ".join(re.sub(r"[*`>]", " ", read(relative)).split()).lower()


def chapter() -> str:
    """Lowercased, flattened whole of RULEBOOK.md §43 (its `##` down to the next `##`).

    A subsection extractor is wrong here: §43.1's prose and §43.2's type table live in
    different `###` blocks, so a per-subsection read would miss half the taxonomy.
    """
    text = read("RULEBOOK.md")
    match = re.search(rf"(?m)^## {re.escape(TAXONOMY_HEADING)}\s*$", text)
    if match is None:
        return ""
    rest = text[match.end():]
    nxt = re.search(r"(?m)^## ", rest)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(re.sub(r"[*`>]", " ", body).split()).lower()


def section(heading: str) -> str:
    """Lowercased, flattened body of a `##`/`###` section of RULEBOOK.md, by heading text."""
    text = read("RULEBOOK.md")
    match = re.search(rf"(?m)^#{{2,3}} {re.escape(heading)}\s*$", text)
    if match is None:
        return ""
    rest = text[match.end():]
    nxt = re.search(r"(?m)^#{2,3} ", rest)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(re.sub(r"[*`>]", " ", body).split()).lower()


class TaxonomySectionTests(unittest.TestCase):
    def test_the_taxonomy_section_exists(self) -> None:
        self.assertTrue(chapter(),
                        f"RULEBOOK.md no longer has the {TAXONOMY_HEADING!r} section")

    def test_every_faction_type_is_named(self) -> None:
        body = flat("RULEBOOK.md")
        for kind in ("political", "criminal", "civil society and knowledge",
                     "religious and esoteric", "corporate", "governmental", "nhi"):
            with self.subTest(kind=kind):
                self.assertIn(kind, body)

    def test_the_governmental_scale_field_is_documented(self) -> None:
        body = chapter()
        for scale in ("local", "regional", "nation-state", "supranational",
                      "global / planetary"):
            with self.subTest(scale=scale):
                self.assertIn(scale, body)

    def test_the_generic_faction_schema_is_documented(self) -> None:
        body = chapter()
        for field in ("name", "faction type", "scale", "members / constituents",
                      "ideology", "allies", "enemies", "parent faction", "subfactions"):
            with self.subTest(field=field):
                self.assertIn(field, body)

    def test_faction_is_the_umbrella_concept(self) -> None:
        self.assertIn("umbrella gameplay concept", chapter())


class NhiTypeVsFactionTests(unittest.TestCase):
    def test_the_split_is_stated(self) -> None:
        body = section("43.4 NHI type vs NHI faction")
        self.assertIn("does not determine its political allegiance", body)

    def test_the_four_core_types(self) -> None:
        body = section("43.4 NHI type vs NHI faction")
        for core in ("biologics", "constructs", "plasmoids", "noetics"):
            with self.subTest(core=core):
                self.assertIn(core, body)

    def test_the_extended_descriptors(self) -> None:
        body = section("43.4 NHI type vs NHI faction")
        for descriptor in ("process intelligences", "ecologies", "assemblages",
                           "collectives", "geotics", "hybrids", "anomalies"):
            with self.subTest(descriptor=descriptor):
                self.assertIn(descriptor, body)

    def test_process_intelligence_is_flagged_as_the_formal_class_candidate(self) -> None:
        self.assertIn("strongest candidate for an additional formal class",
                      section("43.4 NHI type vs NHI faction"))


class MachineReadableTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = json.loads(read("data/world/faction_taxonomy.json"))

    def test_the_model_names_the_types(self) -> None:
        ids = {entry["id"] for entry in self.model["faction_types"]}
        self.assertEqual(ids, {"political", "criminal", "civil_society_knowledge",
                               "religious_esoteric", "corporate", "governmental", "nhi"})

    def test_the_model_separates_type_from_allegiance(self) -> None:
        self.assertTrue(self.model["rules"]["type_does_not_determine_political_allegiance"])

    def test_the_model_records_the_nhi_core_types_and_descriptors(self) -> None:
        nhi = self.model["nhi_types"]
        self.assertEqual(nhi["core"], ["Biologics", "Constructs", "Plasmoids", "Noetics"])
        ids = {entry["id"] for entry in nhi["extended_descriptors"]}
        self.assertIn("process_intelligences", ids)
        self.assertIn("geotics", ids)

    def test_the_campaign_scope_rule_is_recorded(self) -> None:
        self.assertIn("Helsinki-relevant", self.model["rules"]["default_campaign_scope"])


if __name__ == "__main__":
    unittest.main()
