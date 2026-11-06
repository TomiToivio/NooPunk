"""The clock-driven event queue (#1230 Phase 1).

The daily loop, tasks, appointments and faction ticks all need the same thing: *"what is due, and has it already
happened?"* This module answers that question and nothing else. It is not a second event log — the canonical record of
what happened is still :mod:`simulation.events`; the scheduler only decides *when* something becomes due and guarantees
it becomes due **once**.

Determinism rules, each of which has a test:

* **Ordering is ``(due, id)``.** Two events due in the same minute fire in a stable order, so a replay produces the
  same sequence on any machine.
* **Ids are unique.** Scheduling an id twice with the same content is a no-op (that is what makes resume safe);
  scheduling it with different content is an error, because silently replacing a pending appointment is how a save
  loses an event.
* **Processing is idempotent.** Every fired id is recorded. Processing the same window twice, or restoring a save and
  processing again, fires nothing a second time.
* **No repeats.** A recurring obligation (a morning briefing) enqueues its next occurrence when it fires; the queue
  itself does not guess an interval. That keeps "daily" a decision of the daily loop rather than a hidden rule here.
"""
from __future__ import annotations

import hashlib
import json
import random
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .clock import ClockError, GameClock

__all__ = ["DueEvent", "Scheduler", "SchedulerError"]


class SchedulerError(ValueError):
    """An operation the queue refuses rather than guessing at."""


@dataclass(frozen=True, slots=True)
class DueEvent:
    """Something that becomes due at a moment. ``kind`` and ``payload`` are open vocabulary.

    The vocabulary is deliberately open: #1230 names briefings, task completions, appointments and faction ticks, but
    the author has not frozen the full list, and an enum here would turn a proposal into canon.
    """

    id: str
    due: datetime
    kind: str
    payload: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise SchedulerError("a scheduled event needs an id")
        if not self.kind.strip():
            raise SchedulerError(f"scheduled event {self.id!r} needs a kind")
        if self.due.tzinfo is None:
            raise SchedulerError(f"scheduled event {self.id!r} needs a timezone-aware due time")

    def sort_key(self) -> tuple[datetime, str]:
        """The one ordering rule: due time, then id."""
        return (self.due, self.id)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "due": self.due.isoformat(), "kind": self.kind,
                "payload": dict(sorted(self.payload.items()))}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> DueEvent:
        try:
            return cls(
                id=str(payload["id"]),
                due=datetime.fromisoformat(str(payload["due"])),
                kind=str(payload["kind"]),
                payload=dict(payload.get("payload") or {}),
            )
        except (KeyError, ValueError) as exc:
            raise SchedulerError(f"unreadable scheduled event: {payload!r}") from exc


@dataclass
class Scheduler:
    """Pending events plus the record of what has already fired."""

    pending: dict[str, DueEvent] = field(default_factory=dict)
    fired: list[str] = field(default_factory=list)

    #: Seed for per-event randomness. Persisted so a replay produces the same numbers.
    seed: int = 20451

    #: Every id that has fired, for O(1) idempotency checks. Derived from ``fired`` on load.
    _fired_ids: set[str] = field(default_factory=set, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.fired and not self._fired_ids:
            self._fired_ids = set(self.fired)

    # -- queueing ------------------------------------------------------------------------------ #
    def schedule(self, event: DueEvent) -> bool:
        """Add an event; returns ``True`` if it was added.

        Re-scheduling an identical id is a no-op so that resuming a save cannot double-book; re-scheduling the same id
        with different content is refused, because one id means one occurrence.
        """
        existing = self.pending.get(event.id)
        if existing is not None:
            if existing == event:
                return False
            raise SchedulerError(
                f"{event.id!r} is already scheduled for {existing.due.isoformat()}; "
                "one id is one occurrence — use a new id for a new event"
            )
        if event.id in self._fired_ids:
            raise SchedulerError(
                f"{event.id!r} has already fired; firing it again would duplicate a world event"
            )
        self.pending[event.id] = event
        return True

    def cancel(self, event_id: str) -> DueEvent | None:
        """Remove a pending event. Cancelling something already fired is not an error — it is simply gone."""
        return self.pending.pop(event_id, None)

    # -- running ------------------------------------------------------------------------------- #
    def due(self, clock: GameClock, *, horizon_minutes: int = 0) -> tuple[DueEvent, ...]:
        """Events due at or before the clock's moment (plus an optional look-ahead), in firing order."""
        limit = clock.now.timestamp() + horizon_minutes * 60
        return tuple(sorted(
            (event for event in self.pending.values() if event.due.timestamp() <= limit),
            key=DueEvent.sort_key,
        ))

    def next_due(self) -> DueEvent | None:
        """The soonest pending event, or ``None``. Used to fast-forward without simulating every minute."""
        if not self.pending:
            return None
        return min(self.pending.values(), key=DueEvent.sort_key)

    def run(self, clock: GameClock, handler: Callable[[DueEvent], None],
            *, horizon_minutes: int = 0) -> tuple[DueEvent, ...]:
        """Fire everything currently due, in order, exactly once.

        ``handler`` is the caller's: this module does not know what a briefing or a task completion means. An event is
        removed from the queue *before* the handler is called and appended to ``fired`` regardless of what the handler
        does, so a handler that raises still cannot cause the same event to fire twice on the next resume. That is the
        idempotency guarantee the issue asks for, and it is why the fired list is the record, not the queue.
        """
        fired: list[DueEvent] = []
        for event in self.due(clock, horizon_minutes=horizon_minutes):
            del self.pending[event.id]
            self.fired.append(event.id)
            self._fired_ids.add(event.id)
            fired.append(event)
            handler(event)
        return tuple(fired)

    # -- deterministic randomness --------------------------------------------------------------- #
    def rng_for(self, event_id: str) -> random.Random:
        """A generator bound to one event, so a replay draws the same numbers.

        The seed is derived with ``sha256`` rather than ``hash()``: the builtin is salted per
        interpreter, so two runs of the same save would diverge and a replay would stop reproducing
        the original — the one thing #1230 asks this module to guarantee. Passing the event id in
        makes the stream independent of *when* the event is handled, so reordering an unrelated
        handler cannot shift it.
        """
        digest = hashlib.sha256(event_id.encode("utf-8")).digest()[:8]
        return random.Random(self.seed ^ int.from_bytes(digest, "big"))

    # -- persistence --------------------------------------------------------------------------- #
    def to_dict(self) -> dict[str, Any]:
        return {
            "pending": [event.to_dict() for event in sorted(self.pending.values(), key=DueEvent.sort_key)],
            "fired": list(self.fired),
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> Scheduler:
        pending: dict[str, DueEvent] = {}
        for raw in payload.get("pending") or ():
            event = DueEvent.from_dict(raw)
            if event.id in pending:
                raise SchedulerError(f"a save contains {event.id!r} twice")
            pending[event.id] = event
        fired = [str(item) for item in (payload.get("fired") or ())]
        if len(set(fired)) != len(fired):
            raise SchedulerError("a save's fired list contains duplicates; the queue cannot be trusted")
        overlap = set(pending) & set(fired)
        if overlap:
            raise SchedulerError(f"a save has {sorted(overlap)} both pending and fired")
        return cls(pending=pending, fired=fired, seed=int(payload.get("seed", 20451)))

    def save(self, path: Path, clock: GameClock) -> None:
        """Write clock and queue together — a save that restores one but not the other is not a save."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(
            {"version": 1, "clock": clock.to_dict(), "scheduler": self.to_dict()},
            indent=2, ensure_ascii=False,
        ) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> tuple[GameClock, Scheduler]:
        """Read clock and queue back. Refuses an unknown format version rather than guessing."""
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("version") != 1:
            raise SchedulerError(f"unsupported save version {payload.get('version')!r}")
        try:
            return GameClock.from_dict(payload["clock"]), cls.from_dict(payload["scheduler"])
        except (KeyError, ClockError) as exc:
            raise SchedulerError(f"incomplete save: {exc}") from exc


def merge_payloads(events: Iterable[DueEvent]) -> dict[str, Any]:  # pragma: no cover - helper for callers
    """Collect payload fields from a run, last-writer-wins per key, in firing order.

    A convenience for adapters that only need the net effect of a window. Kept here so two adapters cannot invent two
    different merge rules.
    """
    merged: dict[str, Any] = {}
    for event in events:
        merged.update(event.payload)
    return merged
