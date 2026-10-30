class_name RookieCharacter
extends RefCounted

## A UNSA agent straight from the academy (#835). Seven attributes, each rolled as 3d6 and shown as
## its converted signed value. The table, the attribute list and the difficulty reference live in
## res://data/attributes.json so the rulebook and the game cannot drift apart.

const DATA_PATH := "res://data/attributes.json"

var data: Dictionary = {}
var totals: Dictionary = {}
var values: Dictionary = {}


func _init(path: String = DATA_PATH) -> void:
	var text := FileAccess.get_file_as_string(path)
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("RookieCharacter: %s is not a JSON object" % path)
		return
	data = parsed


func attribute_ids() -> Array:
	var ids: Array = []
	for entry in data.get("attributes", []):
		ids.append(String(entry["id"]))
	return ids


## Convert one raw 3d6 total with the same table the rulebook publishes.
func convert_total(total: int) -> int:
	for row in data.get("generation", {}).get("table", []):
		if total >= int(row["min"]) and total <= int(row["max"]):
			return int(row["value"])
	push_error("RookieCharacter: 3d6 total %d is outside the generation table" % total)
	return 0


func is_valid_total(total: int) -> bool:
	for row in data.get("generation", {}).get("table", []):
		if total >= int(row["min"]) and total <= int(row["max"]):
			return true
	return false


func human_range() -> Vector2i:
	var human: Dictionary = data.get("human", {})
	return Vector2i(int(human.get("min", -3)), int(human.get("max", 3)))


## Roll all seven attributes independently. Passing a seeded RNG makes the roll reproducible.
func roll(rng: RandomNumberGenerator = null) -> Dictionary:
	var generator := rng if rng != null else RandomNumberGenerator.new()
	if rng == null:
		generator.randomize()
	var count := int(data.get("generation", {}).get("dice_count", 3))
	var sides := int(data.get("generation", {}).get("dice_sides", 6))
	totals = {}
	values = {}
	for id in attribute_ids():
		var total := 0
		for i in count:
			total += generator.randi_range(1, sides)
		totals[id] = total
		values[id] = convert_total(total)
	return values.duplicate()


func label_for(id: String) -> String:
	for entry in data.get("attributes", []):
		if String(entry["id"]) == id:
			return String(entry["name"])
	return id


func signed(id: String) -> String:
	var value := int(values.get(id, 0))
	return ("+%d" % value) if value > 0 else str(value)
