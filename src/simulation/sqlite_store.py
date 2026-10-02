"""SQLite-backed event log: the durable spine of a NoöPunk simulation.

Issue #40 Phase B. Design constraints taken straight from the issue and the
architecture spec:

* **Append-only.** An event is immutable once logged; corrections are new events.
  This module therefore exposes no update or delete for events.
* **The log is the source of truth.** World state is derived by replaying the log
  (:mod:`world_state`), never stored as the only home of a canonical fact.
* **Idempotent append.** A duplicate ``event_id`` is ignored, so replaying a run
  into an existing database cannot double-apply it.
* **Synthetic/empirical separation is structural.** Every row carries
  ``simulation_id`` and ``synthetic``; :func:`list_exchanges_for_export` refuses to
  return synthetic rows for a non-synthetic export, so simulated data cannot be
  pulled out as if it were empirical (spec §5).

Python's stdlib ``sqlite3`` only: no dependency is added, per ``AGENTS.md`` §10.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Iterator

from .events import Event, order_key

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    seq           INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id TEXT    NOT NULL,
    event_id      TEXT    NOT NULL,
    turn          INTEGER NOT NULL,
    occurrence    INTEGER NOT NULL,
    timestamp     TEXT    NOT NULL DEFAULT '',
    actor         TEXT    NOT NULL,
    action_type   TEXT    NOT NULL,
    target        TEXT    NOT NULL DEFAULT '',
    content       TEXT    NOT NULL DEFAULT '',
    location      TEXT    NOT NULL DEFAULT '',
    visibility    TEXT    NOT NULL DEFAULT 'public',
    source        TEXT    NOT NULL,
    synthetic     INTEGER NOT NULL,
    UNIQUE (simulation_id, event_id)
);

CREATE INDEX IF NOT EXISTS idx_events_run_turn
    ON events (simulation_id, turn, occurrence, seq);
"""


class EventLogError(RuntimeError):
    """The event log was used in a way the spine does not allow."""


def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Open (and initialise) an event-log database."""
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.executescript(_SCHEMA)
    connection.execute(
        "INSERT OR IGNORE INTO schema_meta (key, value) VALUES ('schema_version', ?)",
        (str(SCHEMA_VERSION),),
    )
    connection.commit()
    return connection


def append(connection: sqlite3.Connection, *events: Event) -> int:
    """Append events; returns how many were newly written.

    Duplicates (same ``simulation_id`` + ``event_id``) are skipped, which is what
    makes replaying a log into a live database safe.
    """
    written = 0
    for event in events:
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO events (
                simulation_id, event_id, turn, occurrence, timestamp, actor,
                action_type, target, content, location, visibility, source, synthetic
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.simulation_id,
                event.event_id,
                event.turn,
                event.occurrence,
                event.timestamp,
                event.actor,
                event.action_type,
                event.target,
                event.content,
                event.location,
                event.visibility,
                event.source,
                1 if event.synthetic else 0,
            ),
        )
        written += cursor.rowcount
    connection.commit()
    return written


def iter_events(connection: sqlite3.Connection, simulation_id: str) -> Iterator[Event]:
    """Yield one run's events in canonical order: ``(turn, occurrence, seq)``."""
    cursor = connection.execute(
        """
        SELECT * FROM events
        WHERE simulation_id = ?
        ORDER BY turn ASC, occurrence ASC, seq ASC
        """,
        (simulation_id,),
    )
    for row in cursor:
        yield Event.from_dict(dict(row))


def list_events(connection: sqlite3.Connection, simulation_id: str) -> list[Event]:
    return list(iter_events(connection, simulation_id))


def count_events(connection: sqlite3.Connection, simulation_id: str) -> int:
    row = connection.execute(
        "SELECT COUNT(*) AS n FROM events WHERE simulation_id = ?", (simulation_id,)
    ).fetchone()
    return int(row["n"])


def list_simulations(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """One row per run: id, event count, turn span, and whether it is synthetic."""
    cursor = connection.execute(
        """
        SELECT simulation_id,
               COUNT(*)               AS event_count,
               MIN(turn)              AS first_turn,
               MAX(turn)              AS last_turn,
               MIN(synthetic)         AS min_synthetic,
               MAX(synthetic)         AS max_synthetic
        FROM events
        GROUP BY simulation_id
        ORDER BY simulation_id
        """
    )
    return [
        {
            "simulation_id": row["simulation_id"],
            "event_count": int(row["event_count"]),
            "first_turn": int(row["first_turn"]),
            "last_turn": int(row["last_turn"]),
            # A run is synthetic when any event in it is: mixing is a defect, not a mode.
            "synthetic": bool(row["max_synthetic"]),
            "mixed_synthetic": bool(row["max_synthetic"]) and not bool(row["min_synthetic"]),
        }
        for row in cursor
    ]


def assert_append_only(connection: sqlite3.Connection) -> None:
    """Fail if the log has been mutated other than by appending.

    The log is only useful as evidence if nothing can rewrite it. SQLite cannot be
    made append-only by schema declaration alone, so this check is run by tests and
    by any consumer that needs the guarantee: it verifies the row sequence is
    contiguous, i.e. no row was deleted out of the middle.
    """
    rows = connection.execute("SELECT seq FROM events ORDER BY seq ASC").fetchall()
    for expected, row in enumerate(rows, start=1):
        if int(row["seq"]) != expected:
            raise EventLogError(
                "event log is not append-only: expected seq "
                f"{expected} but found {row['seq']} (rows were deleted or renumbered)"
            )


def list_exchanges_for_export(
    connection: sqlite3.Connection, simulation_id: str, *, synthetic: bool
) -> list[Event]:
    """Public communications of one run, for a declared export kind.

    Refuses to hand back a synthetic run for a non-synthetic export. That is the
    structural half of the simulation-vs-empirical rule: the caller must state
    which kind of data it wants, and a mismatch is an error rather than a silent
    mislabelling.
    """
    run = next(
        (row for row in list_simulations(connection) if row["simulation_id"] == simulation_id),
        None,
    )
    if run is None:
        return []
    if run["synthetic"] != synthetic:
        raise EventLogError(
            f"refusing to export simulation {simulation_id!r}: it is "
            f"{'synthetic' if run['synthetic'] else 'empirical'} data but the export "
            f"declared synthetic={synthetic}. Synthetic and empirical data must not "
            "be mixed (docs/SIMULATION_ARCHITECTURE_SPEC.md §5)."
        )
    return [
        event
        for event in iter_events(connection, simulation_id)
        if event.is_public_communication()
    ]


def ordered(events: Iterable[Event]) -> list[Event]:
    """Sort by the canonical key so callers never sort by timestamp."""
    return sorted(events, key=order_key)
