"""Executable contracts for #506 Phase 2: the organisation around the project engine.

Code only, per ``AGENTS.md`` and issue #271: these exercise behaviour — concurrency, the shared
capacity pool, personnel availability, bounded investments, sabotage that cannot delete progress,
and the mission↔research loop — and never whether a document says a particular thing.

Two test doubles, both declared:

* :class:`FixedDice` stands in for ``random.Random`` so a check's *outcome* can be declared instead
  of hunted for. It only implements ``choice`` because that is all ``rpg.fate.roll_fate`` calls.
* the campaign fixture is a fixture: every id and number in it is demo data.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_operations_phase2.py"
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game.campaign import (
    Campaign,
    CampaignError,
    CampaignFaction,
    Case,
    MissionOutcome,
    apply_mission_outcome,
    load_campaign,
    save_campaign,
)
from strategy_game.operations import (
    PERSONNEL_RESOURCE_KIND,
    SABOTAGE_LEAD_SKILL,
    TUNING_CAPACITY_INVESTMENT_CEILING_SEATS,
    TUNING_CAPACITY_INVESTMENT_UNITS,
    TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME,
    TUNING_SABOTAGE_SETBACK_SEGMENTS,
    AllocationPlan,
    AvailabilityState,
    CapacityInvestment,
    InvestmentKind,
    InvestmentResult,
    OperationError,
    PersonnelReport,
    ProjectInput,
    ProjectTurnKind,
    RemedyKind,
    SabotageAttempt,
    SabotageConsequenceKind,
    SabotageReport,
    Shortfall,
    apply_investment,
    assign_support,
    available_missions,
    invested_units,
    personnel_availability,
    plan_allocations,
    project_inputs,
    project_personnel,
    remedies_for,
    resolve_sabotage,
    run_faction_turn,
)
from strategy_game.projects import (
    FactionCapacity,
    Prerequisites,
    ProgressCause,
    ProjectClock,
    ProjectStage,
    StrategicProject,
    pause_project,
    reassign_project,
    resume_project,
)
from strategy_game.research import (
    RESEARCH_LEAD_SKILL,
    RESEARCH_RESOURCE_KIND,
    ResearchProject,
    ResearchYield,
    TechNode,
    complete_research,
)
from strategy_game.rpg.fate import Character, Consequence, Outcome
from strategy_game.rpg.roster import AGENT_SEAT_COUNT, TurnLedger, default_seats

FACTION_ID = "f-1"
OTHER_FACTION_ID = "f-2"
LEADER_ID = "l-1"
AGENT_IDS = ("a-1", "a-2", "a-3", "a-4")
CASE_ID = "case-1"
SABOTEUR_ID = "x-1"

#: The proposal roster, passed in by the caller as Phase 1 requires. Only membership matters to the
#: kernel, so the values are opaque.
ROSTER: dict[str, object] = {
    RESEARCH_LEAD_SKILL: object(),
    "stewardship": object(),
    SABOTAGE_LEAD_SKILL: object(),
    "fieldcraft": object(),
}

NODE_WITH_OPTION = "node-understanding"
NODE_WITHOUT_OPTION = "node-silent"
NODE_SECOND = "node-manufacture"


class FixedDice:
    """A generator that returns a declared dice sequence, repeated, and counts its draws.

    A test double, not a rule: it exists so a check's outcome is *stated* by the test rather than
    searched for in a seed, and so "no dice were rolled" is observable as ``draws == 0``.
    """

    def __init__(self, *dice: int) -> None:
        if not dice:
            raise ValueError("FixedDice needs at least one value")
        self.dice = tuple(dice)
        self.draws = 0

    def choice(self, sequence):
        value = self.dice[self.draws % len(self.dice)]
        self.draws += 1
        return value


def style() -> FixedDice:
    """+4: a success with style against any difficulty at or below the rating plus four."""
    return FixedDice(1, 1, 1, 1)


def succeed() -> FixedDice:
    """+1: a success (never a style) when the rating is one above the difficulty."""
    return FixedDice(1, 0, 0, 0)


def fail() -> FixedDice:
    """-4: a failure against any difficulty at or above the rating."""
    return FixedDice(-1, -1, -1, -1)


def tie() -> FixedDice:
    """0: a tie when the rating equals the difficulty."""
    return FixedDice(0, 0, 0, 0)


def _sheet(character_id: str, *, science: int = 2, security: int = 2) -> Character:
    return Character(
        id=character_id,
        name=character_id,
        aspects=[],
        skills={},
        strategic_skills={
            RESEARCH_LEAD_SKILL: science,
            "stewardship": 2,
            SABOTAGE_LEAD_SKILL: security,
            "fieldcraft": 2,
        },
    )


def declared_nodes() -> dict[str, TechNode]:
    """Three declared nodes: one that opens a mission, one that does not, one that requires the first."""
    return {
        NODE_WITH_OPTION: TechNode(
            node_id=NODE_WITH_OPTION,
            label="Understanding the recovered component",
            stage=ProjectStage.UNDERSTANDING,
            yields=ResearchYield(option="option:model", capability="xeno-engineering"),
        ),
        NODE_WITHOUT_OPTION: TechNode(
            node_id=NODE_WITHOUT_OPTION,
            label="A competence with no mission attached",
            stage=ProjectStage.UNDERSTANDING,
            yields=ResearchYield(capability="quiet-competence"),
        ),
        NODE_SECOND: TechNode(
            node_id=NODE_SECOND,
            label="The component in reproducible production",
            stage=ProjectStage.MANUFACTURE,
            requires=Prerequisites(node_ids=(NODE_WITH_OPTION,)),
            yields=ResearchYield(option="option:manufacture"),
        ),
    }


def build_campaign() -> Campaign:
    """One faction, one leader, four agents, one opposition operative, one capacity pool."""
    sheets = {LEADER_ID: _sheet(LEADER_ID), SABOTEUR_ID: _sheet(SABOTEUR_ID, security=2)}
    for agent in AGENT_IDS:
        sheets[agent] = _sheet(agent)
    return Campaign(
        faction_id=FACTION_ID,
        leader_id=LEADER_ID,
        sheets=sheets,
        factions={
            FACTION_ID: CampaignFaction(
                identifier=FACTION_ID,
                name="The Faction",
                leader_id=LEADER_ID,
                member_ids=[LEADER_ID, *AGENT_IDS],
                resources=["funding:lab", "funding:hire"],
            ),
            OTHER_FACTION_ID: CampaignFaction(
                identifier=OTHER_FACTION_ID,
                name="The Opposition",
                leader_id=SABOTEUR_ID,
                member_ids=[SABOTEUR_ID],
            ),
        },
        cases={
            CASE_ID: Case(
                case_id=CASE_ID,
                core_question="Who moved the component?",
                hook="A salvage claim that should not exist.",
                investigator=LEADER_ID,
                partner="a-4",
                initial_scene="A warehouse before the customs team arrives.",
            )
        },
        capacities={
            FACTION_ID: FactionCapacity(
                faction_id=FACTION_ID,
                units={RESEARCH_RESOURCE_KIND: 4, PERSONNEL_RESOURCE_KIND: 3, "funding": 1},
            )
        },
        tech_nodes=declared_nodes(),
    )


def mk_project(
    project_id: str,
    *,
    lead: str = "a-1",
    resource_kind: str = RESEARCH_RESOURCE_KIND,
    work: int = 6,
    difficulty: int = 1,
    stage: ProjectStage = ProjectStage.UNDERSTANDING,
    requires: Prerequisites | None = None,
    node_id: str = "",
    support: tuple[str, ...] = (),
    lead_skill: str = RESEARCH_LEAD_SKILL,
    grants: tuple[str, ...] = (),
) -> StrategicProject:
    return StrategicProject(
        project_id=project_id,
        faction_id=FACTION_ID,
        title=project_id,
        kind="research",
        lead_id=lead,
        lead_skill=lead_skill,
        lead_difficulty=difficulty,
        clock=ProjectClock(work),
        resource_kind=resource_kind,
        stage=stage,
        support_ids=support,
        requires=requires or Prerequisites(),
        node_id=node_id,
        grants_resource_ids=grants,
    )


def build(*projects: StrategicProject) -> tuple[Campaign, TurnLedger]:
    """A campaign with the given projects declared, and a fresh turn ledger on turn 1."""
    campaign = build_campaign()
    for project in projects:
        campaign.projects[project.project_id] = project
    ledger = TurnLedger(default_seats(LEADER_ID, AGENT_IDS))
    ledger.next_turn()
    return campaign, ledger


def ledger_for(*character_ids: str) -> TurnLedger:
    """A ledger with an arbitrary seat set, for the unseated-lead case."""
    from strategy_game.rpg.roster import Seat, SeatKind

    seats = tuple(
        Seat(f"seat-{index}", SeatKind.AGENT, character_id)
        for index, character_id in enumerate(character_ids, start=1)
    )
    ledger = TurnLedger(seats)
    ledger.next_turn()
    return ledger


class CapacityPlanningTest(unittest.TestCase):
    """Two projects, one pool: the shortage is a reported fact, not a silent zero."""

    def test_two_projects_share_one_pool_and_the_shortfall_is_reported(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        plan = plan_allocations(campaign, FACTION_ID, (("p-a", 3), ("p-b", 3)))
        self.assertEqual(plan.granted("p-a"), 3)
        self.assertEqual(plan.granted("p-b"), 1)
        self.assertEqual(len(plan.shortfalls), 1)
        shortfall = plan.shortfalls[0]
        self.assertEqual(shortfall.project_id, "p-b")
        self.assertEqual((shortfall.requested, shortfall.granted, shortfall.shortfall), (3, 1, 2))
        self.assertEqual(shortfall.free_after, 0)
        self.assertEqual(plan.unmet, ((RESEARCH_RESOURCE_KIND, 2),))
        self.assertTrue(any("2 unit(s) short" in note for note in plan.notes))

    def test_the_plan_never_over_commits_beyond_the_ledger(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        ledger = campaign.capacities[FACTION_ID]
        plan_allocations(campaign, FACTION_ID, (("p-a", 3), ("p-b", 3)))
        self.assertEqual(ledger.committed(RESEARCH_RESOURCE_KIND), 4)
        self.assertEqual(ledger.free(RESEARCH_RESOURCE_KIND), 0)
        # The invariant lives in the ledger itself, so the plan cannot have broken it silently.
        FactionCapacity(ledger.faction_id, dict(ledger.units), list(ledger.commitments))

    def test_a_second_plan_replaces_rather_than_accumulates(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        plan_allocations(campaign, FACTION_ID, (("p-a", 3), ("p-b", 1)))
        second = plan_allocations(campaign, FACTION_ID, (("p-a", 1), ("p-b", 1)))
        self.assertEqual(second.granted("p-a"), 1)
        self.assertEqual(second.granted("p-b"), 1)
        self.assertEqual(campaign.capacities[FACTION_ID].committed(RESEARCH_RESOURCE_KIND), 2)
        self.assertEqual(second.shortfalls, ())

    def test_the_plan_grants_in_the_declared_priority_order(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        plan = plan_allocations(campaign, FACTION_ID, (("p-b", 3), ("p-a", 3)))
        self.assertEqual(plan.granted("p-b"), 3)
        self.assertEqual(plan.granted("p-a"), 1)
        self.assertEqual(tuple(pid for pid, _ in plan.grants), ("p-b", "p-a"))

    def test_a_whole_demand_can_be_unmeetable(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        plan = plan_allocations(
            campaign, FACTION_ID, (("p-a", 4), ("p-b", 3))
        )
        self.assertEqual(plan.granted("p-a"), 4)
        self.assertEqual(plan.granted("p-b"), 0)
        self.assertEqual(plan.shortfalls[0].granted, 0)
        self.assertIn("NO_CAPACITY", plan.notes[0])

    def test_stranded_capacity_on_a_finished_programme_is_reported(self) -> None:
        finished = mk_project("p-done", work=2)
        finished.clock.add(2)
        campaign, _ = build(finished, mk_project("p-a"))
        campaign.capacities[FACTION_ID].allocate("p-done", RESEARCH_RESOURCE_KIND, 2)
        plan = plan_allocations(campaign, FACTION_ID, (("p-a", 4),))
        self.assertEqual(plan.stranded, (("p-done", 2),))
        self.assertEqual(plan.granted("p-a"), 2)
        self.assertTrue(any("release" in note.lower() for note in plan.notes))

    def test_a_plan_refuses_a_project_of_another_faction(self) -> None:
        foreign = mk_project("p-foreign")
        foreign.faction_id = OTHER_FACTION_ID
        campaign = build_campaign()
        campaign.factions[OTHER_FACTION_ID].member_ids.append("a-1")
        campaign.projects["p-foreign"] = foreign
        with self.assertRaises(OperationError):
            plan_allocations(campaign, FACTION_ID, (("p-foreign", 1),))

    def test_a_plan_refuses_an_unknown_project(self) -> None:
        campaign, _ = build()
        with self.assertRaises(OperationError):
            plan_allocations(campaign, FACTION_ID, (("p-nope", 1),))

    def test_a_plan_refuses_a_faction_without_a_ledger(self) -> None:
        campaign, _ = build()
        with self.assertRaises(OperationError):
            plan_allocations(campaign, OTHER_FACTION_ID, ())

    def test_a_plan_refuses_the_same_project_twice(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        with self.assertRaises(OperationError):
            plan_allocations(campaign, FACTION_ID, (("p-a", 1), ("p-a", 2)))

    def test_the_plan_serialises(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        payload = plan_allocations(campaign, FACTION_ID, (("p-a", 3), ("p-b", 3))).to_dict()
        json.dumps(payload)
        self.assertEqual(payload["schema_version"], "allocation-plan-1")
        self.assertEqual(payload["unmet"], [{"resource_kind": RESEARCH_RESOURCE_KIND, "units": 2}])
        self.assertEqual(payload["shortfalls"][0]["remedies"][0]["kind"], "upgrade_facility")


class ConcurrentTurnTest(unittest.TestCase):
    """Several projects in one turn, on one ledger, with the one-action rule intact."""

    def test_concurrent_projects_run_in_one_turn(self) -> None:
        campaign, ledger = build(
            mk_project("p-a"), mk_project("p-b", lead="a-2"), mk_project("p-c", lead="a-3")
        )
        for pid in ("p-a", "p-b", "p-c"):
            campaign.capacities[FACTION_ID].allocate(pid, RESEARCH_RESOURCE_KIND, 1)
        report = run_faction_turn(
            campaign, turn=ledger.turn, ledger=ledger, rng=style(), roster=ROSTER
        )
        self.assertEqual(report.actions_used, 3)
        self.assertEqual([item.kind for item in report.turns],
                         [ProjectTurnKind.RAN] * 3)
        self.assertTrue(all(item.result.progress_added == 2 for item in report.turns))
        self.assertEqual(set(ledger.acted), {"agent_1", "agent_2", "agent_3"})

    def test_a_lead_cannot_drive_two_projects_in_one_turn(self) -> None:
        campaign, ledger = build(
            mk_project("p-first"), mk_project("p-second", work=6)
        )
        campaign.capacities[FACTION_ID].allocate("p-first", RESEARCH_RESOURCE_KIND, 2)
        campaign.capacities[FACTION_ID].allocate("p-second", RESEARCH_RESOURCE_KIND, 2)
        report = run_faction_turn(
            campaign,
            turn=ledger.turn,
            ledger=ledger,
            rng=style(),
            roster=ROSTER,
            order=("p-first", "p-second"),
        )
        self.assertEqual(report.turn_for("p-first").kind, ProjectTurnKind.RAN)
        busy = report.turn_for("p-second")
        self.assertEqual(busy.kind, ProjectTurnKind.BUSY)
        self.assertFalse(busy.action_taken)
        self.assertIn("already acted this turn", busy.reason)
        self.assertEqual(campaign.projects["p-second"].clock.filled, 0)
        self.assertEqual(report.actions_used, 1)
        self.assertEqual(len(ledger.acted), 1)

    def test_the_declared_order_decides_who_gets_the_lead(self) -> None:
        campaign, ledger = build(mk_project("p-first"), mk_project("p-second"))
        for pid in ("p-first", "p-second"):
            campaign.capacities[FACTION_ID].allocate(pid, RESEARCH_RESOURCE_KIND, 2)
        report = run_faction_turn(
            campaign, turn=ledger.turn, ledger=ledger, rng=style(), roster=ROSTER,
            order=("p-second", "p-first"),
        )
        self.assertEqual(report.turn_for("p-second").kind, ProjectTurnKind.RAN)
        self.assertEqual(report.turn_for("p-first").kind, ProjectTurnKind.BUSY)

    def test_a_turn_shows_a_shortage_and_still_runs_the_project(self) -> None:
        campaign, ledger = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        report = run_faction_turn(
            campaign,
            turn=ledger.turn,
            ledger=ledger,
            rng=style(),
            roster=ROSTER,
            demands=(("p-a", 3), ("p-b", 3)),
        )
        self.assertIsInstance(report.allocations, AllocationPlan)
        self.assertEqual(report.allocations.granted("p-b"), 1)
        self.assertEqual(report.allocations.shortfalls[0].shortfall, 2)
        # 1 unit of throughput + the tuning style bonus, which is what the institution really gave.
        self.assertEqual(report.turn_for("p-b").result.progress_added, 1 + 1)

    def test_a_zero_grant_reports_no_capacity_as_its_cause(self) -> None:
        campaign, ledger = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        report = run_faction_turn(
            campaign,
            turn=ledger.turn,
            ledger=ledger,
            rng=style(),
            roster=ROSTER,
            demands=(("p-a", 4), ("p-b", 3)),
        )
        result = report.turn_for("p-b").result
        self.assertEqual(result.cause, ProgressCause.NO_CAPACITY)
        self.assertEqual(result.progress_added, 0)
        self.assertEqual(report.allocations.granted("p-b"), 0)

    def test_an_unseated_lead_is_reported_and_no_dice_are_rolled(self) -> None:
        campaign = build_campaign()
        campaign.projects["p-a"] = mk_project("p-a", lead="a-4")
        ledger = ledger_for(LEADER_ID, "a-1", "a-2")
        rng = style()
        report = run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=rng, roster=ROSTER)
        item = report.turn_for("p-a")
        self.assertEqual(item.kind, ProjectTurnKind.UNSEATED)
        self.assertFalse(item.action_taken)
        self.assertEqual(rng.draws, 0)
        self.assertIn("holds no seat", item.reason)

    def test_a_lead_with_no_sheet_is_reported_and_no_dice_are_rolled(self) -> None:
        campaign, ledger = build(mk_project("p-a", lead="ghost"))
        rng = style()
        report = run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=rng, roster=ROSTER)
        self.assertEqual(report.turn_for("p-a").kind, ProjectTurnKind.NO_SHEET)
        self.assertEqual(rng.draws, 0)

    def test_a_taken_out_lead_cannot_run_its_project(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        campaign.sheets["a-1"].physical_stress = [True, True]
        rng = style()
        report = run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=rng, roster=ROSTER)
        item = report.turn_for("p-a")
        self.assertEqual(item.kind, ProjectTurnKind.UNAVAILABLE)
        self.assertIn("taken out", item.reason)
        self.assertEqual(rng.draws, 0)
        self.assertEqual(ledger.acted, {})

    def test_a_lead_carrying_an_unrecovered_consequence_cannot_run_its_project(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        campaign.sheets["a-1"].consequences = [Consequence("Broken wrist", 2)]
        report = run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=style(), roster=ROSTER)
        self.assertEqual(report.turn_for("p-a").kind, ProjectTurnKind.UNAVAILABLE)
        self.assertIn("unrecovered consequence", report.turn_for("p-a").reason)

    def test_a_recovered_consequence_does_not_block_the_lead(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        campaign.capacities[FACTION_ID].allocate("p-a", RESEARCH_RESOURCE_KIND, 2)
        campaign.sheets["a-1"].consequences = [Consequence("Broken wrist", 2, recovered=True)]
        report = run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=style(), roster=ROSTER)
        self.assertEqual(report.turn_for("p-a").kind, ProjectTurnKind.RAN)

    def test_a_blocked_project_spends_no_action_and_rolls_no_dice(self) -> None:
        campaign, ledger = build(
            mk_project("p-a", requires=Prerequisites(resource_ids=("artefact:missing",)))
        )
        rng = style()
        report = run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=rng, roster=ROSTER)
        item = report.turn_for("p-a")
        self.assertEqual(item.kind, ProjectTurnKind.BLOCKED)
        self.assertIn("artefact:missing", item.reason)
        self.assertEqual(rng.draws, 0)
        self.assertEqual(ledger.acted, {})

    def test_a_paused_project_takes_no_action_and_rolls_no_dice(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        pause_project(campaign, "p-a", "waiting for the ethics board")
        rng = style()
        report = run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=rng, roster=ROSTER)
        self.assertEqual(report.turn_for("p-a").kind, ProjectTurnKind.PAUSED)
        self.assertIn("ethics board", report.turn_for("p-a").reason)
        self.assertEqual(rng.draws, 0)

    def test_a_closed_project_takes_no_action(self) -> None:
        finished = mk_project("p-done", work=2)
        finished.clock.add(2)
        campaign, ledger = build(finished)
        report = run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=style(), roster=ROSTER)
        self.assertEqual(report.turn_for("p-done").kind, ProjectTurnKind.CLOSED)
        self.assertFalse(report.turn_for("p-done").action_taken)
        self.assertEqual(ledger.acted, {})

    def test_a_turn_whose_ledger_disagrees_is_refused(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        with self.assertRaises(OperationError):
            run_faction_turn(campaign, turn=ledger.turn + 1, ledger=ledger, rng=style(), roster=ROSTER)

    def test_the_turn_declares_the_lead_s_action_on_the_roster_ledger(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        campaign.capacities[FACTION_ID].allocate("p-a", RESEARCH_RESOURCE_KIND, 2)
        run_faction_turn(campaign, turn=ledger.turn, ledger=ledger, rng=style(), roster=ROSTER)
        self.assertEqual(ledger.acted, {"agent_1": "p-a"})

    def test_the_report_accounts_for_every_project_and_every_action(self) -> None:
        campaign, ledger = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        report = run_faction_turn(
            campaign, turn=ledger.turn, ledger=ledger, rng=style(), roster=ROSTER,
            demands=(("p-a", 2), ("p-b", 2)),
        )
        payload = report.to_dict()
        json.dumps(payload)
        self.assertEqual({item["project_id"] for item in payload["turns"]}, {"p-a", "p-b"})
        self.assertEqual(payload["actions_used"], len(ledger.acted))
        self.assertEqual(payload["actions_free"], len(ledger.seats) - len(ledger.acted))
        self.assertEqual(report.errors, ())


class PersonnelTest(unittest.TestCase):
    """A lead and its supporters, on the one roster the campaign already has."""

    def test_assign_support_records_the_supporters(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        project = assign_support(campaign, "p-a", ["a-2", "a-3"])
        self.assertEqual(project.support_ids, ("a-2", "a-3"))

    def test_assign_support_refuses_a_name_without_a_sheet(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        with self.assertRaises(OperationError):
            assign_support(campaign, "p-a", ["nobody"])

    def test_assign_support_refuses_the_lead_as_its_own_support(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        with self.assertRaises(OperationError):
            assign_support(campaign, "p-a", ["a-1"])

    def test_assign_support_refuses_a_duplicate(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        with self.assertRaises(OperationError):
            assign_support(campaign, "p-a", ["a-2", "a-2"])

    def test_a_project_may_have_no_support_at_all(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        report = project_personnel(campaign, "p-a")
        self.assertEqual(report.support, ())
        self.assertTrue(report.ready)

    def test_project_personnel_reports_lead_and_support_availability(self) -> None:
        campaign, ledger = build(mk_project("p-a", support=("a-2", "a-3")))
        campaign.sheets["a-3"].mental_stress = [True, True]
        report = project_personnel(campaign, "p-a", ledger=ledger)
        by_id = {item.character_id: item for item in report.support}
        self.assertEqual(by_id["a-2"].state, AvailabilityState.AVAILABLE)
        self.assertEqual(by_id["a-3"].state, AvailabilityState.TAKEN_OUT)
        self.assertEqual(report.support_available, ("a-2",))
        self.assertIsInstance(report, PersonnelReport)

    def test_an_acted_lead_is_reported_as_acted(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        ledger.declare("agent_1", statement="something else")
        availability = personnel_availability(campaign, "a-1", ledger=ledger)
        self.assertEqual(availability.state, AvailabilityState.ACTED)
        self.assertIn("already acted", availability.reasons[0])

    def test_a_character_with_no_sheet_is_not_available(self) -> None:
        campaign, _ = build()
        availability = personnel_availability(campaign, "ghost")
        self.assertEqual(availability.state, AvailabilityState.NO_SHEET)
        self.assertFalse(availability.available)

    def test_support_ids_survive_the_save_round_trip(self) -> None:
        campaign, _ = build(mk_project("p-a", support=("a-2",)))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "campaign.json"
            save_campaign(campaign, path)
            loaded = load_campaign(path)
        self.assertEqual(loaded.projects["p-a"].support_ids, ("a-2",))

    def test_reassignment_moves_the_clock_and_drops_the_new_lead_from_support(self) -> None:
        campaign, _ = build(mk_project("p-a", support=("a-2",)))
        campaign.projects["p-a"].clock.add(3)
        reassign_project(campaign, "p-a", "a-2")
        project = campaign.projects["p-a"]
        self.assertEqual(project.lead_id, "a-2")
        self.assertEqual(project.support_ids, ())
        self.assertEqual(project.clock.filled, 3)
        self.assertEqual(project.detail["reassigned_from"], ["a-1"])


class InvestmentTest(unittest.TestCase):
    """Capacity raised by an explicit, bounded, costed action — never a multiplier."""

    def test_a_facility_investment_charges_its_cost_and_raises_capacity(self) -> None:
        campaign, _ = build()
        ledger = campaign.capacities[FACTION_ID]
        result = apply_investment(
            campaign,
            CapacityInvestment(
                investment_id="lab",
                faction_id=FACTION_ID,
                kind=InvestmentKind.FACILITY,
                resource_kind=RESEARCH_RESOURCE_KIND,
                cost_resource_ids=("funding:lab",),
            ),
            turn=1,
        )
        self.assertTrue(result.applied)
        self.assertEqual((result.capacity_before, result.capacity_after), (4, 5))
        self.assertEqual(ledger.units[RESEARCH_RESOURCE_KIND], 5)
        self.assertNotIn("funding:lab", campaign.faction().resources)
        self.assertEqual(campaign.capacity_investments["lab"].investment_id, "lab")

    def test_an_investment_whose_cost_is_not_held_changes_nothing(self) -> None:
        campaign, _ = build()
        ledger = campaign.capacities[FACTION_ID]
        with self.assertRaises(OperationError):
            apply_investment(
                campaign,
                CapacityInvestment(
                    investment_id="lab",
                    faction_id=FACTION_ID,
                    kind=InvestmentKind.FACILITY,
                    resource_kind=RESEARCH_RESOURCE_KIND,
                    cost_resource_ids=("funding:never-granted",),
                ),
                turn=1,
            )
        self.assertEqual(ledger.units[RESEARCH_RESOURCE_KIND], 4)
        self.assertIn("funding:lab", campaign.faction().resources)
        self.assertEqual(campaign.capacity_investments, {})

    def test_the_ceiling_is_enforced_with_the_numbers(self) -> None:
        campaign, _ = build()
        campaign.faction().resources.extend([f"funding:lab-{i}" for i in range(6)])
        for index in range(TUNING_CAPACITY_INVESTMENT_CEILING_SEATS):
            apply_investment(
                campaign,
                CapacityInvestment(
                    investment_id=f"lab-{index}",
                    faction_id=FACTION_ID,
                    kind=InvestmentKind.FACILITY,
                    resource_kind=RESEARCH_RESOURCE_KIND,
                    cost_resource_ids=(f"funding:lab-{index}",),
                ),
                turn=1,
            )
        with self.assertRaises(OperationError) as caught:
            apply_investment(
                campaign,
                CapacityInvestment(
                    investment_id="lab-too-many",
                    faction_id=FACTION_ID,
                    kind=InvestmentKind.FACILITY,
                    resource_kind=RESEARCH_RESOURCE_KIND,
                    cost_resource_ids=("funding:lab-5",),
                ),
                turn=1,
            )
        self.assertIn(str(TUNING_CAPACITY_INVESTMENT_CEILING_SEATS), str(caught.exception))
        self.assertEqual(
            invested_units(campaign, FACTION_ID, RESEARCH_RESOURCE_KIND),
            TUNING_CAPACITY_INVESTMENT_CEILING_SEATS,
        )

    def test_an_investment_applies_once(self) -> None:
        campaign, _ = build()
        investment = CapacityInvestment(
            investment_id="lab",
            faction_id=FACTION_ID,
            kind=InvestmentKind.FACILITY,
            resource_kind=RESEARCH_RESOURCE_KIND,
            cost_resource_ids=("funding:lab",),
        )
        first = apply_investment(campaign, investment, turn=1)
        campaign.faction().resources.append("funding:lab")
        second = apply_investment(campaign, investment, turn=2)
        self.assertTrue(first.applied)
        self.assertFalse(second.applied)
        self.assertEqual(second.units, 0)
        self.assertEqual(campaign.capacities[FACTION_ID].units[RESEARCH_RESOURCE_KIND], 5)
        self.assertIn("funding:lab", campaign.faction().resources)
        self.assertEqual(
            len([n for n in campaign.campaign_notes if n["kind"] == "capacity_investment"]), 1
        )

    def test_an_investment_id_cannot_be_reused_for_different_terms(self) -> None:
        campaign, _ = build()
        apply_investment(
            campaign,
            CapacityInvestment(
                investment_id="lab",
                faction_id=FACTION_ID,
                kind=InvestmentKind.FACILITY,
                resource_kind=RESEARCH_RESOURCE_KIND,
                cost_resource_ids=("funding:lab",),
            ),
            turn=1,
        )
        with self.assertRaises(OperationError):
            apply_investment(
                campaign,
                CapacityInvestment(
                    investment_id="lab",
                    faction_id=FACTION_ID,
                    kind=InvestmentKind.FACILITY,
                    resource_kind="equipment",
                    cost_resource_ids=("funding:hire",),
                ),
                turn=2,
            )

    def test_a_recruitment_raises_personnel_capacity_and_not_the_roster(self) -> None:
        campaign, _ = build()
        before = list(campaign.faction().member_ids)
        result = apply_investment(
            campaign,
            CapacityInvestment(
                investment_id="hire",
                faction_id=FACTION_ID,
                kind=InvestmentKind.RECRUITMENT,
                resource_kind=PERSONNEL_RESOURCE_KIND,
                cost_resource_ids=("funding:hire",),
            ),
            turn=1,
        )
        self.assertTrue(result.applied)
        self.assertEqual(campaign.capacities[FACTION_ID].units[PERSONNEL_RESOURCE_KIND], 4)
        self.assertEqual(campaign.faction().member_ids, before)
        self.assertLessEqual(
            len([m for m in campaign.faction().member_ids if m != LEADER_ID]), AGENT_SEAT_COUNT
        )

    def test_a_recruitment_must_raise_personnel_capacity(self) -> None:
        with self.assertRaises(OperationError):
            CapacityInvestment(
                investment_id="hire",
                faction_id=FACTION_ID,
                kind=InvestmentKind.RECRUITMENT,
                resource_kind=RESEARCH_RESOURCE_KIND,
                cost_resource_ids=("funding:hire",),
            )

    def test_a_facility_must_not_raise_personnel_capacity(self) -> None:
        with self.assertRaises(OperationError):
            CapacityInvestment(
                investment_id="lab",
                faction_id=FACTION_ID,
                kind=InvestmentKind.FACILITY,
                resource_kind=PERSONNEL_RESOURCE_KIND,
                cost_resource_ids=("funding:lab",),
            )

    def test_an_investment_adds_at_most_the_tuning_units(self) -> None:
        with self.assertRaises(OperationError):
            CapacityInvestment(
                investment_id="lab",
                faction_id=FACTION_ID,
                kind=InvestmentKind.FACILITY,
                resource_kind=RESEARCH_RESOURCE_KIND,
                units=TUNING_CAPACITY_INVESTMENT_UNITS + 1,
                cost_resource_ids=("funding:lab",),
            )

    def test_an_investment_needs_a_cost(self) -> None:
        with self.assertRaises(OperationError):
            CapacityInvestment(
                investment_id="lab",
                faction_id=FACTION_ID,
                kind=InvestmentKind.FACILITY,
                resource_kind=RESEARCH_RESOURCE_KIND,
            )

    def test_an_investment_writes_one_audit_note_with_provenance(self) -> None:
        campaign, _ = build()
        result = apply_investment(
            campaign,
            CapacityInvestment(
                investment_id="lab",
                faction_id=FACTION_ID,
                kind=InvestmentKind.FACILITY,
                resource_kind=RESEARCH_RESOURCE_KIND,
                cost_resource_ids=("funding:lab",),
                label="A second bench",
            ),
            turn=3,
        )
        note = campaign.campaign_notes[result.note_index]
        self.assertEqual(note["kind"], "capacity_investment")
        self.assertEqual(note["turn"], 3)
        self.assertEqual(note["capacity_after"], 5)
        self.assertEqual(note["provenance"]["kind"], "simulated")
        self.assertIsInstance(result, InvestmentResult)

    def test_the_raised_capacity_actually_lifts_the_next_plan(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        before = plan_allocations(campaign, FACTION_ID, (("p-a", 3), ("p-b", 3)))
        self.assertEqual(before.shortfalls[0].shortfall, 2)
        apply_investment(
            campaign,
            CapacityInvestment(
                investment_id="lab",
                faction_id=FACTION_ID,
                kind=InvestmentKind.FACILITY,
                resource_kind=RESEARCH_RESOURCE_KIND,
                cost_resource_ids=("funding:lab",),
            ),
            turn=1,
        )
        after = plan_allocations(campaign, FACTION_ID, (("p-a", 3), ("p-b", 3)))
        self.assertEqual(after.granted("p-b"), 2)
        self.assertEqual(after.shortfalls[0].shortfall, 1)

    def test_an_investment_for_an_untracked_faction_is_refused(self) -> None:
        campaign, _ = build()
        with self.assertRaises(CampaignError):
            apply_investment(
                campaign,
                CapacityInvestment(
                    investment_id="lab",
                    faction_id="f-nope",
                    kind=InvestmentKind.FACILITY,
                    resource_kind=RESEARCH_RESOURCE_KIND,
                    cost_resource_ids=("funding:lab",),
                ),
                turn=1,
            )


class RemedyTest(unittest.TestCase):
    """A shortage names the choices, and each choice states what it would move."""

    def test_a_personnel_shortage_offers_recruitment(self) -> None:
        campaign, _ = build(mk_project("p-a", resource_kind=PERSONNEL_RESOURCE_KIND))
        kinds = [remedy.kind for remedy in remedies_for(campaign, "p-a", shortfall_units=2)]
        self.assertIn(RemedyKind.RECRUIT, kinds)
        recruit = next(r for r in remedies_for(campaign, "p-a") if r.kind is RemedyKind.RECRUIT)
        self.assertIn(str(TUNING_CAPACITY_INVESTMENT_UNITS), recruit.effect)
        self.assertIn(str(TUNING_CAPACITY_INVESTMENT_CEILING_SEATS), recruit.effect)

    def test_a_material_shortage_offers_a_facility_upgrade(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        remedies = remedies_for(campaign, "p-a", shortfall_units=2)
        self.assertEqual(remedies[0].kind, RemedyKind.UPGRADE_FACILITY)
        self.assertIn("2 unit(s)", remedies[0].effect)

    def test_the_remedies_name_a_free_seated_candidate_for_reassignment(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        ledger.declare("agent_1", statement="p-a")
        remedies = remedies_for(campaign, "p-a", ledger=ledger)
        reassign = next(r for r in remedies if r.kind is RemedyKind.REASSIGN_LEAD)
        self.assertIn("a-2", reassign.effect)
        self.assertNotIn("a-1", reassign.effect)

    def test_no_reassignment_is_offered_when_everyone_else_has_acted(self) -> None:
        campaign, ledger = build(mk_project("p-a"))
        for seat in ("agent_1", "agent_2", "agent_3", "agent_4", "leader"):
            ledger.declare(seat, statement="elsewhere")
        kinds = [remedy.kind for remedy in remedies_for(campaign, "p-a", ledger=ledger)]
        self.assertNotIn(RemedyKind.REASSIGN_LEAD, kinds)

    def test_the_remedies_always_offer_the_pause_and_state_what_it_preserves(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        campaign.projects["p-a"].clock.add(3)
        pause = next(
            r for r in remedies_for(campaign, "p-a") if r.kind is RemedyKind.PAUSE
        )
        self.assertIn("3/6", pause.effect)

    def test_a_finished_programme_holding_capacity_is_offered_for_release(self) -> None:
        finished = mk_project("p-done", work=2)
        finished.clock.add(2)
        campaign, _ = build(finished, mk_project("p-a"))
        campaign.capacities[FACTION_ID].allocate("p-done", RESEARCH_RESOURCE_KIND, 2)
        remedy = next(
            r for r in remedies_for(campaign, "p-a", shortfall_units=1)
            if r.kind is RemedyKind.RELEASE_STRANDED
        )
        self.assertIn("p-done", remedy.effect)
        self.assertIn("2 unit(s)", remedy.effect)

    def test_a_shortage_plan_carries_the_remedies_it_offers(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        plan = plan_allocations(campaign, FACTION_ID, (("p-a", 3), ("p-b", 3)))
        shortfall = plan.shortfalls[0]
        self.assertIsInstance(shortfall, Shortfall)
        self.assertTrue(shortfall.remedies)
        self.assertEqual(shortfall.to_dict()["shortfall"], 2)


class SabotageTest(unittest.TestCase):
    """A disruption records a longer road, an interruption or a lost allocation — never a loss."""

    def _attempt(self, consequences=("setback",)) -> SabotageAttempt:
        return SabotageAttempt(
            attempt_id="s-1",
            project_id="p-a",
            saboteur_id=SABOTEUR_ID,
            difficulty=2,
            consequences=tuple(consequences),
        )

    def test_a_failed_disruption_changes_nothing(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        campaign.projects["p-a"].clock.add(3)
        campaign.capacities[FACTION_ID].allocate("p-a", RESEARCH_RESOURCE_KIND, 2)
        report = resolve_sabotage(campaign, self._attempt(), rng=fail(), turn=3, roster=ROSTER)
        self.assertEqual(report.outcome, Outcome.FAILURE)
        self.assertEqual(report.applied, ())
        self.assertEqual(campaign.projects["p-a"].clock.to_dict(),
                         {"work_required": 6, "filled": 3})
        self.assertFalse(campaign.projects["p-a"].paused)
        self.assertEqual(campaign.capacities[FACTION_ID].allocated("p-a"), 2)

    def test_a_successful_disruption_lengthens_the_road_and_keeps_the_progress(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        campaign.projects["p-a"].clock.add(3)
        report = resolve_sabotage(campaign, self._attempt(), rng=succeed(), turn=3, roster=ROSTER)
        self.assertEqual(report.outcome, Outcome.SUCCESS)
        self.assertEqual(report.applied, (SabotageConsequenceKind.SETBACK,))
        self.assertEqual(report.filled_before, 3)
        self.assertEqual(report.filled_after, 3)
        self.assertTrue(report.progress_preserved)
        self.assertEqual(report.work_required_after,
                         report.work_required_before + TUNING_SABOTAGE_SETBACK_SEGMENTS)
        self.assertEqual(campaign.projects["p-a"].clock.filled, 3)

    def test_a_disruption_with_style_lands_two_consequences(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        campaign.projects["p-a"].clock.add(2)
        attempt = self._attempt(("setback", "complication", "allocation_loss"))
        report = resolve_sabotage(campaign, attempt, rng=style(), turn=3, roster=ROSTER)
        self.assertEqual(report.outcome, Outcome.SUCCESS_WITH_STYLE)
        self.assertEqual(
            report.applied,
            (SabotageConsequenceKind.SETBACK, SabotageConsequenceKind.COMPLICATION),
        )
        self.assertTrue(report.paused)
        self.assertTrue(campaign.projects["p-a"].paused)

    def test_the_ladder_decides_how_many_consequences_land(self) -> None:
        self.assertEqual(TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME[Outcome.FAILURE], 0)
        self.assertEqual(TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME[Outcome.TIE], 0)
        self.assertEqual(TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME[Outcome.SUCCESS], 1)
        self.assertEqual(TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME[Outcome.SUCCESS_WITH_STYLE], 2)

    def test_sabotage_never_erases_completed_progress(self) -> None:
        for menu in (
            ("setback",),
            ("setback", "complication"),
            ("allocation_loss", "setback"),
        ):
            with self.subTest(menu=menu):
                campaign, _ = build(mk_project("p-a", work=6))
                campaign.projects["p-a"].clock.add(5)
                campaign.capacities[FACTION_ID].allocate("p-a", RESEARCH_RESOURCE_KIND, 2)
                before = campaign.projects["p-a"].clock.filled
                report = resolve_sabotage(
                    campaign, self._attempt(menu), rng=style(), turn=3, roster=ROSTER
                )
                self.assertEqual(campaign.projects["p-a"].clock.filled, before)
                self.assertEqual(report.filled_after, before)
                self.assertLessEqual(
                    campaign.projects["p-a"].clock.filled,
                    campaign.projects["p-a"].clock.work_required,
                )

    def test_a_complication_can_be_resumed_with_the_clock_intact(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        campaign.projects["p-a"].clock.add(4)
        attempt = SabotageAttempt(
            attempt_id="s-1", project_id="p-a", saboteur_id=SABOTEUR_ID, difficulty=2,
            consequences=(SabotageConsequenceKind.COMPLICATION,),
        )
        resolve_sabotage(campaign, attempt, rng=succeed(), turn=3, roster=ROSTER)
        project = campaign.projects["p-a"]
        self.assertTrue(project.paused)
        self.assertIn("sabotage", project.pause_reasons[0])
        resume_project(campaign, "p-a")
        self.assertFalse(project.paused)
        self.assertEqual(project.clock.filled, 4)

    def test_an_allocation_loss_returns_the_units_and_the_shortage_shows(self) -> None:
        campaign, _ = build(mk_project("p-a"), mk_project("p-b", lead="a-2"))
        campaign.capacities[FACTION_ID].allocate("p-a", RESEARCH_RESOURCE_KIND, 2)
        campaign.projects["p-a"].clock.add(1)
        attempt = SabotageAttempt(
            attempt_id="s-1", project_id="p-a", saboteur_id=SABOTEUR_ID, difficulty=2,
            consequences=(SabotageConsequenceKind.ALLOCATION_LOSS,),
        )
        report = resolve_sabotage(campaign, attempt, rng=succeed(), turn=3, roster=ROSTER)
        self.assertEqual(report.released_units, 2)
        self.assertEqual(campaign.capacities[FACTION_ID].allocated("p-a"), 0)
        plan = plan_allocations(campaign, FACTION_ID, (("p-a", 3),))
        self.assertEqual(plan.granted("p-a"), 3)

    def test_a_closed_programme_cannot_be_sabotaged(self) -> None:
        finished = mk_project("p-a", work=2)
        finished.clock.add(2)
        campaign, _ = build(finished)
        with self.assertRaises(OperationError):
            resolve_sabotage(campaign, self._attempt(), rng=style(), turn=3, roster=ROSTER)

    def test_a_saboteur_without_a_sheet_is_refused_before_any_dice(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        attempt = SabotageAttempt(
            attempt_id="s-1", project_id="p-a", saboteur_id="ghost", difficulty=2
        )
        rng = style()
        with self.assertRaises(OperationError):
            resolve_sabotage(campaign, attempt, rng=rng, turn=3, roster=ROSTER)
        self.assertEqual(rng.draws, 0)

    def test_the_projects_own_lead_cannot_be_its_saboteur(self) -> None:
        campaign, _ = build(mk_project("p-a", lead="a-1"))
        attempt = SabotageAttempt(
            attempt_id="s-1", project_id="p-a", saboteur_id="a-1", difficulty=2
        )
        with self.assertRaises(OperationError):
            resolve_sabotage(campaign, attempt, rng=style(), turn=3, roster=ROSTER)

    def test_a_replayed_attempt_applies_nothing_twice(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        campaign.projects["p-a"].clock.add(3)
        first = resolve_sabotage(campaign, self._attempt(), rng=succeed(), turn=3, roster=ROSTER)
        second = resolve_sabotage(campaign, self._attempt(), rng=style(), turn=4, roster=ROSTER)
        self.assertTrue(first.applied)
        self.assertEqual(second.applied, ())
        self.assertIn("already resolved", second.notes[0])
        self.assertEqual(campaign.projects["p-a"].clock.work_required, 6 + 1)
        self.assertEqual(len(campaign.sabotages), 1)

    def test_the_attempt_is_recorded_on_the_project_and_in_the_audit_trail(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        campaign.projects["p-a"].clock.add(1)
        report = resolve_sabotage(campaign, self._attempt(), rng=succeed(), turn=3, roster=ROSTER)
        self.assertEqual(campaign.projects["p-a"].detail["sabotage_attempts"], ["s-1"])
        note = campaign.campaign_notes[-1]
        self.assertEqual(note["kind"], "sabotage")
        self.assertEqual(note["provenance"]["source"], "strategy_game.operations.resolve_sabotage")
        self.assertEqual(note["filled_before"], note["filled_after"])
        self.assertEqual(campaign.sabotages["s-1"].to_dict(), report.to_dict())

    def test_the_report_refuses_to_describe_lost_progress(self) -> None:
        with self.assertRaises(OperationError):
            SabotageReport(
                attempt_id="s-bad",
                project_id="p-a",
                faction_id=FACTION_ID,
                turn=1,
                saboteur_id=SABOTEUR_ID,
                outcome=Outcome.SUCCESS,
                filled_before=4,
                filled_after=2,
                work_required_before=6,
                work_required_after=6,
            )

    def test_the_report_refuses_a_shorter_road(self) -> None:
        with self.assertRaises(OperationError):
            SabotageReport(
                attempt_id="s-bad",
                project_id="p-a",
                faction_id=FACTION_ID,
                turn=1,
                saboteur_id=SABOTEUR_ID,
                outcome=Outcome.SUCCESS,
                work_required_before=6,
                work_required_after=4,
            )

    def test_a_sabotage_attempt_needs_a_menu(self) -> None:
        with self.assertRaises(OperationError):
            SabotageAttempt(
                attempt_id="s-1", project_id="p-a", saboteur_id=SABOTEUR_ID, difficulty=2,
                consequences=(),
            )

    def test_a_sabotage_attempt_refuses_a_repeated_consequence(self) -> None:
        with self.assertRaises(OperationError):
            SabotageAttempt(
                attempt_id="s-1", project_id="p-a", saboteur_id=SABOTEUR_ID, difficulty=2,
                consequences=("setback", "setback"),
            )

    def test_the_report_survives_the_save_round_trip(self) -> None:
        campaign, _ = build(mk_project("p-a"))
        campaign.projects["p-a"].clock.add(2)
        resolve_sabotage(campaign, self._attempt(("setback", "complication")), rng=style(),
                         turn=3, roster=ROSTER)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "campaign.json"
            save_campaign(campaign, path)
            loaded = load_campaign(path)
        self.assertEqual(loaded.to_json(), campaign.to_json())
        self.assertEqual(loaded.sabotages["s-1"].applied,
                         (SabotageConsequenceKind.SETBACK, SabotageConsequenceKind.COMPLICATION))


class LoopTest(unittest.TestCase):
    """Research opens a mission; a mission feeds research. Both directions are read-only."""

    def _research_project(self, **kwargs) -> ResearchProject:
        return ResearchProject(
            project_id=kwargs.pop("project_id", "p-research"),
            faction_id=FACTION_ID,
            title="Reverse-engineer the recovered component",
            kind="reverse_engineering",
            lead_id=kwargs.pop("lead", "a-1"),
            lead_skill=RESEARCH_LEAD_SKILL,
            lead_difficulty=1,
            clock=ProjectClock(kwargs.pop("work", 2)),
            resource_kind=RESEARCH_RESOURCE_KIND,
            stage=kwargs.pop("stage", ProjectStage.UNDERSTANDING),
            requires=kwargs.pop("requires", Prerequisites()),
            node_id=kwargs.pop("node_id", NODE_WITH_OPTION),
        )

    def _run_to_completion(self, campaign: Campaign, project_id: str) -> None:
        ledger = TurnLedger(default_seats(LEADER_ID, AGENT_IDS))
        for _ in range(6):
            if campaign.projects[project_id].clock.is_complete:
                return
            ledger.next_turn()
            run_faction_turn(
                campaign,
                turn=ledger.turn,
                ledger=ledger,
                rng=style(),
                roster=ROSTER,
                order=(project_id,),
                demands=((project_id, 2),),
            )
        raise AssertionError(f"{project_id} did not complete")

    def test_research_opens_a_mission_only_after_the_programme_completes(self) -> None:
        campaign, _ = build(self._research_project())
        self.assertEqual(available_missions(campaign), ())
        self._run_to_completion(campaign, "p-research")
        complete_research(campaign, "p-research", declared_nodes()[NODE_WITH_OPTION], turn=2)
        missions = available_missions(campaign)
        self.assertEqual([item.mission_id for item in missions], ["option:model"])
        self.assertEqual(missions[0].node_id, NODE_WITH_OPTION)
        self.assertEqual(missions[0].stage, ProjectStage.UNDERSTANDING)

    def test_a_capability_without_an_option_opens_no_mission(self) -> None:
        campaign, _ = build(self._research_project(node_id=NODE_WITHOUT_OPTION))
        self._run_to_completion(campaign, "p-research")
        complete_research(campaign, "p-research", declared_nodes()[NODE_WITHOUT_OPTION], turn=2)
        self.assertEqual(available_missions(campaign), ())
        self.assertIn(NODE_WITHOUT_OPTION, campaign.capabilities)

    def _mission(self, *, resources=("data:telemetry",)) -> MissionOutcome:
        return MissionOutcome(
            mission_id="option:model",
            case_id=CASE_ID,
            outcome=Outcome.SUCCESS,
            leader_id=LEADER_ID,
            resources_gained=tuple(resources),
            agent_ids=("a-1",),
        )

    def test_a_mission_makes_a_project_startable(self) -> None:
        second = mk_project(
            "p-second",
            work=2,
            requires=Prerequisites(resource_ids=("data:telemetry",), node_ids=(NODE_WITH_OPTION,)),
        )
        campaign, _ = build(second)
        report = self._mission()
        before = {item.project_id: item for item in project_inputs(campaign, report)}
        self.assertFalse(before["p-second"].ready)
        self.assertIn("data:telemetry", before["p-second"].missing)

        apply_mission_outcome(campaign, report)
        after = {item.project_id: item for item in project_inputs(campaign, report)}
        self.assertFalse(after["p-second"].ready)  # the node is still missing
        self.assertEqual(after["p-second"].satisfied_by_report, ("data:telemetry",))

    def test_project_inputs_writes_nothing(self) -> None:
        campaign, _ = build(mk_project("p-a", requires=Prerequisites(resource_ids=("data:x",))))
        before = campaign.to_json()
        project_inputs(campaign, self._mission(resources=("data:x",)))
        self.assertEqual(campaign.to_json(), before)

    def test_the_loop_closes_from_mission_to_research_to_mission(self) -> None:
        first = self._research_project(project_id="p-first")
        second = self._research_project(
            project_id="p-second",
            stage=ProjectStage.MANUFACTURE,
            node_id=NODE_SECOND,
            requires=Prerequisites(resource_ids=("data:telemetry",), node_ids=(NODE_WITH_OPTION,)),
        )
        campaign, _ = build(first, second)

        # mission → research: the salvage hands over the specimen
        salvage = MissionOutcome(
            mission_id="mission-salvage",
            case_id=CASE_ID,
            outcome=Outcome.SUCCESS,
            leader_id=LEADER_ID,
            resources_gained=("artefact:component",),
            agent_ids=("a-4",),
        )
        apply_mission_outcome(campaign, salvage)
        first.requires = Prerequisites(resource_ids=("artefact:component",))
        self.assertTrue(
            {item.project_id: item for item in project_inputs(campaign, salvage)}["p-first"].ready
        )

        # research → mission: the understanding opens an option
        self._run_to_completion(campaign, "p-first")
        complete_research(campaign, "p-first", declared_nodes()[NODE_WITH_OPTION], turn=2)
        opened = [item.mission_id for item in available_missions(campaign)]
        self.assertEqual(opened, ["option:model"])

        # mission → research: playing the opened mission feeds the second programme
        field_trial = self._mission()
        apply_mission_outcome(campaign, field_trial)
        inputs = {item.project_id: item for item in project_inputs(campaign, field_trial)}
        self.assertTrue(inputs["p-second"].ready)
        self.assertEqual(inputs["p-second"].satisfied_by_report, ("data:telemetry",))

        self._run_to_completion(campaign, "p-second")
        completion = complete_research(
            campaign, "p-second", declared_nodes()[NODE_SECOND], turn=4
        )
        self.assertEqual(completion.stage, ProjectStage.MANUFACTURE)
        self.assertEqual(
            sorted(item.mission_id for item in available_missions(campaign)),
            ["option:manufacture", "option:model"],
        )

    def test_an_unapplied_mission_report_leaves_the_project_unready(self) -> None:
        project = mk_project("p-a", requires=Prerequisites(resource_ids=("data:telemetry",)))
        campaign, _ = build(project)
        inputs = project_inputs(campaign, self._mission())
        self.assertFalse(inputs[0].ready)
        self.assertIn("added nothing it holds", inputs[0].note)
        self.assertIsInstance(inputs[0], ProjectInput)


class SliceTest(unittest.TestCase):
    """The headless demo, pinned: it must report the run this repository documents."""

    def test_the_slice_reproduces_the_documented_run(self) -> None:
        from strategy_game.operations_slice import DEMO_SEED, run_demo

        report = run_demo(seed=DEMO_SEED)
        self.assertEqual(report["sabotage"]["outcome"], "success_with_style")
        self.assertEqual(report["sabotage"]["applied"], ["setback", "complication"])
        self.assertEqual(report["sabotage"]["filled_before"], 3)
        self.assertEqual(report["sabotage"]["filled_after"], 3)
        self.assertEqual(report["sabotage"]["work_required_before"], 12)
        self.assertEqual(report["sabotage"]["work_required_after"], 13)
        self.assertEqual(report["capacity_before"][RESEARCH_RESOURCE_KIND], 4)
        self.assertEqual(report["capacity_after"][RESEARCH_RESOURCE_KIND], 5)
        self.assertEqual(report["capacity_after"][PERSONNEL_RESOURCE_KIND], 4)
        self.assertEqual(report["loop"]["turns"], 7)
        self.assertEqual(report["loop"]["research_opened"], ["option:nhi-propulsion-model"])
        self.assertEqual(report["loop"]["research_fed"], ["project-telemetry-review"])
        self.assertEqual(
            report["loop"]["research_completed"], "propulsion-component-manufacture"
        )
        self.assertEqual(
            [item["mission_id"] for item in report["missions"]["after_manufacture"]],
            ["option:nhi-propulsion-model", "option:propulsion-manufacture-programme"],
        )
        self.assertEqual(report["clocks"]["project-nhi-propulsion"],
                         {"work_required": 13, "filled": 13})
        self.assertEqual(report["save"]["reload_identical"], True)

    def test_the_slice_s_first_turn_shows_a_busy_lead_and_a_shortage(self) -> None:
        from strategy_game.operations_slice import DEMO_SEED, run_demo

        turn = run_demo(seed=DEMO_SEED)["first_turn"]
        self.assertEqual(turn["projects"]["project-lab-outreach"]["kind"], "busy")
        self.assertFalse(turn["projects"]["project-lab-outreach"]["action_taken"])
        self.assertEqual(turn["actions_used"], 3)
        grants = {item["project_id"]: item["units"] for item in turn["allocations"]["grants"]}
        self.assertEqual(grants["project-field-protocol"], 1)
        self.assertEqual(turn["allocations"]["unmet"],
                         [{"resource_kind": RESEARCH_RESOURCE_KIND, "units": 3}])

    def test_the_slice_reports_no_structural_problems(self) -> None:
        from strategy_game.operations_slice import DEMO_SEED, run_demo

        self.assertEqual(run_demo(seed=DEMO_SEED)["structural_problems"], [])


if __name__ == "__main__":
    unittest.main()
