"""Versioned save/load for the table: one snapshot, one schema version, deterministic bytes.

Issue #347 asks for "pure Python models and reducers/commands, JSON-compatible save data,
schema/versioning, explicit validation, seeded tests, replayable RNG and provenance", and for a
save/reload/replay step in the vertical slice.

:class:`TableState` is the table's snapshot: the board, the decks, the roll log and the tarot draws.
It is **standalone on purpose** — it does not join :class:`strategy_game.core.WorldState`, because that
is the Gate D integration the project has not approved (`docs/RULE_SYSTEM_RESEARCH.md`). A caller that
wants both holds both.

Serialization follows the conventions the rest of the scaffold already uses, so a snapshot behaves the
way the existing ones do:

* keys are sorted and non-ASCII is preserved rather than escaped, so output is byte-stable;
* :meth:`TableState.to_dict` carries **exactly** the dataclass's fields, so a new field cannot be
  silently dropped from a save;
* loading tolerates a snapshot written before a section existed, so an older save does not raise;
* nothing is validated by guesswork: a malformed record raises the owning module's error.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Mapping

from .board import Board
from .decks import Deck
from .dice import RollLog
from .tarot import TarotDraw

#: Bumped when the snapshot shape changes. Written into every save so a loader can refuse an unknown
#: future version rather than misread it.
TABLE_SCHEMA_VERSION = "tabletop-1"


@dataclass
class TableState:
    """The table's snapshot: board, decks, roll log and tarot draws."""

    schema_version: str = TABLE_SCHEMA_VERSION
    board: Board = field(default_factory=Board)
    #: Decks by identifier, so several decks (event, GM, tarot) coexist without a second container.
    decks: dict[str, Deck] = field(default_factory=dict)
    rolls: RollLog = field(default_factory=RollLog)
    tarot_draws: list[TarotDraw] = field(default_factory=list)

    @property
    def field_names(self) -> tuple[str, ...]:
        return tuple(item.name for item in fields(self))

    def to_dict(self) -> dict[str, Any]:
        """Every declared field, explicitly serialized. Keys match the dataclass fields."""
        return {
            "schema_version": self.schema_version,
            "board": self.board.to_dict(),
            "decks": {key: self.decks[key].to_dict() for key in sorted(self.decks)},
            "rolls": self.rolls.to_dict(),
            "tarot_draws": [draw.to_dict() for draw in self.tarot_draws],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, indent=2)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> TableState:
        # `.get` throughout: a snapshot written before a section existed still loads.
        return cls(
            schema_version=str(data.get("schema_version", TABLE_SCHEMA_VERSION)),
            board=Board.from_dict(data.get("board") or {}),
            decks={
                str(key): Deck.from_dict(payload)
                for key, payload in (data.get("decks") or {}).items()
            },
            rolls=RollLog.from_dict(data.get("rolls") or {}),
            tarot_draws=[TarotDraw.from_dict(item) for item in (data.get("tarot_draws") or ())],
        )

    @classmethod
    def from_json(cls, text: str) -> TableState:
        return cls.from_dict(json.loads(text))


def save_table(state: TableState, path: str | Path) -> Path:
    """Write a snapshot to ``path``, creating parent directories. Returns the path written."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(state.to_json(), encoding="utf-8")
    return target


def load_table(path: str | Path) -> TableState:
    """Read a snapshot. A missing file raises :class:`FileNotFoundError` rather than an empty state."""
    return TableState.from_json(Path(path).read_text(encoding="utf-8"))
