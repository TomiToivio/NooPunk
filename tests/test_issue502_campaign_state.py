"""Focused tests for issue #502 Phase 1: the shared campaign world state.

Covers the state module's declared behaviour: the one-of-each collections, the PC
premise (leader + faction bound together, sheets held by identity), the Phase-1
books, structural validation, and the versioned save/load round trip.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from strategy_game import core
from strategy_game.campaign import (
    AGENT_CAPACITY,
    Campaign,
    CampaignError,
    CampaignFaction,
    Case,
    SCHEMA_VERSION,
    load_campaign,
    save_campaign,
)
from strategy_game.campaign.state import campaign_from_dict
from strategy_game.rpg.fate import Character
from strategy_game.rpg.roster import AGENT_SEAT_COUNT


def _leader_sheet() -> Character:
    return Character(id="l-1", name="Leader Uno", aspects=["driven"], skills={"COG": 2})


def _agent_sheet(name: str = "Agent One", cid: str = "a-1") -> Character:
    return Character(id=cid, name=name, aspects=["careful"])


def _campaign() -> Campaign:
    """The minimal playable campaign: leader + one agent + one case."""
    return Campaign(
        faction_id="unsa",
        leader_id="l-1",
        sheets={"l-1": _leader_sheet(), "a-1": _agent_sheet()},
        factions={
            "unsa": CampaignFaction(
                identifier="unsa",
                name="UNSA Helsinki",
                leader_id="l-1",
                member_ids=["l-1", "a-1"],
                resources=["res-1"],
            )
        },
        cases={
            "case-1": Case(
                case_id="case-1",
                core_question="Who ran the glitch?",
                investigator="l-1",
            )
        },
    )


class CampaignIdentityTests(unittest.TestCase):
    def test_capacity_is_the_approved_roster_seat_count_itself(self):
        self.assertIs(AGENT_CAPACITY, AGENT_SEAT_COUNT)

    def test_faction_is_isinstance_of_the_scaffold_faction(self):
        faction = CampaignFaction(identifier="f", name="F", leader_id="l-1")
        self.assertIsInstance(faction, core.Faction)

    def test_faction_to_dict_carries_the_phase1_books(self):
        faction = CampaignFaction(
            identifier="f",
            name="F",
            leader_id="l-1",
            member_ids=["l-1", "a-1"],
            objectives=["o1"],
            intelligence_ids=["int-1"],
            reputation_labels=["known_in_helsinki"],
            resources=["res-1"],
        )
        payload = faction.to_dict()
        for key in (
            "id",
            "name",
            "leader_id",
            "asset_ids",
            "member_ids",
            "objectives",
            "intelligence_ids",
            "reputation_labels",
            "resources",
            "provenance",
        ):
            self.assertIn(key, payload)
        self.assertEqual(payload["member_ids"], ["l-1", "a-1"])
        self.assertEqual(payload["reputation_labels"], ["known_in_helsinki"])

    def test_leader_and_agent_are_distinct_types(self):
        from strategy_game.campaign import Agent, Leader

        leader = Leader(identifier="l-1", name="L", faction_id="f")
        agent = Agent(identifier="a-1", name="A", faction_id="f")
        self.assertIsNot(type(leader), type(agent))
        self.assertEqual(leader.to_dict(), {"id": "l-1", "name": "L", "faction_id": "f"})
        self.assertEqual(agent.to_dict(), {"id": "a-1", "name": "A", "faction_id": "f"})


class CampaignPremiseTests(unittest.TestCase):
    def test_faction_without_leader_is_refused(self):
        faction = CampaignFaction(identifier="u", name="U", leader_id="l-1")
        with self.assertRaisesRegex(CampaignError, "PC premise binds the leader"):
            Campaign(
                faction_id="u", factions={"u": faction}, sheets={"l-1": _leader_sheet()}
            )

    def test_leader_without_faction_is_refused(self):
        with self.assertRaisesRegex(CampaignError, "PC premise binds the leader"):
            Campaign(
                leader_id="l-1",
                sheets={"l-1": _leader_sheet()},
                factions={"u": CampaignFaction(identifier="u", name="U", leader_id="l-1")},
            )

    def test_leader_without_sheet_is_refused(self):
        with self.assertRaisesRegex(CampaignError, "has no sheet"):
            Campaign(
                faction_id="u",
                leader_id="l-1",
                factions={"u": CampaignFaction(identifier="u", name="U", leader_id="l-1")},
                sheets={},
            )

    def test_unknown_leader_id_is_refused_even_with_a_sheet_for_someone_else(self):
        with self.assertRaisesRegex(CampaignError, "has no sheet"):
            Campaign(
                faction_id="u",
                leader_id="l-9",
                factions={"u": CampaignFaction(identifier="u", name="U", leader_id="l-1")},
                sheets={"l-1": _leader_sheet()},
            )

    def test_unknown_faction_id_is_refused(self):
        with self.assertRaisesRegex(CampaignError, "unknown faction id is a defect"):
            Campaign(faction_id="ghost", leader_id="l-1", sheets={"l-1": _leader_sheet()})

    def test_empty_campaign_is_allowed_but_has_no_faction(self):
        empty = Campaign()
        self.assertEqual(empty.faction_id, "")
        self.assertEqual(empty.leader_id, "")
        with self.assertRaises(CampaignError):
            empty.faction()


class StructuralProblemsTests(unittest.TestCase):
    def test_clean_campaign_reports_no_problems(self):
        self.assertEqual(_campaign().structural_problems(), ())

    def test_member_without_sheet_is_reported(self):
        camp = Campaign(
            factions={
                "u2": CampaignFaction(
                    identifier="u2", name="B", leader_id="l-1", member_ids=["x1"]
                )
            },
            sheets={"l-1": _leader_sheet()},
        )
        problems = camp.structural_problems()
        self.assertTrue(any("member 'x1' has no sheet" in p for p in problems), problems)

    def test_case_participant_without_sheet_is_reported(self):
        camp = Campaign(
            cases={"c2": Case(case_id="c2", core_question="q", investigator="ghost")}
        )
        problems = camp.structural_problems()
        self.assertTrue(
            any("case 'c2': participant 'ghost' has no sheet" in p for p in problems),
            problems,
        )

    def test_tie_to_unknown_endpoint_is_reported(self):
        from strategy_game.relationships import RelationshipEdge

        camp = Campaign(
            ties={
                "t1": RelationshipEdge(
                    identifier="t1", holder_id="ghost", other_id="nobody"
                )
            }
        )
        problems = camp.structural_problems()
        self.assertTrue(
            any("tie t1" in p and "not a known record" in p for p in problems), problems
        )

    def test_campaign_leader_mismatch_is_reported(self):
        camp = _campaign()
        camp.leader_id = "a-1"  # type: ignore[assignment]
        problems = camp.structural_problems()
        self.assertTrue(any("is not the faction's own" in p for p in problems), problems)


class FactionMembershipRulesTests(unittest.TestCase):
    def test_over_capacity_faction_is_refused(self):
        with self.assertRaisesRegex(CampaignError, "more than 4 agent members"):
            CampaignFaction(
                identifier="x",
                name="X",
                leader_id="l",
                member_ids=["l", "a", "b", "c", "d", "e"],
            )

    def test_duplicate_member_or_resource_refs_are_refused(self):
        with self.assertRaisesRegex(CampaignError, "duplicate member id"):
            CampaignFaction(
                identifier="x", name="X", leader_id="l", member_ids=["l", "a", "a"]
            )
        with self.assertRaisesRegex(CampaignError, "duplicate resource id"):
            CampaignFaction(identifier="x", name="X", leader_id="l", resources=["r", "r"])

    def test_agent_views_return_leader_excluded_records_in_member_order(self):
        camp = _campaign()
        views = camp.agent_views()
        self.assertEqual(tuple(view.identifier for view in views), ("a-1",))
        self.assertEqual(views[0].name, "Agent One")

    def test_agent_views_refuse_member_without_sheet(self):
        camp = _campaign()
        camp.factions["unsa"].member_ids.append("ghost")
        with self.assertRaisesRegex(CampaignError, "have no sheet"):
            camp.agent_views()

    def test_roster_report_shows_declared_blanks(self):
        camp = _campaign()
        report = camp.roster_report()
        self.assertEqual(report["leader_id"], "l-1")
        self.assertEqual(report["member_ids"], ["a-1"])
        self.assertEqual(report["agent_capacity"], AGENT_CAPACITY)
        self.assertEqual(report["unfilled_seats"], AGENT_CAPACITY - 1)


class SaveLoadRoundTripTests(unittest.TestCase):
    def test_round_trip_is_exactly_equal(self):
        camp = _campaign()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "camp.json"
            save_campaign(camp, path)
            loaded = load_campaign(path)
            self.assertEqual(loaded.to_json(), camp.to_json())

    def test_round_trip_survives_the_audit_trail(self):
        from strategy_game.campaign import MissionOutcome
        from strategy_game.campaign.missions import apply_mission_outcome
        from strategy_game.rpg.fate import Outcome

        camp = _campaign()
        report = MissionOutcome(
            mission_id="m-1",
            case_id="case-1",
            outcome=Outcome.SUCCESS,
            leader_id="l-1",
            seed=42,
        )
        applied = apply_mission_outcome(camp, report)
        self.assertIsNotNone(applied)  # returns the applied record
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "camp.json"
            save_campaign(camp, path)
            loaded = load_campaign(path)
            self.assertEqual(loaded.to_json(), camp.to_json())
            note = loaded.campaign_notes[0]
            self.assertEqual(note["kind"], "mission_outcome")
            self.assertEqual(note["provenance"]["kind"], "simulated")
            self.assertEqual(note["seed"], 42)

    def test_save_payload_declares_the_current_schema_version(self):
        payload = _campaign().to_dict()
        self.assertEqual(payload["schema_version"], SCHEMA_VERSION)
        self.assertEqual(SCHEMA_VERSION, "campaign-save-1")

    def test_foreign_schema_version_is_refused_on_load(self):
        camp = _campaign()
        payload = camp.to_dict()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "foreign.json"
            path.write_text(
                json.dumps({**payload, "schema_version": "campaign-save-X"}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(CampaignError, "schema_version 'campaign-save-X'"):
                load_campaign(path)

    def test_missing_schema_version_is_refused(self):
        with self.assertRaisesRegex(CampaignError, "unsupported campaign save"):
            campaign_from_dict({"faction_id": "u"})

    def test_non_mapping_save_is_refused(self):
        with self.assertRaisesRegex(CampaignError, "must be a mapping"):
            campaign_from_dict(["not", "a", "mapping"])  # type: ignore[arg-type]

    def test_sheet_payload_round_trips_through_the_save(self):
        camp = _campaign()
        payload = camp.to_dict()
        sheet_payload = payload["sheets"]["l-1"]
        for key in ("id", "name", "aspects", "skills", "strategic_skills", "fate_points"):
            self.assertIn(key, sheet_payload)
        # loading refuses nothing about the sheet; equality is the round-trip proof
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "camp.json"
            save_campaign(camp, path)
            loaded = load_campaign(path)
            self.assertEqual(loaded.sheets["l-1"].skills, {"COG": 2})
            self.assertEqual(loaded.sheets["l-1"].name, "Leader Uno")


if __name__ == "__main__":
    unittest.main()