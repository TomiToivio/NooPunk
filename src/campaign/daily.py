"""The daily loop and its event-driven fast-forward (#1230).

The default day is a schedule, not a click-by-click timetable. Meals, ordinary sleep and routine
preparation auto-resolve; the player can explicitly skip or change them. The loop never forces a
narration for an uneventful minute.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .clock import GameClock, GameTime, ScheduledEvent
from .dreams import DreamEngine, DreamScene
from .story import StoryDirector


class DailyLoopError(ValueError):
    """A daily-loop invariant was violated."""


@dataclass(frozen=True)
class DayTemplate:
    wake: int = 7 * 60
    briefing: int = 8 * 60
    work_start: int = 9 * 60
    lunch: int = 12 * 60
    work_end: int = 17 * 60
    leisure: int = 18 * 60
    sleep: int = 23 * 60

    def __post_init__(self) -> None:
        times = (
            self.wake,
            self.briefing,
            self.work_start,
            self.lunch,
            self.work_end,
            self.leisure,
            self.sleep,
        )
        if any(not 0 <= value < 24 * 60 for value in times):
            raise DailyLoopError("template times must be within one day")
        if list(times) != sorted(times):
            raise DailyLoopError("template times must be ordered")


@dataclass
class DailyLoop:
    clock: GameClock
    template: DayTemplate = field(default_factory=DayTemplate)
    dreams: DreamEngine = field(default_factory=DreamEngine)
    story: StoryDirector = field(default_factory=StoryDirector)
    routine_defaults: bool = True

    def schedule_day(self, day: int) -> tuple[str, ...]:
        """Schedule one day's structural events once. Meal/rest defaults need no events."""
        if day < 1:
            raise DailyLoopError("day must be >= 1")
        events = (
            ("wake", self.template.wake),
            ("morning_briefing", self.template.briefing),
            ("work_start", self.template.work_start),
            ("lunch_default", self.template.lunch),
            ("work_end", self.template.work_end),
            ("leisure", self.template.leisure),
            ("sleep", self.template.sleep),
        )
        scheduled: list[str] = []
        for kind, minute in events:
            event_id = f"day.{day}.{kind}"
            if self.clock.scheduler.has(event_id) or self.clock.log.has(event_id):
                continue
            self.clock.schedule(
                ScheduledEvent(event_id, GameTime(day, minute), kind, {"day": day})
            )
            scheduled.append(event_id)
        return tuple(scheduled)

    def advance(self, minutes: int) -> tuple[dict[str, Any], ...]:
        """Advance the clock, returning fired events and affected arcs."""
        fired = self.clock.advance(minutes)
        return tuple(
            self._enrich(
                event.kind, {"id": event.id, "kind": event.kind, "at": event.at.label()}
            )
            for event in fired
        )

    def fast_forward(self, limit_events: int = 100) -> tuple[dict[str, Any], ...]:
        """Jump from event to event; no minute-by-minute narration."""
        results: list[dict[str, Any]] = []
        for _ in range(limit_events):
            fired = self.clock.run_until_next_event()
            if not fired:
                break
            results.extend(
                self._enrich(
                    event.kind,
                    {"id": event.id, "kind": event.kind, "at": event.at.label()},
                )
                for event in fired
            )
        return tuple(results)

    def sleep(
        self,
        *,
        night: int | None = None,
        forced_dream: str | None = None,
        seed: int = 0,
        source: str = "",
    ) -> DreamScene:
        """Advance to sleep, process the dream and schedule the next day."""
        day = self.clock.time.day if night is None else night
        sleep_time = GameTime(day, self.template.sleep)
        if self.clock.time < sleep_time:
            self.advance(sleep_time.total_minutes - self.clock.time.total_minutes)
        dream = self.dreams.choose(day, seed=seed, forced=forced_dream, source=source)
        self.schedule_day(day + 1)
        return dream

    def _enrich(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        arcs = self.story.on_event(kind, event_id=str(payload["id"]))
        if arcs:
            payload["arcs"] = list(arcs)
        return payload

    def snapshot(self) -> dict[str, Any]:
        return {"clock": self.clock.snapshot(), "story": self.story.snapshot()}

    @classmethod
    def from_snapshot(
        cls,
        payload: dict[str, Any],
        *,
        dreams: DreamEngine | None = None,
        template: DayTemplate | None = None,
    ) -> DailyLoop:
        return cls(
            GameClock.from_snapshot(payload["clock"]),
            template=template or DayTemplate(),
            dreams=dreams or DreamEngine(),
            story=StoryDirector.from_snapshot(payload.get("story", ())),
        )


__all__ = ["DailyLoop", "DailyLoopError", "DayTemplate"]
