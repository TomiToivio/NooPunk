class_name NooPunkCampaignState
extends RefCounted

## Separate from the legacy Lakkahaltia CaseState; deliberately no autoload.
## Save data stores choices made by the player, not assumed CWN character stats.
const VERSION := 1
const SAVE_PATH := "user://noopunk_campaign_v1.json"
const LOCATIONS := {
	"home": ["hq"],
	"hq": ["home", "mission"],
	"mission": ["hq"]
}

var current_location: String = "home"
var flags: Dictionary = {}
var journal: Array[String] = []
var dialogue_choices: Dictionary = {}
var character: Dictionary = {}
var inventory: Array = []
var encounter: Dictionary = {}
var network: Dictionary = {}

func travel(destination: String) -> bool:
	if not LOCATIONS.has(current_location):
		return false
	if not LOCATIONS[current_location].has(destination):
		return false
	if destination == "mission" and not bool(flags.get("mission_accepted", false)):
		return false
	current_location = destination
	return true

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
		"network": network.duplicate(true)
	}

func from_data(data: Dictionary) -> bool:
	if int(data.get("version", -1)) != VERSION:
		return false
	var location: String = str(data.get("current_location", ""))
	if not LOCATIONS.has(location):
		return false
	if location == "mission" and not bool((data.get("flags", {}) as Dictionary).get("mission_accepted", false)):
		return false
	for key in ["flags", "dialogue_choices", "character", "encounter", "network"]:
		if typeof(data.get(key, null)) != TYPE_DICTIONARY:
			return false
	for key in ["journal", "inventory"]:
		if typeof(data.get(key, null)) != TYPE_ARRAY:
			return false
	for flag_value in (data["flags"] as Dictionary).values():
		if typeof(flag_value) != TYPE_BOOL:
			return false
	for choice in (data["dialogue_choices"] as Dictionary).values():
		if typeof(choice) != TYPE_STRING and typeof(choice) != TYPE_INT:
			return false
	var next_journal: Array[String] = []
	for entry in data["journal"]:
		if typeof(entry) != TYPE_STRING:
			return false
		if not next_journal.has(entry):
			next_journal.append(entry)
	current_location = location
	flags = data["flags"].duplicate(true)
	journal = next_journal
	dialogue_choices = data["dialogue_choices"].duplicate(true)
	character = data["character"].duplicate(true)
	inventory = data["inventory"].duplicate(true)
	encounter = data["encounter"].duplicate(true)
	network = data["network"].duplicate(true)
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
