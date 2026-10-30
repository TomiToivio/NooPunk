extends RefCounted
const V := preload("res://godot/core/cwn_vehicles.gd")

func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]

func run() -> Array:
	var rows: Array = []
	rows.append(_eq("vehicle catalogue is present", V.entry("vehicles", "nonexistent").is_empty(), true))
	rows.append(_eq("larger hull accepts smaller fitting", V.size_allows("L", "S"), true))
	rows.append(_eq("small hull rejects larger fitting", V.size_allows("S", "M"), false))
	rows.append(_eq("stationary vehicle AC -4", V.armor_class(13, false, 3), 9))
	rows.append(_eq("moving vehicle AC plus Drive", V.armor_class(13, true, 2), 15))
	rows.append(_eq("immune hull is referee ruling", V.can_be_harmed({"armor_note": "immune"}), null))
	rows.append(_eq("heavy_only hull denies light attacks", V.can_be_harmed({"armor_note": "heavy_only"}), false))
	rows.append(_eq("vehicle armor AFTER Trauma", V.damage_to_vehicle(5, 3, 8).get("damage"), 7))
	rows.append(_eq("vehicle damage cannot be negative", V.damage_to_vehicle(-1).get("ok"), false))
	rows.append(_eq("zero HP destroys vehicle", V.is_destroyed(0), true))
	rows.append(_eq("destruction luck halves damage", V.destruction_damage(9, true), 4))
	rows.append(_eq("two crash saves unscathed", V.crash_outcome(true, true).get("unscathed"), true))
	rows.append(_eq("no crash saves mortal", V.crash_outcome(false, false).get("mortally_wounded"), true))
	rows.append(_eq("ram person evasion negates harm", V.ram_person(12, 9, true, 20).get("damage"), 0))
	rows.append(_eq("ram vehicle damages both hulls", V.ram_vehicle(12, 9, 20).get("rammer_damage"), 20))
	rows.append(_eq("chase ties escape", V.chase(12, [12]).get("escaped"), true))
	rows.append(_eq("one faster pursuer catches", V.chase(12, [11, 13]).get("caught_by"), [false, true]))
	rows.append(_eq("no pursuers is invalid", V.chase(12, []).get("ok"), false))
	rows.append(_eq("repairs consume 200 per HP", V.repair_estimate(7, 1, 0).get("cost"), 1400))
	rows.append(_eq("repair takes ceil daily rate", V.repair_estimate(7, 1, 0).get("days"), 4))
	rows.append(_eq("destroyed hull totaled", V.repair_estimate(7, 1, 0, false, 0).get("totaled"), true))
	return rows
