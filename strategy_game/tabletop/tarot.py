"""One reusable tarot deck, several interpreters — with no meanings and no effects attached.

Issue #347 requires a **single reusable tarot card/deck data model** and explicitly forbids
multiplying identical decks: "Same deck, different interpreters/context rules; do not multiply
identical decks." It also names five selectable uses, and draws a hard boundary:

    "Exact tarot deck composition, meanings, mechanical modifiers and metaphysical claims need
    author approval per #304. Initial implementation may support typed tarot placeholders and
    harmless prompts, without fixing unapproved canonical effects."

So this module provides exactly that: :class:`TarotCard` is a typed **placeholder** with no meaning,
no numeral semantics, no reversal rule and no modifier; :class:`TarotDraw` records *attribution* —
which card, which use, which scene, which actor, which seed, what the interpreter said — and nothing
else. The same :class:`~strategy_game.tabletop.decks.Deck` type is reused for tarot cards, so there is
one deck implementation rather than two, and the draw is written into the deck's existing reproducible
log.

What is deliberately absent: card meanings, upright/reversed handling, spreads, mechanical modifiers,
and any claim about what a card metaphysically is. :meth:`TarotCard.assert_placeholder` exists so a
data author can prove the field is still unclaimed rather than discovering the opposite while playing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .cards import Card, CardError, CardType, CardVisibility
from .decks import Deck, Zone


class TarotUse(Enum):
    """The five interpreter contexts the issue lists. One deck, five readings."""

    #: Narrative/RPG omens, strange encounters and complications.
    NARRATIVE_OMEN = "narrative_omen"
    #: GM scenario/event prompts, world crises and emergent side stories.
    GM_PROMPT = "gm_prompt"
    #: Faction strategy, ideological articulation and propaganda symbolism.
    FACTION_SYMBOLISM = "faction_symbolism"
    #: PSI/Astral investigation, dreams, visions and uncertainty.
    PSI_INVESTIGATION = "psi_investigation"
    #: Character background, psychological interpretation and relationship prompts.
    CHARACTER_INTERPRETATION = "character_interpretation"


#: The declared value set, so callers can validate without constructing an enum member.
TAROT_USES: tuple[str, ...] = tuple(use.value for use in TarotUse)


@dataclass
class TarotCard:
    """A tarot placeholder: identity and art reference only.

    Nothing here is a meaning. ``symbols`` is free-form labelling for the art pipeline; a later
    author decision is what would give any of it mechanical or metaphysical content.
    """

    identifier: str
    display_name: str
    art_ref: str = ""
    symbols: tuple[str, ...] = ()
    #: Author-facing note. Not player-facing content, and not read by anything here.
    notes: str = ""

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise CardError("a tarot card needs a non-empty identifier")
        if not str(self.display_name).strip():
            raise CardError(f"tarot card {self.identifier!r} needs a non-empty display name")
        self.symbols = tuple(str(symbol) for symbol in self.symbols)

    def assert_placeholder(self) -> None:
        """Raise if this card has been given anything beyond placeholder fields.

        Called by the codex/scenario loaders when they need to prove a tarot entry carries no approved
        mechanics. It is a shape check on *this* dataclass, not a canon check on prose.
        """
        unexpected = sorted(set(self.__dict__) - {"identifier", "display_name", "art_ref",
                                                  "symbols", "notes"})
        if unexpected:
            raise CardError(f"tarot card {self.identifier!r} carries non-placeholder field(s): {unexpected}")

    def to_card(self) -> Card:
        """The same card as a generic :class:`~strategy_game.tabletop.cards.Card`, for one deck type."""
        return Card(
            identifier=self.identifier,
            card_type=CardType.TAROT,
            title=self.display_name,
            text="",
            art_ref=self.art_ref,
            tags=self.symbols,
            visibility=CardVisibility.PUBLIC,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "display_name": self.display_name,
            "art_ref": self.art_ref,
            "symbols": list(self.symbols),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> TarotCard:
        return cls(
            identifier=str(data.get("identifier", "")),
            display_name=str(data.get("display_name", "")),
            art_ref=str(data.get("art_ref", "")),
            symbols=tuple(str(symbol) for symbol in (data.get("symbols") or ())),
            notes=str(data.get("notes", "")),
        )


@dataclass
class TarotDraw:
    """One attributable draw. Attribution is the whole record: there is no effect field.

    The issue asks that "a card draw be attributable (scene, player/GM, seed, interpretation) and
    optionally contextual", which is what these fields are. ``interpretation`` is free text: the
    interpreter's reading, which is *not* elevated into a rule by being stored.
    """

    card_id: str
    use: TarotUse
    scene_id: str | None = None
    actor_id: str | None = None
    #: "player" or "gm" — who drew it, when the caller knows.
    drawn_by: str = ""
    #: The seed of the draw, when one was supplied.
    seed: int | None = None
    #: Optional context (the question asked, the situation).
    context: str = ""
    #: The reading given. Free text; never interpreted by the scaffold.
    interpretation: str = ""
    #: Alternative readings, kept so uncertainty is visible rather than collapsed to one answer.
    alternatives: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not str(self.card_id).strip():
            raise CardError("a tarot draw needs the card it drew")
        self.alternatives = tuple(str(item) for item in self.alternatives)

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_id": self.card_id,
            "use": self.use.value,
            "scene_id": self.scene_id,
            "actor_id": self.actor_id,
            "drawn_by": self.drawn_by,
            "seed": self.seed,
            "context": self.context,
            "interpretation": self.interpretation,
            "alternatives": list(self.alternatives),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> TarotDraw:
        raw_use = str(data.get("use", TarotUse.NARRATIVE_OMEN.value))
        return cls(
            card_id=str(data.get("card_id", "")),
            use=TarotUse(raw_use) if raw_use in TAROT_USES else TarotUse.NARRATIVE_OMEN,
            scene_id=None if data.get("scene_id") is None else str(data["scene_id"]),
            actor_id=None if data.get("actor_id") is None else str(data["actor_id"]),
            drawn_by=str(data.get("drawn_by", "")),
            seed=None if data.get("seed") is None else int(data["seed"]),
            context=str(data.get("context", "")),
            interpretation=str(data.get("interpretation", "")),
            alternatives=tuple(str(item) for item in (data.get("alternatives") or ())),
        )


def tarot_deck(identifier: str, cards: list[TarotCard], name: str = "") -> Deck:
    """Wrap tarot placeholders in the shared deck type, so tarot has no separate deck machinery."""
    deck = Deck(identifier=identifier, name=name)
    for card in cards:
        deck.add(card.to_card())
    return deck


def draw_tarot(deck: Deck, use: TarotUse, rng: Any = None, *, seed: int | None = None,
               scene_id: str | None = None, actor_id: str | None = None, drawn_by: str = "",
               context: str = "", interpretation: str = "",
               alternatives: tuple[str, ...] = ()) -> TarotDraw:
    """Draw one card for one interpreter context and record it.

    The deck draw itself is the shared, reproducible one: the move lands in the deck's history like any
    other, so tarot draws are auditable alongside the rest of the table. This function adds attribution
    and nothing else — in particular it does not look up a meaning, because no meanings are approved.
    """
    drawn = deck.draw(1, rng=rng, seed=seed, source=Zone.DECK, target=Zone.HAND)
    card = drawn[0]
    if card.card_type is not CardType.TAROT:
        raise CardError(
            f"deck {deck.identifier!r} drew a {card.card_type.value!r} card, not a tarot card; "
            "the tarot reading must use the tarot deck"
        )
    return TarotDraw(
        card_id=card.identifier,
        use=use,
        scene_id=scene_id,
        actor_id=actor_id,
        drawn_by=drawn_by,
        seed=seed,
        context=context,
        interpretation=interpretation,
        alternatives=alternatives,
    )
