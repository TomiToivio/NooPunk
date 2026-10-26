"""Mortal wounds, stabilization, Frail, first aid and System Strain.

Original implementation of the numerical procedures in the Cities Without Number
SRD, "Injury, Healing, and System Strain". The prose here is ours; no SRD text
is reproduced. Every number the SRD leaves open is left open here too rather
than being invented for convenience.

The layer is deliberately about *time and consequence* rather than damage:
being dropped starts a clock, stabilizing stops the clock but changes what the
character can do for a week, and every act of modern medicine is paid for in
System Strain rather than in money.
"""
from __future__ import annotations

from dataclasses import dataclass

MORTAL_WOUND_ROUNDS = 6
STABILIZE_BASE_DIFFICULTY = 8
NO_MEDKIT_PENALTY = 2
FRAIL_REMOVAL_DIFFICULTY = 10
STABILIZED_REST_MINUTES = 10
FRAIL_BED_REST_WEEK = 7


class HealingRulesError(ValueError):
    """Raised when a call is outside the procedure rather than merely unlucky."""


@dataclass
class SystemStrain:
    """A body's tolerance for biochemical manipulation, capped by Constitution.

    ``permanent`` holds the share from cyberware and other lasting changes: those
    points never come back while the implant is in place, so they are tracked
    apart from what a night's sleep can clear.
    """

    constitution: int
    current: int = 0
    permanent: int = 0

    def __post_init__(self) -> None:
        if self.constitution < 1:
            raise HealingRulesError("Constitution must be at least 1")
        if self.permanent < 0 or self.current < 0:
            raise HealingRulesError("System Strain cannot be negative")
        if self.permanent > self.constitution:
            raise HealingRulesError("permanent strain cannot exceed the maximum")

    @property
    def maximum(self) -> int:
        return self.constitution

    @property
    def shedable(self) -> int:
        return max(0, self.current - self.permanent)

    def can_accept(self, amount: int = 1) -> bool:
        """A body already at its maximum gains nothing from further intervention."""
        if amount < 0:
            raise HealingRulesError("strain cannot be negative")
        return self.current + amount <= self.maximum

    def add(self, amount: int = 1) -> bool:
        """Apply strain if there is room; report whether the effect took hold."""
        if not self.can_accept(amount):
            return False
        self.current += amount
        return True

    def add_permanent(self, amount: int) -> None:
        """Cyberware and similar: taken from the ceiling permanently."""
        if amount < 0:
            raise HealingRulesError("strain cannot be negative")
        if self.current + amount > self.maximum:
            raise HealingRulesError("an implant that exceeds the maximum is not installable")
        self.current += amount
        self.permanent += amount

    def nights_sleep(self, nights: int = 1) -> int:
        """One shedable point leaves per night of good sleep; permanent never does."""
        if nights < 0:
            raise HealingRulesError("nights cannot be negative")
        shed = min(self.shedable, nights)
        self.current -= shed
        return shed


@dataclass
class Patient:
    """Just enough state to run the procedures."""

    hit_points: int
    level_or_hit_dice: int
    frail: bool = False
    downed_round: int | None = None

    def __post_init__(self) -> None:
        if self.hit_points < 0:
            raise HealingRulesError("hit points cannot be negative")
        if self.level_or_hit_dice < 1:
            raise HealingRulesError("level or hit dice is at least 1")

    @property
    def mortally_wounded(self) -> bool:
        """Zero hit points from a lethal attack means dying, not merely resting."""
        return self.hit_points <= 0

    def rounds_until_death(self, current_round: int) -> int:
        """Rounds left before the sixth round after downing has passed."""
        if self.downed_round is None:
            raise HealingRulesError("this patient has not been downed")
        if current_round < self.downed_round:
            raise HealingRulesError("the current round cannot precede the downing")
        return max(0, MORTAL_WOUND_ROUNDS - (current_round - self.downed_round))


def stabilize_difficulty(rounds_since_downed: int, *, has_medkit: bool = True) -> int:
    """Difficulty 8 plus each full round elapsed, two harder without a medkit."""
    if rounds_since_downed < 0:
        raise HealingRulesError("rounds since downing cannot be negative")
    return STABILIZE_BASE_DIFFICULTY + rounds_since_downed + (0 if has_medkit else NO_MEDKIT_PENALTY)


def stabilized(patient: Patient) -> Patient:
    """A stabilized patient wakes with one hit point after ten minutes, and is Frail.

    Frailty is the cost of surviving: the character acts normally but cannot heal
    naturally and dies outright at zero until a week of bed rest has passed.
    """
    if not patient.mortally_wounded:
        raise HealingRulesError("only a mortally wounded patient needs stabilizing")
    patient.hit_points = 1
    patient.frail = True
    patient.downed_round = None
    return patient


def remove_frailty(*, skill_total: int, difficulty: int = FRAIL_REMOVAL_DIFFICULTY,
                   already_attempted: bool = False) -> dict[str, bool]:
    """One medkit, one hour, one roll - and only one chance per Frailty.

    Returns what happened rather than mutating, because "the medic gets one
    attempt" is a state a caller has to keep.
    """
    if already_attempted:
        return {"allowed": False, "succeeded": False}
    return {"allowed": True, "succeeded": skill_total >= difficulty}


def natural_healing(patient: Patient) -> int:
    """A night's rest restores level or hit dice in HP - but never to the Frail."""
    if patient.frail:
        return 0
    return patient.level_or_hit_dice


def frail_week(*, has_medic_care: bool, physical_save_success: bool | None = None) -> str:
    """The week of bed rest that decides whether frailty ends or kills.

    With Heal-0 care and a medkit the frailty simply ends. Without it, a Physical
    save decides: failure means death within days, success means another month.
    """
    if has_medic_care:
        return "recovered"
    if physical_save_success is None:
        raise HealingRulesError("without care, the week needs its Physical save")
    return "month_more" if physical_save_success else "dying"


def first_aid(*, die_roll: int, heal_skill: int = 0, has_medkit: bool = True,
              strain: SystemStrain | None = None) -> dict[str, int | bool]:
    """Minutes of care: 1d6 plus Heal level, or 1d6-1 with no Heal skill at all.

    Each application costs the patient one System Strain, and a body at its
    maximum gains nothing - the intervention is simply too much for it.
    """
    if not has_medkit:
        raise HealingRulesError("first aid needs a medkit")
    if die_roll < 1:
        raise HealingRulesError("a die roll is at least 1")
    if heal_skill < 0:
        raise HealingRulesError("Heal skill cannot be negative")

    healed = die_roll + heal_skill if heal_skill > 0 else die_roll - 1
    healed = max(0, healed)

    if strain is not None and not strain.can_accept(1):
        return {"healed": 0, "strain_added": 0, "refused": True}
    if strain is not None:
        strain.add(1)
    return {"healed": healed, "strain_added": 1 if strain is not None else 0, "refused": False}
