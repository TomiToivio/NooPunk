"""Ukweli leader roster: the dynasty, the leader template and the declared blanks (issue #326).

Issue #326 asks for the Ukweli leader/NPC roster: Sir Mars Eldrich as a present-day flagship NPC,
Sir Uranus and Sir Mercury as **historical** people, a concise template for the twelve faction leader
seats, and a handful of consequential independent NPCs -- *"without inventing unrequested individuals
as canon."*

What this module is
-------------------

A stdlib-only reader and validator for ``data/ukweli_leaders.json``. It enforces the constraints the
issue and the surrounding canon actually state, so a later pass cannot quietly break them:

* **The dynasty's eras hold.** Uranus and Mercury are ``historical`` and invocable, never agentic:
  they generate events and consume no action slot. Only a ``present`` person may act.
* **Sir Mars Eldrich is referenced, not restated.** He already exists as a landed canonical character
  card, so the roster carries a ``card_ref`` to it and this module checks that reference resolves.
* **No invented individuals.** The twelve seats and the independent-NPC slot are *declared blanks*:
  this module fails if a person is filled in without the author having specified them.
* **No second action economy and no new statistic.** Four seats per faction, four existing portfolios,
  no numeric field anywhere in the roster.

What this module is not
-----------------------

Not an engine, not a rule and not a roster. It performs no resolution, grants no action, and decides
nothing about who any leader is. It defines no canon: filling a ``TODO`` is author work, and every
person this roster names was already named by the repository before it. ``RULEBOOK.md`` still says
NO RULES APPROVED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import json

__all__ = [
    "ROSTER_FORMAT",
    "DATA_PATH",
    "ERAS",
    "PORTFOLIOS",
    "EXTERNAL_REFS",
    "RosterError",
    "Person",
    "Seat",
    "LeaderRoster",
    "roster_from_dict",
    "load_ukweli_leaders",
]

#: Declared document type. A differently-typed file is not a roster.
ROSTER_FORMAT = "noopunk.strategy_game.ukweli_leaders"

#: The packaged roster, next to the other strategy-game data.
DATA_PATH = Path(__file__).with_name("data") / "ukweli_leaders.json"

#: The existing leader records this roster annotates. Never duplicated -- only referenced.
LOCAL_DATA_PATH = Path(__file__).with_name("data") / "ukweli_local.json"

#: The landed canonical character cards. Sir Mars Eldrich lives here, not in this roster.
CARD_DATA_PATH = Path(__file__).with_name("data") / "character_cards.json"

#: A person is either dead and invocable, or present and agentic. There is no third kind.
ERAS: tuple[str, ...] = ("historical", "present")

#: The four portfolios from #323, as the existing leader records already use them.
PORTFOLIOS: tuple[str, ...] = ("politics", "networks", "operations", "research")

#: Faction ids the roster's edges may name, matching data/ukweli_local.json.
FACTION_IDS: tuple[str, ...] = ("cpu", "uip", "ulp")

#: Non-person, non-faction endpoints an edge may name (media, offices and other collectives).
EXTERNAL_REFS: tuple[str, ...] = ("sympathetic_media", "eldrich_corporation")

#: Fields a roster entry may carry. Anything numeric would be a statistic, so none is allowed.
_NUMERIC_FORBIDDEN = ("score", "strength", "rating", "influence", "power", "hearts", "track")


class RosterError(ValueError):
    """Raised when a roster document cannot be read as a roster."""


def _strings(value: Any) -> tuple[str, ...]:
    """Coerce a JSON list of scalars into a tuple of strings; never raise on shape."""
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(item) for item in value)


@dataclass
class Person:
    """A dynasty member. ``era`` decides whether they may act at all."""

    person_ref: str
    display_name: str
    era: str = "historical"
    generation: int = 0
    role: str = ""
    canon_status: str = ""
    card_ref: str = ""
    holds_council_seat: bool = False
    keeps: str = ""
    must_not_assert: str = ""
    evidence_classes: tuple[str, ...] = ()
    event_hooks: tuple[str, ...] = ()
    canon_invariants: tuple[str, ...] = ()
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def is_agentic(self) -> bool:
        """Only a present person may hold a council seat or take a move."""
        return self.era == "present"

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {**self.detail}
        data.update(
            person_ref=self.person_ref,
            display_name=self.display_name,
            era=self.era,
            generation=self.generation,
            role=self.role,
            canon_status=self.canon_status,
            card_ref=self.card_ref,
            holds_council_seat=self.holds_council_seat,
            keeps=self.keeps,
            must_not_assert=self.must_not_assert,
            evidence_classes=list(self.evidence_classes),
            event_hooks=list(self.event_hooks),
            canon_invariants=list(self.canon_invariants),
        )
        return {k: v for k, v in data.items() if v not in ("", (), [], None)}


@dataclass
class Seat:
    """One of the twelve leader seats. A seat is a shape; a person filling it is author work."""

    leader_ref: str
    faction: str
    portfolio: str
    institutional_tie: str = ""
    person: str | None = None
    todo: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def is_filled(self) -> bool:
        return bool(self.person)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {**self.detail}
        data.update(
            leader_ref=self.leader_ref,
            portfolio=self.portfolio,
            institutional_tie=self.institutional_tie,
            person=self.person,
            todo=self.todo,
        )
        return {k: v for k, v in data.items() if v not in ("", None)}


@dataclass
class LeaderRoster:
    """The read roster: dynasty, seats, edges and hooks."""

    format: str = ROSTER_FORMAT
    status: str = ""
    sources: tuple[str, ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)
    naming_note: dict[str, Any] = field(default_factory=dict)
    eras: tuple[dict[str, Any], ...] = ()
    people: dict[str, Person] = field(default_factory=dict)
    leader_template: dict[str, Any] = field(default_factory=dict)
    portfolios: tuple[str, ...] = ()
    seats: tuple[Seat, ...] = ()
    independent_npcs: dict[str, Any] = field(default_factory=dict)
    edges: tuple[dict[str, Any], ...] = ()
    hooks: tuple[dict[str, Any], ...] = ()
    cautions: tuple[str, ...] = ()
    detail: dict[str, Any] = field(default_factory=dict)

    # -- lookups -----------------------------------------------------------------
    def person(self, person_ref: str) -> Person | None:
        return self.people.get(person_ref)

    def historical(self) -> tuple[Person, ...]:
        return tuple(p for p in self.people.values() if p.era == "historical")

    def seats_for(self, faction: str) -> tuple[Seat, ...]:
        return tuple(s for s in self.seats if s.faction == faction)

    def unfilled_seats(self) -> tuple[Seat, ...]:
        return tuple(s for s in self.seats if not s.is_filled)

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": self.format,
            "status": self.status,
            "sources": list(self.sources),
            "provenance": self.provenance,
            "naming_note": self.naming_note,
            "eras": [dict(e) for e in self.eras],
            "dynasty": [p.to_dict() for p in self.people.values()],
            "leader_template": self.leader_template,
            "portfolios": {"ids": list(self.portfolios)},
            "seats": {f: [s.to_dict() for s in self.seats_for(f)] for f in FACTION_IDS},
            "independent_npcs": self.independent_npcs,
            "relationships": {"edges": [dict(e) for e in self.edges]},
            "event_hooks": {"hooks": [dict(h) for h in self.hooks]},
            "cautions": list(self.cautions),
        }

    # -- validation --------------------------------------------------------------
    def off_vocabulary(self) -> tuple[str, ...]:
        """Roster-internal problems, checkable without the rest of the scaffold."""
        problems: list[str] = []
        if self.format != ROSTER_FORMAT:
            problems.append(f"format is {self.format!r}, expected {ROSTER_FORMAT!r}")

        for person in self.people.values():
            if person.era not in ERAS:
                problems.append(f"{person.person_ref}: era {person.era!r} not in {ERAS}")
            if person.era == "historical" and person.holds_council_seat:
                problems.append(f"{person.person_ref}: historical person may not hold a council seat")
            if person.era != "present" and person.card_ref:
                problems.append(f"{person.person_ref}: only a present person has a live character card")
            for key in person.detail:
                if any(bad in key for bad in _NUMERIC_FORBIDDEN):
                    problems.append(f"{person.person_ref}: numeric-looking field {key!r}")

        for seat in self.seats:
            if seat.faction not in FACTION_IDS:
                problems.append(f"{seat.leader_ref}: faction {seat.faction!r} unknown")
            if seat.portfolio not in PORTFOLIOS:
                problems.append(f"{seat.leader_ref}: portfolio {seat.portfolio!r} not in {PORTFOLIOS}")
            for key in seat.detail:
                if any(bad in key for bad in _NUMERIC_FORBIDDEN):
                    problems.append(f"{seat.leader_ref}: numeric-looking field {key!r}")

        hooks = {h.get("id") for h in self.hooks}
        for person in self.people.values():
            for hook in person.event_hooks:
                if hook not in hooks:
                    problems.append(f"{person.person_ref}: hook {hook!r} is not declared")

        for hook in self.hooks:
            if hook.get("drawn_from") and hook["drawn_from"] not in self.people:
                problems.append(f"hook {hook.get('id')!r}: drawn_from {hook['drawn_from']!r} unknown")

        known = set(self.people) | set(FACTION_IDS) | set(EXTERNAL_REFS)
        for edge in self.edges:
            for side in ("a", "b"):
                if edge.get(side) not in known:
                    problems.append(f"edge {edge.get('a')!r}->{edge.get('b')!r}: {side}={edge.get(side)!r} unknown")

        for faction in FACTION_IDS:
            if len(self.seats_for(faction)) != 4:
                problems.append(f"{faction}: expected four seats, found {len(self.seats_for(faction))}")

        return tuple(problems)

    def undeclared_people(self) -> tuple[str, ...]:
        """Names invented for a seat or an NPC without the author having specified them.

        The issue forbids inventing individuals as canon, so a filled seat whose ``person`` was not
        authored is a defect rather than an enrichment.
        """
        return tuple(s.leader_ref for s in self.seats if s.is_filled)


def _person_from_dict(record: dict[str, Any]) -> Person:
    known = {
        "person_ref", "display_name", "era", "generation", "role", "canon_status", "card_ref",
        "holds_council_seat", "what_the_scenario_keeps", "what_must_not_be_asserted",
        "evidence_classes", "event_hooks", "canon_invariants", "seat_note",
    }
    return Person(
        person_ref=str(record.get("person_ref", "")),
        display_name=str(record.get("display_name", "")),
        era=str(record.get("era", "historical")),
        generation=int(record.get("generation", 0) or 0),
        role=str(record.get("role", "")),
        canon_status=str(record.get("canon_status", "")),
        card_ref=str(record.get("card_ref", "")),
        holds_council_seat=bool(record.get("holds_council_seat", False)),
        keeps=str(record.get("what_the_scenario_keeps", "")),
        must_not_assert=str(record.get("what_must_not_be_asserted", "")),
        evidence_classes=_strings(record.get("evidence_classes")),
        event_hooks=_strings(record.get("event_hooks")),
        canon_invariants=_strings(record.get("canon_invariants")),
        detail={k: v for k, v in record.items() if k not in known},
    )


def roster_from_dict(data: dict[str, Any]) -> LeaderRoster:
    """Build a :class:`LeaderRoster` from an already-parsed document."""
    if not isinstance(data, dict):
        raise RosterError("roster document must be an object")

    people = {}
    for record in data.get("dynasty", []) or []:
        person = _person_from_dict(record)
        if not person.person_ref:
            raise RosterError("dynasty entry without person_ref")
        people[person.person_ref] = person

    seats: list[Seat] = []
    # ``seats`` carries a prose ``note`` alongside the per-faction lists, so only list values are
    # factions; skipping non-lists here would also hide an unknown faction, so nothing is dropped
    # silently by the validator below.
    for faction, records in (data.get("seats", {}) or {}).items():
        if faction == "note" or not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict):
                raise RosterError(f"seat entry under {faction!r} is not an object")
            known = {"leader_ref", "portfolio", "institutional_tie", "person", "todo"}
            seats.append(
                Seat(
                    leader_ref=str(record.get("leader_ref", "")),
                    faction=str(faction),
                    portfolio=str(record.get("portfolio", "")),
                    institutional_tie=str(record.get("institutional_tie", "")),
                    person=record.get("person"),
                    todo=str(record.get("todo", "")),
                    detail={k: v for k, v in record.items() if k not in known},
                )
            )

    independent = data.get("independent_npcs", {}) or {}
    hooks = (data.get("event_hooks", {}) or {}).get("hooks", []) or []
    edges = (data.get("relationships", {}) or {}).get("edges", []) or []

    return LeaderRoster(
        format=str(data.get("format", "")),
        status=str(data.get("status", "")),
        sources=_strings(data.get("sources")),
        provenance=data.get("provenance", {}) or {},
        naming_note=data.get("naming_note", {}) or {},
        eras=tuple(data.get("eras", []) or []),
        people=people,
        leader_template=data.get("leader_template", {}) or {},
        portfolios=_strings((data.get("portfolios", {}) or {}).get("ids")),
        seats=tuple(seats),
        independent_npcs=independent if isinstance(independent, dict) else {},
        edges=tuple(edges),
        hooks=tuple(hooks),
        cautions=_strings(data.get("cautions")),
        detail={},
    )


def load_ukweli_leaders(path: Path | str | None = None) -> LeaderRoster:
    """Read and validate the packaged roster.

    The declared ``format`` is checked here, so a differently-typed file is refused rather than
    half-read.
    """
    target = Path(path) if path is not None else DATA_PATH
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:  # pragma: no cover - packaging error
        raise RosterError(f"roster data not found at {target}") from exc
    except json.JSONDecodeError as exc:
        raise RosterError(f"roster data is not valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise RosterError(f"{target} must contain a JSON object, got {type(data).__name__}")
    if data.get("format") != ROSTER_FORMAT:
        raise RosterError(f"{target} declares format {data.get('format')!r}, expected {ROSTER_FORMAT!r}")
    return roster_from_dict(data)


def load_local_leaders() -> dict[str, dict[str, Any]]:
    """The existing leader records, keyed by id -- read-only, for reference checks."""
    data = json.loads(LOCAL_DATA_PATH.read_text(encoding="utf-8"))
    return {str(rec.get("id")): rec for rec in data.get("leaders", [])}


def load_card_identifiers() -> set[str]:
    """The identifiers of the landed canonical character cards."""
    data = json.loads(CARD_DATA_PATH.read_text(encoding="utf-8"))
    return {str(entry.get("identifier")) for entry in data.get("entries", [])}
