"""Read one paradigm event seed as the four UN parties read it (issues #469, #470).

Why this module exists. Issue #469 asks for a *mechanism*, not a mood: the same in-world event,
read four ways, with each reading stating what the faction believes is happening, what it counts
as evidence, whom it trusts, what it does, and how it justifies itself — and with the epistemic
kind of the reading named rather than blurred. Issue #470 supplies the four parties. This module
is the read-only reader that turns one seed card into those four readings.

What it deliberately is not. It carries **no rules**: no probability, threshold, difficulty, cost,
rate, cap, clock, seat count or effect, and no scalar "influence" (``docs/design/NOOPUNK_GLOBAL.md``
section 7: the six quantities are not interchangeable and are not one number). It resolves nothing.
An unknown event id raises :class:`KeyError` and an unknown quantity name is *reported* by
:func:`unknown_quantity_names` rather than invented, because the alternative — quietly answering a
question the author has not — is the failure both issues warn about.

The vocabulary. Two questions are kept apart. How well established an *event* is uses the
event-level statuses already recorded in the repository (observed, corroborated, contested,
alleged, unknown). What kind of claim a faction's *reading* is uses issue #469's five:
demonstrated in-world fact, credible but incomplete evidence, propaganda, delusion, open mystery.
The reading statuses are declared in the data file's ``reading_vocabulary`` and re-exported here as
:data:`READING_STATUSES`; nothing in this module assigns one.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .quantities import QUANTITY_IDS

__all__ = [
    "DATA_PATH",
    "ROSTER_PATH",
    "READING_STATUSES",
    "SEEDS_FORMAT",
    "FactionReading",
    "event_ids",
    "load_event_seeds",
    "load_un_parliamentary_parties",
    "missing_readings",
    "quantity_profile",
    "reading_for",
    "reading_statuses",
    "readings_for",
    "unknown_quantity_names",
    "unknown_reading_statuses",
]

DATA_PATH = Path(__file__).with_name("data") / "paradigm_event_seeds.json"
ROSTER_PATH = Path(__file__).with_name("data") / "global_factions.json"

#: The format tag the shipped seed file declares. A different tag is refused, not guessed at.
SEEDS_FORMAT = "noopunk.strategy_game.paradigm_event_seeds"

#: Issue #469's five, in the issue's own order. Transcribed, not extended: a sixth kind of claim is
#: the author's to declare, and :func:`unknown_reading_statuses` reports one rather than accepting it.
READING_STATUSES: tuple[str, ...] = (
    "demonstrated_in_world_fact",
    "credible_incomplete_evidence",
    "propaganda",
    "delusion",
    "open_mystery",
)

#: The reading fields this reader knows how to expose. The data file may carry more (it carries
#: ``basis`` and sometimes ``epistemic_note``); unknown author fields are kept in ``detail``.
_READING_FIELDS = ("reads", "counts_as_evidence", "trusts", "does", "justifies_with")


@dataclass(frozen=True)
class FactionReading:
    """One faction's reading of one event. Descriptive text only — no value, weight or effect."""

    faction: str
    reads: str
    counts_as_evidence: str
    trusts: str
    does: str
    justifies_with: str
    epistemic_status: str
    detail: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = {"faction": self.faction, "epistemic_status": self.epistemic_status}
        payload.update({field: getattr(self, field) for field in _READING_FIELDS})
        payload.update(dict(self.detail))
        return payload


def _read_json(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as stream:
        payload = json.load(stream)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} does not hold a JSON object")
    return payload


def load_event_seeds(path: str | Path | None = None) -> dict[str, Any]:
    """The seed document, with the structure this reader depends on checked.

    Raises :class:`ValueError` naming the offending card rather than skipping it: a malformed seed
    must fail loudly, not read as an empty reading.
    """
    payload = _read_json(path or DATA_PATH)
    if payload.get("format") != SEEDS_FORMAT:
        raise ValueError(
            f"unsupported event-seed format: {payload.get('format')!r}; expected {SEEDS_FORMAT!r}"
        )
    cards = payload.get("cards")
    if not isinstance(cards, list):
        raise ValueError("cards must be an array")
    seen: set[str] = set()
    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            raise ValueError(f"cards[{index}] is not an object")
        identifier = card.get("id")
        if not isinstance(identifier, str) or not identifier:
            raise ValueError(f"cards[{index}] has no id")
        if identifier in seen:
            raise ValueError(f"duplicate card id {identifier!r}")
        seen.add(identifier)
        block = card.get("faction_readings")
        if not isinstance(block, dict):
            raise ValueError(f"cards[{index}] ({identifier}) has no faction_readings block")
        readings = block.get("readings")
        if not isinstance(readings, list) or not readings:
            raise ValueError(f"cards[{index}] ({identifier}) has no readings")
        factions: list[str] = []
        for position, reading in enumerate(readings):
            if not isinstance(reading, dict):
                raise ValueError(f"cards[{index}] ({identifier}) readings[{position}] is not an object")
            faction = reading.get("faction")
            if not isinstance(faction, str) or not faction:
                raise ValueError(f"cards[{index}] ({identifier}) readings[{position}] names no faction")
            factions.append(faction)
        if len(set(factions)) != len(factions):
            raise ValueError(f"cards[{index}] ({identifier}) reads one faction twice")
    return payload


def event_ids(path: str | Path | None = None) -> tuple[str, ...]:
    """Every seed id in document order."""
    return tuple(card["id"] for card in load_event_seeds(path)["cards"])


def _card(event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    for card in payload["cards"]:
        if card["id"] == event_id:
            return card
    raise KeyError(event_id)


def readings_for(event_id: str, *, path: str | Path | None = None) -> tuple[FactionReading, ...]:
    """The seed's faction readings, in the document's own order.

    An event the document does not carry raises :class:`KeyError`: nothing is synthesised for an
    event nobody authored.
    """
    card = _card(event_id, load_event_seeds(path))
    readings = []
    for entry in card["faction_readings"]["readings"]:
        detail = {
            key: value for key, value in entry.items()
            if key not in _READING_FIELDS and key not in ("faction", "epistemic_status")
        }
        readings.append(
            FactionReading(
                faction=entry["faction"],
                epistemic_status=entry["epistemic_status"],
                detail=detail,
                **{field: entry.get(field) for field in _READING_FIELDS},
            )
        )
    return tuple(readings)


def reading_for(event_id: str, faction_id: str, *, path: str | Path | None = None) -> FactionReading:
    """One faction's reading of one event, or :class:`KeyError` naming both."""
    for reading in readings_for(event_id, path=path):
        if reading.faction == faction_id:
            return reading
    raise KeyError(f"{faction_id!r} reads no {event_id!r}")


def reading_statuses(path: str | Path | None = None) -> tuple[str, ...]:
    """The reading statuses the shipped document declares, in its own order."""
    declared = load_event_seeds(path)["reading_vocabulary"]["reading_statuses"]
    return tuple(entry["id"] for entry in declared)


def unknown_reading_statuses(payload: dict[str, Any] | None = None) -> tuple[str, ...]:
    """Reading statuses used in ``payload`` that this module does not know, in card order.

    Reports instead of raising, so a document can be audited without being rejected wholesale.
    """
    document = payload if payload is not None else load_event_seeds()
    known = set(READING_STATUSES) | set(status for status in reading_statuses())
    unknown: list[str] = []
    for card in document["cards"]:
        for reading in card["faction_readings"]["readings"]:
            status = reading.get("epistemic_status")
            if status not in known and status not in unknown:
                unknown.append(status)
    return tuple(unknown)


def missing_readings(factions: Iterable[str], *, payload: dict[str, Any] | None = None) -> tuple[str, ...]:
    """``"<event>/<faction>"`` for every pair the document does not read.

    A gap is reported, never filled: the alternative would be to put words in a faction's mouth.
    """
    document = payload if payload is not None else load_event_seeds()
    wanted = tuple(factions)
    gaps: list[str] = []
    for card in document["cards"]:
        present = {reading["faction"] for reading in card["faction_readings"]["readings"]}
        for faction in wanted:
            if faction not in present:
                gaps.append(f"{card['id']}/{faction}")
    return tuple(gaps)


def load_un_parliamentary_parties(path: str | Path | None = None) -> tuple[dict[str, Any], ...]:
    """The four UN parliamentary parties as ``strategy_game/data/global_factions.json`` records them.

    A missing key reads as an empty tuple — the register may legitimately not be present in a
    future revision — rather than raising.
    """
    payload = _read_json(path or ROSTER_PATH)
    block = payload.get("un_parliamentary_parties") or {}
    parties = block.get("parties") or ()
    return tuple(entry for entry in parties if isinstance(entry, dict))


def quantity_profile(faction_id: str, *, path: str | Path | None = None) -> dict[str, Any]:
    """``{quantity id: note}`` for one party, over the six quantities and no others.

    The keys come from :mod:`strategy_game.quantities`, so a profile can name only one of the six
    that ``docs/design/NOOPUNK_GLOBAL.md`` section 7 distinguishes. Names this module does not know
    are not returned here; :func:`unknown_quantity_names` reports them.
    """
    for party in load_un_parliamentary_parties(path):
        if party.get("id") == faction_id:
            profile = party.get("six_quantities") or {}
            return {name: (profile[name] or {}).get("note") for name in QUANTITY_IDS if name in profile}
    raise KeyError(faction_id)


def unknown_quantity_names(faction_id: str, *, path: str | Path | None = None) -> tuple[str, ...]:
    """Names in one party's profile that are not among section 7's six, in the profile's order."""
    for party in load_un_parliamentary_parties(path):
        if party.get("id") == faction_id:
            profile = party.get("six_quantities") or {}
            return tuple(name for name in profile if name not in QUANTITY_IDS)
    raise KeyError(faction_id)
