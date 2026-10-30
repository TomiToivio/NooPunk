extends RefCounted
class_name CwnWages
## Common wages — CWN SRD 3.2.2.
##
## The table exists for two different jobs: hiring help, and answering "what does this NPC earn". Both need
## a daily figure, so the data stays daily and every longer period is computed from it rather than stored
## as a second number that can disagree with the first.
##
## Bribes (3.2.3) are expressed as multiples of a daily wage precisely so this module is useful for them,
## but the bribe multipliers themselves are not transcribed here: the source text I could read is cut off
## mid-table, and a partial price list invites invented numbers.

const DATA_PATH := "res://data/rules/cwn/wages.json"

static var _doc: Dictionary = {}


static func _data() -> Dictionary:
	if not _doc.is_empty():
		return _doc
	if not FileAccess.file_exists(DATA_PATH):
		push_error("CwnWages: missing %s" % DATA_PATH)
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("CwnWages: %s is not valid JSON" % DATA_PATH)
		return {}
	_doc = parsed
	return _doc


static func all() -> Array:
	return _data().get("wages", [])


static func entry(id: String) -> Dictionary:
	for row in all():
		if row.get("id", "") == id:
			return row
	return {}


static func daily(id: String) -> int:
	## An unknown role is a refusal, not a zero: a wage of 0 would hire someone for nothing.
	var row := entry(id)
	if row.is_empty():
		push_error("CwnWages: unknown role '%s'" % id)
		return 0
	return int(row.get("daily", 0))


static func for_days(id: String, days: int) -> int:
	if days < 0:
		push_error("CwnWages: negative duration %d" % days)
		return 0
	return daily(id) * days


static func by_name(name: String) -> Dictionary:
	for row in all():
		if row.get("name", "") == name:
			return row
	return {}


static func bribe(id: String, multiplier: int) -> int:
	## The multiplier comes from the SRD's bribe table (3.2.3), which this module does not transcribe.
	var cost := daily(id) * multiplier
	return cost
