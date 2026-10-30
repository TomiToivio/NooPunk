class_name NoopunkAttributes
extends RefCounted

## The character sheet rules from `noopunk/rulebook/RULEBOOK.md` ("Characters"), read from
## `noopunk/game/data/attributes.json` (#835).
##
## One table, two readers: the rulebook quotes it for the tabletop, this file loads it for the game.
## The game never holds a second copy of the bands, so the two cannot disagree about what a 3d6 total
## of 15 means.
##
## Scope note: this milestone is a sheet and a roll. No check mechanic exists for the difficulty
## targets - the table is reference data until the author specifies how a roll is resolved.

const DATA_PATH := "res://data/attributes.json"

static var _data: Dictionary = {}

static func data() -> Dictionary:
	if _data.is_empty():
		if not FileAccess.file_exists(DATA_PATH):
			push_error("NoopunkAttributes: missing %s" % DATA_PATH)
			return {}
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
		_data = parsed if typeof(parsed) == TYPE_DICTIONARY else {}
	return _data

static func premise() -> String:
	return str(data().get("premise", ""))

## The seven attributes in sheet order: [{"name", "definition"}, ...].
static func attribute_definitions() -> Array:
	return data().get("attributes", [])

static func attribute_names() -> Array:
	var names: Array = []
	for entry in attribute_definitions():
		names.append(str(entry.get("name", "")))
	return names

static func human_min() -> int:
	return int(data().get("human_range", {}).get("min", -3))

static func human_max() -> int:
	return int(data().get("human_range", {}).get("max", 3))

## Convert a 3d6 total into the displayed attribute value, exactly as the rulebook table says.
## Totals outside 3..18 are not a possible roll and are refused rather than clamped: a caller passing
## 2 or 19 has a bug, and quietly returning a value would hide it.
static func modifier_for(total: int) -> int:
	for band in data().get("bands", []):
		if total >= int(band["min"]) and total <= int(band["max"]):
			return int(band["value"])
	push_error("NoopunkAttributes: %d is not a possible 3d6 total" % total)
	return 0

static func is_human_value(value: int) -> bool:
	return value >= human_min() and value <= human_max()

## Roll 3d6 for each attribute. Dice come from the caller's RNG so a seeded run is reproducible and a
## test can pin the boundaries.
static func roll(rng: RandomNumberGenerator) -> Dictionary:
	var rolled := {}
	for name in attribute_names():
		var total := 0
		for die in 3:
			total += rng.randi_range(1, 6)
		rolled[name] = {"total": total, "value": modifier_for(total)}
	return rolled

## The sheet as the player sees it: the converted signed value per attribute, not the raw dice.
static func sheet(rolled: Dictionary) -> Dictionary:
	var out := {}
	for name in attribute_names():
		out[name] = int(rolled.get(name, {}).get("value", 0))
	return out

## A human-readable summary, e.g. "Fitness +1  Reflexes 0  Cognition -2 ...".
static func format_sheet(values: Dictionary) -> String:
	var parts: Array = []
	for name in attribute_names():
		var value := int(values.get(name, 0))
		parts.append("%s %s%d" % [name, "+" if value >= 0 else "", value])
	return "   ".join(parts)

static func difficulty_scale() -> Array:
	return data().get("difficulty", [])
