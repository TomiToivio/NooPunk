extends RefCounted
class_name NoopunkAttributes

## Seven attributes, 3d6 each, converted through the one table in `noopunk/data/attributes.json`.
##
## The rulebook states the same table in prose and points here (#835 requirement 4): one table, read by
## both, so the book and the game cannot drift. Nothing here decides how a difficulty target is
## resolved — that mechanic is undecided and deliberately absent.

const CONTRACT_PATH := "res://data/attributes.json"

static var _contract: Dictionary = {}


static func contract() -> Dictionary:
	if _contract.is_empty():
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CONTRACT_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_contract = parsed
	return _contract


static func names() -> Array:
	return contract().get("attributes", [])


static func definition(attribute_name: String) -> String:
	return String(contract().get("definitions", {}).get(attribute_name, ""))


## The converted value for a 3d6 total, straight from the table. Totals outside 3-18 are refused
## rather than clamped: a 19 is a bug, not a very good roll.
static func value_for_total(total: int) -> int:
	for band in contract().get("generation", {}).get("bands", []):
		if total >= int(band["low"]) and total <= int(band["high"]):
			return int(band["value"])
	return -2147483648  # sentinel: no band matched, callers must treat it as an error


static func is_valid_total(total: int) -> bool:
	for band in contract().get("generation", {}).get("bands", []):
		if total >= int(band["low"]) and total <= int(band["high"]):
			return true
	return false


static func human_range() -> Array:
	return contract().get("generation", {}).get("human_range", [-3, 3])


static func difficulty_label(target: int) -> String:
	for entry in contract().get("difficulty", []):
		if int(entry["target"]) == target:
			return String(entry["label"])
	return ""


## The sheet syntax for a converted attribute: `Fitness+2`, `Empathy-3`, `Agency+0`.
static func display(attribute_name: String, value: int) -> String:
	return "%s%+d" % [attribute_name, value]


## Roll one attribute: three six-sided dice, converted. Returns both numbers so a caller can show the
## total if it wants to, while the *stored* value is always the converted one.
static func roll_one(rng: RandomNumberGenerator, attribute_name: String) -> Dictionary:
	var total := rng.randi_range(1, 6) + rng.randi_range(1, 6) + rng.randi_range(1, 6)
	return {"name": attribute_name, "total": total, "value": value_for_total(total)}


## Roll the whole sheet: exactly seven attributes, in the contract's order.
static func roll_all(rng: RandomNumberGenerator) -> Array:
	var rolls: Array = []
	for attribute_name in names():
		rolls.append(roll_one(rng, String(attribute_name)))
	return rolls


static func sheet_lines(rolls: Array) -> Array:
	var lines: Array = []
	for roll in rolls:
		lines.append(display(String(roll.get("name", "")), int(roll.get("value", 0))))
	return lines
