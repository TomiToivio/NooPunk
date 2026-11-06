"""Deterministic clock, calendar and event scheduling for the living campaign (#1230)."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

MINUTES_PER_DAY = 24 * 60
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


class ClockError(ValueError):
    """A clock, calendar or schedule invariant was violated."""


@dataclass(frozen=True, order=True)
class GameTime:
    """One deterministic instant: a 1-based campaign day and a minute 0..1439."""

    day: int = 1
    minute: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.day, int) or self.day < 1:
            raise ClockError("day must be an integer >= 1")
        if not isinstance(self.minute, int) or not 0 <= self.minute < MINUTES_PER_DAY:
            raise ClockError("minute must be an integer 0..1439")

    @property
    def total_minutes(self) -> int:
        return (self.day - 1) * MINUTES_PER_DAY + self.minute

    @property
    def weekday(self) -> str:
        return DAYS[(self.day - 1) % 7]

    @property
    def is_weekend(self) -> bool:
        return self.weekday in ("Saturday", "Sunday")

    def add(self, minutes: int) -> GameTime:
        if not isinstance(minutes, int) or minutes < 0:
            raise ClockError("minutes to add must be a non-negative integer")
        total = self.total_minutes + minutes
        return GameTime(total // MINUTES_PER_DAY + 1, total % MINUTES_PER_DAY)

    def advance_to(self, target: GameTime) -> GameTime:
        if target < self:
            raise ClockError("the clock cannot move backwards")
        return target

    def label(self) -> str:
        return f"{self.weekday}, day {self.day}, {self.minute // 60:02d}:{self.minute % 60:02d}"


@dataclass(frozen=True)
class ScheduledEvent:
    """A due date and a stable id. Duplicate ids are rejected, not silently replaced."""

    id: str
    at: GameTime
    kind: str
    payload: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ClockError("a scheduled event needs an id")
        if not self.kind.strip():
            raise ClockError("a scheduled event needs a kind")


@dataclass(frozen=True)
class FiredEvent:
    """An event that has happened, recorded once by its stable id."""

    id: str
    at: GameTime
    kind: str
    payload: Mapping[str, Any] = field(default_factory=dict)


class EventLog:
    """Append-only, idempotent event history.

    Replaying a save or receiving an overlapping scheduler tick twice must not duplicate an
    event. The id is the idempotency key; the first payload wins.
    """

    def __init__(self, entries: Iterable[FiredEvent] = ()) -> None:
        self._entries: list[FiredEvent] = []
        self._ids: set[str] = set()
        for entry in entries:
            self.record(entry)

    def record(self, event: FiredEvent) -> bool:
        if event.id in self._ids:
            return False
        self._ids.add(event.id)
        self._entries.append(event)
        return True

    def has(self, event_id: str) -> bool:
        return event_id in self._ids

    @property
    def entries(self) -> tuple[FiredEvent, ...]:
        return tuple(self._entries)

    def by_kind(self, kind: str) -> tuple[FiredEvent, ...]:
        return tuple(event for event in self._entries if event.kind == kind)

    def snapshot(self) -> list[dict[str, Any]]:
        return [
            {
                "id": event.id,
                "day": event.at.day,
                "minute": event.at.minute,
                "kind": event.kind,
                "payload": dict(event.payload),
            }
            for event in self._entries
        ]

    @classmethod
    def from_snapshot(cls, rows: Iterable[Mapping[str, Any]]) -> EventLog:
        return cls(
            FiredEvent(
                str(row["id"]),
                GameTime(int(row["day"]), int(row["minute"])),
                str(row["kind"]),
                dict(row.get("payload", {})),
            )
            for row in rows
        )


class Scheduler:
    """A deterministic due-date queue; event-driven, not per-minute simulation."""

    def __init__(self, events: Iterable[ScheduledEvent] = ()) -> None:
        self._events: dict[str, ScheduledEvent] = {}
        for event in events:
            self.schedule(event)

    def schedule(self, event: ScheduledEvent) -> None:
        if event.id in self._events:
            raise ClockError(f"duplicate scheduled event id: {event.id}")
        self._events[event.id] = event

    def cancel(self, event_id: str) -> bool:
        return self._events.pop(event_id, None) is not None

    def has(self, event_id: str) -> bool:
        return event_id in self._events

    def due(self, now: GameTime) -> tuple[ScheduledEvent, ...]:
        return tuple(
            sorted(
                (event for event in self._events.values() if event.at <= now),
                key=lambda event: (event.at, event.id),
            )
        )

    def pop_due(self, now: GameTime) -> tuple[ScheduledEvent, ...]:
        due = self.due(now)
        for event in due:
            self._events.pop(event.id, None)
        return due

    def next_at(self) -> GameTime | None:
        return min((event.at for event in self._events.values()), default=None)

    def snapshot(self) -> list[dict[str, Any]]:
        return [
            {
                "id": event.id,
                "day": event.at.day,
                "minute": event.at.minute,
                "kind": event.kind,
                "payload": dict(event.payload),
            }
            for event in sorted(
                self._events.values(), key=lambda event: (event.at, event.id)
            )
        ]

    @classmethod
    def from_snapshot(cls, rows: Iterable[Mapping[str, Any]]) -> Scheduler:
        return cls(
            ScheduledEvent(
                str(row["id"]),
                GameTime(int(row["day"]), int(row["minute"])),
                str(row["kind"]),
                dict(row.get("payload", {})),
            )
            for row in rows
        )


class GameClock:
    """Authoritative clock + scheduler + event log. Save and replay preserve all three."""

    def __init__(
        self,
        time: GameTime | None = None,
        *,
        scheduler: Scheduler | None = None,
        log: EventLog | None = None,
    ) -> None:
        self.time = time or GameTime()
        self.scheduler = scheduler or Scheduler()
        self.log = log or EventLog()

    def schedule(self, event: ScheduledEvent) -> None:
        self.scheduler.schedule(event)

    def advance(self, minutes: int) -> tuple[FiredEvent, ...]:
        """Advance, firing every due event once. An event already logged is never replayed."""
        target = self.time.add(minutes)
        return self.advance_to(target)

    def advance_to(self, target: GameTime) -> tuple[FiredEvent, ...]:
        if target < self.time:
            raise ClockError("the clock cannot move backwards")
        fired: list[FiredEvent] = []
        for due in self.scheduler.pop_due(target):
            event = FiredEvent(due.id, due.at, due.kind, dict(due.payload))
            if self.log.record(event):
                fired.append(event)
        self.time = target
        return tuple(fired)

    def run_until_next_event(self) -> tuple[FiredEvent, ...]:
        """Event-driven fast-forward; returns no events if the queue is empty."""
        nxt = self.scheduler.next_at()
        if nxt is None:
            return ()
        return self.advance_to(nxt)

    def snapshot(self) -> dict[str, Any]:
        return {
            "day": self.time.day,
            "minute": self.time.minute,
            "scheduled": self.scheduler.snapshot(),
            "log": self.log.snapshot(),
        }

    @classmethod
    def from_snapshot(cls, payload: Mapping[str, Any]) -> GameClock:
        return cls(
            GameTime(int(payload["day"]), int(payload["minute"])),
            scheduler=Scheduler.from_snapshot(payload.get("scheduled", ())),
            log=EventLog.from_snapshot(payload.get("log", ())),
        )
