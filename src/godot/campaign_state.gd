class_name NooPunkCampaignState
extends RefCounted

## Campaign state for the source-faithful MVP (issue #750).
##
## Separate from the legacy Lakkahaltia CaseState; deliberately no autoload, so the older slice and
## the campaign slice cannot fight over globals. The save stores *choices the player made* and
## *undecided build options*, never assumed CWN statistics: writing a background or an edge into
## the save because the default felt reasonable is exactly the kind of silent invention #751 forbids.
const VERSION := 2
const SAVE_PATH := "user://noopunk_campaign_v2.json"

## Home -> HQ -> mission -> debrief. The mission is locked until accepted, and the debrief is locked
## until the mission is resolved, so the debrief cannot report on a mission that never happened.
## A character may also walk straight back to HQ from a resolved mission; the debrief is the
## formal debriefing, not a corridor the story is forced down.
const LOCATIONS := {
	"home": ["hq"],
	"hq": ["home", "mission"],
	"mission": ["debrief", "hq"],
	"debrief": ["hq"]
}

const OUTCOMES := ["success", "failure", "complication"]
const APPROACHES := ["investigative", "tactical", "mixed"]

var current_location: String = "home"
var flags: Dictionary = {}
var journal: Array[String] = []
var dialogue_choices: Dictionary = {}
var character: Dictionary = {}
var inventory: Array = []
var encounter: Dictionary = {}
var network: Dictionary = {}

var objective: Dictionary = {"id": "", "text": "", "resolved": false}
var outcome: String = ""
var approach: String = ""

func travel(destination: String) -> bool:
	if not LOCATIONS.has(current_location):
		return false
	if not LOCATIONS[current_location].has(destination):
		return false
	if destination == "mission" and not bool(flags.get("mission_accepted", false)):
		return false
	if destination == "debrief" and outcome.is_empty():
		return false
	current_location = destination
	return true

## The briefing hands the character a job. Recording it is what unlocks the mission leg.
func accept_mission(objective_id: String, objective_text: String) -> bool:
	if objective_id.is_empty() or not outcome.is_empty():
		return false
	if bool(flags.get("mission_accepted", false)):
		return false
	if not record_once("mission_accepted", "Mission accepted: " + objective_text):
		return false
	objective = {"id": objective_id, "text": objective_text, "resolved": false}
	return true

## Resolution is recorded once. It carries *how* the mission was solved as well as whether it was,
## because the source treats investigative and tactical solutions as equally legitimate.
func resolve_mission(result: String, how: String) -> bool:
	if not OUTCOMES.has(result) or not APPROACHES.has(how):
		return false
	if current_location != "mission":
		return false
	if not outcome.is_empty():
		return false
	outcome = result
	approach = how
	objective["resolved"] = true
	var line := "Mission %s (%s)" % [result, how]
	journal.append(line)
	return true

func mission_resolved() -> bool:
	return not outcome.is_empty()

## Character build slots deliberately left to the player. An undecided slot must stay visibly
## undecided all the way through save and reload.
func undecided_choices() -> Array:
	var pending: Array = []
	var choices: Dictionary = character.get("choices", {})
	for key in choices.keys():
		if str(choices[key]) == "choice" or str(choices[key]).is_empty():
			pending.append(key)
	return pending

func record_once(flag: String, journal_line: String) -> bool:
	if flag.is_empty() or bool(flags.get(flag, false)):
		return false
	flags[flag] = true
	if not journal_line.is_empty() and not journal.has(journal_line):
		journal.append(journal_line)
	return true

func to_data() -> Dictionary:
	return {
		"version": VERSION,
		"current_location": current_location,
		"flags": flags.duplicate(true),
		"journal": journal.duplicate(),
		"dialogue_choices": dialogue_choices.duplicate(true),
		"character": character.duplicate(true),
		"inventory": inventory.duplicate(true),
		"encounter": encounter.duplicate(true),
		"network": network.duplicate(true),
		"objective": objective.duplicate(true),
		"outcome": outcome,
		"approach": approach
	}

func from_data(data: Dictionary) -> bool:
	if int(data.get("version", -1)) != VERSION:
		return false
	var location: String = str(data.get("current_location", ""))
	if not LOCATIONS.has(location):
		return false
	for key in ["flags", "dialogue_choices", "character", "encounter", "network", "objective"]:
		if typeof(data.get(key, null)) != TYPE_DICTIONARY:
			return false
	for value in (data["flags"] as Dictionary).values():
		if typeof(value) != TYPE_BOOL:
			return false
	if location == "mission" and not bool((data["flags"] as Dictionary).get("mission_accepted", false)):
		return false
	for key in ["journal", "inventory"]:
		if typeof(data.get(key, null)) != TYPE_ARRAY:
			return false
	var next_journal: Array[String] = []
	for entry in data["journal"]:
		if typeof(entry) != TYPE_STRING:
			return false
		if not next_journal.has(entry):
			next_journal.append(entry)
	var next_outcome: String = str(data.get("outcome", ""))
	var next_approach: String = str(data.get("approach", ""))
	if not next_outcome.is_empty() and not OUTCOMES.has(next_outcome):
		return false
	if not next_approach.is_empty() and not APPROACHES.has(next_approach):
		return false
	if location == "debrief" and next_outcome.is_empty():
		return false
	current_location = location
	flags = data["flags"].duplicate(true)
	journal = next_journal
	dialogue_choices = data["dialogue_choices"].duplicate(true)
	character = data["character"].duplicate(true)
	inventory = data["inventory"].duplicate(true)
	encounter = data["encounter"].duplicate(true)
	network = data["network"].duplicate(true)
	objective = data["objective"].duplicate(true)
	outcome = next_outcome
	approach = next_approach
	return true

func save(path: String = SAVE_PATH) -> bool:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		return false
	file.store_string(JSON.stringify(to_data(), "\t"))
	file.close()
	return true

func load_save(path: String = SAVE_PATH) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return false
	return from_data(parsed)
