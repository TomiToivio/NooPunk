## Game state behaviour: evidence, objectives, ending gates, save/load. The state is instantiated
## directly rather than through the autoload, so the suite runs without a scene tree.
extends RefCounted

const GameStateScript := preload("res://godot/core/game_state.gd")

func run() -> Array:
	var rows: Array = []
	var state = GameStateScript.new()
	state.new_case(11)

	rows.append(_eq("scenario loaded", String(state.scenario.get("id", "")), "lakkahaltia"))
	rows.append(_eq("six evidence items", state.evidence_items.size(), 6))
	rows.append(_eq("attribute read from the sheet", state.attribute("INT"), 14))
	rows.append(_eq("untrained skill is -1", state.skill("Forensics"), -1))
	rows.append(_eq("trained skill", state.skill("Psychology"), 3))

	rows.append(_eq("evidence added", state.add_evidence("E1"), true))
	rows.append(_eq("evidence not added twice", state.add_evidence("E1"), false))
	rows.append(_eq("unknown evidence refused", state.add_evidence("E404"), false))
	state.add_journal("first line")
	rows.append(_eq("journal is a log", state.journal.size(), 1))

	rows.append(_eq("objective starts at interviews",
		state.current_objective, "obj_interviews"))
	state.add_evidence("E3")
	state.add_evidence("E2")
	rows.append(_eq("interviews complete advances the objective",
		state.current_objective, "obj_annex"))

	# Ending gates: the anomalous ending needs the sealed annex *and* one of the two readings.
	rows.append(_eq("no ending before the annex", state.available_endings().size(), 0))
	state.set_flag("annex_seen")
	var mundane_only: Array = state.available_endings()
	rows.append(_eq("mundane ending available", mundane_only.size(), 1))
	rows.append(_eq("mundane ending id", String(mundane_only[0]["id"]), "mundane"))
	state.set_flag("place_anchored")
	rows.append(_eq("anomalous ending unlocks", state.available_endings().size(), 2))
	rows.append(_eq("ending reached", String(state.reach_ending("anomalous").get("id", "")), "anomalous"))

	# A check records the roll in the journal and publishes its parts.
	var before: int = state.journal.size()
	var result: Dictionary = state.resolve_check("INT", "Psychology", 10)
	rows.append(_eq("check publishes its die pool", String(result["die_pool"]), "2d6 (kernel)"))
	rows.append(_eq("check appends one journal line", state.journal.size(), before + 1))

	# Save/load round trip.
	var path := "user://test_save_lakkahaltia.json"
	rows.append(_eq("save returns OK", state.save_to_file(path), OK))
	var reloaded = GameStateScript.new()
	reloaded.new_case(11)
	rows.append(_eq("load returns OK", reloaded.load_from_file(path), OK))
	rows.append(_eq("evidence survives", reloaded.evidence, state.evidence))
	rows.append(_eq("flags survive", reloaded.flags, state.flags))
	rows.append(_eq("objective survives", reloaded.current_objective, state.current_objective))
	rows.append(_eq("journal survives", reloaded.journal, state.journal))
	rows.append(_eq("seed survives", reloaded.run_seed, state.run_seed))

	# A save from another case, or a future version, must be refused rather than half-applied.
	var raw := FileAccess.open(path, FileAccess.READ)
	var payload: Dictionary = JSON.parse_string(raw.get_as_text())
	raw.close()
	payload["save_version"] = 99
	var bumped := FileAccess.open(path, FileAccess.WRITE)
	bumped.store_string(JSON.stringify(payload))
	bumped.close()
	rows.append(_eq("version mismatch refused", reloaded.load_from_file(path), ERR_FILE_UNRECOGNIZED))

	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	return rows

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]
