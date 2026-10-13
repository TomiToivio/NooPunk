"""Executable contracts for the one stateful relationship edge (issues #323 and #346).

Code-only, per `AGENTS.md` and issue #271. These exercise the **record and the validator**: that the
edge is sparse rather than dense, that a state is a named position rather than a number, that an empty
field must carry a reason, that belief and capability stay apart, that a tie can change, and that GM
material is withheld by the code.

They do not assert what any tie says, and no test here computes affinity, opinion, trust, a modifier or
a threshold.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import dataclasses
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap, mirrors the sibling test modules
    sys.path.insert(0, str(ROOT))

from strategy_game.characters import Tag, load_character_cards  # noqa: E402
from strategy_game.faction_creation import load_faction_creation  # noqa: E402
from strategy_game.relationships import (  # noqa: E402
    EDGE_KINDS,
    RELATIONSHIP_TAGS,
    RelationshipEdge,
    RelationshipError,
    RelationshipSet,
    edge_from_dict,
)
from strategy_game.tabletop.cards import CardVisibility  # noqa: E402

#: Field names that would mean a DRAFT numeric scale had been implemented. The council specification
#: proposes sparse ``opinion`` and ``trust`` integers and marks them DRAFT; no scale is approved, so a
#: field of this name appearing on the edge is a regression this contract catches.
FORBIDDEN_SCALE_FIELDS = (
    "opinion",
    "trust",
    "affinity",
    "score",
    "modifier",
    "difficulty",
    "threshold",
    "magnitude",
    "stat",
    "stats",
    "attributes",
    "skill",
)

#: The founder's and the patron's named positions, as the design comment lists them. Repeated here
#: rather than imported so a change to the shipped vocabulary has to be made deliberately in both.
FOUNDER_STATES = ("ascendant", "contested", "discredited", "superseded", "departed")
PATRON_STATES = ("aligned", "divergent", "conditional", "withdrawing", "captured", "severed")


def _vocabulary() -> dict[str, str]:
    """Issue #346's tag ids mapped to their declared kind — the belief/capability guard's input."""
    model = load_faction_creation()
    return {tag.identifier: tag.kind for tag in model.tags.values()}


def _edge(**overrides: Any) -> RelationshipEdge:
    base: dict[str, Any] = dict(
        identifier="edge",
        holder_id="sir_mars_eldrich",
        other_id="ulp",
        kind="patron_of",
        role="patron",
        state="divergent",
        state_vocabulary=PATRON_STATES,
        tags=("indebted",),
        goals=("colonise Mars",),
    )
    base.update(overrides)
    return RelationshipEdge(**base)


class SparseRecordTests(unittest.TestCase):
    """The record is sparse and pairwise: no authored tie means unmodelled, not zero."""

    def test_two_unmodelled_records_have_no_edge_and_that_is_not_zero(self):
        edges = RelationshipSet([_edge()])
        self.assertEqual(edges.between("placeholder_a", "placeholder_b"), ())
        self.assertEqual(len(edges.between("sir_mars_eldrich", "ulp")), 1)

    def test_between_is_symmetric(self):
        edges = RelationshipSet([_edge()])
        self.assertEqual(
            edges.between("ulp", "sir_mars_eldrich"), edges.between("sir_mars_eldrich", "ulp")
        )

    def test_a_tie_to_oneself_is_refused(self):
        with self.assertRaises(RelationshipError):
            _edge(holder_id="ulp", other_id="ulp")

    def test_an_identifier_must_be_a_stable_slug(self):
        with self.assertRaises(RelationshipError):
            _edge(identifier="Not A Slug")

    def test_duplicate_identifiers_are_refused_by_the_set(self):
        with self.assertRaises(RelationshipError):
            RelationshipSet([_edge(), _edge()])

    def test_edges_touching_a_record_can_be_listed(self):
        edges = RelationshipSet([_edge(), _edge(identifier="other", holder_id="ulp", other_id="npc")])
        self.assertEqual(len(edges.of("ulp")), 2)


class NamedStateTests(unittest.TestCase):
    """A condition is a named position; a number in that field is refused with a reason."""

    def test_a_state_outside_the_declared_vocabulary_is_reported(self):
        edge = _edge(state="mildly_miffed")
        problems = " | ".join(RelationshipSet([edge]).validate())
        self.assertIn("mildly_miffed", problems)
        self.assertIn("named position", problems)

    def test_a_number_in_the_state_field_is_refused_and_says_why(self):
        edge = _edge(state=0.5)
        problems = " | ".join(RelationshipSet([edge]).validate())
        self.assertIn("0.5", problems)
        self.assertIn("a number", problems)

    def test_a_state_with_no_declared_vocabulary_cannot_be_checked_and_is_reported(self):
        edge = _edge(state="divergent", state_vocabulary=())
        problems = " | ".join(RelationshipSet([edge]).validate())
        self.assertIn("no declared vocabulary", problems)

    def test_an_empty_state_without_a_reason_is_reported(self):
        edge = _edge(state="", state_rationale="")
        problems = " | ".join(RelationshipSet([edge]).validate())
        self.assertIn("empty with no reason", problems)

    def test_an_empty_state_with_a_reason_is_accepted(self):
        edge = _edge(state="", state_rationale="the author has not said what condition the tie is in")
        self.assertEqual(RelationshipSet([edge]).validate(), ())

    def test_a_state_can_change_and_the_previous_one_is_logged(self):
        edge = _edge()
        previous = edge.reassign_state("withdrawing", reason="the financing stopped")
        self.assertEqual(previous, "divergent")
        self.assertEqual(edge.state, "withdrawing")
        self.assertEqual(edge.state_history, ("divergent",))
        self.assertEqual(edge.detail.get("last_state_reason"), "the financing stopped")

    def test_a_change_to_an_undeclared_state_is_refused(self):
        edge = _edge()
        with self.assertRaises(RelationshipError):
            edge.reassign_state("vibes")
        self.assertEqual(edge.state, "divergent")

    def test_a_severed_edge_is_read_not_deleted(self):
        edge = _edge(state="severed")
        self.assertTrue(edge.is_severed)
        self.assertIn(edge.identifier, RelationshipSet([edge]).edges)

    def test_a_patron_state_is_not_a_founder_state(self):
        self.assertEqual(set(FOUNDER_STATES) & set(PATRON_STATES), set())
        wrong_role = _edge(state="divergent", state_vocabulary=FOUNDER_STATES, role="founder")
        problems = " | ".join(RelationshipSet([wrong_role]).validate())
        self.assertIn("divergent", problems)
        self.assertIn("not one of", problems)


class BeliefIsNotCapabilityTests(unittest.TestCase):
    """Issue #346: the kind of a tag is what stops a doctrine being read as a capability."""

    def test_an_id_declared_as_a_belief_may_not_be_attached_as_a_competence(self):
        edge = _edge(typed_tags=(Tag("competence", "MATERIALIST"),))
        problems = " | ".join(RelationshipSet([edge]).validate(tag_vocabulary=_vocabulary()))
        self.assertIn("MATERIALIST", problems)
        self.assertIn("belief is not capability", problems)

    def test_an_id_declared_as_a_competence_may_not_be_attached_as_a_belief(self):
        edge = _edge(typed_tags=(Tag("belief", "REMOTE_VIEWER"),))
        problems = " | ".join(RelationshipSet([edge]).validate(tag_vocabulary=_vocabulary()))
        self.assertIn("REMOTE_VIEWER", problems)

    def test_a_correctly_typed_pair_validates(self):
        edge = _edge(
            typed_tags=(
                Tag("belief", "MATERIALIST"),
                Tag("competence", "REMOTE_VIEWER"),
            )
        )
        self.assertEqual(RelationshipSet([edge]).validate(tag_vocabulary=_vocabulary()), ())

    def test_free_text_tags_are_the_norm_and_are_not_reported(self):
        """A materialist trained remote viewer is representable; so is an authored competence line."""
        edge = _edge(typed_tags=(Tag("competence", "literature synthesis and method criticism"),))
        self.assertEqual(RelationshipSet([edge]).validate(tag_vocabulary=_vocabulary()), ())

    def test_an_unknown_tag_kind_is_refused_on_construction(self):
        with self.assertRaises(ValueError):
            Tag("vibes", "AUTONOMIST_MARXIST")


class EdgeVocabularyTests(unittest.TestCase):
    def test_an_unknown_kind_or_tag_is_reported_rather_than_coerced(self):
        edge = _edge(kind="owes_a_favour_to", tags=("indebted", "frenemy"))
        problems = " | ".join(RelationshipSet([edge]).validate())
        self.assertIn("owes_a_favour_to", problems)
        self.assertIn("frenemy", problems)
        self.assertIn("open", problems)

    def test_the_declared_kinds_and_tags_are_the_documents_lists(self):
        self.assertIn("patron_of", EDGE_KINDS)
        self.assertIn("founded_by", EDGE_KINDS)
        for tag in ("friend", "rival", "family", "mentor", "indebted", "suspicious", "former_ally"):
            self.assertIn(tag, RELATIONSHIP_TAGS)

    def test_a_tie_with_no_tag_and_no_goal_is_reported(self):
        edge = _edge(tags=(), goals=(), typed_tags=())
        problems = " | ".join(RelationshipSet([edge]).validate())
        self.assertIn("carries nothing", problems)

    def test_an_unknown_endpoint_is_reported_when_the_known_set_is_supplied(self):
        edge = _edge()
        problems = " | ".join(
            RelationshipSet([edge]).validate(known_endpoint_ids={"someone_else"})
        )
        self.assertIn("ulp", problems)
        self.assertEqual(RelationshipSet([edge]).validate(known_endpoint_ids={"ulp", "sir_mars_eldrich"}), ())

    def test_a_missing_edge_is_reported_by_name(self):
        with self.assertRaises(RelationshipError):
            RelationshipSet().get("no_such_edge")


class PlayerViewTests(unittest.TestCase):
    def test_the_gm_note_is_withheld_by_the_code(self):
        edge = _edge(gm_notes="the author's to write")
        view = RelationshipSet([edge]).player_view(edge)
        self.assertNotIn("the author's to write", str(view))
        self.assertIn("redacted", str(view["gm_notes"]))
        self.assertIn("the author's to write", str(RelationshipSet([edge]).player_view(edge, reveal_secrets=True)))

    def test_observation_and_inference_stay_two_lists(self):
        edge = _edge(
            observable=("he funds the party and owns sympathetic media",),
            inferences=("that the party is his instrument",),
        )
        view = RelationshipSet([edge]).player_view(edge)
        self.assertEqual(view["observable"], ["he funds the party and owns sympathetic media"])
        self.assertEqual(view["inferences"], ["that the party is his instrument"])


class SharedRecordTests(unittest.TestCase):
    """The design instruction: the founding edges reuse the council layer's record, not a parallel one."""

    def test_a_card_tie_upgrades_into_a_stateful_edge_keeping_its_direction(self):
        card = load_character_cards().get("sir_mars_eldrich")
        self.assertTrue(card.relationships, "the canon patron card should declare a tie")
        edges = RelationshipSet.from_card_relationships(
            card.identifier,
            card.relationships,
            role="patron",
            state="divergent",
            state_vocabulary=PATRON_STATES,
        )
        declared = card.relationships[0]
        self.assertEqual(edges[0].holder_id, card.identifier)
        self.assertEqual(edges[0].other_id, declared.other_id)
        self.assertEqual(edges[0].kind, declared.kind)
        self.assertIs(edges[0].visibility, declared.visibility)
        self.assertEqual(edges[0].state, "divergent")
        self.assertEqual(edges[0].state_vocabulary, PATRON_STATES)

    def test_the_round_trip_through_a_record_keeps_the_named_state(self):
        edge = _edge()
        restored = edge_from_dict(edge.to_dict())
        self.assertEqual(restored.state, edge.state)
        self.assertEqual(restored.state_vocabulary, edge.state_vocabulary)
        self.assertEqual(restored.tags, edge.tags)
        self.assertEqual(restored.goals, edge.goals)

    def test_a_record_without_an_id_is_refused(self):
        with self.assertRaises(RelationshipError):
            edge_from_dict({"holder_id": "a", "other_id": "b"})

    def test_the_edge_declares_no_numeric_scale_field(self):
        """A DRAFT opinion or trust integer is not implemented, so this contract fails if one appears."""
        names = {item.name for item in dataclasses.fields(RelationshipEdge)}
        for forbidden in FORBIDDEN_SCALE_FIELDS:
            self.assertNotIn(forbidden, names)

    def test_the_default_visibility_is_public(self):
        self.assertIs(_edge().visibility, CardVisibility.PUBLIC)


if __name__ == "__main__":
    unittest.main()
