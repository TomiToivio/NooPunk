"""Turn loop and simulation runs for the deterministic NoöPunk simulation core.

Issue #40 Phase B. This module sequences turns and owns run identity. It contains
**no rules**: an actor's decision is supplied by the caller (a human, a fixture, or
later a Concordia agent), and the engine only records what they emitted.

Fixture vocabulary is deliberately **non-canonical**. Per ``AGENTS.md`` §1/§4 the
author has not specified factions, institutions, or social mechanics, so the
constants below are marked as fixtures for tests and demos and must not be read as
setting content. The engine accepts any entity id and relation string, so nothing
here constrains the vocabulary the author eventually chooses.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Iterable, Protocol

from .events import Event, next_occurrence
from .world_state import WorldState, reduce_events

# --------------------------------------------------------------------------- #
# Non-canonical fixtures
# --------------------------------------------------------------------------- #
#: Prefix that marks synthetic entity ids in fixtures. It exists so a reader can
#: see at a glance that an id is not author-specified setting material.
FIXTURE_PREFIX = "fixture:"

#: Example relation names for tests and demos. NOT a canonical vocabulary: the
#: architecture spec records relation types as unconfirmed candidates (DEFER-2),
#: and this tuple must never be treated as the registry.
FIXTURE_RELATIONS = ("mentions", "communicates_with", "opposes", "allies_with")


def fixture_id(name: str) -> str:
    """Mark an entity id as a non-canonical fixture, e.g. ``fixture:resident-a``."""
    return f"{FIXTURE_PREFIX}{name}"


def is_fixture_id(entity_id: str) -> bool:
    return str(entity_id).startswith(FIXTURE_PREFIX)


class Actor(Protocol):
    """Anything that can decide an action for a turn.

    The engine never asks an actor for dice, numbers, or rules outcomes — only for
    an action it will record. That keeps "rules code resolves rules" true even when
    the actor is an LLM (spec §7.4).
    """

    def decide(self, *, turn: int, state: WorldState) -> Iterable[dict]:
        ...


#: A plain callable actor, for callers that do not want a class.
ActorFn = Callable[..., Iterable[dict]]


def new_simulation_id(prefix: str = "sim") -> str:
    """A fresh run id. Uniqueness is required by ``#40``; the shape is not."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Simulation:
    """A single run: its identity, its turns, and its accumulated state.

    The log is the source of truth. :attr:`state` is always the reduction of
    :attr:`events`, recomputed from them rather than mutated in place, so a failed
    turn or an out-of-order append cannot leave state and log disagreeing.
    """

    simulation_id: str = field(default_factory=new_simulation_id)
    synthetic: bool = True
    source: str = "system"
    #: Prefix carried into branch run ids, so lineage is visible in the id.
    branch_of: str = ""
    events: list[Event] = field(default_factory=list)
    turn: int = 0

    def __post_init__(self) -> None:
        # A simulation is synthetic by construction: it is a simulation.
        if self.synthetic is not True:
            raise ValueError(
                "simulation runs are synthetic by construction; a non-synthetic run "
                "would be empirical data and must not be produced by this engine"
            )

    @property
    def state(self) -> WorldState:
        return reduce_events(self.events, simulation_id=self.simulation_id)

    def emit(
        self,
        *,
        actor: str,
        action_type: str,
        target: str = "",
        content: str = "",
        location: str = "",
        visibility: str = "public",
        source: str = "",
        turn: int | None = None,
    ) -> Event:
        """Record one act and return the appended event.

        ``source`` defaults to the run's own source so the *boundary* decides
        provenance; an actor cannot claim a different view. ``synthetic`` is never
        a parameter — it is fixed by the run.
        """
        effective_turn = self.turn if turn is None else turn
        event = Event.create(
            simulation_id=self.simulation_id,
            turn=effective_turn,
            actor=actor,
            action_type=action_type,
            source=source or self.source,
            synthetic=self.synthetic,
            timestamp=utc_now(),
            target=target,
            content=content,
            location=location,
            visibility=visibility,
            occurrence=next_occurrence(
                self.events, simulation_id=self.simulation_id, turn=effective_turn
            ),
        )
        self.events.append(event)
        return event

    def run_turn(self, actors: Iterable[Actor | ActorFn]) -> list[Event]:
        """Advance one turn: each actor decides, the engine records the result.

        Actors are asked for actions, never for outcomes. An actor that yields
        nothing is fine (it abstained); the turn still advances.
        """
        emitted: list[Event] = []
        state = self.state
        for actor in actors:
            if callable(actor) and not hasattr(actor, "decide"):
                decisions = actor(turn=self.turn, state=state)
            else:
                decisions = actor.decide(turn=self.turn, state=state)  # type: ignore[union-attr]
            for decision in decisions or ():
                emitted.append(
                    self.emit(
                        actor=str(decision["actor"]),
                        action_type=str(decision["action_type"]),
                        target=str(decision.get("target", "")),
                        content=str(decision.get("content", "")),
                        location=str(decision.get("location", "")),
                        visibility=str(decision.get("visibility", "public")),
                    )
                )
        self.turn += 1
        return emitted

    def run(self, actors: Iterable[Actor | ActorFn], *, turns: int) -> None:
        for _ in range(turns):
            self.run_turn(actors)

    # -- branching ---------------------------------------------------------- #

    def branch(self, *, through_turn: int, branch_id: str = "") -> "Simulation":
        """Create a counterfactual run sharing this run's prefix.

        The branch replays the same events through ``through_turn``, so its state is
        provably identical to this run's at that point rather than a copy that could
        have drifted. A new ``simulation_id`` keeps the two runs separable in a log.
        """
        last_turn = max((event.turn for event in self.events), default=-1)
        if through_turn < 0 or through_turn > last_turn:
            raise ValueError(
                f"cannot branch at turn {through_turn}: the log covers turns "
                f"0..{last_turn}"
            )
        prefix = [event for event in self.events if event.turn <= through_turn]
        if not prefix:
            raise ValueError(f"no events at or before turn {through_turn}")
        child = Simulation(
            simulation_id=branch_id or new_simulation_id(prefix="branch"),
            synthetic=self.synthetic,
            source=self.source,
            branch_of=self.simulation_id,
        )
        for event in prefix:
            child.emit(
                actor=event.actor,
                action_type=event.action_type,
                target=event.target,
                content=event.content,
                location=event.location,
                visibility=event.visibility,
                source=event.source,
                turn=event.turn,
            )
        child.turn = through_turn + 1
        return child

    def lineage(self) -> dict[str, str]:
        return {
            "simulation_id": self.simulation_id,
            "branch_of": self.branch_of,
            "synthetic": str(self.synthetic),
        }


def replay(simulation_id: str, events: Iterable[Event]) -> WorldState:
    """Rebuild a run's state from its log alone (the reproducibility requirement)."""
    return reduce_events(events, simulation_id=simulation_id)
