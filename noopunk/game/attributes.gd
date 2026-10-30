extends RefCounted
## NoöPunk attribute rules (#835) — read from the single data file, never duplicated here.
##
## `res://data/attributes.json` is the authority for the seven attributes, the 3d6 bands, the human range
## and the difficulty scale; noopunk/rulebook/RULEBOOK.md cites the same path. Keeping one copy is the
## point: a second table in GDScript would drift from the book the first time either was edited.

const DATA_PATH := "res://data/attributes.json"

static var NAMES: PackedStringArray = []
static var DEFINITIONS: Array[String] = []
static var DIFFICULTIES: Dictionary = {}
static var BANDS: Array = []
static var HUMAN_MIN := -3
static var HUMAN_MAX := 3
static var _loaded := false


static func ensure_loaded() -> void:
	if _loaded:
		return
	_loaded = true
	var file := FileAccess.open(DATA_PATH, FileAccess.READ)
	if file == null:
		push_error("cannot open %s" % DATA_PATH)
		return
	var doc = JSON.parse_string(file.get_as_text())
	if typeof(doc) != TYPE_DICTIONARY:
		push_error("%s is not valid JSON" % DATA_PATH)
		return
	NAMES = PackedStringArray()
	DEFINITIONS = []
	for entry in doc.get("attributes", []):
		NAMES.append(entry["name"])
		DEFINITIONS.append(entry["definition"])
	BANDS = []
	for band in doc.get("generation", {}).get("bands", []):
		BANDS.append([int(band[0]), int(band[1]), int(band[2])])
	var human: Array = doc.get("human_range", [-3, 3])
	HUMAN_MIN = int(human[0])
	HUMAN_MAX = int(human[1])
	DIFFICULTIES = {}
	for entry in doc.get("difficulty", []):
		DIFFICULTIES[int(entry["target"])] = entry["label"]


static func modifier(total: int) -> int:
	## The author's bands, read from the shared data file. Out of range is refused, never clamped.
	ensure_loaded()
	for band in BANDS:
		if total >= band[0] and total <= band[1]:
			return band[2]
	push_error("3d6 total %d outside 3..18" % total)
	return 0


static func roll_character(rng: RandomNumberGenerator) -> Dictionary:
	ensure_loaded()
	var values := {}
	for name in NAMES:
		var total := rng.randi_range(1, 6) + rng.randi_range(1, 6) + rng.randi_range(1, 6)
		values[name] = modifier(total)
	return values


static func display_value(value: int) -> String:
	return "%+d" % value
