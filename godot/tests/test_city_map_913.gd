## The Helsinki city map: two places at the start, everything else earned (#913).
extends RefCounted

const CityMap := preload("res://godot/narrative/location_map.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _ids(nodes: Array) -> Array:
	var out: Array = []
	for node in nodes:
		out.append(String(node.get("id", "")))
	out.sort()
	return out


func run() -> Array:
	var rows: Array = []
	var map := CityMap.helsinki()

	# ---- exactly two places exist at the start ------------------------------
	rows.append(_eq("the shipped map loads", map.nodes.size(), 6))
	rows.append(_eq("the player starts at home", map.current, "home_helsinginkatu"))
	var opening: Array = _ids(map.visible({}))
	rows.append(_eq("exactly two places are visible on a fresh save", opening,
		["home_helsinginkatu", "unsa_hq_ratakatu"]))
	rows.append(_eq("the bar is not on the opening map", map.is_visible("olutravintola_putki", {}), false))
	rows.append(_eq("the university is not on the opening map",
		map.is_visible("university_of_helsinki", {}), false))
	rows.append(_eq("kurvi is not on the opening map", map.is_visible("kurvi", {}), false))

	# hidden means absent, not disabled
	rows.append(_eq("a hidden place reports hidden, not locked",
		map.status("olutravintola_putki", {}), "hidden"))
	rows.append(_eq("nothing leaks the name as a locked marker",
		_ids(map.visible({"putki_recommended": false})).has("olutravintola_putki"), false))

	# ---- discovery ----------------------------------------------------------
	var newly: Array = map.refresh({"putki_recommended": true})
	rows.append(_eq("learning about the bar puts it on the map", newly, ["olutravintola_putki"]))
	rows.append(_eq("and it is now visible", map.is_visible("olutravintola_putki", {"putki_recommended": true}), true))
	rows.append(_eq("discovery does not reveal anything else",
		_ids(map.visible({"putki_recommended": true})).has("university_of_helsinki"), false))

	var university: Array = map.refresh({"university_lead": true})
	rows.append(_eq("the university unlocks on its own lead", university, ["university_of_helsinki"]))
	var kurvi: Array = map.refresh({"kurvi_mentioned": true})
	rows.append(_eq("kurvi unlocks when someone mentions it", kurvi, ["kurvi"]))

	# refresh is idempotent
	rows.append(_eq("re-learning a place reports nothing new",
		map.refresh({"putki_recommended": true}), []))

	# ---- the underground is concealed, never teased -------------------------
	rows.append(_eq("the underground is concealed at the start",
		map.status("unsa_underground", {}), "concealed"))
	rows.append(_eq("it stays concealed even once every surface place is known",
		map.underground_concealed({"putki_recommended": true, "university_lead": true,
			"kurvi_mentioned": true}), true))
	rows.append(_eq("it is not in the visible list",
		_ids(map.visible({"putki_recommended": true, "university_lead": true,
			"kurvi_mentioned": true})).has("unsa_underground"), false))
	var refused: Dictionary = map.travel_to("unsa_underground", {})
	rows.append(_eq("travelling there is refused", refused["ok"], false))
	rows.append(_eq("and says clearance is required", refused["reason"], "clearance_required"))
	rows.append(_eq("with the clearance flag it becomes visible",
		map.status("unsa_underground", {"underground_clearance": true}), "known"))
	rows.append(_eq("and only then is it no longer concealed",
		map.underground_concealed({"underground_clearance": true}), false))

	# ---- travel -------------------------------------------------------------
	var opening_map := CityMap.helsinki()
	var blocked: Dictionary = opening_map.travel_to("olutravintola_putki", {})
	rows.append(_eq("travel to an undiscovered place is refused", blocked["ok"], false))
	rows.append(_eq("and says not discovered", blocked["reason"], "not_discovered"))

	var move: Dictionary = opening_map.travel_to("unsa_hq_ratakatu", {})
	rows.append(_eq("travel between the two starting places works", move["ok"], true))
	rows.append(_eq("the current location moves", opening_map.current, "unsa_hq_ratakatu"))
	rows.append(_eq("visiting is recorded", opening_map.has_visited("unsa_hq_ratakatu"), true))
	rows.append(_eq("HQ offers its own actions", Array(move["actions"]).has("reception"), true))
	rows.append(_eq("home offers its own actions",
		opening_map.actions_at("home_helsinginkatu", {}).has("inspect_boxes"), true))
	rows.append(_eq("a hidden place offers no actions",
		opening_map.actions_at("kurvi", {}), []))
	rows.append(_eq("an invented id is refused", opening_map.travel_to("atlantis", {})["reason"],
		"unknown_location"))

	# ---- save / load --------------------------------------------------------
	var saving := CityMap.helsinki()
	saving.refresh({"putki_recommended": true, "kurvi_mentioned": true})
	saving.travel_to("olutravintola_putki", {"putki_recommended": true, "kurvi_mentioned": true})
	var state: Dictionary = saving.to_dict()
	var loaded := CityMap.from_dict(state)
	rows.append(_eq("the current place survives a save", loaded.current, "olutravintola_putki"))
	rows.append(_eq("discoveries survive a save",
		loaded.is_visible("olutravintola_putki", {"putki_recommended": true, "kurvi_mentioned": true}), true))
	rows.append(_eq("visits survive a save", loaded.has_visited("olutravintola_putki"), true))
	rows.append(_eq("nothing else is invented by the save",
		loaded.is_visible("university_of_helsinki", {}), false))

	# a corrupt or foreign save must not conjure locations
	var foreign := CityMap.from_dict({"current": "atlantis", "discovered": ["atlantis", "home_helsinginkatu"],
		"visited": ["atlantis"]})
	rows.append(_eq("unknown ids in a save are dropped", foreign.nodes.has("atlantis"), false))
	rows.append(_eq("a foreign current location falls back safely", foreign.current,
		"home_helsinginkatu"))
	rows.append(_eq("discovered ids from the save are kept", foreign.discovered.has("home_helsinginkatu"), true))

	# ---- map geometry -------------------------------------------------------
	var positions: Array = []
	for node_id in map.nodes:
		positions.append(map.nodes[node_id].get("position", []))
	rows.append(_eq("every node has a position", positions.size(), 6))
	var inside := true
	var distinct := true
	for index in positions.size():
		var point: Array = positions[index]
		if float(point[0]) < 0.0 or float(point[0]) > 1.0 or float(point[1]) < 0.0 or float(point[1]) > 1.0:
			inside = false
		for other_index in range(index + 1, positions.size()):
			var other: Array = positions[other_index]
			if absf(float(point[0]) - float(other[0])) < 0.01 and absf(float(point[1]) - float(other[1])) < 0.01:
				distinct = false
	rows.append(_eq("positions are normalized on the map panel", inside, true))
	rows.append(_eq("no two places sit on the same point", distinct, true))

	# ---- the two opening descriptions establish "moved in yesterday" --------
	var home: Dictionary = map.nodes["home_helsinginkatu"]
	rows.append(_eq("home says the player moved in yesterday",
		String(home.get("description", "")).to_lower().contains("yesterday"), true))
	var hq: Dictionary = map.nodes["unsa_hq_ratakatu"]
	rows.append(_eq("HQ names its real street", String(hq.get("name", "")).contains("Ratakatu"), true))
	rows.append(_eq("HQ's surface is institutional, not sci-fi",
		String(hq.get("description", "")).to_lower().contains("badge"), true))

	# ---- the underground never appears in an opening illustration list ------
	var illustrated := 0
	for node_id in map.nodes:
		if not String(map.nodes[node_id].get("illustration", "")).is_empty():
			illustrated += 1
	rows.append(_eq("every node has an illustration path reserved", illustrated, 6))

	return rows
