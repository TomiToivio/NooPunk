## The location screen: does a player actually reach the map and the notebook (#897 §4)?
extends RefCounted

const Screen := preload("res://godot/ui/location_screen.gd")
const Map := preload("res://godot/narrative/location_map.gd")
const Notebook := preload("res://godot/narrative/investigation.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _screen(flags: Dictionary = {}) -> Object:
	var file := FileAccess.open("res://data/world/lakkahaltia_clues.json", FileAccess.READ)
	var data: Variant = JSON.parse_string(file.get_as_text()) if file != null else {}
	var screen: Object = Screen.new()
	screen.setup(Map.from_data(Map.load_data()), Notebook.from_data(data if data is Dictionary else {}), flags)
	return screen


func run() -> Array:
	var rows: Array = []
	var screen := _screen({})
	rows.append(_eq("only two Helsinki locations at start", screen.map.visible({}).size(), 2))
	rows.append(_eq("university initially hidden", screen.map.revealed.has("university_of_helsinki"), false))
	rows.append(_eq("the screen names the current place", screen._title.text, "Home · Helsinginkatu"))
	rows.append(_eq("the district is shown", screen._district.text != "", true))
	rows.append(_eq("actions are offered", screen._actions.get_child_count() > 0, true))
	rows.append(_eq("travel destinations are drawn", screen._travel.get_child_count() > 1, true))
	rows.append(_eq("the travel list has no duplicates after a refresh",
		screen._travel.get_child_count() == _travellable(screen) + 1, true))
	rows.append(_eq("the status line counts visits", screen._status.text.contains("visited"), true))

	# travel updates the screen, not just the model
	screen._on_travel("unsa_hq_ratakatu")
	rows.append(_eq("travel moves the title", screen._title.text, "UNSA Helsinki Field Office · Ratakatu"))
	rows.append(_eq("travel is logged", screen._log.get_parsed_text().contains("arrived"), true))
	rows.append(_eq("the current place is not offered as a destination",
		_travel_disabled(screen, "unsa_hq_ratakatu"), true))

	# an undiscovered place cannot be reached from the UI either
	screen._on_travel("olutravintola_putki")
	rows.append(_eq("an undiscovered place is refused", screen._log.get_parsed_text().contains("cannot travel"), true))

	# investigate is conditional on a lead, in the screen as in the model
	var no_lead := _screen({})
	rows.append(_eq("no investigate without a lead", _has_action(no_lead, "interview"), false))
	var with_lead := _screen({"knows_university": true, "has_lead": true})
	with_lead._on_travel("university_of_helsinki")  # investigate lives at the harbour, not at HQ
	rows.append(_eq("investigate appears with a lead", _has_action(with_lead, "interview"), true))

	# placeholder actions admit they are placeholders rather than faking an outcome
	with_lead._on_action("interview")
	rows.append(_eq("a placeholder says so", with_lead._log.get_parsed_text().contains("not yet wired"), true))

	# the notebook is visible to the player
	rows.append(_eq("leads are shown", with_lead._clues.text.contains("leads"), true))

	# Free what we built. A Control left alive holds its labels, fonts and RichTextLabel items, and the
	# shutdown gate reports those as leaked RIDs at exit (#883). A suite that measures something must also
	# clean up after itself.
	for screen_object in [screen, no_lead, with_lead]:
		screen_object.free()
	return rows


func _travellable(screen: Object) -> int:
	return screen.map.visible(screen.flags).size()


func _has_action(screen: Object, name: String) -> bool:
	for child in screen._actions.get_children():
		if String(child.text) == name:
			return true
	return false


func _travel_disabled(screen: Object, node_id: String) -> bool:
	for child in screen._travel.get_children():
		if child is Button and String(screen.map.nodes[node_id].get("name", "")) in String(child.text):
			return bool(child.disabled)
	return false
