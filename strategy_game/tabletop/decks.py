"""Deck, hand and discard: seeded shuffles, duplicate policy and a reproducible draw log.

Issue #347 asks for "seeded shuffles, public/private zones, duplicate policies, reproducible draw log;
**not all entity cards are drawn randomly**. An organization or city card may be a persistent board
entity rather than a hand card."

That last clause shapes the model. A :class:`Deck` holds cards whose *position* is explicit, so a
persistent entity can be placed rather than drawn: :meth:`Deck.place` puts a card into a zone without
touching the RNG, and only :meth:`Deck.draw` is random. Nothing here decides when a player may draw,
how many cards they hold, or what a drawn card permits — those are rules.

Reproducibility has two independent guarantees:

* a seeded shuffle/draw is deterministic for a given seed, and
* :class:`DrawLogEntry` records the card that actually moved, so :meth:`Deck.draw_history` is an exact
  record that does not depend on the random implementation at all.

Visibility is a property of the card (:class:`strategy_game.tabletop.cards.CardVisibility`), not of the
zone, because the same drawn card can be public in one context and concealed in another. A zone is
therefore a location, not a permission.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping

from .cards import Card


class DeckError(ValueError):
    """Raised for an invalid deck operation, such as drawing from an empty deck."""


class Zone(Enum):
    """Where a card currently is. A location, not a rule about who may see it."""

    DECK = "deck"
    HAND = "hand"
    DISCARD = "discard"


class DuplicatePolicy(Enum):
    """What to do when two cards in one deck share an identifier."""

    #: Keep every copy. A deck may legitimately hold several copies of one card.
    ALLOW = "allow"
    #: Keep the first, drop later copies. The default: a duplicated identifier is normally an
    #: authoring mistake, and silently holding two "same" entity records forks the record.
    DEDUPE_BY_ID = "dedupe_by_id"
    #: Refuse the deck. For a deck where a duplicate is a data error rather than a design choice.
    REFUSE = "refuse"


@dataclass(frozen=True)
class DrawLogEntry:
    """One recorded move of one card. The reproducible audit trail."""

    sequence: int
    card_id: str
    from_zone: str
    to_zone: str
    #: The seed used for the draw that produced this entry, when the caller supplied one.
    seed: int | None = None
    #: Cards remaining in the source zone *after* the move, so a log can be checked without replay.
    remaining_in_source: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "card_id": self.card_id,
            "from_zone": self.from_zone,
            "to_zone": self.to_zone,
            "seed": self.seed,
            "remaining_in_source": self.remaining_in_source,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> DrawLogEntry:
        return cls(
            sequence=int(data.get("sequence", 0)),
            card_id=str(data.get("card_id", "")),
            from_zone=str(data.get("from_zone", Zone.DECK.value)),
            to_zone=str(data.get("to_zone", Zone.HAND.value)),
            seed=None if data.get("seed") is None else int(data["seed"]),
            remaining_in_source=int(data.get("remaining_in_source", 0)),
        )


@dataclass
class Deck:
    """A deck's cards and their zones, plus the log of every move."""

    identifier: str
    name: str = ""
    duplicate_policy: DuplicatePolicy = DuplicatePolicy.DEDUPE_BY_ID
    #: Every card in the deck, by identifier, whatever zone it is currently in.
    cards: dict[str, Card] = field(default_factory=dict)
    zones: dict[str, list[str]] = field(default_factory=dict)
    history: list[DrawLogEntry] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise DeckError("a deck needs a non-empty identifier")
        for zone in Zone:
            self.zones.setdefault(zone.value, [])

    # -- construction ---------------------------------------------------------------------------

    @classmethod
    def from_cards(cls, identifier: str, cards: Iterable[Card], name: str = "",
                   duplicate_policy: DuplicatePolicy = DuplicatePolicy.DEDUPE_BY_ID) -> Deck:
        """Build a deck, applying the duplicate policy as cards are added."""
        deck = cls(identifier=identifier, name=name, duplicate_policy=duplicate_policy)
        for card in cards:
            deck.add(card)
        return deck

    def add(self, card: Card, zone: Zone = Zone.DECK) -> Card:
        """Add one card to a zone, honouring the duplicate policy."""
        if card.identifier in self.cards:
            if self.duplicate_policy is DuplicatePolicy.REFUSE:
                raise DeckError(
                    f"deck {self.identifier!r} already holds a card identified {card.identifier!r} "
                    "and its duplicate policy is REFUSE"
                )
            if self.duplicate_policy is DuplicatePolicy.DEDUPE_BY_ID:
                return self.cards[card.identifier]
        self.cards[card.identifier] = card
        self.zones[zone.value].append(card.identifier)
        return card

    # -- deliberate placement (persistent entities are not drawn) --------------------------------

    def place(self, card_id: str, zone: Zone) -> None:
        """Move a card to a zone deliberately, without the RNG and without logging a draw.

        This is how a persistent board entity gets onto the table: an organization or a city is
        placed, not dealt. Only :meth:`draw` is random.
        """
        self._require(card_id)
        self._move(card_id, source=None, target=zone, log=False)

    # -- random draw ------------------------------------------------------------------------------

    def shuffle(self, rng: random.Random | None = None, *, seed: int | None = None,
                zone: Zone = Zone.DECK) -> tuple[str, ...]:
        """Shuffle one zone in place and return its new order.

        Deterministic for a given ``seed``. Pass ``rng=`` to share a stream with the rest of a turn.
        """
        if rng is None:
            rng = random.Random(seed)
        order = self.zones[zone.value]
        rng.shuffle(order)
        return tuple(order)

    def draw(self, count: int = 1, rng: random.Random | None = None, *, seed: int | None = None,
             source: Zone = Zone.DECK, target: Zone = Zone.HAND) -> tuple[Card, ...]:
        """Draw ``count`` cards from ``source`` into ``target``, logging every move.

        The top of the zone is the end of the list, so the order a shuffle produced is the order cards
        leave in. Drawing more than remains raises rather than silently returning fewer: a short draw
        usually means the rules were misunderstood, and a quiet partial hand hides that.
        """
        if count < 1:
            raise DeckError(f"draw count must be at least 1, got {count}")
        available = self.zones[source.value]
        if len(available) < count:
            raise DeckError(
                f"deck {self.identifier!r} has {len(available)} card(s) in {source.value} "
                f"but {count} were drawn"
            )
        if rng is None:
            rng = random.Random(seed)
        picked: list[Card] = []
        for _ in range(count):
            index = rng.randrange(len(available))
            card_id = available.pop(index)
            self.zones[target.value].append(card_id)
            self.history.append(
                DrawLogEntry(
                    sequence=len(self.history) + 1,
                    card_id=card_id,
                    from_zone=source.value,
                    to_zone=target.value,
                    seed=seed,
                    remaining_in_source=len(available),
                )
            )
            picked.append(self.cards[card_id])
        return tuple(picked)

    def discard(self, card_id: str) -> None:
        """Move a card from wherever it is into the discard zone."""
        self._require(card_id)
        self._move(card_id, source=None, target=Zone.DISCARD, log=True)

    def recycle(self) -> None:
        """Return the whole discard pile to the deck, unshuffled.

        The caller decides whether to shuffle afterwards; doing it here would decide a rule about
        when a deck is randomised.
        """
        discard = self.zones[Zone.DISCARD.value]
        if not discard:
            return
        self.zones[Zone.DECK.value].extend(discard)
        self.zones[Zone.DISCARD.value] = []
        self.history.append(
            DrawLogEntry(
                sequence=len(self.history) + 1,
                card_id="*",
                from_zone=Zone.DISCARD.value,
                to_zone=Zone.DECK.value,
                remaining_in_source=0,
            )
        )

    # -- queries ----------------------------------------------------------------------------------

    def zone_of(self, card_id: str) -> Zone:
        self._require(card_id)
        for zone in Zone:
            if card_id in self.zones[zone.value]:
                return zone
        raise DeckError(f"card {card_id!r} is in no zone of deck {self.identifier!r}")

    def cards_in(self, zone: Zone) -> tuple[Card, ...]:
        """Cards in a zone, in their current order."""
        return tuple(self.cards[card_id] for card_id in self.zones[zone.value])

    def card_ids_in(self, zone: Zone) -> tuple[str, ...]:
        return tuple(self.zones[zone.value])

    # -- internals --------------------------------------------------------------------------------

    def _require(self, card_id: str) -> None:
        if card_id not in self.cards:
            raise DeckError(f"deck {self.identifier!r} holds no card identified {card_id!r}")

    def _move(self, card_id: str, *, source: Zone | None, target: Zone, log: bool) -> None:
        for zone in Zone:
            if card_id in self.zones[zone.value]:
                self.zones[zone.value].remove(card_id)
                break
        self.zones[target.value].append(card_id)
        if log:
            self.history.append(
                DrawLogEntry(
                    sequence=len(self.history) + 1,
                    card_id=card_id,
                    from_zone="*" if source is None else source.value,
                    to_zone=target.value,
                    remaining_in_source=len(self.zones[target.value]) - 1,
                )
            )

    # -- serialization ----------------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "duplicate_policy": self.duplicate_policy.value,
            "zones": {zone.value: list(self.zones[zone.value]) for zone in Zone},
            "cards": {key: self.cards[key].to_dict() for key in sorted(self.cards)},
            "history": [entry.to_dict() for entry in self.history],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Deck:
        raw_policy = str(data.get("duplicate_policy", DuplicatePolicy.DEDUPE_BY_ID.value))
        deck = cls(
            identifier=str(data.get("identifier", "")),
            name=str(data.get("name", "")),
            duplicate_policy=DuplicatePolicy(raw_policy)
            if raw_policy in {p.value for p in DuplicatePolicy}
            else DuplicatePolicy.DEDUPE_BY_ID,
        )
        # Restore cards first (bypassing the duplicate policy, which was applied when the deck was
        # built), then the zones verbatim, so a saved deck reloads into exactly the state it had.
        for key, payload in (data.get("cards") or {}).items():
            deck.cards[str(key)] = Card.from_dict(payload)
        for zone in Zone:
            deck.zones[zone.value] = [str(cid) for cid in ((data.get("zones") or {}).get(zone.value) or ())]
        deck.history = [DrawLogEntry.from_dict(item) for item in (data.get("history") or ())]
        return deck
