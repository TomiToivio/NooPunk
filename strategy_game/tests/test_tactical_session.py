"""Executable contracts for the headless mission session (issue #515's spike).

Code-only, per ``AGENTS.md``. These tests exercise the behaviour #515's first milestone promises —
four selectable agents acting one at a time, click-to-move resolved by pathfinding, a dialogue and a
clue, objectives, and an outcome written into persistent state — and they assert the *reuse* the
mission layer claims: the turn ledger is :class:`strategy_game.rpg.roster.TurnLedger`, the checks are
the approved Fate kernel, a failed confrontation applies the scene layer's own hit procedure, and the
mission outcome is written by ``campaign.missions.apply_mission_outcome`` alone.

Determinism is by injection: :class:`FixedDice` supplies scripted Fate faces, so an outcome is chosen
by the test rather than discovered by it.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap
    sys.path.insert(0, str(ROOT))

from strategy_game.campaign import Campaign, load_campaign, save_campaign
from strategy_game.rpg.fate import Outcome
from strategy_game.rpg.roster import AGENT_SEAT_COUNT, SeatKind, TurnLedger
from strategy_game.tactical.demo import DEMO_SEED, FIXTURE_CASE, fixture_campaign
from strategy_game.tactical.grid import Cell
from strategy_game.tactical.mission import (
    MISSION_FORMAT,
    MISSION_SCHEMA_VERSION,
    MissionError,
    load_mission,
    mission_from_dict,
)
from strategy_game.tactical.session import MissionSession

#: A small mission used where the fixture's 20x20 map is irrelevant: a sealed pocket at (3,3), and a
#: single check-free dialogue so the session can resolve something.
TINY_ROWS = (
    "#######",
    "#.....#",
    "#.###.#",
    "#.#.#.#",
    "#.###.#",
    "#.....#",
    "#######",
)


class FixedDice:
    """An injectable rng: hands out scripted Fate faces, one per ``choice`` call."""

    def __init__(self, faces: tuple[int, ...]) -> None:
        self.faces = faces
        self.calls = 0

    def choice(self, options):
        face = self.faces[self.calls % len(self.faces)]
        self.calls += 1
        assert face in options, f"scripted face {face} is not one of {options}"
        return face


def tiny_document() -> dict:
    return {
        "format": MISSION_FORMAT,
        "schema_version": MISSION_SCHEMA_VERSION,
        "status": "TEST_FIXTURE",
        "mission_id": "tiny_test_mission",
        "case_id": FIXTURE_CASE,
        "title": "Tiny test mission",
        "grid": {
            "width": 7,
            "height": 7,
            "legend": {".": "floor", "#": "wall", "+": "door"},
            "rows": list(TINY_ROWS),
        },
        "deploy_cells": [[1, 1], [1, 2], [5, 1], [5, 2]],
        "interactions": [
            {
                "id": "talk",
                "kind": "dialogue",
                "at": [2, 1],
                "objectives": ["talked"],
            }
        ],
        "objectives": [{"id": "talked", "label": "test:talked", "required": True}],
    }


def new_session(*, rng=None, campaign: Campaign | None = None, spec=None, seed: int = DEMO_SEED):
    return MissionSession(
        spec if spec is not None else load_mission(),
        campaign if campaign is not None else fixture_campaign(),
        seed=seed,
        rng=rng,
    )


def walk_into_place(session: MissionSession) -> None:
    """Put agent_1 beside the witness and agent_2 beside the annex ledger, then end the turn."""
    session.select("agent_1")
    assert session.request_move("agent_1", (9, 9)).ok
    session.select("agent_2")
    assert session.request_move("agent_2", (6, 12)).ok
    session.end_turn()


def play_fixture(*, rng=None, seed: int = DEMO_SEED, campaign: Campaign | None = None):
    """The fixture mission's shortest successful path, with the campaign returned for assertions."""
    session = new_session(rng=rng, seed=seed, campaign=campaign)
    walk_into_place(session)
    session.select("agent_1")
    assert session.interact("agent_1", "interview_witness").ok
    session.select("agent_2")
    assert session.interact("agent_2", "read_ledger").ok
    return session, session.campaign


class RosterTests(unittest.TestCase):
    def test_the_mission_offers_the_four_agent_seats_and_reuses_the_ledger(self):
        session = new_session()
        self.assertEqual(session.seat_ids, ("agent_1", "agent_2", "agent_3", "agent_4"))
        self.assertEqual(len(session.seat_ids), AGENT_SEAT_COUNT)
        self.assertIsInstance(session.ledger, TurnLedger)
        self.assertEqual(session.ledger.seats, session.seats)
        for seat in session.seats:
            self.assertIs(seat.kind, SeatKind.AGENT)
        self.assertEqual(
            [session.sheet(seat_id).id for seat_id in session.seat_ids],
            ["spike-agent-1", "spike-agent-2", "spike-agent-3", "spike-agent-4"],
        )

    def test_each_of_the_four_agents_can_be_selected(self):
        session = new_session()
        for seat_id in session.seat_ids:
            self.assertEqual(session.select(seat_id).id, seat_id)
            self.assertEqual(session.selected, seat_id)

    def test_selecting_is_not_an_action(self):
        session = new_session()
        session.select("agent_3")
        self.assertFalse(session.has_acted("agent_3"))
        self.assertEqual(session.ledger.acted, {})

    def test_an_unknown_seat_is_a_programming_error(self):
        session = new_session()
        with self.assertRaises(MissionError) as raised:
            session.select("agent_9")
        self.assertIn("agent_1", str(raised.exception))

    def test_only_the_selected_agent_may_act(self):
        session = new_session()
        session.select("agent_1")
        result = session.request_move("agent_2", (17, 4))
        self.assertFalse(result.ok)
        self.assertIn("not the selected agent", result.reason)
        self.assertEqual(session.position("agent_2"), Cell(17, 6))
        self.assertFalse(session.has_acted("agent_2"))

    def test_each_character_acts_once_per_turn_and_the_ledger_says_so(self):
        session = new_session()
        session.select("agent_1")
        self.assertTrue(session.request_move("agent_1", (9, 9)).ok)
        again = session.request_move("agent_1", (9, 8))
        self.assertFalse(again.ok)
        # The refusal is the ledger's own, not a second wording for the same rule.
        self.assertIn("already acted this turn", again.reason)
        self.assertIn("next turn", again.reason)
        self.assertEqual(session.position("agent_1"), Cell(9, 9))

        session.select("agent_2")
        self.assertTrue(session.request_move("agent_2", (6, 12)).ok)

        self.assertEqual(session.end_turn(), 1)
        self.assertFalse(session.has_acted("agent_1"))
        session.select("agent_1")
        self.assertTrue(session.request_move("agent_1", (9, 8)).ok)


class MovementTests(unittest.TestCase):
    def test_click_to_move_returns_the_steps_through_the_annex_door(self):
        session = new_session()
        session.select("agent_2")
        result = session.request_move("agent_2", (6, 12))
        self.assertTrue(result.ok, result.reason)
        self.assertEqual(result.destination, Cell(6, 12))
        self.assertEqual(result.steps[-1], Cell(6, 12))
        self.assertIn(Cell(6, 10), result.steps, "the route should pass through the annex door")
        self.assertGreater(len(result.steps), 10, "a 17-step walk should report its steps")
        self.assertEqual(session.position("agent_2"), Cell(6, 12))
        self.assertTrue(session.has_acted("agent_2"))

    def test_moving_onto_another_agent_is_refused(self):
        session = new_session()
        session.select("agent_2")
        result = session.request_move("agent_2", (17, 3))
        self.assertFalse(result.ok)
        self.assertIn("occupied by agent_1", result.reason)
        self.assertFalse(session.has_acted("agent_2"))

    def test_moving_to_the_cell_you_stand_on_is_refused(self):
        session = new_session()
        session.select("agent_1")
        result = session.request_move("agent_1", (17, 3))
        self.assertFalse(result.ok)
        self.assertIn("already stands at (17,3)", result.reason)

    def test_a_target_off_the_grid_is_refused(self):
        session = new_session()
        session.select("agent_1")
        result = session.request_move("agent_1", (99, 99))
        self.assertFalse(result.ok)
        self.assertIn("outside the 20x20 grid", result.reason)

    def test_a_wall_as_the_destination_is_refused(self):
        session = new_session()
        session.select("agent_1")
        result = session.request_move("agent_1", (0, 0))
        self.assertFalse(result.ok)
        self.assertIn("a wall blocks (0,0)", result.reason)

    def test_an_unreachable_cell_is_refused_with_a_legible_reason(self):
        session = new_session(spec=mission_from_dict(tiny_document()))
        session.select("agent_1")
        result = session.request_move("agent_1", (3, 3))
        self.assertFalse(result.ok)
        self.assertIn("no route", result.reason)
        self.assertIn("(3,3)", result.reason)
        self.assertFalse(session.has_acted("agent_1"))

    def test_a_refused_move_spends_no_action_and_moves_nobody(self):
        session = new_session()
        session.select("agent_1")
        before = session.position("agent_1")
        session.request_move("agent_1", (0, 0))
        self.assertEqual(session.position("agent_1"), before)
        self.assertEqual(session.ledger.acted, {})


class InteractionTests(unittest.TestCase):
    def test_an_interaction_needs_an_adjacent_cell(self):
        session = new_session()
        session.select("agent_1")
        result = session.interact("agent_1", "interview_witness")
        self.assertFalse(result.ok)
        self.assertIn("cells away", result.reason)
        self.assertIn("adjacent", result.reason)
        self.assertFalse(session.has_acted("agent_1"))

    def test_a_dialogue_resolves_without_a_check_and_completes_its_objective(self):
        session = new_session()
        walk_into_place(session)
        session.select("agent_1")
        result = session.interact("agent_1", "interview_witness")
        self.assertTrue(result.ok, result.reason)
        self.assertIsNone(result.outcome)
        self.assertEqual(result.objectives, ("interview_witness",))
        done = {status.id: status.done for status in session.objectives()}
        self.assertTrue(done["interview_witness"])
        self.assertFalse(done["read_ledger"])
        self.assertEqual(session.report()["interactions"][0]["resolved"], True)

    def test_the_clue_requires_the_interview_first(self):
        session = new_session()
        session.select("agent_2")
        session.request_move("agent_2", (6, 12))
        session.end_turn()
        result = session.interact("agent_2", "read_ledger")
        self.assertFalse(result.ok)
        self.assertIn("requires ['interview_witness']", result.reason)
        self.assertFalse(session.has_acted("agent_2"))

    def test_a_resolved_interaction_cannot_be_replayed(self):
        session = new_session()
        walk_into_place(session)
        session.select("agent_1")
        self.assertTrue(session.interact("agent_1", "interview_witness").ok)
        session.end_turn()
        session.select("agent_1")
        again = session.interact("agent_1", "interview_witness")
        self.assertFalse(again.ok)
        self.assertIn("already resolved", again.reason)

    def test_a_successful_clue_grants_evidence_intel_and_the_objective(self):
        session = new_session(rng=FixedDice((1, 1, 0, 0)))
        walk_into_place(session)
        session.select("agent_1")
        session.interact("agent_1", "interview_witness")
        session.select("agent_2")
        result = session.interact("agent_2", "read_ledger")
        self.assertTrue(result.ok, result.reason)
        self.assertEqual(result.outcome, Outcome.SUCCESS_WITH_STYLE)
        self.assertEqual(result.evidence, ("spike:ledger_page",))
        self.assertEqual(result.intel, ("spike:ledger_names",))
        self.assertTrue(session.mission_complete)

    def test_a_failed_check_grants_nothing_and_spends_the_action(self):
        session = new_session(rng=FixedDice((-1, -1, -1, 0)))
        walk_into_place(session)
        session.select("agent_1")
        session.interact("agent_1", "interview_witness")
        session.select("agent_2")
        result = session.interact("agent_2", "read_ledger")
        self.assertFalse(result.ok)
        self.assertEqual(result.outcome, Outcome.FAILURE)
        self.assertEqual(result.evidence, ())
        self.assertEqual(session.report()["evidence"], [])
        self.assertTrue(session.has_acted("agent_2"))
        done = {status.id: status.done for status in session.objectives()}
        self.assertFalse(done["read_ledger"])
        self.assertIn("failed by 2 shift(s)", result.reason)

    def test_a_tie_grants_nothing_and_wounds_nobody(self):
        # Faces summing to -1: COG 3 against difficulty 2 lands on exactly 0 shifts.
        session = new_session(rng=FixedDice((-1, -1, 0, 1)))
        walk_into_place(session)
        session.select("agent_1")
        session.interact("agent_1", "interview_witness")
        session.select("agent_2")
        result = session.interact("agent_2", "read_ledger")
        self.assertFalse(result.ok)
        self.assertEqual(result.outcome, Outcome.TIE)
        self.assertEqual(result.shifts, 0)
        self.assertEqual(result.wound, "")
        self.assertEqual(session.report()["wounds"], [])
        self.assertIn("tied", result.reason)

    def test_a_failed_confrontation_writes_a_mild_consequence_onto_the_sheet(self):
        # Four -1 faces: SOM 3 against difficulty 2 fails by 3, so the mild consequence absorbs two
        # shifts and the remaining one fills the first stress box.
        session = new_session(rng=FixedDice((-1, -1, -1, -1)))
        walk_into_place(session)
        session.select("agent_1")
        self.assertTrue(session.interact("agent_1", "interview_witness").ok)
        session.end_turn()
        session.select("agent_1")
        self.assertTrue(session.request_move("agent_1", (6, 5)).ok)
        session.end_turn()
        session.select("agent_1")
        result = session.interact("agent_1", "confront_contact")
        self.assertFalse(result.ok)
        self.assertEqual(result.wound, "Bruised")
        sheet = session.campaign.sheets["spike-agent-1"]
        self.assertEqual([(c.name, c.severity) for c in sheet.consequences], [("Bruised", 2)])
        self.assertTrue(sheet.physical_stress[0], "the residual hit should fill the first stress box")
        wounds = session.report()["wounds"]
        self.assertEqual(len(wounds), 1)
        self.assertEqual(wounds[0]["consequence"], "Bruised")
        self.assertFalse(wounds[0]["taken_out"])

    def test_the_optional_confrontation_does_not_gate_the_mission(self):
        # First check fails (the confrontation), second succeeds (the clue).
        session = new_session(
            rng=FixedDice((-1, -1, -1, -1, 1, 1, 0, 0))
        )
        walk_into_place(session)
        session.select("agent_1")
        self.assertTrue(session.interact("agent_1", "interview_witness").ok)
        session.end_turn()
        session.select("agent_1")
        self.assertTrue(session.request_move("agent_1", (6, 5)).ok)
        session.end_turn()
        session.select("agent_1")
        self.assertFalse(session.interact("agent_1", "confront_contact").ok)
        session.select("agent_2")
        self.assertTrue(session.interact("agent_2", "read_ledger").ok)
        self.assertTrue(session.mission_complete)
        report = session.complete()
        self.assertEqual(report.objectives_completed, ("spike:witness_interviewed", "spike:ledger_read"))
        self.assertEqual(report.evidence_gained, ("spike:ledger_page",))


class ObjectiveAndOutcomeTests(unittest.TestCase):
    def test_objectives_report_their_labels_and_state(self):
        session = new_session()
        statuses = {status.id: status for status in session.objectives()}
        self.assertEqual(statuses["read_ledger"].label, "spike:ledger_read")
        self.assertTrue(statuses["read_ledger"].required)
        self.assertFalse(any(status.done for status in statuses.values()))

    def test_completion_refuses_while_a_required_objective_is_open(self):
        session = new_session()
        walk_into_place(session)
        session.select("agent_1")
        session.interact("agent_1", "interview_witness")
        with self.assertRaises(MissionError) as raised:
            session.complete()
        self.assertIn("read_ledger", str(raised.exception))

    def test_the_mission_outcome_is_the_decisive_checks_outcome_not_an_aggregate(self):
        session, _ = play_fixture(seed=DEMO_SEED)
        report = session.complete()
        ledger_check = session.report()  # the report is readable after completion too
        self.assertTrue(ledger_check["applied"])
        self.assertEqual(report.outcome, Outcome.SUCCESS_WITH_STYLE)
        self.assertEqual(report.seed, DEMO_SEED)

    def test_a_mission_with_no_decisive_check_cannot_complete(self):
        session = new_session(spec=mission_from_dict(tiny_document()))
        # agent_1 deploys at (1,1), already adjacent to the dialogue at (2,1).
        session.select("agent_1")
        self.assertTrue(session.interact("agent_1", "talk").ok)
        self.assertTrue(session.mission_complete)
        with self.assertRaises(MissionError) as raised:
            session.complete()
        self.assertIn("no resolved check", str(raised.exception))

    def test_completing_the_mission_writes_the_campaign_books(self):
        session, campaign = play_fixture()
        report = session.complete()
        faction = campaign.faction()
        self.assertEqual(
            faction.objectives, ["spike:witness_interviewed", "spike:ledger_read"]
        )
        self.assertEqual(faction.intelligence_ids, ["spike:witness_account", "spike:ledger_names"])
        self.assertEqual(campaign.intelligence_ids, ["spike:witness_account", "spike:ledger_names"])
        self.assertEqual(campaign.cases[FIXTURE_CASE].evidence_ids, ["spike:ledger_page"])
        self.assertEqual(len(campaign.campaign_notes), 1)
        note = campaign.campaign_notes[0]
        self.assertEqual(note["kind"], "mission_outcome")
        self.assertEqual(note["mission_id"], "spike_municipal_records")
        self.assertEqual(note["leader_id"], "spike-leader")
        self.assertEqual(note["agent_ids"], [
            "spike-agent-1", "spike-agent-2", "spike-agent-3", "spike-agent-4",
        ])
        self.assertEqual(note["outcome"], report.outcome.value)

    def test_completing_twice_applies_one_record_only(self):
        session, campaign = play_fixture()
        first = session.complete()
        second = session.complete()
        self.assertIs(first, second)
        self.assertEqual(len(campaign.campaign_notes), 1)
        self.assertEqual(campaign.faction().objectives.count("spike:ledger_read"), 1)

    def test_the_saved_campaign_carries_the_mission_result(self):
        session, campaign = play_fixture()
        session.complete()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "campaign.json"
            save_campaign(campaign, path)
            loaded = load_campaign(path)
        faction = loaded.faction()
        self.assertEqual(faction.objectives, ["spike:witness_interviewed", "spike:ledger_read"])
        self.assertEqual(faction.intelligence_ids, ["spike:witness_account", "spike:ledger_names"])
        self.assertEqual(loaded.cases[FIXTURE_CASE].evidence_ids, ["spike:ledger_page"])
        self.assertEqual(len(loaded.campaign_notes), 1)
        self.assertEqual(loaded.campaign_notes[0]["mission_id"], "spike_municipal_records")

    def test_a_wound_taken_in_the_mission_survives_the_save(self):
        session = new_session(rng=FixedDice((-1, -1, -1, 0)))
        walk_into_place(session)
        session.select("agent_1")
        session.interact("agent_1", "interview_witness")
        session.end_turn()
        session.select("agent_1")
        session.request_move("agent_1", (6, 5))
        session.end_turn()
        session.select("agent_1")
        session.interact("agent_1", "confront_contact")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "campaign.json"
            save_campaign(session.campaign, path)
            loaded = load_campaign(path)
        self.assertEqual(
            [(c.name, c.severity) for c in loaded.sheets["spike-agent-1"].consequences],
            [("Bruised", 2)],
        )

    def test_an_injected_rng_records_no_seed(self):
        session = new_session(rng=FixedDice((1, 1, 0, 0)))
        walk_into_place(session)
        session.select("agent_1")
        session.interact("agent_1", "interview_witness")
        session.select("agent_2")
        session.interact("agent_2", "read_ledger")
        self.assertIsNone(session.complete().seed)
        self.assertIsNone(session.report()["seed"])

    def test_two_seeded_sessions_reproduce_the_same_report(self):
        first, _ = play_fixture(seed=5)
        second, _ = play_fixture(seed=5)
        self.assertEqual(first.report(), second.report())

    def test_the_report_carries_no_presentation_field(self):
        session, _ = play_fixture()
        report = session.report()
        self.assertEqual(
            set(report),
            {
                "mission_id", "case_id", "title", "turn", "selected", "complete", "applied",
                "seed", "grid", "agents", "interactions", "objectives", "evidence", "intel",
                "wounds",
            },
        )
        blocked = {"sprite", "tileset", "tile_id", "texture", "pixel", "color", "colour",
                   "camera", "layer", "z_index", "animation"}

        def walk(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    self.assertNotIn(str(key).lower(), blocked)
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(report)


class PreconditionTests(unittest.TestCase):
    def test_a_mission_needs_the_four_agent_roster(self):
        campaign = fixture_campaign()
        faction = campaign.faction()
        faction.member_ids.remove("spike-agent-4")
        with self.assertRaises(MissionError) as raised:
            new_session(campaign=campaign)
        self.assertIn("played by 4 agents", str(raised.exception))

    def test_a_mission_needs_its_case_on_the_campaign(self):
        campaign = fixture_campaign()
        campaign.cases.clear()
        with self.assertRaises(MissionError) as raised:
            new_session(campaign=campaign)
        self.assertIn("not on this campaign", str(raised.exception))

    def test_the_leader_chairs_the_faction_and_does_not_deploy(self):
        campaign = fixture_campaign()
        session = new_session(campaign=campaign)
        self.assertNotIn("spike-leader", [seat.character_id for seat in session.seats])
        self.assertEqual(len(session.seats), 4)


class HeadlessEntrypointTests(unittest.TestCase):
    def test_the_demo_command_runs_headless_and_reports_a_completed_mission(self):
        completed = subprocess.run(
            [sys.executable, "-m", "strategy_game.tactical", "--json"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["mission"]["complete"])
        self.assertEqual(payload["outcome"]["outcome"], "success_with_style")
        self.assertEqual(
            payload["persisted"]["objectives"],
            ["spike:witness_interviewed", "spike:ledger_read"],
        )
        self.assertNotIn("pygame", completed.stdout)

    def test_the_demo_command_reports_a_refused_mission_document(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.json"
            path.write_text('{"format": "nope"}', encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "strategy_game.tactical", "--mission", str(path)],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120, check=False,
            )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("mission refused", completed.stderr)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
