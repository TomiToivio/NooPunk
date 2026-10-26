"""Cities Without Number: vehicles, vehicle combat, chases, and repair.

Covers the SRD chapters the rest of the chassis did not yet own:

* ``gear-vehicles-cyberware/vehicles/`` — the hull table, fittings, vehicle mods,
  vehicle-only weapons, repair;
* ``rules-of-the-game/combat/vehicle-combat/`` — moving/stationary AC, Armor,
  destruction, crashes, ramming, Traumatic Hits against a hull;
* ``rules-of-the-game/chases-and-pursuit/`` — foot and vehicle pursuit.

Transcribed from the **Cities Without Number SRD** (CC0, verified in
``data/sources/game_system_rights.json``). Numbers live in
``data/rules/cwn_vehicles.json``; this module is arithmetic over that contract and
holds no table of its own. Prose summaries in the data file are original.

## The three rules that are easy to get wrong

1. **Armor is subtracted after the Trauma multiplier.** A Traumatic Hit multiplies
   the whole damage roll, and only then does the hull's Armor come off
   (:func:`damage_to_vehicle`).
2. **A chasing pursuer must strictly exceed the fleeing total.** A tie is an
   escape (SRD 2.6.1/2.6.2), so ``>=`` would turn every tie into a capture.
3. **A fitting's Min. Size is a floor, not an equality**, and Power/Mass are
   budgets: a fitting may not be installed without free capacity
   (:func:`fit_out` raises rather than silently clamping).

## What this module does not model

Vehicle chase *distance* is abstracted by the SRD itself — every vehicle in a
fray is assumed to be within shooting range. No grid, no hexes, no facing.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

VEHICLES_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "cwn_vehicles.json"

SIZE_RANK: Mapping[str, int] = {"S": 0, "M": 1, "L": 2}

HeadStart = Literal["none", "one_round", "under_a_minute", "over_a_minute"]
ArmorNote = Literal["immune", "heavy_only"]


class VehicleError(ValueError):
    """A vehicle, fitting or chase was asked for that the contract does not allow."""


# --------------------------------------------------------------------------- #
# The contract
# --------------------------------------------------------------------------- #


@lru_cache(maxsize=2)
def load_vehicles(path: str | Path | None = None) -> dict[str, Any]:
    """Load the vehicle contract once (cached) and return it verbatim."""
    return json.loads(Path(path or VEHICLES_PATH).read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Vehicle:
    id: str
    name: str
    cost: int
    speed: int
    armor: int | None
    armor_note: ArmorNote | None
    trauma_target: int
    ac: int
    hit_points: int
    crew: int
    power: int
    mass: int
    size: str
    hardpoints: int
    summary: str = ""

    @property
    def armored(self) -> bool:
        """A null Armor with no note is Armor 0 — reachable, just not armoured."""
        return self.armor is not None


@dataclass(frozen=True)
class Fitting:
    id: str
    name: str
    cost: int
    power: int
    power_grant: int
    mass: int
    min_size: str
    max_stacks: int | None
    max_stacks_by_size: Mapping[str, int] | None
    effects: Mapping[str, Any]

    def stack_limit(self, size: str) -> int | None:
        if self.max_stacks_by_size is not None:
            return int(self.max_stacks_by_size.get(size, 0))
        return self.max_stacks


@dataclass(frozen=True)
class VehicleModification:
    """A vehicle mod: priced as a percentage of the hull's base cost."""

    id: str
    name: str
    skills: Mapping[str, int]
    cost_percent: int
    components: int
    effects: Mapping[str, Any]
    max_stacks_by_size: Mapping[str, int] | None = None

    def price(self, base_cost: int) -> int:
        return round(base_cost * self.cost_percent / 100)


@dataclass(frozen=True)
class VehicleWeapon:
    id: str
    name: str
    damage: str
    range: str
    cost: int
    magazine: int
    attribute: str
    trauma_die: str | None
    trauma_rating: str | None
    vehicle_trauma: bool = False
    nonlethal: bool = False
    suppressive: bool = False
    always_hits_ac: int | None = None
    ammo_cost: int = 0
    aim_rounds: int = 0
    mount: str = "vehicle"


def _rows(key: str) -> list[dict]:
    rows = load_vehicles().get(key)
    if not isinstance(rows, list):
        raise VehicleError(f"contract has no {key!r} list")
    return rows


def vehicle(vehicle_id: str) -> Vehicle:
    for row in _rows("vehicles"):
        if row["id"] == vehicle_id:
            return Vehicle(
                id=row["id"], name=row["name"], cost=int(row["cost"]),
                speed=int(row["speed"]), armor=None if row.get("armor") is None else int(row["armor"]),
                armor_note=row.get("armor_note"), trauma_target=int(row["trauma_target"]),
                ac=int(row["ac"]), hit_points=int(row["hit_points"]), crew=int(row["crew"]),
                power=int(row["power"]), mass=int(row["mass"]), size=str(row["size"]),
                hardpoints=int(row["hardpoints"]), summary=str(row.get("summary", "")),
            )
    raise VehicleError(f"unknown vehicle: {vehicle_id}")


def vehicles() -> dict[str, Vehicle]:
    return {row["id"]: vehicle(row["id"]) for row in _rows("vehicles")}


def fitting(fitting_id: str) -> Fitting:
    for row in _rows("fittings"):
        if row["id"] == fitting_id:
            return Fitting(
                id=row["id"], name=row["name"], cost=int(row["cost"]),
                power=int(row.get("power", 0)), power_grant=int(row.get("power_grant", 0)),
                mass=int(row.get("mass", 0)), min_size=str(row.get("min_size", "S")),
                max_stacks=None if row.get("max_stacks", 1) is None else int(row.get("max_stacks", 1)),
                max_stacks_by_size=row.get("max_stacks_by_size"),
                effects=row.get("effects") or {},
            )
    raise VehicleError(f"unknown fitting: {fitting_id}")


def modification(mod_id: str) -> VehicleModification:
    for row in _rows("mods"):
        if row["id"] == mod_id:
            return VehicleModification(
                id=row["id"], name=row["name"], skills=row.get("skills") or {},
                cost_percent=int(row["cost_percent"]), components=int(row.get("components", 0)),
                effects=row.get("effects") or {}, max_stacks_by_size=row.get("max_stacks_by_size"),
            )
    raise VehicleError(f"unknown vehicle mod: {mod_id}")


def weapon(weapon_id: str) -> VehicleWeapon:
    for row in _rows("vehicle_weapons"):
        if row["id"] == weapon_id:
            return VehicleWeapon(
                id=row["id"], name=row["name"], damage=str(row["damage"]), range=str(row["range"]),
                cost=int(row["cost"]), magazine=int(row["magazine"]),
                attribute=str(row["attribute"]), trauma_die=row.get("trauma_die"),
                trauma_rating=row.get("trauma_rating"),
                vehicle_trauma=bool(row.get("vehicle_trauma", False)),
                nonlethal=bool(row.get("nonlethal", False)),
                suppressive=bool(row.get("suppressive", False)),
                always_hits_ac=row.get("always_hits_ac"), ammo_cost=int(row.get("ammo_cost", 0)),
                aim_rounds=int(row.get("aim_rounds", 0)), mount=str(row.get("mount", "vehicle")),
            )
    raise VehicleError(f"unknown vehicle weapon: {weapon_id}")


def chase_modifier_table(mode: Literal["foot", "vehicle"]) -> dict[str, Any]:
    table = load_vehicles().get("chase_modifiers", {}).get(mode)
    if not isinstance(table, dict):
        raise VehicleError(f"contract has no chase modifier table for {mode!r}")
    return table


# --------------------------------------------------------------------------- #
# Fitting a hull out
# --------------------------------------------------------------------------- #


def size_allows(size: str, minimum: str) -> bool:
    """Min. Size is a *floor*: a large hull may mount a small fitting."""
    if size not in SIZE_RANK or minimum not in SIZE_RANK:
        raise VehicleError(f"unknown size: {size!r} / {minimum!r}")
    return SIZE_RANK[size] >= SIZE_RANK[minimum]


@dataclass(frozen=True)
class FittedVehicle:
    """A hull plus what has been bolted onto it, with the budgets resolved."""

    base: Vehicle
    fitting_ids: tuple[str, ...] = ()
    mod_ids: tuple[str, ...] = ()
    armor: int = 0
    hit_points: int = 0
    speed: int = 0
    crew: int = 0
    power_available: int = 0
    power_used: int = 0
    mass_available: int = 0
    mass_used: int = 0
    hardpoints: int = 0
    effects: Mapping[str, Any] = field(default_factory=dict)

    @property
    def over_power(self) -> bool:
        return self.power_used > self.power_available

    @property
    def over_mass(self) -> bool:
        return self.mass_used > self.mass_available

    @property
    def legal(self) -> bool:
        return not self.over_power and not self.over_mass

    def has(self, effect: str) -> bool:
        return bool(self.effects.get(effect))


def fit_out(vehicle_id: str, *, fittings: Iterable[str] = (), mods: Iterable[str] = ()) -> FittedVehicle:
    """Resolve a hull + fittings + mods, or raise :class:`VehicleError`.

    Raises rather than clamping: an over-budget build is an illegal build, and a
    silently trimmed one hides the mistake until a player relies on the gun that
    is not actually mounted.
    """
    hull = vehicle(vehicle_id)
    fitting_ids = tuple(fittings)
    mod_ids = tuple(mods)

    counts: dict[str, int] = {}
    mod_counts: dict[str, int] = {}
    power_used = 0
    mass_used = 0
    power_grant = 0
    mass_bonus = 0
    armor = hull.armor or 0
    hit_points = hull.hit_points
    speed = hull.speed
    crew = hull.crew
    hardpoints = hull.hardpoints
    effects: dict[str, Any] = {}

    for fid in fitting_ids:
        piece = fitting(fid)
        if not size_allows(hull.size, piece.min_size):
            raise VehicleError(f"{piece.name} needs a {piece.min_size} hull or larger")
        counts[fid] = counts.get(fid, 0) + 1
        limit = piece.stack_limit(hull.size)
        if limit is not None and counts[fid] > limit:
            raise VehicleError(f"{piece.name} may be installed at most {limit} time(s) on a {hull.size} hull")
        power_used += piece.power
        power_grant += piece.power_grant
        mass_used += piece.mass
        eff = piece.effects
        armor += int(eff.get("armor", 0))
        hit_points += _percent_of(hull.hit_points, int(eff.get("hit_points_percent", 0)))
        speed += int(eff.get("speed", 0))
        crew += int((eff.get("crew_by_size") or {}).get(hull.size, 0))
        hardpoints += int(eff.get("hardpoints", 0))
        for key, value in eff.items():
            effects.setdefault(key, value)

    for mid in mod_ids:
        change = modification(mid)
        # A vehicle mod installs once unless the contract says otherwise.
        limit = 1 if change.max_stacks_by_size is None else int(change.max_stacks_by_size.get(hull.size, 0))
        mod_counts[mid] = mod_counts.get(mid, 0) + 1
        if mod_counts[mid] > limit:
            raise VehicleError(f"{change.name} may be installed at most {limit} time(s) on a {hull.size} hull")
        eff = change.effects
        armor += int(eff.get("armor", 0))
        hit_points += _percent_of(hull.hit_points, int(eff.get("hit_points_percent", 0)))
        speed += int(eff.get("speed", 0))
        crew += int((eff.get("crew_by_size") or {}).get(hull.size, 0))
        hardpoints += int(eff.get("hardpoints", 0))
        power_grant += int((eff.get("power_by_size") or {}).get(hull.size, 0))
        mass_bonus += int((eff.get("mass_by_size") or {}).get(hull.size, 0)) + int(eff.get("mass", 0))
        for key, value in eff.items():
            effects.setdefault(key, value)

    mass_available = hull.mass + mass_bonus
    percent = int(effects.get("mass_percent", 0) or 0)
    if percent:
        mass_available += _percent_of(hull.mass, percent)

    fitted = FittedVehicle(
        base=hull, fitting_ids=fitting_ids, mod_ids=mod_ids,
        armor=max(0, armor), hit_points=max(1, hit_points), speed=speed, crew=max(1, crew),
        power_available=hull.power + power_grant, power_used=power_used,
        mass_available=max(0, mass_available), mass_used=mass_used,
        hardpoints=max(0, hardpoints), effects=effects,
    )
    if fitted.over_power:
        raise VehicleError(
            f"{hull.name}: fittings draw {fitted.power_used} Power, hull has {fitted.power_available}"
        )
    if fitted.over_mass:
        raise VehicleError(
            f"{hull.name}: fittings take {fitted.mass_used} Mass, hull has {fitted.mass_available}"
        )
    return fitted


def _percent_of(base: int, percent: int) -> int:
    """A percentage adjustment always rounds up, as the SRD's HP mods do."""
    if percent == 0:
        return 0
    magnitude = abs(percent)
    value = -(-base * magnitude // 100)
    return value if percent > 0 else -value


# --------------------------------------------------------------------------- #
# Vehicle combat (SRD 2.5.1)
# --------------------------------------------------------------------------- #


def armor_class_in_combat(base_ac: int, *, moving: bool, driver_drive_skill: int = 0) -> int:
    """A stationary hull is easier to hit; a moving one adds its driver's Drive skill."""
    if not moving:
        return base_ac - 4
    return base_ac + max(0, driver_drive_skill)


def can_be_harmed(hull: Vehicle, *, heavy_weapon: bool = False, vehicle_trauma: bool = False) -> bool | None:
    """``True``/``False`` when the contract settles it, ``None`` when the referee does.

    An immune hull is a referee call, not a code call — returning ``False`` there
    would be a rule the SRD does not make.
    """
    if hull.armor_note == "immune":
        return None
    if hull.armor_note == "heavy_only":
        return heavy_weapon or vehicle_trauma
    return True


def damage_to_vehicle(damage: int, *, trauma_multiplier: int = 1, armor: int = 0) -> int:
    """Multiply for a Traumatic Hit first, then subtract Armor (SRD 2.5.1/2.5.1.3)."""
    if damage < 0:
        raise VehicleError("damage cannot be negative")
    if trauma_multiplier < 1:
        raise VehicleError("trauma multiplier must be at least 1")
    return max(0, damage * trauma_multiplier - armor)


def is_destroyed(hit_points: int) -> bool:
    return hit_points <= 0


@dataclass(frozen=True)
class CrashResult:
    """One passenger's outcome after a hull is destroyed or goes out of control."""

    physical_save_made: bool
    luck_save_made: bool

    @property
    def unscathed(self) -> bool:
        return self.physical_save_made and self.luck_save_made

    @property
    def damage_fraction(self) -> float:
        """Both saves: none. One save: half maximum hit points. Neither: mortally wounded."""
        if self.unscathed:
            return 0.0
        return 0.5

    @property
    def mortally_wounded(self) -> bool:
        return not self.physical_save_made and not self.luck_save_made

    @property
    def major_injury_if_survives(self) -> bool:
        return self.mortally_wounded


def crash_outcome(*, physical_save_made: bool, luck_save_made: bool) -> CrashResult:
    return CrashResult(physical_save_made=bool(physical_save_made), luck_save_made=bool(luck_save_made))


def destruction_damage(damage: int, *, luck_save_made: bool) -> int:
    """Occupants take the damage that killed the hull; a Luck save halves it."""
    if damage < 0:
        raise VehicleError("damage cannot be negative")
    return damage // 2 if luck_save_made else damage


@dataclass(frozen=True)
class RamResult:
    """Ramming: opposed DEX/Drive vs DEX/Exert, then an Evasion save against people."""

    driver_won: bool
    evasion_save_made: bool
    damage: int
    evasion_allowed: bool = True
    trauma_die: str = "1d12"
    trauma_rating: str = "x3"

    @property
    def target_hurt(self) -> bool:
        if not self.driver_won:
            return False
        return (not self.evasion_allowed) or not self.evasion_save_made

    @property
    def damage_dealt(self) -> int:
        return self.damage if self.target_hurt else 0


def ram_person(*, driver_total: int, target_total: int, evasion_save_made: bool,
               hull_hit_points: int) -> RamResult:
    """A person takes the hull's *maximum* hit points, with a 1d12/x3 Trauma Die."""
    if hull_hit_points <= 0:
        raise VehicleError("a destroyed hull cannot ram")
    return RamResult(
        driver_won=driver_total > target_total,
        evasion_save_made=bool(evasion_save_made),
        damage=int(hull_hit_points),
    )


def ram_vehicle(*, driver_total: int, target_total: int, hull_hit_points: int) -> RamResult:
    """Vehicle-on-vehicle: no Evasion save, and the rammer takes the same damage back."""
    if hull_hit_points <= 0:
        raise VehicleError("a destroyed hull cannot ram")
    return RamResult(
        driver_won=driver_total > target_total,
        evasion_save_made=True,  # there is no Evasion save in a hull-versus-hull ram
        evasion_allowed=False,
        damage=int(hull_hit_points) if driver_total > target_total else 0,
    )


# --------------------------------------------------------------------------- #
# Repair (SRD 3.7.1)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class RepairEstimate:
    hit_points_lost: int
    days: int
    cost: int
    totaled: bool
    qualified: bool


def repair_estimate(
    hull: Vehicle | FittedVehicle,
    hit_points_lost: int,
    *,
    fix_skill: int,
    drive_skill: int,
    free_parts: bool = False,
    current_hit_points: int | None = None,
) -> RepairEstimate:
    """One hit point per day, plus the technician's Fix and Drive skill.

    A hull reduced to zero is totaled and cannot be cost-effectively repaired.
    Ace Driver and Roamer scrounge parts, so ``free_parts`` zeroes the bill.
    """
    if hit_points_lost < 0:
        raise VehicleError("hit points lost cannot be negative")
    if current_hit_points is not None and current_hit_points <= 0:
        return RepairEstimate(hit_points_lost, days=0, cost=0, totaled=True, qualified=False)
    qualified = fix_skill >= 0 or drive_skill >= 1
    per_day = 1 + max(0, fix_skill) + max(0, drive_skill)
    days = -(-hit_points_lost // per_day) if hit_points_lost else 0
    cost = 0 if free_parts else hit_points_lost * 200
    return RepairEstimate(hit_points_lost, days=days, cost=cost, totaled=False, qualified=qualified)


# --------------------------------------------------------------------------- #
# Chases (SRD 2.6)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ChaseOutcome:
    fleeing_total: int
    pursuer_totals: tuple[int, ...]

    @property
    def caught_by(self) -> tuple[bool, ...]:
        """Strictly greater, not greater-or-equal: a tie is an escape."""
        return tuple(total > self.fleeing_total for total in self.pursuer_totals)

    @property
    def escaped(self) -> bool:
        return not any(self.caught_by)


def resolve_chase(fleeing_total: int, pursuer_totals: Iterable[int]) -> ChaseOutcome:
    totals = tuple(int(total) for total in pursuer_totals)
    if not totals:
        raise VehicleError("a chase needs at least one pursuer")
    return ChaseOutcome(fleeing_total=int(fleeing_total), pursuer_totals=totals)


def hindrance_bonus(successes: int, *, botched: int = 0) -> int:
    """Each successful hindrance is +1 to the fleeing pace, capped at +3.

    A botched effort is -1 *each*: the SRD applies the penalty when the effort is
    actively harmful, and a group can botch more than once.
    """
    if successes < 0 or botched < 0:
        raise VehicleError("hindrance counts cannot be negative")
    table = chase_modifier_table("foot")
    return min(int(table["hindrance_bonus_max"]), successes) + botched * int(table["hindrance_botch_penalty"])


def foot_chase_modifier(
    *,
    more_pursuers_than_pursued: bool = False,
    head_start: HeadStart = "under_a_minute",
    terrain_knowledge: int = 0,
    half_hearted: bool = False,
    enraged: bool = False,
) -> int:
    table = chase_modifier_table("foot")
    if not int(table["terrain_knowledge_min"]) <= terrain_knowledge <= int(table["terrain_knowledge_max"]):
        raise VehicleError("terrain knowledge is a referee band, -2..+2")
    modifier = 0
    if more_pursuers_than_pursued:
        modifier += int(table["more_pursuers_than_pursued"])
    modifier += {
        "none": int(table["no_head_start"]),
        "one_round": int(table["one_round_head_start"]),
        "under_a_minute": int(table["less_than_a_minute_head_start"]),
        "over_a_minute": int(table["more_than_a_minute_head_start"]),
    }[head_start]
    modifier += terrain_knowledge
    if half_hearted:
        modifier += int(table["pursuit_half_hearted"])
    if enraged:
        modifier += int(table["pursuers_enraged"])
    return modifier


def vehicle_chase_modifier(
    *,
    cannot_see_target: bool = False,
    pursuer_flying: bool = False,
    pursued_flying: bool = False,
    spotter: bool = False,
    terrain_knowledge: int = 0,
    half_hearted: bool = False,
    enraged: bool = False,
) -> int:
    table = chase_modifier_table("vehicle")
    if not int(table["terrain_knowledge_min"]) <= terrain_knowledge <= int(table["terrain_knowledge_max"]):
        raise VehicleError("terrain knowledge is a referee band, -2..+2")
    modifier = 0
    if cannot_see_target:
        modifier += int(table["pursuer_cannot_see_target"])
    if pursuer_flying and not pursued_flying:
        modifier += int(table["pursuer_flying_pursued_not"])
    if pursued_flying and not pursuer_flying:
        modifier += int(table["pursued_flying_pursuer_not"])
    if spotter:
        modifier += int(table["spotter_relaying"])
    modifier += terrain_knowledge
    if half_hearted:
        modifier += int(table["pursuit_half_hearted"])
    if enraged:
        modifier += int(table["pursuers_enraged"])
    return modifier


__all__ = [
    "SIZE_RANK",
    "VEHICLES_PATH",
    "ChaseOutcome",
    "CrashResult",
    "FittedVehicle",
    "Fitting",
    "RamResult",
    "RepairEstimate",
    "Vehicle",
    "VehicleError",
    "VehicleModification",
    "VehicleWeapon",
    "armor_class_in_combat",
    "can_be_harmed",
    "chase_modifier_table",
    "crash_outcome",
    "damage_to_vehicle",
    "destruction_damage",
    "fit_out",
    "fitting",
    "foot_chase_modifier",
    "hindrance_bonus",
    "is_destroyed",
    "load_vehicles",
    "modification",
    "ram_person",
    "ram_vehicle",
    "repair_estimate",
    "resolve_chase",
    "size_allows",
    "vehicle",
    "vehicle_chase_modifier",
    "vehicles",
    "weapon",
]
