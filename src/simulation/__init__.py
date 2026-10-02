"""Deterministic simulation core for NoöPunk (issue #40, Phase B).

One shared world state derived from an append-only event log, with no rules,
mechanics, factions or setting content. Phase B of the architecture spec:
SQLite + event log, world-state reducer, replay and branches.

The canonical specification is ``docs/SIMULATION_ARCHITECTURE_SPEC.md``. Phase C+
(Concordia, LaclauGPT/PCM adapters, Godot) are later phases and depend on
decisions still recorded in that document's DEFER register.
"""
from .engine import (
    FIXTURE_PREFIX,
    FIXTURE_RELATIONS,
    Simulation,
    fixture_id,
    is_fixture_id,
    new_simulation_id,
    replay,
)
from .events import (
    BOUNDARY_OWNED_FIELDS,
    EVENT_SOURCES,
    VISIBILITIES,
    Event,
    EventValidationError,
    next_occurrence,
    order_key,
)
from .sqlite_store import (
    EventLogError,
    append,
    assert_append_only,
    connect,
    count_events,
    iter_events,
    list_events,
    list_exchanges_for_export,
    list_simulations,
)
from .world_state import (
    ACTION_COMMUNICATE,
    ACTION_MENTION,
    ACTION_OBSERVE,
    ACTION_RELATE,
    ReducerError,
    WorldState,
    branch_prefix,
    reduce_events,
    replay_digest,
)

__all__ = [
    "ACTION_COMMUNICATE",
    "ACTION_MENTION",
    "ACTION_OBSERVE",
    "ACTION_RELATE",
    "BOUNDARY_OWNED_FIELDS",
    "EVENT_SOURCES",
    "FIXTURE_PREFIX",
    "FIXTURE_RELATIONS",
    "VISIBILITIES",
    "Event",
    "EventLogError",
    "EventValidationError",
    "ReducerError",
    "Simulation",
    "WorldState",
    "append",
    "assert_append_only",
    "branch_prefix",
    "connect",
    "count_events",
    "fixture_id",
    "is_fixture_id",
    "iter_events",
    "list_events",
    "list_exchanges_for_export",
    "list_simulations",
    "new_simulation_id",
    "next_occurrence",
    "order_key",
    "reduce_events",
    "replay",
    "replay_digest",
]
