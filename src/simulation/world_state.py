"""Deterministic world-state reducer: ``state = reduce(events)``.

Issue #40 Phase B. Two properties matter more than the contents of the state:

* **State is a function of the log.** Anything not derivable by replaying events
  is not canonical, so there is deliberately no way to write state directly.
* **Reduction is deterministic.** Same events in, byte-identical state out, which
  is what makes replay, save/load and branching possible at all.

**No mechanics live here.** The reducer records *what happened and who relates to
whom*. It does not compute power, legitimacy, cohesion, influence, or any other
derived quantity, because `AGENTS.md` §4 leaves those to the author and the
architecture spec forbids storing an unspecified number — storing one *is*
inventing a mechanic.

Entity kinds and relation types are open strings validated only as non-empty, and
the reducer accepts any event ``action_type``. Freezing either into an enum would
turn the issue's proposed vocabulary into canon (spec §2.1, DEFER-1/DEFER-2).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .events import Event, order_key

#: Action types the reducer understands structurally. This is NOT a canonical
#: vocabulary — it is the small set whose *shape* the reducer must know to build
#: nodes and relations. Any other action_type is still recorded as history.
ACTION_OBSERVE = "observe"
ACTION_MENTION = "mention"
ACTION_RELATE = "relate"
ACTION_COMMUNICATE = "communicate"

#: Relation-bearing action types: they create an edge between two entities.
RELATION_ACTIONS = (ACTION_MENTION, ACTION_RELATE)

#: Action types that reference a location.
LOCATION_ACTIONS = (ACTION_OBSERVE, ACTION_COMMUNICATE, ACTION_MENTION, ACTION_RELATE)


class ReducerError(RuntimeError):
    """The reducer was asked to do something non-deterministic."""


def _text(raw: Any) -> str:
    if raw is None:
        return ""
    text = str(raw).strip()
    return "" if text.lower() in {"nan", "none", "<na>"} else text


@dataclass(slots=True)
class WorldState:
    """Accumulated state for one simulation run, built only by :func:`reduce_events`."""

    simulation_id: str = ""
    synthetic: bool = False
    last_turn: int = 0
    #: entity id -> {kind, label}. ``kind`` is open vocabulary; default "actor".
    entities: dict[str, dict[str, str]] = field(default_factory=dict)
    #: (source, relation, target) -> count. Relations are open vocabulary.
    relations: dict[tuple[str, str, str], int] = field(default_factory=dict)
    #: entity id -> times it was the actor of an event.
    activity: dict[str, int] = field(default_factory=dict)
    #: entity id -> locations it was observed at / communicated from.
    locations: dict[str, set[str]] = field(default_factory=dict)
    #: Public communications only, in canonical order (the LaclauGPT input, #40 §4).
    public_communications: list[dict[str, str]] = field(default_factory=list)
    event_count: int = 0

    def as_dict(self) -> dict[str, Any]:
        """JSON-serialisable view, with sets sorted for reproducibility.

        Sets are sorted so two runs with identical events produce identical dicts;
        an unordered set would make ``as_dict()`` differ between replays and break
        the determinism this module exists to guarantee.
        """
        return {
            "simulation_id": self.simulation_id,
            "synthetic": self.synthetic,
            "last_turn": self.last_turn,
            "event_count": self.event_count,
            "entity_count": len(self.entities),
            "entities": {
                node: dict(payload) for node, payload in sorted(self.entities.items())
            },
            "relations": [
                {"source": source, "relation": relation, "target": target, "count": count}
                for (source, relation, target), count in sorted(self.relations.items())
            ],
            "activity": dict(sorted(self.activity.items())),
            "locations": {
                node: sorted(places) for node, places in sorted(self.locations.items())
            },
            "public_communications": list(self.public_communications),
        }


def reduce_events(events: Iterable[Event], *, simulation_id: str = "") -> WorldState:
    """Replay events into state. Pure: no clock, no randomness, no I/O.

    ``simulation_id`` may be supplied to assert which run is being reduced; when
    omitted it is taken from the first event, and a later event from a different
    run is an error rather than a silent merge of two runs.
    """
    ordered = sorted(events, key=order_key)
    if not ordered:
        return WorldState(simulation_id=simulation_id)

    # Establish run identity and the synthetic flag from the first event *before*
    # the loop. Deriving `synthetic` inside the loop only when `simulation_id` was
    # unset meant that a caller supplying the id explicitly left the flag at its
    # default, and every synthetic event then tripped the mixing check below.
    first = ordered[0]
    run_id = simulation_id or first.simulation_id
    if simulation_id and first.simulation_id != simulation_id:
        raise ReducerError(
            f"refusing to reduce: asked for run {simulation_id!r} but the log starts "
            f"with events from {first.simulation_id!r}"
        )
    state = WorldState(simulation_id=run_id, synthetic=first.synthetic)

    for event in ordered:
        if event.simulation_id != state.simulation_id:
            raise ReducerError(
                f"refusing to reduce across runs: state is {state.simulation_id!r} but "
                f"event {event.event_id!r} belongs to {event.simulation_id!r}"
            )
        if event.synthetic != state.synthetic:
            raise ReducerError(
                f"run {state.simulation_id!r} mixes synthetic and non-synthetic events; "
                "that is a defect, not a mode (spec §5)"
            )

        state.event_count += 1
        state.last_turn = max(state.last_turn, event.turn)
        state.activity[event.actor] = state.activity.get(event.actor, 0) + 1
        state.entities.setdefault(event.actor, {"kind": "actor", "label": event.actor})

        if event.action_type in RELATION_ACTIONS and event.target:
            state.entities.setdefault(event.target, {"kind": "actor", "label": event.target})
            key = (event.actor, event.action_type, event.target)
            state.relations[key] = state.relations.get(key, 0) + 1

        if event.action_type in LOCATION_ACTIONS and event.location:
            state.locations.setdefault(event.actor, set()).add(event.location)

        if event.is_public_communication() and event.content:
            state.public_communications.append(
                {
                    "actor": event.actor,
                    "turn": str(event.turn),
                    "content": event.content,
                    "action_type": event.action_type,
                }
            )

    return state


def replay_digest(events: Iterable[Event]) -> str:
    """Stable digest of a reduced run, for comparing replays and branches."""
    import hashlib
    import json

    state = reduce_events(events)
    payload = json.dumps(state.as_dict(), ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def branch_prefix(events: Iterable[Event], *, through_turn: int) -> list[Event]:
    """The shared prefix of a branch: every event up to and including a turn.

    Branching is a log operation (spec §4): a branch is a new ``simulation_id``
    that reuses this prefix and then diverges, so a counterfactual starts from a
    provably identical state rather than a copied one.
    """
    return [event for event in sorted(events, key=order_key) if event.turn <= through_turn]


__all__ = [
    "ACTION_COMMUNICATE",
    "ACTION_MENTION",
    "ACTION_OBSERVE",
    "ACTION_RELATE",
    "LOCATION_ACTIONS",
    "RELATION_ACTIONS",
    "ReducerError",
    "WorldState",
    "branch_prefix",
    "reduce_events",
    "replay_digest",
]
