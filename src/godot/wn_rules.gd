class_name NooPunkWnRules
extends RefCounted

## Godot adapter over the Without Number core contract (#615, #620, #631).
##
## The author's direction of 2026-10-26 makes the Without Number chassis the baseline:
## 2d6 + attribute modifier + skill level + situational + aid against 6/8/10/12/14, attributes
## on 3..18 with a -2..+2 modifier band. The older `core_rules.gd` still resolves on the
## superseded 1d10 kernel; it is left in place because scenarios still run on it, and it must
## not be used for new content.
##
## Determinism: every roll goes through an injected RandomNumberGenerator, and `skill_check`
## also accepts explicit dice, so a table that rolled real dice can enter the result and a
## replay can be reproduced exactly.

const CONTRACT_PATH := "res://data/rules/wn_core.json"

var contract: Dictionary

func _init() -> void:
	var file := FileAccess.open(CONTRACT_PATH, FileAccess.READ)
	if file == null:
		push_error("Cannot open the Without Number contract at %s" % CONTRACT_PATH)
		contract = {}
		return
	contract = JSON.parse_string(file.get_as_text())

func attribute_modifier(score: int) -> int:
	## 3 -> -2, 4-7 -> -1, 8-13 -> 0, 14-17 -> +1, 18 -> +2.
	## Out-of-range scores are refused rather than clamped: a silent clamp hides a generation bug.
	if score < 3 or score > 18:
		push_error("attribute score %d is outside 3..18" % score)
		return 0
	var table: Dictionary = contract["stats"]["modifier_table"]
	return int(table.get(str(score), 0))

func difficulty(name: String) -> int:
	for key in contract["skill_check"]["difficulties"]:
		if String(contract["skill_check"]["difficulties"][key]).to_lower() == name.to_lower():
			return int(key)
	push_error("unknown difficulty %s" % name)
	return 8

func skill_check(
	attribute_score: int,
	skill_level: int,
	difficulty_value: int,
	rng: RandomNumberGenerator = null,
	dice: Array = []
) -> Dictionary:
	## 2d6 + attribute modifier + skill level against a difficulty. `skill_level = -1` is the
	## untrained penalty and is not a numbered level.
	if attribute_score < 3 or attribute_score > 18 or skill_level < -1 or skill_level > 4 or difficulty_value < 1:
		return {}
	var rolled: Array = dice.duplicate()
	if rolled.is_empty():
		if rng == null:
			push_error("skill_check needs either an rng or explicit dice")
			return {}
		rolled = [rng.randi_range(1, 6), rng.randi_range(1, 6)]
	if rolled.size() != 2:
		push_error("a 2d6 check needs exactly two dice")
		return {}
	for face in rolled:
		if not (face is int or face is float) or face != int(face) or int(face) < 1 or int(face) > 6:
			push_error("a d6 shows 1..6, got %s" % str(face))
			return {}
	var modifier := attribute_modifier(attribute_score)
	var total: int = int(rolled[0]) + int(rolled[1]) + modifier + skill_level
	return {
		"dice": rolled,
		"modifier": modifier,
		"skill_level": skill_level,
		"total": total,
		"difficulty": difficulty_value,
		"success": total >= difficulty_value,
	}
