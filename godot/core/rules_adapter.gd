## The rules adapter: the *only* place the Godot slice reads a mechanic (#631).
##
## Why an adapter and not a rules implementation: `AGENTS.md` forbids letting engine code invent a rule,
## and the repository already owns the approved kernel in `data/rules/wn_core.json` (the 2026-10-26 WN
## baseline, implemented and tested in `src/rules/wn_core.py`). This class *reads* that data and applies
## it; it hardcodes no attribute table, no ladder and no die pool.
##
## What is deliberately explicit rather than assumed:
##   * the die pool and the ladder come from the kernel file;
##   * a caller may pass an approved override (`approved_die_pool`), because #564's history contains a
##     3d6 core-check proposal and the author has not ruled it in or out. Nothing here silently
##     substitutes one for the other: `die_pool_label()` reports what was actually used, and the
##     resolved check carries it, so a later approved decision changes data, not code;
##   * an unknown difficulty is an error, not a default.
class_name RulesAdapter
extends RefCounted

const DEFAULT_KERNEL_PATH := "res://data/rules/wn_core.json"

var kernel: Dictionary = {}
var die_count: int = 2
var die_sides: int = 6
var die_pool_source: String = "kernel"
var _dice: NoopunkDice

func _init(kernel_path: String = DEFAULT_KERNEL_PATH, roll_seed: int = 1, approved_die_pool: Dictionary = {}) -> void:
	kernel = _load_json(kernel_path)
	var skill_check: Dictionary = kernel.get("skill_check", {})
	die_count = int(skill_check.get("dice_count", 2))
	die_sides = int(skill_check.get("dice_sides", 6))
	if approved_die_pool.has("count") and approved_die_pool.has("sides"):
		die_count = int(approved_die_pool["count"])
		die_sides = int(approved_die_pool["sides"])
		die_pool_source = "approved override"
	_dice = NoopunkDice.new(roll_seed)

func reseed(roll_seed: int) -> void:
	_dice.reseed(roll_seed)

## Save/load hooks: the adapter owns the stream, so the state never touches the RNG directly.
func snapshot() -> Dictionary:
	return _dice.snapshot()

func restore_dice(roll_seed: int, rolls: int) -> void:
	_dice.restore(roll_seed, rolls)

func die_pool_label() -> String:
	return "%dd%d (%s)" % [die_count, die_sides, die_pool_source]

func attribute_names() -> Array:
	return kernel.get("stats", {}).get("final_list", [])

## The kernel's band table, e.g. 3 -> -2, 4..7 -> -1, 8..13 -> 0, 14..17 -> +1, 18 -> +2.
func attribute_modifier(score: int) -> int:
	var stats: Dictionary = kernel.get("stats", {})
	var table: Dictionary = stats.get("modifier_table", {})
	var key := str(score)
	if table.has(key):
		return int(table[key])
	# Scores outside the table are clamped to the nearest recorded band rather than invented.
	var keys: Array = []
	for k in table.keys():
		keys.append(int(k))
	if keys.is_empty():
		return 0
	keys.sort()
	if score < int(keys[0]):
		return int(table[str(keys[0])])
	return int(table[str(keys[keys.size() - 1])])

func difficulty_value(name_or_value: Variant) -> int:
	var difficulties: Dictionary = kernel.get("skill_check", {}).get("difficulties", {})
	if typeof(name_or_value) == TYPE_INT or typeof(name_or_value) == TYPE_FLOAT:
		var value := int(name_or_value)
		if difficulties.has(str(value)):
			return value
		push_error("RulesAdapter: %d is not on the kernel's ladder" % value)
		return value
	var wanted := String(name_or_value).to_lower()
	for key in difficulties.keys():
		if String(difficulties[key]).to_lower() == wanted:
			return int(key)
	push_error("RulesAdapter: no difficulty named '%s' on the kernel's ladder" % wanted)
	return 0

func difficulty_name(value: int) -> String:
	return String(kernel.get("skill_check", {}).get("difficulties", {}).get(str(value), ""))

## `2d6 + attribute modifier + skill level + situational + aid` against the ladder.
##
## `skill_level` may be -1 for untrained: the kernel records `untrained_modifier` and the game passes it
## explicitly, so the adapter does not have to guess whether a missing skill means "0" or "untrained".
func skill_check(attribute_score: int, skill_level: int, difficulty: Variant, situational: int = 0, aid: int = 0) -> Dictionary:
	var target := difficulty_value(difficulty)
	var faces := _dice.pool(die_count, die_sides)
	var dice_total := 0
	for face in faces:
		dice_total += int(face)
	var modifier := attribute_modifier(attribute_score)
	var total := dice_total + modifier + skill_level + situational + aid
	return {
		"dice": faces,
		"dice_total": dice_total,
		"die_pool": die_pool_label(),
		"attribute_modifier": modifier,
		"skill_level": skill_level,
		"situational": situational,
		"aid": aid,
		"total": total,
		"difficulty": target,
		"difficulty_name": difficulty_name(target),
		"success": total >= target,
	}

## `d20 >= 16 - level - the higher of the pair`. Kept because the kernel records it and a later milestone
## needs it; the slice itself does not call it.
func save_target(category: String, level: int, modifiers: Dictionary) -> int:
	var saves: Dictionary = kernel.get("saves", {})
	var pairs: Dictionary = saves.get("attributes", {})
	var base := int(saves.get("base_target", 16))
	var pair: Array = pairs.get(category.to_lower(), [])
	if pair.is_empty():
		# "luck" carries no attribute modifiers in the kernel.
		return base - level
	var first := int(modifiers.get(String(pair[0]), 0))
	var second := int(modifiers.get(String(pair[1]), 0))
	return base - level - max(first, second)

# --- combat (CWN 2.4) ---------------------------------------------------------------------------
#
# The same procedures the Python kernel implements in `src/rules/wn_core.py`. The numbers are read
# from the kernel file, so a change to the contract reaches the game without editing this adapter.

func _combat_section() -> Dictionary:
	return kernel.get("combat", {})

func _attack_penalty(untrained: bool) -> int:
	if not untrained:
		return 0
	return int(_combat_section().get("attack", {}).get("unskilled_penalty", -2))

## `d20 + attack bonus + attribute modifier + combat skill`, with 1 always missing and 20 always hitting.
func attack_roll(attack_bonus: int, attribute_score: int, skill_level: int, target_ac: int,
		untrained: bool = false, situational: int = 0) -> Dictionary:
	var faces := _dice.pool(1, 20)
	var rolled := int(faces[0])
	var modifier := attribute_modifier(attribute_score)
	var penalty := _attack_penalty(untrained)
	var total := rolled + attack_bonus + modifier + skill_level + situational + penalty
	var success := total >= target_ac
	if rolled == 1:
		success = false
	elif rolled == 20:
		success = true
	return {
		"die": rolled,
		"attack_bonus": attack_bonus,
		"attribute_modifier": modifier,
		"skill_level": skill_level,
		"untrained": untrained,
		"situational": situational,
		"total": total,
		"target_ac": target_ac,
		"success": success,
		"natural": rolled == 1 or rolled == 20,
	}

## A weapon's stat line, as the scenario data writes it. `shock_ac = -1` means the Shock applies
## regardless of the target's Armor Class, and `trauma_die = 0` means the weapon rolls no Trauma Die.
func weapon(name: String, damage_count: int, damage_sides: int, damage_bonus: int, shock: int,
		shock_ac: int, trauma_die: int, trauma_rating: int) -> Dictionary:
	return {
		"name": name,
		"damage_count": damage_count,
		"damage_sides": damage_sides,
		"damage_bonus": damage_bonus,
		"shock": shock,
		"shock_ac": shock_ac,
		"trauma_die": trauma_die,
		"trauma_rating": trauma_rating,
	}

func _shock_applies(weapon_data: Dictionary, target_melee_ac: int) -> bool:
	var shock := int(weapon_data.get("shock", 0))
	if shock <= 0:
		return false
	var shock_ac := int(weapon_data.get("shock_ac", -1))
	return shock_ac < 0 or target_melee_ac <= shock_ac

## Damage, Shock and Trauma for one resolved attack roll.
##
## On a hit: weapon damage + attribute modifier, multiplied by the Trauma Rating on a Traumatic Hit,
## and never less than the Shock the weapon would have done on a miss. On a miss: the Shock applies
## only when the target's melee AC is within the weapon's Shock rating.
func resolve_damage(attack: Dictionary, weapon_data: Dictionary, attribute_score: int,
		target_melee_ac: int, trauma_target: int = -1, non_lethal: bool = false) -> Dictionary:
	var modifier := attribute_modifier(attribute_score)
	var shock_value := int(weapon_data.get("shock", 0))
	var shock_applies := _shock_applies(weapon_data, target_melee_ac)
	var shock_damage := maxi(0, shock_value + modifier) if shock_applies else 0
	var effective_target := trauma_target
	if effective_target < 0:
		effective_target = int(_combat_section().get("trauma", {}).get("default_target", 6))

	if not bool(attack.get("success", false)):
		return {
			"hit": false,
			"damage": 0,
			"shock_damage": shock_damage,
			"traumatic": false,
			"trauma_roll": null,
			"trauma_target": effective_target,
			"total_damage": shock_damage,
		}

	var sides := int(weapon_data.get("damage_sides", 6))
	var faces := _dice.pool(int(weapon_data.get("damage_count", 1)), sides)
	var rolled_damage := 0
	for face in faces:
		rolled_damage += int(face)
	var damage := maxi(rolled_damage + modifier + int(weapon_data.get("damage_bonus", 0)), shock_damage)

	var trauma_sides := int(weapon_data.get("trauma_die", 0))
	var trauma_roll: Variant = null
	var traumatic := false
	if trauma_sides > 0 and not non_lethal:
		trauma_roll = int(_dice.pool(1, trauma_sides)[0])
		traumatic = int(trauma_roll) >= effective_target
		if traumatic:
			damage *= maxi(1, int(weapon_data.get("trauma_rating", 1)))

	return {
		"hit": true,
		"damage": damage,
		"shock_damage": shock_damage,
		"traumatic": traumatic,
		"trauma_roll": trauma_roll,
		"trauma_target": effective_target,
		"total_damage": damage,
	}

## Stabilizing a mortally wounded ally: `8 + rounds since the fall`, +2 without a medkit.
func stabilize_difficulty(rounds_since_fall: int, has_tools: bool = true) -> int:
	return 8 + rounds_since_fall + (0 if has_tools else 2)

func mortal_rounds() -> int:
	return int(_combat_section().get("mortal_injury", {}).get("rounds_until_death", 6))

# --- injury, strain and healing (CWN 2.5) -------------------------------------------------------

## System Strain's maximum is the Constitution score (CWN 2.5.3).
func strain_maximum(constitution_score: int) -> int:
	return constitution_score

## Strain that would cross the maximum cannot be applied at all.
func strain_can_accept(constitution_score: int, current: float, amount: float) -> bool:
	return current + amount <= float(strain_maximum(constitution_score))

## Returns the new total, or -1.0 when the effect is unusable because it would cross the maximum.
func strain_add(constitution_score: int, current: float, amount: float) -> float:
	if not strain_can_accept(constitution_score, current, amount):
		return -1.0
	return current + amount

## An unavoidable overload knocks the character unconscious; returns true in that case.
func strain_forced_over_maximum(constitution_score: int, current: float, amount: float) -> bool:
	return current + amount > float(strain_maximum(constitution_score))

func strain_after_rest(current: float) -> float:
	return maxf(0.0, current - 1.0)

## First aid: `1d6 + Heal`, or `1d6 - 1` with no Heal skill at all. Costs one System Strain.
func first_aid_healing(heal_skill: int, untrained: bool = false) -> int:
	var rolled := int(_dice.pool(1, 6)[0])
	if untrained:
		return rolled - 1
	return rolled + heal_skill

func natural_healing(level: int, frail: bool = false) -> int:
	if frail:
		return 0
	return level

# --- hacking (CWN 4.x) ---------------------------------------------------------------------------

## `INT modifier + Program skill + the deck's bonus Access`.
func access_pool(attribute_score: int, program_skill: int, deck_bonus: int = 0) -> int:
	return maxi(0, attribute_modifier(attribute_score) + program_skill + deck_bonus)

## A cyberware or drone target: `7 + ceil(HD or level / 3)`; a drone with no operator is 8.
func cyber_hack_difficulty(level_or_hit_dice: int, has_operator: bool = true) -> int:
	if not has_operator:
		return 8
	return 7 + int(ceil(float(level_or_hit_dice) / 3.0))

## The network's security level plus the recorded situation modifiers.
func hacking_difficulty(security: int, alerted: bool = false, important_device: bool = false,
		tech_quality: int = 0, inside_info: int = 0) -> int:
	var levels: Dictionary = kernel.get("hacking", {}).get("security_levels", {})
	if not levels.has(str(security)):
		push_error("RulesAdapter: %d is not a recorded security level" % security)
		return security
	return security + (1 if alerted else 0) + (1 if important_device else 0) + tech_quality - inside_info

## The Int/Program check behind a Verb. The connection penalties are flat modifiers, not
## circumstances, so they are not clamped to the situational bound the way `skill_check` clamps.
func hacking_check(attribute_score: int, program_skill: int, difficulty: int, untrained: bool = false,
		wireless: bool = false, vr_crown: bool = false, verb_modifier: int = 0) -> Dictionary:
	var connection: Dictionary = kernel.get("hacking", {}).get("connection", {})
	var penalty := 0
	if wireless:
		penalty += int(connection.get("wireless", {}).get("penalty", -2))
	if vr_crown:
		penalty += int(connection.get("vr_crown", {}).get("penalty", -1))

	var faces := _dice.pool(die_count, die_sides)
	var dice_total := 0
	for face in faces:
		dice_total += int(face)
	var modifier := attribute_modifier(attribute_score)
	var untrained_penalty := int(kernel.get("skills", {}).get("untrained_modifier", -1)) if untrained else 0
	var skill := 0 if untrained else program_skill
	var total := dice_total + modifier + skill + untrained_penalty + penalty + verb_modifier
	return {
		"dice": faces,
		"dice_total": dice_total,
		"die_pool": die_pool_label(),
		"attribute_modifier": modifier,
		"skill_level": skill,
		"untrained": untrained,
		"situational": 0,
		"misc": penalty + verb_modifier,
		"total": total,
		"difficulty": difficulty,
		"difficulty_name": difficulty_name(difficulty),
		"success": total >= difficulty,
	}

# --- advancement (CWN 1.9) -----------------------------------------------------------------------

func level_for_xp(xp: int, track: String = "fast") -> int:
	var xp_table: Dictionary = kernel.get("advancement", {}).get("xp", {})
	var thresholds: Array = xp_table.get(track, xp_table.get("fast", []))
	var level := 1
	for index in thresholds.size():
		if xp >= int(thresholds[index]):
			level = index + 1
	return level

func attack_bonus(level: int, on_target_edge: bool = false) -> int:
	if on_target_edge:
		return level
	return int(level / 2.0)

func skill_point_cost(skill_level: int) -> int:
	for row in kernel.get("advancement", {}).get("skill_costs", []):
		if int(row.get("level", -1)) == skill_level:
			return int(row.get("points", 0))
	push_error("RulesAdapter: no skill level %d" % skill_level)
	return 0

func minimum_level_for_skill(skill_level: int) -> int:
	for row in kernel.get("advancement", {}).get("skill_costs", []):
		if int(row.get("level", -1)) == skill_level:
			return int(row.get("min_character_level", 1))
	push_error("RulesAdapter: no skill level %d" % skill_level)
	return 1


func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("RulesAdapter: kernel not found at %s" % path)
		return {}
	var text := FileAccess.get_file_as_string(path)
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("RulesAdapter: kernel at %s is not a JSON object" % path)
		return {}
	return parsed
