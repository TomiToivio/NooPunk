"""Card records: stable identity, a generic type, content data and declared visibility — never rules.

Issue #347 asks for "a generic type plus content data instead of hardcoded subclasses per unique
card", and names the required card families. It also requires that a card's prerequisites and effects
exist as *structured data* while nothing in the scaffold interprets them, and that **persistent
records are distinguishable from playable moves** — an organization or city card is a board entity,
not a card in a hand.

So :class:`Card` is one dataclass with a :class:`CardType` and a :class:`CardRole`. Adding a card never
means adding a class. The two structured fields are carried verbatim:

* :attr:`Card.prerequisites` / :attr:`Card.effects` are tuples of plain mappings. This module validates
  only that they are JSON-serializable mappings with a declared ``kind`` string; it does not know what
  any ``kind`` means, does not evaluate a condition and does not apply an effect. That is Gate A/C
  work, and it is not approved.

Content provenance reuses :mod:`strategy_game.provenance` rather than inventing a second scheme, so an
authored card, a generated card and an observed record keep the same distinction the rest of the
scaffold already makes — and an unrecorded origin stays ``UNKNOWN`` rather than reading as fact.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping

from ..provenance import Provenance


class CardError(ValueError):
    """Raised for a malformed card record."""


class CardType(Enum):
    """The card families the issue names. A category, not a mechanic."""

    CHARACTER = "character"
    FACTION = "faction"
    ORGANIZATION = "organization"
    PLACE = "place"
    RESEARCH = "research"
    EVENT = "event"
    EQUIPMENT = "equipment"
    MISSION = "mission"
    RELATIONSHIP = "relationship"
    IDEOLOGY = "ideology"
    TAROT = "tarot"


#: The declared value set, so callers can validate without constructing an enum member.
CARD_TYPES: tuple[str, ...] = tuple(kind.value for kind in CardType)


class CardRole(Enum):
    """Whether a card is a standing record or something a player can play.

    The issue requires this distinction explicitly. It is a *kind* distinction and carries no
    permission: this module has no notion of a legal move, a cost or a turn.
    """

    #: A persistent board/entity record (a city, an organization, a faction).
    PERSISTENT_RECORD = "persistent_record"
    #: A move a player may be permitted to make. What "permitted" means is not defined here.
    PLAYABLE_MOVE = "playable_move"


class CardVisibility(Enum):
    """Who may read a card's content. Display policy only; no rule reads this field."""

    #: Public or already-discovered information.
    PUBLIC = "public"
    #: Known to its owner only.
    PRIVATE = "private"
    #: Exists in the collection but reads as a hidden card back.
    CONCEALED = "concealed"


def _structured(items: Iterable[Mapping[str, Any]], field_name: str) -> tuple[dict[str, Any], ...]:
    """Validate a structured-data tuple: mappings, JSON-serializable, each carrying a ``kind``.

    The ``kind`` requirement is a shape check, so a data author cannot store a bare sentence where the
    engine will later look for a mechanism — and so the scaffold can serialize the field without
    guessing. Nothing else about the contents is inspected or enforced.
    """
    out: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise CardError(f"{field_name}[{index}] must be a mapping, got {type(item).__name__}")
        record = dict(item)
        if not str(record.get("kind", "")).strip():
            raise CardError(
                f"{field_name}[{index}] needs a non-empty 'kind' so the data stays self-describing"
            )
        try:
            json.dumps(record)
        except (TypeError, ValueError) as exc:
            raise CardError(f"{field_name}[{index}] is not JSON-serializable: {exc}") from exc
        out.append(record)
    return tuple(out)


@dataclass
class Card:
    """One card record. Content data, not a mechanic."""

    identifier: str
    card_type: CardType
    title: str
    role: CardRole = CardRole.PERSISTENT_RECORD
    text: str = ""
    #: Reference to artwork stored separately from mechanics, so content can be swapped without
    #: touching rules and a thousand illustrations are never hand-authored into code.
    art_ref: str = ""
    tags: tuple[str, ...] = ()
    #: Owner, when the card belongs to a faction, organization or character.
    owner_id: str | None = None
    visibility: CardVisibility = CardVisibility.PUBLIC
    #: Structured, uninterpreted. See :func:`_structured`.
    prerequisites: tuple[dict[str, Any], ...] = ()
    effects: tuple[dict[str, Any], ...] = ()
    #: Where the card's *content* came from. Defaults to UNKNOWN: an unrecorded origin stays visible.
    provenance: Provenance = field(default_factory=Provenance)

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise CardError("a card needs a non-empty identifier")
        if not str(self.title).strip():
            raise CardError(f"card {self.identifier!r} needs a non-empty title")
        if not isinstance(self.card_type, CardType):
            raise CardError(f"card {self.identifier!r} needs a CardType, got {self.card_type!r}")
        self.tags = tuple(str(tag) for tag in self.tags)
        self.prerequisites = _structured(list(self.prerequisites), "prerequisites")
        self.effects = _structured(list(self.effects), "effects")
        if not isinstance(self.provenance, Provenance):
            self.provenance = Provenance.from_dict(self.provenance)

    @property
    def is_playable_move(self) -> bool:
        return self.role is CardRole.PLAYABLE_MOVE

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "card_type": self.card_type.value,
            "role": self.role.value,
            "title": self.title,
            "text": self.text,
            "art_ref": self.art_ref,
            "tags": list(self.tags),
            "owner_id": self.owner_id,
            "visibility": self.visibility.value,
            "prerequisites": [dict(item) for item in self.prerequisites],
            "effects": [dict(item) for item in self.effects],
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Card:
        raw_type = str(data.get("card_type", CardType.EVENT.value))
        raw_role = str(data.get("role", CardRole.PERSISTENT_RECORD.value))
        raw_visibility = str(data.get("visibility", CardVisibility.PUBLIC.value))
        return cls(
            identifier=str(data.get("identifier", "")),
            card_type=CardType(raw_type) if raw_type in CARD_TYPES else CardType.EVENT,
            title=str(data.get("title", "")),
            role=CardRole(raw_role) if raw_role in {r.value for r in CardRole}
            else CardRole.PERSISTENT_RECORD,
            text=str(data.get("text", "")),
            art_ref=str(data.get("art_ref", "")),
            tags=tuple(str(tag) for tag in (data.get("tags") or ())),
            owner_id=None if data.get("owner_id") is None else str(data["owner_id"]),
            visibility=CardVisibility(raw_visibility)
            if raw_visibility in {v.value for v in CardVisibility}
            else CardVisibility.PUBLIC,
            prerequisites=tuple(data.get("prerequisites") or ()),
            effects=tuple(data.get("effects") or ()),
            provenance=Provenance.from_dict(data.get("provenance")),
        )
