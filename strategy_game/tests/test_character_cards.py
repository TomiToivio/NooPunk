"""Tests for the character-card layer (issue #356).

Executable-code tests only, per the #271 policy: they exercise the schema, the loader, the
validator, instantiation, filters and renders. Nothing here asserts lore, prose or canon wording.

The guards are written so they can fail: several tests deliberately feed the validator a card
that contradicts the codex, and assert that the contradiction is reported.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from strategy_game.characters import (
    CHARACTER_CARDS_FORMAT,
    CHARACTER_CARDS_VERSION,
    CLAIM_STATUSES,
    CONSCIOUSNESS_STATUSES,
    DECLARED_ACTION_KINDS,
    NHI_CATEGORIES,
    NHI_TAG_KINDS,
    TAG_KINDS,
    CharacterCard,
    CharacterError,
    CharacterFamily,
    CharacterRoster,
    ClaimStatus,
    NhiCategory,
    NhiClassification,
    Tag,
    classification_from_codex_entry,
    codex_entry_map,
    load_character_cards,
    load_world_card_catalogue,
    normalise_ontology,
    render_detail,
    render_front,
    slug,
    tag_vocabulary_matches,
    to_card,
)
from strategy_game.provenance import Provenance, ProvenanceKind
from strategy_game.tabletop.cards import CardRole, CardType, CardVisibility

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "character_cards.json"

#: Content keys that would mean a mechanic had crept into the data.
FORBIDDEN_MECHANIC_KEYS = (
    "stat",
    "stats",
    "attributes",
    "skill",
    "skill_value",
    "target_number",
    "modifier",
    "difficulty",
    "dice",
    "threshold",
    "cost",
    "upkeep",
)


class CharacterCardDataTests(unittest.TestCase):
    """The shipped content file loads and stays gate-free."""

    def setUp(self) -> None:
        self.roster = load_character_cards()
        self.codex = codex_entry_map()

    def test_data_file_declares_the_expected_format_and_version(self) -> None:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        self.assertEqual(payload["format"], CHARACTER_CARDS_FORMAT)
        self.assertEqual(payload["version"], CHARACTER_CARDS_VERSION)
        self.assertEqual(self.roster.version, CHARACTER_CARDS_VERSION)
        self.assertTrue(self.roster.sources)

    def test_roster_loads_all_three_families(self) -> None:
        self.assertGreaterEqual(len(self.roster), 15)
        for family in CharacterFamily:
            self.assertTrue(self.roster.filter(family=family), f"no cards for family {family.value}")

    def test_identifiers_are_unique_stable_slugs(self) -> None:
        for card in self.roster:
            self.assertEqual(card.identifier, slug(card.identifier))
            self.assertNotIn("__", card.identifier)

    def test_canonical_exemplar_is_sir_mars_eldrich(self) -> None:
        card = self.roster.get("sir_mars_eldrich")
        self.assertIs(card.family, CharacterFamily.CANONICAL)
        self.assertEqual(card.display_name, "Sir Mars Eldrich")
        self.assertIn("ulp", card.faction_ids)
        self.assertIs(card.claim_status, ClaimStatus.CANON)
        self.assertTrue(card.art_ref.startswith("placeholder:"))
        self.assertTrue(card.sources)
        self.assertIsNone(card.template_id)

    def test_canonical_cards_cite_sources_and_are_not_instances(self) -> None:
        for card in self.roster.filter(family=CharacterFamily.CANONICAL):
            self.assertTrue(card.sources, f"{card.identifier} must cite sources")
            self.assertIsNone(card.template_id)

    def test_archetypes_are_reusable_templates(self) -> None:
        archetypes = self.roster.filter(family=CharacterFamily.ARCHETYPE)
        self.assertGreaterEqual(len(archetypes), 8)
        for card in archetypes:
            self.assertIsNone(card.template_id)
            self.assertTrue(card.tags, f"{card.identifier} should carry tags")
            self.assertIsNone(card.nhi)

    def test_nhi_family_covers_all_four_categories(self) -> None:
        for category in NhiCategory:
            self.assertTrue(
                self.roster.filter(family=CharacterFamily.NHI, category=category),
                f"no NHI exemplar for category {category.value}",
            )

    def test_the_whole_roster_validates_against_the_real_codex(self) -> None:
        self.assertEqual(self.roster.validate(codex=self.codex), ())

    def test_nhi_classifications_match_the_codex_entry_by_entry(self) -> None:
        for card in self.roster.filter(family=CharacterFamily.NHI):
            assert card.nhi is not None
            entry = self.codex[card.nhi.species_ref]
            derived = classification_from_codex_entry(entry)
            self.assertIs(card.nhi.category, derived.category)
            self.assertIs(card.nhi.claim_status, derived.claim_status)
            self.assertEqual(card.nhi.contested, derived.contested)
            self.assertEqual(card.nhi.reveal_stage, derived.reveal_stage)

    def test_nhi_hypotheses_and_allegiances_are_quoted_from_the_codex(self) -> None:
        """A card may not invent an origin claim or an allegiance the codex does not carry."""
        for card in self.roster.filter(family=CharacterFamily.NHI):
            assert card.nhi is not None
            entry = self.codex[card.nhi.species_ref]
            claims = entry.get("origin_claims")
            expected = (claims,) if isinstance(claims, str) else tuple(claims or ())
            self.assertEqual(card.nhi.origin_hypotheses, expected)
            self.assertEqual(card.nhi.allegiances, tuple(entry.get("faction_relationships") or ()))

    def test_a_contested_classification_is_not_flattened(self) -> None:
        card = self.roster.get("nhi_orbs_of_light")
        assert card.nhi is not None
        self.assertTrue(card.nhi.contested)
        self.assertIs(card.nhi.category, NhiCategory.PLASMOID)
        self.assertTrue(self.codex[card.nhi.species_ref]["alternative_ontologies"])

    def test_declared_actions_are_labels_only(self) -> None:
        for card in self.roster:
            for action in card.declared_actions:
                self.assertIn(action, DECLARED_ACTION_KINDS)

    def test_no_card_carries_a_numeric_mechanic(self) -> None:
        """The content stays gate-free: no stat, threshold, modifier, dice or cost key."""
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        for entry in payload["entries"]:
            for key in FORBIDDEN_MECHANIC_KEYS:
                self.assertNotIn(key, entry, f"{entry.get('identifier')} carries {key!r}")
            for tag in entry.get("tags", []):
                self.assertIn(tag["kind"], TAG_KINDS)

    def test_tag_kinds_agree_with_issue_346(self) -> None:
        self.assertTrue(tag_vocabulary_matches())
        for card in self.roster:
            for tag in card.tags:
                self.assertIn(tag.kind, TAG_KINDS)


class InstantiationTests(unittest.TestCase):
    """template -> instance, without duplicating a canonical identity."""

    def setUp(self) -> None:
        self.roster = load_character_cards()

    def test_instantiate_creates_a_generated_instance_linked_to_its_template(self) -> None:
        instance = self.roster.instantiate("archetype_netrunner", display_name="Mika's Cousin")
        self.assertEqual(instance.template_id, "archetype_netrunner")
        self.assertEqual(instance.identifier, "archetype_netrunner_mika_s_cousin")
        self.assertIs(instance.provenance.kind, ProvenanceKind.GENERATED)
        self.assertIs(instance.family, CharacterFamily.ARCHETYPE)
        self.assertEqual(instance.tags, self.roster.get("archetype_netrunner").tags)
        self.assertIn(instance.identifier, [card.identifier for card in self.roster])

    def test_instance_can_carry_declared_progression_state(self) -> None:
        instance = self.roster.instantiate(
            "archetype_soldier", display_name="Unit 7 rifleman", state={"injury": "concussion", "loyalty": "shaken"}
        )
        self.assertEqual(instance.state["loyalty"], "shaken")
        self.assertIn("state: injury=concussion", render_detail(instance))

    def test_instantiate_refuses_a_canonical_character(self) -> None:
        with self.assertRaises(CharacterError):
            self.roster.instantiate("sir_mars_eldrich")

    def test_instantiate_refuses_a_duplicate_identifier(self) -> None:
        self.roster.instantiate("archetype_faction_organizer", display_name="Ward Three")
        with self.assertRaises(CharacterError):
            self.roster.instantiate("archetype_faction_organizer", display_name="Ward Three")

    def test_an_instance_keeps_its_template_readable(self) -> None:
        instance = self.roster.instantiate("archetype_journalist", display_name="Night desk")
        text = render_detail(instance, roster=self.roster)
        self.assertIn("instance of: archetype_journalist", text)


class FilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.roster = load_character_cards()

    def test_filter_by_family_faction_tag_category_role_and_text(self) -> None:
        self.assertEqual(len(self.roster.filter(family="nhi")), 4)
        self.assertEqual(
            [card.identifier for card in self.roster.filter(faction="ulp")], ["sir_mars_eldrich"]
        )
        self.assertTrue(self.roster.filter(tag="competence"))
        self.assertEqual(len(self.roster.filter(category="plasmoid")), 1)
        self.assertTrue(self.roster.filter(role="netrunner"))
        self.assertTrue(self.roster.filter(text="shipping magnate"))
        self.assertEqual(self.roster.filter(text="no such phrase anywhere"), ())

    def test_get_raises_for_an_unknown_identifier(self) -> None:
        with self.assertRaises(CharacterError):
            self.roster.get("not_a_card")


class RenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.roster = load_character_cards()
        self.codex = codex_entry_map()

    def test_front_is_compact_and_names_family_or_role(self) -> None:
        text = render_front(self.roster.get("sir_mars_eldrich"))
        self.assertIn("Sir Mars Eldrich", text)
        self.assertIn("ulp", text)
        self.assertLessEqual(len(text.splitlines()), 6)

    def test_front_never_leaks_gm_notes(self) -> None:
        for card in self.roster:
            if card.gm_notes:
                self.assertNotIn(card.gm_notes, render_front(card))

    def test_detail_redacts_a_gm_truth_card_until_asked(self) -> None:
        card = CharacterCard(
            identifier="test_secret",
            family=CharacterFamily.ARCHETYPE,
            display_name="Secret holder",
            claim_status=ClaimStatus.GM_TRUTH,
            gm_notes="the patron is an NHI construct",
        )
        hidden = render_detail(card)
        self.assertIn("[redacted", hidden)
        self.assertNotIn("the patron is an NHI construct", hidden)
        shown = render_detail(card, reveal_secrets=True)
        self.assertIn("the patron is an NHI construct", shown)

    def test_detail_expands_lore_from_the_codex(self) -> None:
        text = render_detail(self.roster.get("nhi_orbs_of_light"), codex=self.codex)
        self.assertIn("plasmoid", text)
        self.assertIn("contested=True", text)
        self.assertIn("lore:", text)


class BridgeTests(unittest.TestCase):
    def test_to_card_reuses_the_shared_card_primitive(self) -> None:
        card = to_card(load_character_cards().get("sir_mars_eldrich"))
        self.assertIs(card.card_type, CardType.CHARACTER)
        self.assertIs(card.role, CardRole.PERSISTENT_RECORD)
        self.assertEqual(card.owner_id, "ulp")
        self.assertTrue(all(":" in tag for tag in card.tags))
        # Nothing interprets a character card yet: the mechanic slots stay empty.
        self.assertEqual(card.prerequisites, ())
        self.assertEqual(card.effects, ())
        self.assertIs(card.visibility, CardVisibility.PUBLIC)


class ValidationTests(unittest.TestCase):
    """The validator must be able to fail, or it is not evidence."""

    def setUp(self) -> None:
        self.roster = load_character_cards()
        self.codex = codex_entry_map()

    def test_validate_detects_a_category_that_contradicts_the_codex(self) -> None:
        entry = self.codex["orbs_of_light"]
        wrong = CharacterCard(
            identifier="test_wrong_category",
            family=CharacterFamily.NHI,
            display_name="Orb, mislabelled",
            nhi=NhiClassification(
                category=NhiCategory.CONSTRUCT,
                species_ref="orbs_of_light",
                form=str(entry["form"]),
                claim_status=ClaimStatus(entry["knowledge_status"]),
                contested=bool(entry["alternative_ontologies"]),
            ),
        )
        problems = CharacterRoster([wrong], version=CHARACTER_CARDS_VERSION).validate(codex=self.codex)
        self.assertTrue(any("contradicts codex ontology" in problem for problem in problems), problems)

    def test_validate_detects_a_claim_status_that_contradicts_the_codex(self) -> None:
        wrong = CharacterCard(
            identifier="test_wrong_claim",
            family=CharacterFamily.NHI,
            display_name="Rumour promoted to canon",
            nhi=NhiClassification(
                category=NhiCategory.PLASMOID,
                species_ref="orbs_of_light",
                form="mythonym",
                claim_status=ClaimStatus.CANON,
            ),
        )
        problems = CharacterRoster([wrong], version=CHARACTER_CARDS_VERSION).validate(codex=self.codex)
        self.assertTrue(any("contradicts codex knowledge_status" in problem for problem in problems), problems)

    def test_validate_detects_an_unknown_species_reference(self) -> None:
        unknown = CharacterCard(
            identifier="test_unknown_species",
            family=CharacterFamily.NHI,
            display_name="Invented species",
            nhi=NhiClassification(
                category=NhiCategory.NOETIC, species_ref="invented_species", form="species"
            ),
        )
        problems = CharacterRoster([unknown], version=CHARACTER_CARDS_VERSION).validate(codex=self.codex)
        self.assertTrue(any("not in the codex" in problem for problem in problems), problems)

    def test_validate_detects_an_unknown_faction_id(self) -> None:
        problems = self.roster.validate(known_faction_ids=("cpu", "uip", "ulp"))
        self.assertEqual(problems, ())
        problems = self.roster.validate(known_faction_ids=("cpu", "uip"))
        self.assertTrue(any("not a known faction id" in problem for problem in problems), problems)


class SchemaTests(unittest.TestCase):
    """Construction rules: the shape refuses the mistakes a content author would make."""

    def test_unknown_tag_kind_is_refused(self) -> None:
        with self.assertRaises(CharacterError):
            Tag(kind="mood", value="brooding")

    def test_nhi_card_without_a_classification_is_refused(self) -> None:
        with self.assertRaises(CharacterError):
            CharacterCard(identifier="bare_nhi", family=CharacterFamily.NHI, display_name="Bare")

    def test_archetype_may_not_carry_an_nhi_classification(self) -> None:
        with self.assertRaises(CharacterError):
            CharacterCard(
                identifier="confused_archetype",
                family=CharacterFamily.ARCHETYPE,
                display_name="Confused",
                nhi=NhiClassification(category=NhiCategory.NOETIC, species_ref="q_uo"),
            )

    def test_canonical_card_must_cite_sources(self) -> None:
        with self.assertRaises(CharacterError):
            CharacterCard(identifier="unsourced_canon", family=CharacterFamily.CANONICAL, display_name="Nobody")

    def test_unknown_declared_action_is_refused(self) -> None:
        with self.assertRaises(CharacterError):
            CharacterCard(
                identifier="odd_action",
                family=CharacterFamily.ARCHETYPE,
                display_name="Odd",
                declared_actions=("interpretive_dance",),
            )

    def test_an_unrecorded_origin_stays_unknown_rather_than_reading_as_fact(self) -> None:
        card = CharacterCard(identifier="silent_origin", family=CharacterFamily.ARCHETYPE, display_name="Silent")
        self.assertIs(card.provenance.kind, ProvenanceKind.UNKNOWN)
        self.assertIsNot(card.provenance.kind, ProvenanceKind.EVIDENCE)

    def test_duplicate_identifiers_are_refused_by_the_roster(self) -> None:
        card = CharacterCard(identifier="twin", family=CharacterFamily.ARCHETYPE, display_name="Twin")
        with self.assertRaises(CharacterError):
            CharacterRoster([card, card])

    def test_every_claim_status_in_the_schema_is_one_the_codex_declares(self) -> None:
        declared = {str(entry.get("knowledge_status")) for entry in codex_entry_map().values()}
        self.assertTrue(set(CLAIM_STATUSES) >= declared, declared - set(CLAIM_STATUSES))
        self.assertTrue(set(NHI_CATEGORIES) >= {str(e.get("ontology")) for e in codex_entry_map().values()})


class LoaderTests(unittest.TestCase):
    def test_missing_file_is_reported_as_a_character_error(self) -> None:
        with self.assertRaises(CharacterError):
            load_character_cards(Path(tempfile.gettempdir()) / "definitely_not_here.json")

    def test_wrong_format_and_version_are_refused(self) -> None:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        for mutate in ({"format": "something.else"}, {"version": 99}):
            broken = dict(payload)
            broken.update(mutate)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "cards.json"
                path.write_text(json.dumps(broken), encoding="utf-8")
                with self.assertRaises(CharacterError):
                    load_character_cards(path)

    def test_tag_vocabulary_check_detects_a_divergence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "faction_creation.json"
            path.write_text(json.dumps({"tag_kinds": [{"id": "belief"}]}), encoding="utf-8")
            self.assertFalse(tag_vocabulary_matches(path))


class NonCollapseTests(unittest.TestCase):
    """The three families are held apart: an entity is not a person, and facts are not inferences."""

    def setUp(self) -> None:
        self.roster = load_character_cards()
        self.codex = codex_entry_map()

    def test_nhi_cards_carry_no_statted_capability(self) -> None:
        for card in self.roster.filter(family=CharacterFamily.NHI):
            self.assertEqual(card.declared_actions, (), card.identifier)
            for tag in card.tags:
                self.assertIn(tag.kind, NHI_TAG_KINDS, card.identifier)

    def test_an_nhi_card_may_not_declare_an_action(self) -> None:
        with self.assertRaises(CharacterError):
            CharacterCard(
                identifier="statted_entity",
                family=CharacterFamily.NHI,
                display_name="Statted entity",
                declared_actions=("combat",),
                nhi=NhiClassification(
                    category=NhiCategory.CONSTRUCT, species_ref="metallic_spheres", form="vessel_or_technology"
                ),
            )

    def test_a_competence_tag_is_refused_on_an_nhi_card(self) -> None:
        with self.assertRaises(CharacterError):
            CharacterCard(
                identifier="capable_entity",
                family=CharacterFamily.NHI,
                display_name="Capable entity",
                tags=(Tag(kind="competence", value="hacks anything"),),
                nhi=NhiClassification(
                    category=NhiCategory.CONSTRUCT, species_ref="metallic_spheres", form="vessel_or_technology"
                ),
            )

    def test_an_nhi_card_must_declare_the_codex_form_as_well_as_the_category(self) -> None:
        with self.assertRaises(CharacterError):
            CharacterCard(
                identifier="formless_entity",
                family=CharacterFamily.NHI,
                display_name="Formless entity",
                nhi=NhiClassification(category=NhiCategory.NOETIC, species_ref="q_uo"),
            )

    def test_an_nhi_card_is_never_a_template_for_a_person(self) -> None:
        with self.assertRaises(CharacterError):
            self.roster.instantiate("nhi_metallic_spheres")

    def test_observable_facts_are_separate_from_inferences(self) -> None:
        for card in self.roster.filter(family=CharacterFamily.NHI):
            self.assertTrue(card.observable_facts, card.identifier)
            self.assertTrue(card.inferences, card.identifier)
            self.assertFalse(
                set(card.observable_facts) & set(card.inferences),
                f"{card.identifier} merges observation with attribution",
            )

    def test_observable_facts_come_from_the_codex_manifestations(self) -> None:
        """A card may not invent what was seen: every codex manifestation must appear as observed."""
        for card in self.roster.filter(family=CharacterFamily.NHI):
            assert card.nhi is not None
            entry = self.codex[card.nhi.species_ref]
            for manifestation in entry.get("manifestations") or ():
                self.assertIn(manifestation, card.observable_facts, card.identifier)

    def test_consciousness_status_defaults_to_unknown_and_is_never_asserted_lightly(self) -> None:
        plain = CharacterCard(identifier="plain_person", family=CharacterFamily.ARCHETYPE, display_name="Plain")
        self.assertEqual(plain.consciousness_status, "unknown")
        for card in self.roster:
            self.assertIn(card.consciousness_status, CONSCIOUSNESS_STATUSES)
        with self.assertRaises(CharacterError):
            CharacterCard(
                identifier="certain_entity",
                family=CharacterFamily.NHI,
                display_name="Certainly conscious",
                consciousness_status="asserted_in_world",
                nhi=NhiClassification(
                    category=NhiCategory.NOETIC, species_ref="q_uo", form="individual"
                ),
            )

    def test_front_shows_observable_facts_while_the_identity_stays_unestablished(self) -> None:
        text = render_front(self.roster.get("nhi_orbs_of_light"))
        self.assertIn("observed:", text)
        self.assertIn("A light that moves against the wind", text)
        self.assertIn("contested", text)

    def test_detail_prints_facts_and_inferences_as_two_lists(self) -> None:
        text = render_detail(self.roster.get("nhi_metallic_spheres"))
        self.assertIn("observable facts:", text)
        self.assertIn("inferences (attribution, not observation):", text)

    def test_detail_withholds_gm_secrets_from_a_codex_entry(self) -> None:
        codex = dict(self.codex)
        entry = dict(codex["orbs_of_light"])
        entry["gm_secrets"] = "the orbs are a maintenance swarm for something larger"
        codex["orbs_of_light"] = entry
        text = render_detail(self.roster.get("nhi_orbs_of_light"), codex=codex, reveal_secrets=True)
        self.assertNotIn("maintenance swarm", text)

    def test_filter_by_form(self) -> None:
        self.assertEqual(
            [card.identifier for card in self.roster.filter(form="mythonym")], ["nhi_orbs_of_light"]
        )
        self.assertTrue(self.roster.filter(form="species"))


class WorldCatalogueAdapterTests(unittest.TestCase):
    """The root world-card catalogue is read into the single record, and what it may not import
    is reported rather than silently carried."""

    def setUp(self) -> None:
        self.roster, self.problems = load_world_card_catalogue()

    def test_the_root_catalogue_loads_into_the_single_record(self) -> None:
        self.assertTrue(self.roster)
        self.assertGreaterEqual(len(self.roster), 5)
        for card in self.roster:
            self.assertEqual(card.identifier, slug(card.identifier))
        self.assertTrue(self.roster.get("leader_sir_mars_eldrich"))

    def test_numeric_attributes_are_reported_and_not_carried(self) -> None:
        self.assertTrue(any("numeric attributes" in problem for problem in self.problems), self.problems)
        for card in self.roster:
            self.assertFalse(hasattr(card, "attributes"))
            self.assertFalse(hasattr(card, "stats"))

    def test_untyped_tags_are_reported_and_not_imported(self) -> None:
        self.assertTrue(any("untyped tags" in problem for problem in self.problems), self.problems)
        for card in self.roster:
            self.assertEqual(card.tags, ())

    def test_nhi_cards_without_a_codex_reference_are_reported(self) -> None:
        reported = " ".join(self.problems)
        for name in ("nhi.biologic", "nhi.construct", "nhi.noetic", "nhi.plasmoid"):
            self.assertIn(slug(name), reported, name)
        self.assertFalse(self.roster.filter(family=CharacterFamily.NHI))

    def test_faction_labels_are_slugged_and_the_mapping_is_reported(self) -> None:
        self.assertTrue(any("faction label" in problem for problem in self.problems), self.problems)
        leader = self.roster.get("leader_sir_mars_eldrich")
        self.assertEqual(leader.faction_ids, ("eldrich_corporation",))

    def test_the_imported_roster_validates_clean_against_the_codex(self) -> None:
        self.assertEqual(self.roster.validate(codex=codex_entry_map()), ())

    def test_observations_are_carried_and_attributes_reported_on_a_synthetic_entry(self) -> None:
        payload = {
            "schema_version": 1,
            "cards": [
                {
                    "id": "archetype.test",
                    "card_type": "archetype",
                    "name": "Test person",
                    "role": "tester",
                    "summary": "Does the thing.",
                    "factions": [],
                    "tags": ["plain"],
                    "attributes": {"INT": 2},
                    "actions": ["investigation"],
                    "public": {"observation": "A light that moves against the wind"},
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "world_cards.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            roster, problems = load_world_card_catalogue(path)
        card = roster.get("archetype_test")
        self.assertEqual(card.observable_facts, ("A light that moves against the wind",))
        self.assertTrue(any("numeric attributes" in problem for problem in problems), problems)

    def test_normalise_ontology_accepts_both_spellings_and_refuses_junk(self) -> None:
        for value in ("Constructs", "construct", "CONSTRUCTS"):
            self.assertEqual(normalise_ontology(value), "construct")
        with self.assertRaises(CharacterError):
            normalise_ontology("technology")

    def test_missing_catalogue_is_a_character_error(self) -> None:
        with self.assertRaises(CharacterError):
            load_world_card_catalogue(Path(tempfile.gettempdir()) / "not_a_catalogue.json")


if __name__ == "__main__":
    unittest.main()
