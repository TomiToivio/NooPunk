extends "res://tests/godot/godot_test.gd"

## Navigation integrity for the dialogue data: every `next` names a node that exists and
## every graph can terminate. This is the data contract the running dialogue engine needs;
## it does not assert anything about the prose.

func _dialogue() -> Dictionary:
	var file := FileAccess.open("res://data/scenarios/lakkahaltia/dialogue.json", FileAccess.READ)
	return JSON.parse_string(file.get_as_text())

func test_every_next_target_exists() -> void:
	var data := _dialogue()
	for npc_id in data.keys():
		if str(npc_id).begins_with("_"):
			continue
		var graph: Dictionary = data[npc_id]
		var nodes: Dictionary = graph["nodes"]
		check(nodes.has(graph["start"]), "%s start node exists" % npc_id)
		for node_id in nodes.keys():
			for choice in nodes[node_id].get("choices", []):
				var next: Variant = choice.get("next", null)
				if next != null:
					check(nodes.has(str(next)), "%s/%s -> %s exists" % [npc_id, node_id, str(next)])

func test_every_graph_has_a_terminating_choice() -> void:
	var data := _dialogue()
	for npc_id in data.keys():
		if str(npc_id).begins_with("_"):
			continue
		var nodes: Dictionary = data[npc_id]["nodes"]
		var terminal := 0
		for node_id in nodes.keys():
			for choice in nodes[node_id].get("choices", []):
				if choice.get("next", null) == null:
					terminal += 1
		check(terminal > 0, "%s has at least one way out" % npc_id)

func test_the_case_gives_access_to_three_speakers_and_two_checks() -> void:
	var state := NooPunkCaseState.new(
		"res://data/scenarios/lakkahaltia/case.json",
		"res://data/scenarios/lakkahaltia/dialogue.json"
	)
	for npc_id in ["doctor", "nurse", "patient"]:
		check(state.start_dialogue(npc_id), "%s is reachable" % npc_id)
		state.end_dialogue()
	var checks := 0
	for obj in state.case_data.get("objects", []):
		if obj.has("check"):
			checks += 1
			check(obj["check"].has("stat") and obj["check"].has("skill") and obj["check"].has("dv"), "a check names stat, skill and DV")
	check_eq(checks, 2, "two mechanically meaningful checks")
