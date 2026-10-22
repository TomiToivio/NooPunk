"""NoöPunk Tarot resolution — an alternative to the 4dF die roll.

Drawn from sources/laclaugpt-data-storage-noopunk/TAROT.md and RULES.md §3.

A's CP-RED mechanic ("the card number replaces the 1d10 roll; Major Arcana
value 0 overrides the narrative; reversed inverts/corrupts") is translated onto
B's existing 4dF/Fate pipeline:

* Minor Arcana (Ace=1 .. King=14) map linearly onto the 4dF total range -4..+4
  and are fed to ``resolve_action(..., roll=...)`` so the character's attribute,
  skill, and the difficulty still matter — the card only replaces the die.
* Reversed cards negate the roll (inverting the outcome) and carry a "corrupted"
  narrative note.
* Major Arcana (value 0) never feed the roll: they force their ``override_tier``
  directly, escalating the situation beyond the player's control.

All draws are deterministic for a given ``seed`` (``random.Random``); no live
randomness and no LLM is involved. The module is pure-Python and adds no
dependencies — ``requirements.txt`` is unchanged.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from .actions import ActionType, ActionResult
from .models import Character, CheckResult, ResultTier, SkillCheck
from .rules import resolve_check

# Representative margin for a forced Major-Arcana tier, so ActionResult.shifts
# (max(0, margin)) and the success predicates stay meaningful when the card
# overrides the narrative entirely.
_REPRESENTATIVE_MARGIN: dict[ResultTier, int] = {
    ResultTier.CRITICAL_SUCCESS: 3,
    ResultTier.SUCCESS: 1,
    ResultTier.COSTLY_SUCCESS: -1,
    ResultTier.FAILURE: -3,
    ResultTier.CATASTROPHIC_FAILURE: -5,
}


@dataclass(frozen=True)
class Card:
    id: str
    name: str
    suit: str | None
    value: int
    arcana: str | None = None
    override_tier: ResultTier | None = None
    upright: str = ""
    reversed: str = ""
    note: str = ""

    @property
    def is_major(self) -> bool:
        return self.arcana is not None


@dataclass(frozen=True)
class DrawnCard:
    card: Card
    reversed: bool

    @property
    def narrative(self) -> str:
        return self.card.reversed if self.reversed else self.card.upright


@dataclass
class Deck:
    major: list[Card] = field(default_factory=list)
    minor: list[Card] = field(default_factory=list)
    suits: tuple[str, ...] = ()
    reversed_probability: float = 0.5

    @property
    def all_cards(self) -> list[Card]:
        return [*self.major, *self.minor]


def _card_from_dict(data: dict[str, Any]) -> Card:
    override = data.get("override_tier")
    return Card(
        id=data["id"],
        name=data["name"],
        suit=data.get("suit"),
        value=int(data["value"]),
        arcana=data.get("arcana"),
        override_tier=ResultTier(override) if override else None,
        upright=data.get("upright", ""),
        reversed=data.get("reversed", ""),
        note=data.get("note", ""),
    )


def load_deck(path: str | Path | None = None) -> Deck:
    """Load the NoöPunk Tarot deck.

    Defaults to ``data/rpg/tarot_deck.json`` next to the package.
    """
    if path is None:
        path = Path(__file__).resolve().parent.parent.parent / "data" / "rpg" / "tarot_deck.json"
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return Deck(
        major=[_card_from_dict(item) for item in raw["major_arcana"]],
        minor=[_card_from_dict(item) for item in raw["minor_arcana"]],
        suits=tuple(raw["suits"]),
        reversed_probability=float(raw.get("reversed_probability", 0.5)),
    )


def value_to_roll(value: int, reversed: bool = False) -> int:
    """Map a Minor Arcana card value (1..14) onto the 4dF total range (-4..+4).

    Reversed negates the roll, inverting the outcome per RULES.md §3.
    Major Arcana (value 0) map to 0 but are never used as a roll — their
    ``override_tier`` is applied directly.
    """
    if value <= 0:
        roll = 0
    else:
        # Linear map 1..14 → -4..+4.
        roll = round((value - 1) * 8 / 13) - 4
    roll = max(-4, min(4, roll))
    return -roll if reversed else roll


def draw(
    seed: int,
    deck: Deck,
    *,
    suit: str | None = None,
    force_reversed: bool | None = None,
    exclude: str | None = None,
) -> DrawnCard:
    """Draw one card deterministically.

    ``suit`` restricts the draw to a Minor suit (per the GM's call in RULES.md
    §3); ``None`` draws from the full deck (Major + Minor). ``force_reversed``
    overrides the random reversed flip (used by tests and LUCK-redraw logic).
    ``exclude`` drops a card id from the pool — used by ``redraw`` so a LUCK
    redraw never returns the identical card; a degenerate single-card pool
    keeps the original rather than crashing.
    """
    rng = random.Random(seed)
    if suit is not None:
        if suit not in deck.suits:
            raise ValueError(f"Unknown tarot suit: {suit}")
        pool = [card for card in deck.minor if card.suit == suit]
    else:
        pool = deck.all_cards
    if exclude is not None:
        filtered = [card for card in pool if card.id != exclude]
        if filtered:
            pool = filtered
    if not pool:
        raise ValueError("Empty tarot draw pool")
    card = rng.choice(pool)
    if force_reversed is not None:
        is_reversed = force_reversed
    else:
        is_reversed = rng.random() < deck.reversed_probability
    return DrawnCard(card=card, reversed=is_reversed)


def _forced_check(
    actor: Character,
    check: SkillCheck,
    tier: ResultTier,
) -> CheckResult:
    """Build a CheckResult whose tier is forced by a Major Arcana.

    The attribute/skill/bonus fields are still computed (for display and so the
    scenario's check is validated fail-fast), but the tier and margin come from
    the card — Major Arcana "override the narrative entirely".
    """
    base = resolve_check(actor, check, lambda: 0)  # roll 0 → dice (0,0,0,0)
    margin = _REPRESENTATIVE_MARGIN[tier]
    return replace(
        base,
        tier=tier,
        roll=0,
        margin=margin,
        total=base.difficulty + margin,
    )


def resolve_check_tarot(
    actor: Character,
    *,
    seed: int,
    check: SkillCheck,
    deck: Deck | None = None,
    suit: str | None = None,
    force_card: DrawnCard | None = None,
) -> tuple[CheckResult, DrawnCard]:
    """Resolve a ``SkillCheck`` by drawing a Tarot card instead of rolling 4dF.

    Returns ``(check_result, drawn_card)``. The ``CheckResult`` is the same
    shape ``resolve_check`` produces, so the engine's outcome selection and
    save/restore keep working. Used by ``RPGSession.perform_interaction`` when
    an interaction declares ``"resolver": "tarot"``.
    """
    deck = deck or load_deck()
    drawn = force_card if force_card is not None else draw(seed, deck, suit=suit)

    if drawn.card.is_major:
        if drawn.card.override_tier is None:
            raise ValueError(
                f"Major Arcana {drawn.card.id!r} has no override_tier; "
                "Major Arcana must force a tier and never feed the roll"
            )
        return _forced_check(actor, check, drawn.card.override_tier), drawn

    roll = value_to_roll(drawn.card.value, drawn.reversed)
    # Feed the card-derived roll through the shared resolver so the character's
    # attribute, skill, bonuses, and the difficulty all still matter.
    fate_die = iter(_zero_pad_to_total(roll))
    return resolve_check(actor, check, lambda: next(fate_die)), drawn


def _zero_pad_to_total(total: int):
    """Yield four Fate die values (-1/0/+1) summing to ``total`` (clamped)."""
    total = max(-4, min(4, total))
    values = ([1] * total + [-1] * -total) if total != 0 else []
    values += [0] * (4 - len(values))
    for value in values:
        yield value


def resolve_action_tarot(
    actor: Character,
    *,
    seed: int,
    attribute: str,
    skill: str | None,
    difficulty: int,
    deck: Deck | None = None,
    action: ActionType = ActionType.OVERCOME,
    suit: str | None = None,
    situational_modifier: int = 0,
    target: str | None = None,
    created_aspect: str | None = None,
    graph_effects: tuple = (),
    stunt: str | None = None,
    force_card: DrawnCard | None = None,
) -> tuple[ActionResult, DrawnCard]:
    """Resolve an action by drawing a Tarot card instead of rolling 4dF.

    Returns ``(action_result, drawn_card)`` so callers can narrate the card.
    ``force_card`` bypasses the draw (for deterministic scenario scripting and
    tests). The returned ``ActionResult`` is the same shape as
    ``resolve_action`` produces, so every downstream consumer (``.succeeded``,
    ``.shifts``, ``.applicable_graph_effects``) keeps working.
    """
    check = SkillCheck(
        attribute=attribute,
        difficulty=difficulty,
        skill=skill,
        situational_modifier=situational_modifier + (2 if stunt in actor.stunts else 0),
    )
    check_result, drawn = resolve_check_tarot(
        actor, seed=seed, check=check, deck=deck, suit=suit, force_card=force_card,
    )
    result = ActionResult(
        action=action,
        check=check_result,
        target=target,
        created_aspect=created_aspect,
        graph_effects=graph_effects,
    )
    return result, drawn


def redraw(
    seed: int,
    deck: Deck,
    previous: DrawnCard,
    *,
    suit: str | None = None,
) -> DrawnCard:
    """Spend one LUCK point to redraw (RULES.md §3). You must keep the new draw.

    The redraw is seeded deterministically from ``seed`` but perturbed by the
    previous card id and excludes the previous card from the pool, so a redraw
    never returns the identical card (for any deck with more than one card in
    the pool).
    """
    perturbed = seed ^ (sum(ord(ch) for ch in (previous.card.id or "")) + 1)
    return draw(perturbed, deck, suit=suit, exclude=previous.card.id)