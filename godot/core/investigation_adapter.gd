## The investigation adapter: the *only* place the Godot slice reads the investigative layer (#718).
##
## Why an adapter and not an implementation: `AGENTS.md` §14 puts the order at
## tabletop rule -> digital specification -> Godot -> Concordia, and the repository already owns the
## approved layer in `src/rules/investigation.py` with its data in
## `data/scenarios/lakkahaltia/case_graph.json`. This class *reads* that graph and applies it; it
## hardcodes no clue, no competency, no scene and no band.
##
## What is deliberately explicit rather than assumed:
##   * the graph is `noopunk-case-graph` format and is validated by the Python loader, not here; this
##     adapter refuses a file whose `format` is not the known one rather than guessing;
##   * discovery is automatic: a competent investigator receives the clue. Nothing here rolls;
##   * an unknown scene is an error, not an empty result. An empty result and a missing scene must not
##     look the same to a caller.
##
## UNVERIFIED AT RUNTIME: this file was written on a host with no Godot binary (see #718). The contract
## it depends on is tested in `tests/test_case_graph_contract.py`, which runs in CI; the GDScript itself
## still needs one `godot --headless` smoke run before it can be called proven.
class_name InvestigationAdapter
extends RefCounted

const DEFAULT_GRAPH_PATH := "res://data/scenarios/lakkahaltia/case_graph.json"
const FORMAT := "noopunk-case-graph"

var graph: Dictionary = {}

func _init(graph_path: String = DEFAULT_GRAPH_PATH) -> void:
	graph = _load_json(graph_path)
	if graph.get("format", "") != FORMAT:
		push_error("InvestigationAdapter: %s is not a %s file" % [graph_path, FORMAT])

func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("InvestigationAdapter: missing %s" % path)
		return {}
	var text := FileAccess.get_file_as_string(path)
	var parsed: Variant = JSON.parse_string(text)
	return parsed if parsed is Dictionary else {}

func case_id() -> String:
	return String(graph.get("case_id", ""))

func scene_ids() -> Array:
	var ids: Array = []
	for scene in graph.get("scenes", []):
		ids.append(String(scene.get("id", "")))
	return ids

func scene(scene_id: String) -> Dictionary:
	for entry in graph.get("scenes", []):
		if String(entry.get("id", "")) == scene_id:
			return entry
	return {}

## The discovery call. `sheet` maps competency -> rank; rank 0 is trained, absence is untrained.
## Returns the clues the investigator simply receives, and whether the scene can be left.
## No die, no difficulty, no band: if the caller wants a roll, it is for action, not for finding.
func discover(scene_id: String, sheet: Dictionary) -> Dictionary:
	var entry := scene(scene_id)
	if entry.is_empty():
		push_error("InvestigationAdapter: unknown scene %s" % scene_id)
		return {"scene_id": scene_id, "clues": [], "can_leave": false, "error": "unknown_scene"}

	var granted: Array = []
	var can_leave := false
	for clue in entry.get("clues", []):
		var competency := String(clue.get("competency", ""))
		if sheet.has(competency):
			granted.append(clue)
			if String(clue.get("kind", "")) == "core":
				can_leave = true

	return {
		"scene_id": scene_id,
		"clues": granted,
		"can_leave": can_leave,
		"granted_by": "competency" if not granted.is_empty() else "none",
	}

## Hypotheses are data, not a verdict. The adapter can list them and their family; it never decides.
func hypotheses() -> Array:
	return graph.get("hypotheses", [])
