extends "res://tests/godot/godot_test.gd"

## Executable campaign navigation/persistence regression checks for #750.

func test_campaign_starts_home_and_mission_is_locked() -> void:
	var campaign := NooPunkCampaignState.new()
	check_eq(campaign.current_location, "home", "campaign starts at home")
	check(not campaign.travel("mission"), "cannot skip HQ")
	check(campaign.travel("hq"), "travel to HQ")
	check(not campaign.travel("mission"), "briefing required")
	check(campaign.record_once("mission_accepted", "Assignment accepted."), "accept once")
	check(not campaign.record_once("mission_accepted", "Assignment accepted."), "accept only once")
	check_eq(campaign.journal.size(), 1, "journal not duplicated")
	check(campaign.travel("mission"), "mission unlocked")
	check(not campaign.travel("hq"), "the mission does not return straight to HQ")
	check(campaign.travel("debrief"), "the mission goes to the debrief")
	check(campaign.travel("hq"), "the debrief returns to HQ")
	check(campaign.record_once("debrief_complete", "Debrief"), "complete once")
	check(not campaign.record_once("debrief_complete", "Debrief"), "debrief idempotent")

func test_campaign_save_roundtrip_preserves_modes_and_choices() -> void:
	var campaign := NooPunkCampaignState.new()
	campaign.travel("hq")
	campaign.record_once("mission_accepted", "Assignment accepted.")
	campaign.travel("mission")
	campaign.dialogue_choices["briefing"] = "accept"
	campaign.encounter["status"] = "unresolved"
	campaign.network["current_node"] = "entry"
	campaign.inventory.append({"item_id": "test-fixture"})
	var path := "user://test_campaign_750.json"
	check(campaign.save(path), "save")
	var loaded := NooPunkCampaignState.new()
	check(loaded.load_save(path), "load")
	check_eq(loaded.to_data(), campaign.to_data(), "round-trip preserves all states")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func test_campaign_rejects_invalid_saves_without_changing_state() -> void:
	var campaign := NooPunkCampaignState.new()
	var snapshot := campaign.to_data()
	var invalid := snapshot.duplicate(true)
	invalid["version"] = 99
	check(not campaign.from_data(invalid), "reject wrong version")
	invalid = snapshot.duplicate(true)
	invalid["current_location"] = "mission"
	check(not campaign.from_data(invalid), "reject mission without acceptance")
	invalid = snapshot.duplicate(true)
	invalid["flags"] = {"mission_accepted": "yes"}
	check(not campaign.from_data(invalid), "reject non-boolean flag")
	check_eq(campaign.to_data(), snapshot, "invalid loads never mutate live state")
