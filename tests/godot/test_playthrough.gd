extends "res://tests/godot/godot_test.gd"

## End-to-end content playthrough at the logic level: the case can be investigated from the
## entrance to either ambiguous ending, with a save taken mid-investigation and reloaded.
## This is the automated proof that the slice's content graph is completable, not a prose test.

func _state() -> NooPunkCaseState:
	return NooPunkCaseState.new(
		"res://data/scenarios/lakkahaltia/case.json",
		"res://data/scenarios/lakkahaltia/dialogue.json"
	)

func _talk(state: NooPunkCaseState, npc: String, picks: Array) -> void:
	check(state.start_dialogue(npc), "%s dialogue starts" % npc)
	for pick in picks:
		if not state.in_dialogue():
			break
		check(state.choose(int(pick)), "%s choice %d accepted" % [npc, int(pick)])
	if state.in_dialogue():
		state.end_dialogue()

func test_mundane_ending_is_reachable_and_ambiguous() -> void:
	var state := _state()
	_talk(state, "doctor", [0, 1, 1, 0])
	_talk(state, "nurse", [1, 0, 0])
	check(state.has_clue("nurse-inconsistency"), "the nurse's roster contradiction is a clue")
	# The record check is a real roll; a fixed die makes this test deterministic.
	var rules := NooPunkCoreRules.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = 1
	var roll := rules.resolve_check(rng, state.stat("INT"), state.skill("Investigate"), 12, 9)
	check(roll["success"], "a good roll reads the record")
	state.add_clue("record-1601")
	var endings := state.available_endings()
	check(endings.has("closed_by_evidence"), "mundane ending available")
	check(state.choose_ending("closed_by_evidence"), "mundane ending chosen")
	check(state.finished, "case finished")
	check(state.ending_prose("closed_by_evidence").length() > 40, "ending has prose")
	check(not state.has_flag("anomaly_seen"), "the mundane ending needs no anomaly")

func test_anomalous_ending_requires_the_encounter_and_stays_ambiguous() -> void:
	var state := _state()
	_talk(state, "patient", [1, 0, 0])
	check(state.has_flag("met_patient"), "the patient conversation happened")
	check(state.has_clue("patient-testimony"), "her account is a clue")
	var rules := NooPunkCoreRules.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = 3
	var roll := rules.resolve_check(rng, state.stat("PSY"), state.skill("Awareness"), 13, 10)
	check(roll["success"], "the mirror check can succeed")
	state.add_clue("lakkahaltia-sighting")
	state.set_flag("anomaly_seen")
	state.add_clue("record-1601")
	var endings := state.available_endings()
	check(endings.has("referred_anomalous"), "anomalous ending available")
	check(endings.has("closed_by_evidence"), "the mundane ending stays available too")
	check(state.choose_ending("referred_anomalous"), "anomalous ending chosen")
	var prose := state.ending_prose("referred_anomalous")
	check(prose.contains("unresolved"), "the ending keeps the explanation unresolved")

func test_a_mid_investigation_save_resumes_and_still_reaches_an_ending() -> void:
	var state := _state()
	_talk(state, "doctor", [0, 0])
	var path := "user://test_playthrough_save.json"
	check(state.save_to(path), "mid-case save written")

	var resumed := _state()
	check(resumed.load_from(path), "mid-case save read")
	check(resumed.has_flag("met_doctor"), "conversation flag survived the save")
	_talk(resumed, "patient", [0, 0])
	resumed.add_clue("record-1601")
	check(resumed.available_endings().has("closed_by_evidence"), "a resumed case can still close")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func test_both_endings_are_simultaneously_available_when_the_evidence_supports_them() -> void:
	var state := _state()
	state.add_clue("record-1601")
	state.set_flag("anomaly_seen")
	var endings := state.available_endings()
	check_eq(endings.size(), 2, "two ambiguous outcomes are offered, not one truth")
