extends RefCounted

## Preloaded rather than referenced by global class name: the global class cache only exists after an
## import pass, so a headless run on a clean checkout cannot resolve `NooPunkCampaignState` and the
## whole suite fails to load (the other suites here preload for the same reason).
const NooPunkCampaignState := preload("res://src/godot/campaign_state.gd")

func run() -> Array:
	var rows: Array = []
	var state := NooPunkCampaignState.new()
	rows.append(["new game starts at home", state.current_location == "home", ""])
	rows.append(["mission locked until acceptance", not state.travel("mission"), ""])
	var first := state.record_once("home_note", "Find HQ")
	var repeat := state.record_once("home_note", "Find HQ")
	rows.append(["idempotent journal entry", first and not repeat and state.journal.size() == 1, ""])
	var at_hq := state.travel("hq")
	var locked := not state.travel("mission")
	state.record_once("mission_accepted", "Mission assigned")
	var at_mission := state.travel("mission")
	state.record_once("mission_visited", "Investigation")
	var returned := state.travel("hq")
	state.record_once("debrief_complete", "Debrief")
	rows.append(["travel unlock and return", at_hq and locked and at_mission and returned, ""])
	var copy := NooPunkCampaignState.new()
	var roundtrip := copy.from_data(state.to_data())
	rows.append(["state serialization", roundtrip and copy.to_data() == state.to_data(), ""])
	var bad := state.to_data()
	bad["version"] = 999
	rows.append(["incompatible versions rejected", not copy.from_data(bad) and copy.current_location == "hq", ""])
	var path := "user://campaign_gate1_test.json"
	var saved := state.save(path)
	var reloaded := NooPunkCampaignState.new()
	var loaded := saved and reloaded.load_save(path)
	rows.append(["save/load roundtrip", loaded and reloaded.to_data() == state.to_data(), ""])
	if saved:
		DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	return rows
