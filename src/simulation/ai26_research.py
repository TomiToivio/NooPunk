"""AI26-inspired *synthetic* social science experiment (NoöPunk #1286).

Uses the existing event envelope and reducer. No RPG rules, fictional canon,
LLM agent decisions or empirical inference enter this module.

The communication process below is a deliberately simple, inspectable null
model, NOT a causal operationalisation of Laclau/Palonen's discourse theory.
See docs/research/AI26_SIMULATOR.md before interpreting the output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from .events import Event, next_occurrence
from .provenance import Origin, Provenance
from .world_state import reduce_events, replay_digest

_KINDS = {"individual", "organization"}
_START = datetime(2026, 1, 1, tzinfo=timezone.utc)


@dataclass(frozen=True, slots=True)
class ResearchActor:
    """An explicitly synthetic individual or organization, never an RPG character."""

    actor_id: str
    kind: str
    affiliation: str = ""
    #: Where this actor came from. A simulated population is `synthesized` (invented) or, at most, `inferred` (derived
    #: from analysis). It is never `observed`: an actor is not a corpus record, and allowing the label would let a
    #: synthetic stand-in be exported as if it were a person in the data (#1286 acceptance conditions).
    origin: Origin = Origin.SYNTHESIZED

    def __post_init__(self) -> None:
        if not self.actor_id.startswith("synthetic:"):
            raise ValueError("research actors must have a synthetic: id")
        if self.kind not in _KINDS:
            raise ValueError("kind must be individual or organization")
        if self.origin not in (Origin.SYNTHESIZED, Origin.INFERRED):
            raise ValueError(f"a research actor is synthesized or inferred, not {self.origin.value!r}")
        if self.affiliation and self.kind != "individual":
            raise ValueError("only individuals may have organization affiliations")


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _validate_roster(roster: tuple[ResearchActor, ...]) -> None:
    ids = [actor.actor_id for actor in roster]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate actor IDs")
    kinds = {a.actor_id: a.kind for a in roster}
    for actor in roster:
        if actor.affiliation and kinds.get(actor.affiliation) != "organization":
            raise ValueError(f"unknown organization affiliation: {actor.affiliation}")


def _make_event(
    existing: list[Event], *, run_id: str, turn: int, actor: str,
    action: str, target: str, content: str = "",
) -> Event:
    # Absolute timestamps are derived from turn, not wall-clock time.
    return Event.create(
        simulation_id=run_id, turn=turn, actor=actor, target=target,
        action_type=action, content=content, source="system", synthetic=True,
        timestamp=(_START + timedelta(minutes=turn)).isoformat(),
        visibility="public",
        occurrence=next_occurrence(existing, simulation_id=run_id, turn=turn),
    )


def simulate(
    roster: Iterable[ResearchActor], *, seed: int = 0, turns: int = 12,
) -> dict:
    """Run a seeded random-encounter null model with one message per turn.

    Messages are neutral synthetic tokens, NOT inferred discourse articulations.
    Affiliations are declared structural ties; no persuasion, network power or
    semantic interpretation is assumed. The full event list is replayable.
    """
    if turns < 0:
        raise ValueError("turns must be nonnegative")
    actors = tuple(sorted(roster, key=lambda a: a.actor_id))
    _validate_roster(actors)
    config = {"actors": [
        {"actor_id": a.actor_id, "kind": a.kind, "affiliation": a.affiliation, "origin": a.origin.value}
        for a in actors
    ], "seed": seed, "turns": turns, "model": "random-encounter-null-v1"}
    run_id = "ai26-synthetic:" + hashlib.sha256(
        _canonical_json(config).encode("utf-8")
    ).hexdigest()[:20]
    events: list[Event] = []
    for actor in actors:
        if actor.affiliation:
            events.append(_make_event(
                events, run_id=run_id, turn=0,
                actor=actor.actor_id, action="relate",
                target=actor.affiliation,
            ))

    rng = random.Random(seed)
    individuals = [a.actor_id for a in actors if a.kind == "individual"]
    if len(individuals) >= 2:
        for turn in range(1, turns + 1):
            speaker, listener = rng.sample(individuals, 2)
            events.append(_make_event(
                events, run_id=run_id, turn=turn, actor=speaker,
                action="communicate", target=listener,
                content=f"synthetic-neutral-message-{turn:04d}",
            ))

    # Do not silently drop actors who never communicated.
    actor_ids = {a.actor_id for a in actors}
    social = [
        {"source": e.actor, "target": e.target, "relation": "affiliated_with", "turn": e.turn}
        for e in events if e.action_type == "relate"
    ]
    communication = [
        {"source": e.actor, "target": e.target, "relation": "communicated_to", "turn": e.turn,
         "event_id": e.event_id}
        for e in events if e.action_type == "communicate"
    ]
    for edge in social + communication:
        if edge["source"] not in actor_ids or edge["target"] not in actor_ids:
            raise ValueError("dangling graph edge")
    state = reduce_events(events, simulation_id=run_id)
    result = {
        "schema": "ai26-synthetic-experiment-v2",
        "provenance": Provenance(
            Origin.SIMULATED,
            source=run_id,
            method="random-encounter-null-v1",
            uncertainty="seeded null model; no empirical calibration",
        ).to_dict(),
        "origins": {
            origin.value: sum(1 for actor in actors if actor.origin is origin)
            for origin in (Origin.OBSERVED, Origin.INFERRED, Origin.SYNTHESIZED, Origin.SIMULATED)
        },
        "scientific_status": "hypothetical_null_model_not_empirical_finding",
        "run_id": run_id,
        "configuration": config,
        "events": [e.to_dict() for e in events],
        "graphs": {
            "nodes": config["actors"], "social_edges": social,
            "communication_edges": communication,
        },
        "summary": {
            "actors": len(actors), "events": state.event_count,
            "communication_events": len(communication),
            "social_edges": len(social),
            "isolated_actors": sorted(actor_ids - {
                edge[k] for edge in social + communication for k in ("source", "target")
            }),
            "replay_digest": replay_digest(events) if events else "",
        },
    }
    return result


def verify_replay(payload: dict) -> bool:
    """Check event roundtrip, deterministic IDs and reducer digest."""
    events = [Event.from_dict(raw) for raw in payload["events"]]
    if any(Event.create(
        simulation_id=e.simulation_id, turn=e.turn, actor=e.actor,
        action_type=e.action_type, source=e.source, synthetic=e.synthetic,
        timestamp=e.timestamp, target=e.target, content=e.content,
        location=e.location, visibility=e.visibility, occurrence=e.occurrence,
    ).event_id != e.event_id for e in events):
        return False
    digest = replay_digest(events) if events else ""
    return digest == payload["summary"]["replay_digest"]


def demo_roster(population: int = 20) -> tuple[ResearchActor, ...]:
    """Synthetic, anonymous test population and two fictional organizations."""
    if population < 0:
        raise ValueError("population must be nonnegative")
    orgs = (
        ResearchActor("synthetic:organization-a", "organization"),
        ResearchActor("synthetic:organization-b", "organization"),
    )
    individuals = tuple(
        ResearchActor(
            f"synthetic:person-{n:04d}", "individual",
            orgs[n % 2].actor_id,
        ) for n in range(population)
    )
    return orgs + individuals


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synthetic AI26 research null-model simulation")
    parser.add_argument("--population", type=int, default=20)
    parser.add_argument("--turns", type=int, default=12)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    result = simulate(demo_roster(args.population), seed=args.seed, turns=args.turns)
    if not verify_replay(result):
        raise RuntimeError("simulation replay verification failed")
    encoded = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
        print(f"Wrote synthetic simulation: {args.output}")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
