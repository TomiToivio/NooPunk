extends RefCounted
class_name CwnHackingCatalogue
## The SRD hacking catalogue: Verbs, Subjects and the legality rule that joins them.
##
## Source: Cities Without Number SRD, Hacking chapter, sections 4.3.2 (Verbs) and 4.3.3 (Subjects),
## transcribed into `res://data/rules/cwn/hacking_catalogue.json`. The SRD is CC0 and permits verbatim
## transcription with citation; the commercial book's setting material is not used here.
##
## This module exists because `hacking.gd` deliberately refused to assert a catalogue: it models the
## procedure (Access pool, security check, alert clock) but had no source of truth for what a Verb costs,
## which Subjects it may touch, or what it does to difficulty. That gap is closed here, and the numbers
## come from the file rather than from memory.

const DATA_PATH := "res://data/rules/cwn/hacking_catalogue.json"

static var _doc: Dictionary = {}


static func _data() -> Dictionary:
	if not _doc.is_empty():
		return _doc
	if not FileAccess.file_exists(DATA_PATH):
		push_error("CwnHackingCatalogue: missing %s" % DATA_PATH)
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("CwnHackingCatalogue: %s is not valid JSON" % DATA_PATH)
		return {}
	_doc = parsed
	return _doc


static func verbs() -> Array:
	return _data().get("verbs", [])


static func subjects() -> Array:
	return _data().get("subjects", [])


static func verb(name: String) -> Dictionary:
	for entry in verbs():
		if entry.get("name", "") == name:
			return entry
	return {}


static func subject(name: String) -> Dictionary:
	for entry in subjects():
		if entry.get("name", "") == name:
			return entry
	return {}


static func has_verb(name: String) -> bool:
	return not verb(name).is_empty()


static func has_subject(name: String) -> bool:
	return not subject(name).is_empty()


static func can_target(verb_name: String, subject_name: String) -> bool:
	## Verbs are flexible but bounded: each may only touch certain Subject types. Glitch is Device/Cyber,
	## so Drone (a Device) is legal and Datafile (Data) is not — the SRD's own example.
	var v := verb(verb_name)
	var s := subject(subject_name)
	if v.is_empty() or s.is_empty():
		return false
	return s.get("target_type", "") in v.get("target_types", [])


static func difficulty_modifier(verb_name: String) -> int:
	## Verbs shift the Security check. The SRD lists "N/A" for Defend, which has no roll; it returns 0 so
	## callers must consult `has_security_check` rather than treating 0 as "no modifier".
	var v := verb(verb_name)
	if v.is_empty() or v.get("difficulty_modifier") == null:
		return 0
	return int(v["difficulty_modifier"])


static func has_security_check(verb_name: String) -> bool:
	var v := verb(verb_name)
	return not v.is_empty() and v.get("difficulty_modifier") != null


static func price(verb_name: String) -> int:
	return int(verb(verb_name).get("price", 0))


static func subject_price(subject_name: String) -> int:
	return int(subject(subject_name).get("price", 0))


static func occupies_cpu(verb_name: String) -> bool:
	## A program that does not self-terminate keeps its CPU slot until terminated (SRD 4.2.1 step 4).
	return bool(verb(verb_name).get("persistent", false))


static func cpu_cost(verb_name: String) -> int:
	return int(verb(verb_name).get("cpu", 0))
