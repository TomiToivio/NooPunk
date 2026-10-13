"""The local-to-global link as structure (issue #322): a tendency, never a roster count.

Issue #322 asks the MVP to keep **global shocks and local effects** while refusing to simulate
international politics, and it asks for a link between the local factions and the wider global layer.
The repository has an unresolved question sitting exactly where that link lands: **three global
rosters are unreconciled, four / seven / eleven** (``docs/design/NOOPUNK_GLOBAL.md`` section 6B.3),
and a design that binds to "a handful of factions" before that is settled encodes an arbitrary number.

So this module does the opposite of binding: it declares which global **current** each local party
*TENDS* toward, with ``membership`` false and ``declared_not_enforced`` false, and it **asserts no
count at all**. A current is a name; a roster size is an author ruling, and this layer never needs it
to say "the CPU tends toward the establishment-pragmatic current".

Two separations the module keeps honest:

* **A tendency is not a membership.** Outside networks recruit individuals inside mainstream parties,
  civil services and corporations without the party itself becoming them, so a link may not assert
  belonging.
* **A link names WHICH of the six quantities it plausibly touches**, read from
  :mod:`strategy_game.quantities` rather than restated. *Which* quantities a tendency touches is a
  design claim recorded as data - ``declared_not_enforced`` is false everywhere, so no code applies it
  and no scalar "influence" is computed anywhere.

Not approved rules. ``strategy_game/RULEBOOK.md`` still says **NO RULES APPROVED**;
``numeric_scale_approved`` stays false; no affinity is computed, no event is drawn and no turn is
resolved. It records names, checks references, and leaves the roster-count question exactly where it
found it: open, and recorded with a reason.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .leaders import FACTION_IDS
from .quantities import QUANTITY_IDS

__all__ = [
    "LINK_FORMAT",
    "LINK_VERSION",
    "DATA_PATH",
    "LOCAL_PARTY_IDS",
    "LocalGlobalLink",
    "LinkRecord",
    "LinkError",
    "link_from_dict",
    "load_local_global_link",
]

#: Declared document type. A differently-typed file is not this record.
LINK_FORMAT = "noopunk.strategy_game.local_global_link"

#: Bumped when the record's shape changes incompatibly.
LINK_VERSION = 1

#: The packaged record, next to the other strategy-game data.
DATA_PATH = Path(__file__).with_name("data") / "local_global_link.json"

#: The local parties a link may name. Consumed from the leader roster, which already declares the
#: faction ids the board uses, rather than restating a second copy of them.
LOCAL_PARTY_IDS: tuple[str, ...] = FACTION_IDS

#: Key fragments that would bind the link to a global roster size. None may appear on a link.
_ROSTER_TOKENS: tuple[str, ...] = ("roster_count", "roster_size", "faction_count", "party_count")

#: Numeric-shaped field fragments a record entry may not carry.
_NUMERIC_FORBIDDEN: tuple[str, ...] = (
    "score",
    "strength",
    "rating",
    "threshold",
    "weight",
    "probability",
    "magnitude",
    "affinity_value",
)


class LinkError(ValueError):
    """Raised when the link record cannot be read as this record."""


def _strings(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(item) for item in value)


@dataclass(frozen=True)
class LinkRecord:
    """One local party's tendency toward one global current. A name, not a membership or a score."""

    local_party: str
    global_current: str
    membership: bool = False
    declared_not_enforced: bool = False
    basis: str = ""
    quantities_touched: tuple[str, ...] = ()
    cannot_move: tuple[str, ...] = ()
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def is_tendency(self) -> bool:
        """True when the link claims no belonging. A membership claim would be a modelling error."""
        return not self.membership

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "local_party": self.local_party,
            "global_current": self.global_current,
            "membership": self.membership,
            "declared_not_enforced": self.declared_not_enforced,
            "basis": self.basis,
            "quantities_touched": list(self.quantities_touched),
            "cannot_move": list(self.cannot_move),
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class LocalGlobalLink:
    """The read record: the tendencies, the shock intake rule and the open questions."""

    format: str = LINK_FORMAT
    version: int = LINK_VERSION
    status: str = ""
    numeric_scale_approved: bool = False
    roster_count_asserted: bool = False
    sources: tuple[str, ...] = ()
    link_rule: str = ""
    quantity_rule: str = ""
    links: tuple[LinkRecord, ...] = ()
    shock_intake: dict[str, Any] = field(default_factory=dict)
    pending_decisions: tuple[dict[str, Any], ...] = ()
    detail: dict[str, Any] = field(default_factory=dict)

    # -- readings ------------------------------------------------------------
    def for_party(self, party: str) -> tuple[LinkRecord, ...]:
        return tuple(link for link in self.links if link.local_party == party)

    def currents(self) -> tuple[str, ...]:
        """The distinct currents named, in declaration order. A set of names - never a count."""
        return tuple(dict.fromkeys(link.global_current for link in self.links))

    def quantities_touched(self) -> tuple[str, ...]:
        return tuple(sorted({q for link in self.links for q in link.quantities_touched}))

    def decisions(self) -> tuple[dict[str, Any], ...]:
        return tuple(self.pending_decisions)

    def unresolved_decisions(self) -> tuple[dict[str, Any], ...]:
        return tuple(d for d in self.pending_decisions if not d.get("resolved", False))

    # -- validation ----------------------------------------------------------
    def problems(self) -> tuple[str, ...]:
        """Return the structural problems found; empty means the record is consistent."""
        problems: list[str] = []
        if self.format != LINK_FORMAT:
            problems.append(f"format is {self.format!r}, expected {LINK_FORMAT!r}")
        if self.version != LINK_VERSION:
            problems.append(f"version is {self.version!r}, expected {LINK_VERSION!r}")
        if self.numeric_scale_approved:
            problems.append(
                "numeric_scale_approved is true: no ordered or numeric scale is approved, so the "
                "flag may not be raised by an unauthorised record"
            )
        if self.roster_count_asserted:
            problems.append(
                "roster_count_asserted is true: the 4 / 7 / 11 global-roster question is OPEN, so a "
                "link record may not assert a count"
            )

        seen: set[tuple[str, str]] = set()
        for link in self.links:
            key = (link.local_party, link.global_current)
            if key in seen:
                problems.append(f"{link.local_party} -> {link.global_current}: duplicate link")
            seen.add(key)
            if link.local_party not in LOCAL_PARTY_IDS:
                problems.append(
                    f"{link.local_party!r} is not one of the local party ids {LOCAL_PARTY_IDS}"
                )
            if not link.global_current.strip():
                problems.append(f"{link.local_party}: a link must name a global current")
            if link.membership:
                problems.append(
                    f"{link.local_party} -> {link.global_current}: membership is true; a link is a "
                    "tendency, and membership is never forced by a global network"
                )
            if link.declared_not_enforced:
                problems.append(
                    f"{link.local_party} -> {link.global_current}: declared_not_enforced is true, so "
                    "the record claims an effect is applied - no rule is approved"
                )
            if not link.quantities_touched:
                problems.append(
                    f"{link.local_party} -> {link.global_current}: names no quantity, so the link "
                    "would collapse the six quantities into one generic modifier"
                )
            for quantity in link.quantities_touched:
                if quantity not in QUANTITY_IDS:
                    problems.append(
                        f"{link.local_party} -> {link.global_current}: {quantity!r} is not one of the "
                        f"six quantities {QUANTITY_IDS}"
                    )
            if len(set(link.quantities_touched)) != len(link.quantities_touched):
                problems.append(
                    f"{link.local_party} -> {link.global_current}: quantities_touched repeats an entry"
                )
            for quantity in link.cannot_move:
                if quantity not in QUANTITY_IDS:
                    problems.append(
                        f"{link.local_party} -> {link.global_current}: cannot_move {quantity!r} is not "
                        f"one of the six quantities {QUANTITY_IDS}"
                    )
                if quantity in link.quantities_touched:
                    problems.append(
                        f"{link.local_party} -> {link.global_current}: {quantity!r} is both touched "
                        "and cannot_move"
                    )
            for keyname in link.detail:
                if any(bad in str(keyname) for bad in _ROSTER_TOKENS):
                    problems.append(
                        f"{link.local_party} -> {link.global_current}: {keyname!r} binds the link to "
                        "a global roster size"
                    )
                if any(bad in str(keyname) for bad in _NUMERIC_FORBIDDEN):
                    problems.append(
                        f"{link.local_party} -> {link.global_current}: numeric-looking field {keyname!r}"
                    )

        if not self.links:
            problems.append("no local-to-global link is declared")
        for party in LOCAL_PARTY_IDS:
            if not self.for_party(party):
                problems.append(f"{party}: no link is declared for this local party")

        if not self.shock_intake:
            problems.append("the external-shock intake is not declared")
        else:
            if self.shock_intake.get("simulates_international_politics"):
                problems.append(
                    "shock_intake claims the local layer simulates international politics; issue #322 "
                    "puts that permanently out of scope"
                )
            if not self.shock_intake.get("local_research_is_adoption"):
                problems.append(
                    "shock_intake does not record that local research means adoption of global "
                    "technology rather than global R&D"
                )

        for decision in self.pending_decisions:
            if not str(decision.get("why_not_decided", "")).strip():
                problems.append(f"{decision.get('id')!r}: an open decision must say WHY it is open")

        return tuple(problems)

    # -- serialization -------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "format": self.format,
            "version": self.version,
            "status": self.status,
            "numeric_scale_approved": self.numeric_scale_approved,
            "roster_count_asserted": self.roster_count_asserted,
            "sources": list(self.sources),
            "link_rule": self.link_rule,
            "quantity_rule": self.quantity_rule,
            "links": [link.to_dict() for link in self.links],
            "shock_intake": dict(self.shock_intake),
            "pending_author_decisions": [dict(d) for d in self.pending_decisions],
        }
        payload.update(self.detail)
        return payload


def link_from_dict(data: Mapping[str, Any]) -> LocalGlobalLink:
    """Build a :class:`LocalGlobalLink` from an already-parsed document."""
    if not isinstance(data, Mapping):
        raise LinkError("the link record must be a JSON object")
    links: list[LinkRecord] = []
    for record in data.get("links") or []:
        if not isinstance(record, Mapping):
            raise LinkError("a link entry is not an object")
        known = {
            "local_party",
            "global_current",
            "membership",
            "declared_not_enforced",
            "basis",
            "quantities_touched",
            "cannot_move",
            "note",
        }
        links.append(
            LinkRecord(
                local_party=str(record.get("local_party", "")),
                global_current=str(record.get("global_current", "")),
                membership=bool(record.get("membership", False)),
                declared_not_enforced=bool(record.get("declared_not_enforced", False)),
                basis=str(record.get("basis", "")),
                quantities_touched=_strings(record.get("quantities_touched")),
                cannot_move=_strings(record.get("cannot_move")),
                note=str(record.get("note", "")),
                detail={k: v for k, v in record.items() if k not in known},
            )
        )
    return LocalGlobalLink(
        format=str(data.get("format", "")),
        version=int(data.get("version", 0) or 0),
        status=str(data.get("status", "")),
        numeric_scale_approved=bool(data.get("numeric_scale_approved", False)),
        roster_count_asserted=bool(data.get("roster_count_asserted", False)),
        sources=_strings(data.get("sources")),
        link_rule=str(data.get("link_rule", "")),
        quantity_rule=str(data.get("quantity_rule", "")),
        links=tuple(links),
        shock_intake=dict(data.get("shock_intake") or {}),
        pending_decisions=tuple(
            dict(item)
            for item in (data.get("pending_author_decisions") or [])
            if isinstance(item, Mapping)
        ),
    )


def load_local_global_link(path: Path | str | None = None) -> LocalGlobalLink:
    """Read and validate the packaged link record's declared format."""
    target = Path(path) if path is not None else DATA_PATH
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LinkError(f"link record not found: {target}") from exc
    except json.JSONDecodeError as exc:
        raise LinkError(f"{target} is not valid JSON: {exc}") from exc
    declared = str(data.get("format", ""))
    if declared != LINK_FORMAT:
        raise LinkError(f"{target} declares format {declared!r}, expected {LINK_FORMAT!r}")
    return link_from_dict(data)
