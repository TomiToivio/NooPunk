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

	# Map placement: the illustrated map (#908) needs coordinates, and a list of nodes is not a map.
	var placed := Map.from_data(Map.load_data())
	var seen: Array = []
	var all_inside := true
	for node_id in placed.nodes:
		var point: Array = placed.nodes[node_id].get("position", [])
		if point.size() != 2:
			all_inside = false
			continue
		if float(point[0]) < 0.0 or float(point[0]) > 1.0 or float(point[1]) < 0.0 or float(point[1]) > 1.0:
			all_inside = false
		seen.append("%.3f,%.3f" % [float(point[0]), float(point[1])])
	rows.append(_eq("every location has a map position", all_inside, true))
	rows.append(_eq("no two locations share a point", seen.size(), _unique(seen).size()))
	var home: Array = placed.nodes["home_helsinginkatu"]["position"]
	var hq: Array = placed.nodes["unsa_hq_ratakatu"]["position"]
	rows.append(_eq("home is north of HQ", float(home[1]) < float(hq[1]), true))
	rows.append(_eq("home is east of HQ", float(home[0]) > float(hq[0]), true))
	var bunker: Array = placed.nodes["unsa_underground"]["position"]
	rows.append(_eq("the bunker sits below HQ, not across the city",
		absf(float(bunker[0]) - float(hq[0])) < 0.05 and float(bunker[1]) > float(hq[1]), true))
	return rows


func _unique(values: Array) -> Array:
	var out: Array = []
	for value in values:
		if not out.has(value):
			out.append(value)
	return out
