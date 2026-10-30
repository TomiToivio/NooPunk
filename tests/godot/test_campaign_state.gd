extends "res://tests/godot/godot_test.gd"

## Gate 1 of #749 (#750): campaign state, Home -> HQ -> mission transitions and saves.
## The campaign state is deliberately separate from the Lakkahaltia CaseState and is no autoload.


func _fresh() -> NooPunkCampaignState:
	return NooPunkCampaignState.new()


func test_a_new_campaign_starts_at_home() -> void:
	var state := _fresh()
	check_eq(state.current_location, "home", "a new campaign starts at Romppainen's home")
	check_eq(state.journal.size(), 0, "a new campaign starts with an empty journal")
	check_eq(state.flags.size(), 0, "a new campaign starts with no flags")
	check_eq(state.inventory.size(), 0, "no inventory or build choice is invented for the player")


func test_travel_follows_the_location_graph() -> void:
	var state := _fresh()
	check(state.travel("hq"), "home -> hq is adjacent")
	check_eq(state.current_location, "hq", "travel moves the campaign")
	check(not state.travel("mission"), "hq -> mission stays locked until the mission is accepted")
	check_eq(state.current_location, "hq", "a refused move does not move the campaign")
	check(not state.travel("nowhere"), "an unknown destination is refused")
	check(state.travel("home"), "hq -> home is a legal return")
	check_eq(state.current_location, "home", "the return is recorded")


func test_accepting_the_mission_unlocks_it_and_return_works() -> void:
	var state := _fresh()
	check(state.record_once("mission_accepted", "Took the case."), "the mission flag is set once")
	check(state.travel("hq"), "home -> hq")
	check(state.travel("mission"), "the accepted mission is reachable from hq")
	check(not state.travel("hq"), "mission -> hq is refused: the debrief is the way back")
	check(not state.travel("debrief"), "and the debrief is closed until the mission is resolved")
	check(state.resolve_mission("success", "investigative"), "the mission resolves at its location")
	check(state.travel("debrief"), "mission -> debrief")
	check(state.travel("hq"), "debrief -> hq returns the campaign")
	check_eq(state.current_location, "hq", "the debrief returns the campaign to hq")


func test_record_once_is_idempotent() -> void:
	var state := _fresh()
	check(state.record_once("met_patron", "Met the patron."), "the first interaction applies")
	check(not state.record_once("met_patron", "Met the patron."), "a repeated interaction does not re-apply")
	check(not state.record_once("met_patron", "A different line."), "a repeated flag is still refused")
	check_eq(state.journal.size(), 1, "the journal keeps one line for one flag")
	check_eq(state.journal[0], "Met the patron.", "the journal keeps the first line, not the repeat")
	check(not state.record_once("", ""), "an empty flag is refused")


func test_save_and_load_restore_the_campaign() -> void:
	var path := "user://test_campaign_state_round_trip.json"
	var state := _fresh()
	state.record_once("mission_accepted", "Took the case.")
	state.travel("hq")
	state.travel("mission")
	state.character = {"name": "Romppainen"}
	state.inventory = ["flashlight"]
	state.dialogue_choices = {"patron": "accept"}
	check(state.save(path), "the campaign saves")

	var loaded := _fresh()
	check(loaded.load_save(path), "the campaign loads")
	check_eq(loaded.current_location, "mission", "the location round-trips")
	check_eq(loaded.flags.get("mission_accepted"), true, "flags round-trip")
	check_eq(loaded.character, {"name": "Romppainen"}, "the player's build choice round-trips")
	check_eq(loaded.inventory, ["flashlight"], "inventory round-trips")
	check_eq(loaded.dialogue_choices, {"patron": "accept"}, "dialogue choices round-trip")
	check_eq(loaded.journal, ["Took the case."], "the journal round-trips")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func test_incompatible_and_malformed_saves_are_rejected() -> void:
	var state := _fresh()
	state.record_once("mission_accepted", "Took the case.")
	var future: Dictionary = state.to_data()
	future["version"] = 999
	check(not state.from_data(future), "a future save version is rejected")
	check_eq(state.current_location, "home", "a rejected save leaves the campaign untouched")
	check(not state.from_data({"version": 1, "current_location": "atlantis"}), "an unknown location is rejected")
	check(not state.from_data({"version": 1, "current_location": "home"}), "a save without the typed containers is rejected")
	check(not state.load_save("user://no_such_campaign_file.json"), "a missing save is refused rather than faked")


func test_the_legacy_lakkahaltia_case_still_loads() -> void:
	var state := NooPunkCaseState.new(
		"res://data/scenarios/lakkahaltia/case.json",
		"res://data/scenarios/lakkahaltia/dialogue.json"
	)
	check_eq(state.case_data.get("id"), "lakkahaltia", "the legacy case still loads unchanged")
	check_eq(state.stat("INT"), 14, "the legacy character sheet is untouched")
