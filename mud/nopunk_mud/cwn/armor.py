"""Armor accessories and obsolete gear (#1068).

From the Cities Without Number SRD (public domain), Armor:

* Accessories cannot be applied twice to one suit, cannot be modded, and cannot go on the three
  suit-armor systems.
* A riot shield negates the first melee Shock a bearer takes in a round, and only one shield helps.
* Absorption plates and joint reinforcement each cost -1 on Sneak and Exert.
* Obsolete armor is half price, then loses 1d2 AC (floor 10) and 1d4 Damage Soak (floor 0) — rolled
  after purchase, so the buyer does not know what they bought.
"""
from __future__ import annotations

SUIT_ARMOR = frozenset({"armored_suit", "combat_suit", "heavy_suit"})
ACCESSORIES = ("riot_shield", "absorption_plates", "joint_reinforcement")
AC_FLOOR = 10


class ArmorError(ValueError):
    """An armour combination the rules forbid."""


def can_attach(accessory: str, *, base_armor: str, already: tuple[str, ...] = ()) -> bool:
    if accessory not in ACCESSORIES:
        raise ArmorError(f"unknown accessory {accessory!r}")
    if base_armor in SUIT_ARMOR:
        # A riot shield may still be carried with a suit; it is not attached to it.
        return accessory == "riot_shield"
    if accessory in already:
        return False  # "a given accessory can only be applied once"
    return True


def stealth_exert_penalty(accessories: tuple[str, ...]) -> int:
    """Absorption plates and joint reinforcement each hinder movement."""
    return -sum(1 for a in ("absorption_plates", "joint_reinforcement") if a in accessories)


def shock_absorbed(*, shield: bool, melee_shock: int, shields_carried: int = 1) -> int:
    """A shield negates the first melee Shock of the round; extra arms do not stack it."""
    if not shield or shields_carried < 1:
        return 0
    return min(melee_shock, 1)


def obsolete_armor(*, ac_ranged: int, ac_melee: int, soak: int, ac_roll: int, soak_roll: int,
                   cost: int) -> dict[str, int]:
    """Rolled after purchase: AC drops 1d2 (floor 10), Soak 1d4 (floor 0), price halved."""
    if ac_roll not in (1, 2):
        raise ArmorError("the AC penalty is 1d2")
    if not 1 <= soak_roll <= 4:
        raise ArmorError("the Soak penalty is 1d4")
    return {
        "ac_ranged": max(AC_FLOOR, ac_ranged - ac_roll),
        "ac_melee": max(AC_FLOOR, ac_melee - ac_roll),
        "damage_soak": max(0, soak - soak_roll),
        "cost": cost // 2,
    }
