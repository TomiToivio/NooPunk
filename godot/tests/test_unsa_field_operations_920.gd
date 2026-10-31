extends RefCounted
const Operations := preload("res://godot/narrative/unsa_field_operations.gd")
func _eq(name: String, actual: Variant, wanted: Variant) -> Array:
	return [name, actual == wanted, "got %s wanted %s" % [actual, wanted]]

func run() -> Array:
	var rows: Array = []
	var ops := Operations.new()
	rows.append(_eq("rookie created", ops.start_agent("tony", "Tony German"), true))
	rows.append(_eq("solo by default", ops.party.members.size(), 1))
	var laura := {"id": "laura", "level": 1, "name": "Laura Wendt"}
	rows.append(_eq("recruitment is availability gated", ops.recruit(laura)["ok"], false))
	ops.set_available("laura", true)
	rows.append(_eq("Laura joins when available", ops.recruit(laura)["ok"], true))
	ops.set_available("hacker", true)
	ops.set_available("romppainen", true)
	ops.set_available("psyker", true)
	rows.append(_eq("specialist joins", ops.recruit({"id": "hacker", "level": 2})["ok"], true))
	rows.append(_eq("Romppainen joins", ops.recruit({"id": "romppainen", "level": 5})["ok"], true))
	rows.append(_eq("fifth member refused", ops.recruit({"id": "psyker", "level": 3})["ok"], false))
	rows.append(_eq("remote controller never uses a party slot", ops.party.members.size(), 4))
	rows.append(_eq("cannot dismiss PC", ops.release("tony"), false))
	rows.append(_eq("companion may leave", ops.release("romppainen"), true))
	rows.append(_eq("AI action requires human approval", ops.can_execute("access_patient_records"), false))
	rows.append(_eq("no active PSI for ordinary agent", ops.scripted_psi({"id": "tony"}, "clinic", "psi_clinic")["ok"], false))
	rows.append(_eq("approved human action logged", ops.authorize("UNSA", "human_controller", "psi_clinic", true), true))
	rows.append(_eq("scripted PSI performed by designated asset", ops.scripted_psi({"id": "psyker", "designated_psi_asset": true}, "clinic", "psi_clinic")["ok"], true))
	rows.append(_eq("disputed authority blocks action", ops.authorize("Europol", "duty_officer", "psi_clinic", false), true))
	rows.append(_eq("denial prevents further use", ops.can_execute("psi_clinic"), false))
	ops.alter_trust("laura", 20)
	rows.append(_eq("trust is bounded", ops.trust["laura"], 10))
	var saved: Dictionary = ops.to_dict()
	var restored := Operations.new()
	rows.append(_eq("save restored", restored.from_dict(saved), true))
	rows.append(_eq("save roundtrip", restored.to_dict(), saved))
	rows.append(_eq("bad save refused", restored.from_dict({"version": 1}), false))
	rows.append(_eq("rejected save doesn't corrupt state", restored.to_dict(), saved))
	return rows
