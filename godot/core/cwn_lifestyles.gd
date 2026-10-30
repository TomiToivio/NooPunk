extends RefCounted
class_name CwnLifestyles
## Lifestyle costs and their System Strain ceilings — CWN SRD 3.2.1.
##
## The table is not decoration: the SRD says the modifier applies "as soon as a PC starts paying - or not
## paying - for a given lifestyle level". So a squatter's maximum System Strain is two lower than a
## luxury resident's, which changes how much cyberware a character can carry at all.
##
## `0` is a real modifier here, not a missing value: middle-class living changes nothing. A lookup that
## returned null for it would force every caller to special-case the most common level.

const DATA_PATH := "res://data/rules/cwn/lifestyles.json"

static var _doc: Dictionary = {}


static func _data() -> Dictionary:
	if not _doc.is_empty():
		return _doc
	if not FileAccess.file_exists(DATA_PATH):
		push_error("CwnLifestyles: missing %s" % DATA_PATH)
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("CwnLifestyles: %s is not valid JSON" % DATA_PATH)
		return {}
	_doc = parsed
	return _doc


static func levels() -> Array:
	return _data().get("levels", [])


static func level(id: String) -> Dictionary:
	for entry in levels():
		if entry.get("id", "") == id:
			return entry
	return {}


static func monthly_cost(id: String) -> int:
	return int(level(id).get("monthly_cost", 0))


static func strain_modifier(id: String) -> int:
	## Unknown lifestyle is a refusal, not a quiet zero: guessing someone's living costs is worse than
	## telling the caller the id is wrong.
	var entry := level(id)
	if entry.is_empty():
		push_error("CwnLifestyles: unknown lifestyle '%s'" % id)
		return 0
	return int(entry.get("max_strain_modifier", 0))


static func max_system_strain(base: int, id: String) -> int:
	## A lifestyle can never raise the ceiling above what the rules allow, but it can lower it below one.
	return maxi(0, base + strain_modifier(id))


static func most_expensive_affordable(budget: int) -> String:
	## The best level the character can actually pay for; squatter life is always available at $0.
	var best := "squatter"
	for entry in levels():
		if int(entry.get("monthly_cost", 0)) <= budget:
			if int(entry.get("monthly_cost", 0)) >= monthly_cost(best):
				best = String(entry.get("id"))
	return best
