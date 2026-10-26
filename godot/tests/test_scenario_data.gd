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

	rows.append_array(_chassis_rows(scenario, dialogue, level))
	return rows


## The sheet, the dialogue checks and the NPC stat lines must all speak the adopted chassis.
##
## This is the guard against the failure mode a rename leaves behind: a check naming a skill the sheet
## does not have resolves as *untrained*, so the character rolls -1 and nobody learns why. It reads the
## canonical vocabulary from the kernel, never from prose.
func _chassis_rows(scenario: Dictionary, dialogue: Dictionary, level: Dictionary) -> Array:
	var rows: Array = []
	var kernel: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/rules/wn_core.json"))
	var attributes: Array = kernel.get("stats", {}).get("final_list", [])
	# The skill vocabulary lives in the versioned baseline; the psionic disciplines live on the
	# psionics class. Reading them from one place each keeps this guard pointed at the real contract.
	var baseline: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/rules/without_number.json"))
	var skills: Array = (baseline.get("skills", {}).get("names", []) as Array).duplicate()
	for psionic_skill in NoopunkPsionics.DISCIPLINES:
		skills.append(psionic_skill)

	var sheet: Dictionary = scenario.get("player_sheet", {})
	var sheet_skills: Dictionary = sheet.get("skills", {})
	var sheet_attributes: Dictionary = sheet.get("attributes", {})

	var bad_attributes: Array = []
	var bad_skills: Array = []
	var unmakeable: Array = []
	for node_id in (dialogue.get("nodes", {}) as Dictionary).keys():
		var node: Dictionary = (dialogue["nodes"] as Dictionary)[node_id]
		for choice in node.get("choices", []):
			if not choice.has("check"):
				continue
			var spec: Dictionary = choice["check"]
			var attribute := String(spec.get("attribute", ""))
			var skill := String(spec.get("skill", ""))
			if not attributes.has(attribute):
				bad_attributes.append("%s -> %s" % [node_id, attribute])
			if not skills.has(skill):
				bad_skills.append("%s -> %s" % [node_id, skill])
			if not sheet_attributes.has(attribute) or not sheet_skills.has(skill):
				unmakeable.append("%s -> %s/%s" % [node_id, attribute, skill])
	rows.append(_eq("every check uses a canonical attribute", bad_attributes, []))
	rows.append(_eq("every check uses a canonical CWN or psionic skill", bad_skills, []))
	rows.append(_eq("the sheet can make every check it is offered", unmakeable, []))

	var psi: Dictionary = sheet.get("psionics", {})
	var best := 0
	for discipline in (psi.get("disciplines", {}) as Dictionary).keys():
		best = maxi(best, int((psi["disciplines"] as Dictionary)[discipline]))
	var table: Dictionary = kernel.get("stats", {}).get("modifier_table", {})
	var wisdom := int(table.get(str(int(sheet_attributes.get("WIS", 10))), 0))
	var constitution := int(table.get(str(int(sheet_attributes.get("CON", 10))), 0))
	rows.append(_eq("the sheet's Effort maximum follows the adopted formula",
		int(psi.get("effort_maximum", -1)), 1 + maxi(wisdom, constitution) + best))

	var incomplete: Array = []
	for npc in level.get("npcs", []):
		var stat_line: Dictionary = npc.get("stat_line", {})
		for field in ["hit_dice", "attack_bonus", "ac_melee", "ac_ranged", "hit_points", "trauma_target", "weapon"]:
			if not stat_line.has(field):
				incomplete.append("%s -> %s" % [npc.get("id", ""), field])
	rows.append(_eq("every level NPC carries a complete CWN stat line", incomplete, []))
	return rows

func _load(file_name: String) -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SCENARIO_DIR + file_name))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("scenario data test: %s is not a JSON object" % file_name)
		return {}
	return parsed

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]
