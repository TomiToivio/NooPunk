## Party and authority rules (#920): 1-4 slots, situational recruitment, human approval, scripted PSI.
extends RefCounted

const Roster := preload("res://godot/narrative/party_roster.gd")


func _ok(name: String, condition: bool, detail := "") -> Array:
	return [name, condition, detail]


func run() -> Array:
	var rows: Array = []
	var r := Roster.new()

	rows.append(_ok("starts with Tony alone", r.size() == 1 and r.is_active("tony_german")))
	rows.append(_ok("Tony has no active PSI", not r.pc_has_active_psi()))
	rows.append(_ok("cap is four including Tony", r.cap() == 4))

	rows.append(_ok("Laura needs the partner mission tag",
		not bool(r.recruit("laura_wendt", {"mission_tags": [], "trust": 3}).get("ok", true))))
	rows.append(_ok("Laura needs trust", not bool(r.recruit("laura_wendt",
		{"mission_tags": ["partner"], "trust": 0}).get("ok", true))))
	rows.append(_ok("Laura joins with tag and trust", bool(r.recruit("laura_wendt",
		{"mission_tags": ["partner"], "trust": 2}).get("ok", false))))

	rows.append(_ok("Romppainen needs NHI and inspector authority",
		not bool(r.recruit("harri_romppainen", {"mission_tags": ["nhi"]}).get("ok", true))))
	rows.append(_ok("Romppainen joins when authorised", bool(r.recruit("harri_romppainen",
		{"mission_tags": ["nhi"], "authorization": "unsa_inspector"}).get("ok", false))))
	rows.append(_ok("a cyber specialist joins a cyber mission", bool(r.recruit("cyber_specialist",
		{"mission_tags": ["cyber"], "authorization": "unsa_field_office"}).get("ok", false))))
	rows.append(_ok("party is four", r.size() == 4))

	rows.append(_ok("a fifth member is refused", not bool(r.recruit("psi_asset",
		{"mission_tags": ["psi"], "authorization": "unsa_psi_office"}).get("ok", true))))
	r.dismiss("cyber_specialist")
	rows.append(_ok("a slot can be freed", r.size() == 3))
	rows.append(_ok("psionic asset joins when authorised", bool(r.recruit("psi_asset",
		{"mission_tags": ["psi"], "authorization": "unsa_psi_office"}).get("ok", false))))

	rows.append(_ok("AI action without approval is refused",
		not bool(r.execute_ai_action("run_plate_search").get("ok", true))))
	rows.append(_ok("approval needs a named human",
		not bool(r.approve("", "unsa", "run_plate_search").get("ok", true))))
	rows.append(_ok("a named human approval is recorded",
		bool(r.approve("Inspector Romppainen", "unsa", "run_plate_search").get("ok", false))))
	rows.append(_ok("approved AI action executes",
		bool(r.execute_ai_action("run_plate_search").get("ok", false))))

	rows.append(_ok("Tony cannot use active PSI",
		not bool(r.use_active_psi("tony_german", "warehouse_signal").get("ok", true))))
	rows.append(_ok("PSI needs psi-office authority on record",
		not bool(r.use_active_psi("psi_asset", "warehouse_signal").get("ok", true))))
	r.approve("UNSA psi office", "unsa_psi_office", "psychic_support")
	rows.append(_ok("PSI needs a scripted scene",
		not bool(r.use_active_psi("psi_asset", "market_chat").get("ok", true))))
	rows.append(_ok("designated asset uses scripted PSI", bool(r.use_active_psi("psi_asset",
		"warehouse_signal").get("ok", false))))

	var state := r.to_dict()
	var loaded := Roster.new()
	rows.append(_ok("party saves and loads", loaded.from_dict(state)))
	rows.append(_ok("loaded party keeps four members", loaded.size() == 4))
	rows.append(_ok("a fifth member is invalid on load", not loaded.from_dict(
		{"active": ["tony_german", "laura_wendt", "harri_romppainen", "cyber_specialist", "psi_asset"]})))
	return rows
