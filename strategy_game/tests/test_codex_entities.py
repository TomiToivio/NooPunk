"""Runtime contracts for the codex entity records (issue #348).

Executable behaviour only: record shape, the two independent axes, lookup, the player-facing
projection and serialization. Per ``AGENTS.md`` there is **no** assertion about entity prose, canon,
lore or wording — the codex *content* is author-reviewed material. The only content the tests touch is
the shipped data file's *structure*, because loading it is code behaviour.

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game.codex import (  # noqa: E402
    CODEX_PATH,
    Codex,
    CodexError,
    EntityForm,
    EntityOntology,
    EntityRecord,
    KnowledgeStatus,
    load_codex,
)


def _record(identifier: str = "e1", **kwargs: Any) -> EntityRecord:
    payload: dict[str, Any] = {"display_name": f"Entity {identifier}"}
    payload.update(kwargs)
    return EntityRecord(identifier=identifier, **payload)


class EntityRecordTests(unittest.TestCase):
    def test_a_record_needs_identity(self):
        with self.assertRaises(CodexError):
            EntityRecord(identifier="", display_name="x")
        with self.assertRaises(CodexError):
            EntityRecord(identifier="e1", display_name="  ")

    def test_the_two_axes_must_be_enum_members(self):
        with self.assertRaises(CodexError):
            _record(ontology="biologic")  # type: ignore[arg-type]
        with self.assertRaises(CodexError):
            _record(form="species")  # type: ignore[arg-type]
        with self.assertRaises(CodexError):
            _record(knowledge_status="gm_truth")  # type: ignore[arg-type]

    def test_the_primary_ontology_cannot_also_be_an_alternative(self):
        with self.assertRaises(CodexError):
            _record(ontology=EntityOntology.NOETIC,
                    alternative_ontologies=(EntityOntology.NOETIC,))

    def test_hypotheses_put_the_primary_first(self):
        record = _record(ontology=EntityOntology.PLASMOID,
                         alternative_ontologies=(EntityOntology.CONSTRUCT, EntityOntology.NOETIC))
        self.assertEqual(record.hypotheses,
                         (EntityOntology.PLASMOID, EntityOntology.CONSTRUCT, EntityOntology.NOETIC))
        self.assertTrue(record.is_contested)

    def test_a_settled_record_is_not_contested(self):
        self.assertFalse(_record().is_contested)

    def test_affiliation_is_independent_of_ontology(self):
        """The issue's central warning: the four kinds are not four factions."""
        record = _record(ontology=EntityOntology.CONSTRUCT,
                         faction_relationships=("some polity",))
        self.assertIs(record.ontology, EntityOntology.CONSTRUCT)
        self.assertEqual(record.faction_relationships, ("some polity",))

    def test_alias_lookup_is_case_insensitive(self):
        record = _record(aliases=("Other Name",))
        self.assertTrue(record.knows("other name"))
        self.assertTrue(record.knows("ENTITY E1"))
        self.assertFalse(record.knows("unrelated"))
        # The identifier is an internal key, not a name the entry is "known by".
        self.assertFalse(record.knows("e1"))

    def test_the_form_distinguishes_a_mythonym_from_a_species(self):
        self.assertIsNot(EntityForm.MYTHONYM, EntityForm.SPECIES)
        self.assertEqual(EntityForm.VESSEL_OR_TECHNOLOGY.value, "vessel_or_technology")

    def test_the_epistemic_register_keeps_disclosure_explicit(self):
        self.assertTrue(KnowledgeStatus.GM_TRUTH.is_gm_only)
        self.assertFalse(KnowledgeStatus.GM_TRUTH.is_player_visible)
        for status in (KnowledgeStatus.RUMOUR, KnowledgeStatus.CANON,
                       KnowledgeStatus.REPORTED_CLAIM, KnowledgeStatus.SOURCE_MYTHOLOGY,
                       KnowledgeStatus.PLAYER_KNOWN, KnowledgeStatus.UNKNOWN):
            with self.subTest(status=status):
                self.assertTrue(status.is_player_visible)

    def test_an_unrecorded_status_is_unknown_not_canon(self):
        self.assertIs(_record().knowledge_status, KnowledgeStatus.UNKNOWN)

    def test_a_record_round_trips(self):
        record = _record(
            "e9",
            aliases=("A",),
            ontology=EntityOntology.NOETIC,
            alternative_ontologies=(EntityOntology.BIOLOGIC,),
            form=EntityForm.AVATAR,
            phenotype="a shape",
            communication_modes=("telepathy",),
            faction_relationships=("a bloc",),
            manifestations=("a dream",),
            related_entities=("e1",),
            human_folklore_analogues=("a legend",),
            source_references=("a source",),
            knowledge_status=KnowledgeStatus.RUMOUR,
            reveal_stage="later",
            gm_secrets="hidden",
            art_direction="a brief",
        )
        self.assertEqual(EntityRecord.from_dict(json.loads(json.dumps(record.to_dict()))), record)

    def test_a_missing_field_falls_back_to_its_default(self):
        restored = EntityRecord.from_dict({"identifier": "e1", "display_name": "x"})
        self.assertIs(restored.ontology, EntityOntology.BIOLOGIC)
        self.assertIs(restored.form, EntityForm.SPECIES)
        self.assertIs(restored.knowledge_status, KnowledgeStatus.UNKNOWN)

    def test_an_unrecognised_value_raises_instead_of_taking_the_default(self):
        """A typo must not load as a plausible classification that looks deliberate."""
        for payload in (
            {"identifier": "e1", "display_name": "x", "ontology": "biology"},
            {"identifier": "e1", "display_name": "x", "form": "speces"},
            {"identifier": "e1", "display_name": "x", "knowledge_status": "canonn"},
            {"identifier": "e1", "display_name": "x", "alternative_ontologies": ["bogus"]},
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(CodexError):
                    EntityRecord.from_dict(payload)


class CodexTests(unittest.TestCase):
    def _codex(self) -> Codex:
        codex = Codex()
        codex.add(_record("a", ontology=EntityOntology.BIOLOGIC, reveal_stage="common"))
        codex.add(_record("b", ontology=EntityOntology.NOETIC,
                          alternative_ontologies=(EntityOntology.PLASMOID,),
                          reveal_stage="later"))
        codex.add(_record("c", ontology=EntityOntology.CONSTRUCT,
                          knowledge_status=KnowledgeStatus.GM_TRUTH,
                          gm_secrets="the withheld truth", reveal_stage="later",
                          related_entities=("a", "not-in-the-codex")))
        return codex

    def test_a_duplicate_identifier_is_refused(self):
        codex = Codex()
        codex.add(_record("a"))
        with self.assertRaises(CodexError):
            codex.add(_record("a"))

    def test_lookup_is_by_identifier_display_name_or_alias(self):
        codex = Codex()
        codex.add(_record("a", aliases=("Other",)))
        self.assertEqual(codex.get("a").identifier, "a")
        self.assertEqual(codex.get("Other").identifier, "a")
        self.assertEqual(codex.get("a").identifier, "a")
        with self.assertRaises(CodexError):
            codex.get("nothing")
        self.assertIsNone(codex.find("nothing"))

    def test_queries_by_the_two_axes_and_by_stage(self):
        codex = self._codex()
        self.assertEqual([r.identifier for r in codex.by_ontology(EntityOntology.BIOLOGIC)], ["a"])
        self.assertEqual([r.identifier for r in codex.by_form(EntityForm.SPECIES)], ["a", "b", "c"])
        self.assertEqual([r.identifier for r in codex.by_reveal_stage("later")], ["b", "c"])
        self.assertEqual(
            [r.identifier for r in codex.by_knowledge_status(KnowledgeStatus.GM_TRUTH)], ["c"]
        )

    def test_contested_entries_are_the_ones_with_rival_readings(self):
        self.assertEqual([r.identifier for r in self._codex().contested()], ["b"])

    def test_related_entries_ignore_names_the_codex_does_not_hold(self):
        related = self._codex().related("c")
        self.assertEqual([r.identifier for r in related], ["a"])

    def test_a_player_facing_view_withholds_gm_material(self):
        codex = self._codex()
        self.assertNotIn("gm_secrets", codex.player_view("a"))
        self.assertEqual([r.identifier for r in codex.player_records()], ["a", "b"])

    def test_no_gm_secret_survives_in_the_player_payload(self):
        """The issue's 'do not spoil GM-only truths in player UI' as a property of the code."""
        codex = self._codex()
        payload = json.dumps(codex.player_payload(), ensure_ascii=False)
        self.assertNotIn("the withheld truth", payload)
        self.assertNotIn("gm_secrets", payload)
        self.assertNotIn('"c"', payload)

    def test_the_codex_round_trips(self):
        codex = self._codex()
        self.assertEqual(Codex.from_json(codex.to_json()).to_json(), codex.to_json())


class ShippedCodexDataTests(unittest.TestCase):
    """Structural checks on the data file, because loading it is code behaviour."""

    def test_the_data_file_exists_and_loads(self):
        self.assertTrue(CODEX_PATH.exists(), f"missing codex data file at {CODEX_PATH}")
        self.assertGreater(len(load_codex()), 0)

    def test_every_ontology_is_represented(self):
        codex = load_codex()
        for ontology in EntityOntology:
            with self.subTest(ontology=ontology):
                self.assertTrue(codex.by_ontology(ontology),
                                f"no codex entry uses ontology {ontology.value!r}")

    def test_more_than_one_form_is_represented(self):
        forms = {record.form for record in load_codex().entries.values()}
        self.assertGreater(len(forms), 1)

    def test_the_locked_bloc_names_are_used(self):
        codex = load_codex()
        self.assertEqual(codex.get("uccc").display_name, "Union of Collective Consciousness Communes")
        self.assertEqual(codex.get("orion_sphere").display_name,
                         "Greater Orion Arm Co-Prosperity Sphere")

    def test_the_older_orion_label_is_only_an_exonym(self):
        """The issue locks the names and forbids reverting to the old ones as official labels."""
        orion = load_codex().get("orion_sphere")
        self.assertIn("Orion Group", orion.aliases)
        self.assertNotEqual(orion.display_name, "Orion Group")
        self.assertNotEqual(load_codex().get("uccc").display_name, "Confederation")

    def test_confederation_appears_only_as_a_historical_exonym(self):
        uccc = load_codex().get("uccc")
        self.assertTrue(any("Confederation" in alias for alias in uccc.aliases))
        self.assertIn("exonym", " ".join(uccc.aliases).lower())

    def test_every_entry_carries_a_knowledge_status_that_is_not_the_default_by_accident(self):
        codex = load_codex()
        unclassified = [r.identifier for r in codex.by_knowledge_status(KnowledgeStatus.UNKNOWN)]
        self.assertEqual(unclassified, [], "every shipped entry should declare how it is known")

    def test_at_least_one_entry_is_contested_and_one_is_gm_only(self):
        codex = load_codex()
        self.assertTrue(codex.contested(), "the codex should carry rival readings")
        self.assertTrue(codex.by_knowledge_status(KnowledgeStatus.GM_TRUTH),
                        "the GM-only filtering path needs at least one GM-only entry")

    def test_no_gm_only_truth_leaks_into_the_player_payload_of_the_shipped_codex(self):
        codex = load_codex()
        payload = json.dumps(codex.player_payload(), ensure_ascii=False)
        for record in codex.entries.values():
            if record.gm_secrets:
                with self.subTest(record=record.identifier):
                    self.assertNotIn(record.gm_secrets, payload)
        for record in codex.by_knowledge_status(KnowledgeStatus.GM_TRUTH):
            with self.subTest(record=record.identifier):
                self.assertNotIn(record.display_name, payload)


if __name__ == "__main__":
    unittest.main()
