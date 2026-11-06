"""Append-only event records for the social-science simulator (#1286).

Events are the inspectable trace of a run. They carry the rule that produced them
and the provenance of the input, so a reviewer can ask *why* a simulated action
happened without reading the code. The log is deterministic: event ids are
assigned by sequence, not by wall time.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from .model import Provenance

__all__ = ["EVENT_KINDS", "EventLog", "SimEvent"]

#: Event vocabulary for the MVP. New kinds are a schema change, not an incidental
#: extension: the point is to keep the trace comparable across runs.
EVENT_KINDS = (
    "communicate",
    "respond",
    "abstain",
    "affiliate",
    "support",
    "contest",
    "link_demands",
    "separate_demands",
    "resource_change",
    "attention_change",
    "institutional_response",
)


@dataclass(frozen=True, slots=True)
class SimEvent:
    event_id: str
    time: int
    kind: str
    actor: str
    target: str
    payload: dict[str, Any]
    rule: str
    provenance: Provenance
    synthetic: bool = True

    def __post_init__(self) -> None:
        if not self.event_id.startswith("evt:"):
            raise ValueError("event_id must use the 'evt:' prefix")
        if self.time < 0:
            raise ValueError("event time must be non-negative")
        if self.kind not in EVENT_KINDS:
            raise ValueError(f"unknown event kind {self.kind!r}")
        if not str(self.actor).strip():
            raise ValueError("event actor must be non-empty")
        if not str(self.rule).strip():
            raise ValueError("event rule must be non-empty")
        if self.synthetic is not True:
            raise ValueError("simulator events are synthetic by construction")

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "time": self.time,
            "kind": self.kind,
            "actor": self.actor,
            "target": self.target,
            "payload": dict(self.payload),
            "rule": self.rule,
            "provenance": self.provenance.to_dict(),
            "synthetic": self.synthetic,
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> SimEvent:
        return cls(
            event_id=str(raw["event_id"]),
            time=int(raw["time"]),
            kind=str(raw["kind"]),
            actor=str(raw["actor"]),
            target=str(raw.get("target", "")),
            payload=dict(raw.get("payload", {})),
            rule=str(raw["rule"]),
            provenance=Provenance.from_dict(raw["provenance"]),
            synthetic=bool(raw.get("synthetic", True)),
        )


@dataclass
class EventLog:
    """Append-only, sequence-ordered event trace."""

    events: list[SimEvent] = field(default_factory=list)
    _ids: set[str] = field(default_factory=set, repr=False)

    def append(self, event: SimEvent) -> SimEvent:
        if event.event_id in self._ids:
            raise ValueError(f"duplicate event id {event.event_id!r}")
        if self.events and event.time < self.events[-1].time:
            raise ValueError("events must be appended in non-decreasing time order")
        self.events.append(event)
        self._ids.add(event.event_id)
        return event

    def extend(self, events: list[SimEvent]) -> None:
        for event in events:
            self.append(event)

    def __len__(self) -> int:
        return len(self.events)

    def to_dicts(self) -> list[dict[str, Any]]:
        return [event.to_dict() for event in self.events]

    @classmethod
    def from_dicts(cls, rows: list[Mapping[str, Any]]) -> EventLog:
        log = cls()
        for row in rows:
            log.append(SimEvent.from_dict(row))
        return log
