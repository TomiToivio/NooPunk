"""Living story arcs and a non-omniscient Story Director (#1230).

An arc is a persistent authored possibility, not a railroad. The Director activates arcs only
when their activation event occurs and never overrides a player choice, an NPC's autonomy, dice
results or factual state. It is deliberately small: event matching, progress, side-quest
activation/expiry and a spoiler-safe view.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

ARC_MODES = ("scripted", "conditional", "procedural", "emergent")
ARC_STATES = ("dormant", "active", "resolved", "abandoned", "expired")


class StoryError(ValueError):
    """An arc invariant was violated."""


@dataclass
class Arc:
    id: str
    title: str
    mode: str = "scripted"
    status: str = "dormant"
    activation_event: str = ""
    progress_events: tuple[str, ...] = ()
    resolution_event: str = ""
    goal_ids: tuple[str, ...] = ()
    progress: int = 0

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.title.strip():
            raise StoryError("an arc needs an id and a title")
        if self.mode not in ARC_MODES:
            raise StoryError(f"unknown arc mode: {self.mode}")
        if self.status not in ARC_STATES:
            raise StoryError(f"unknown arc status: {self.status}")
        if self.progress < 0:
            raise StoryError("arc progress cannot be negative")

    def activate(self) -> None:
        if self.status == "dormant":
            self.status = "active"

    def resolve(self) -> None:
        if self.status == "active":
            self.status = "resolved"

    def abandon(self) -> None:
        if self.status == "active":
            self.status = "abandoned"

    def expire(self) -> None:
        if self.status == "dormant":
            self.status = "expired"

    def snapshot(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "mode": self.mode,
            "status": self.status,
            "activation_event": self.activation_event,
            "progress_events": list(self.progress_events),
            "resolution_event": self.resolution_event,
            "goal_ids": list(self.goal_ids),
            "progress": self.progress,
        }


@dataclass
class StoryDirector:
    """Event-to-arc matcher; returns arc ids affected by an event, with no spoiler text."""

    arcs: dict[str, Arc] = field(default_factory=dict)

    def add(self, arc: Arc) -> Arc:
        if arc.id in self.arcs:
            raise StoryError(f"duplicate arc id: {arc.id}")
        self.arcs[arc.id] = arc
        return arc

    def on_event(self, event_kind: str, *, event_id: str = "") -> tuple[str, ...]:
        affected: list[str] = []
        for arc in self.arcs.values():
            if arc.status == "dormant" and arc.activation_event == event_kind:
                arc.activate()
                affected.append(arc.id)
                continue
            if arc.status != "active":
                continue
            if event_kind in arc.progress_events:
                arc.progress += 1
                affected.append(arc.id)
            if arc.resolution_event and arc.resolution_event == event_kind:
                arc.resolve()
                affected.append(arc.id)
        return tuple(dict.fromkeys(affected))

    def active(self, *, spoiler_safe: bool = True) -> tuple[dict, ...]:
        rows = []
        for arc in self.arcs.values():
            if arc.status != "active":
                continue
            row = {"id": arc.id, "title": arc.title, "progress": arc.progress}
            if not spoiler_safe:
                row.update({"mode": arc.mode, "goal_ids": list(arc.goal_ids)})
            rows.append(row)
        return tuple(rows)

    def snapshot(self) -> list[dict]:
        return [
            arc.snapshot() for arc in sorted(self.arcs.values(), key=lambda arc: arc.id)
        ]

    @classmethod
    def from_snapshot(cls, rows: Iterable[Mapping]) -> StoryDirector:
        director = cls()
        for row in rows:
            director.add(
                Arc(
                    str(row["id"]),
                    str(row["title"]),
                    str(row.get("mode", "scripted")),
                    str(row.get("status", "dormant")),
                    str(row.get("activation_event", "")),
                    tuple(str(value) for value in row.get("progress_events", ())),
                    str(row.get("resolution_event", "")),
                    tuple(str(value) for value in row.get("goal_ids", ())),
                    int(row.get("progress", 0)),
                )
            )
        return director
