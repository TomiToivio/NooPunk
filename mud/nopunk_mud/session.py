"""Typed adapter boundary over the campaign engine (#1053, #1054).

`CampaignEngine.command(line) -> str` is the rules/application core: a player says a
sentence, the engine returns prose. That is enough for the console, but an adapter that
must render a state change (a MUD prompt, a GUI panel, a simulation transcript) otherwise
has to diff state documents itself — and the second adapter to do that becomes a second
place where "what happened" is decided.

This module adds the thin typed layer the architecture asks for, and nothing else:

    Action(text)  ->  CampaignSession.execute(...)  ->  ActionResult(text, events, state, finished)

It owns **no rules**. Events are derived from the before/after state document, so an
event can never describe something the engine did not do. A rejected command produces
`rejected` and an unchanged state, which is exactly what a front-end needs to know.

Keep framework imports out of this module: it is part of the domain layer and
`tools/check_engine_boundary.py` scans it.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .campaign import CampaignEngine

SESSION_VERSION = 1


@dataclass(frozen=True)
class Action:
    """One player command, already parsed no further than the engine needs."""

    text: str


@dataclass(frozen=True)
class Event:
    """Something the engine did, derived from the state transition.

    `kind` is a small closed vocabulary so adapters can switch on it:
    ``turn``, ``rejected``, ``location_changed``, ``clue_gained``, ``flag_gained``,
    ``hp_changed``, ``ending_reached``.
    """

    kind: str
    detail: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionResult:
    """What the player sees, what changed, and the state after the change."""

    text: str
    events: tuple[Event, ...]
    state: Mapping[str, Any]
    finished: bool


def _diff(before: Mapping[str, Any], after: Mapping[str, Any]) -> tuple[Event, ...]:
    """Events from a state transition, never from prose."""
    events: list[Event] = []
    if after.get("turns") == before.get("turns"):
        # The engine only increments `turns` for a known verb, so this is a rejection.
        return (Event("rejected", {}),)
    if after.get("location") != before.get("location"):
        events.append(Event("location_changed", {
            "from": before.get("location", ""), "to": after.get("location", ""),
        }))
    for clue in after.get("clues", []):
        if clue not in before.get("clues", []):
            events.append(Event("clue_gained", {"clue": clue}))
    for flag in after.get("flags", []):
        if flag not in before.get("flags", []):
            events.append(Event("flag_gained", {"flag": flag}))
    if after.get("hp") != before.get("hp"):
        events.append(Event("hp_changed", {
            "from": before.get("hp"), "to": after.get("hp"),
        }))
    if after.get("ending") and after.get("ending") != before.get("ending"):
        events.append(Event("ending_reached", {"ending": after["ending"]}))
    events.append(Event("turn", {"number": after.get("turns", 0)}))
    return tuple(events)


class CampaignSession:
    """The session an adapter drives. One engine, one state document, one event stream."""

    def __init__(self, engine: CampaignEngine | None = None) -> None:
        self._engine = engine or CampaignEngine()

    @property
    def engine(self) -> CampaignEngine:
        return self._engine

    @property
    def state(self) -> dict[str, Any]:
        return self._engine.to_dict()

    @property
    def finished(self) -> bool:
        return bool(self.state.get("ending"))

    def execute(self, action: Action) -> ActionResult:
        before = self.state
        text = self._engine.command(action.text)
        after = self.state
        return ActionResult(text=text, events=_diff(before, after), state=after,
                            finished=bool(after.get("ending")))

    # ---- persistence: the same document CampaignEngine already version-checks ----------
    def to_dict(self) -> dict[str, Any]:
        return self.state

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CampaignSession:
        return cls(CampaignEngine.from_dict(dict(data)))

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
                              encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> CampaignSession:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
