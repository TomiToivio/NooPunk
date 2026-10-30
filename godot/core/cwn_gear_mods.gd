## Cities Without Number — crafting, modifying and maintaining gear.
##
## Transcribed from the SRD (CC0), ``rules-of-the-game/crafting-and-modifying-gear/*``. The mod
## catalogue itself is data (`data/rules/cwn_gear_mods.json`, extracted from the SRD); this module is
## the arithmetic the rules put around it.
##
## Two rules are easy to get wrong and are the reason this is a module rather than a formula in a UI:
##
## 1. **Mod bonuses to hit, damage and Shock cap at +3 combined.** Shock Burst's 2d6 is explicitly
##    outside that cap, so it is returned as a separate uncapped value rather than folded in.
## 2. **Maintenance is a skill gate and a count, not a cost.** A tech who lacks the mod's minimum Fix
##    cannot maintain it at all, and how many they can keep alive is `INT mod + CON mod + 3 × Fix`.
##
## Dice are never rolled here.
extends RefCounted
class_name CwnGearMods

const DATA_PATH := "res://data/rules/cwn_gear_mods.json"

static var _data: Dictionary = {}


static func data() -> Dictionary:
	if _data.is_empty():
		var file := FileAccess.open(DATA_PATH, FileAccess.READ)
		if file == null:
			return {}
		var parsed: Variant = JSON.parse_string(file.get_as_text())
		if parsed is Dictionary:
			_data = parsed
	return _data


static func rules(section: String) -> Dictionary:
	return Dictionary(data().get(section, {}))


static func _mods(kind: String) -> Array:
	return Array(data().get(kind, []))


## Look up a catalogue row: `kind` is weapon_mods, armor_mods, drone_mods or deck_mods.
static func entry(kind: String, mod_id: String) -> Dictionary:
	for row in _mods(kind):
		if String(Dictionary(row).get("id", "")) == mod_id:
			return Dictionary(row)
	return {}


static func weapon_mod(mod_id: String) -> Dictionary:
	return entry("weapon_mods", mod_id)


## How many mods one tech can keep working: `INT mod + CON mod + 3 × Fix`, doubled by full-time work.
##
## Negative totals mean "none", not anti-maintenance. Untrained Fix is refused, because the SRD makes
## maintenance a trained skill.
static func maintenance_score(int_modifier: int, con_modifier: int, fix_skill: int, full_time: bool = false) -> Dictionary:
	if fix_skill < 0:
		return {"ok": false, "reason": "Fix is a trained rank 0-4; untrained cannot maintain mods"}
	var score := int_modifier + con_modifier + 3 * fix_skill
	if full_time:
		score *= int(rules("maintenance").get("full_time_multiplier", 1))
	return {"ok": true, "score": maxi(0, score)}


## Whether a tech's skills allow building this mod at all.
static func can_build(fix_skill: int, mod: Dictionary, drive_skill: int = 0, heal_skill: int = 0) -> bool:
	return fix_skill >= int(mod.get("min_fix", 0)) \
		and drive_skill >= int(mod.get("min_drive", 0)) \
		and heal_skill >= int(mod.get("min_heal", 0))


## A tech may only maintain mods they could have built.
static func can_maintain(fix_skill: int, mod: Dictionary) -> bool:
	return fix_skill >= int(mod.get("min_fix", 0))


## Workshop time: one week per minimum skill level, halved by an assistant, then by obsession.
static func install_weeks(mod: Dictionary, assistant: bool = false, obsessive: bool = false) -> int:
	var crafting := rules("crafting")
	var weeks := (int(mod.get("min_fix", 0)) + int(mod.get("min_heal", 0))) \
		* int(crafting.get("weeks_per_minimum_skill_level", 1))
	if weeks == 0:
		weeks = 1  # a Fix-0 mod still costs a week of workshop time, never zero
	if assistant:
		weeks = ceili(float(weeks) / float(int(crafting.get("assistant_time_divisor", 2))))
	if obsessive:
		weeks = ceili(float(weeks) / float(int(crafting.get("obsessive_time_divisor", 2))))
	return maxi(1, weeks)


## `working`, `mod_dead` or `item_dead` — the SRD's 24-hour and 7-day maintenance clocks.
static func maintenance_lapse(hours_without: float) -> String:
	var maintenance := rules("maintenance")
	if hours_without >= float(int(maintenance.get("lapse_days_item_stops", 7)) * 24):
		return "item_dead"
	if hours_without >= float(int(maintenance.get("lapse_hours_mod_stops", 24))):
		return "mod_dead"
	return "working"


## Jury-rigged, normal or mastercrafted: time, parts bill, and the strings attached.
static func craft_plan(quality: String, market_cost: int, vehicle: bool = false) -> Dictionary:
	if market_cost < 0:
		return {"ok": false, "reason": "market cost cannot be negative"}
	var crafting := rules("crafting")
	var qualities: Dictionary = Dictionary(crafting.get("quality", {}))
	if not qualities.has(quality):
		return {"ok": false, "reason": "unknown crafting quality: %s" % quality}
	var grade: Dictionary = Dictionary(qualities[quality])
	var build_time: Dictionary = Dictionary(crafting.get("build_time_days", {}))
	var base_days := int(build_time.get("vehicle" if vehicle else "portable_complex_device", 0))
	var divisor := maxi(1, int(grade.get("time_divisor", 1)))
	var multiplier := maxi(1, int(grade.get("time_multiplier", 1)))
	return {
		"ok": true,
		"quality": quality,
		"days": ceili(float(base_days * multiplier) / float(divisor)),
		"parts_cost": roundi(float(market_cost) * float(int(grade.get("parts_percent_of_market", 0))) / 100.0),
		"counts_as_mod_requiring_fix": grade.get("counts_as_mod", null),
		"stops_after_hours": grade.get("stops_after_hours_without_maintenance", null),
		"further_modding": bool(grade.get("further_modding", true)),
		"first_mod_needs_no_maintenance": bool(grade.get("first_mod_needs_no_maintenance", false)),
	}


## Factory-modded gear: five times the mod's build price on top of the base, doubling per component.
static func factory_price(base_cost: int, mod_cost: int, components: int = 0) -> Dictionary:
	if base_cost < 0 or mod_cost < 0 or components < 0:
		return {"ok": false, "reason": "costs and component counts cannot be negative"}
	return {"ok": true, "price": (base_cost + 5 * mod_cost) * int(pow(2, components))}


## Apply weapon mods to a damage profile.
##
## `connected` is whether the wielder has a Gunlink or Cranial Jack; a mod that needs one stays
## installed but contributes nothing, and is reported in `inactive` rather than silently dropped.
static func apply_weapon_mods(
	mod_ids: Array,
	category: String = "firearm",
	connected: bool = false
) -> Dictionary:
	var caps := rules("mod_bonus_cap")
	var hit := 0
	var damage := 0
	var shock := 0
	var magazine := 1
	var range_multiplier := 1.0
	var loses_trauma_die := false
	var nonlethal := false
	var vehicle_trauma := false
	var uncapped := ""
	var inactive: Array = []
	var seen: Array = []
	for mod_id in mod_ids:
		var key := String(mod_id)
		var change := weapon_mod(key)
		if change.is_empty():
			return {"ok": false, "reason": "unknown weapon mod: %s" % key}
		if seen.has(key):
			return {"ok": false, "reason": "%s may be applied only once to an item" % key}
		seen.append(key)
		var applies_to: Array = Array(change.get("applies_to", []))
		if not applies_to.is_empty() and not applies_to.has(category):
			return {"ok": false, "reason": "%s does not apply to a %s" % [String(change.get("name", key)), category]}
		var requires: Array = Array(change.get("requires_connection", []))
		if not requires.is_empty() and not connected:
			inactive.append(key)
			continue
		var effects: Dictionary = Dictionary(change.get("effects", {}))
		hit += int(effects.get("hit", 0))
		damage += int(effects.get("damage", 0))
		shock += int(effects.get("shock", 0))
		if int(effects.get("magazine_multiplier", 0)) != 0:
			magazine *= int(effects["magazine_multiplier"])
		if float(effects.get("range_multiplier", 0.0)) != 0.0:
			range_multiplier *= float(effects["range_multiplier"])
		if bool(effects.get("loses_trauma_die", false)):
			loses_trauma_die = true
		if bool(effects.get("nonlethal", false)):
			nonlethal = true
		if bool(effects.get("vehicle_trauma", false)):
			vehicle_trauma = true
		if bool(effects.get("uncapped", false)) and effects.has("once_per_fight_damage"):
			uncapped = String(effects["once_per_fight_damage"])
	return {
		"ok": true,
		"mod_ids": seen,
		"hit_bonus": mini(int(caps.get("hit", 3)), hit),
		"damage_bonus": mini(int(caps.get("damage", 3)), damage),
		"shock_bonus": mini(int(caps.get("shock", 3)), shock),
		"uncapped_damage": uncapped,
		"magazine_multiplier": magazine,
		"range_multiplier": range_multiplier,
		"loses_trauma_die": loses_trauma_die,
		"nonlethal": nonlethal,
		"vehicle_trauma": vehicle_trauma,
		"inactive": inactive,
	}
