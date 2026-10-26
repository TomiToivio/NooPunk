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
## This is the test that would have caught the class of bug a rename introduces: a check naming a
## skill the sheet does not have silently resolves as *untrained*, so the character rolls -1 and the
## table never learns why the detective cannot read a record.
func _chassis_rows(scenario: Dictionary, dialogue: Dictionary, level: Dictionary) -> Array:
	var rows: Array = []
	var kernel: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/rules/wn_core.json"))
	var attributes: Array = kernel.get("stats", {}).get("final_list", [])
	var skills: Array = (kernel.get("skills", {}).get("list", []) as Array).duplicate()
	for psionic_skill in kernel.get("skills", {}).get("psionic_skills", []):
		skills.append(psionic_skill)

	var profile: Dictionary = scenario.get("rules_profile", {})
	rows.append(_eq("the scenario declares the CWN chassis", String(profile.get("chassis", "")), "cwn"))
	rows.append(_eq("the scenario names the kernel it resolves against",
		String(profile.get("contract", "")), "res://data/rules/wn_core.json"))

	var sheet: Dictionary = scenario.get("player_sheet", {})
	var sheet_skills: Dictionary = sheet.get("skills", {})
	var sheet_attributes: Dictionary = sheet.get("attributes", {})

	var unknown_attributes: Array = []
	var unknown_skills: Array = []
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
				unknown_attributes.append("%s -> %s" % [node_id, attribute])
			if not skills.has(skill):
				unknown_skills.append("%s -> %s" % [node_id, skill])
			if not sheet_attributes.has(attribute) or not sheet_skills.has(skill):
				unmakeable.append("%s -> %s/%s" % [node_id, attribute, skill])
	rows.append(_eq("every check uses a canonical attribute", unknown_attributes, []))
	rows.append(_eq("every check uses a canonical CWN or psionic skill", unknown_skills, []))
	rows.append(_eq("the player sheet can actually make every check", unmakeable, []))

	var sheet_fields := ["level", "hit_points", "max_hit_points", "attack_bonus", "armor_class",
		"saves", "system_strain", "weapons", "cyberware", "psionics"]
	var missing_fields: Array = []
	for field in sheet_fields:
		if not sheet.has(field):
			missing_fields.append(field)
	rows.append(_eq("the player sheet is a CWN stat line", missing_fields, []))

	var strain: Dictionary = sheet.get("system_strain", {})
	var constitution := int(sheet_attributes.get("CON", 0))
	rows.append(_eq("System Strain maximum is the Constitution score",
		int(strain.get("maximum", -1)), constitution))

	var psi: Dictionary = sheet.get("psionics", {})
	var disciplines: Dictionary = psi.get("disciplines", {})
	var best_psi := 0
	for discipline in disciplines.keys():
		best_psi = maxi(best_psi, int(disciplines[discipline]))
	var wisdom_mod := 0
	var con_mod := 0
	for entry in (kernel.get("stats", {}).get("modifier_table", {}) as Dictionary).keys():
		if int(entry) == int(sheet_attributes.get("WIS", 10)):
			wisdom_mod = int(kernel["stats"]["modifier_table"][entry])
		if int(entry) == int(sheet_attributes.get("CON", 10)):
			con_mod = int(kernel["stats"]["modifier_table"][entry])
	rows.append(_eq("the sheet's Effort maximum follows the adopted formula",
		int(psi.get("effort_maximum", -1)), 1 + maxi(wisdom_mod, con_mod) + best_psi))
	var catalogue: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/rules/psionics_techniques.json"))
	var known_ids: Dictionary = {}
	for entry in catalogue.get("techniques", []):
		known_ids[String(entry.get("id", ""))] = entry
	for entry in (catalogue.get("discipline_cores", {}) as Dictionary).values():
		known_ids[String(entry.get("id", ""))] = entry

	var unknown_techniques: Array = []
	var illegal_techniques: Array = []
	for technique_id in psi.get("known_techniques", []):
		var key := String(technique_id)
		if not known_ids.has(key):
			unknown_techniques.append(key)
			continue
		var entry: Dictionary = known_ids[key]
		var discipline := String(entry.get("discipline", ""))
		for core_discipline in (catalogue.get("discipline_cores", {}) as Dictionary).keys():
			if String(((catalogue["discipline_cores"] as Dictionary)[core_discipline] as Dictionary).get("id", "")) == key:
				discipline = String(core_discipline)
		var trained := int(disciplines.get(discipline, -1))
		if trained < int(entry.get("min_skill", 0)):
			illegal_techniques.append("%s needs %s-%d" % [key, discipline, int(entry.get("min_skill", 0))])
	rows.append(_eq("every known technique exists in the catalogue", unknown_techniques, []))
	rows.append(_eq("the sheet is trained for every technique it knows", illegal_techniques, []))

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
