extends RefCounted

## #809: the campaign save migrates, and a v2 save must still load.
##
## The migration question is not "does version 3 work" but "does the save a player already has still
## open". A v2 campaign had exactly one protagonist and no companions, so an empty roster is the
## faithful migration; inventing a companion would put a character in the party who never existed.
const CampaignState := preload("res://src/godot/campaign_state.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	rows.append(_eq("current version is three", CampaignState.VERSION, 3))
	rows.append(_eq("version two is still supported", CampaignState.SUPPORTED_VERSIONS.has(2), true))

	var state := CampaignState.new()
	rows.append(_eq("a new campaign has no party yet", state.party, {}))

	# Build a v3 save with a party and round-trip it.
	state.character = {"name": "Agent Virtanen", "choices": {"background": "choice"}}
	state.party = {"version": 1, "members": [
		{"id": "pc", "name": "Agent Virtanen", "level": 1, "is_pc": true, "inventory": []},
		{"id": "romppainen", "name": "Dr. Inspector Harri Romppainen", "level": 6, "is_pc": false,
			"controllable": true, "inventory": []},
	], "controlled_id": "pc"}
	var saved: Dictionary = state.to_data()
	rows.append(_eq("the save carries version three", int(saved["version"]), 3))
	rows.append(_eq("the save carries the party", typeof(saved["party"]), TYPE_DICTIONARY))

	var copy := CampaignState.new()
	rows.append(_eq("a v3 save loads", copy.from_data(saved), true))
	rows.append(_eq("the party survives", copy.party.get("members", []).size(), 2))

	# A v2 save: same payload with version 2 and no party key.
	var legacy: Dictionary = state.to_data()
	legacy["version"] = 2
	legacy.erase("party")
	var migrated := CampaignState.new()
	rows.append(_eq("a v2 save still loads", migrated.from_data(legacy), true))
	rows.append(_eq("the migration adds an empty party, not a guess", migrated.party, {}))
	rows.append(_eq("the character is preserved", str(migrated.character.get("name", "")), "Agent Virtanen"))

	# A future version must be refused rather than half-read.
	var future: Dictionary = state.to_data()
	future["version"] = 4
	rows.append(_eq("a future version is refused", CampaignState.new().from_data(future), false))

	# A v3 save whose party is malformed is still a v3 save: it must be refused by the party loader,
	# not silently accepted here as an empty roster.
	var broken: Dictionary = state.to_data()
	broken["party"] = "not a dictionary"
	rows.append(_eq("a malformed party is refused at the state boundary",
		CampaignState.new().from_data(broken), false))

	# The save path must not change, or every existing player save is orphaned.
	rows.append(_eq("the save path keeps its v2 filename",
		CampaignState.SAVE_PATH, "user://noopunk_campaign_v2.json"))

	return rows
