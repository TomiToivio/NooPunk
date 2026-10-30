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

## Public die rolls for modules that need dice but must not own a second RNG (#749).
##
## Combat, hacking and encounter resolution all draw from this stream, so one seed reproduces an
## entire vertical slice rather than one module of it.
func roll_die(sides: int) -> int:
	return _dice.roll(sides)

func roll_dice(count: int, sides: int) -> int:
	if count < 0 or sides < 2:
		push_error("RulesAdapter: invalid dice pool")
		return 0
	var total := 0
	for _i in range(count):
		total += _dice.roll(sides)
	return total

## CWN d20 attack against a caller-selected melee or ranged Armor Class.
## Trained combat ranks are 0..4; -1 signifies an untrained attack (-2).
## Damage, Trauma and Shock belong to the later complete combat module.
func attack_roll(attribute_score: int, combat_rank: int, attack_bonus: int, armor_class: int, other_modifier: int = 0) -> Dictionary:
	if combat_rank < -1 or combat_rank > 4 or armor_class < 1:
		push_error("RulesAdapter: invalid combat rank or Armor Class")
		return {}
	var face := _dice.roll(20)
	var skill_bonus := -2 if combat_rank == -1 else combat_rank
	var attr_bonus := attribute_modifier(attribute_score)
	var total := face + attack_bonus + attr_bonus + skill_bonus + other_modifier
	return {
		"die": face,
		"attack_bonus": attack_bonus,
		"attribute_modifier": attr_bonus,
		"skill_modifier": skill_bonus,
		"other_modifier": other_modifier,
		"armor_class": armor_class,
		"total": total,
		"hit": total >= armor_class,
		"margin": total - armor_class,
	}

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

# --- CWN procedures the kernel records but the first slice did not expose (#749/#751) -----------

## 3d6 down the line, in the kernel's attribute order. Returns scores and modifiers.
func roll_attributes(dice: NoopunkDice = null) -> Dictionary:
	var names: Array = attribute_names()
	var scores: Dictionary = {}
	var modifiers: Dictionary = {}
	for name in names:
		var total := 0
		for _i in 3:
			total += (dice.roll(6) if dice != null else _dice.roll(6))
		scores[name] = total
		modifiers[name] = attribute_modifier(total)
	return {"scores": scores, "modifiers": modifiers}


## System Strain (#SRD injury-healing-system-strain/system-strain): maximum equals Constitution,
## cyberware is permanent strain, and forcing past the maximum knocks the character out for an hour.
func strain_max(constitution: int) -> int:
	return int(constitution)


func strain_absorb(current: float, amount: float, constitution: int, force: bool = false) -> Dictionary:
	var maximum := strain_max(constitution)
	var total := float(current) + float(amount)
	if total > maximum:
		if not force:
			return {"ok": false, "reason": "overflow refused", "total": current, "maximum": maximum}
		return {"ok": true, "total": maximum, "unconscious_hours": 1, "forced": true, "maximum": maximum}
	return {"ok": true, "total": total, "forced": false, "maximum": maximum}


func strain_recover(current: float, warm_fed_rested: bool = true) -> float:
	if not warm_fed_rested:
		return float(current)
	var per_night := float(kernel.get("strain", {}).get("recovery_per_night", 1))
	return maxf(0.0, float(current) - per_night)


## Advancement (#SRD character-advancement): fast/slow XP ladders, level for XP, attack bonus and
## the per-level hit point and skill point budgets.
func xp_threshold(level: int, pace: String = "fast") -> int:
	var ladder: Dictionary = kernel.get("advancement", {}).get("xp", {}).get(pace, {})
	return int(ladder.get(str(clampi(level, 1, 10)), 0))


func level_for_xp(xp: int, pace: String = "fast") -> int:
	var ladder: Dictionary = kernel.get("advancement", {}).get("xp", {}).get(pace, {})
	var best := 1
	for level in range(1, 11):
		if xp >= int(ladder.get(str(level), 0)):
			best = level
	return best


func attack_bonus_for_level(level: int, on_target_edge: bool = false) -> int:
	if on_target_edge:
		return level
	return int(floor(float(level) / 2.0))


func hp_gain(level: int, constitution_modifier: int, hard_to_kill: bool = false) -> int:
	var total := 0
	for _i in maxi(1, level):
		var die := maxi(1, _dice.roll(6))
		total += maxi(1, die + constitution_modifier + (2 if hard_to_kill else 0))
	return total


func skill_points_for_level(level: int, educated: bool = false) -> int:
	var per_level := int(kernel.get("advancement", {}).get("skill_points_per_level", 3))
	return maxi(1, level) * per_level + (int(kernel.get("advancement", {}).get("educated_bonus", 1)) if educated else 0)


func skill_rank_allowed(rank: int, character_level: int) -> bool:
	var minimums: Dictionary = kernel.get("advancement", {}).get("skill_min_character_level", {})
	return character_level >= int(minimums.get(str(clampi(rank, 0, 4)), 1))


## Encumbrance (#SRD encumbrance): stowed = Strength, readied = half Strength, and overload
## costs speed in two steps.
func encumbrance(strength: int) -> Dictionary:
	return {
		"stowed": strength,
		"readied": int(floor(float(strength) / 2.0)),
		"overload_step": kernel.get("encumbrance", {}).get("overload_step", {}),
	}


func speed_for_load(base_metres: float, heavy: bool = false, overloaded: bool = false) -> float:
	var speed := float(base_metres)
	if heavy:
		speed *= 0.7
	if overloaded:
		speed *= 0.5
	return snappedf(speed, 0.1)


## Major injury (#SRD injury-healing-system-strain/major-injuries): d12 + modifiers, clamped 1..12.
func major_injury(roll: int, modifier: int = 0) -> Dictionary:
	var table: Dictionary = kernel.get("combat", {}).get("major_injury", {})
	var clamped := clampi(roll + modifier, 1, 12)
	var rows: Dictionary = table.get("rows", {})
	return {"roll": roll, "modifier": modifier, "result": clamped, "injury": String(rows.get(str(clamped), ""))}


## Action economy flags (#SRD combat/combat-actions).
func action_economy() -> Dictionary:
	return kernel.get("combat", {}).get("actions", {}).duplicate(true)


## Charge and total-defence modifiers, kept as data so combat code cannot drift from the kernel.
func combat_action_modifier(action: String) -> Dictionary:
	var actions: Dictionary = kernel.get("combat", {}).get("actions", {})
	return (actions.get(action, {}) as Dictionary).duplicate(true)


# CWN hacking bridge (SRD: Hacking Mechanics / Program Verbs).
# Use the existing canonical CWN kernels and the adapter's seeded dice stream.
# The rules layer never silently fabricates a program, cost, or security target.
const HackingRules := preload("res://godot/core/cwn_hacking.gd")
const ProgramRules := preload("res://godot/core/cwn_program_rules.gd")

func hacking_security_target(security: int, alerted: bool = false,
		important_device: bool = false, tech_quality: int = 0,
		inside_info: int = 0) -> Dictionary:
	return HackingRules.security_difficulty(
		security, alerted, important_device, tech_quality, inside_info)

func hacking_access(intelligence_score: int, program_rank: int,
		deck_bonus_access: int = 0) -> int:
	if program_rank < 0:
		# Untrained Program skill has no usable Access reserve.
		return 0
	return HackingRules.access_pool(attribute_modifier(intelligence_score),
		program_rank, deck_bonus_access)

func hacking_preflight(verb: String, target_family: String, access: int,
		cpu_used: int, cpu_total: int, loaded_verbs: Array,
		loaded_subjects: Array, subject: String,
		target_is_friendly: bool = true) -> Dictionary:
	return ProgramRules.preflight(verb, target_family, access, cpu_used,
		cpu_total, loaded_verbs, loaded_subjects, subject, target_is_friendly)

func hacking_check(intelligence_score: int, program_rank: int, difficulty: int,
		wireless: bool = false, vr_crown: bool = false,
		verb_modifier: int = 0, situational: int = 0) -> Dictionary:
	if program_rank < -1 or program_rank > 4:
		return {"ok": false, "reason": "invalid_program_rank"}
	return HackingRules.hacking_check(
		[_dice.roll(6), _dice.roll(6)],
		attribute_modifier(intelligence_score), program_rank, difficulty,
		wireless, vr_crown, verb_modifier, situational)

func hacking_resolve(preflight_result: Dictionary, access: int,
		cpu_used: int, check_success: bool,
		program_id: String = "") -> Dictionary:
	return ProgramRules.resolve(preflight_result, access, cpu_used,
		check_success, program_id)
