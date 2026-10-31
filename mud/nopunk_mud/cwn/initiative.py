"""Deterministic CWN side-based initiative, plus the optional individual variant.

Source: https://cwn.quadrifons.com/rules-of-the-game/combat/combat-initiative/
Rolls are supplied by the caller for replay and headless testing.
This schedules turns; the caller remains responsible for judging surprise and
automatic-initiative powers, applying action budgets, and resolving morale.
"""
from dataclasses import dataclass
from typing import Iterable

from . import CwnError


@dataclass(frozen=True)
class InitiativeEntry:
    """A side (default) or one combatant (optional individual initiative)."""

    name: str
    die: int
    dex_modifier: int = 0
    pc: bool = False
    automatic: bool = False


def initiative_order(entries: Iterable[InitiativeEntry]) -> tuple[InitiativeEntry, ...]:
    """Return the fixed CWN turn order, highest first, with PC-side ties won.

    Roll 1d8 + the *best* Dexterity modifier of the side, supplied by the
    caller. For individual initiative supply one entry per combatant instead.
    Automatic initiative goes ahead of ordinary initiative; automatic actors
    roll normally against one another. Reuse this order each subsequent round.
    """
    parties = tuple(entries)
    names = set()
    for party in parties:
        if not isinstance(party, InitiativeEntry):
            raise CwnError("initiative entries must be InitiativeEntry instances")
        if not party.name or party.name in names:
            raise CwnError("initiative sides must have unique nonempty names")
        names.add(party.name)
        if type(party.die) is not int or not 1 <= party.die <= 8:
            raise CwnError("CWN initiative uses a 1d8 roll (1..8)")
        if type(party.dex_modifier) is not int:
            raise CwnError("initiative Dexterity modifier must be an integer")
    # Python sort stability preserves provided order for otherwise identical
    # ties, making the fixture replayable without inventing another dice roll.
    return tuple(sorted(
        parties,
        key=lambda p: (p.automatic, p.die + p.dex_modifier, p.pc),
        reverse=True,
    ))


def surprise_round(
    entries: Iterable[InitiativeEntry], surprised: Iterable[str]
) -> tuple[InitiativeEntry, ...]:
    """Return actors eligible for the *one* free round before initiative.

    A GM determines which groups were caught unawares. Actively vigilant
    groups must not be put in `surprised`; this is a calling-layer decision.
    Normal initiative follows this free round, without re-rolling.
    """
    parties = initiative_order(entries)
    surprised_names = tuple(surprised)
    if len(set(surprised_names)) != len(surprised_names):
        raise CwnError("duplicate surprised side")
    if set(surprised_names) - {p.name for p in parties}:
        raise CwnError("unknown surprised side")
    return tuple(p for p in parties if p.name not in surprised_names)
