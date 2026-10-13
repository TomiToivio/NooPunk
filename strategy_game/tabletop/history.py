"""Append-only, rule-neutral turn/event history for the strategy tabletop.

The history records *reported* outcomes. It never interprets, authorizes, or
applies an action, and is deliberately independent from world-state models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any

SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class HistoryEntry:
    sequence: int
    kind: str
    description: str
    actor_id: str | None = None
    source_id: str | None = None
    provenance: str = "unknown"
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        # A JSON roundtrip both rejects non-portable types and detaches callers'
        # mutable dictionaries from the stored representation.
        return json.loads(json.dumps({
            "sequence": self.sequence, "kind": self.kind,
            "description": self.description, "actor_id": self.actor_id,
            "source_id": self.source_id, "provenance": self.provenance,
            "details": self.details,
        }, allow_nan=False))


class HistoryLog:
    """Ordered observations, with explicit serialisation and no rule evaluation."""

    def __init__(self, entries: list[HistoryEntry] | None = None):
        self._entries: list[HistoryEntry] = []
        for entry in entries or []:
            self._append_existing(entry)

    def _append_existing(self, entry: HistoryEntry) -> None:
        if type(entry.sequence) is not int or entry.sequence != len(self._entries):
            raise ValueError("history sequence must be consecutive starting at zero")
        if not entry.kind.strip():
            raise ValueError("history kind must not be blank")
        detached = HistoryEntry(**entry.to_dict())
        self._entries.append(detached)

    @property
    def entries(self) -> tuple[HistoryEntry, ...]:
        # Do not hand out references to mutable entry.details.
        return tuple(HistoryEntry(**entry.to_dict()) for entry in self._entries)

    def append(self, kind: str, description: str, *, actor_id: str | None = None,
               source_id: str | None = None, provenance: str = "unknown",
               details: dict[str, Any] | None = None) -> HistoryEntry:
        entry = HistoryEntry(len(self._entries), kind, description, actor_id,
                             source_id, provenance, details or {})
        self._append_existing(entry)
        return self.entries[-1]

    def to_dict(self) -> dict[str, Any]:
        return {"schema_version": SCHEMA_VERSION,
                "entries": [entry.to_dict() for entry in self._entries]}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False, allow_nan=False)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> HistoryLog:
        if payload.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("unsupported history schema version")
        if not isinstance(payload.get("entries"), list):
            raise ValueError("history entries must be a list")
        return cls([HistoryEntry(**entry) for entry in payload["entries"]])

    @classmethod
    def from_json(cls, payload: str) -> HistoryLog:
        return cls.from_dict(json.loads(payload))
