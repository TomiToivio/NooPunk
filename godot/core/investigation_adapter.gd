## The investigation adapter: the *only* place Godot reads a clue rule (#718).
##
## Why an adapter: `AGENTS.md` §14 orders tabletop rule -> digital specification -> Godot, and the
## rule is already implemented and tested in `src/rules/investigation.py`. This class reads the
## **same** `noopunk-case-graph` JSON and applies the same three rules; it computes no clue, no
## band and no difficulty locally.
##
## The three rules, restated because Godot must not drift from Python:
##   1. competence is the *presence* of a skill entry - CWN rank 0 is trained;
##   2. competence is necessary, never sufficient: a clue may also require ``access`` and a
##      declared kind of ``inquiry`` (a passive clue needs no inquiry);
##   3. nothing here rolls. Discovery is not a check.
class_name InvestigationAdapter
extends RefCounted

const DEFAULT_CASE_PATH := "res://data/scenarios/lakkahaltia/case_graph.json"
const DEFAULT_KERNEL_PATH := "res://data/rules/without_number.json"

var case_graph: Dictionary = {}
var kernel: Dictionary = {}

func _init(case_path: String = DEFAULT_CASE_PATH, kernel_path: String = DEFAULT_KERNEL_PATH) -> void:
	case_graph = _load_json(case_path)
	kernel = _load_json(kernel_path)

func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("InvestigationAdapter: missing %s" % path)
		return {}
	var text := FileAccess.get_file_as_string(path)
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("InvestigationAdapter: %s is not a JSON object" % path)
		return {}
	return parsed

func scene_ids() -> Array:
	var ids: Array = []
	for scene in case_graph.get("scenes", []):
		ids.append(String(scene.get("id", "")))
	return ids

func scene(scene_id: String) -> Dictionary:
	for scene in case_graph.get("scenes", []):
		if String(scene.get("id", "")) == scene_id:
			return scene
	push_error("InvestigationAdapter: no scene %s" % scene_id)
	return {}

## Competence is the presence of a skill entry. Rank 0 counts: CWN 0 is basic competence.
func is_competent(sheet: Dictionary, competency: String) -> bool:
	return sheet.has(competency)

## What a competent investigator gets in this scene, and what the scene withheld.
##
## `access` and `inquiry` are arrays of strings. A clue with an `access` key needs that
## permission; a clue with an `inquiry` key needs that declared approach unless it is passive.
func discover(scene_id: String, sheet: Dictionary, access: Array = [], inquiry: Array = []) -> Dictionary:
	var target := scene(scene_id)
	if target.is_empty():
		return {"scene": scene_id, "clues": [], "withheld": [], "can_leave": false}
	var clues: Array = []
	var withheld: Array = []
	var can_leave := false
	for clue in target.get("clues", []):
		if _permits(clue, sheet, access, inquiry):
			clues.append(clue)
			if String(clue.get("kind", "")) == "core":
				can_leave = true
		else:
			withheld.append(String(clue.get("id", "")))
	return {"scene": scene_id, "clues": clues, "withheld": withheld, "can_leave": can_leave}

func _permits(clue: Dictionary, sheet: Dictionary, access: Array, inquiry: Array) -> bool:
	if not is_competent(sheet, String(clue.get("competency", ""))):
		return false
	var required_access := String(clue.get("access", ""))
	if required_access != "" and not access.has(required_access):
		return false
	var required_inquiry := String(clue.get("inquiry", ""))
	if required_inquiry != "" and not bool(clue.get("passive", false)) and not inquiry.has(required_inquiry):
		return false
	return true

## Every scene must be leavable, so the Godot slice cannot ship a dead-ended case.
func validate() -> Array:
	var problems: Array = []
	if case_graph.get("scenes", []).is_empty():
		problems.append("case has no scenes")
	for scene in case_graph.get("scenes", []):
		var has_core := false
		for clue in scene.get("clues", []):
			if String(clue.get("kind", "")) == "core":
				has_core = true
		if not has_core and not bool(scene.get("terminal", false)):
			problems.append("scene %s has no core clue" % String(scene.get("id", "")))
	return problems

## Every competency named in the case graph must exist in the WN skill list.
func unknown_competencies() -> Array:
	var known: Array = kernel.get("skills", {}).get("names", [])
	var unknown: Array = []
	for scene in case_graph.get("scenes", []):
		for clue in scene.get("clues", []):
			var competency := String(clue.get("competency", ""))
			if competency != "" and not known.has(competency):
				unknown.append(competency)
	return unknown
