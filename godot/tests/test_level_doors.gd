## Level connectivity: every room the case needs must actually be walkable from the lobby.
##
## The first build passed the data suite and was still unplayable: its doorway segments tiled the walls
## exactly, and the corridor's side walls were solid. This suite pins the properties that failed.
extends RefCounted

const LEVEL := "res://godot/scenarios/lakkahaltia/level_hospital.json"

func run() -> Array:
	var rows: Array = []
	var level: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(LEVEL))
	var doors: Array = level.get("doorways", [])
	rows.append(_eq("the level declares doorways", doors.size() >= 6, true))

	var connections := [
		["lobby", "north", "corridor", "south"],
		["corridor", "west", "reception", "east"],
		["corridor", "east", "consultation", "west"],
	]
	for pair in connections:
		var a: Dictionary = _find(doors, pair[0], pair[1])
		var b: Dictionary = _find(doors, pair[2], pair[3])
		rows.append(_eq("%s/%s has a door" % [pair[0], pair[1]], not a.is_empty(), true))
		rows.append(_eq("%s/%s has a door" % [pair[2], pair[3]], not b.is_empty(), true))
		if not a.is_empty() and not b.is_empty():
			rows.append(_eq("the two sides of %s/%s agree on width" % [pair[0], pair[2]],
				float(a["width"]), float(b["width"])))
			rows.append(_eq("the two sides of %s/%s agree on offset" % [pair[0], pair[2]],
				float(a["offset"]), float(b["offset"])))

	# An opening wider than its wall would cut the wall away and leave the room open to the void.
	for door in doors:
		var room := _room(level.get("rooms", []), String(door["room"]))
		if room.is_empty():
			rows.append(_eq("door names a real room: %s" % door["room"], false, true))
			continue
		var size: Array = room["size"]
		var length := float(size[0]) if String(door["wall"]) in ["north", "south"] else float(size[2])
		var fits := float(door["width"]) <= length - 0.4
		rows.append(_eq("door fits its wall in %s/%s" % [door["room"], door["wall"]], fits, true))
	return rows

func _find(doors: Array, room: String, wall: String) -> Dictionary:
	for door in doors:
		if String(door.get("room", "")) == room and String(door.get("wall", "")) == wall:
			return door
	return {}

func _room(rooms: Array, room_id: String) -> Dictionary:
	for room in rooms:
		if String(room.get("id", "")) == room_id:
			return room
	return {}

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]
