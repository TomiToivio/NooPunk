extends RefCounted

## Preloaded rather than referenced by global class name: the global class cache only exists after an
## import pass, so a headless run on a clean checkout cannot resolve `NooPunkCampaignState` and the
## whole suite fails to load (the other suites here preload for the same reason).
const NooPunkCampaignState := preload("res://src/godot/campaign_state.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []
	var state := NooPunkCampaignState.new()
	rows.append(_eq("new game starts at home", state.current_location, "home"))
	rows.append(_eq("mission locked until acceptance", state.travel("mission"), false))
	rows.append(_eq("debrief unreachable before a mission", state.travel("debrief"), false))

	var first := state.record_once("home_note", "Find HQ")
	var repeat := state.record_once("home_note", "Find HQ")
	rows.append(["idempotent journal entry", first and not repeat and state.journal.size() == 1, ""])

	var at_hq := state.travel("hq")
	var locked := not state.travel("mission")
	var accepted := state.accept_mission("warehouse", "Recover the manifest")
	var at_mission := state.travel("mission")
	rows.append(["briefing unlocks the mission", at_hq and locked and accepted and at_mission, ""])

	# The debrief is gated on resolution, not on merely having visited the mission.
	rows.append(_eq("debrief locked until resolved", state.travel("debrief"), false))
	rows.append(_eq("resolution needs a legal outcome", state.resolve_mission("triumph", "mixed"), false))
	rows.append(_eq("resolution needs a legal approach", state.resolve_mission("success", "diplomacy"), false))
	var resolved := state.resolve_mission("success", "investigative")
	var again := state.resolve_mission("failure", "tactical")
	rows.append(["mission resolves once", resolved and not again and state.outcome == "success", ""])
	rows.append(_eq("approach recorded", state.approach, "investigative"))
	rows.append(_eq("objective marked resolved", state.objective["resolved"], true))

	var to_debrief := state.travel("debrief")
	var back_to_hq := state.travel("hq")
	rows.append(["mission to debrief to hq", to_debrief and back_to_hq and state.current_location == "hq", ""])

	# An undecided build slot must survive a save without being filled in by the application.
	state.character = {"name": "Romppainen", "choices": {"background": "choice", "edge": "choice", "focus": "choice"}}
	rows.append(_eq("build choices stay undecided", state.undecided_choices(), ["background", "edge", "focus"]))

	var copy := NooPunkCampaignState.new()
	var roundtrip := copy.from_data(state.to_data())
	rows.append(["state serialization", roundtrip and copy.to_data() == state.to_data(), ""])
	rows.append(_eq("undecided choices survive save", copy.undecided_choices().size(), 3))

	var bad := state.to_data()
	bad["version"] = 999
	rows.append(["incompatible versions rejected", not copy.from_data(bad) and copy.current_location == "hq", ""])

	var bad_outcome := state.to_data()
	bad_outcome["outcome"] = "triumph"
	rows.append(_eq("unknown outcome rejected on load", copy.from_data(bad_outcome), false))

	var skip := state.to_data()
	skip["current_location"] = "debrief"
	skip["outcome"] = ""
	rows.append(_eq("debrief save without an outcome rejected", copy.from_data(skip), false))

	var path := "user://campaign_gate1_test.json"
	var saved := state.save(path)
	var reloaded := NooPunkCampaignState.new()
	var loaded := saved and reloaded.load_save(path)
	rows.append(["save/load roundtrip", loaded and reloaded.to_data() == state.to_data(), ""])
	if saved:
		DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	return rows
