"""Time-consuming tasks that are not Scenes (#1230).

A task consumes real in-game time and may pause, resume, be interrupted, or produce an optional
clue. It never invents a new action economy: a CWN check is supplied by the caller only where
uncertainty is meaningful, and failure costs time/quality rather than blocking all progress.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any


class TaskError(ValueError):
    """A task invariant was violated."""


TASK_STATES = ("pending", "active", "paused", "completed", "abandoned")


@dataclass
class Task:
    id: str
    description: str
    duration_minutes: int
    location: str = ""
    goal_id: str = ""
    skill: str = ""
    difficulty: int | None = None
    priority: int = 0
    deadline_day: int | None = None
    state: str = "pending"
    remaining_minutes: int | None = None
    quality: str = "normal"
    interruptions: int = 0

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.description.strip():
            raise TaskError("a task needs an id and a description")
        if not isinstance(self.duration_minutes, int) or self.duration_minutes <= 0:
            raise TaskError("duration_minutes must be positive")
        if self.remaining_minutes is None:
            self.remaining_minutes = self.duration_minutes
        if (
            not isinstance(self.remaining_minutes, int)
            or not 0 <= self.remaining_minutes <= self.duration_minutes
        ):
            raise TaskError("remaining_minutes must be within 0..duration_minutes")
        if self.state not in TASK_STATES:
            raise TaskError(f"unknown task state: {self.state}")
        if self.difficulty is not None and self.difficulty < 0:
            raise TaskError("difficulty cannot be negative")

    @property
    def completed(self) -> bool:
        return self.state == "completed"

    def pause(self) -> None:
        if self.state == "active":
            self.state = "paused"

    def resume(self) -> None:
        if self.state in ("pending", "paused"):
            self.state = "active"

    def snapshot(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "location": self.location,
            "goal_id": self.goal_id,
            "skill": self.skill,
            "difficulty": self.difficulty,
            "priority": self.priority,
            "deadline_day": self.deadline_day,
            "state": self.state,
            "remaining_minutes": self.remaining_minutes,
            "quality": self.quality,
            "interruptions": self.interruptions,
        }

    @classmethod
    def from_snapshot(cls, payload: Mapping[str, Any]) -> Task:
        return cls(
            str(payload["id"]),
            str(payload["description"]),
            int(payload["duration_minutes"]),
            str(payload.get("location", "")),
            str(payload.get("goal_id", "")),
            str(payload.get("skill", "")),
            None if payload.get("difficulty") is None else int(payload["difficulty"]),
            int(payload.get("priority", 0)),
            None
            if payload.get("deadline_day") is None
            else int(payload["deadline_day"]),
            str(payload.get("state", "pending")),
            None
            if payload.get("remaining_minutes") is None
            else int(payload["remaining_minutes"]),
            str(payload.get("quality", "normal")),
            int(payload.get("interruptions", 0)),
        )


@dataclass(frozen=True)
class TaskResult:
    task_id: str
    elapsed_minutes: int
    completed: bool
    check_required: bool
    success: bool | None
    quality: str
    note: str = ""


@dataclass
class TaskBoard:
    """Pausable/resumable tasks with no double-spending of time."""

    tasks: dict[str, Task] = field(default_factory=dict)

    def add(self, task: Task) -> Task:
        if task.id in self.tasks:
            raise TaskError(f"duplicate task id: {task.id}")
        self.tasks[task.id] = task
        return task

    def task(self, task_id: str) -> Task:
        try:
            return self.tasks[task_id]
        except KeyError as exc:
            raise TaskError(f"unknown task: {task_id}") from exc

    def start(self, task_id: str) -> Task:
        task = self.task(task_id)
        task.resume()
        return task

    def pause(self, task_id: str) -> Task:
        task = self.task(task_id)
        task.pause()
        return task

    def interrupt(self, task_id: str) -> Task:
        task = self.task(task_id)
        if not task.completed:
            task.interruptions += 1
            task.state = "paused"
        return task

    def advance(
        self, task_id: str, minutes: int, *, check_total: int | None = None
    ) -> TaskResult:
        """Spend in-game minutes on a task.

        If ``check_total`` is supplied, the task must declare a difficulty; success is
        ``check_total >= difficulty``. Failure costs 25% additional time (minimum one minute) and
        reduces quality; it does not erase progress or block the clue permanently.
        """
        if not isinstance(minutes, int) or minutes <= 0:
            raise TaskError("minutes must be a positive integer")
        task = self.task(task_id)
        if task.completed:
            return TaskResult(
                task_id, 0, True, False, None, task.quality, "already complete"
            )
        if task.state == "pending":
            task.resume()
        if task.state not in ("active", "paused"):
            raise TaskError(f"task {task_id!r} is {task.state}")

        check_required = check_total is not None
        success: bool | None = None
        remaining = task.remaining_minutes
        if remaining is None:
            raise TaskError("task has no remaining time")
        if check_required:
            if task.difficulty is None:
                raise TaskError("a check was supplied but the task has no difficulty")
            success = int(check_total) >= task.difficulty
            if not success:
                task.quality = "reduced"
                remaining += max(1, task.duration_minutes // 4)

        task.remaining_minutes = max(0, remaining - minutes)
        if task.remaining_minutes == 0:
            task.state = "completed"
        note = ""
        if check_required and not success:
            note = "check failed: time and quality paid, progress retained"
        return TaskResult(
            task_id,
            minutes,
            task.completed,
            check_required,
            success,
            task.quality,
            note,
        )

    def snapshot(self) -> list[dict[str, Any]]:
        return [
            task.snapshot()
            for task in sorted(self.tasks.values(), key=lambda task: task.id)
        ]

    @classmethod
    def from_snapshot(cls, rows: Iterable[Mapping[str, Any]]) -> TaskBoard:
        board = cls()
        for row in rows:
            board.add(Task.from_snapshot(row))
        return board
