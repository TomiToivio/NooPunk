"""The issue #506 Phase-1 vertical slice: two examples, three projects, one shared engine.

**Noncanonical.** Nothing here is approved content. The faction, the artefact, the laboratory, the
archive, the node ids and every rating below are fixture data written to exercise the engine, in the
same spirit as ``rpg/fate.demo_*`` and ``global_slice.py``. The dice are seeded so the run replays.

What the run shows, in order
----------------------------

1. **A mission-sourced artefact.** A resolved case — a UNSA-style investigation worksheet, reusing
   ``campaign.case`` and ``campaign.missions`` verbatim — reports the recovered propulsion component,
   and :func:`strategy_game.campaign.missions.apply_mission_outcome` records it as a held resource.
   Nothing else may hand the reverse-engineering project its specimen: that same project advanced
   *before* the mission is refused by name (see ``tests/test_research_projects.py``).
2. **The alien reverse-engineering example.** ``project-nhi-propulsion`` is a research project whose
   success gate is the lead scientist's SCIENCE check and whose work is 12 segments — issue #506's own
   worked example, where "progress becomes 3/12, then 6/12" — reached three segments a turn because
   that is what the faction commits. With :data:`DEMO_SEED` the programme's first turn is a **failed
   check**: zero segments, everything already completed preserved. Completion grants **scientific
   understanding**, one stage, never a drive plant: the faction gains a capability, an investigation
   clue and an RPG option, and no equipment.
3. **A non-research task.** ``project-archive-access`` is the organising programme (#506's "political
   organizing" family) on the *same* engine with another lead skill — ``stewardship`` — another
   resource kind, and no capability at all. Its completion grants the archive access the transfer
   programme needs, which is how a mundane project depends on an operation rather than on a discovery.
4. **The mundane technology-transfer example.** ``project-archive-terminal-transfer`` industrialises
   a technology whose principles are already known: it requires the archive, it discovers nothing, and
   its completion grants **reproducible manufacture** — a different stage of a different technology
   from the alien programme's understanding. The two programmes are deliberately not one progress bar.
5. **Save/load.** The run writes a campaign snapshot, reads it back and reports whether the reloaded
   model serialises identically.

The documented run (:data:`DEMO_SEED`) is eleven turns long, and the *only* stalled turn in it is the
one above:

============================  =====  ==================================================
turns                         cause  meaning
============================  =====  ==================================================
1                             fail   the reverse-engineering check fails; 0 of 12 segments
2–5                           pass   3, 4, 4, 1 segments: the clock fills at 12/12 on turn 5
6–8                           pass   the organising programme: 10/10 segments (stewardship)
9–11                          pass   the transfer programme: 10/10 segments (science)
============================  =====  ==================================================

Run:
    python -m strategy_game.research_slice
    python -m strategy_game.research_slice --seed 117 --save /tmp/noopunk-research.json
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
from .projects import (
    FactionCapacity,
    Prerequisites,
    ProjectResult,
    ProjectStage,
    StrategicProject,
    advance_project,
    clock_for_difficulty,
    complete_project,
)
from .research import (
    RESEARCH_LEAD_SKILL,
    RESEARCH_RESOURCE_KIND,
    ResearchProject,
    ResearchYield,
    TechNode,
    complete_research,
    rpg_options,
)
from .rpg.fate import Character, Outcome
from .rpg.roster import TurnLedger, default_seats
from .strategic_skills import load_strategic_roster

#: The seed the documented run reproduces. Chosen so that the reverse-engineering programme's first
#: turn is a **failed** check and its remaining turns succeed: the slice has to show failure and
#: stall, not only success. ``tests/test_research_projects.py`` pins the property, and
#: ``test_the_slice_reproduces_the_documented_run`` re-derives every line of the timeline below, so
#: the constant cannot drift.
DEMO_SEED = 117

SLICE_SCHEMA = "noopunk.strategy_game.research_slice"

#: A cap on the run, so a seed that made every check fail would report rather than hang.
MAX_TURNS_PER_PROGRAMME = 12

# -- fixture ids -------------------------------------------------------------------------------

FACTION_ID = "unsa-helsinki"
LEADER_ID = "l-1"
AGENT_IDS = ("a-1", "a-2", "a-3", "a-4")
CASE_ID = "helsinki-2029"

#: The mission-sourced artefact. It reaches the faction through exactly one writer, the mission
#: outcome, and it is the reverse-engineering project's only prerequisite.
ARTEFACT_ID = "artefact:nhi-propulsion-component"
#: The laboratory and the archive. Both are held-resource ids like the artefact — one book, not three.
LAB_ID = "facility:helsinki-field-lab"
ARCHIVE_ID = "archive:ruoholahti-civic-archive"

CLUE_ID = "clue:propulsion-anomaly"
OPTION_ID = "option:nhi-propulsion-model"
EQUIPMENT_ID = "equipment:field-archive-terminal"

PROJECT_ARTEFACT = "project-nhi-propulsion"
PROJECT_ARCHIVE = "project-archive-access"
PROJECT_TRANSFER = "project-archive-terminal-transfer"

#: The capability the alien programme produces: **understanding**, one stage.
NODE_UNDERSTANDING = "nhi-propulsion-understanding"
#: The capability the mundane transfer produces: **manufacture**, a different stage of a different
#: technology. Nothing in the run may collapse the two.
NODE_MANUFACTURE = "civic-archive-terminal-manufacture"

#: The belief one fixture member holds, and the doctrine the alien programme's node names. The
#: contradiction is **reported** at completion and blocks nothing (row D28).
BUTLERIAN_BELIEF = "doctrine:butlerian-retrenchment"

#: The per-turn throughput the fixture faction commits. Three, which is issue #506's own example.
RESEARCH_THROUGHPUT = 3
STAFF_THROUGHPUT = 3

#: The two capabilities the run is documented to grant, so the report can point at the sheets that
#: gained one. Fixture data, like everything else in this module.
CAPABILITY_TAGS = frozenset({"xeno-engineering", "archive-engineering"})


def declared_nodes() -> dict[str, TechNode]:
    """The two capability nodes the slice's world declares, as author data.

    Declared here rather than inside the engine, because a technology is content: the engine reads
    nodes, it does not contain them.
    """
    return {
        NODE_UNDERSTANDING: TechNode(
            node_id=NODE_UNDERSTANDING,
            label="Partial understanding of the recovered propulsion component",
            stage=ProjectStage.UNDERSTANDING,
            # A hybrid pathway in the sense issue #506 gives the word: the principles read as both
            # alien-derived and exotic-physics, and nothing derives a taxonomy from the labels.
            branch="alien_derived",
            hybrid_of=("quantumpunk",),
            # A named ideological prohibition, **reported, never enforced** (row D28): one member of
            # the faction holds the belief, and the completion says so.
            prohibited_by=(BUTLERIAN_BELIEF,),
            yields=ResearchYield(
                capability="xeno-engineering", option=OPTION_ID, clue=CLUE_ID, equipment="",
            ),
        ),
        NODE_MANUFACTURE: TechNode(
            node_id=NODE_MANUFACTURE,
            label="Civic archive terminal in reproducible production",
            stage=ProjectStage.MANUFACTURE,
            branch="cyberpunk",
            yields=ResearchYield(
                capability="archive-engineering", option="", equipment=EQUIPMENT_ID, clue="",
            ),
        ),
    }


def _leader_sheet() -> Character:
    return Character(
        id=LEADER_ID,
        name="UNSA Helsinki Director",
        aspects=["The Programme Is the Argument", "Signs the Paperwork Himself"],
        skills={"COG": 3, "INT": 2, "REF": 1, "SAV": 3, "SOM": 1, "WIL": 2},
        strategic_skills={
            RESEARCH_LEAD_SKILL: 3,
            "stewardship": 3,
            "statecraft": 2,
            "inquiry": 2,
            "command": 1,
            "security": 1,
            "fieldcraft": 0,
        },
        tags=(
            Tag("belief", "doctrine:open-science"),
            Tag("competence", "Forensics"),
        ),
        refresh=3,
        fate_points=3,
    )


def _agent_sheets() -> dict[str, Character]:
    return {
        "a-1": Character(
            id="a-1",
            name="Lead Scientist",
            aspects=["Xenopunk Instrumentalist"],
            skills={"COG": 4, "INT": 3, "REF": 1, "SAV": 1, "SOM": 1, "WIL": 2},
            strategic_skills={RESEARCH_LEAD_SKILL: 4, "inquiry": 3},
            tags=(
                Tag("competence", "Parapsychology"),
                Tag("competence", "Engineering"),
            ),
        ),
        "a-2": Character(
            id="a-2",
            name="Programme Administrator",
            aspects=["Builds Institutions, Not Monuments"],
            skills={"COG": 2, "INT": 2, "REF": 1, "SAV": 3, "SOM": 1, "WIL": 2},
            strategic_skills={"stewardship": 4, "statecraft": 3},
            tags=(Tag("competence", "Logistics"),),
        ),
        "a-3": Character(
            id="a-3",
            name="Archive Engineer",
            aspects=["Reproducible Or It Did Not Happen"],
            skills={"COG": 3, "INT": 2, "REF": 2, "SAV": 1, "SOM": 1, "WIL": 1},
            strategic_skills={RESEARCH_LEAD_SKILL: 3, "stewardship": 2},
            tags=(
                Tag("competence", "Engineering"),
                Tag("belief", BUTLERIAN_BELIEF),
            ),
        ),
        "a-4": Character(
            id="a-4",
            name="Counter-Intelligence Officer",
            aspects=["Nobody Reads the Room Like She Does"],
            skills={"COG": 2, "INT": 3, "REF": 2, "SAV": 2, "SOM": 2, "WIL": 3},
            strategic_skills={"security": 3, "fieldcraft": 2},
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
        domain_leads={
            "physical": ["registry discrepancy", "salvage insurance trail"],
            "cybernetic": ["an archive terminal that answers too slowly"],
            "psychic_noospace": ["an operator who will not go back inside the hull"],
        },
        witnesses=["Salvage broker", "Port archivist"],
        evidence_ids=["evidence:salvage-claim"],
        contradictions=["The component's mass does not match the claim"],
        possible_player_choices=["Secure the component", "Trade it to a rival", "Publish the find"],
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
                name="UNSA Helsinki",
                leader_id=LEADER_ID,
                member_ids=[LEADER_ID, *AGENT_IDS],
                resources=["budget:programme-2029"],
                reputation_labels=["known_in_helsinki"],
            )
        },
        cases={CASE_ID: _case()},
        capacities={
            FACTION_ID: FactionCapacity(
                faction_id=FACTION_ID,
                units={RESEARCH_RESOURCE_KIND: 4, "personnel": 3, "funding": 1},
                commitments=[],
            )
        },
        tech_nodes=declared_nodes(),
    )


# -- the three projects --------------------------------------------------------------------------


def reverse_engineering_project() -> ResearchProject:
    """The alien example: 12 segments of work, gated on the lead scientist's SCIENCE check.

    The work total is issue #506's own worked example (12 units), and difficulty 2 is where
    :func:`strategy_game.projects.clock_for_difficulty` produces exactly that total — a coincidence of
    the tuning convention, recorded here so the arithmetic is checkable rather than asserted.
    """
    return ResearchProject(
        project_id=PROJECT_ARTEFACT,
        faction_id=FACTION_ID,
        title="Reverse-engineer the recovered propulsion component",
        kind="reverse_engineering",
        lead_id="a-1",
        lead_skill=RESEARCH_LEAD_SKILL,
        lead_difficulty=2,
        clock=clock_for_difficulty(2),
        resource_kind=RESEARCH_RESOURCE_KIND,
        stage=ProjectStage.UNDERSTANDING,
        requires=Prerequisites(resource_ids=(ARTEFACT_ID,)),
        node_id=NODE_UNDERSTANDING,
        domain_tags=("Engineering", "Parapsychology"),
        grants_resource_ids=(LAB_ID,),
    )


def archive_access_project() -> StrategicProject:
    """The **non-research** example: the same engine, another lead skill, no capability at all.

    Organising access to the municipal archive is administrative work — issue #506's "political
    organizing" family — so its lead check is ``stewardship``, its resource is personnel, and
    completing it produces no technology. It exists to show that research is one instance of the
    shared engine rather than the engine.
    """
    return StrategicProject(
        project_id=PROJECT_ARCHIVE,
        faction_id=FACTION_ID,
        title="Organise standing access to the Ruoholahti civic archive",
        kind="organize",
        lead_id="a-2",
        lead_skill="stewardship",
        lead_difficulty=1,
        clock=clock_for_difficulty(1),
        resource_kind="personnel",
        stage=ProjectStage.DEPLOYMENT,
        grants_resource_ids=(ARCHIVE_ID,),
    )


def technology_transfer_project() -> ResearchProject:
    """The mundane example: industrialise a **known** technology. Discovery is not involved.

    "A faction might know how a jet engine works in broad outline, yet lack engineers, factories,
    supply chains or the capacity to produce one" (issue #506). So nothing here is a specimen: the
    prerequisite is the archive the organising programme won, and the stage produced is
    **manufacture** — not understanding, and not a prototype. Reaching the prototype stage of a *new*
    device would be a separate project with its own lead skills, clock and difficulty.
    """
    return ResearchProject(
        project_id=PROJECT_TRANSFER,
        faction_id=FACTION_ID,
        title="Put the civic archive terminal into reproducible production",
        kind="technology_transfer",
        lead_id="a-3",
        lead_skill=RESEARCH_LEAD_SKILL,
        lead_difficulty=1,
        clock=clock_for_difficulty(1),
        resource_kind=RESEARCH_RESOURCE_KIND,
        stage=ProjectStage.MANUFACTURE,
        requires=Prerequisites(resource_ids=(ARCHIVE_ID,)),
        node_id=NODE_MANUFACTURE,
        domain_tags=("Engineering",),
    )


def artefact_mission_outcome(*, seed: int | None = None) -> MissionOutcome:
    """The resolved case that hands the faction the artefact — the *only* way it arrives."""
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


# -- the run -------------------------------------------------------------------------------------


class _Runner:
    """The turn machinery: one ledger, one action per character per turn, one project per turn."""

    def __init__(self, campaign: Campaign, seed: int) -> None:
        self.campaign = campaign
        self.rng = Random(seed)
        self.roster = load_strategic_roster()
        self.ledger = TurnLedger(default_seats(LEADER_ID, AGENT_IDS))
        self.steps: list[dict[str, Any]] = []

    def commit(self, project_id: str, resource_kind: str, units: int) -> None:
        self.campaign.capacities[FACTION_ID].allocate(project_id, resource_kind, units)

    def release(self, project_id: str) -> int:
        """Give a finished programme's committed capacity back to the faction.

        Nothing carries over on its own: a closed programme holds no staff, and re-committing is a
        player decision this slice makes explicitly rather than a rule the ledger invents.
        """
        return self.campaign.capacities[FACTION_ID].release(project_id)

    def advance_until_complete(self, project_id: str, seat_id: str) -> list[ProjectResult]:
        """Take turns on one project until its clock is full, or the cap is reached."""
        results: list[ProjectResult] = []
        for _ in range(MAX_TURNS_PER_PROGRAMME):
            if self.campaign.projects[project_id].clock.is_complete:
                return results
            turn = self.ledger.next_turn()
            self.ledger.declare(seat_id, statement=project_id)
            result = advance_project(
                self.campaign, project_id, rng=self.rng, turn=turn, roster=self.roster
            )
            results.append(result)
            payload = result.to_dict()
            payload["step"] = "project_turn"
            self.steps.append(payload)
        raise RuntimeError(
            f"{project_id} did not finish within {MAX_TURNS_PER_PROGRAMME} turns; the fixture seed "
            "makes its checks fail too often to demonstrate the clock"
        )


def run_demo(*, seed: int = DEMO_SEED, save_to: str | Path | None = None) -> dict[str, Any]:
    """Play the slice and return a JSON-able report of every visible outcome.

    One project is advanced per turn on one ledger: ``rpg.roster.TurnLedger`` holds the crossover's
    one-action-per-character rule, so the lead who runs a project this turn *is* the opportunity cost
    of a stalled round — the engine invents no second price for failure.
    """
    campaign = build_campaign()
    runner = _Runner(campaign, seed)

    # 1. the mission resolves and the specimen enters the faction's books
    mission = apply_mission_outcome(campaign, artefact_mission_outcome(seed=seed))
    runner.steps.append(
        {
            "turn": 0,
            "step": "mission_outcome",
            "mission_id": mission.mission_id,
            "case_id": mission.case_id,
            "outcome": mission.outcome.value,
            "resources_gained": list(mission.resources_gained),
            "note": "the only writer that may hand the faction the artefact",
        }
    )

    # 2. the alien reverse-engineering programme, to completion
    campaign.projects[PROJECT_ARTEFACT] = reverse_engineering_project()
    runner.commit(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, RESEARCH_THROUGHPUT)
    artefact_turns = runner.advance_until_complete(PROJECT_ARTEFACT, "agent_1")
    understanding = complete_research(
        campaign, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=runner.ledger.turn
    )
    runner.release(PROJECT_ARTEFACT)

    # 3. the non-research organising programme, to completion
    campaign.projects[PROJECT_ARCHIVE] = archive_access_project()
    runner.commit(PROJECT_ARCHIVE, "personnel", STAFF_THROUGHPUT)
    archive_turns = runner.advance_until_complete(PROJECT_ARCHIVE, "agent_2")
    access = complete_project(campaign, PROJECT_ARCHIVE, turn=runner.ledger.turn)
    runner.release(PROJECT_ARCHIVE)

    # 4. the mundane transfer, whose only prerequisite is what the organising programme won
    campaign.projects[PROJECT_TRANSFER] = technology_transfer_project()
    runner.commit(PROJECT_TRANSFER, RESEARCH_RESOURCE_KIND, RESEARCH_THROUGHPUT)
    transfer_turns = runner.advance_until_complete(PROJECT_TRANSFER, "agent_3")
    manufacture = complete_research(
        campaign, PROJECT_TRANSFER, declared_nodes()[NODE_MANUFACTURE],
        turn=runner.ledger.turn, case_id=CASE_ID,
    )

    report: dict[str, Any] = {
        "schema": SLICE_SCHEMA,
        "seed": seed,
        "faction_id": FACTION_ID,
        "leader_id": LEADER_ID,
        "lead_check": {
            "skill": RESEARCH_LEAD_SKILL,
            "layer": "faction_agent (ActionContext.FACTION_AGENT)",
            "roster_status": "PROPOSAL - the strategic roster is not approved (#482, row D22)",
        },
        "steps": runner.steps,
        "programmes": {
            PROJECT_ARTEFACT: _programme(artefact_turns),
            PROJECT_ARCHIVE: _programme(archive_turns),
            PROJECT_TRANSFER: _programme(transfer_turns),
        },
        "completions": [understanding.to_dict(), manufacture.to_dict()],
        "generic_completion": access.to_dict(),
        "rpg_options": [option.to_dict() for option in rpg_options(campaign)],
        "held_capabilities": sorted(campaign.capabilities),
        "stages_kept_separate": {
            NODE_UNDERSTANDING: ProjectStage.UNDERSTANDING.value,
            NODE_MANUFACTURE: ProjectStage.MANUFACTURE.value,
        },
        "turns": runner.ledger.turn,
        "faction_resources": list(campaign.faction().resources),
        "sheets_gear": {
            cid: list(sheet.gear) for cid, sheet in sorted(campaign.sheets.items()) if sheet.gear
        },
        "sheets_with_new_capabilities": {
            cid: sorted(tag.value for tag in sheet.tags_of_kind("competence"))
            for cid, sheet in sorted(campaign.sheets.items())
            if any(tag.value in CAPABILITY_TAGS for tag in sheet.tags_of_kind("competence"))
        },
        "structural_problems": list(campaign.structural_problems()),
    }
    report["save"] = _save_and_reload(campaign, save_to)
    return report


def _programme(results: Sequence[ProjectResult]) -> dict[str, Any]:
    """The shape of one programme's run: turns taken, stalls, and the clock it left behind."""
    last = results[-1]
    return {
        "turns": len(results),
        "stalled_turns": [r.turn for r in results if r.progress_added == 0],
        "causes": [r.cause.value for r in results],
        "clock": {"filled": last.filled, "work_required": last.work_required},
        "completed": last.completed,
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
        "capabilities": sorted(loaded.capabilities),
        "clocks": {pid: p.clock.to_dict() for pid, p in sorted(loaded.projects.items())},
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Issue #506 Phase 1 research-project slice (noncanonical)."
    )
    parser.add_argument("--seed", type=int, default=DEMO_SEED, help="seed for the replayable dice")
    parser.add_argument("--save", default=None, help="write the campaign snapshot here")
    args = parser.parse_args(argv)
    print(json.dumps(run_demo(seed=args.seed, save_to=args.save), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
