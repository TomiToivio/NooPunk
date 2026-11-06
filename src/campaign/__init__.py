"""Living-campaign clock, tasks, story arcs and dream scenes (#1230).

Phase 1-2+4 of the issue: the authoritative clock/scheduler/event log, time-consuming tasks, a
small story director and Dream Scenes. Faction, enclave and NPC loops remain adapters over the
existing rules modules and are not re-implemented here; see docs/rules/LIVING_CAMPAIGN_1230.md.
"""

from .clock import (
    ClockError,
    EventLog,
    FiredEvent,
    GameClock,
    GameTime,
    ScheduledEvent,
    Scheduler,
)
from .daily import DailyLoop, DailyLoopError, DayTemplate
from .dreams import DreamEngine, DreamError, DreamKind, DreamScene
from .story import Arc, StoryDirector, StoryError
from .tasks import Task, TaskBoard, TaskError, TaskResult

__all__ = [
    "Arc",
    "ClockError",
    "DailyLoop",
    "DailyLoopError",
    "DayTemplate",
    "DreamEngine",
    "DreamError",
    "DreamKind",
    "DreamScene",
    "EventLog",
    "FiredEvent",
    "GameClock",
    "GameTime",
    "ScheduledEvent",
    "Scheduler",
    "StoryDirector",
    "StoryError",
    "Task",
    "TaskBoard",
    "TaskError",
    "TaskResult",
]
