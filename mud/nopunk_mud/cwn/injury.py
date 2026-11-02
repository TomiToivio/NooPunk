"""Mortal injury, stabilization, Frailty and Major Injuries (#1068).

From the Cities Without Number SRD (public domain), Injury/Healing:

* Zero hit points from lethal damage means Mortally Wounded: death at the end of the sixth round unless
  stabilized.
* Stabilizing is a Main Action, Dex/Heal or Int/Heal, difficulty **8 + full rounds since the fall**, +2
  without a medkit; one attempt per round.
* A stabilized victim is incapacitated for ten minutes, then recovers with 1 hit point and the **Frail**
  condition. Zero hit points again while Frail is instant death. Frailty clears after a week of rest, or a
  physician's difficulty-10 check with an hour and a medkit.
* A Traumatic Hit followed by reaching zero in the same scene forces a Physical save; failing rolls 1d12 on
  the Major Injury table.
* Non-lethal damage to zero: incapacitated ten minutes, then 1 hit point, no Frailty.
"""
from __future__ import annotations

from dataclasses import dataclass, field

MORTAL_ROUNDS = 6
RECOVERY_MINUTES = 10
NO_MEDKIT_PENALTY = 2

#: d12 -> injury. Roll clamped to 1..12.
MAJOR_INJURIES: dict[int, str] = {
    1: "instant_death",
    2: "internal_damage",
    3: "brain_damage",
    4: "eye_damage",
    5: "gut_wound",
    6: "right_leg_ruined",
    7: "left_leg_ruined",
    8: "right_arm_ruined",
    9: "left_arm_ruined",
    10: "system_damage",
    11: "flesh_wound",
    12: "flesh_wound",
}

#: Injuries that leave a character dead without intervention.
LETHAL_INJURIES = frozenset({"instant_death"})
#: Injuries that require a street doc's clinic within the hour.
CLINIC_INJURIES = frozenset({"internal_damage", "gut_wound"})


class InjuryError(ValueError):
    """An injury state transition the rules do not allow."""


@dataclass
class MortalState:
    """One character's path through zero hit points."""

    rounds_down: int = 0
    stabilized: bool = False
    frail: bool = False
    dead: bool = False
    major_injury: str | None = None
    notes: list[str] = field(default_factory=list)

    def tick(self) -> None:
        """Advance one round. Returns nothing; the state answers `is_dead`."""
        if self.dead or self.stabilized:
            return
        self.rounds_down += 1
        if self.rounds_down >= MORTAL_ROUNDS:
            self.dead = True
            self.notes.append("died: six rounds without stabilization")

    @property
    def is_dead(self) -> bool:
        return self.dead

    @property
    def is_helpless(self) -> bool:
        return not self.dead and not self.stabilized


def stabilization_difficulty(*, rounds_since_fall: int, has_medkit: bool = True) -> int:
    if rounds_since_fall < 0:
        raise InjuryError("rounds cannot be negative")
    return 8 + rounds_since_fall + (0 if has_medkit else NO_MEDKIT_PENALTY)


def try_stabilize(state: MortalState, *, total: int, has_medkit: bool = True) -> bool:
    """One attempt. On success the victim is stable and will recover in ten minutes."""
    if state.dead:
        raise InjuryError("the dead do not stabilize")
    if state.stabilized:
        return True
    difficulty = stabilization_difficulty(rounds_since_fall=state.rounds_down, has_medkit=has_medkit)
    if total >= difficulty:
        state.stabilized = True
        state.notes.append(f"stabilized at difficulty {difficulty}")
        return True
    state.notes.append(f"failed stabilization at difficulty {difficulty}")
    return False


def recover(state: MortalState) -> dict[str, object]:
    """After ten minutes of being stable: 1 hp and Frail."""
    if not state.stabilized or state.dead:
        raise InjuryError("recovery needs a stabilized, living victim")
    state.frail = True
    state.notes.append("recovered with 1 hp and Frail")
    return {"hit_points": 1, "frail": True}


def zero_hit_points_while_frail(state: MortalState) -> None:
    if not state.frail:
        raise InjuryError("not Frail; this is an ordinary mortal wound")
    state.dead = True
    state.notes.append("died: reduced to zero while Frail")


def clear_frailty(state: MortalState, *, method: str, total: int | None = None) -> bool:
    """A week of bed rest, or a physician's difficulty-10 check (medkit, one hour)."""
    if method == "rest":
        state.frail = False
        return True
    if method == "physician":
        if total is None:
            raise InjuryError("a physician's attempt needs a check total")
        if total >= 10:
            state.frail = False
            return True
        return False
    raise InjuryError(f"unknown frailty treatment {method!r}")


def major_injury(roll: int) -> dict[str, object]:
    """The d12 table, clamped. Returned as data so a caller can render or persist it."""
    clamped = max(1, min(12, roll))
    injury = MAJOR_INJURIES[clamped]
    return {
        "roll": clamped,
        "injury": injury,
        "lethal": injury in LETHAL_INJURIES,
        "needs_clinic_within_hour": injury in CLINIC_INJURIES,
        "limb_lost": injury.endswith("_ruined"),
    }


def major_injury_save_required(*, traumatic_hit: bool, reached_zero_same_scene: bool) -> bool:
    return traumatic_hit and reached_zero_same_scene


def nonlethal_incapacitation() -> dict[str, object]:
    return {"minutes": RECOVERY_MINUTES, "hit_points": 1, "frail": False}
