extends RefCounted
class_name Agent
## A UNSA agent fresh from the academy (#835).
##
## The rules live in exactly one place — `res://data/attributes.json` — and this script reads them. The
## rulebook cites the same file, so the book and the game cannot drift into two tables.

const DATA_PATH := "res://data/attributes.json"
const HUMAN_MIN := -3
const HUMAN_MAX := 3

static var _doc: Dictionary = {}


static func _data() -> Dictionary:
	if _doc.is_empty():
		var file := FileAccess.open(DATA_PATH, FileAccess.READ)
		if file == null:
			push_error("cannot open %s" % DATA_PATH)
			return {}
		_doc = JSON.parse_string(file.get_as_text())
	return _doc


static func attribute_names() -> PackedStringArray:
	var names := PackedStringArray()
	for entry in _data().get("attributes", []):
		names.append(entry["name"])
	return names


static func roll_total() -> int:
	## 3d6, separately for each attribute.
	return randi() % 6 + 1 + randi() % 6 + 1 + randi() % 6 + 1


static func value_for_total(total: int) -> int:
	## The author's bands, read from the shared data file. Out-of-range totals are refused, never clamped.
	for band in _data().get("generation", {}).get("bands", []):
		if total >= band[0] and total <= band[1]:
			return band[2]
	push_error("3d6 total %d outside 3-18" % total)
	return 0


static func signed(value: int) -> String:
	return "%+d" % value


static func roll_sheet() -> Array:
	## One [name, definition, value] row per attribute — the sheet, not the raw rolls.
	var rows := []
	for entry in _data().get("attributes", []):
		rows.append([entry["name"], entry["definition"], value_for_total(roll_total())])
	return rows


static func is_transhuman(rows: Array) -> bool:
	return rows.any(func(row): return row[2] > HUMAN_MAX)
