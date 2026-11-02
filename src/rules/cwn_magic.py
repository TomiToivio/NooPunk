"""CWN 6.1 — Mages, Mage Effort and spellcasting (issue #1068).

Implemented from the CWN SRD, including the two rules that are easiest to get subtly wrong: the Effort pool is
*not* a flat number, and cyberware eats it.

**Mage Effort** (6.1.1) = the higher of the Intelligence or Wisdom modifier, plus the Cast skill level, minimum 1.
It refreshes completely after eight uninterrupted hours of reasonably comfortable sleep. A caster who is starved,
freezing, thirsting, sick or otherwise physically distracted **does not refresh**.

Three commitment durations exist, and they are not interchangeable:

* ``day``      — returns the next morning.
* ``scene``    — returns at the end of the scene.
* ``duration`` — reclaimable as an Instant action, but whatever it fuelled ends when it is reclaimed.

**Cyberware** (6.2.2, applied to summoners but the same shape here) reduces the maximum by the System Strain of
each implant, to a minimum of one point.

Casting (6.1.3.2) needs at least one hand free and the ability to speak; heavy armour or partial restraint is
fine, being severely jostled is not.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from src.rules.wn_core import attribute_modifier

COMMITMENTS = ("day", "scene", "duration")


class MagicError(ValueError):
    """A rule was about to be broken."""


def mage_effort(*, intelligence: int, wisdom: int, cast_skill: int,
                cyberware_strain: float = 0.0) -> int:
    """Max Mage Effort = max(INT, WIS modifier) + Cast skill, min 1, less cyberware strain."""
    if cast_skill < 0:
        raise MagicError("Cast skill cannot be negative")
    if intelligence <= 0 or wisdom <= 0:
        raise MagicError("attributes must be positive")
    base = max(attribute_modifier(intelligence), attribute_modifier(wisdom)) + cast_skill
    pool = base - math.ceil(cyberware_strain)
    return max(1, pool)


def summoner_effort(*, constitution: int, charisma: int, summon_skill: int,
                    cyberware_strain: float = 0.0) -> int:
    """6.2.1: max(CON, CHA modifier) + Summon skill, min 1, reduced by each implant's System Strain."""
    if summon_skill < 0:
        raise MagicError("Summon skill cannot be negative")
    base = max(attribute_modifier(constitution), attribute_modifier(charisma)) + summon_skill
    return max(1, base - math.ceil(cyberware_strain))


def cyberware_penalty(strains) -> int:
    """Effort lost to implants: the System Strain of each, totalled and rounded up.

    **Recorded discrepancy.** The SRD's worked example reads "System Strain costs of 2, 0, and 0.5 would lose four
    points". 2 + 0 + 0.5 = 2.5, which rounds up to 3, not 4. This function implements the stated rule (sum, round
    up, floor at one); the example is flagged in `SDT_EXAMPLE_MISMATCH` rather than quietly matched, because
    guessing which of the three numbers was meant would bake a guess into a rule.
    """
    strains = [float(s) for s in strains]
    if any(s < 0 for s in strains):
        raise MagicError("System Strain cannot be negative")
    return math.ceil(sum(strains))


SDT_EXAMPLE_MISMATCH = ("SRD 6.2.2 example: 2 + 0 + 0.5 is said to cost four points; the rule as stated "
                        "gives three. Implemented as stated; the example is unverified.")


@dataclass
class EffortPool:
    """A pool with the three commitment durations, kept separate per caster class."""
    maximum: int
    label: str = "mage"
    _committed: dict[str, int] = field(default_factory=lambda: {k: 0 for k in COMMITMENTS})

    def __post_init__(self):
        if self.maximum < 1:
            raise MagicError("an Effort pool is at least 1")

    @property
    def available(self) -> int:
        return self.maximum - sum(self._committed.values())

    @property
    def committed(self) -> dict[str, int]:
        return dict(self._committed)

    def commit(self, amount: int, *, duration: str) -> None:
        if duration not in COMMITMENTS:
            raise MagicError(f"unknown commitment {duration!r}")
        if amount < 0:
            raise MagicError("cannot commit negative Effort")
        if amount > self.available:
            raise MagicError(f"only {self.available} Effort available, {amount} requested")
        self._committed[duration] += amount

    def end_scene(self) -> int:
        released, self._committed["scene"] = self._committed["scene"], 0
        return released

    def reclaim_duration(self) -> int:
        """Instant action; whatever the Effort fuelled ends immediately."""
        released, self._committed["duration"] = self._committed["duration"], 0
        return released

    def refresh_morning(self, *, slept_eight_hours: bool = True, comfortable: bool = True) -> bool:
        """6.1.1: day commitments and everything else return, but only with sleep and no hardship."""
        if not slept_eight_hours or not comfortable:
            return False
        self._committed = {k: 0 for k in COMMITMENTS}
        return True


def can_cast(*, free_hand: bool, can_speak: bool) -> bool:
    """6.1.3.2: one hand free and the ability to speak. Heavy armour is explicitly fine."""
    return bool(free_hand and can_speak)
