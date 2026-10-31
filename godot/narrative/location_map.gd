## Helsinki location graph for the narrative campaign (#897 §4).
##
## Location-based narrative rather than tactical movement: the player chooses a place, then an action.
## Everything here is data-driven from `data/world/helsinki_locations.json`, so the map can grow without
## touching code and a scenario can ship its own.
##
## Discovery is a consequence of play, not of proximity: a location appears when a flag it requires is
## true. Nothing is revealed "because the player walked past" — the campaign's reveals are explicit.
extends RefCounted
class_name NoopunkLocationMap

const DATA_PATH := "res://data/world/helsinki_locations.json"

var nodes: Dictionary = {}      # id -> node dictionary
var start: String = ""
var current: String = ""
var visited: Array = []
var revealed: Array = []


static func load_data(path: String = DATA_PATH) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


## Build a map. `flags` are the campaign facts the map may consult on the first call to `refresh`.
static func from_data(data: Dictionary) -> NoopunkLocationMap:
	var map := NoopunkLocationMap.new()
	map.start = String(data.get("start", ""))
	for node in Array(data.get("nodes", [])):
		var entry: Dictionary = node
		map.nodes[String(entry.get("id", ""))] = entry
	map.current = map.start
	if not map.current.is_empty():
		map.visited.append(map.current)
		map.revealed.append(map.current)
	return map


## A node is available when every flag it requires is true. Empty requirement means always available.
static func requirements_met(node: Dictionary, flags: Dictionary) -> bool:
	for flag in Array(node.get("requires", [])):
		if not bool(flags.get(String(flag), false)):
			return false
	return true


## Reveal everything unlocked by a flag change. Returns the ids newly revealed, so the UI can say
## "a new location" instead of silently redrawing the map.
func refresh(flags: Dictionary) -> Array:
	var newly: Array = []
	for node_id in nodes:
		if revealed.has(node_id):
			continue
		if requirements_met(nodes[node_id], flags):
			revealed.append(node_id)
			newly.append(node_id)
	newly.sort()
	return newly


## Locations the player may currently travel to.
func visible(flags: Dictionary) -> Array:
	refresh(flags)
	var out: Array = []
	for node_id in revealed:
		if nodes.has(node_id):
			out.append(nodes[node_id])
	out.sort_custom(func(a, b): return String(a["id"]) < String(b["id"]))
	return out


## Actions offered at a location. `rest` and `recover` are gated by nothing; `travel` is always last.
func actions_at(node_id: String, flags: Dictionary) -> Array:
	if not nodes.has(node_id):
		return []
	var node: Dictionary = nodes[node_id]
	var out: Array = []
	for action in Array(node.get("actions", [])):
		var name := String(action)
		if name == "investigate":
			# An investigation action needs a lead to investigate, or it is a dead menu entry.
			if not bool(flags.get("has_lead", false)):
				continue
		out.append(name)
	return out


## Move to a location. Refuses unrevealed places — travel is not a way to discover the map.
func travel_to(node_id: String, flags: Dictionary) -> Dictionary:
	refresh(flags)
	if not nodes.has(node_id):
		return {"ok": false, "reason": "unknown_location"}
	if not revealed.has(node_id):
		return {"ok": false, "reason": "not_discovered"}
	var previous := current
	current = node_id
	if not visited.has(node_id):
		visited.append(node_id)
	return {"ok": true, "from": previous, "to": node_id,
		"actions": actions_at(node_id, flags)}


func has_visited(node_id: String) -> bool:
	return visited.has(node_id)


## Which locations this one opens up, for a "what did I learn" panel.
func leads_from(node_id: String) -> Array:
	if not nodes.has(node_id):
		return []
	return Array(nodes[node_id].get("reveals", []))
