"""Executable contracts for the council, portfolio, mission and relationship layer (issue #323).

Code-only, per `AGENTS.md` and issue #271. These exercise the **two validators and the structural
readings**: that the issue's own requirements are refused by name (a leaderless mission, two missions
for one leader, more moves than leader-turns, a move that names no quantity, two leaders in one post),
that everything the author has not ruled on is *reported* rather than refused, that the four offices can
disagree, that a relationship is read rather than scored, and that nothing here resolves a mission.

No test computes a magnitude, a threshold, a turn, an economy or an outcome.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap, mirrors the sibling test modules
    sys.path.insert(0, str(ROOT))

from strategy_game.council import (  # noqa: E402
    COUNCIL_FORMAT,
    DATA_PATH,
    LEADER_STATUSES,
    PORTFOLIO_IDS,
    Council,
    CouncilLeader,
    MissionDeclaration,
    load_council,
)
from strategy_game.founding_story import load_founding_story, story_from_example  # noqa: E402
from strategy_game.quantities import QUANTITY_IDS  # noqa: E402
from strategy_game.relationships import RelationshipEdge, RelationshipSet  # noqa: E402

#: Keys that would mean a price, a scale or a resolution had crept into the content file.
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
NAMED_POSITION_KEYS = ("state", "position", "primary", "quantity", "status")


def _walk(node: Any, path: tuple[str, ...] = ()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield path, str(key), value
            yield from _walk(value, (*path, str(key)))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, (*path, str(index)))


def _leaders() -> tuple[CouncilLeader, ...]:
    return tuple(
        CouncilLeader(identifier=f"leader_{index}", name=f"Leader {index}", portfolio=portfolio)
        for index, portfolio in enumerate(PORTFOLIO_IDS, start=1)
    )


def _mission(index: int, quantity: str, **overrides: Any) -> MissionDeclaration:
    base: dict[str, Any] = dict(
        identifier=f"mission_{index}",
        leader_id=f"leader_{index}",
        kind="organise",
        target_id=f"target_{index}",
        location_id=f"district_{index}",
        quantity=quantity,
        authorised_by="principal",
    )
    base.update(overrides)
    return MissionDeclaration(**base)


def _council(**overrides: Any) -> Council:
    base: dict[str, Any] = dict(
        identifier="council",
        principal_id="principal",
        leaders=_leaders(),
        missions=tuple(
            _mission(index, quantity)
            for index, quantity in enumerate(
                ("institutional_access", "opinion_support", "membership_resources", "discursive_hegemony"),
                start=1,
            )
        ),
    )
    base.update(overrides)
    return Council(**base)


class PortfolioTests(unittest.TestCase):
    """The four offices: what each decides, which quantity it serves, and how they disagree."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_council()

    def test_the_document_declares_its_format_and_exactly_four_offices(self):
        payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(payload["format"], COUNCIL_FORMAT)
        self.assertEqual(set(self.model.portfolios), set(PORTFOLIO_IDS))
        self.assertEqual(self.model.council_size, 4)
        self.assertTrue(self.model.sources)

    def test_every_office_says_what_it_decides_and_which_quantity_it_serves(self):
        for portfolio in self.model.portfolios.values():
            with self.subTest(office=portfolio.identifier):
                self.assertTrue(portfolio.decides)
                self.assertTrue(portfolio.serves)
                self.assertTrue(portfolio.standing_position)
                self.assertTrue(portfolio.argues_for)
                self.assertIn(portfolio.primary, portfolio.serves)

    def test_the_four_offices_do_not_serve_one_quantity(self):
        """A council whose members always agree is a council whose four offices serve one quantity."""
        report = self.model.shared_interest_report()
        self.assertFalse(report["all_four_serve_one_quantity"])
        self.assertGreaterEqual(len(report["distinct_primaries"]), 3)
        self.assertEqual(report["shared_primaries"], {})

    def test_all_six_quantities_are_claimed_by_some_office(self):
        self.assertEqual(self.model.unclaimed_quantities(), ())
        for portfolio in self.model.portfolios.values():
            for name in portfolio.serves:
                self.assertIn(name, QUANTITY_IDS)

    def test_the_worked_turn_pursues_four_of_six_and_names_the_two_it_leaves(self):
        council = self.model.worked_example_council()
        unpursued = self.model.unpursued_quantities(council)
        self.assertEqual(len(unpursued), 2)
        self.assertEqual(
            set(unpursued), set(QUANTITY_IDS) - {mission.quantity for mission in council.missions}
        )
        self.assertEqual(self.model.structural_problems(council), ())

    def test_an_office_whose_primary_is_not_a_quantity_is_reported(self):
        model = load_council()
        model.portfolios["politics_diplomacy"].primary = "influence"
        self.assertIn(("politics_diplomacy", "primary", "influence"), model.off_vocabulary())

    def test_the_passive_magnitude_is_unapproved_with_a_reason(self):
        for portfolio in self.model.portfolios.values():
            with self.subTest(office=portfolio.identifier):
                self.assertIs(portfolio.passive.magnitude_declared, False)
                self.assertIn(portfolio.passive.quantity, QUANTITY_IDS)
                self.assertTrue(portfolio.passive.reason)


class StructuralRuleTests(unittest.TestCase):
    """The checks issue #323 states as acceptance criteria, refused by name."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_council()

    def test_a_well_formed_council_has_no_structural_problem(self):
        self.assertEqual(self.model.structural_problems(_council()), ())

    def test_a_mission_without_a_leader_is_invalid(self):
        council = _council(missions=(_mission(1, "opinion_support", leader_id=""),))
        problems = " | ".join(self.model.structural_problems(council))
        self.assertIn("no leader", problems)
        self.assertIn("exactly one named leader", problems)

    def test_one_leader_cannot_lead_two_missions_in_a_turn(self):
        council = _council(
            missions=(
                _mission(1, "opinion_support"),
                _mission(2, "membership_resources", leader_id="leader_1"),
            )
        )
        problems = " | ".join(self.model.structural_problems(council))
        self.assertIn("leader_1", problems)
        self.assertIn("at most one active mission per leader per turn", problems)

    def test_more_moves_than_leader_turns_is_refused(self):
        council = _council(
            missions=tuple(
                _mission(index, quantity, leader_id=f"leader_{index}")
                for index, quantity in enumerate(
                    ("opinion_support", "membership_resources", "institutional_access",
                     "discursive_hegemony", "opinion_support"),
                    start=1,
                )
            )
        )
        problems = " | ".join(self.model.structural_problems(council))
        self.assertIn("5 missions declared against 4 leader-turns", problems)
        self.assertIn("never add one", problems)

    def test_a_mission_must_name_one_of_the_six_quantities(self):
        unnamed = _council(missions=(_mission(1, ""),))
        self.assertIn("names no quantity", " | ".join(self.model.structural_problems(unnamed)))
        unknown = _council(missions=(_mission(1, "influence"),))
        problems = " | ".join(self.model.structural_problems(unknown))
        self.assertIn("influence", problems)
        self.assertIn("not one of the six", problems)

    def test_a_mission_needs_a_target_and_an_authoriser(self):
        council = _council(missions=(_mission(1, "opinion_support", target_id="", authorised_by=""),))
        problems = " | ".join(self.model.structural_problems(council))
        self.assertIn("no target", problems)
        self.assertIn("nobody authorised it", problems)

    def test_a_leader_outside_the_roster_is_refused(self):
        council = _council(missions=(_mission(1, "opinion_support", leader_id="someone_else"),))
        problems = " | ".join(self.model.structural_problems(council))
        self.assertIn("someone_else", problems)
        self.assertIn("not in this faction's roster", problems)

    def test_one_post_cannot_be_held_by_two_leaders(self):
        leaders = tuple(
            CouncilLeader(identifier=f"leader_{index}", portfolio=PORTFOLIO_IDS[0])
            for index in range(1, 3)
        )
        council = _council(leaders=leaders, missions=())
        problems = " | ".join(self.model.structural_problems(council))
        self.assertIn("held by both", problems)

    def test_an_unknown_office_or_status_is_refused(self):
        leaders = (CouncilLeader(identifier="leader_1", portfolio="shadow_cabinet", status="vibing"),)
        problems = " | ".join(self.model.structural_problems(_council(leaders=leaders, missions=())))
        self.assertIn("shadow_cabinet", problems)
        self.assertIn("vibing", problems)

    def test_a_mission_may_not_draw_on_a_patron_edge_that_does_not_exist(self):
        council = _council(
            missions=(_mission(1, "opinion_support", patron_edge_id="no_such_edge"),)
        )
        self.assertEqual(self.model.structural_problems(council), ())
        problems = " | ".join(
            self.model.structural_problems(council, edges=_patron_edges())
        )
        self.assertIn("no_such_edge", problems)

    def test_the_central_rule_is_recorded_and_unapproved(self):
        rule = self.model.central_rule
        self.assertEqual(rule.get("id"), "one_named_leader_per_active_move")
        self.assertIs(rule.get("approved"), False)
        self.assertTrue(rule.get("structural_checks"))


def _patron_edges() -> RelationshipSet:
    story = story_from_example(load_founding_story(), "eldrich_patron_of_ulp")
    assert story.patron_edge is not None
    return RelationshipSet([story.patron_edge])


def _leader_tie() -> RelationshipSet:
    """A tie from a mission's leader to its target, so the edge is the one the mission reads."""
    return RelationshipSet(
        [
            RelationshipEdge(
                identifier="leader_1_indebted_to_ulp",
                holder_id="leader_1",
                other_id="ulp",
                kind="indebted_to",
                tags=("indebted",),
                state_rationale="the author has declared no named positions for this tie",
            )
        ]
    )


class ReportedConsequenceTests(unittest.TestCase):
    """Everything whose effect is still unauthored is reported, never refused."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_council()

    def test_a_draft_no_mission_status_is_reported_not_refused(self):
        leaders = tuple(
            CouncilLeader(
                identifier=leader.identifier,
                portfolio=leader.portfolio,
                status="injured" if leader.identifier == "leader_1" else "",
            )
            for leader in _leaders()
        )
        council = _council(leaders=leaders)
        self.assertEqual(self.model.structural_problems(council), ())
        reports = " | ".join(self.model.consequence_reports(council))
        self.assertIn("injured", reports)
        self.assertIn("DRAFT status table", reports)
        self.assertIn("reported rather than refused", reports)

    def test_the_status_vocabulary_is_the_specifications_and_every_row_is_unenforced(self):
        self.assertEqual(
            {row.status for row in self.model.status_rows}, set(LEADER_STATUSES)
        )
        self.assertIs(self.model.status_record.get("enforced"), False)
        self.assertTrue(self.model.status_record.get("reason"))

    def test_a_refusal_is_a_described_slot_and_the_rule_is_open(self):
        council = _council(missions=(_mission(1, "opinion_support", refusals=("leader_1",)),))
        self.assertEqual(self.model.structural_problems(council), ())
        reports = " | ".join(self.model.consequence_reports(council))
        self.assertIn("contested by", reports)
        self.assertIn("D6", reports)

    def test_a_roster_that_is_not_four_is_reported_and_the_question_is_left_open(self):
        council = _council(leaders=_leaders()[:3], missions=())
        self.assertEqual(self.model.structural_problems(council), ())
        reports = " | ".join(self.model.consequence_reports(council))
        self.assertIn("3 leaders against 4 slots", reports)
        self.assertIn("#346", reports)

    def test_the_roster_size_question_is_flagged_rather_than_resolved(self):
        record = self.model.council_size_record
        self.assertIs(record.get("approved"), False)
        self.assertTrue(record.get("not_this_question"))
        questions = {item.get("id") for item in self.model.pending_decisions()}
        self.assertIn("roster_size", questions)
        self.assertIn("founder_authority", questions)

    def test_a_patron_drawing_mission_is_a_dependence_debt(self):
        council = _council(
            missions=(_mission(1, "opinion_support", patron_edge_id="eldrich_patron_of_ulp"),)
        )
        reports = " | ".join(
            self.model.consequence_reports(council, edges=_patron_edges())
        )
        self.assertIn("dependence debt", reports)
        self.assertIn("#346", reports)

    def test_a_declared_resource_is_named_and_not_priced(self):
        council = _council(
            missions=(_mission(1, "opinion_support", allocated_resource_ids=("lab",)),)
        )
        reports = " | ".join(self.model.consequence_reports(council))
        self.assertIn("lab", reports)
        self.assertIn("Named, not priced", reports)

    def test_a_mission_authorised_by_someone_other_than_the_principal_is_reported(self):
        council = _council(
            missions=(_mission(1, "opinion_support", authorised_by="the_council"),)
        )
        self.assertEqual(self.model.structural_problems(council), ())
        self.assertIn(
            "the_council", " | ".join(self.model.consequence_reports(council))
        )

    def test_the_turn_unit_and_the_leader_card_are_left_to_the_author(self):
        questions = {item.get("id") for item in self.model.pending_decisions()}
        self.assertIn("turn_unit", questions)
        self.assertIn("leader_attributes", questions)
        self.assertIn("refusal_effect", questions)


class RelationshipChannelTests(unittest.TestCase):
    """How a personal tie reaches the strategic layer, and how nothing is granted by it."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_council()
        cls.story = story_from_example(load_founding_story(), "eldrich_patron_of_ulp")

    def test_the_patron_tie_opens_the_declared_channels_and_grants_nothing(self):
        edge = self.story.patron_edge
        assert edge is not None
        channels = self.model.channels_for(edge)
        names = {channel.identifier for channel in channels}
        self.assertIn("gates_legality_and_cost", names)
        self.assertIn("carries_quantities", names)
        for channel in channels:
            with self.subTest(channel=channel.identifier):
                self.assertIs(channel.enforced, False)
                self.assertTrue(channel.reason)

    def test_a_tie_with_no_matching_tag_opens_only_the_structural_channels(self):
        plain = RelationshipEdge(
            identifier="plain",
            holder_id="leader_1",
            other_id="target_1",
            kind="rival_of",
            tags=("suspicious",),
            state_rationale="the author has declared no positions for this tie",
        )
        names = {channel.identifier for channel in self.model.channels_for(plain)}
        self.assertEqual(names, {"gates_legality_and_cost", "carries_quantities",
                                "decides_trade_off_or_split", "written_back_as_state"})
        untagged = RelationshipEdge(
            identifier="untagged",
            holder_id="leader_1",
            other_id="target_2",
            kind="rival_of",
            tags=("frenemy",),
            state_rationale="the author has declared no positions for this tie",
        )
        self.assertNotIn(
            "gates_legality_and_cost",
            {channel.identifier for channel in self.model.channels_for(untagged)},
        )

    def test_an_unmodelled_target_is_unmodelled_and_not_a_neutral_zero(self):
        council = _council()
        reports = " | ".join(self.model.consequence_reports(council, edges=RelationshipSet()))
        self.assertIn("UNMODELLED", reports)
        self.assertIn("sparse", reports)

    def test_a_modelled_target_reports_the_channel_it_opens(self):
        mission = _mission(1, "opinion_support", target_id="ulp")
        council = _council(missions=(mission,))
        self.assertEqual(self.model.structural_problems(council), ())
        reports = " | ".join(self.model.consequence_reports(council, edges=_leader_tie()))
        self.assertIn("gates_legality_and_cost", reports)
        self.assertIn("nothing is granted", reports)

    def test_the_strategic_consequences_reading_applies_nothing(self):
        mission = _mission(1, "opinion_support", target_id="ulp")
        reading = self.model.strategic_consequences(mission, _leader_tie())
        self.assertTrue(reading["target_modelled"])
        self.assertEqual(reading["edge_ids"], ["leader_1_indebted_to_ulp"])
        self.assertIn("gates_legality_and_cost", reading["channels"])
        self.assertIs(reading["enforced"], False)
        self.assertIn("no modifier, no threshold and no outcome", reading["note"])

    def test_the_founder_tie_is_not_the_mission_leaders_tie(self):
        """A tie between two other records is not read: the record is sparse and pairwise."""
        mission = _mission(1, "opinion_support", target_id="ulp")
        reading = self.model.strategic_consequences(mission, _patron_edges())
        self.assertFalse(reading["target_modelled"])
        self.assertEqual(reading["edge_ids"], [])

    def test_the_four_channels_are_the_proposals_four(self):
        self.assertEqual(
            {channel.identifier for channel in self.model.channels},
            {
                "gates_legality_and_cost",
                "carries_quantities",
                "decides_trade_off_or_split",
                "written_back_as_state",
            },
        )


class NoResolutionTests(unittest.TestCase):
    """Nothing in this package resolves, advances or writes anything."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_council()

    def test_running_every_validator_leaves_the_council_byte_identical(self):
        council = self.model.worked_example_council()
        before = copy.deepcopy(council.to_dict())
        self.model.structural_problems(council)
        self.model.consequence_reports(council)
        self.model.shared_interest_report(council)
        self.model.unpursued_quantities(council)
        self.assertEqual(before, council.to_dict())

    def test_no_mission_carries_an_outcome(self):
        for mission in self.model.worked_example_council().missions:
            with self.subTest(mission=mission.identifier):
                self.assertEqual(mission.outcome, "")

    def test_a_declared_outcome_is_reported_as_out_of_scope(self):
        council = _council(missions=(_mission(1, "opinion_support", outcome="succeeded"),))
        self.assertIn("succeeded", " | ".join(self.model.consequence_reports(council)))

    def test_the_resolution_gate_is_recorded_as_closed(self):
        resolution = self.model.mission.get("resolution") or {}
        self.assertIs(resolution.get("declared"), False)
        self.assertIn("no mission is resolved", str(resolution.get("reason")))

    def test_the_mission_costs_are_named_and_unpriced(self):
        identifiers = {cost.identifier for cost in self.model.costs}
        self.assertEqual(
            identifiers, {"leader_turn", "declared_resources", "leader_status_risk",
                          "patron_edge_stress"}
        )
        for cost in self.model.costs:
            with self.subTest(cost=cost.identifier):
                self.assertTrue(cost.note)
                self.assertFalse(
                    any(isinstance(value, (int, float)) for value in cost.to_dict().values())
                )

    def test_the_failure_shape_is_declared_false_and_quotes_the_six_quantities(self):
        failure = self.model.mission.get("failure_is_not_nothing") or {}
        self.assertIs(failure.get("declared"), False)
        self.assertTrue(failure.get("reason"))
        for example in failure.get("examples") or []:
            with self.subTest(example=example.get("mission")):
                self.assertIn(example.get("attempted"), QUANTITY_IDS)
                for name in example.get("moves_wrong_way") or []:
                    self.assertIn(name, QUANTITY_IDS)


class RivalParityTests(unittest.TestCase):
    """Issue #323: enemy AI uses the same rules. No special case exists in this module."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_council()

    def test_a_rival_and_a_player_council_are_validated_by_the_same_function(self):
        over_cap = tuple(
            _mission(index, "opinion_support", leader_id=f"leader_{index}")
            for index in range(1, 6)
        )
        player = _council(identifier="player", missions=over_cap)
        rival = _council(identifier="rival", missions=over_cap)
        results = self.model.validate_all((player, rival))
        self.assertEqual(set(results), {"player", "rival"})
        self.assertEqual(set(results["player"]), set(results["rival"]))
        self.assertEqual(results["player"], results["rival"])

    def test_a_rival_cannot_hold_a_fifth_office(self):
        leaders = (*_leaders(), CouncilLeader(identifier="leader_5", portfolio=PORTFOLIO_IDS[0]))
        rival = _council(identifier="rival", leaders=leaders, missions=())
        self.assertTrue(self.model.structural_problems(rival))

    def test_resources_never_add_a_mission(self):
        over_cap = tuple(
            _mission(index, "opinion_support", leader_id=f"leader_{index}",
                     allocated_resource_ids=(f"asset_{index}",))
            for index in range(1, 6)
        )
        problems = " | ".join(self.model.structural_problems(_council(missions=over_cap)))
        self.assertIn("never add one", problems)


class ShippedDocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_council()
        cls.payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    def test_every_pending_decision_carries_the_reason_it_is_open(self):
        self.assertTrue(self.model.pending_decisions())
        self.assertEqual(self.model.unreasoned_decisions(), ())
        for item in self.model.pending_decisions():
            with self.subTest(decision=item.get("id")):
                self.assertTrue(item.get("why_not_decided"))
                self.assertTrue(item.get("container_instead"))

    def test_no_numeric_mechanic_or_numeric_named_position_in_the_data(self):
        for path, key, value in _walk(self.payload):
            with self.subTest(path="/".join(path), key=key):
                self.assertNotIn(key, FORBIDDEN_KEYS)
                if key in NAMED_POSITION_KEYS:
                    self.assertFalse(isinstance(value, (int, float)) and not isinstance(value, bool))

    def test_the_document_declares_what_it_consumes_rather_than_restating_it(self):
        consumes = self.payload.get("consumes") or {}
        self.assertIn("quantities", consumes)
        self.assertIn("edges", consumes)
        self.assertIn("leader_card", consumes)

    def test_the_layer_reuses_the_shared_edge_record(self):
        self.assertIn("RelationshipEdge", str(self.payload.get("consumes", {}).get("edges")))

    def test_a_document_that_is_not_a_council_vocabulary_is_refused(self):
        import tempfile

        with tempfile.TemporaryDirectory() as folder:
            trap = Path(folder) / "not_a_council.json"
            trap.write_text(json.dumps({"format": "noopunk.something.else"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_council(trap)

    def test_the_unpursued_reading_leaves_something_out_whenever_four_moves_are_named(self):
        council = _council()
        self.assertEqual(len(self.model.unpursued_quantities(council)), 2)
        empty = _council(missions=())
        self.assertEqual(self.model.unpursued_quantities(empty), QUANTITY_IDS)


if __name__ == "__main__":
    unittest.main()
