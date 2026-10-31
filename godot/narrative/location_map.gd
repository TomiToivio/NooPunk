## Helsinki city map: nodes, discovery, travel and persistence (#913).
##
## Replaces the earlier flag-gated graph as the project's location model. The rule that shapes it:
## **a place the player has not learned about does not exist on the map.** Not greyed out, not "???", not a
## locked pin — absent. That is why `visible()` returns only discovered nodes and why the underground has
## its own `hidden_until` guard rather than a lock icon.
##
## Positions are normalized 0..1 on the map panel so the layout survives every window size. Helsinki
## geography, ordinary streets, no invented districts.
##
## Save/load is a plain dictionary: `to_dict()` and `from_dict()`. Whatever owns the save file decides
## where it goes; this model only guarantees the round trip.
extends RefCounted
class_name NoopunkCityMap

const DATA_PATH := "res://data/world/helsinki_city.json"

##: Order matters only for display; discovery does not depend on it.
var nodes: Dictionary = {}
var order: Array = []
var start: String = ""
var current: String = ""
var discovered: Array = []
var visited: Array = []


static func load_data(path: String = DATA_PATH) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


static func from_data(data: Dictionary) -> NoopunkCityMap:
	var map := NoopunkCityMap.new()
	map.start = String(data.get("start", ""))
	map.current = map.start
	for entry in Array(data.get("nodes", [])):
		var node: Dictionary = entry
		var node_id := String(node.get("id", ""))
		if node_id.is_empty():
			continue
		map.nodes[node_id] = node
		map.order.append(node_id)
		if bool(node.get("visible_at_start", false)):
			map.discovered.append(node_id)
	if not map.current.is_empty() and map.discovered.has(map.current):
		map.visited.append(map.current)
	return map


## Build the shipped Helsinki map.
static func helsinki() -> NoopunkCityMap:
	return from_data(load_data())


# ---- discovery -----------------------------------------------------------------------------------

## Why a node is or is not on the map. Returned rather than implied, so tests and UI can explain it.
func status(node_id: String, flags: Dictionary) -> String:
	if not nodes.has(node_id):
		return "unknown"
	var node: Dictionary = nodes[node_id]
	if bool(node.get("underground", false)) and not _hidden_guard_open(node, flags):
		# The underground is concealed, never merely locked: a visible locked door is still a reveal.
		return "concealed"
	var guard := String(node.get("hidden_until", ""))
	if not guard.is_empty() and _hidden_guard_open(node, flags):
		# The milestone that opens the guard is itself the discovery: the player has been told.
		return "visited" if visited.has(node_id) else "known"
	if discovered.has(node_id) or _triggered(node, flags):
		return "visited" if visited.has(node_id) else "known"
	return "hidden"


func _hidden_guard_open(node: Dictionary, flags: Dictionary) -> bool:
	var guard := String(node.get("hidden_until", ""))
	if guard.is_empty():
		return true
	return bool(flags.get(guard, false))


func _triggered(node: Dictionary, flags: Dictionary) -> bool:
	var discovery: Variant = node.get("discovery", {})
	if not (discovery is Dictionary):
		return false
	var flag := String((discovery as Dictionary).get("flag", ""))
	return not flag.is_empty() and bool(flags.get(flag, false))


## Learn about everything the current flags justify. Returns the ids newly discovered, so the UI can say
## "a new place" instead of silently redrawing the map.
func refresh(flags: Dictionary) -> Array:
	var newly: Array = []
	for node_id in order:
		var node: Dictionary = nodes[node_id]
		if bool(node.get("underground", false)) and not _hidden_guard_open(node, flags):
			continue
		if discovered.has(node_id) or not _triggered(node, flags):
			continue
		discovered.append(node_id)
		newly.append(node_id)
	newly.sort()
	return newly


## Nodes the player may see and travel to. Hidden nodes are absent, not disabled.
func visible(flags: Dictionary) -> Array:
	refresh(flags)
	var out: Array = []
	for node_id in discovered:
		var state := status(node_id, flags)
		if state == "hidden" or state == "concealed":
			continue
		out.append(nodes[node_id])
	out.sort_custom(func(a, b): return String(a["id"]) < String(b["id"]))
	return out


func is_visible(node_id: String, flags: Dictionary) -> bool:
	return status(node_id, flags) in ["known", "visited"]


# ---- travel --------------------------------------------------------------------------------------

func actions_at(node_id: String, flags: Dictionary) -> Array:
	if not is_visible(node_id, flags):
		return []
	return Array(nodes[node_id].get("actions", []))


## Travel to a visible node. Refuses hidden and concealed places: travel is not a way to discover the map.
func travel_to(node_id: String, flags: Dictionary) -> Dictionary:
	if not nodes.has(node_id):
		return {"ok": false, "reason": "unknown_location"}
	var state := status(node_id, flags)
	if state == "hidden":
		return {"ok": false, "reason": "not_discovered"}
	if state == "concealed":
		return {"ok": false, "reason": "clearance_required"}
	var previous := current
	current = node_id
	if not visited.has(node_id):
		visited.append(node_id)
	return {"ok": true, "from": previous, "to": node_id, "actions": actions_at(node_id, flags)}


func has_visited(node_id: String) -> bool:
	return visited.has(node_id)


# ---- persistence ---------------------------------------------------------------------------------

func to_dict() -> Dictionary:
	return {
		"city": "helsinki",
		"current": current,
		"discovered": discovered.duplicate(),
		"visited": visited.duplicate(),
	}


## Rebuild from a save. Unknown ids in the save are dropped rather than recreated: a save from a different
## campaign must not conjure locations this build does not have.
static func from_dict(data: Dictionary) -> NoopunkCityMap:
	var map := helsinki()
	map.discovered = []
	map.visited = []
	for node_id in Array(data.get("discovered", [])):
		if map.nodes.has(String(node_id)):
			map.discovered.append(String(node_id))
	for node_id in Array(data.get("visited", [])):
		if map.nodes.has(String(node_id)) and not map.visited.has(String(node_id)):
			map.visited.append(String(node_id))
	var saved_current := String(data.get("current", ""))
	if map.nodes.has(saved_current) and map.discovered.has(saved_current):
		map.current = saved_current
	return map


## True when the underground has not been disclosed in any form. Used by tests and by the screen to prove
## that nothing leaks it early.
func underground_concealed(flags: Dictionary) -> bool:
	for node_id in nodes:
		if bool(nodes[node_id].get("underground", false)):
			if status(node_id, flags) != "concealed":
				return false
	return true
