## Vanilla CWN vehicle procedures. Data and rulings are shared with
## src/rules/cwn_vehicles.py and data/rules/cwn_vehicles.json.
## Pure functions make this usable by the top-down game and tests.
extends RefCounted
class_name CwnVehicles

const DATA_PATH := "res://data/rules/cwn_vehicles.json"
const SIZE_RANK := {"S": 0, "M": 1, "L": 2}

static func catalogue() -> Dictionary:
	if not FileAccess.file_exists(DATA_PATH):
		return {}
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
	return data if data is Dictionary else {}

static func entry(kind: String, id: String) -> Dictionary:
	for row in catalogue().get(kind, []):
		if str(row.get("id", "")) == id:
			return row
	return {}

static func size_allows(size: String, minimum: String) -> bool:
	if not SIZE_RANK.has(size) or not SIZE_RANK.has(minimum):
		return false
	return int(SIZE_RANK[size]) >= int(SIZE_RANK[minimum])

static func armor_class(base_ac: int, moving: bool, drive_skill: int = 0) -> int:
	return base_ac + maxi(0, drive_skill) if moving else base_ac - 4

## Returns null when the referee must decide whether an immune hull is harmed.
static func can_be_harmed(hull: Dictionary, heavy_weapon: bool = false, vehicle_trauma: bool = false) -> Variant:
	match str(hull.get("armor_note", "")):
		"immune":
			return null
		"heavy_only":
			return heavy_weapon or vehicle_trauma
	return true

## Trauma multiplies damage BEFORE Armor reduces it.
static func damage_to_vehicle(damage: int, trauma_multiplier: int = 1, armor: int = 0) -> Dictionary:
	if damage < 0 or trauma_multiplier < 1 or armor < 0:
		return {"ok": false, "reason": "invalid_damage"}
	return {"ok": true, "damage": maxi(0, damage * trauma_multiplier - armor)}

static func is_destroyed(hit_points: int) -> bool:
	return hit_points <= 0

static func destruction_damage(damage: int, luck_save: bool) -> int:
	return -1 if damage < 0 else (damage / 2 if luck_save else damage)

static func crash_outcome(physical_save: bool, luck_save: bool) -> Dictionary:
	return {
		"unscathed": physical_save and luck_save,
		"damage_fraction": 0.0 if physical_save and luck_save else 0.5,
		"mortally_wounded": not physical_save and not luck_save,
		"major_injury_if_survives": not physical_save and not luck_save
	}

static func ram_person(driver_total: int, target_total: int, evasion_save: bool, hull_hp: int) -> Dictionary:
	if hull_hp <= 0:
		return {"ok": false, "reason": "destroyed_hull"}
	var hurt := driver_total > target_total and not evasion_save
	return {"ok": true, "target_hurt": hurt, "damage": hull_hp if hurt else 0,
		"trauma_die": "1d12", "trauma_rating": "x3"}

static func ram_vehicle(driver_total: int, target_total: int, hull_hp: int) -> Dictionary:
	if hull_hp <= 0:
		return {"ok": false, "reason": "destroyed_hull"}
	var hit := driver_total > target_total
	return {"ok": true, "target_hurt": hit, "damage": hull_hp if hit else 0,
		"rammer_damage": hull_hp if hit else 0, "trauma_die": "1d12", "trauma_rating": "x3"}

## A pursuer must STRICTLY beat the fleeing total. Ties escape.
static func chase(fleeing_total: int, pursuer_totals: Array) -> Dictionary:
	if pursuer_totals.is_empty():
		return {"ok": false, "reason": "no_pursuers"}
	var caught_by: Array = []
	for total in pursuer_totals:
		caught_by.append(int(total) > fleeing_total)
	return {"ok": true, "caught_by": caught_by, "escaped": not caught_by.has(true)}

static func hindrance_bonus(successes: int, botched: int = 0) -> int:
	if successes < 0 or botched < 0:
		return 0
	var table: Dictionary = catalogue().get("chase_modifiers", {}).get("foot", {})
	return mini(int(table.get("hindrance_bonus_max", 3)), successes) + botched * int(table.get("hindrance_botch_penalty", -1))

static func repair_estimate(lost_hp: int, fix_skill: int, drive_skill: int,
		free_parts: bool = false, current_hp: int = 1) -> Dictionary:
	if lost_hp < 0:
		return {"ok": false, "reason": "negative_damage"}
	if current_hp <= 0:
		return {"ok": true, "totaled": true, "qualified": false, "days": 0, "cost": 0}
	var rate := 1 + maxi(0, fix_skill) + maxi(0, drive_skill)
	return {"ok": true, "totaled": false, "qualified": fix_skill >= 0 or drive_skill >= 1,
		"days": ceili(float(lost_hp) / float(rate)), "cost": 0 if free_parts else lost_hp * 200}
