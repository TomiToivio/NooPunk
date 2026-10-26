## One authoritative game state for the slice (#631): the character, the evidence, the journal, the
## flags, the current objectives and the ending.
##
## Registered as the autoload `GameState` in `project.godot` — a single owned instance rather than
## per-scene state, so that a scene change, a save and a reload cannot disagree about what happened.
##
## This class *uses* the rules adapter and never re-derives a mechanic. It also owns the seeded dice
## stream: the seed is saved, so a reloaded game continues the same sequence and a test can replay it.
extends Node

signal evidence_added(evidence_id: String)
signal journal_updated(line: String)
signal check_resolved(result: Dictionary)
signal objective_changed(objective_id: String)
signal ending_reached(ending: Dictionary)
signal flags_changed()

const SAVE_VERSION := 1
const SCENARIO_DIR := "res://godot/scenarios/lakkahaltia/"
const UNTRAINED := -1

var scenario: Dictionary = {}
var evidence_items: Dictionary = {}
var character: Dictionary = {}
var dialogue_nodes: Dictionary = {}

var evidence: Array = []
var journal: Array = []
var flags: Dictionary = {}
var current_objective: String = ""
var ending: Dictionary = {}
var run_seed: int = 1
var rules: RulesAdapter
var psionics: NoopunkPsionics
var psi_disciplines: Dictionary = {}
var psi_packages: Array = []

func _ready() -> void:
	rules = RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, run_seed)

## Loads the scenario bundle. Safe to call twice; the second call resets the case.
func new_case(roll_seed: int = 1) -> void:
	scenario = _load_json(SCENARIO_DIR + "scenario.json")
	var dialogue := _load_json(SCENARIO_DIR + "dialogue.json")
	dialogue_nodes = dialogue.get("nodes", {})
	character = (scenario.get("player_sheet", {}) as Dictionary).duplicate(true)
	_load_psionics()

	# evidence.json stores an array; the state keys it by id. Anything that is not an object with an id
	# is skipped rather than silently becoming a `null` entry the UI would then have to defend against.
	var by_id: Dictionary = {}
	for item in _load_json(SCENARIO_DIR + "evidence.json").get("items", []):
		if typeof(item) == TYPE_DICTIONARY and item.has("id"):
			by_id[String(item["id"])] = item
	evidence_items = by_id

	evidence = []
	journal = []
	flags = {}
	ending = {}
	# The objective id, not its text: the HUD asks for the text separately so a re-wording needs no state change.
	var objectives: Array = scenario.get("objectives", [])
	current_objective = String(objectives[0].get("id", "")) if not objectives.is_empty() else ""

	run_seed = roll_seed
	rules = RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, roll_seed)

func attribute(stat: String) -> int:
	return int((character.get("attributes", {}) as Dictionary).get(stat, 0))

## The character's level in a named skill, or UNTRAINED.
##
## Looked up by *skill* name ("Investigate", "Talk"), never by attribute name: the sheet keys its
## skills by their own names, so an attribute-keyed lookup silently returned UNTRAINED for every
## check in the game.
func skill(skill_name: String) -> int:
	var skills: Dictionary = character.get("skills", {})
	if skills.has(skill_name):
		return int(skills[skill_name])
	return UNTRAINED

# --- psionics (#652) ------------------------------------------------------------------------------
#
# The Effort pool and its package/rank gates live in `godot/core/psionics.gd`; a case only keeps the
# instance and its save record. A refused technique is a permission failure and spends nothing.

func _load_psionics() -> void:
	var sheet: Dictionary = character.get("psionics", {})
	psi_disciplines = (sheet.get("disciplines", {}) as Dictionary).duplicate(true)
	psi_packages = (sheet.get("packages", []) as Array).duplicate()
	psionics = NoopunkPsionics.new(attribute("WIS"), attribute("CON"), psi_disciplines, psi_packages)

## Uses a technique through the package and rank gates. Returns `{ok, reason|technique}`.
func use_technique(technique_id: String) -> Dictionary:
	if psionics == null:
		return { "ok": false, "reason": "psionics are not loaded" }
	var key := technique_id
	var index := 2
	while psionics.commitments.has(key):
		key = "%s#%d" % [technique_id, index]
		index += 1
	if not psionics.use_technique(key, technique_id):
		return { "ok": false, "reason": "not authorized or not trained for %s" % technique_id }
	add_journal("Psionic technique used: %s." % technique_id)
	return { "ok": true, "technique": technique_id }

func effort_maximum() -> int:
	return psionics.capacity() if psionics != null else 0

func effort_available() -> int:
	return psionics.available_effort() if psionics != null else 0

func end_scene() -> void:
	if psionics != null:
		psionics.end_scene()

func night_rest() -> void:
	if psionics != null:
		psionics.rest()

func add_evidence(evidence_id: String) -> bool:
	if evidence_id == "" or evidence.has(evidence_id) or not evidence_items.has(evidence_id):
		return false
	evidence.append(evidence_id)
	# An evidence item can carry the flags its discovery sets (E4 seals the annex, E5 anchors the place).
	# Applying them here is what makes those facts part of the state instead of prose in a data file.
	for flag in (evidence_items.get(evidence_id, {}) as Dictionary).get("flags", []):
		set_flag(String(flag))
	evidence_added.emit(evidence_id)
	_refresh_objective()
	return true

func has_evidence(evidence_id: String) -> bool:
	return evidence.has(evidence_id)

func add_journal(line: String) -> void:
	if line.strip_edges() == "":
		return
	journal.append(line)
	journal_updated.emit(line)

func set_flag(flag: String) -> void:
	if flag == "":
		return
	flags[flag] = true
	flags_changed.emit()
	_refresh_objective()

func has_flag(flag: String) -> bool:
	return bool(flags.get(flag, false))

## The one call the dialogue layer makes for a mechanic. The roll is public: the result carries the
## faces, the modifier, the skill level and the target, so the UI shows the maths rather than a verdict.
func resolve_check(stat: String, skill_name: String, difficulty: int) -> Dictionary:
	var result := rules.skill_check(attribute(stat), skill(skill_name), difficulty)
	result["stat"] = stat
	result["skill"] = skill_name
	var faces := ", ".join(result["dice"].map(func(face): return str(face)))
	add_journal("%s check: %s = [%s] %+d modifier %+d skill vs %d — %s" % [
		skill_name,
		result["die_pool"],
		faces,
		int(result["attribute_modifier"]),
		int(result["skill_level"]),
		int(result["difficulty"]),
		"success" if bool(result["success"]) else "failure",
	])
	check_resolved.emit(result)
	return result

func objective_text() -> String:
	for objective in scenario.get("objectives", []):
		if String(objective.get("id", "")) == current_objective:
			return String(objective.get("text", ""))
	return String(scenario.get("opening_objective", ""))

func _refresh_objective() -> void:
	# Objectives are an ordered list. Advance through every gate whose requirements are already met, so
	# that acquiring the last piece of evidence in one action cannot leave the HUD one objective behind.
	var objectives: Array = scenario.get("objectives", [])
	var guard := objectives.size() + 1
	while guard > 0:
		guard -= 1
		var index := -1
		for i in objectives.size():
			if String(objectives[i].get("id", "")) == current_objective:
				index = i
				break
		if index < 0 or index + 1 >= objectives.size():
			return
		var satisfied := true
		for required in objectives[index].get("requires_evidence", []):
			if not has_evidence(String(required)):
				satisfied = false
				break
		if not satisfied:
			return
		current_objective = String(objectives[index + 1].get("id", ""))
		objective_changed.emit(current_objective)

## Which endings the case currently supports. Both are ambiguous outcomes; neither labels a cause.
func available_endings() -> Array:
	var out: Array = []
	for candidate in scenario.get("endings", []):
		var ok := true
		for required_flag in candidate.get("requires_flags", []):
			if not has_flag(String(required_flag)):
				ok = false
				break
		if ok:
			for forbidden in candidate.get("forbids_flags", []):
				if has_flag(String(forbidden)):
					ok = false
					break
		if ok and candidate.has("requires_any_flags"):
			var any_ok := false
			for alt in candidate.get("requires_any_flags", []):
				if has_flag(String(alt)):
					any_ok = true
					break
			ok = any_ok
		if ok:
			out.append(candidate)
	return out

func reach_ending(ending_id: String) -> Dictionary:
	for candidate in available_endings():
		if String(candidate.get("id", "")) == ending_id:
			ending = candidate
			ending_reached.emit(candidate)
			return candidate
	return {}

func save_to_file(path: String = "user://save_lakkahaltia.json") -> Error:
	var payload := {
		"save_version": SAVE_VERSION,
		"scenario_id": scenario.get("id", ""),
		"run_seed": run_seed,
		"character": character,
		"evidence": evidence,
		"journal": journal,
		"flags": flags,
		"current_objective": current_objective,
		"ending": ending,
		"dice": rules.snapshot(),
		"psionics": psionics.snapshot() if psionics != null else {},
	}
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		return FileAccess.get_open_error()
	file.store_string(JSON.stringify(payload, "  "))
	file.close()
	return OK

func load_from_file(path: String = "user://save_lakkahaltia.json") -> Error:
	if not FileAccess.file_exists(path):
		return ERR_FILE_NOT_FOUND
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return ERR_FILE_CORRUPT
	var payload: Dictionary = parsed
	if int(payload.get("save_version", 0)) != SAVE_VERSION:
		return ERR_FILE_UNRECOGNIZED
	if String(payload.get("scenario_id", "")) != String(scenario.get("id", "")):
		return ERR_INVALID_DATA

	character = (payload.get("character", {}) as Dictionary).duplicate(true)
	evidence = payload.get("evidence", [])
	journal = payload.get("journal", [])
	flags = payload.get("flags", {})
	current_objective = String(payload.get("current_objective", ""))
	ending = payload.get("ending", {})

	# The dice stream resumes where the save left it: same seed, and the same number of rolls already spent.
	run_seed = int(payload.get("run_seed", 1))
	rules = RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, run_seed)
	var dice_state: Dictionary = payload.get("dice", {})
	if not dice_state.is_empty():
		rules.restore_dice(int(dice_state.get("seed", run_seed)), int(dice_state.get("rolls", 0)))

	# The Effort pool resumes where the save left it; a save written before the pool existed keeps
	# the sheet's own block.
	var psi_state: Dictionary = payload.get("psionics", {})
	if not psi_state.is_empty() and psionics != null:
		if not psionics.restore(psi_state):
			push_error("GameState: the saved Effort state is malformed; the pool starts unspent")

	flags_changed.emit()
	journal_updated.emit("Case reloaded.")
	return OK

func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("GameState: missing data file %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("GameState: %s is not a JSON object" % path)
		return {}
	return parsed
