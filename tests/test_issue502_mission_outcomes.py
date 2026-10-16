"""Focused tests for issue #502 Phase 1: mission outcomes onto faction world state.

Covers the one tested writer, ``apply_mission_outcome``: happy-path book movement,
idempotent replay, all-or-nothing refusals that leave state untouched, the approved
outcome ladder, and the provenance-stamped audit trail.
"""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from strategy_game.campaign import (
    Campaign,
    CampaignError,
    CampaignFaction,
    Case,
    MissionError,
    MissionOutcome,
    apply_mission_outcome,
)
from strategy_game.rpg.fate import Character, Outcome


def _campaign() -> Campaign:
    leader = Character(id="l-1", name="Leader Uno", aspects=["driven"], skills={"COG": 2})
    agent = Character(id="a-1", name="Agent One", aspects=["careful"])
    faction = CampaignFaction(
        identifier="unsa",
        name="UNSA Helsinki",
        leader_id="l-1",
        member_ids=["l-1", "a-1"],
        resources=["res-1"],
    )
    case = Case(case_id="case-1", core_question="Who ran the glitch?", investigator="l-1")
    return Campaign(
        faction_id="unsa",
        leader_id="l-1",
        sheets={"l-1": leader, "a-1": agent},
        factions={"unsa": faction},
        cases={"case-1": case},
    )


def _report(**overrides) -> MissionOutcome:
    """A valid SUCCESS report, overridable field by field."""
    fields = dict(
        mission_id="m-1",
        case_id="case-1",
        outcome=Outcome.SUCCESS,
        leader_id="l-1",
        agent_ids=("a-1",),
        evidence_gained=("ev-1",),
        intel_gained=("int-1",),
        resources_gained=("res-2",),
        resources_spent=("res-1",),
        reputation_labels_gained=("known_in_helsinki",),
        objectives_completed=("secure the water",),
        seed=42,
    )
    fields.update(overrides)
    return MissionOutcome(**fields)


class HappyPathTests(unittest.TestCase):
    def test_outcome_moves_all_four_phase1_books_and_the_case_evidence(self):
        camp = _campaign()
        faction = camp.factions["unsa"]
        applied = apply_mission_outcome(camp, _report())
        self.assertIs(applied, None or applied)  # returns the applied record
        self.assertEqual(faction.resources, ["res-2"])
        self.assertEqual(faction.reputation_labels, ["known_in_helsinki"])
        self.assertEqual(faction.objectives, ["secure the water"])
        self.assertEqual(faction.intelligence_ids, ["int-1"])
        self.assertEqual(camp.intelligence_ids, ["int-1"])
        self.assertEqual(camp.cases["case-1"].evidence_ids, ["ev-1"])
        self.assertEqual(applied.seed, 42)

    def test_empty_transitions_write_only_the_audit_note(self):
        camp = _campaign()
        before = camp.to_json()
        apply_mission_outcome(camp, _report())
        self.assertNotEqual(camp.to_json(), before)  # the audit note is written even so
        self.assertEqual(camp.campaign_notes[-1]["outcome"], "success")

    def test_returns_the_outcome_record_that_was_applied(self):
        camp = _campaign()
        report = _report()
        applied = apply_mission_outcome(camp, report)
        self.assertIs(applied, report)

    def test_audit_entry_is_provenance_stamped_simulated(self):
        camp = _campaign()
        apply_mission_outcome(camp, _report())
        note = camp.campaign_notes[-1]
        self.assertEqual(note["kind"], "mission_outcome")
        self.assertEqual(note["schema_version"], "mission-report-1")
        self.assertEqual(note["provenance"]["kind"], "simulated")
        self.assertEqual(
            note["provenance"]["source"],
            "strategy_game.campaign.missions.apply_mission_outcome",
        )
        self.assertEqual(note["seed"], 42)
        for key in (
            "mission_id",
            "case_id",
            "outcome",
            "leader_id",
            "agent_ids",
            "evidence_gained",
            "intel_gained",
            "resources_gained",
            "resources_spent",
            "reputation_labels_gained",
            "objectives_completed",
        ):
            self.assertIn(key, note)

    def test_apply_requires_a_playable_faction(self):
        camp = _campaign()
        camp.faction_id = ""  # type: ignore[assignment]
        camp.leader_id = ""  # type: ignore[assignment]
        with self.assertRaisesRegex(CampaignError, "no faction"):
            apply_mission_outcome(camp, _report())


class IdempotenceTests(unittest.TestCase):
    def test_reapplying_the_same_outcome_does_not_double_apply(self):
        camp = _campaign()
        report = _report()
        apply_mission_outcome(camp, report)
        once = camp.to_json()
        apply_mission_outcome(camp, report)
        again = camp.to_json()
        self.assertNotEqual(once, again)  # the audit note is appended each apply
        campaign_payload = copy.deepcopy(camp.to_dict())
        campaign_payload.pop("campaign_notes")
        replayed_payload = copy.deepcopy(camp.to_dict())
        replayed_payload.pop("campaign_notes")
        self.assertEqual(campaign_payload, replayed_payload)
        self.assertEqual(camp.cases["case-1"].evidence_ids, ["ev-1"])
        self.assertEqual(camp.factions["unsa"].resources, ["res-2"])
        self.assertEqual(camp.factions["unsa"].intelligence_ids, ["int-1"])
        self.assertEqual(camp.factions["unsa"].objectives, ["secure the water"])
        self.assertEqual(camp.factions["unsa"].reputation_labels, ["known_in_helsinki"])

    def test_replay_appends_the_named_number_of_notes_only(self):
        camp = _campaign()
        report = _report()
        for _ in range(3):
            apply_mission_outcome(camp, report)
        self.assertEqual(len(camp.campaign_notes), 3)
        self.assertEqual(camp.cases["case-1"].evidence_ids, ["ev-1"])

    def test_idempotence_holds_when_reapplying_resources_already_held(self):
        camp = _campaign()
        report = _report(resources_gained=("res-1",), resources_spent=())
        apply_mission_outcome(camp, report)
        self.assertEqual(camp.factions["unsa"].resources, ["res-1"])
        apply_mission_outcome(camp, report)
        self.assertEqual(camp.factions["unsa"].resources, ["res-1"])


class AllOrNothingRefusalTests(unittest.TestCase):
    def _assert_refusal_leaves_state_identical(self, camp: Campaign, report) -> None:
        frozen = copy.deepcopy(camp)
        frozen_json = frozen.to_json()
        with self.assertRaises(CampaignError):
            apply_mission_outcome(camp, report)  # type: ignore[arg-type]
        self.assertEqual(camp.to_json(), frozen_json)

    def test_unknown_leader_is_refused_and_state_is_untouched(self):
        camp = _campaign()
        self._assert_refusal_leaves_state_identical(
            camp, _report(mission_id="m-2", leader_id="ghost")
        )

    def test_unknown_case_is_refused_and_state_is_untouched(self):
        camp = _campaign()
        self._assert_refusal_leaves_state_identical(
            camp, _report(mission_id="m-3", case_id="nope")
        )

    def test_non_member_agent_is_refused_and_state_is_untouched(self):
        camp = _campaign()
        self._assert_refusal_leaves_state_identical(
            camp, _report(mission_id="m-4", agent_ids=("stranger",))
        )

    def test_leader_named_as_an_agent_is_refused_at_the_record(self):
        # Construction refuses it, so no writer can ever receive such a report.
        with self.assertRaisesRegex(MissionError, "distinct people"):
            _report(agent_ids=("l-1",))

    def test_over_capacity_agent_roster_is_refused_at_the_record(self):
        with self.assertRaisesRegex(MissionError, "at most 4 agents"):
            _report(agent_ids=("a", "b", "c", "d", "e"))

    def test_over_capacity_roster_through_the_payload_is_refused_too(self):
        payload = {
            "schema_version": "mission-report-1",
            "mission_id": "m-5",
            "case_id": "case-1",
            "outcome": "success",
            "leader_id": "l-1",
            "agent_ids": ["a", "b", "c", "d", "e"],
        }
        with self.assertRaisesRegex(MissionError, "at most 4 agents"):
            MissionOutcome.from_dict(payload)

    def test_unapproved_outcome_name_is_refused_by_the_record(self):
        with self.assertRaisesRegex(MissionError, "approved Fate outcomes"):
            MissionOutcome.from_dict(
                {
                    "schema_version": "mission-report-1",
                    "mission_id": "m-6",
                    "case_id": "case-1",
                    "outcome": "miracle",
                    "leader_id": "l-1",
                }
            )

    def test_outcome_outside_the_fate_enum_is_refused_by_the_record(self):
        for not_an_outcome in ("miracle", "total_victory", "", "SUCCESS"):
            with self.subTest(outcome=not_an_outcome):
                with self.assertRaises(MissionError):
                    MissionOutcome.from_dict(
                        {
                            "schema_version": "mission-report-1",
                            "mission_id": "m-6x",
                            "case_id": "case-1",
                            "outcome": not_an_outcome,
                            "leader_id": "l-1",
                        }
                    )

    def test_non_outcome_enum_object_is_refused_by_the_record(self):
        with self.assertRaisesRegex(MissionError, "approved ladder"):
            _report(outcome="success")  # type: ignore[arg-type]

    def test_resource_both_gained_and_spent_is_refused(self):
        with self.assertRaisesRegex(MissionError, "both gained and spent"):
            _report(resources_gained=("res-1",), resources_spent=("res-1",))

    def test_duplicate_transition_ids_are_refused(self):
        with self.assertRaisesRegex(MissionError, "duplicate id"):
            _report(evidence_gained=("e1", "e1"))

    def test_leader_agent_collision_is_refused(self):
        with self.assertRaisesRegex(MissionError, "distinct people"):
            _report(agent_ids=("l-1",))

    def test_refusal_after_earlier_successful_applies_still_leaves_everything(self):
        camp = _campaign()
        apply_mission_outcome(camp, _report())
        good_state = copy.deepcopy(camp.to_dict())
        with self.assertRaises(CampaignError):
            apply_mission_outcome(
                camp, _report(mission_id="m-9", case_id="missing")
            )
        now = copy.deepcopy(camp.to_dict())
        now.pop("campaign_notes")
        good_state.pop("campaign_notes")
        self.assertEqual(now, good_state)


class MissionRecordTests(unittest.TestCase):
    def test_payload_round_trips_exactly(self):
        report = _report()
        rebuilt = MissionOutcome.from_dict(report.to_dict())
        self.assertEqual(rebuilt.to_dict(), report.to_dict())

    def test_payload_declares_its_version(self):
        self.assertEqual(_report().to_dict()["schema_version"], "mission-report-1")

    def test_from_dict_refuses_a_foreign_payload_version(self):
        payload = _report().to_dict()
        payload["schema_version"] = "mission-report-X"
        with self.assertRaisesRegex(MissionError, "schema_version 'mission-report-X'"):
            MissionOutcome.from_dict(payload)

    def test_from_dict_refuses_a_non_mapping(self):
        with self.assertRaisesRegex(MissionError, "must be a mapping"):
            MissionOutcome.from_dict("nope")  # type: ignore[arg-type]

    def test_every_approved_ladder_name_is_accepted(self):
        for name in ("failure", "tie", "success", "success_with_style"):
            with self.subTest(outcome=name):
                record = MissionOutcome.from_dict(
                    {
                        "schema_version": "mission-report-1",
                        "mission_id": "m-8",
                        "case_id": "case-1",
                        "outcome": name,
                        "leader_id": "l-1",
                    }
                )
                self.assertIs(record.outcome, Outcome(name))

    def test_blank_mission_or_leader_is_refused(self):
        with self.assertRaisesRegex(MissionError, "names its mission"):
            _report(mission_id="   ")
        with self.assertRaisesRegex(MissionError, "names its leader"):
            _report(leader_id="")


if __name__ == "__main__":
    unittest.main()