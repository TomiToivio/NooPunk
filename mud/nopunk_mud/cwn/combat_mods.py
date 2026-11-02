"""Attack modifiers and combat maneuvers (#1068).

From the Cities Without Number SRD (public domain), Combat:

* The attack roll is 1d20 + base attack + attribute modifier + combat skill; lacking even level-0 in the
  combat skill is -2. Meeting the target's Melee/Ranged AC hits.
* The situational table is finite and cited; "N/A" is not a penalty, it is "this action is not possible".
* Shove and grapple are opposed Str/Exert or Str/Punch checks after a successful melee attack that does no
  damage. Larger-than-human targets cost -2, quadrupeds -4.
* Dual-wielding requires level-1 in the weapon skills and adds +2 damage (never to Shock).
"""
from __future__ import annotations

#: Circumstance -> modifier. ``None`` means the action cannot be attempted as described.
ATTACK_MODIFIERS: dict[str, int | None] = {
    "target_prone_not_in_melee": -2,
    "target_prone_adjacent": 2,
    "beyond_normal_range": -2,
    "prone_melee_attack": -4,
    "target_half_cover": -2,
    "target_almost_full_cover": -4,
    "thrown_while_in_melee": -4,
    "one_handed_gun_in_melee": -4,
    "two_handed_gun_in_melee": None,
    "unseen_target_known_position": -4,
    "unseen_target_unknown_position": None,
}

#: Unskilled combat penalty (no level-0 in the relevant combat skill).
UNSKILLED_PENALTY = -2

#: Opposed-maneuver penalty by target size.
SIZE_MODIFIERS: dict[str, int] = {"human": 0, "large_humanoid": -2, "quadruped": -4}

#: Dual-wielding damage bonus, never applied to Shock.
DUAL_WIELD_DAMAGE = 2


class CombatRuleError(ValueError):
    """A manoeuvre the rules do not allow."""


def attack_total(
    *,
    die: int,
    base_attack: int,
    attribute_modifier: int,
    combat_skill: int,
    circumstances: list[str] | None = None,
    gunlink: bool = False,
) -> dict[str, object]:
    """One attack roll. Raises when a listed circumstance makes the attack impossible."""
    # Untrained is a flat -2, not the rank penalty plus a penalty: the SRD replaces the skill
    # contribution rather than stacking on it.
    skill_part = combat_skill if combat_skill >= 0 else UNSKILLED_PENALTY
    total = die + base_attack + attribute_modifier + skill_part
    for name in circumstances or []:
        if name not in ATTACK_MODIFIERS:
            raise CombatRuleError(f"unknown combat circumstance {name!r}")
        modifier = ATTACK_MODIFIERS[name]
        if modifier is None:
            raise CombatRuleError(f"{name} cannot be attempted")
        # Gunlink ignores 2 points of cover/concealment penalty and long-range penalty.
        if gunlink and name in {"target_half_cover", "target_almost_full_cover", "beyond_normal_range"}:
            total += min(0, modifier + 2)
        else:
            total += modifier
    return {"total": total, "unskilled": combat_skill < 0}


def hits(*, total: int, armor_class: int) -> bool:
    return total >= armor_class


def opposed_maneuver(*, attacker_total: int, defender_total: int, target_size: str = "human") -> bool:
    if target_size not in SIZE_MODIFIERS:
        raise CombatRuleError(f"unknown target size {target_size!r}")
    return attacker_total + SIZE_MODIFIERS[target_size] >= defender_total


def grapple_holds(*, attacker_won: bool) -> dict[str, object]:
    """A grappled victim is fixed, fights unarmed only, and takes unarmed damage each round end."""
    if not attacker_won:
        return {"grappled": False}
    return {
        "grappled": True,
        "movement": "no",
        "attacks": "unarmed only",
        "round_end_damage": "assailant's unarmed damage",
        "escape": "Main Action, opposed Str/Punch",
    }


def dual_wield(*, damage: int, shock: int = 0, weapon_ranks: tuple[int, int] = (1, 1),
               target_in_range_of_both: bool = True) -> dict[str, int]:
    """+2 damage when both weapons are in range and both skills are at least level 1."""
    if min(weapon_ranks) < 1:
        raise CombatRuleError("dual-wielding needs level-1 in the relevant weapon skills")
    if not target_in_range_of_both:
        return {"damage": damage, "shock": shock, "bonus_applied": 0}
    return {"damage": damage + DUAL_WIELD_DAMAGE, "shock": shock, "bonus_applied": DUAL_WIELD_DAMAGE}
