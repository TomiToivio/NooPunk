"""Executable contracts for the founding story as a mechanical input (issue #346).

Code-only, per `AGENTS.md` and issue #271. These exercise the **roles, the edges and the validator**:
that the founder is a required edge rather than a name, that the patron's edge carries a goal of its own,
that belief and capability stay apart on a founder edge, that a state is one of the role's named
positions, that a divergence of goals is permitted rather than refused, and that every field the author
has not ruled on is empty **with a reason**.

They do not assert the setting's prose and no test here computes a magnitude, a transition rule or an
effect.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap, mirrors the sibling test modules
    sys.path.insert(0, str(ROOT))

from strategy_game.characters import Tag, load_character_cards  # noqa: E402
from strategy_game.faction_creation import load_faction_creation  # noqa: E402
from strategy_game.founding_story import (  # noqa: E402
    DATA_PATH,
    FOUNDER_STATES,
    FOUNDING_STORY_FORMAT,
    PATRON_STATES,
    ROLE_IDS,
    FoundingStory,
    load_founding_story,
    story_from_example,
)
from strategy_game.quantities import QUANTITY_IDS  # noqa: E402
from strategy_game.relationships import (  # noqa: E402
    RelationshipEdge,
    RelationshipError,
    RelationshipSet,
)

#: The real record ids the shipped examples may legitimately point at: the character roster and the
#: faction ids the character cards already use.
KNOWN_RECORDS = ("cpu", "uip", "ulp")

#: Keys that would mean a mechanic, a price or a scale had crept into the content file.
FORBIDDEN_KEYS = (
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
    "upkeep",
    "bonus",
)

#: Keys whose value must stay a **name**, never a number.
NAMED_POSITION_KEYS = ("state", "position", "primary", "quantity", "states")


def _walk(node: Any, path: tuple[str, ...] = ()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield path, str(key), value
            yield from _walk(value, (*path, str(key)))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, (*path, str(index)))


def _tag_kinds() -> dict[str, str]:
    return {tag.identifier: tag.kind for tag in load_faction_creation().tags.values()}


class RoleVocabularyTests(unittest.TestCase):
    """The two roles, their named positions and their edge kinds."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_founding_story()

    def test_the_two_roles_are_the_two_the_flow_names(self):
        self.assertEqual(set(self.model.roles), set(ROLE_IDS))

    def test_the_founder_states_are_the_design_comments_named_positions(self):
        self.assertEqual(self.model.states("founder"), FOUNDER_STATES)

    def test_the_patron_states_are_the_design_comments_named_positions(self):
        self.assertEqual(self.model.states("patron"), PATRON_STATES)

    def test_each_role_uses_its_own_edge_kind(self):
        self.assertEqual(self.model.role("founder").edge_kind, "founded_by")
        self.assertEqual(self.model.role("patron").edge_kind, "patron_of")

    def test_a_built_edge_carries_its_roles_vocabulary_and_no_numbers(self):
        edge = self.model.edge(
            "patron",
            identifier="probe",
            holder_id="sir_mars_eldrich",
            other_id="ulp",
            state="aligned",
            goals=("colonise Mars",),
        )
        self.assertEqual(edge.role, "patron")
        self.assertEqual(edge.kind, "patron_of")
        self.assertEqual(edge.state_vocabulary, PATRON_STATES)
        self.assertFalse(any(isinstance(value, (int, float)) for value in edge.to_dict().values()))

    def test_the_roles_quantity_claims_name_real_quantities(self):
        self.assertEqual(self.model.off_vocabulary(), ())
        for role in self.model.roles.values():
            with self.subTest(role=role.identifier):
                self.assertTrue(role.quantities_touched)
                for name in role.quantities_touched:
                    self.assertIn(name, QUANTITY_IDS)

    def test_the_patron_cannot_buy_opinion_or_seats_and_that_is_declared_not_enforced(self):
        """The ceiling is a canon row recorded as data; nothing in the layer refuses on it."""
        patron = self.model.role("patron")
        self.assertEqual(set(patron.cannot_move), {"opinion_support", "legislative_representation"})
        self.assertIn("DECLARED, NOT ENFORCED", patron.cannot_move_note)

    def test_the_founder_is_the_source_of_legitimacy_and_the_patron_is_not(self):
        self.assertIn("institutional_access", self.model.role("founder").quantities_touched)
        self.assertIn("discursive_hegemony", self.model.role("founder").quantities_touched)
        self.assertIn("membership_resources", self.model.role("patron").quantities_touched)
        self.assertNotIn("opinion_support", self.model.role("patron").quantities_touched)


class StoryValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_founding_story()
        cls.patron = story_from_example(cls.model, "eldrich_patron_of_ulp")
        cls.founder = story_from_example(cls.model, "placeholder_founder_edge")

    def _combined(self) -> FoundingStory:
        return FoundingStory(
            faction_id="ulp",
            founder_edge=self.founder.founder_edge,
            patron_edge=self.patron.patron_edge,
        )

    def test_a_story_without_a_founder_edge_is_reported(self):
        problems = " | ".join(self.model.validate(self.patron))
        self.assertIn("no founder edge", problems)
        self.assertIn("step 2", problems)

    def test_a_patron_edge_without_a_goal_is_reported(self):
        patron = self.model.edge(
            "patron",
            identifier="patron_without_a_goal",
            holder_id="sir_mars_eldrich",
            other_id="ulp",
            state="aligned",
            tags=("indebted",),
        )
        story = FoundingStory(faction_id="ulp", founder_edge=self.founder.founder_edge, patron_edge=patron)
        problems = " | ".join(self.model.validate(story))
        self.assertIn("carries no goal", problems)

    def test_a_state_from_the_other_roles_vocabulary_is_reported(self):
        edge = self.model.edge(
            "founder",
            identifier="founder_with_a_patron_state",
            holder_id="placeholder_leader_cosmist",
            other_id="cosmist_international",
            state="divergent",
            goals=("DISCLOSE_UFO_SECRETS",),
        )
        story = FoundingStory(faction_id="cosmist_international", founder_edge=edge)
        problems = " | ".join(self.model.validate(story))
        self.assertIn("divergent", problems)

    def test_an_empty_state_with_a_reason_is_accepted_and_without_one_is_not(self):
        without = FoundingStory(
            faction_id="cosmist_international",
            founder_edge=self.model.edge(
                "founder",
                identifier="founder_unstated",
                holder_id="placeholder_leader_cosmist",
                other_id="cosmist_international",
                goals=("DISCLOSE_UFO_SECRETS",),
            ),
        )
        self.assertIn("empty with no reason", " | ".join(self.model.validate(without)))
        with_reason = FoundingStory(
            faction_id="cosmist_international",
            founder_edge=self.model.edge(
                "founder",
                identifier="founder_unstated",
                holder_id="placeholder_leader_cosmist",
                other_id="cosmist_international",
                state_rationale="the author has not said what condition the founder is in",
                goals=("DISCLOSE_UFO_SECRETS",),
            ),
        )
        self.assertEqual(self.model.validate(with_reason), ())

    def test_belief_is_not_competence_on_a_founder_edge(self):
        """A competent researcher whose thesis is falsified is a different game from a fraud."""
        rigorous = self.model.edge(
            "founder",
            identifier="founder_wrong_but_rigorous",
            holder_id="placeholder_leader_cosmist",
            other_id="cosmist_international",
            state="discredited",
            typed_tags=(
                Tag("belief", "QIP_PANPSYCHIST"),
                Tag("competence", "literature synthesis and method criticism"),
            ),
        )
        story = FoundingStory(faction_id="cosmist_international", founder_edge=rigorous)
        self.assertEqual(self.model.validate(story, tag_vocabulary=_tag_kinds()), ())

        conflated = self.model.edge(
            "founder",
            identifier="founder_conflated",
            holder_id="placeholder_leader_cosmist",
            other_id="cosmist_international",
            state="discredited",
            typed_tags=(Tag("competence", "QIP_PANPSYCHIST"),),
        )
        problems = " | ".join(
            self.model.validate(
                FoundingStory(faction_id="cosmist_international", founder_edge=conflated),
                tag_vocabulary=_tag_kinds(),
            )
        )
        self.assertIn("QIP_PANPSYCHIST", problems)
        self.assertIn("belief is not capability", problems)

    def test_a_patrons_goal_need_not_be_one_the_faction_shares(self):
        """The divergence IS the mechanic, so a rule refusing it would be the defect."""
        story = self._combined()
        faction_tags = load_faction_creation().template.get("tags") or []
        self.assertEqual(self.model.validate(story, faction_tag_ids=faction_tags), ())
        self.assertEqual(self.model.unshared_goals(story, faction_tags), ("colonise Mars",))
        self.assertIn("deliberately not treated as a problem", story.note)

    def test_an_unknown_endpoint_is_reported_when_the_known_set_is_supplied(self):
        roster_ids = tuple(card.identifier for card in load_character_cards())
        known_real = (*roster_ids, *KNOWN_RECORDS, "cosmist_international")
        # The placeholder founder endpoint is honestly NOT a real record, and saying so is the point
        # of marking the example a placeholder rather than canon.
        self.assertIn(
            "placeholder_leader_cosmist",
            " | ".join(self.model.validate(self._combined(), known_endpoint_ids=known_real)),
        )
        real_endpoints = FoundingStory(
            faction_id="ulp",
            founder_edge=self.model.edge(
                "founder",
                identifier="founder_on_the_record",
                holder_id="ulp",
                other_id="cosmist_international",
                state="ascendant",
                tags=("mentor",),
                goals=("DISCLOSE_UFO_SECRETS",),
            ),
            patron_edge=self.patron.patron_edge,
        )
        self.assertEqual(self.model.validate(real_endpoints, known_endpoint_ids=known_real), ())

    def test_an_edge_from_a_record_to_itself_is_refused_at_construction(self):
        """The record is pairwise, so a self-tie never reaches validation."""
        with self.assertRaises(RelationshipError):
            self.model.edge(
                "founder",
                identifier="self_referential",
                holder_id="ulp",
                other_id="ulp",
                state="ascendant",
                goals=("DISCLOSE_UFO_SECRETS",),
            )

    def test_the_missing_founder_is_the_only_problem_with_the_canon_patron_example(self):
        roster_ids = tuple(card.identifier for card in load_character_cards())
        problems = self.model.validate(self.patron, known_endpoint_ids=(*roster_ids, *KNOWN_RECORDS))
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("no founder edge", problems[0])

    def test_the_placeholder_founder_example_validates_when_its_placeholders_are_known(self):
        self.assertEqual(
            self.model.validate(
                self.founder,
                known_endpoint_ids=("placeholder_leader_cosmist", "cosmist_international"),
                tag_vocabulary=_tag_kinds(),
            ),
            (),
        )


class ShippedDocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_founding_story()
        cls.payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    def test_the_document_declares_its_format(self):
        self.assertEqual(self.payload["format"], FOUNDING_STORY_FORMAT)
        self.assertTrue(self.model.sources)

    def test_the_shared_record_is_the_one_the_council_layer_uses(self):
        self.assertEqual(
            self.model.shared_edge.get("record"), "strategy_game.relationships.RelationshipEdge"
        )
        edge = story_from_example(self.model, "eldrich_patron_of_ulp").patron_edge
        self.assertIsInstance(edge, RelationshipEdge)

    def test_the_static_card_tie_and_the_stateful_edge_carry_the_same_ids(self):
        card = load_character_cards().get("sir_mars_eldrich")
        declared = card.relationships[0]
        edge = story_from_example(self.model, "eldrich_patron_of_ulp").patron_edge
        assert edge is not None
        self.assertEqual(edge.holder_id, card.identifier)
        self.assertEqual(edge.other_id, declared.other_id)
        self.assertEqual(edge.kind, declared.kind)
        self.assertIs(edge.visibility, declared.visibility)
        self.assertEqual(edge.state, "divergent")
        self.assertEqual(edge.goals, ("colonise Mars",))

    def test_the_shipped_edge_validates_against_the_real_roster(self):
        edge = story_from_example(self.model, "eldrich_patron_of_ulp").patron_edge
        assert edge is not None
        roster_ids = tuple(card.identifier for card in load_character_cards())
        self.assertEqual(
            RelationshipSet([edge]).validate(known_endpoint_ids=(*roster_ids, *KNOWN_RECORDS)), ()
        )

    def test_no_secret_is_added_to_any_named_character(self):
        for example in self.model.examples:
            self.assertFalse(example.get("gm_notes"), example.get("id"))

    def test_every_declared_state_effect_is_unapproved_with_a_reason(self):
        for role in self.model.roles.values():
            with self.subTest(role=role.identifier):
                self.assertIs(role.state_effects.get("declared"), False)
                self.assertTrue(role.state_effects.get("reason"))
        self.assertIs(self.model.transitions.get("declared"), False)
        self.assertTrue(self.model.transitions.get("reason"))

    def test_the_founder_role_records_that_it_is_not_one_of_the_four_leaders(self):
        """The authority question is flagged, not answered."""
        questions = {item["id"] for item in self.model.role("founder").pending_author_decisions}
        self.assertIn("founder_authority", questions)
        for role in self.model.roles.values():
            for item in role.pending_author_decisions:
                self.assertTrue(item.get("container_instead"))

    def test_every_pending_decision_carries_the_reason_it_is_open(self):
        self.assertTrue(self.model.pending_decisions())
        self.assertEqual(self.model.unreasoned_decisions(), ())
        for item in self.model.pending_decisions():
            with self.subTest(decision=item.get("id")):
                self.assertTrue(item.get("container_instead"))

    def test_the_patron_seat_question_is_open_rather_than_defaulted(self):
        questions = {
            item["id"] for item in self.model.role("patron").pending_author_decisions
        }
        self.assertIn("patron_seat", questions)
        self.assertIn("severed_edge_fate", questions)

    def test_no_numeric_mechanic_or_numeric_named_position_in_the_data(self):
        for path, key, value in _walk(self.payload):
            with self.subTest(path="/".join(path), key=key):
                self.assertNotIn(key, FORBIDDEN_KEYS)
                if key in NAMED_POSITION_KEYS:
                    self.assertFalse(isinstance(value, (int, float)) and not isinstance(value, bool))

    def test_a_module_level_state_can_change_and_the_change_is_logged(self):
        edge = story_from_example(self.model, "eldrich_patron_of_ulp").patron_edge
        assert edge is not None
        edge.reassign_state("withdrawing", reason="the financing stopped")
        self.assertEqual(edge.state, "withdrawing")
        self.assertEqual(edge.state_history, ("divergent",))

    def test_a_document_that_is_not_a_founding_story_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            trap = Path(folder) / "not_a_founding_story.json"
            trap.write_text(json.dumps({"format": "noopunk.something.else"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_founding_story(trap)


if __name__ == "__main__":
    unittest.main()
