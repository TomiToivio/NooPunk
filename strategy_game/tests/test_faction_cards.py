"""Tests for the faction-card layer (issue #346, acceptance criterion 4).

Executable-code tests only, per the #271 policy: they exercise the schema, the loader, the validator
and the projection. Nothing here asserts lore, prose or canon wording.

The guards are written so they can fail: several tests deliberately hand the validator a card that
contradicts the tag scopes or the control vocabulary and assert that the contradiction is reported.
"""
from __future__ import annotations

import dataclasses
import json
import tempfile
import typing
import unittest
from pathlib import Path

from strategy_game.characters import TAG_KINDS, Tag
from strategy_game.faction_cards import (
    CARD_TYPE_IDS,
    CONTROL_STATES,
    EFFECTS_ENFORCED,
    FACTION_CARDS_FORMAT,
    FACTION_CARDS_VERSION,
    FORBIDDEN_CARD_KEYS,
    PROJECTABLE_TO_PRIMITIVE,
    UNPROJECTABLE,
    FactionCard,
    FactionCardError,
    faction_cards_from_dict,
    load_faction_cards,
    render_front,
    tag_model,
    to_card,
)
from strategy_game.provenance import Provenance, ProvenanceKind
from strategy_game.tabletop.cards import CardRole, CardType

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "faction_cards.json"

#: Metric-shaped field-name tokens a card record must never carry.
METRIC_TOKENS = ("score", "strength", "modifier", "threshold", "cost", "rating", "level")


class ShippedDataTests(unittest.TestCase):
    """The shipped data file loads and specifies all four card types."""

    def setUp(self) -> None:
        self.model = load_faction_cards()

    def test_data_file_declares_the_expected_format_and_version(self) -> None:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        self.assertEqual(payload["format"], FACTION_CARDS_FORMAT)
        self.assertEqual(payload["version"], FACTION_CARDS_VERSION)
        self.assertTrue(self.model.sources)

    def test_the_four_card_types_are_declared_and_specified(self) -> None:
        self.assertEqual(CARD_TYPE_IDS, ("character", "organization", "research", "government"))
        self.assertEqual(set(self.model.specs), set(CARD_TYPE_IDS))
        for card_type in CARD_TYPE_IDS:
            with self.subTest(card_type=card_type):
                self.assertTrue(self.model.spec(card_type).represents)

    def test_the_shipped_roster_covers_organization_research_and_government(self) -> None:
        """The three types that had no layer before: character is consumed from characters.py."""
        self.assertEqual(len(self.model.by_type("organization")), 1)
        self.assertEqual(len(self.model.by_type("research")), 1)
        self.assertEqual(len(self.model.by_type("government")), 1)
        self.assertEqual(self.model.by_type("character"), ())

    def test_the_whole_roster_validates_against_the_shared_vocabularies(self) -> None:
        self.assertEqual(self.model.validate(tag_model=tag_model()), ())

    def test_the_shipped_data_carries_no_forbidden_mechanic_key(self) -> None:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        for entry in payload["cards"]:
            for key in FORBIDDEN_CARD_KEYS:
                with self.subTest(card=entry.get("id"), key=key):
                    self.assertNotIn(key, entry)
            for tag in entry.get("tags", []):
                self.assertIn(tag["kind"], TAG_KINDS)

    def test_no_declared_interaction_is_enforced_and_each_says_why(self) -> None:
        self.assertTrue(self.model.interactions)
        for interaction in self.model.interactions:
            with self.subTest(interaction=interaction.identifier):
                self.assertFalse(interaction.enforced)
                self.assertTrue(interaction.reason)

    def test_effects_are_declared_but_never_enforced(self) -> None:
        self.assertIs(EFFECTS_ENFORCED, False)
        for spec in self.model.specs.values():
            with self.subTest(card_type=spec.identifier):
                self.assertFalse(spec.declared_function_enforced)

    def test_every_pending_decision_carries_its_reason(self) -> None:
        self.assertEqual(self.model.unreasoned_decisions(), ())
        ids = {str(item.get("id")) for item in self.model.pending_decisions()}
        self.assertIn("declared_interaction_effects", ids)
        self.assertIn("government_primitive_member", ids)


class SchemaTests(unittest.TestCase):
    """Construction rules: the shape refuses the mistakes a content author would make."""

    def test_an_unknown_card_type_is_refused(self) -> None:
        with self.assertRaises(FactionCardError):
            FactionCard(identifier="odd", card_type="spaceship", title="Odd")

    def test_an_off_vocabulary_control_state_is_refused(self) -> None:
        with self.assertRaises(FactionCardError):
            FactionCard(identifier="ctl", card_type="organization", title="X", control="owned_by_nobody")

    def test_an_unknown_tag_kind_is_refused(self) -> None:
        from strategy_game.characters import CharacterError

        with self.assertRaises(CharacterError):
            Tag(kind="mood", value="brooding")

    def test_a_forbidden_mechanic_state_key_is_refused(self) -> None:
        with self.assertRaises(FactionCardError):
            FactionCard(
                identifier="statted", card_type="organization", title="X", state={"modifier": "warm"}
            )

    def test_an_authored_card_must_cite_its_sources(self) -> None:
        with self.assertRaises(FactionCardError):
            FactionCard(
                identifier="unsourced_canon",
                card_type="organization",
                title="Nobody's organisation",
                provenance=Provenance(kind=ProvenanceKind.AUTHORED),
            )
        authored = FactionCard(
            identifier="sourced_canon",
            card_type="organization",
            title="A sourced organisation",
            provenance=Provenance(kind=ProvenanceKind.AUTHORED),
            sources=("issue #346",),
        )
        self.assertIs(authored.provenance.kind, ProvenanceKind.AUTHORED)

    def test_a_card_data_record_with_an_effect_key_is_refused_by_name(self) -> None:
        doc = {
            "format": FACTION_CARDS_FORMAT,
            "version": 1,
            "cards": [
                {"id": "with_effect", "card_type": "organization", "title": "X", "effects": [{"kind": "x"}]}
            ],
        }
        with self.assertRaises(FactionCardError):
            faction_cards_from_dict(doc)

    def test_no_card_field_is_a_numeric_quantity(self) -> None:
        hints = typing.get_type_hints(FactionCard)
        for declared in dataclasses.fields(FactionCard):
            with self.subTest(field=declared.name):
                self.assertNotIn(hints[declared.name], (int, float))
        names = [declared.name for declared in dataclasses.fields(FactionCard)]
        for token in METRIC_TOKENS:
            with self.subTest(token=token):
                self.assertEqual([name for name in names if token in name], [])


class ValidationTests(unittest.TestCase):
    """The validator must be able to fail, or it is not evidence."""

    def test_a_tag_attached_at_a_scope_it_does_not_declare_is_reported(self) -> None:
        model = load_faction_cards()
        model.roster["mis_scoped"] = FactionCard(
            identifier="mis_scoped",
            card_type="research",
            title="Mis-scoped research",
            control="",
            control_rationale="research is not controlled, recorded with a reason",
            tags=(Tag("asset", "REMOTE_VIEWING_TEAM"),),
        )
        problems = " | ".join(model.validate(tag_model=tag_model()))
        self.assertIn("not declared for scope", problems)

    def test_a_card_with_no_control_state_and_no_reason_is_reported(self) -> None:
        model = load_faction_cards()
        model.roster["silent_control"] = FactionCard(
            identifier="silent_control", card_type="organization", title="Silent"
        )
        problems = " | ".join(model.validate(tag_model=tag_model()))
        self.assertIn("no control state and no reason", problems)

    def test_a_dangling_produces_link_is_reported(self) -> None:
        model = load_faction_cards()
        model.roster["dangling"] = FactionCard(
            identifier="dangling",
            card_type="organization",
            title="Dangling",
            control="allied",
            produces=("no_such_card",),
        )
        problems = " | ".join(model.validate(tag_model=tag_model()))
        self.assertIn("does not resolve to a card", problems)

    def test_an_interaction_with_a_non_card_type_endpoint_is_reported(self) -> None:
        model = faction_cards_from_dict(
            {
                "format": FACTION_CARDS_FORMAT,
                "version": 1,
                "card_types": [{"id": t} for t in CARD_TYPE_IDS],
                "declared_interactions": [
                    {"id": "x", "source": "character", "target": "spaceship", "reason": "a reason"}
                ],
            }
        )
        problems = " | ".join(model.validate())
        self.assertIn("not a declared card type", problems)


class ProjectionTests(unittest.TestCase):
    """A faction card projects onto the shared primitive, or says why it cannot."""

    def setUp(self) -> None:
        self.model = load_faction_cards()

    def test_the_projectable_and_unprojectable_sets_partition_the_four_types(self) -> None:
        self.assertEqual(set(PROJECTABLE_TO_PRIMITIVE) | set(UNPROJECTABLE), set(CARD_TYPE_IDS))

    def test_an_organization_card_projects_with_empty_effects(self) -> None:
        card = to_card(self.model.get("archetype_advocacy_nonprofit"))
        self.assertIs(card.card_type, CardType.ORGANIZATION)
        self.assertIs(card.role, CardRole.PERSISTENT_RECORD)
        self.assertEqual(card.prerequisites, ())
        self.assertEqual(card.effects, ())
        self.assertTrue(all(":" in tag for tag in card.tags))

    def test_a_research_card_projects(self) -> None:
        self.assertIs(to_card(self.model.get("archetype_research_programme")).card_type, CardType.RESEARCH)

    def test_a_government_card_is_refused_by_name_because_the_primitive_has_no_member(self) -> None:
        with self.assertRaises(FactionCardError):
            to_card(self.model.get("archetype_municipal_government_relation"))
        self.assertNotIn("government", [member.value for member in CardType])
        self.assertIn("government", UNPROJECTABLE)


class RenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = load_faction_cards()

    def test_front_names_the_type_and_control(self) -> None:
        text = render_front(self.model.get("archetype_municipal_government_relation"))
        self.assertIn("government", text)
        self.assertIn("cooperating", text)

    def test_front_never_leaks_the_gm_notes(self) -> None:
        card = self.model.get("archetype_advocacy_nonprofit")
        card.gm_notes = "the patron is behind this organisation"
        self.assertNotIn(card.gm_notes, render_front(card))
        player = self.model.player_view(card)
        self.assertNotIn(card.gm_notes, json.dumps(player))
        self.assertIn(card.gm_notes, self.model.player_view(card, reveal_secrets=True)["gm_notes"])


class LoaderTests(unittest.TestCase):
    def test_missing_file_is_reported_as_a_card_error(self) -> None:
        with self.assertRaises(FactionCardError):
            load_faction_cards(Path(tempfile.gettempdir()) / "definitely_not_here.json")

    def test_wrong_format_and_version_are_refused(self) -> None:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        for mutate in ({"format": "something.else"}, {"version": 99}):
            broken = dict(payload)
            broken.update(mutate)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "cards.json"
                path.write_text(json.dumps(broken), encoding="utf-8")
                with self.assertRaises(FactionCardError):
                    load_faction_cards(path)


if __name__ == "__main__":
    unittest.main()
