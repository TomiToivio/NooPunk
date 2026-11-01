"""Cities Without Number: initiative and the combat sequence (SRD 2.4.1 - 2.4.2).

Ported from ``rules-of-the-game/combat/combat-initiative`` and ``/combat-sequence``. Values are taken from
the SRD; nothing here is house-ruled.

Group initiative (the default)
    Each side rolls **1d8 + its best Dexterity modifier**. NPC sides usually add nothing. Sides act from
    highest to lowest and the player-character side wins ties. Members of a side act in whatever order they
    agree on. When the last side has acted the round ends, and a new round begins in the *same* order:
    initiative is not re-rolled.

Individual initiative (optional)
    Each combatant rolls 1d8 + their own Dexterity modifier and acts in order, player characters winning
    ties. It makes a group harder to catch flat-footed but harder to coordinate.

Surprise is a GM decision, not a die roll, so it is modelled as a flag that grants one free round rather
than being computed here. Combatants with automatic-initiative abilities act before everyone else; if more
than one has such an ability they roll off among themselves.
"""
from __future__ import annotations

import random
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from .wn_core import attribute_modifier

INITIATIVE_DIE_FACES = 8


class InitiativeError(ValueError):
    """An initiative input is contradictory or out of range."""



@dataclass(frozen=True)
class Side:
    """One group in a fight, with the Dexterity scores of everyone in it."""

    name: str
    dexterities: Sequence[int]
    is_pc: bool = False

    def best_modifier(self) -> int:
        """The side's best Dexterity modifier; an NPC side with no scores adds nothing."""
        if not self.dexterities:
            return 0
        return max(attribute_modifier(score) for score in self.dexterities)


@dataclass(frozen=True)
class InitiativeEntry:
    side: Side
    roll: int

    @property
    def total(self) -> int:
        return self.roll + self.side.best_modifier()


def initiative_roll(side: Side, *, die: int | None = None,
                    rng: random.Random | None = None) -> InitiativeEntry:
    """Roll 1d8 for one side and add that side's best Dexterity modifier."""
    if die is None:
        die = (rng or random.Random()).randint(1, INITIATIVE_DIE_FACES)
    if not 1 <= die <= INITIATIVE_DIE_FACES:
        raise InitiativeError("initiative die must be 1..8")
    return InitiativeEntry(side, die)


def order_sides(sides: Iterable[Side], *, dice: Sequence[int] | None = None,
                rng: random.Random | None = None) -> list[InitiativeEntry]:
    """Sides from highest to lowest, player characters winning ties.

    ``dice`` supplies the rolls for deterministic tests; otherwise they are drawn.
    """
    sides = list(sides)
    if not sides:
        raise InitiativeError("a fight needs at least one side")
    if dice is not None and len(dice) != len(sides):
        raise InitiativeError("one die per side")
    entries = [initiative_roll(side, die=None if dice is None else dice[i], rng=rng)
               for i, side in enumerate(sides)]
    # PC side wins ties: the second key is 0 for a player-character side and 1 for everyone else.
    return sorted(entries, key=lambda e: (-e.total, 0 if e.side.is_pc else 1))


def order_individual(combatants: Iterable[tuple[str, int, bool]], *,
                     dice: Sequence[int] | None = None,
                     rng: random.Random | None = None) -> list[tuple[str, int]]:
    """Individual initiative: 1d8 + own Dexterity modifier, PCs winning ties.

    ``combatants`` is ``(name, dexterity, is_pc)``.
    """
    people = list(combatants)
    if not people:
        raise InitiativeError("a fight needs at least one combatant")
    if dice is not None and len(dice) != len(people):
        raise InitiativeError("one die per combatant")
    rows = []
    for index, (name, dexterity, is_pc) in enumerate(people):
        face = dice[index] if dice is not None else (rng or random.Random()).randint(1, 8)
        if not 1 <= face <= INITIATIVE_DIE_FACES:
            raise InitiativeError("initiative die must be 1..8")
        rows.append((name, face + attribute_modifier(dexterity), is_pc))
    rows.sort(key=lambda r: (-r[1], 0 if r[2] else 1))
    return [(name, total) for name, total, _ in rows]


class CombatRound:
    """Turn order across rounds. Initiative is rolled once and kept."""

    def __init__(self, order: Sequence[InitiativeEntry], *, automatic: Sequence[str] = ()):
        if not order:
            raise InitiativeError("a round needs an order")
        self._order = list(order)
        self._automatic = list(automatic)
        self._index = 0
        self.round_number = 1
        self.turns_taken: list[str] = []

    @property
    def order(self) -> list[str]:
        """Sides in the order they act, including automatic-initiative actors first."""
        lead = [name for name in self._automatic]
        return lead + [entry.side.name for entry in self._order
                       if entry.side.name not in self._automatic]

    def current(self) -> str:
        return self.order[self._index]

    def advance(self) -> str:
        """Finish the current side's turn and return the next side to act."""
        self.turns_taken.append(self.current())
        self._index += 1
        if self._index >= len(self.order):
            self._index = 0
            self.round_number += 1
            self.turns_taken = []
        return self.current()

    def run_round(self) -> list[str]:
        """Every side acts once, in order, and the round advances."""
        acting = self.order[self._index:] + self.order[:self._index]
        for _ in acting:
            self.advance()
        return acting


def surprise_free_round(surprised: Sequence[str], ready: Sequence[str]) -> list[str]:
    """The order for the free round granted by surprise: the ready side acts, then normal initiative.

    Surprise is the GM's call; this only encodes what it grants.
    """
    if not ready:
        raise InitiativeError("a surprise round needs a side that is ready")
    return list(ready)


def surprise_applies(*, surprised: bool, anticipating: bool) -> bool:
    """Surprise cannot be imposed on a group already expecting a fight (SRD 2.4.1).

    The SRD is explicit: *"Groups cannot be surprised if they are actively anticipating the possibility
    of combat; at most, they might suffer an initiative penalty at the GM's discretion."* Encoding that
    here keeps the carve-out with the rest of the surprise rule instead of leaving it to a caller's
    memory.
    """
    return surprised and not anticipating
