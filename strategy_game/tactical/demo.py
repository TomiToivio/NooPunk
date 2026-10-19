"""A headless, deterministic demonstration of the mission layer (#515's spike).

The demo is the evidence that the mission layer works without a renderer: it builds a
**non-canonical fixture campaign** (a leader, four agents with real :class:`rpg.fate.Character`
sheets, and one case), loads the packaged fixture mission, plays a short scripted mission, and
prints what the mission changed in the campaign's persistent books.

Nothing here is content for the game. The names are deliberately dull ("Fixture Agent Two") so the
fixture cannot be mistaken for a faction, a location or a character in the setting; the mission's own
document carries ``status: SPIKE_FIXTURE`` for the same reason.

    python -m strategy_game.tactical
    python -m strategy_game.tactical --json
"""
from __future__ import annotations

from typing import Any

from ..campaign.case import Case
from ..campaign.state import Campaign, CampaignFaction
from ..rpg.fate import Character
from .mission import MissionSpec, load_mission
from .session import MissionSession

__all__ = ["DEMO_SEED", "fixture_campaign", "render_text", "run_demo"]

#: Chosen so the scripted run's one check (COG 3 against difficulty 2) lands on *success with style*
#: with seed 5's dice — the demo is reproducible rather than "usually works". Any seed works for the
#: tests, which assert on state transitions rather than on this particular roll.
DEMO_SEED = 5

#: The fixture campaign's ids. Prefixed so they read as fixtures in any report.
FIXTURE_FACTION = "spike-faction"
FIXTURE_LEADER = "spike-leader"
FIXTURE_CASE = "spike-records-case"


def _sheet(identifier: str, name: str, *, cog: int, som: int) -> Character:
    return Character(
        id=identifier,
        name=name,
        aspects=["Fixture sheet", "Non-canonical"],
        skills={"COG": cog, "INT": 2, "REF": 2, "SAV": 2, "SOM": som, "WIL": 2},
    )


def fixture_campaign() -> Campaign:
    """The smallest campaign a mission can be played on: one faction, one leader, four agents, one case.

    A fresh object every call, because a mission writes onto it and the sheets inside it.
    """
    agent_ids = ("spike-agent-1", "spike-agent-2", "spike-agent-3", "spike-agent-4")
    sheets = {
        FIXTURE_LEADER: _sheet(FIXTURE_LEADER, "Fixture Leader", cog=2, som=2),
        agent_ids[0]: _sheet(agent_ids[0], "Fixture Agent One", cog=3, som=3),
        agent_ids[1]: _sheet(agent_ids[1], "Fixture Agent Two", cog=3, som=3),
        agent_ids[2]: _sheet(agent_ids[2], "Fixture Agent Three", cog=3, som=3),
        agent_ids[3]: _sheet(agent_ids[3], "Fixture Agent Four", cog=3, som=3),
    }
    return Campaign(
        faction_id=FIXTURE_FACTION,
        leader_id=FIXTURE_LEADER,
        sheets=sheets,
        factions={
            FIXTURE_FACTION: CampaignFaction(
                identifier=FIXTURE_FACTION,
                name="Fixture Faction",
                leader_id=FIXTURE_LEADER,
                member_ids=[FIXTURE_LEADER, *agent_ids],
            )
        },
        cases={
            FIXTURE_CASE: Case(
                case_id=FIXTURE_CASE,
                core_question="Fixture: what does the annex ledger record?",
                investigator=FIXTURE_LEADER,
            )
        },
    )


def _describe(step: str, result: Any) -> str:
    """One log line per request: what was asked, and what came back."""
    if getattr(result, "ok", False):
        detail = ""
        if getattr(result, "destination", None) is not None:
            detail = f" -> {result.destination} ({len(result.steps)} steps)"
        if getattr(result, "interaction_id", ""):
            detail = f" -> outcome {result.outcome.value if result.outcome else 'no check'}"
            if result.wound:
                detail += f", consequence {result.wound!r}"
        return f"ok   {step}{detail}"
    return f"refused {step}: {result.reason}"


def run_demo(mission: MissionSpec | None = None, *, seed: int = DEMO_SEED) -> dict[str, Any]:
    """Play the fixture mission headless and return everything the run changed.

    The scripted plan is deliberately small: two agents walk (one needs the annex door, the other
    stops beside the witness), two more reposition, the turn ends, and the interview and the ledger
    are resolved. That is #515's click-to-move, pathfinding, dialogue, clue and objective completion
    in one run — with no rendering and no combat.
    """
    spec = mission if mission is not None else load_mission()
    campaign = fixture_campaign()
    session = MissionSession(spec, campaign, seed=seed)
    log: list[str] = []

    session.select("agent_1")
    log.append(_describe("agent_1 move to (9,9)", session.request_move("agent_1", (9, 9))))
    session.select("agent_2")
    log.append(_describe("agent_2 move to (6,12)", session.request_move("agent_2", (6, 12))))
    session.select("agent_3")
    log.append(_describe("agent_3 move to (17,12)", session.request_move("agent_3", (17, 12))))
    session.select("agent_4")
    log.append(_describe("agent_4 move to (15,6)", session.request_move("agent_4", (15, 6))))
    log.append(f"turn {session.end_turn()} begins; every agent's action refreshed")

    session.select("agent_1")
    log.append(
        _describe(
            "agent_1 interviews the duty clerk",
            session.interact("agent_1", "interview_witness"),
        )
    )
    session.select("agent_2")
    log.append(
        _describe("agent_2 reads the annex ledger", session.interact("agent_2", "read_ledger"))
    )

    outcome: dict[str, Any] | None = None
    if session.mission_complete:
        applied = session.complete()
        outcome = applied.to_dict()

    faction = campaign.faction()
    return {
        "log": log,
        "mission": session.report(),
        "outcome": outcome,
        "persisted": {
            "objectives": list(faction.objectives),
            "intelligence_ids": list(faction.intelligence_ids),
            "reputation_labels": list(faction.reputation_labels),
            "resources": list(faction.resources),
            "case_evidence": list(campaign.cases[spec.case_id].evidence_ids),
            "campaign_notes": len(campaign.campaign_notes),
        },
    }


def render_text(result: dict[str, Any]) -> str:
    """The demo's report as reading text — deterministic, and free of any drawing instruction."""
    lines = [f"mission: {result['mission']['mission_id']} ({result['mission']['title']})"]
    lines.extend(f"  {line}" for line in result["log"])
    lines.append("")
    for agent in result["mission"]["agents"]:
        lines.append(
            f"  {agent['seat']}: {agent['character']} at {tuple(agent['position'])}"
            f"{' (acted)' if agent['acted'] else ''}"
        )
    lines.append("")
    for objective in result["mission"]["objectives"]:
        mark = "done" if objective["done"] else "open"
        lines.append(f"  objective {objective['id']}: {mark} -> {objective['label']}")
    lines.append(f"  mission complete: {result['mission']['complete']}")
    if result["outcome"] is not None:
        lines.append(f"  mission outcome: {result['outcome']['outcome']}")
        lines.append(f"  agent squad: {', '.join(result['outcome']['agent_ids'])}")
    lines.append("")
    lines.append("persisted state:")
    for name, values in result["persisted"].items():
        lines.append(f"  {name}: {values}")
    return "\n".join(lines)
