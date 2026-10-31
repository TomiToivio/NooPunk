"""CWN core for the NoöPunk MUD (#950).

Pure Python, deterministic when given a seeded ``random.Random``: character attributes, modifiers,
saves, skill checks, attacks, damage/trauma/shock, HP and System Strain. It reads the published numbers
from ``data/rules/without_number.json`` and raises rather than guessing when a value is unsupported.

This is the first porting slice, not the full CWN rulebook: equipment, cyberware and hacking follow.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
CANON_PATH = REPO_ROOT / "data" / "rules" / "without_number.json"
ATTRIBUTES = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
DIFFICULTIES = (6, 8, 10, 12, 14)


def _canon() -> dict:
    return json.loads(CANON_PATH.read_text(encoding="utf-8"))


def attribute_modifier(score: int) -> int:
    """CWN's bounded -2..+2 modifier: 3 or less -2, 4-7 -1, 8-13 0, 14-17 +1, 18 +2."""
    if not 3 <= score <= 18:
        raise ValueError(f"attribute score {score} outside 3..18")
    for upper, modifier in _canon()["attributes"]["modifier_upper_bounds"]:
        if score <= upper:
            return int(modifier)
    raise ValueError(f"no modifier bound covers {score}")


def roll_attributes(rng: random.Random | None = None) -> dict[str, int]:
    """3d6 down the line, one roll per attribute."""
    rng = rng or random.Random()
    return {name: sum(rng.randint(1, 6) for _ in range(3)) for name in ATTRIBUTES}


def assign_array(order: Iterable[int] | None = None) -> dict[str, int]:
    """The published array assigned in STR..CHA order (14, 12, 11, 10, 9, 7 by default)."""
    values = list(order or _canon()["attributes"]["array"])
    if len(values) != len(ATTRIBUTES) or any(not 3 <= value <= 18 for value in values):
        raise ValueError("an attribute array needs six scores in 3..18")
    return dict(zip(ATTRIBUTES, values))


def hit_points(level: int, constitution: int, rolls: Iterable[int] | None = None) -> int:
    """d6 per level plus the CON modifier; the first die is maximised at level 1."""
    if level < 1:
        raise ValueError("level must be at least 1")
    mod = attribute_modifier(constitution)
    dice = list(rolls or [6] * level)
    if len(dice) != level or any(not 1 <= die <= 6 for die in dice):
        raise ValueError(f"hit point rolls must be {level} values in 1..6")
    return max(1, sum(dice) + mod * level)


def save_target(level: int, attributes: dict[str, int], category: str) -> int:
    """d20 >= 16 - level - the better modifier of the category's attribute pair."""
    pairs = _canon()["saves"]["attributes"]
    if category not in pairs:
        raise ValueError(f"unknown save category {category!r}")
    best = max((attribute_modifier(attributes[name]) for name in pairs[category]), default=0)
    return int(_canon()["saves"]["base"]) - level - best


@dataclass(frozen=True)
class Check:
    dice: tuple[int, int]
    total: int
    difficulty: int
    success: bool


def skill_check(
    rank: int,
    attribute_score: int,
    difficulty: int,
    *,
    rng: random.Random | None = None,
    dice: tuple[int, int] | None = None,
    circumstances: int = 0,
) -> Check:
    """2d6 + skill rank + attribute modifier + circumstances versus a published difficulty."""
    if not -1 <= rank <= 4:
        raise ValueError("skill rank outside -1..4")
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"difficulty {difficulty} is not a published band")
    if not -2 <= circumstances <= 2:
        raise ValueError("circumstances cap at +/-2")
    pair = dice or (lambda r: (r.randint(1, 6), r.randint(1, 6)))(rng or random.Random())
    total = pair[0] + pair[1] + rank + attribute_modifier(attribute_score) + circumstances
    return Check(pair, total, difficulty, total >= difficulty)


@dataclass(frozen=True)
class Attack:
    die: int
    total: int
    armor_class: int
    hit: bool


def attack_roll(
    attack_bonus: int,
    attribute_score: int,
    combat_rank: int,
    armor_class: int,
    *,
    rng: random.Random | None = None,
    die: int | None = None,
) -> Attack:
    """d20 + attack bonus + attribute modifier + combat skill versus AC."""
    if not -1 <= combat_rank <= 4:
        raise ValueError("combat rank outside -1..4")
    if armor_class < 1:
        raise ValueError("armour class must be positive")
    face = die if die is not None else (rng or random.Random()).randint(1, 20)
    if not 1 <= face <= 20:
        raise ValueError("attack die must be 1..20")
    total = face + attack_bonus + attribute_modifier(attribute_score) + combat_rank
    return Attack(face, total, armor_class, total >= armor_class)


def damage(weapon_die: int, rolls: Iterable[int], attribute_score: int, *, shock: int | None = None,
           trauma_die: int | None = None, trauma_roll: int | None = None,
           trauma_target: int = 6, trauma_rating: int = 1) -> dict:
    """Weapon damage and optional trauma. Shock is applied by the caller only on a miss."""
    dice = list(rolls)
    if weapon_die not in (4, 6, 8, 10, 12):
        raise ValueError("unsupported weapon die")
    if len(dice) != 1 or any(not 1 <= face <= weapon_die for face in dice):
        raise ValueError(f"damage needs one roll in 1..{weapon_die}")
    total = dice[0] + attribute_modifier(attribute_score)
    result: dict = {"damage": max(0, total), "rolls": dice, "shock": shock}
    if trauma_die is not None:
        if trauma_die not in (6, 8, 10, 12) or trauma_roll is None:
            raise ValueError("trauma needs a die and a roll")
        if not 1 <= trauma_roll <= trauma_die:
            raise ValueError("trauma roll outside its die")
        result["trauma"] = trauma_roll >= trauma_target
        result["trauma_bonus_damage"] = trauma_rating * (trauma_die // 2) if result["trauma"] else 0
    return result


def strain_max(constitution: int) -> int:
    """Permanent System Strain capacity equals CON."""
    return constitution


def strain_absorb(current: int, amount: int, constitution: int) -> dict:
    """Absorb strain up to CON; overflow is refused, never silently clamped."""
    if amount < 0 or current < 0:
        raise ValueError("strain values cannot be negative")
    capacity = strain_max(constitution)
    if current + amount > capacity:
        return {"ok": False, "current": current, "capacity": capacity, "overflow": current + amount - capacity}
    return {"ok": True, "current": current + amount, "capacity": capacity, "overflow": 0}


# --- Action economy, encumbrance, shock and catalogue lookups (#950) ------------------------------
# Numbers are transcribed from the CWN SRD and the existing Python/Godot kernels; this module does
# not invent alternatives.

CATALOGUE_PATH = REPO_ROOT / "data" / "rules" / "cwn_catalogue.json"

ACTION_ECONOMY = {
    "main_per_round": 1,
    "move_per_round": 1,
    "snap_attack_penalty": -4,
    "charge_to_hit": 2,
    "charge_ac_penalty": -2,
    "charge_min_metres": 3.0,
    "swarm_per_other_hit": 2,
    "swarm_max_other": 3,
    "total_defense_ac": 2,
}

READIED_DIVISOR = 2
OVERLOAD_READIED_BONUS = 2
OVERLOAD_STOWED_BONUS = 4
BASE_MOVE_METRES = 10.0


def _catalogue() -> dict:
    return json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))


def weapon(weapon_id: str) -> dict:
    for row in _catalogue()["weapons"]:
        if row["id"] == weapon_id:
            return row
    raise ValueError(f"unknown weapon {weapon_id!r}")


def armour(armour_id: str) -> dict:
    for row in _catalogue()["armor"]:
        if row["id"] == armour_id:
            return row
    raise ValueError(f"unknown armour {armour_id!r}")


def shock_on_miss(weapon_id: str, target_ac: int) -> int:
    """Shock damage applies on a miss when the target's AC is at or below the weapon's Shock AC."""
    shock = weapon(weapon_id).get("shock")
    if not shock or target_ac > int(shock["ac"]):
        return 0
    return int(shock["damage"])


def combat_action(action: str, *, main_unspent: bool = True) -> dict:
    """The published modifiers for the named combat actions."""
    if action == "snap":
        if not main_unspent:
            raise ValueError("Snap Attack needs an unspent Main action")
        return {"to_hit": ACTION_ECONOMY["snap_attack_penalty"]}
    if action == "charge":
        return {"to_hit": ACTION_ECONOMY["charge_to_hit"], "ac": ACTION_ECONOMY["charge_ac_penalty"],
                "min_distance_metres": ACTION_ECONOMY["charge_min_metres"]}
    if action == "total_defense":
        if not main_unspent:
            raise ValueError("Total Defense needs an unspent Main action")
        return {"ac": ACTION_ECONOMY["total_defense_ac"], "immune_to_shock": True}
    if action == "swarm":
        return {"per_other_to_hit": ACTION_ECONOMY["swarm_per_other_hit"],
                "max_other": ACTION_ECONOMY["swarm_max_other"]}
    raise ValueError(f"unknown combat action {action!r}")


def encumbrance(strength: int, *, stowed: float = 0.0, readied: float = 0.0) -> dict:
    """Fits and movement tier: base limits, then +2 Readied/+4 Stowed per overload step.

    One step costs 30 % of Move (10 m -> 7 m), the second 50 % (10 m -> 5 m); beyond that the load
    cannot be hauled any significant distance.
    """
    if not 3 <= strength <= 18:
        raise ValueError("strength outside 3..18")
    if stowed < 0 or readied < 0:
        raise ValueError("load cannot be negative")
    stowed_max = float(strength)
    readied_max = float(strength // READIED_DIVISOR)
    for step in range(3):
        limit_stowed = stowed_max + step * OVERLOAD_STOWED_BONUS
        limit_readied = readied_max + step * OVERLOAD_READIED_BONUS
        if stowed <= limit_stowed and readied <= limit_readied:
            speed = BASE_MOVE_METRES * (1.0 if step == 0 else 0.7 if step == 1 else 0.5)
            return {"fits": True, "overload_steps": step, "stowed_max": limit_stowed,
                    "readied_max": limit_readied, "speed_metres": speed}
    return {"fits": False, "overload_steps": 3, "stowed_max": stowed_max + 2 * OVERLOAD_STOWED_BONUS,
            "readied_max": readied_max + 2 * OVERLOAD_READIED_BONUS, "speed_metres": 0.0}
