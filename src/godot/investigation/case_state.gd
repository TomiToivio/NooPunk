extends RefCounted

const Rules = preload("res://src/godot/wn_rules.gd")
const DATA = "res://data/scenarios/lakkahaltia.json"
const SAVE = "user://lakkahaltia-v1.json"
var content: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(DATA))
var state: Dictionary
var rng := RandomNumberGenerator.new()

func _init() -> void:
	rng.randomize()
	reset()

func reset() -> void:
	state = {"version": 1, "character": content.character.duplicate(true), "flags": {}, "evidence": [], "journal": [], "position": [0, 0, 6], "roll": {}, "ending": ""}

func interview(id: String, choice: int) -> String:
	if not content.interviews.has(id) or choice < 0 or choice >= content.interviews[id].choices.size():
		return ""
	var item: Dictionary = content.interviews[id].choices[choice]
	state.flags[id] = true
	if not state.flags.has(item.flag):
		state.flags[item.flag] = true
		state.journal.append(content.interviews[id].name + ": " + item.reply)
	return item.reply

func collect(id: String) -> void:
	if content.evidence.has(id) and not id in state.evidence:
		state.evidence.append(id)

func inspect_record(dice: Array = []) -> Dictionary:
	collect("record")
	if state.roll.is_empty():
		state.roll = Rules.new().skill_check(int(state.character.attributes.INT), int(state.character.skills.Program), 8, rng, dice)
		if state.roll.get("success", false):
			collect("audit")
		else:
			state.journal.append("Clock comparison inconclusive. Ask the nurse for the chronology; the case can continue.")
	return state.roll

func encounter() -> bool:
	if not state.flags.has("patient") or not "record" in state.evidence:
		return false
	collect("reflection")
	state.flags.encounter = true
	return true

func can_finish() -> bool:
	return state.flags.has("doctor") and state.flags.has("nurse") and state.flags.has("patient") and "record" in state.evidence

func finish(kind: String) -> String:
	if not can_finish() or not content.endings.has(kind):
		return "Interview all three witnesses and inspect the record first."
	if kind == "anomalous" and not state.flags.has("encounter"):
		return "Inspect the consultation-room window first."
	state.ending = kind
	return content.endings[kind]

func save_game(path: String = SAVE) -> Error:
	var file := FileAccess.open(path + ".tmp", FileAccess.WRITE)
	if file == null:
		return FileAccess.get_open_error()
	file.store_string(JSON.stringify(state))
	file.close()
	return DirAccess.rename_absolute(path + ".tmp", path)

func load_game(path: String = SAVE) -> Error:
	if not FileAccess.file_exists(path):
		return ERR_FILE_NOT_FOUND
	var value = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not value is Dictionary or value.get("version") != 1:
		return ERR_INVALID_DATA
	for key in state:
		if not value.has(key) or typeof(value[key]) != typeof(state[key]) and not (key == "version" and value[key] is float):
			return ERR_INVALID_DATA
	if value.position.size() != 3 or not value.character.get("attributes") is Dictionary or not value.character.get("skills") is Dictionary:
		return ERR_INVALID_DATA
	for coordinate in value.position:
		if not (coordinate is float or coordinate is int) or not is_finite(float(coordinate)) or abs(float(coordinate)) > 20:
			return ERR_INVALID_DATA
	for attribute in content.character.attributes:
		var score = value.character.attributes.get(attribute)
		if not (score is float or score is int) or score != int(score) or score < 3 or score > 18:
			return ERR_INVALID_DATA
	for skill in content.character.skills:
		var rank = value.character.skills.get(skill)
		if not (rank is float or rank is int) or rank != int(rank) or rank < -1 or rank > 4:
			return ERR_INVALID_DATA
	for clue in value.evidence:
		if not clue is String or not content.evidence.has(clue):
			return ERR_INVALID_DATA
	for line in value.journal:
		if not line is String:
			return ERR_INVALID_DATA
	if value.ending != "" and not content.endings.has(value.ending):
		return ERR_INVALID_DATA
	if not value.roll.is_empty():
		for field in ["dice", "modifier", "skill_level", "total", "difficulty", "success"]:
			if not value.roll.has(field):
				return ERR_INVALID_DATA
		if not value.roll.dice is Array or value.roll.dice.size() != 2 or not value.roll.success is bool:
			return ERR_INVALID_DATA
		for field in ["modifier", "skill_level", "total", "difficulty"]:
			if not (value.roll[field] is float or value.roll[field] is int):
				return ERR_INVALID_DATA
	state = value
	return OK
