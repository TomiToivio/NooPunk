"""Issue #506 Phase 2, headless slice: concurrent projects, a shortage, sabotage, and the loop.

**Noncanonical.** Nothing here is approved content: the faction, the projects, the opposition, the
node ids, the difficulty numbers and every rating are fixtures written to exercise the Phase-2 engine
in ``strategy_game.operations``, in the same spirit as ``research_slice.py``, ``rpg/fate.demo_*`` and
``global_slice.py``. The dice are seeded, so the run replays exactly.

What the run shows, in order
----------------------------

1. **Four projects in one turn on one capacity pool.** One faction turn runs the artefact programme,
   the field-protocol programme, the civic index and a laboratory outreach — each with its own lead,
   its own allocation and its own clock. :func:`strategy_game.operations.plan_allocations` hands out
   the faction's four ``research`` units in the declared priority order, so the field protocol gets
   **one** of the three it asked for, and the outreach gets a lead who has already acted: the report
   says both, in words.
2. **A lead cannot act twice.** The outreach and the artefact programme share the lead ``a-1``. The
   outreach is reported ``busy`` — not silently skipped, and not advanced with a second action.
3. **Opposition sabotage, and nothing lost.** An operative of the Bureau of Continuity attempts to
   disrupt the artefact programme. The check goes through the one Fate kernel; the consequence lands
   on the **clock's total work**, so the segments already completed stay completed. The report carries
   ``filled_before == filled_after`` and the extra work the programme now needs.
4. **An injured lead, and the remedies a shortage really has.** ``a-3`` is taken out (every physical
   stress box ticked), so the field protocol cannot run. The report names the state, lists the
   remedies with their consequences — reassign, upgrade, recruit, pause — and the faction then takes
   **three** of them explicitly: the field protocol goes to ``a-4`` (a real reassignment, the clock
   and its completed segments moving with it), ``research`` capacity is raised by one unit for the
   instrumentation grant (which covers the field protocol's two-unit shortfall), and ``personnel``
   capacity is raised by one unit for the staffing appropriation. A fourth decision, pausing the
   laboratory outreach, shows the remedy that costs nothing and stops a clock.
5. **The loop closes.** The artefact programme completes, granting **scientific understanding** — a
   capability, and with it a mission option the RPG layer did not have before. That mission is played
   out through :func:`strategy_game.campaign.missions.apply_mission_outcome`, and the telemetry it
   brings home satisfies the prerequisite of a second research programme, which then completes into
   **reproducible manufacture** — a different stage, whose own mission option is now open.

Run:
    python -m strategy_game.operations_slice
    python -m strategy_game.operations_slice --seed 7 --save /tmp/noopunk-operations.json
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from random import Random
from typing import Any

from .campaign import (
    Campaign,
    CampaignFaction,
    Case,
    MissionOutcome,
    apply_mission_outcome,
    load_campaign,
    save_campaign,
)
from .characters import Tag
from .operations import (
    TUNING_CAPACITY_INVESTMENT_CEILING_SEATS,
    TUNING_CAPACITY_INVESTMENT_UNITS,
    TUNING_SABOTAGE_SETBACK_SEGMENTS,
    CapacityInvestment,
    FactionTurnReport,
    InvestmentKind,
    SabotageAttempt,
    SabotageConsequenceKind,
    apply_investment,
    available_missions,
    personnel_availability,
    project_inputs,
    project_personnel,
    remedies_for,
    resolve_sabotage,
    run_faction_turn,
)
from .projects import (
    FactionCapacity,
    Prerequisites,
    ProjectClock,
    ProjectStage,
    StrategicProject,
    clock_for_difficulty,
    pause_project,
    reassign_project,
    resume_project,
)
from .research import (
    RESEARCH_LEAD_SKILL,
    RESEARCH_RESOURCE_KIND,
    ResearchProject,
    ResearchYield,
    TechNode,
    complete_research,
)
from .rpg.fate import Character, Outcome
from .rpg.roster import TurnLedger, default_seats
from .strategic_skills import load_strategic_roster

#: The seed the documented run reproduces. Chosen so the Bureau's operative **succeeds with style**
#: at the disruption — the slice has to show a sabotage that lands, and the Fate ladder's top step
#: landing two consequences of the declared menu is the interesting case — and so every programme
#: still finishes inside the turn cap. ``test_operations_slice`` pins the run line by line.
DEMO_SEED = 6

SLICE_SCHEMA = "noopunk.strategy_game.operations_slice"

#: A cap on the run, so a seed that made every check fail would report rather than hang.
MAX_TURNS = 40

# -- fixture ids -------------------------------------------------------------------------------

FACTION_ID = "city-directorate"
LEADER_ID = "l-1"
AGENT_IDS = ("a-1", "a-2", "a-3", "a-4")
OPPOSITION_ID = "bureau-of-continuity"
SABOTEUR_ID = "x-1"
CASE_ID = "helsinki-hull-2045"

ARTEFACT_ID = "artefact:nhi-propulsion-component"
LAB_ID = "facility:helsinki-field-lab"
ARCHIVE_ID = "archive:ruoholahti-civic-archive"
TELEMETRY_ID = "data:propulsion-telemetry"
FUNDING_HIRE = "funding:staff-appropriation"
FUNDING_LAB = "funding:instrumentation-grant"

PROJECT_ARTEFACT = "project-nhi-propulsion"
PROJECT_FIELD = "project-field-protocol"
PROJECT_CIVIC = "project-civic-index"
PROJECT_OUTREACH = "project-lab-outreach"
PROJECT_TELEMETRY = "project-telemetry-review"

NODE_UNDERSTANDING = "nhi-propulsion-understanding"
NODE_MANUFACTURE = "propulsion-component-manufacture"
NODE_FIELD = "field-protocol-deployment"

OPTION_MODEL = "option:nhi-propulsion-model"
OPTION_MANUFACTURE = "option:propulsion-manufacture-programme"
OPTION_FIELD = "option:field-protocol-trial"

CLUE_ID = "clue:propulsion-anomaly"
EQUIPMENT_ID = "equipment:propulsion-test-bench"

#: The throughput the fixture faction asks for, per project. Three is issue #506's own worked
#: example; the total deliberately exceeds the four ``research`` units the faction has.
ARTEFACT_DEMAND = 3
FIELD_DEMAND = 3
OUTREACH_DEMAND = 1
CIVIC_DEMAND = 2
TELEMETRY_DEMAND = 4

#: The fixture's starting capacity. Data, not a rule.
RESEARCH_UNITS = 4
PERSONNEL_UNITS = 3
FUNDING_UNITS = 1


def declared_nodes() -> dict[str, TechNode]:
    """The three capability nodes the slice's world declares, as author data."""
    return {
        NODE_UNDERSTANDING: TechNode(
            node_id=NODE_UNDERSTANDING,
            label="Partial understanding of the recovered propulsion component",
            stage=ProjectStage.UNDERSTANDING,
            branch="alien_derived",
            hybrid_of=("quantumpunk",),
            yields=ResearchYield(
                capability="xeno-engineering", option=OPTION_MODEL, clue=CLUE_ID,
            ),
        ),
        NODE_MANUFACTURE: TechNode(
            node_id=NODE_MANUFACTURE,
            label="Propulsion component in reproducible production",
            stage=ProjectStage.MANUFACTURE,
            branch="alien_derived",
            # Manufacture cannot arrive before the understanding it depends on: the stage is a
            # separate project, and this is the prerequisite that says so structurally.
            requires=Prerequisites(node_ids=(NODE_UNDERSTANDING,)),
            yields=ResearchYield(option=OPTION_MANUFACTURE, equipment=EQUIPMENT_ID),
        ),
        NODE_FIELD: TechNode(
            node_id=NODE_FIELD,
            label="Field protocol in deployment",
            stage=ProjectStage.DEPLOYMENT,
            branch="civic",
            yields=ResearchYield(option=OPTION_FIELD, capability="field-protocol"),
        ),
    }


def _leader_sheet() -> Character:
    return Character(
        id=LEADER_ID,
        name="Director of the City Directorate",
        aspects=["The Programme Is the Argument", "Signs the Paperwork Herself"],
        skills={"COG": 3, "INT": 2, "REF": 1, "SAV": 3, "SOM": 1, "WIL": 2},
        strategic_skills={
            RESEARCH_LEAD_SKILL: 3, "stewardship": 3, "statecraft": 2, "inquiry": 2,
            "command": 1, "security": 2, "fieldcraft": 1,
        },
        tags=(Tag("belief", "doctrine:open-science"),),
    )


def _agent_sheets() -> dict[str, Character]:
    return {
        "a-1": Character(
            id="a-1",
            name="Lead Scientist",
            aspects=["Xenopunk Instrumentalist"],
            skills={"COG": 4, "INT": 3, "REF": 1, "SAV": 1, "SOM": 1, "WIL": 2},
            strategic_skills={RESEARCH_LEAD_SKILL: 4, "inquiry": 3, "fieldcraft": 2},
            tags=(Tag("competence", "Engineering"),),
        ),
        "a-2": Character(
            id="a-2",
            name="Programme Administrator",
            aspects=["Builds Institutions, Not Monuments"],
            skills={"COG": 2, "INT": 2, "REF": 1, "SAV": 3, "SOM": 1, "WIL": 2},
            strategic_skills={"stewardship": 4, "statecraft": 3},
        ),
        "a-3": Character(
            id="a-3",
            name="Field Researcher",
            aspects=["Reproducible Or It Did Not Happen"],
            skills={"COG": 3, "INT": 2, "REF": 2, "SAV": 1, "SOM": 1, "WIL": 1},
            strategic_skills={RESEARCH_LEAD_SKILL: 3, "fieldcraft": 3},
        ),
        "a-4": Character(
            id="a-4",
            name="Counter-Intelligence Officer",
            aspects=["Nobody Reads the Room Like She Does"],
            skills={"COG": 3, "INT": 3, "REF": 2, "SAV": 2, "SOM": 2, "WIL": 3},
            strategic_skills={"security": 3, RESEARCH_LEAD_SKILL: 2, "fieldcraft": 2},
        ),
        SABOTEUR_ID: Character(
            id=SABOTEUR_ID,
            name="Bureau Operative",
            aspects=["Continuity Is a Kindness"],
            skills={"COG": 2, "INT": 3, "REF": 2, "SAV": 3, "SOM": 2, "WIL": 3},
            strategic_skills={"security": 4, "fieldcraft": 3, "inquiry": 2},
            tags=(Tag("belief", "doctrine:continuity"),),
        ),
    }


def _case() -> Case:
    return Case(
        case_id=CASE_ID,
        core_question="Who moved the recovered component out of the registry, and why now?",
        hook="A salvage claim filed in Helsinki points at a hull that should not be in the Baltic.",
        investigator=LEADER_ID,
        partner="a-4",
        initial_scene="A warehouse in Ruoholahti, before the customs team arrives.",
    )


def build_campaign() -> Campaign:
    """The slice's starting campaign: the PC leads the faction from turn one (#502's premise)."""
    sheets = {LEADER_ID: _leader_sheet(), **_agent_sheets()}
    return Campaign(
        faction_id=FACTION_ID,
        leader_id=LEADER_ID,
        sheets=sheets,
        factions={
            FACTION_ID: CampaignFaction(
                identifier=FACTION_ID,
                name="City Directorate",
                leader_id=LEADER_ID,
                member_ids=[LEADER_ID, *AGENT_IDS],
                resources=[FUNDING_HIRE, FUNDING_LAB, "budget:programme-2045"],
                reputation_labels=["known_in_helsinki"],
            ),
            # The opposition exists as a faction with one operative, so the saboteur is a character
            # with a sheet on this campaign rather than a name in a report.
            OPPOSITION_ID: CampaignFaction(
                identifier=OPPOSITION_ID,
                name="Bureau of Continuity",
                leader_id=SABOTEUR_ID,
                member_ids=[SABOTEUR_ID],
            ),
        },
        cases={CASE_ID: _case()},
        capacities={
            FACTION_ID: FactionCapacity(
                faction_id=FACTION_ID,
                units={
                    RESEARCH_RESOURCE_KIND: RESEARCH_UNITS,
                    "personnel": PERSONNEL_UNITS,
                    "funding": FUNDING_UNITS,
                },
            )
        },
        tech_nodes=declared_nodes(),
    )


# -- the four concurrent projects ----------------------------------------------------------------


def artefact_project() -> ResearchProject:
    """The alien programme: 12 segments, gated on the lead scientist's SCIENCE check."""
    return ResearchProject(
        project_id=PROJECT_ARTEFACT,
        faction_id=FACTION_ID,
        title="Reverse-engineer the recovered propulsion component",
        kind="reverse_engineering",
        lead_id="a-1",
        support_ids=("a-2",),
        lead_skill=RESEARCH_LEAD_SKILL,
        lead_difficulty=2,
        clock=clock_for_difficulty(2),
        resource_kind=RESEARCH_RESOURCE_KIND,
        stage=ProjectStage.UNDERSTANDING,
        requires=Prerequisites(resource_ids=(ARTEFACT_ID,)),
        node_id=NODE_UNDERSTANDING,
        grants_resource_ids=(LAB_ID,),
    )


def field_project() -> ResearchProject:
    """The civic programme: a different clock, another lead, the same resource pool."""
    return ResearchProject(
        project_id=PROJECT_FIELD,
        faction_id=FACTION_ID,
        title="Put the field protocol into deployment",
        kind="applied_engineering",
        lead_id="a-3",
        support_ids=("a-4",),
        lead_skill=RESEARCH_LEAD_SKILL,
        lead_difficulty=1,
        clock=clock_for_difficulty(1),
        resource_kind=RESEARCH_RESOURCE_KIND,
        stage=ProjectStage.DEPLOYMENT,
        node_id=NODE_FIELD,
    )


def civic_project() -> StrategicProject:
    """The non-research operation on the same engine: personnel, stewardship, no capability."""
    return StrategicProject(
        project_id=PROJECT_CIVIC,
        faction_id=FACTION_ID,
        title="Organise the civic evidence index",
        kind="organize",
        lead_id="a-2",
        lead_skill="stewardship",
        lead_difficulty=1,
        clock=clock_for_difficulty(1),
        resource_kind="personnel",
        stage=ProjectStage.DEPLOYMENT,
        grants_resource_ids=(ARCHIVE_ID,),
    )


def outreach_project() -> StrategicProject:
    """The fourth project, and the one whose lead is already busy: a deliberate clash."""
    return StrategicProject(
        project_id=PROJECT_OUTREACH,
        faction_id=FACTION_ID,
        title="Laboratory outreach to the harbour schools",
        kind="organize",
        lead_id="a-1",
        lead_skill="fieldcraft",
        lead_difficulty=1,
        clock=ProjectClock(4),
        resource_kind=RESEARCH_RESOURCE_KIND,
        stage=ProjectStage.ADOPTION,
    )


def telemetry_project() -> ResearchProject:
    """The programme the *second* mission makes possible: manufacture, not discovery."""
    return ResearchProject(
        project_id=PROJECT_TELEMETRY,
        faction_id=FACTION_ID,
        title="Build the propulsion component to reproducible standard",
        kind="technology_transfer",
        # The artefact programme's lead, free again once that programme is closed: a person drives
        # one programme at a time, so the second stage waits for the first to finish.
        lead_id="a-1",
        lead_skill=RESEARCH_LEAD_SKILL,
        lead_difficulty=0,
        clock=ProjectClock(8),
        resource_kind=RESEARCH_RESOURCE_KIND,
        stage=ProjectStage.MANUFACTURE,
        requires=Prerequisites(
            resource_ids=(TELEMETRY_ID,), node_ids=(NODE_UNDERSTANDING,),
        ),
        node_id=NODE_MANUFACTURE,
    )


def declare_projects(campaign: Campaign) -> None:
    """Every project the world has declared — including the one it cannot start yet."""
    for project in (
        artefact_project(), field_project(), civic_project(),
        outreach_project(), telemetry_project(),
    ):
        campaign.projects[project.project_id] = project


# -- the missions --------------------------------------------------------------------------------


def artefact_mission_outcome(*, seed: int | None = None) -> MissionOutcome:
    """The resolved case that hands the faction the artefact — the only writer that may."""
    return MissionOutcome(
        mission_id="mission-nhi-salvage",
        case_id=CASE_ID,
        outcome=Outcome.SUCCESS,
        leader_id=LEADER_ID,
        evidence_gained=("evidence:salvage-claim-signed",),
        intel_gained=("intel:salvage-broker",),
        resources_gained=(ARTEFACT_ID,),
        reputation_labels_gained=("held_the_find",),
        objectives_completed=("recover_the_component",),
        agent_ids=("a-4",),
        seed=seed,
    )


def model_mission_outcome(*, seed: int | None = None) -> MissionOutcome:
    """The mission the *understanding* opens: a field trial that brings home telemetry."""
    return MissionOutcome(
        mission_id=OPTION_MODEL,
        case_id=CASE_ID,
        outcome=Outcome.SUCCESS,
        leader_id=LEADER_ID,
        intel_gained=("intel:bureau-interest",),
        resources_gained=(TELEMETRY_ID,),
        objectives_completed=("test_the_model",),
        agent_ids=("a-1", "a-4"),
        seed=seed,
    )


# -- the run -------------------------------------------------------------------------------------


class _Runner:
    """One ledger, one capacity pool, one campaign: the turn machinery of the slice."""

    def __init__(self, campaign: Campaign, seed: int) -> None:
        self.campaign = campaign
        self.rng = Random(seed)
        self.roster = load_strategic_roster()
        self.ledger = TurnLedger(default_seats(LEADER_ID, AGENT_IDS))
        self.timeline: list[dict[str, Any]] = []
        self.reports: list[FactionTurnReport] = []

    def turn(
        self, phase: str, order: Sequence[str], demands: Sequence[tuple[str, int]]
    ) -> FactionTurnReport:
        self.ledger.next_turn()
        if self.ledger.turn > MAX_TURNS:
            raise RuntimeError(
                f"the run passed {MAX_TURNS} turns; this fixture seed makes the checks fail too "
                "often to demonstrate the clock"
            )
        report = run_faction_turn(
            self.campaign,
            turn=self.ledger.turn,
            ledger=self.ledger,
            rng=self.rng,
            roster=self.roster,
            order=order,
            demands=demands,
        )
        self.reports.append(report)
        self.timeline.append(
            {"phase": phase, "turn": self.ledger.turn, "report": report.to_dict()}
        )
        return report

    def advance_until_complete(
        self,
        phase: str,
        order: Sequence[str],
        demands: Sequence[tuple[str, int]],
        project_id: str,
    ) -> FactionTurnReport:
        """Take turns with a fixed order and demand list until ``project_id``'s clock is full."""
        for _ in range(MAX_TURNS):
            if self.campaign.projects[project_id].clock.is_complete:
                return self.reports[-1]
            report = self.turn(phase, order, demands)
            if self.campaign.projects[project_id].clock.is_complete:
                return report
        raise RuntimeError(
            f"{project_id} did not finish within {MAX_TURNS} turns; the fixture cannot demonstrate "
            "the clock with this seed"
        )


def run_demo(*, seed: int = DEMO_SEED, save_to: str | Path | None = None) -> dict[str, Any]:
    """Play the slice and return a JSON-able report of every visible outcome."""
    campaign = build_campaign()
    declare_projects(campaign)
    runner = _Runner(campaign, seed)
    ledger = campaign.capacities[FACTION_ID]
    capacity_before = dict(ledger.units)

    # 1. the mission resolves and the specimen enters the faction's books
    salvage = apply_mission_outcome(campaign, artefact_mission_outcome(seed=seed))
    runner.timeline.append(
        {
            "phase": "mission",
            "turn": 0,
            "mission_id": salvage.mission_id,
            "outcome": salvage.outcome.value,
            "resources_gained": list(salvage.resources_gained),
            "project_inputs": [item.to_dict() for item in project_inputs(campaign, salvage)],
        }
    )

    # 2. four projects in one turn, on one pool, in a declared priority order
    order = (PROJECT_ARTEFACT, PROJECT_FIELD, PROJECT_OUTREACH, PROJECT_CIVIC)
    demands = (
        (PROJECT_ARTEFACT, ARTEFACT_DEMAND),
        (PROJECT_FIELD, FIELD_DEMAND),
        (PROJECT_OUTREACH, OUTREACH_DEMAND),
        (PROJECT_CIVIC, CIVIC_DEMAND),
    )
    first = runner.turn("concurrent", order, demands)

    # 3. the Bureau attempts to disrupt the artefact programme. The attempt rolls on its own
    # generator: it is a separate party's act, so its outcome must not depend on how many project
    # checks happened to run before it.
    sabotage = resolve_sabotage(
        campaign,
        SabotageAttempt(
            attempt_id="sabotage-bureau-1",
            project_id=PROJECT_ARTEFACT,
            saboteur_id=SABOTEUR_ID,
            difficulty=2,
            consequences=(
                SabotageConsequenceKind.SETBACK,
                SabotageConsequenceKind.COMPLICATION,
                SabotageConsequenceKind.ALLOCATION_LOSS,
            ),
        ),
        rng=Random(f"{seed}:sabotage"),
        turn=runner.ledger.turn,
        roster=runner.roster,
    )
    # The complication is a pause, and a pause is resumable: the faction's next decision is to
    # resume, and the report above has already recorded that nothing was lost.
    resumed = resume_project(campaign, PROJECT_ARTEFACT)
    runner.timeline.append(
        {
            "phase": "sabotage",
            "turn": runner.ledger.turn,
            "report": sabotage.to_dict(),
            "resumed": {
                "project_id": resumed.project_id,
                "paused": resumed.paused,
                "clock": resumed.clock.to_dict(),
            },
        }
    )

    # 4. the field researcher is taken out; the faction is told, and chooses
    campaign.sheets["a-3"].physical_stress = [True, True]
    injured = runner.turn("injured_lead", order, demands)
    field_report = project_personnel(campaign, PROJECT_FIELD, ledger=runner.ledger)
    remedy_choices = remedies_for(campaign, PROJECT_FIELD, shortfall_units=2, ledger=runner.ledger)
    injured_field_turn = _turn_shape(injured)["projects"][PROJECT_FIELD]

    reassigned = reassign_project(campaign, PROJECT_FIELD, "a-4")
    recruitment = apply_investment(
        campaign,
        CapacityInvestment(
            investment_id="recruit-field-staff",
            faction_id=FACTION_ID,
            kind=InvestmentKind.RECRUITMENT,
            resource_kind="personnel",
            cost_resource_ids=(FUNDING_HIRE,),
            label="Hire two field assistants",
        ),
        turn=runner.ledger.turn,
    )
    upgrade = apply_investment(
        campaign,
        CapacityInvestment(
            investment_id="upgrade-instrument-shop",
            faction_id=FACTION_ID,
            kind=InvestmentKind.FACILITY,
            resource_kind=RESEARCH_RESOURCE_KIND,
            cost_resource_ids=(FUNDING_LAB,),
            label="Instrument shop: one more bench",
        ),
        turn=runner.ledger.turn,
    )
    paused_outreach = pause_project(
        campaign, PROJECT_OUTREACH, "no free lead while the artefact programme runs"
    )
    runner.timeline.append(
        {
            "phase": "remedies",
            "turn": runner.ledger.turn,
            "personnel": field_report.to_dict(),
            "field_turn_while_injured": injured_field_turn,
            "choices": [remedy.to_dict() for remedy in remedy_choices],
            "taken": {
                "reassign": {"project_id": reassigned.project_id, "lead_id": reassigned.lead_id},
                "recruit": recruitment.to_dict(),
                "upgrade": upgrade.to_dict(),
                "pause": {
                    "project_id": paused_outreach.project_id,
                    "reasons": list(paused_outreach.pause_reasons),
                },
            },
        }
    )

    # 5. the artefact programme finishes; the capacity raised above is what lets it
    order_after = (PROJECT_ARTEFACT, PROJECT_FIELD, PROJECT_CIVIC)
    demands_after = (
        (PROJECT_ARTEFACT, 4),
        (PROJECT_FIELD, 1),
        (PROJECT_CIVIC, CIVIC_DEMAND),
    )
    runner.advance_until_complete("artefact", order_after, demands_after, PROJECT_ARTEFACT)
    understanding = complete_research(
        campaign, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=runner.ledger.turn
    )
    ledger.release(PROJECT_ARTEFACT)
    missions_after_understanding = available_missions(campaign)

    # 6. the mission the understanding opened, played through the one writer
    model_mission = apply_mission_outcome(campaign, model_mission_outcome(seed=seed))
    telemetry_inputs = project_inputs(campaign, model_mission)
    runner.timeline.append(
        {
            "phase": "mission_opened_by_research",
            "turn": runner.ledger.turn,
            "mission_id": model_mission.mission_id,
            "resources_gained": list(model_mission.resources_gained),
            "project_inputs": [item.to_dict() for item in telemetry_inputs],
        }
    )

    # 7. the second research programme, fed by that mission, to completion
    runner.advance_until_complete(
        "telemetry",
        (PROJECT_TELEMETRY, PROJECT_FIELD, PROJECT_CIVIC),
        ((PROJECT_TELEMETRY, TELEMETRY_DEMAND), (PROJECT_FIELD, 1)),
        PROJECT_TELEMETRY,
    )
    manufacture = complete_research(
        campaign, PROJECT_TELEMETRY, declared_nodes()[NODE_MANUFACTURE], turn=runner.ledger.turn
    )
    resume_project(campaign, PROJECT_OUTREACH)

    report: dict[str, Any] = {
        "schema": SLICE_SCHEMA,
        "seed": seed,
        "faction_id": FACTION_ID,
        "leader_id": LEADER_ID,
        "noncanonical": (
            "fixtures only: every id, rating and difficulty below is demo data. The numbers the "
            "engine adds in Phase 2 are TUNING_ parameters pending row D39."
        ),
        "tuning": {
            "TUNING_CAPACITY_INVESTMENT_UNITS": TUNING_CAPACITY_INVESTMENT_UNITS,
            "TUNING_CAPACITY_INVESTMENT_CEILING_SEATS": TUNING_CAPACITY_INVESTMENT_CEILING_SEATS,
            "TUNING_SABOTAGE_SETBACK_SEGMENTS": TUNING_SABOTAGE_SETBACK_SEGMENTS,
        },
        "capacity_before": capacity_before,
        "capacity_after": dict(ledger.units),
        "timeline": runner.timeline,
        "first_turn": _turn_shape(first),
        "sabotage": sabotage.to_dict(),
        "remedies_offered": [remedy.to_dict() for remedy in remedy_choices],
        "investments": [recruitment.to_dict(), upgrade.to_dict()],
        "personnel_after": project_personnel(campaign, PROJECT_ARTEFACT).to_dict(),
        "availability_after": {
            cid: personnel_availability(campaign, cid).to_dict()
            for cid in (LEADER_ID, *AGENT_IDS)
        },
        "clocks": {
            pid: project.clock.to_dict()
            for pid, project in sorted(campaign.projects.items())
        },
        "completions": [understanding.to_dict(), manufacture.to_dict()],
        "missions": {
            "after_understanding": [item.to_dict() for item in missions_after_understanding],
            "after_manufacture": [item.to_dict() for item in available_missions(campaign)],
        },
        "loop": {
            "mission_before_research": salvage.mission_id,
            "research_opened": [item.mission_id for item in missions_after_understanding],
            "mission_played": model_mission.mission_id,
            "research_fed": [
                item.project_id for item in telemetry_inputs if item.satisfied_by_report
            ],
            "research_completed": manufacture.node_id,
            "turns": runner.ledger.turn,
        },
        "faction_resources": list(campaign.faction().resources),
        "structural_problems": list(campaign.structural_problems()),
    }
    report["save"] = _save_and_reload(campaign, save_to)
    return report


def _turn_shape(report: FactionTurnReport) -> dict[str, Any]:
    """The first turn, in the shape a reader needs: who ran, who did not, and why."""
    return {
        "turn": report.turn,
        "actions_used": report.actions_used,
        "actions_free": report.actions_free,
        "allocations": report.allocations.to_dict() if report.allocations else None,
        "projects": {
            item.project_id: {
                "kind": item.kind.value,
                "action_taken": item.action_taken,
                "cause": item.result.cause.value if item.result is not None else None,
                "progress_added": item.result.progress_added if item.result is not None else 0,
                "clock": (
                    f"{item.result.filled}/{item.result.work_required}"
                    if item.result is not None
                    else None
                ),
                "reason": item.reason,
            }
            for item in report.turns
        },
        "notes": list(report.notes),
    }


def _save_and_reload(campaign: Campaign, path: str | Path | None) -> dict[str, Any]:
    """Write the campaign, read it back, and report whether the two serialise identically."""
    if path is None:
        with tempfile.TemporaryDirectory() as tmp:
            return _save_and_reload(campaign, Path(tmp) / "campaign.json")
    save_campaign(campaign, path)
    loaded = load_campaign(path)
    return {
        "path": str(path),
        "reload_identical": loaded.to_json() == campaign.to_json(),
        "projects": sorted(loaded.projects),
        "investments": sorted(loaded.capacity_investments),
        "sabotages": sorted(loaded.sabotages),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Issue #506 Phase 2 operations slice (noncanonical)."
    )
    parser.add_argument("--seed", type=int, default=DEMO_SEED, help="seed for the replayable dice")
    parser.add_argument("--save", default=None, help="write the campaign snapshot here")
    args = parser.parse_args(argv)
    print(json.dumps(run_demo(seed=args.seed, save_to=args.save), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
