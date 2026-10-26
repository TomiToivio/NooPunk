"""Cities Without Number: System Strain.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``):

* ``rules-of-the-game/injury-healing-system-strain/system-strain/`` — the whole mechanic;
* ``rules-of-the-game/injury-healing-system-strain/major-injuries/`` — why Strain matters for
  cyberware and for what a Major Injury can destroy.

## The rule, as the SRD states it

A healthy character starts at **0** Strain and may never exceed their **Constitution score**. Cyberware
installation adds **permanent** Strain, which may be **fractional**; the body can never support more
than the maximum, and removing the cyber removes its permanent Strain. Pharmaceutical healing and
cyberware activation add Strain as well: if the addition would pass the maximum, the character
**cannot** activate the cyber, benefit from the drug, or otherwise gain the ability's use. If an
unavoidable effect forces them past the maximum, they are **knocked unconscious for at least an hour**
instead. One point is lost after each night's rest, provided the character is warm, fed, comfortable
and gets at least eight uninterrupted hours of sleep.

## What this module deliberately does not model

The SRD does not say that a forced overflow *raises* the total — it says the total cannot exceed the
maximum. :meth:`SystemStrain.absorb` therefore clamps at the maximum and records the unconsciousness,
rather than inventing a debt above the cap. First aid, poisons and the recovery rate for Major Injuries
live in their own SRD subsections and are not folded in here.
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: SRD: "has their Constitution score as their allowed maximum".
MAXIMUM_ATTRIBUTE = "Constitution"

#: SRD: "lose one point of accumulated System Strain after each night's rest".
RECOVERY_PER_NIGHT = 1.0

#: SRD: at least eight uninterrupted hours, warm, fed and comfortable.
REST_HOURS_REQUIRED = 8.0

#: SRD: a forced overflow knocks the subject out "for at least an hour".
FORCED_OVERFLOW_UNCONSCIOUS_HOURS = 1.0


class StrainError(ValueError):
    """A constraint from the SRD was about to be violated."""


@dataclass
class SystemStrain:
    """A character's Strain: permanent cyberware load plus temporary, recoverable load."""

    constitution: int
    temporary: float = 0.0
    permanent: float = 0.0
    unconscious_hours: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        if self.constitution < 0:
            raise StrainError("Constitution cannot be negative")
        if self.temporary < 0 or self.permanent < 0:
            raise StrainError("Strain cannot be negative")
        if self.total > self.maximum:
            raise StrainError(
                f"Strain {self.total:g} exceeds the Constitution maximum {self.maximum}"
            )

    @property
    def maximum(self) -> int:
        """The allowed maximum: the Constitution score."""
        return self.constitution

    @property
    def total(self) -> float:
        """Permanent plus temporary Strain."""
        return self.permanent + self.temporary

    @property
    def available(self) -> float:
        """How much Strain the character can still take."""
        return max(0.0, self.maximum - self.total)

    def can_absorb(self, amount: float) -> bool:
        """Whether an addition would stay within the maximum."""
        if amount < 0:
            raise StrainError("Strain additions cannot be negative")
        return self.total + amount <= self.maximum

    def absorb(self, amount: float, *, forced: bool = False) -> bool:
        """Add Strain if it fits.

        Returns ``True`` when the Strain was taken. When it does not fit and ``forced`` is false, the
        character simply cannot use the cyber/drug/ability and nothing changes. When it does not fit
        and ``forced`` is true, the total is clamped at the maximum and the character is unconscious
        for at least an hour, per the SRD.
        """
        if amount < 0:
            raise StrainError("Strain additions cannot be negative")
        if self.can_absorb(amount):
            self.temporary += amount
            return True
        if forced:
            self.temporary = max(0.0, self.maximum - self.permanent)
            self.unconscious_hours = max(
                self.unconscious_hours, FORCED_OVERFLOW_UNCONSCIOUS_HOURS
            )
        return False

    def rest_night(
        self, *, hours: float = REST_HOURS_REQUIRED, warm_fed_comfortable: bool = True
    ) -> float:
        """Recover one point after a qualifying night's rest; returns what was recovered."""
        if not warm_fed_comfortable or hours < REST_HOURS_REQUIRED:
            return 0.0
        recovered = min(RECOVERY_PER_NIGHT, self.temporary)
        self.temporary -= recovered
        self.unconscious_hours = 0.0
        return recovered

    def install_cyber(self, strain: float) -> bool:
        """Add permanent Strain for an implant, if the body can support it."""
        if strain < 0:
            raise StrainError("Cyberware Strain cannot be negative")
        if self.total + strain > self.maximum:
            return False
        self.permanent += strain
        return True

    def remove_cyber(self, strain: float) -> None:
        """Remove an implant's permanent Strain, never below zero."""
        if strain < 0:
            raise StrainError("Cyberware Strain cannot be negative")
        self.permanent = max(0.0, self.permanent - strain)
