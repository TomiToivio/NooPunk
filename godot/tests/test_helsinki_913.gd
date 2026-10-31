## Issue #913: hidden-at-start Helsinki nodes, travel, flags and save-state round trip.
extends RefCounted
const Map := preload("res://godot/narrative/location_map.gd")

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]

func _ids(nodes: Array) -> Array:
	var output: Array = []
	for node in nodes:
		output.append(String(node.get("id", "")))
	return output

func run() -> Array:
	var rows: Array = []
	var map := Map.from_data(Map.load_data())
	var start: Array = _ids(map.visible({}))
	rows.append(_eq("exactly two starting nodes", start.size(), 2))
	rows.append(_eq("home starts current", map.current, "home_helsinginkatu"))
	rows.append(_eq("starting home is visible", start.has("home_helsinginkatu"), true))
	rows.append(_eq("Ratakatu HQ is visible", start.has("unsa_hq_ratakatu"), true))
	for secret in ["olutravintola_putki", "university_of_helsinki", "kurvi", "unsa_underground"]:
		rows.append(_eq("%s absent from opening map" % secret, start.has(secret), false))
		rows.append(_eq("%s cannot be travelled to" % secret, map.travel_to(secret, {}).get("ok"), false))
	rows.append(_eq("travel to HQ works", map.travel_to("unsa_hq_ratakatu", {}).get("ok"), true))
	var flags := {"knows_putki": true}
	rows.append(_eq("Putki discovered when told", map.refresh(flags).has("olutravintola_putki"), true))
	rows.append(_eq("University remains hidden", _ids(map.visible(flags)).has("university_of_helsinki"), false))
	rows.append(_eq("Kurvi remains hidden", _ids(map.visible(flags)).has("kurvi"), false))
	rows.append(_eq("underground remains hidden", _ids(map.visible(flags)).has("unsa_underground"), false))
	rows.append(_eq("Putki travel now works", map.travel_to("olutravintola_putki", flags).get("ok"), true))
	var saved: Dictionary = map.to_dict()
	var restored := Map.from_data(Map.load_data())
	rows.append(_eq("map save restores", restored.from_dict(saved), true))
	rows.append(_eq("current location saved", restored.current, "olutravintola_putki"))
	rows.append(_eq("discovered bar persists", _ids(restored.visible({})).has("olutravintola_putki"), true))
	rows.append(_eq("hidden university stays hidden after restore", _ids(restored.visible({})).has("university_of_helsinki"), false))
	flags["knows_university"] = true
	flags["knows_kurvi"] = true
	rows.append(_eq("university and Kurvi unlock individually", restored.refresh(flags).size(), 2))
	rows.append(_eq("bunker still secret", _ids(restored.visible(flags)).has("unsa_underground"), false))
	flags["underground_clearance"] = true
	rows.append(_eq("clearance reveals bunker", restored.refresh(flags).has("unsa_underground"), true))
	return rows
