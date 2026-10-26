extends "res://tests/godot/godot_test.gd"

## The case state is the authoritative game state: clues, flags, journal, endings, save file.

func _state() -> NooPunkCaseState:
	return NooPunkCaseState.new(
		"res://data/scenarios/lakkahaltia/case.json",
		"res://data/scenarios/lakkahaltia/dialogue.json"
	)

func test_the_case_file_loads_with_a_playable_character() -> void:
	var state := _state()
	check_eq(state.case_data.get("id"), "lakkahaltia", "case id")
	check_eq(state.stat("INT"), 7, "Romppainen INT comes from the case file")
	check_eq(state.skill("Investigate"), 3, "skill level comes from the case file")
	check_eq(state.case_data.get("npcs", []).size(), 3, "three conversational NPCs")

func test_effects_are_idempotent_and_typed() -> void:
	var state := _state()
	state.apply_effects([{ "clue": "record-1601" }, { "flag": "met_doctor" }, { "journal": "note" }])
	state.apply_effects([{ "clue": "record-1601" }, { "flag": "met_doctor" }, { "journal": "note" }])
	check_eq(state.clues.size(), 1, "the same clue is recorded once")
	check_eq(state.journal.size(), 1, "the same note is recorded once")
	check(state.has_flag("met_doctor"), "flag set")
	check(not state.has_flag("anomaly_seen"), "unset flag reads false")

func test_unknown_clues_are_rejected_rather_than_silently_counted() -> void:
	var state := _state()
	check_eq(state.add_clue("no-such-clue"), false, "unknown clue rejected")
	check_eq(state.clues.size(), 0, "nothing recorded")

func test_a_dialogue_runs_to_an_end_and_applies_its_effects() -> void:
	var state := _state()
	check(state.start_dialogue("doctor"), "the doctor's graph starts")
	check(state.in_dialogue(), "in dialogue")
	check(state.choose(0), "first choice taken")
	while state.in_dialogue():
		if not state.choose(0):
			break
	check(not state.in_dialogue(), "the dialogue ends")
	check(state.has_flag("met_doctor"), "the conversation set its flag")

func test_endings_stay_locked_until_the_record_is_found() -> void:
	var state := _state()
	check_eq(state.available_endings(), [] as Array[String], "no ending without the record")
	state.add_clue("record-1601")
	check(state.available_endings().has("closed_by_evidence"), "evidence ending unlocks")
	check(not state.available_endings().has("referred_anomalous"), "anomalous ending needs its flag")
	state.set_flag("anomaly_seen")
	check(state.available_endings().has("referred_anomalous"), "anomalous ending unlocks with the flag")
	check(state.choose_ending("referred_anomalous"), "ending chosen")
	check(state.finished, "the case is finished")

func test_save_round_trip_preserves_everything_the_case_needs() -> void:
	var state := _state()
	state.add_clue("record-1601")
	state.add_clue("patient-testimony")
	state.set_flag("anomaly_seen")
	state.add_journal("a note")
	state.add_complication("records-inconsistent")
	var path := "user://test_lakkahaltia_save.json"
	check(state.save_to(path), "save written")

	var loaded := _state()
	check(loaded.load_from(path), "save read")
	check_eq(loaded.clues, state.clues, "clues survive")
	check(loaded.has_flag("anomaly_seen"), "flags survive")
	check_eq(loaded.journal, state.journal, "journal survives")
	check_eq(loaded.complications, state.complications, "complications survive")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func test_a_save_from_another_version_is_refused() -> void:
	var state := _state()
	var payload := state.to_dict()
	payload["save_version"] = 999
	check_eq(state.from_dict(payload), false, "future save versions are refused")
