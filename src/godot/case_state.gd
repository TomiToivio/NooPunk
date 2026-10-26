class_name NooPunkCaseState
extends RefCounted

## Authoritative case state: evidence, dialogue flags, skill-check outcomes, ending.
## Everything a save must carry is in to_dict(); nothing else is.

const SAVE_VERSION := 1

var case_id: String = ""
var evidence: Array[String] = []
var flags: Dictionary = {}
var visited: Dictionary = {}
var rolls: Array[Dictionary] = []
var ending: String = ""

func _init(p_case_id: String = "") -> void:
	case_id = p_case_id

func add_evidence(evidence_id: String) -> bool:
	## Returns true when the evidence is new, so the UI can say "added" rather than "already known".
	if evidence_id.is_empty() or evidence.has(evidence_id):
		return false
	evidence.append(evidence_id)
	return true

func has_evidence(evidence_id: String) -> bool:
	return evidence.has(evidence_id)

func set_flag(key: String, value: Variant = true) -> void:
	flags[key] = value

func get_flag(key: String, default: Variant = false) -> Variant:
	return flags.get(key, default)

func record_roll(entry: Dictionary) -> void:
	rolls.append(entry.duplicate(true))

func mark_visited(npc_id: String, topic_id: String) -> void:
	var key := "%s:%s" % [npc_id, topic_id]
	visited[key] = true

func topic_seen(npc_id: String, topic_id: String) -> bool:
	return visited.has("%s:%s" % [npc_id, topic_id])

func can_end(threshold: int) -> bool:
	return ending.is_empty() and evidence.size() >= threshold

func finish(ending_id: String) -> void:
	if ending.is_empty():
		ending = ending_id

func to_dict() -> Dictionary:
	return {
		"version": SAVE_VERSION,
		"case_id": case_id,
		"evidence": evidence.duplicate(),
		"flags": flags.duplicate(true),
		"visited": visited.duplicate(true),
		"rolls": rolls.duplicate(true),
		"ending": ending,
	}

func from_dict(data: Dictionary) -> bool:
	## Refuses a save from a different version or case rather than loading half of it.
	if int(data.get("version", -1)) != SAVE_VERSION:
		push_error("unsupported save version")
		return false
	if String(data.get("case_id", "")) != case_id:
		push_error("save belongs to another case")
		return false
	evidence = []
	for item in data.get("evidence", []):
		evidence.append(String(item))
	flags = data.get("flags", {}).duplicate(true)
	visited = data.get("visited", {}).duplicate(true)
	rolls = []
	for entry in data.get("rolls", []):
		rolls.append(entry.duplicate(true))
	ending = String(data.get("ending", ""))
	return true

func save_to(path: String) -> bool:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("cannot write save")
		return false
	file.store_string(JSON.stringify(to_dict(), "\t"))
	return true

func load_from(path: String) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("save is not a JSON object")
		return false
	return from_dict(parsed)
