"""Cyberware surgery, skillplugs and concealment (#1068).

From the Cities Without Number SRD (public domain), Gear/Vehicles/Cyberware:

* Implantation cost, recovery time and difficulty are a function of the implant's System Strain.
* The surgeon's check is Int/Heal or Dex/Heal; the theatre and the implant's condition modify it.
* Failing by more than two is a failed operation: System Strain maxes out and the patient drops to 1 hp.
  Failing by one or two installs the cyber but imposes an implant complication.
* Removing safely is the same difficulty as installing; a rushed removal is automatic and often fatal.
* Skillplugs: level 0-1 commonly, 2 rare, 3 mission-only; physical skills cost double and need a
  Skillplug Jack II. A natural 2 on a skillplug-augmented check (or a natural 1 on an attack) is an
  automatic failure that no reroll can save, and the jack locks for the scene. Each additional plug
  widens that failure range by one.
"""
from __future__ import annotations

from dataclasses import dataclass

#: strain ceiling (inclusive) -> (cost, recovery, difficulty). The SRD's last band is open-ended.
INSTALL_TABLE: tuple[tuple[float, int, str, int], ...] = (
    (0.0, 100, "1 hour", 7),
    (0.5, 500, "1 day", 8),
    (1.0, 2_500, "4 days", 10),
    (3.0, 12_500, "2 weeks", 11),
)

#: Applied to the implanting check.
SURGERY_MODIFIERS: dict[str, int] = {
    "cyberdoc_kit": -1,
    "no_dedicated_room": -1,
    "theater_1": 0,
    "theater_2": 1,
    "theater_3": 2,
    "clean_room": 0,
    "sterile_operating_room": 1,
    "full_clinic": 2,
    "new_implant": 1,
}

#: Skillplug prices by plug level. Physical skills cost double.
SKILLPLUG_PRICES: dict[int, int | None] = {0: 1_000, 1: 10_000, 2: 50_000, 3: None}

#: Concealment ratings, from least visible to most.
CONCEALMENT = ("medical", "touch", "sight")


class CyberwareError(ValueError):
    """An implant operation the rules do not allow."""


@dataclass(frozen=True)
class Operation:
    """The outcome of one implantation or removal attempt."""

    success: bool
    complication: bool = False
    strain_maxed: bool = False
    hp_set_to: int | None = None
    implant_reusable: bool = True
    note: str = ""


def install_difficulty(strain: float) -> int:
    if strain < 0:
        raise CyberwareError("System Strain cannot be negative")
    for ceiling, _cost, _recovery, difficulty in INSTALL_TABLE:
        if strain <= ceiling:
            return difficulty
    return 12  # "3.1 or more"


def install_cost(strain: float) -> int:
    if strain < 0:
        raise CyberwareError("System Strain cannot be negative")
    for ceiling, cost, _recovery, _difficulty in INSTALL_TABLE:
        if strain <= ceiling:
            return cost
    return 50_000


def recovery_time(strain: float) -> str:
    for ceiling, _cost, recovery, _difficulty in INSTALL_TABLE:
        if strain <= ceiling:
            return recovery
    return "1 month"


def surgery_modifier(*, circumstances: list[str]) -> int:
    total = 0
    for name in circumstances:
        if name not in SURGERY_MODIFIERS:
            raise CyberwareError(f"unknown surgery circumstance {name!r}")
        total += SURGERY_MODIFIERS[name]
    return total


def install_outcome(*, margin: int, strain: float) -> Operation:
    """`margin` = check total - difficulty. Failing **by more than two** fails the operation."""
    if margin >= 0:
        return Operation(success=True)
    if margin <= -3:
        return Operation(
            success=False,
            strain_maxed=True,
            hp_set_to=1,
            implant_reusable=True,  # survives, but now counts as used cyber
            note="operation failed: strain maxed, patient at 1 hp",
        )
    return Operation(success=True, complication=True, note="implant complication")


def remove_outcome(*, margin: int, patient_alive: bool = True) -> Operation:
    """A failed removal ruins the implant; the patient survives a careful one."""
    if not patient_alive:
        if margin >= 0:
            return Operation(success=True, note="salvaged intact")
        return Operation(success=False, implant_reusable=False, note="ruined in salvage")
    if margin >= 0:
        return Operation(success=True, note="removed intact")
    return Operation(success=True, implant_reusable=False, note="removed, implant ruined")


def cyberdoc_heal_check(difficulty: int, *, skill: int, attribute_modifier: int, roll: int,
                        circumstances: list[str] | None = None) -> Operation:
    margin = roll + skill + attribute_modifier + surgery_modifier(circumstances=circumstances or []) - difficulty
    return Operation(success=margin >= 0, note=f"margin {margin:+d}")


def skillplug_price(level: int, *, physical: bool = False) -> int | None:
    if level not in SKILLPLUG_PRICES:
        raise CyberwareError("skillplug levels run 0..3")
    price = SKILLPLUG_PRICES[level]
    if price is None:
        return None  # mission-only
    return price * 2 if physical else price


def skillplug_requires_jack_ii(*, physical: bool) -> bool:
    return physical


def skillplug_failure_range(*, plugs_running: int = 1) -> int:
    """Natural roll at which the plug auto-fails and the jack locks, counting additional plugs."""
    if plugs_running < 1:
        raise CyberwareError("at least one plug must be running")
    return 1 + plugs_running  # one plug: natural 2 (skill) / 1 (attack); each extra widens by one


def skillplug_check_fails(*, die: int, attack: bool, plugs_running: int = 1) -> bool:
    threshold = skillplug_failure_range(plugs_running=plugs_running) - (1 if attack else 0)
    return die <= threshold


def detectability(rating: str, *, method: str) -> bool:
    """Can a given method notice this class of implant?"""
    if rating not in CONCEALMENT:
        raise CyberwareError(f"unknown concealment rating {rating!r}")
    if method == "medical_exam" or method == "cyber_scanner":
        return True
    if method == "visual":
        return rating == "sight"
    if method == "touch":
        return rating in {"touch", "sight"}
    raise CyberwareError(f"unknown detection method {method!r}")
