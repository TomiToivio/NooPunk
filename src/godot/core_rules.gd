class_name NooPunkCoreRules
extends RefCounted

const CANON_PATH := "res://data/rules/core.json"

var canon: Dictionary

func _init() -> void:
	var file := FileAccess.open(CANON_PATH, FileAccess.READ)
	if file == null:
		push_error("Cannot open canonical NoöPunk rule data.")
		canon = {}
		return
	canon = JSON.parse_string(file.get_as_text())

func attribute_ids() -> Array[String]:
	var ids: Array[String] = []
	for item in canon.get("attributes", []):
		ids.append(str(item["id"]))
	return ids

func empty_attributes(value: int = 0) -> Dictionary:
	var attributes := {}
	for attribute_id in attribute_ids():
		attributes[attribute_id] = value
	return attributes

func human_modifier(raw_3d6: int) -> int:
	if raw_3d6 < 3 or raw_3d6 > 18:
		push_error("Human attribute generation requires a 3d6 total in 3..18.")
		return 0
	return int(canon["human_3d6_modifier"][str(raw_3d6)])

func roll_3d6(rng: RandomNumberGenerator) -> int:
	return rng.randi_range(1, 6) + rng.randi_range(1, 6) + rng.randi_range(1, 6)

func generate_human_attributes(rng: RandomNumberGenerator) -> Dictionary:
	var raw := {}
	var modifiers := {}
	for attribute_id in attribute_ids():
		var rolled := roll_3d6(rng)
		raw[attribute_id] = rolled
		modifiers[attribute_id] = human_modifier(rolled)
	return {"raw_rolls": raw, "modifiers": modifiers}

func difficulty_names() -> Array[String]:
	# Order preserved from data/rules/core.json so displays match the rulebook.
	var names: Array[String] = []
	for key in canon.get("difficulties", {}).keys():
		names.append(str(key))
	return names

func difficulty_target(name: String) -> int:
	# Canonical lookup. The table lives in data/rules/core.json and the names are
	# asserted against the shared Python spec by tests, because the label "Hard"
	# changed target (12 -> 15) in issue #11 and a rename applied to only one
	# runtime would silently reinterpret an old difficulty.
	var table: Dictionary = canon.get("difficulties", {})
	if not table.has(name):
		push_error("Unknown difficulty '%s'; canonical difficulties are %s" % [name, ", ".join(difficulty_names())])
		return -1
	return int(table[name])

func difficulty_meaning(name: String) -> String:
	return str(canon.get("difficulty_meanings", {}).get(name, ""))

func resolve_check(
	rng: RandomNumberGenerator,
	attribute_modifier: int,
	target: int,
	extra_modifiers: Array[int] = [],
	has_skill: bool = true,
	trained_only: bool = false
) -> Dictionary:
	if trained_only and not has_skill:
		return {
			"attempted": false,
			"success": null,
			"total": null,
			"dice_total": null,
			"blocked_reason": "trained_only_without_skill"
		}

	var unskilled_modifier := 0
	if not has_skill:
		unskilled_modifier = int(canon["unskilled_penalty"])

	var dice_total := roll_3d6(rng)
	var extras_total := 0
	for modifier in extra_modifiers:
		extras_total += modifier
	var total := dice_total + attribute_modifier + extras_total + unskilled_modifier

	return {
		"attempted": true,
		"dice_total": dice_total,
		"attribute_modifier": attribute_modifier,
		"extra_modifiers": extra_modifiers.duplicate(),
		"unskilled_modifier": unskilled_modifier,
		"target": target,
		"total": total,
		"success": total >= target
	}

func compare_opposed(left_total: int, right_total: int) -> Dictionary:
	if left_total > right_total:
		return {"winner": "left", "unresolved_tie": false}
	if right_total > left_total:
		return {"winner": "right", "unresolved_tie": false}
	return {"winner": null, "unresolved_tie": true}
