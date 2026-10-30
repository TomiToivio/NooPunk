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
