"""Cities Without Number: crafting, gear mods, and mod maintenance.

One module owns the three questions a modded stat line keeps asking:

* **may this tech build or maintain it?** (``min_fix``, the maintenance score);
* **how long does it take and what does it cost?** (weeks per minimum skill
  level, assistant/obsessive halving, the three quality grades);
* **what does it do to the row?** (:func:`apply_weapon_mods`,
  :func:`apply_armor_mods`, :func:`apply_drone_mods`, :func:`apply_deck_mods`).

The catalogue is ``data/rules/cwn_gear_mods.json``; vehicle mods stay in
``data/rules/cwn_vehicles.json`` because their price is a percentage of a hull.
Transcribed from the **Cities Without Number SRD** (CC0): sections 2.8, 3.1.3,
3.4.5, 3.8.2 and 3.9.1.

## The two rules this module exists to keep straight

1. **Mod bonuses to hit, damage and Shock cap at +3 combined.** Shock Burst's 2d6
   is explicitly outside that cap (:data:`MOD_BONUS_CAP`), so it is reported as a
   separate, uncapped value instead of being folded into ``damage_bonus``.
2. **Maintenance is a skill gate and a count, not a cost.** A tech who lacks the
   mod's minimum Fix cannot maintain it at all, and the number of mods they can
   keep alive is ``INT mod + CON mod + 3 x Fix``. Nothing here is a dice penalty.
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

MODS_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "cwn_gear_mods.json"

MOD_BONUS_CAP = {"hit": 3, "damage": 3, "shock": 3}


class ModError(ValueError):
    """A mod was asked for that the contract does not allow on that item."""


@lru_cache(maxsize=2)
def load_mods(path: str | Path | None = None) -> dict[str, Any]:
    return json.loads(Path(path or MODS_PATH).read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Mod:
    id: str
    name: str
    kind: str
    min_fix: int
    min_drive: int = 0
    min_heal: int = 0
    cost: int = 0
    cost_percent: int = 0
    components: int = 0
    applies_to: tuple[str, ...] = ()
    requires_connection: tuple[str, ...] = ()
    requires_mod: str | None = None
    effects: Mapping[str, Any] = field(default_factory=dict)

    def price(self, base_cost: int = 0) -> int:
        """Absolute mods carry a dollar price; drone, deck and hull mods a percentage."""
        if self.cost_percent:
            if base_cost <= 0:
                raise ModError(f"{self.name} is priced as a percentage; pass the item's base cost")
            return round(base_cost * self.cost_percent / 100)
        return self.cost


def _mods(kind: str) -> Iterable[dict]:
    rows = load_mods().get(kind)
    if not isinstance(rows, list):
        raise ModError(f"contract has no {kind!r} list")
    return rows


def _build(kind: str, row: Mapping[str, Any]) -> Mod:
    skills = row.get("skills") or {}
    return Mod(
        id=str(row["id"]), name=str(row["name"]), kind=kind,
        min_fix=int(row.get("min_fix", skills.get("Fix", 0))),
        min_drive=int(row.get("min_drive", skills.get("Drive", 0))),
        min_heal=int(row.get("min_heal", skills.get("Heal", 0))),
        cost=int(row.get("cost", 0)), cost_percent=int(row.get("cost_percent", 0)),
        components=int(row.get("components", 0)),
        applies_to=tuple(row.get("applies_to") or ()),
        requires_connection=tuple(row.get("requires_connection") or ()),
        requires_mod=row.get("requires_mod"), effects=row.get("effects") or {},
    )


def weapon_mod(mod_id: str) -> Mod:
    for row in _mods("weapon_mods"):
        if row["id"] == mod_id:
            return _build("weapon", row)
    raise ModError(f"unknown weapon mod: {mod_id}")


def armor_mod(mod_id: str) -> Mod:
    for row in _mods("armor_mods"):
        if row["id"] == mod_id:
            return _build("armor", row)
    raise ModError(f"unknown armor mod: {mod_id}")


def drone_mod(mod_id: str) -> Mod:
    for row in _mods("drone_mods"):
        if row["id"] == mod_id:
            return _build("drone", row)
    raise ModError(f"unknown drone mod: {mod_id}")


def deck_mod(mod_id: str) -> Mod:
    for row in _mods("deck_mods"):
        if row["id"] == mod_id:
            return _build("deck", row)
    raise ModError(f"unknown deck mod: {mod_id}")


def all_mods() -> dict[str, Mod]:
    found: dict[str, Mod] = {}
    for kind, build in (("weapon_mods", weapon_mod), ("armor_mods", armor_mod),
                        ("drone_mods", drone_mod), ("deck_mods", deck_mod)):
        for row in _mods(kind):
            found[f"{kind}:{row['id']}"] = build(str(row["id"]))
    return found


# --------------------------------------------------------------------------- #
# Maintenance (SRD 2.8.3)
# --------------------------------------------------------------------------- #


def maintenance_score(int_modifier: int, con_modifier: int, fix_skill: int, *,
                      full_time: bool = False) -> int:
    """How many mods one tech can keep working.

    ``INT mod + CON mod + 3 x Fix``; a tech doing nothing but maintenance doubles
    it, which is the SRD's sixteen-hour-workday clause. The score never goes below
    zero — a negative total means "none", not "anti-maintenance".
    """
    if fix_skill < 0:
        raise ModError("Fix skill is a trained rank 0..4; untrained cannot maintain mods")
    score = int_modifier + con_modifier + 3 * int(fix_skill)
    if full_time:
        score *= int(load_mods()["maintenance"]["full_time_multiplier"])
    return max(0, score)


def can_build(fix_skill: int, mod: Mod, *, drive_skill: int = 0, heal_skill: int = 0) -> bool:
    return fix_skill >= mod.min_fix and drive_skill >= mod.min_drive and heal_skill >= mod.min_heal


def can_maintain(fix_skill: int, mod: Mod) -> bool:
    """A tech may only maintain mods they could have built."""
    return fix_skill >= mod.min_fix


def install_weeks(mod: Mod, *, assistant: bool = False, obsessive: bool = False) -> int:
    """One week per minimum skill level, halved by an assistant, then by obsession."""
    rules = load_mods()["crafting"]
    weeks = (mod.min_fix + mod.min_heal) * int(rules["weeks_per_minimum_skill_level"])
    if weeks == 0:
        # A Fix-0 mod still takes a week of workshop time, never zero.
        weeks = 1
    if assistant:
        weeks = math.ceil(weeks / int(rules["assistant_time_divisor"]))
    if obsessive:
        weeks = math.ceil(weeks / int(rules["obsessive_time_divisor"]))
    return max(1, weeks)


def maintenance_lapse(*, hours_without: float) -> str:
    """``working``, ``mod_dead`` or ``item_dead`` — the SRD's 24 h and 7 day clocks."""
    rules = load_mods()["maintenance"]
    if hours_without >= int(rules["lapse_days_item_stops"]) * 24:
        return "item_dead"
    if hours_without >= int(rules["lapse_hours_mod_stops"]):
        return "mod_dead"
    return "working"


# --------------------------------------------------------------------------- #
# Crafting (SRD 2.8.1)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class CraftPlan:
    quality: str
    days: int
    parts_cost: int
    counts_as_mod_requiring_fix: int | None
    stops_after_hours: int | None
    further_modding: bool
    first_mod_needs_no_maintenance: bool


def craft_plan(quality: str, market_cost: int, *, vehicle: bool = False) -> CraftPlan:
    """Jury-rigged, normal or mastercrafted: time, parts bill, and the strings attached."""
    rules = load_mods()["crafting"]
    if quality not in rules["quality"]:
        raise ModError(f"unknown crafting quality: {quality}")
    grade = rules["quality"][quality]
    base_days = int(rules["build_time_days"]["vehicle" if vehicle else "portable_complex_device"])
    divisor = int(grade.get("time_divisor", 1))
    multiplier = int(grade.get("time_multiplier", 1))
    days = math.ceil(base_days * multiplier / divisor)
    parts = round(market_cost * int(grade["parts_percent_of_market"]) / 100)
    return CraftPlan(
        quality=quality, days=days, parts_cost=parts,
        counts_as_mod_requiring_fix=grade.get("counts_as_mod"),
        stops_after_hours=grade.get("stops_after_hours_without_maintenance"),
        further_modding=bool(grade.get("further_modding", True)),
        first_mod_needs_no_maintenance=bool(grade.get("first_mod_needs_no_maintenance", False)),
    )


def factory_price(base_cost: int, mod_cost: int, components: int = 0) -> int:
    """Factory-modded gear starts at five times the mod's build price, then doubles per component."""
    if base_cost < 0 or mod_cost < 0 or components < 0:
        raise ModError("costs and component counts cannot be negative")
    price = base_cost + 5 * mod_cost
    return price * (2 ** components)


# --------------------------------------------------------------------------- #
# Applying a mod to a row
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class WeaponModResult:
    profile: Mapping[str, Any]
    mod_ids: tuple[str, ...]
    hit_bonus: int
    damage_bonus: int
    shock_bonus: int
    uncapped_damage: str | None
    magazine_multiplier: int
    range_multiplier: float
    loses_trauma_die: bool
    nonlethal: bool
    vehicle_trauma: bool
    inactive: tuple[str, ...]

    def describe(self) -> dict[str, Any]:
        profile = dict(self.profile)
        profile["damage_bonus"] = int(profile.get("damage_bonus", 0)) + self.damage_bonus
        profile["shock"] = int(profile.get("shock", 0)) + self.shock_bonus
        profile["mod_hit_bonus"] = self.hit_bonus
        profile["mod_ids"] = list(self.mod_ids)
        if self.loses_trauma_die:
            profile["trauma_die"] = 0
        if self.nonlethal:
            profile["nonlethal"] = True
        if self.vehicle_trauma:
            profile["vehicle_trauma"] = True
        return profile


def _applies(change: Mod, category: str) -> bool:
    """``projectile`` is a family: a firearm is a projectile weapon, a knife is not."""
    if not change.applies_to:
        return True
    if category in change.applies_to:
        return True
    return "projectile" in change.applies_to and category in {"firearm", "projectile", "heavy"}


def apply_weapon_mods(
    profile: Mapping[str, Any],
    mod_ids: Iterable[str],
    *,
    category: str = "firearm",
    connected: bool = False,
) -> WeaponModResult:
    """Apply mods to a ``cwn_equipment.damage_profile`` row.

    ``connected`` is whether the wielder has a Gunlink or Cranial Jack; a mod that
    needs one stays installed but contributes nothing (``inactive``), it does not
    disappear and it does not raise.
    """
    hit = damage = shock = 0
    magazine = 1
    range_multiplier = 1.0
    loses_trauma_die = False
    nonlethal = False
    vehicle_trauma = False
    uncapped: str | None = None
    inactive: list[str] = []
    applied: list[str] = []
    seen: set[str] = set()

    for mod_id in mod_ids:
        if mod_id in seen:
            raise ModError(f"{mod_id} may be applied only once to an item")
        seen.add(mod_id)
        change = weapon_mod(mod_id)
        applied.append(mod_id)
        if not _applies(change, category):
            raise ModError(f"{change.name} does not apply to a {category}")
        if change.requires_connection and not connected:
            inactive.append(mod_id)
            continue
        eff = change.effects
        hit += int(eff.get("hit", 0))
        damage += int(eff.get("damage", 0))
        shock += int(eff.get("shock", 0))
        if eff.get("magazine_multiplier"):
            magazine *= int(eff["magazine_multiplier"])
        if eff.get("range_multiplier"):
            range_multiplier *= float(eff["range_multiplier"])
        if eff.get("loses_trauma_die"):
            loses_trauma_die = True
        if eff.get("nonlethal"):
            nonlethal = True
        if eff.get("vehicle_trauma"):
            vehicle_trauma = True
        if eff.get("uncapped") and eff.get("once_per_fight_damage"):
            uncapped = str(eff["once_per_fight_damage"])

    return WeaponModResult(
        profile=profile, mod_ids=tuple(applied),
        hit_bonus=min(MOD_BONUS_CAP["hit"], hit),
        damage_bonus=min(MOD_BONUS_CAP["damage"], damage),
        shock_bonus=min(MOD_BONUS_CAP["shock"], shock),
        uncapped_damage=uncapped, magazine_multiplier=magazine,
        range_multiplier=range_multiplier, loses_trauma_die=loses_trauma_die,
        nonlethal=nonlethal, vehicle_trauma=vehicle_trauma, inactive=tuple(inactive),
    )


@dataclass(frozen=True)
class ArmorModResult:
    piece: Mapping[str, Any]
    mod_ids: tuple[str, ...]
    ac_ranged: int
    ac_melee: int
    damage_soak: int
    trauma_target_modifier: int
    encumbrance: int
    readied_bonus: int
    stowed_bonus: int
    subtle: bool
    heavy: bool
    inactive: tuple[str, ...]

    def describe(self) -> dict[str, Any]:
        piece = dict(self.piece)
        piece["ac_ranged"] = self.ac_ranged
        piece["ac_melee"] = self.ac_melee
        piece["damage_soak"] = self.damage_soak
        piece["trauma_target_modifier"] = self.trauma_target_modifier
        piece["encumbrance"] = self.encumbrance
        piece["readied_bonus"] = self.readied_bonus
        piece["stowed_bonus"] = self.stowed_bonus
        piece["subtle"] = self.subtle
        piece["heavy"] = self.heavy
        piece["mod_ids"] = list(self.mod_ids)
        return piece


def apply_armor_mods(piece: Mapping[str, Any], mod_ids: Iterable[str]) -> ArmorModResult:
    """Apply armor mods to a ``cwn_equipment`` armor row."""
    ac_ranged = int(piece.get("ac_ranged", 10))
    ac_melee = int(piece.get("ac_melee", 10))
    soak = int(piece.get("damage_soak", 0))
    trauma = int(piece.get("trauma_target_modifier", 0))
    encumbrance = int(piece.get("encumbrance", 0))
    readied = stowed = 0
    subtle = bool(piece.get("subtle", False))
    heavy = bool(piece.get("heavy", False))
    inactive: list[str] = []
    applied: list[str] = []
    seen: set[str] = set()

    for mod_id in mod_ids:
        if mod_id in seen:
            raise ModError(f"{mod_id} may be applied only once to an item")
        seen.add(mod_id)
        change = armor_mod(mod_id)
        if change.requires_mod and change.requires_mod not in seen:
            raise ModError(f"{change.name} requires {change.requires_mod} to be installed first")
        applied.append(mod_id)
        eff = change.effects
        ac_ranged += int(eff.get("ac_ranged", 0))
        ac_melee += int(eff.get("ac_melee", 0))
        soak += int(eff.get("soak", 0))
        trauma += int(eff.get("trauma_target", 0))
        encumbrance += int(eff.get("encumbrance", 0))
        readied += int(eff.get("readied_encumbrance", 0))
        stowed += int(eff.get("stowed_encumbrance", 0))
        if eff.get("obviousness") == "subtle":
            subtle = True
        if eff.get("removes_quality") == "heavy":
            heavy = False

    return ArmorModResult(
        piece=piece, mod_ids=tuple(applied), ac_ranged=ac_ranged, ac_melee=ac_melee,
        damage_soak=max(0, soak), trauma_target_modifier=trauma,
        encumbrance=max(0, encumbrance), readied_bonus=readied, stowed_bonus=stowed,
        subtle=subtle, heavy=heavy, inactive=tuple(inactive),
    )


def apply_drone_mods(stats: Mapping[str, Any], mod_ids: Iterable[str]) -> dict[str, Any]:
    """Drone hull stats: AC, Move, HP, fitting and hardpoint counts, Encumbrance."""
    out = dict(stats)
    for mod_id in mod_ids:
        eff = drone_mod(mod_id).effects
        out["ac"] = int(out.get("ac", 10)) + int(eff.get("ac", 0))
        out["move"] = int(out.get("move", 0)) + int(eff.get("move_bonus_m", 0))
        if eff.get("hit_points_percent"):
            out["hit_points"] = int(out.get("hit_points", 0)) + math.ceil(
                int(stats.get("hit_points", 0)) * int(eff["hit_points_percent"]) / 100
            )
        out["fittings"] = int(out.get("fittings", 0)) + int(eff.get("drone_fittings", 0))
        out["hardpoints"] = int(out.get("hardpoints", 0)) + int(eff.get("drone_hardpoints", 0))
        if "portable_encumbrance" in eff:
            out["encumbrance"] = max(1, int(out.get("encumbrance", 1)) + int(eff["portable_encumbrance"]))
    return out


def apply_deck_mods(stats: Mapping[str, Any], mod_ids: Iterable[str]) -> dict[str, Any]:
    """Cyberdeck stats: CPU, Memory, Shielding, Bonus Access, Encumbrance."""
    out = dict(stats)
    for mod_id in mod_ids:
        eff = deck_mod(mod_id).effects
        for key in ("cpu", "memory", "shielding", "bonus_access", "encumbrance"):
            if key in eff:
                out[key] = int(out.get(key, 0)) + int(eff[key])
    return out


__all__ = [
    "MODS_PATH",
    "MOD_BONUS_CAP",
    "ArmorModResult",
    "CraftPlan",
    "Mod",
    "ModError",
    "WeaponModResult",
    "all_mods",
    "apply_armor_mods",
    "apply_deck_mods",
    "apply_drone_mods",
    "apply_weapon_mods",
    "armor_mod",
    "can_build",
    "can_maintain",
    "craft_plan",
    "deck_mod",
    "drone_mod",
    "factory_price",
    "install_weeks",
    "load_mods",
    "maintenance_lapse",
    "maintenance_score",
    "weapon_mod",
]
