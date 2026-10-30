## CWN program legality, read from the transcribed SRD table (`data/rules/cwn_program_catalogue.json`).
##
## The engine may not invent a rule (AGENTS.md). This class only *reads* the catalogue and refuses what
## the table forbids, so the hacking screen cannot run an illegal program even if a caller asks.
extends RefCounted

const CATALOGUE_PATH := "res://data/rules/cwn_program_catalogue.json"

var verbs: Dictionary = {}
var subjects: Dictionary = {}

func _init(path := CATALOGUE_PATH) -> void:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("program catalogue missing: %s" % path)
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("program catalogue is not a JSON object")
		return
	verbs = parsed.get("verbs", {})
	subjects = parsed.get("subjects", {})

func has_verb(name: String) -> bool:
	return verbs.has(name)

func has_subject(name: String) -> bool:
	return subjects.has(name)

## Returns {} when the program may run, or {"error": "<reason>"} when the table forbids it.
func check(verb_name: String, subject_name: String, access_available: int, cpu_free: int) -> Dictionary:
	if not verbs.has(verb_name):
		return {"error": "unknown Verb: %s" % verb_name}
	if not subjects.has(subject_name):
		return {"error": "unknown Subject: %s" % subject_name}
	var verb: Dictionary = verbs[verb_name]
	var subject: Dictionary = subjects[subject_name]
	var target_types: Array = verb.get("target_types", [])
	if not target_types.has(subject.get("subject_type", "")):
		return {"error": "%s cannot target a %s" % [verb_name, subject_name]}
	if access_available < int(verb.get("access_cost", 0)):
		return {"error": "%s costs %d Access; %d available" % [verb_name, int(verb["access_cost"]), access_available]}
	if cpu_free < 1:
		return {"error": "no free CPU slot to run %s" % verb_name}
	var self_terminating: bool = bool(verb.get("self_terminating", false))
	return {
		"access_spent": int(verb.get("access_cost", 0)),
		"requires_check": bool(verb.get("requires_check", true)),
		"skill_modifier": verb.get("skill_modifier", 0),
		"cpu_held": 0 if self_terminating else 1,
	}
