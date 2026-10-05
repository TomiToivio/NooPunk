"""SQLite-backed per-actor memory for the Concordia runtime (#60 package C).

The persistent EP2 session (:mod:`ep2_session`) keeps shared *event* memory: one
append-only log every participant can read. That is a world record, not an agent's
mind. This module adds the missing half: memory that belongs to **one actor**.

Motivation, from the issue. Package C lists "Add persistent memory" as its last
unchecked item, and the first-playable milestone requires "persistent agent memory"
(success criterion 8) alongside the world state that already persists. The maintained
milestone doc (`docs/sources/EP2_SESSION_MILESTONE.md`) names "private agent memory"
as the next gap after the shared event log. This module fills that gap without
touching the shared-log semantics.

Three properties are deliberate and structural, not conveniences:

* **Private by default.** A note recorded by one actor is invisible to another.
  This is the whole point: without it, "memory" is just the world log again.
* **No mechanics.** A memory is a short text record with a turn and an optional
  subject. It carries no dice, ratings, statistics or resolution - per ``AGENTS.md``
  §1 nothing mechanical may be invented here, and the resolver seam stays the only
  path from agent output into mechanics.
* **Append-only.** As with the event log (``simulation.sqlite_store``), a memory is
  immutable once recorded; corrections are new memories. There is therefore no
  update or delete.

The store is separate from the session's event database on purpose, so it can be
attached to one actor's private file without sharing the world's. Pass an existing
connection to co-locate it with the session if that is what a caller wants.

Python's stdlib ``sqlite3`` only: no dependency is added, per ``AGENTS.md`` §10.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class MemoryStore:
    """Per-actor private notes, durable across sessions.

    Usage::

        store = MemoryStore("agent.sqlite")
        store.remember("player", "the analyst recognised my face", turn=3)
        store.recall("player")          # -> [that note]

    Reopening the same path restores the notes. One process writer per database is
    expected, as with the event log.
    """

    def __init__(self, path: str | Path = ":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS memory ("
            "  id INTEGER PRIMARY KEY,"
            "  actor TEXT NOT NULL,"
            "  turn INTEGER NOT NULL,"
            "  subject TEXT NOT NULL DEFAULT '',"
            "  note TEXT NOT NULL"
            ")"
        )
        self.db.commit()

    def remember(
        self,
        actor: str,
        note: str,
        *,
        turn: int = 0,
        subject: str = "",
    ) -> dict[str, Any]:
        """Append one privately-held note for ``actor``.

        Raises ``ValueError`` on an empty actor or empty note, matching the
        session's refusal of empty identifiers: a blank memory is not a memory.
        """
        if not actor or not isinstance(actor, str):
            raise ValueError("Memory requires a nonempty actor.")
        if not note or not isinstance(note, str):
            raise ValueError("Memory requires a nonempty note.")
        if not isinstance(turn, int) or turn < 0:
            raise ValueError("Memory turn must be a nonnegative integer.")
        with self.db:
            cursor = self.db.execute(
                "INSERT INTO memory(actor, turn, subject, note) VALUES (?, ?, ?, ?)",
                (actor, turn, subject, note),
            )
        return {
            "id": cursor.lastrowid,
            "actor": actor,
            "turn": turn,
            "subject": subject,
            "note": note,
        }

    def recall(
        self,
        actor: str,
        *,
        subject: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return ``actor``'s own notes in insertion order.

        Passing ``subject`` filters to one subject. Another actor's notes are never
        returned: there is no parameter that reaches them.
        """
        if not actor or not isinstance(actor, str):
            raise ValueError("Recall requires a nonempty actor.")
        sql = "SELECT id, actor, turn, subject, note FROM memory WHERE actor=?"
        params: list[Any] = [actor]
        if subject is not None:
            sql += " AND subject=?"
            params.append(subject)
        sql += " ORDER BY id"
        return [self._row(row) for row in self.db.execute(sql, params)]

    def forget(self, actor: str, memory_id: int) -> bool:
        """Remove one of ``actor``'s notes by id.

        Returns whether a row was removed. Scoped to the owning actor, so an id
        belonging to someone else cannot be erased through this actor. This is the
        one mutation the append-only rule permits: dropping a note is not editing
        history, it is the actor choosing not to keep it.
        """
        if not actor or not isinstance(actor, str):
            raise ValueError("Forget requires a nonempty actor.")
        with self.db:
            cursor = self.db.execute(
                "DELETE FROM memory WHERE id=? AND actor=?", (memory_id, actor)
            )
        return cursor.rowcount > 0

    def actors(self) -> tuple[str, ...]:
        """Every actor that currently holds at least one note."""
        rows = self.db.execute("SELECT DISTINCT actor FROM memory ORDER BY actor")
        return tuple(row[0] for row in rows)

    def close(self) -> None:
        self.db.close()

    @staticmethod
    def _row(row: tuple[Any, ...]) -> dict[str, Any]:
        memory_id, actor, turn, subject, note = row
        return {"id": memory_id, "actor": actor, "turn": turn,
                "subject": subject, "note": note}


class MemoryObserver:
    """An :class:`ep2_session.Observer` that keeps its observations privately.

    ``EP2Session.resolve`` hands every observer the committed event as JSON. An
    agent using this class records those events into its **own** :class:`MemoryStore`,
    which is what turns the shared event log into per-agent memory. Two agents
    attached to the same session build two separate memories.

    Duck-typed on purpose, like the session's own ``Observer`` protocol: this module
    does not import ``ep2_session``, so the memory layer stays independent of the
    session and the two can be tested apart.
    """

    def __init__(self, actor: str, store: MemoryStore):
        if not actor or not isinstance(actor, str):
            raise ValueError("MemoryObserver requires a nonempty actor.")
        self.actor = actor
        self.store = store

    def observe(self, observation: str) -> None:
        """Persist one observation for the owning actor."""
        if not observation:
            raise ValueError("An empty observation is not worth remembering.")
        self.store.remember(self.actor, observation)


__all__ = ["MemoryObserver", "MemoryStore"]
