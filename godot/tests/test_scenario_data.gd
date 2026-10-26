## Scenario data integrity: every node reference, evidence id and ending gate in the JSON must resolve.
##
## This is a *data contract* test on executable game content — the dialogue graph the runner walks — not a
## check on prose. If an author renames a node or an evidence id in the JSON, this fails at the table's
## cost instead of theirs.
extends RefCounted

const SCENARIO_DIR := "res://godot/scenarios/lakkahaltia/"

func run() -> Array:
	var rows: Array = []
	var dialogue: Dictionary = _load("dialogue.json")
	var evidence: Dictionary = _load("evidence.json")
	var scenario: Dictionary = _load("scenario.json")
	var level: Dictionary = _load("level_hospital.json")

	rows.append(_eq("dialogue has nodes", dialogue.has("nodes"), true))
	var nodes: Dictionary = dialogue.get("nodes", {})
	var evidence_ids: Dictionary = {}
	for item in evidence.get("items", []):
		evidence_ids[String(item["id"])] = true

	var dangling: Array = []
	var unknown_evidence: Array = []
	for node_id in nodes.keys():
		var node: Dictionary = nodes[node_id]
		if node.has("next") and node["next"] != null and not nodes.has(String(node["next"])):
			dangling.append("%s.next -> %s" % [node_id, node["next"]])
		for evidence_id in node.get("effects", {}).get("add_evidence", []):
			if not evidence_ids.has(String(evidence_id)):
				unknown_evidence.append("%s -> %s" % [node_id, evidence_id])
		for choice in node.get("choices", []):
			var effects: Dictionary = choice.get("effects", {})
			for evidence_id in effects.get("add_evidence", []):
				if not evidence_ids.has(String(evidence_id)):
					unknown_evidence.append("%s.choice -> %s" % [node_id, evidence_id])
			if choice.has("check"):
				var spec: Dictionary = choice["check"]
				for key in ["success_node", "failure_node"]:
					if not nodes.has(String(spec.get(key, ""))):
						dangling.append("%s.check.%s -> %s" % [node_id, key, spec.get(key, "")])
			elif choice.has("next") and not nodes.has(String(choice["next"])):
				dangling.append("%s.choice.next -> %s" % [node_id, choice["next"]])

	rows.append(_eq("no dangling node references", dangling, []))
	rows.append(_eq("no unknown evidence ids", unknown_evidence, []))

	var entry_problems: Array = []
	for npc_id in dialogue.get("npcs", {}).keys():
		var entry := String(dialogue["npcs"][npc_id])
		if not nodes.has(entry):
			entry_problems.append("%s -> %s" % [npc_id, entry])
	rows.append(_eq("every NPC entry node exists", entry_problems, []))

	# Every level NPC must be reachable in conversation, and every prop interaction must be known to the
	# level builder; a silent mismatch would leave an NPC that cannot be talked to.
	var level_npcs: Array = []
	for npc in level.get("npcs", []):
		level_npcs.append(String(npc["id"]))
	var missing_dialogue: Array = []
	for npc_id in level_npcs:
		if not dialogue.get("npcs", {}).has(npc_id):
			missing_dialogue.append(npc_id)
	rows.append(_eq("every level NPC has dialogue", missing_dialogue, []))
	rows.append(_eq("three conversational NPCs", level_npcs.size(), 3))

	var prop_interactions: Array = []
	for prop in level.get("props", []):
		prop_interactions.append(String(prop.get("interaction", "")))
	for expected in ["terminal", "records", "drawing"]:
		rows.append(_eq("prop interaction %s present" % expected, prop_interactions.has(expected), true))

	# The two endings are distinct, ambiguous outcomes; both must be reachable from the same gate set.
	var endings: Array = scenario.get("endings", [])
	rows.append(_eq("two endings", endings.size(), 2))
	var ids: Array = []
	for ending in endings:
		ids.append(String(ending.get("id", "")))
	rows.append(_eq("endings are mundane and anomalous", ids, ["mundane", "anomalous"]))

	var flag_problems: Array = []
	for objective in scenario.get("objectives", []):
		for evidence_id in objective.get("requires_evidence", []):
			if not evidence_ids.has(String(evidence_id)):
				flag_problems.append("objective %s -> %s" % [objective.get("id", ""), evidence_id])
	rows.append(_eq("objective gates reference real evidence", flag_problems, []))

	return rows

func _load(file_name: String) -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SCENARIO_DIR + file_name))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("scenario data test: %s is not a JSON object" % file_name)
		return {}
	return parsed

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]
