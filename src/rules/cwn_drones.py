"""Cities Without Number: drones (SRD 3.8.0-3.8.4.3).

Drones are the one CWN subsystem where the *operator's* actions, not the drone's stats, are the
scarce resource. Everything here follows from that: a control board costs you a penalty, a Remote
Control Unit costs you System Strain for a second Main Action, and no amount of pilot skill gets a
Drone-0 operator to run a Sneak-4 check through the chassis.

Transcribed from the **Cities Without Number SRD** (CC0, verified 2026-10-10 in
``data/sources/game_system_rights.json``). Section numbers are cited throughout.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

__all__ = [
    "BATTERY_HOURS",
    "DRONES",
    "FLYING_ALTITUDE_METERS",
    "MAX_CHARGE_HOURS",
    "MAX_CONTROL_METERS",
    "SAFE_CONTROL_METERS",
    "Command",
    "Controller",
    "Drone",
    "MountClass",
    "charge_hours",
    "command_capacity",
    "control_penalty",
    "drone_attack_bonuses",
    "gunnery_bonus",
    "is_destroyed",
    "mount_class",
    "parts_cost",
    "range_status",
    "skill_through_drone",
]

#: SRD 3.8.0: "a safe default control range of 1,000 meters".
SAFE_CONTROL_METERS = 1_000
#: SRD 3.8.0: "Their theoretical maximum control range is 8,000 meters."
MAX_CONTROL_METERS = 8_000
#: SRD 3.8.0: flying drones have an operational altitude maximum of 1,000 meters.
FLYING_ALTITUDE_METERS = 1_000
#: SRD 3.8.0: "Drones operate for one hour on a full battery charge."
BATTERY_HOURS = 1
#: SRD 3.8.0: "one hour of charging per Encumbrance, or six hours at most".
MAX_CHARGE_HOURS = 6

MountClass = Literal["pistol", "rifle", "heavy"]
Controller = Literal["board", "remote_control_unit"]


@dataclass(frozen=True)
class Drone:
    """One row of the SRD 3.8.1 table."""

    name: str
    cost: int
    armor_class: int
    trauma_target: int
    hit_points: int
    fittings: int
    mode: Literal["ground", "fly", "swim"]
    move_rate: int
    hardpoints: int
    encumbrance: int | None  # None: non-portable

    @property
    def portable(self) -> bool:
        return self.encumbrance is not None


#: SRD 3.8.1, in table order.
DRONES: dict[str, Drone] = {
    "Mouse": Drone("Mouse", 500, 13, 6, 1, 0, "ground", 5, 0, 1),
    "Roach": Drone("Roach", 1_000, 13, 6, 8, 3, "ground", 10, 0, 3),
    "Hummingbird": Drone("Hummingbird", 2_000, 15, 6, 5, 2, "fly", 10, 0, 3),
    "Sunfish": Drone("Sunfish", 1_000, 15, 6, 8, 3, "swim", 10, 0, 3),
    "Pitbull": Drone("Pitbull", 5_000, 15, 8, 15, 5, "ground", 20, 1, 5),
    "Javelin": Drone("Javelin", 10_000, 16, 6, 12, 5, "fly", 20, 1, 6),
    "Kerberos": Drone("Kerberos", 15_000, 18, 8, 25, 6, "ground", 20, 3, None),
    "Kraken": Drone("Kraken", 10_000, 16, 8, 20, 5, "swim", 15, 2, None),
    "Shrike": Drone("Shrike", 25_000, 18, 8, 20, 6, "fly", 30, 2, None),
}


@dataclass(frozen=True)
class Command:
    """How many drones a controller can drive at once (SRD 3.8.4)."""

    controller: Controller
    drive_skill: int

    @property
    def capacity(self) -> int:
        """A control board drives one; an RCU drives ``1 + Drive skill``."""
        if self.controller == "board":
            return 1
        return 1 + max(0, self.drive_skill)

    def can_command(self, drone_count: int) -> bool:
        return 0 <= drone_count <= self.capacity


def command_capacity(controller: Controller, drive_skill: int = 0) -> int:
    return Command(controller=controller, drive_skill=drive_skill).capacity


def control_penalty(controller: Controller, *, cranial_jack: bool = False) -> int:
    """SRD 3.8.4: a control board imposes -2 on the drone's hit rolls and skill checks.

    "If the user has a cranial jack and plugs into the board, this penalty is eliminated."
    A Remote Control Unit carries no penalty.
    """
    if controller == "board" and not cranial_jack:
        return -2
    return 0


def range_status(distance_m: float) -> Literal["safe", "hijackable", "out_of_range"]:
    """Three tiers, not two.

    Up to 1,000 m control is safe. Beyond that, "any hack or jamming attempt on a drone beyond this
    range is automatically successful" -- the signal is still *usable*, just trivially hijackable.
    Past the 8,000 m theoretical maximum there is no control to hijack.
    """
    if distance_m <= SAFE_CONTROL_METERS:
        return "safe"
    if distance_m <= MAX_CONTROL_METERS:
        return "hijackable"
    return "out_of_range"


def mount_class(drone: Drone) -> MountClass:
    """SRD 3.8.1: base Encumbrance 3 or less -> pistol-sized; larger man-portable -> rifle-sized;
    non-portable -> heavy weapons."""
    if not drone.portable:
        return "heavy"
    assert drone.encumbrance is not None
    return "pistol" if drone.encumbrance <= 3 else "rifle"


def charge_hours(drone: Drone) -> int:
    """SRD 3.8.0: "one hour of charging per Encumbrance, or six hours at most"."""
    if drone.encumbrance is None:
        return MAX_CHARGE_HOURS
    return min(MAX_CHARGE_HOURS, max(1, drone.encumbrance))


def parts_cost(drone: Drone) -> int:
    """SRD 3.8.4.3: "Spare parts for a drone cost 25% of the drone's base cost"."""
    return drone.cost // 4


def skill_through_drone(skill_level: int, drive_skill: int) -> int:
    """SRD 3.8.4.1: skill checks use the operator's level, capped at their Drive skill.

    "They may be a master infiltrator with Sneak-4, but if they've only got Drive-0 skill they can
    exert only Sneak-0 through the drone."
    """
    return max(0, min(skill_level, drive_skill))


def gunnery_bonus(
    *,
    base_attack_bonus: int,
    drive_skill: int,
    program_skill: int,
    int_modifier: int,
    dex_modifier: int,
    autonomous: bool = False,
) -> int:
    """SRD 3.8.4.1: operator's hit bonus + better of Drive/Program, modified by Int or Dex.

    An autonomous drone "usually has a native +2 bonus" and does not use the operator's numbers.
    """
    if autonomous:
        return 2
    return base_attack_bonus + max(drive_skill, program_skill) + max(int_modifier, dex_modifier)


def drone_attack_bonuses(*, weapons: int, directed_bonus: int) -> tuple[int, ...]:
    """SRD 3.8.4.2: the pilot directs **one** attack; "all others fire at the drone's usual attack
    bonus of +2".

    Returns one bonus per mounted weapon, the directed shot first. A drone with no hardpoints returns
    an empty tuple rather than a zero bonus, because it has no attacks to make.
    """
    if weapons <= 0:
        return ()
    return (directed_bonus,) + (2,) * (weapons - 1)


def is_destroyed(hit_points: int) -> bool:
    """SRD 3.8.4.3: "A drone reduced to zero hit points has been destroyed, and cannot be repaired."."""
    return hit_points <= 0
