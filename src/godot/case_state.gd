class_name NooPunkCaseState
extends RefCounted

## Authoritative, scene-independent state for the Lakkahaltia case.
##
## Everything the case knows lives here: clues, flags, journal lines, complications, the
## current dialogue node and the ending. The 3D scene only renders this object and calls
## into it, which is what lets the whole case be tested headlessly and reused by a
## tabletop GM or a later strategy layer.
##
## Save format is versioned and plain JSON (`user://lakkahaltia_save.json` in game).

const SAVE_VERSION := 2

var check_results: Dictionary = {}
var player_position: Array = [0.0, 0.0, 2.0]

signal state_changed

var case_data: Dictionary = {}
var dialogue_data: Dictionary = {}

var clues: Array[String] = []
var flags: Dictionary = {}
var journal: Array[String] = []
var complications: Array[String] = []

var dialogue_npc: String = ""
var dialogue_node: String = ""
var last_speaker: String = ""
var last_text: String = ""

var finished: bool = false
var chosen_ending: String = ""

func _init(case_path: String = "res://data/scenarios/lakkahaltia/case.json",
		dialogue_path: String = "res://data/scenarios/lakkahaltia/dialogue.json") -> void:
	case_data = _read_json(case_path)
	dialogue_data = _read_json(dialogue_path)

func _read_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Cannot open %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("Not a JSON object: %s" % path)
		return {}
	return parsed

# -- character ---------------------------------------------------------------------------

func character() -> Dictionary:
	return case_data.get("character", {})

func stat(name: String) -> int:
	return int(character().get("stats", {}).get(name, 0))

func skill(name: String) -> int:
	return int(character().get("skills", {}).get(name, -1))

# -- state ---------------------------------------------------------------------------------

func has_clue(id: String) -> bool:
	return clues.has(id)

func add_clue(id: String) -> bool:
	if id.is_empty() or clues.has(id):
		return false
	if not case_data.get("clues", {}).has(id):
		push_warning("Unknown clue id: %s" % id)
		return false
	clues.append(id)
	state_changed.emit()
	return true

func has_flag(id: String) -> bool:
	return bool(flags.get(id, false))

func set_flag(id: String, value: bool = true) -> void:
	flags[id] = value
	state_changed.emit()

func add_journal(line: String) -> void:
	if line.is_empty() or journal.has(line):
		return
	journal.append(line)
	state_changed.emit()

func add_complication(id: String) -> void:
	if id.is_empty() or complications.has(id):
		return
	complications.append(id)
	state_changed.emit()

func clue_label(id: String) -> String:
	return str(case_data.get("clues", {}).get(id, {}).get("label", id))

# -- effects -------------------------------------------------------------------------------

## Apply a list of effect dictionaries: {clue}, {flag}, {journal}, {complication}.
func apply_effects(effects: Array) -> void:
	for raw in effects:
		if typeof(raw) != TYPE_DICTIONARY:
			continue
		var effect: Dictionary = raw
		if effect.has("clue"):
			add_clue(str(effect["clue"]))
		if effect.has("flag"):
			set_flag(str(effect["flag"]), true)
		if effect.has("journal"):
			add_journal(str(effect["journal"]))
		if effect.has("complication"):
			add_complication(str(effect["complication"]))

# -- dialogue ------------------------------------------------------------------------------

func start_dialogue(npc_id: String) -> bool:
	var graph: Dictionary = dialogue_data.get(npc_id, {})
	if graph.is_empty():
		return false
	dialogue_npc = npc_id
	return _enter(str(graph.get("start", "")))

func _enter(node_id: String) -> bool:
	if node_id.is_empty():
		_end_dialogue()
		return false
	var nodes: Dictionary = dialogue_data.get(dialogue_npc, {}).get("nodes", {})
	if not nodes.has(node_id):
		push_warning("Unknown dialogue node: %s" % node_id)
		_end_dialogue()
		return false
	dialogue_node = node_id
	var node: Dictionary = nodes[node_id]
	apply_effects(node.get("effects", []))
	last_speaker = str(node.get("speaker", ""))
	last_text = str(node.get("text", ""))
	state_changed.emit()
	return true

func in_dialogue() -> bool:
	return not dialogue_node.is_empty()

func current_node() -> Dictionary:
	if dialogue_node.is_empty():
		return {}
	return dialogue_data.get(dialogue_npc, {}).get("nodes", {}).get(dialogue_node, {})

## Choices whose conditions pass, as [{ "index": int, "text": String }].
func available_choices() -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	var choices: Array = current_node().get("choices", [])
	for index in choices.size():
		var choice: Dictionary = choices[index]
		if _conditions_pass(choice):
			out.append({ "index": index, "text": str(choice.get("text", "...")) })
	return out

func _conditions_pass(choice: Dictionary) -> bool:
	if choice.has("if_flag") and not has_flag(str(choice["if_flag"])):
		return false
	if choice.has("unless_flag") and has_flag(str(choice["unless_flag"])):
		return false
	if choice.has("if_clue") and not has_clue(str(choice["if_clue"])):
		return false
	return true

## Take a choice by its position in available_choices(), not the raw list index.
func choose(available_index: int) -> bool:
	var available := available_choices()
	if available_index < 0 or available_index >= available.size():
		return false
	var choices: Array = current_node().get("choices", [])
	var choice: Dictionary = choices[int(available[available_index]["index"])]
	apply_effects(choice.get("effects", []))
	var next: Variant = choice.get("next", null)
	if next == null:
		_end_dialogue()
		return true
	return _enter(str(next))

func _end_dialogue() -> void:
	dialogue_npc = ""
	dialogue_node = ""
	last_speaker = ""
	last_text = ""
	state_changed.emit()

func end_dialogue() -> void:
	_end_dialogue()

# -- world objects -------------------------------------------------------------------------

func object_definition(object_id: String) -> Dictionary:
	for raw in case_data.get("objects", []):
		if str(raw.get("id", "")) == object_id:
			return raw
	return {}

func can_use_object(object_id: String) -> bool:
	var definition := object_definition(object_id)
	if definition.is_empty():
		return false
	var required := str(definition.get("requires_flag", ""))
	return required.is_empty() or has_flag(required)

# -- endings -------------------------------------------------------------------------------

func available_endings() -> Array[String]:
	var out: Array[String] = []
	var required_clues: Array = case_data.get("resolution", {}).get("requires_clues", [])
	for clue_id in required_clues:
		if not has_clue(str(clue_id)):
			return out
	for ending_id in case_data.get("endings", {}).keys():
		var requires: Array = case_data.get("endings", {})[ending_id].get("requires", [])
		var ok := true
		for flag_id in requires:
			if not has_flag(str(flag_id)):
				ok = false
				break
		if ok:
			out.append(str(ending_id))
	return out

func choose_ending(ending_id: String) -> bool:
	if not available_endings().has(ending_id):
		return false
	chosen_ending = ending_id
	finished = true
	state_changed.emit()
	return true

func ending_prose(ending_id: String) -> String:
	return str(case_data.get("endings", {}).get(ending_id, {}).get("prose", ""))

func ending_label(ending_id: String) -> String:
	return str(case_data.get("endings", {}).get(ending_id, {}).get("label", ending_id))

# -- persistence ---------------------------------------------------------------------------

func to_dict() -> Dictionary:
	return {
		"save_version": SAVE_VERSION,
		"character": character().duplicate(true),
		"check_results": check_results.duplicate(true),
		"player_position": player_position.duplicate(),
		"case_id": str(case_data.get("id", "")),
		"clues": clues.duplicate(),
		"flags": flags.duplicate(true),
		"journal": journal.duplicate(),
		"complications": complications.duplicate(),
		"finished": finished,
		"chosen_ending": chosen_ending
	}

func from_dict(data: Dictionary) -> bool:
	if int(data.get("save_version", -1)) != SAVE_VERSION:
		return false
	if data.get("case_id") != case_data.get("id"):
		return false
	if not data.get("character") is Dictionary or not data.get("check_results") is Dictionary or not data.get("player_position") is Array:
		return false
	var saved_character: Dictionary = data.character
	if not saved_character.get("stats") is Dictionary or not saved_character.get("skills") is Dictionary:
		return false
	for stat_name in character().stats:
		var score = saved_character.stats.get(stat_name)
		if not (score is float or score is int) or score != int(score) or score < 3 or score > 18:
			return false
	for skill_name in saved_character.skills:
		var rank = saved_character.skills[skill_name]
		if not (rank is float or rank is int) or rank != int(rank) or rank < -1 or rank > 4:
			return false
	if data.player_position.size() != 3:
		return false
	for coordinate in data.player_position:
		if not (coordinate is float or coordinate is int) or not is_finite(float(coordinate)):
			return false
	for key in ["clues", "journal", "complications"]:
		if not data.get(key) is Array:
			return false
		for item in data[key]:
			if not item is String:
				return false
	if not data.get("flags") is Dictionary or not data.get("finished") is bool or not data.get("chosen_ending") is String:
		return false
	for object_id in data.check_results:
		var result = data.check_results[object_id]
		if object_definition(object_id).is_empty() or not result is Dictionary:
			return false
		for key in ["dice", "modifier", "skill_level", "total", "difficulty", "success"]:
			if not result.has(key):
				return false
		if not result.dice is Array or result.dice.size() != 2 or not result.success is bool:
			return false
		for face in result.dice:
			if not (face is float or face is int) or face != int(face) or face < 1 or face > 6:
				return false
		for key in ["modifier", "skill_level", "total", "difficulty"]:
			if not (result[key] is float or result[key] is int):
				return false
	case_data.character = saved_character.duplicate(true)
	check_results = data.check_results.duplicate(true)
	player_position = data.player_position.duplicate()
	clues.clear()
	flags.clear()
	journal.clear()
	complications.clear()
	for clue in data.get("clues", []):
		clues.append(str(clue))
	flags = data.get("flags", {}).duplicate(true)
	for line in data.get("journal", []):
		journal.append(str(line))
	for item in data.get("complications", []):
		complications.append(str(item))
	finished = bool(data.get("finished", false))
	chosen_ending = str(data.get("chosen_ending", ""))
	_end_dialogue()
	state_changed.emit()
	return true

func save_to(path: String) -> bool:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("Cannot write save at %s" % path)
		return false
	file.store_string(JSON.stringify(to_dict(), "\t"))
	file.close()
	return true

func load_from(path: String) -> bool:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return false
	return from_dict(parsed)
