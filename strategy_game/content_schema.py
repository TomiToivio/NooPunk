"""The card-kind registry and the data-only content contract (issue #347, items 7 and 9).

Two acceptance items of #347 are asserted here rather than promised:

* item 7 — *"Add data-driven example cards: at least one each character, faction, organization,
  place, research, event, mission, relationship, ideology/signifier and tarot placeholder."*
* item 9 — *"Document modding/content authoring schema; test a new foreign node and new card can be
  added from data alone."*

This module declares where each kind's examples live and counts them from the shipped data, so
"at least one each" is checkable rather than asserted. It defines no rule, no effect and no canon:
each kind is data, and the module that already owns a kind is the module that validates it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).with_name("data")

#: Tokens this module must never contain: a kind registry that grew a mechanic would be a rule system
#: wearing a data file's clothes.
FORBIDDEN_TOKENS = ("modifier", "bonus", "damage", "threshold", "hit points")


@dataclass(frozen=True)
class CardKind:
    """One of the ten example kinds, and where its data lives."""

    identifier: str
    label: str
    data_file: str
    records_path: tuple[str, ...]
    owner: str | None = None
    require: tuple[str, str] | None = None
    nested: str | None = None
    note: str = ""


CARD_KINDS: tuple[CardKind, ...] = (
    CardKind("character", "Character", "character_cards.json", ("entries",), "strategy_game.characters"),
    CardKind("faction", "Faction", "global_factions.json", ("factions",), None),
    CardKind(
        "organization", "Organization", "faction_cards.json", ("cards",), "strategy_game.faction_cards",
        require=("card_type", "organization"), note="faction-card layer; effects deliberately unenforced",
    ),
    CardKind("place", "Place", "ukweli_local.json", ("locations",), None),
    CardKind(
        "research", "Research", "faction_cards.json", ("cards",), "strategy_game.faction_cards",
        require=("card_type", "research"),
    ),
    CardKind("event", "Event", "global_factions.json", ("event_card_seeds",), None),
    CardKind(
        "mission", "Mission", "council.json", ("worked_example", "missions"), "strategy_game.council",
        note="the shipped worked turn; placeholder ids by design",
    ),
    CardKind("relationship", "Relationship", "ukweli_local.json", ("relationships",), None),
    CardKind(
        "ideology_signifier", "Ideology / signifier", "global_factions.json", ("factions",), None,
        nested="core_signifiers",
    ),
    CardKind(
        "tarot_placeholder", "Tarot (placeholder)", "tarot_placeholder.json", ("cards",),
        "strategy_game.tabletop.tarot", note="a placeholder deck, not a designed one",
    ),
)

KIND_IDS: tuple[str, ...] = tuple(kind.identifier for kind in CARD_KINDS)


def _load_json(data_file: str, *, base: Path | None = None) -> Any:
    path = (base or DATA_DIR) / data_file
    return json.loads(path.read_text(encoding="utf-8"))


def _records(kind: CardKind, *, base: Path | None = None) -> list[Any]:
    """The example records for a kind. A seed may legitimately be a bare string, not a mapping."""
    data: Any = _load_json(kind.data_file, base=base)
    for step in kind.records_path:
        data = data[step] if not isinstance(data, list) else [
            row for row in data if isinstance(row, dict) and step in row
        ]
    rows = list(data)
    if kind.require is not None:
        field, value = kind.require
        rows = [row for row in rows if isinstance(row, dict) and row.get(field) == value]
    if kind.nested is not None:
        rows = [row for row in rows if isinstance(row, dict) and row.get(kind.nested)]
    return rows


def kind_examples(*, base: Path | None = None) -> dict[str, int]:
    """How many shipped examples of each kind exist. Zero means the item-7 criterion is unmet."""
    counts = {}
    for kind in CARD_KINDS:
        rows = _records(kind, base=base)
        counts[kind.identifier] = sum(
            len((row.get(kind.nested) or []) if isinstance(row, dict) else []) if kind.nested else 1
            for row in rows
        )
    return counts


def missing_kinds(*, base: Path | None = None) -> tuple[str, ...]:
    """The kinds with no shipped example, in the registry's own order."""
    counts = kind_examples(base=base)
    return tuple(kind for kind in KIND_IDS if counts.get(kind, 0) <= 0)


def validate_registry() -> tuple[str, ...]:
    """Structural problems with this registry itself; empty means it is well formed."""
    problems: list[str] = []
    if len(KIND_IDS) != len(set(KIND_IDS)):
        problems.append("a kind identifier appears more than once")
    if set(KIND_IDS) != {
        "character", "faction", "organization", "place", "research", "event", "mission",
        "relationship", "ideology_signifier", "tarot_placeholder",
    }:
        problems.append("the registry does not carry exactly the ten kinds issue #347 names")
    for kind in CARD_KINDS:
        if not (DATA_DIR / kind.data_file).exists():
            problems.append(f"{kind.identifier}: data file {kind.data_file} is missing")
    source = Path(__file__).read_text(encoding="utf-8")
    code = source.split('"""', 2)[-1]
    # the constant above names these on purpose, so its own definition is excluded from the scan
    lines = code.splitlines(keepends=True)
    scanning = True
    scannable: list[str] = []
    for line in lines:
        if "FORBIDDEN_TOKENS" in line:
            scanning = False
        if scanning:
            scannable.append(line)
        if not scanning and line.strip() == ")":
            scanning = True
    for banned in FORBIDDEN_TOKENS:
        if banned in "".join(scannable):
            problems.append(f"the registry contains the mechanic token {banned!r}")
    return tuple(problems)
