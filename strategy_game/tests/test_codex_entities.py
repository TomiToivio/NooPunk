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
    CONSCIOUSNESS_STATUSES,
    ENTITY_DESCRIPTORS,
    ENTITY_ONTOLOGIES,
    Codex,
    CodexError,
    ConsciousnessStatus,
    EntityDescriptor,
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


class ExtendedDescriptorTests(unittest.TestCase):
    """The `RULEBOOK.md` §43.4 extended categories, carried as a descriptor axis (issue #348)."""

    def test_the_rulebook_extended_descriptors_are_declared(self):
        for name in ("process", "ecology", "assemblage", "collective", "geotic",
                     "hybrid_or_composite", "anomaly_or_unclassified"):
            with self.subTest(name=name):
                self.assertIn(name, ENTITY_DESCRIPTORS)

    def test_a_descriptor_is_not_an_ontology(self):
        """§43.4 says some are 'better treated as cross-cutting descriptors than as formal classes'."""
        self.assertEqual(set(ENTITY_DESCRIPTORS) & set(ENTITY_ONTOLOGIES), set())

    def test_a_descriptor_must_be_a_member(self):
        with self.assertRaises(CodexError):
            _record(ontology_descriptors=("collective",))  # type: ignore[arg-type]

    def test_a_descriptor_may_not_repeat(self):
        with self.assertRaises(CodexError):
            _record(ontology_descriptors=(EntityDescriptor.COLLECTIVE, EntityDescriptor.COLLECTIVE))

    def test_descriptors_ride_on_top_of_the_primary_ontology(self):
        """One primary reading plus descriptors, exactly as §43.4's worked example reads."""
        record = _record(ontology=EntityOntology.NOETIC,
                         ontology_descriptors=(EntityDescriptor.COLLECTIVE, EntityDescriptor.PROCESS))
        self.assertIs(record.ontology, EntityOntology.NOETIC)
        self.assertEqual(record.ontology_descriptors,
                         (EntityDescriptor.COLLECTIVE, EntityDescriptor.PROCESS))

    def test_descriptors_round_trip(self):
        record = _record("e5", ontology_descriptors=(EntityDescriptor.ECOLOGY,))
        self.assertEqual(EntityRecord.from_dict(json.loads(json.dumps(record.to_dict()))), record)

    def test_an_unrecognised_descriptor_raises_rather_than_being_dropped(self):
        with self.assertRaises(CodexError):
            EntityRecord.from_dict(
                {"identifier": "e1", "display_name": "x", "ontology_descriptors": ["vibes"]}
            )


class ConsciousnessPostureTests(unittest.TestCase):
    """The issue refuses to let the model assert what the fiction cannot know (issue #348)."""

    def test_the_default_posture_is_unknown(self):
        self.assertIs(_record().consciousness_status, ConsciousnessStatus.UNKNOWN)

    def test_the_vocabulary_matches_the_character_card_layer(self):
        from strategy_game.characters import CONSCIOUSNESS_STATUSES as CARD_STATUSES

        self.assertEqual(CONSCIOUSNESS_STATUSES, CARD_STATUSES)

    def test_nothing_turns_the_posture_into_a_truth_value(self):
        """No accessor may collapse interiority to a boolean — the setting does not settle it."""
        record = _record(consciousness_status=ConsciousnessStatus.CONTESTED)
        for name in ("is_conscious", "conscious", "is_sentient", "sentient", "has_mind"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(record, name), f"EntityRecord.{name} would assert interiority")
        self.assertNotIsInstance(record.consciousness_status, bool)

    def test_an_in_world_assertion_needs_a_cited_source(self):
        with self.assertRaises(CodexError):
            _record(consciousness_status=ConsciousnessStatus.ASSERTED_IN_WORLD)
        record = _record(consciousness_status=ConsciousnessStatus.ASSERTED_IN_WORLD,
                         source_references=("a witness account",))
        self.assertIs(record.consciousness_status, ConsciousnessStatus.ASSERTED_IN_WORLD)

    def test_the_posture_must_be_a_member(self):
        with self.assertRaises(CodexError):
            _record(consciousness_status="definitely")  # type: ignore[arg-type]

    def test_an_unrecognised_posture_raises(self):
        with self.assertRaises(CodexError):
            EntityRecord.from_dict(
                {"identifier": "e1", "display_name": "x", "consciousness_status": "yes"}
            )

    def test_the_posture_round_trips(self):
        record = _record("e6", consciousness_status=ConsciousnessStatus.CONTESTED)
        self.assertEqual(EntityRecord.from_dict(json.loads(json.dumps(record.to_dict()))), record)


class OntologyAbsenceTests(unittest.TestCase):
    """A polity is not a body: ontology may be absent *with a stated reason* (issue #348, §43.4)."""

    def test_a_body_form_may_not_omit_its_ontology(self):
        with self.assertRaises(CodexError):
            _record(ontology=None, form=EntityForm.SPECIES,
                    ontology_absent_reason="no reason helps a body")

    def test_a_polity_may_omit_its_ontology_with_a_reason(self):
        record = _record(ontology=None, form=EntityForm.POLITY,
                         ontology_absent_reason="a bloc, not a body")
        self.assertIsNone(record.ontology)
        self.assertEqual(record.hypotheses, ())
        self.assertFalse(record.is_contested)

    def test_an_omitted_ontology_needs_a_reason(self):
        with self.assertRaises(CodexError):
            _record(ontology=None, form=EntityForm.ORGANIZATION)

    def test_a_present_but_null_ontology_loads_as_absent_not_as_the_default(self):
        """A ``null`` with a reason is a stated absence, not the historical BIOLOGIC default."""
        record = EntityRecord.from_dict({
            "identifier": "e1", "display_name": "x", "ontology": None,
            "form": "polity", "ontology_absent_reason": "a bloc",
        })
        self.assertIsNone(record.ontology)

    def test_a_missing_ontology_key_still_takes_the_default(self):
        record = EntityRecord.from_dict({"identifier": "e1", "display_name": "x"})
        self.assertIs(record.ontology, EntityOntology.BIOLOGIC)

    def test_an_absent_ontology_round_trips(self):
        record = _record("e7", ontology=None, form=EntityForm.POLITY,
                         ontology_absent_reason="a bloc")
        restored = EntityRecord.from_dict(json.loads(json.dumps(record.to_dict())))
        self.assertIsNone(restored.ontology)
        self.assertEqual(restored.ontology_absent_reason, "a bloc")

    def test_the_absent_ontology_stays_absent_in_the_player_view(self):
        codex = Codex()
        codex.add(_record("p1", ontology=None, form=EntityForm.POLITY,
                          ontology_absent_reason="a bloc, not a body"))
        self.assertIsNone(codex.player_view("p1")["ontology"])


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

    def test_at_least_one_entry_declares_an_extended_descriptor(self):
        """The §43.4 descriptor axis must be exercised by the shipped data, not only by unit tests."""
        self.assertTrue(any(r.ontology_descriptors for r in load_codex().entries.values()))

    def test_every_shipped_descriptor_is_a_valid_member(self):
        for record in load_codex().entries.values():
            for descriptor in record.ontology_descriptors:
                with self.subTest(record=record.identifier):
                    self.assertIn(descriptor.value, ENTITY_DESCRIPTORS)

    def test_a_faction_form_declares_a_ontology_or_states_why_it_has_none(self):
        """Every polity/organization either claims a substrate or records the absence with a reason."""
        for record in load_codex().entries.values():
            if record.form in (EntityForm.POLITY, EntityForm.ORGANIZATION):
                with self.subTest(record=record.identifier):
                    self.assertTrue(
                        record.ontology is not None or record.ontology_absent_reason.strip(),
                        f"{record.identifier}: a faction form must claim a ontology or state its absence",
                    )

    def test_the_reconciled_polities_no_longer_assert_a_substrate(self):
        """The #348 reconciliation: a bloc is not *a* biologic (its own substrate text says so)."""
        codex = load_codex()
        for identifier in ("uccc", "orion_sphere"):
            with self.subTest(record=identifier):
                record = codex.get(identifier)
                self.assertIsNone(record.ontology)
                self.assertTrue(record.ontology_absent_reason.strip())

    def test_every_shipped_posture_is_a_valid_member(self):
        for record in load_codex().entries.values():
            with self.subTest(record=record.identifier):
                self.assertIn(record.consciousness_status.value, CONSCIOUSNESS_STATUSES)


if __name__ == "__main__":
    unittest.main()
