extends RefCounted
class_name CityMap
## The starting Helsinki map (#913): location nodes, exactly two selectable at first.
##
## The map is data, not a drawing. A scene renders whatever `selectable()` returns, so "locked" is a fact
## the renderer cannot disagree with — the usual failure being an undiscovered node that still looks
## pressable because the artist drew it like the others.
##
## Grounding is a rule here too: `forbidden_visual_terms()` exists so a data edit that sneaks a saucer,
## floating traffic or a neon skyline into a Helsinki node fails a test instead of shipping.

const DATA_PATH := "res://data/world/helsinki_map.json"

##: Terms that may not appear in a grounded Helsinki node's text. Any retrofuture belongs to occasional
##: specified assets or the later-unlocked HQ underground, never the street.
const FORBIDDEN_TERMS := ["saucer", "ufo", "hover", "flying car", "neon", "skyscraper", "spaceport",
	"maglev", "holo"]

static var _doc: Dictionary = {}


static func _data() -> Dictionary:
	if not _doc.is_empty():
		return _doc
	if not FileAccess.file_exists(DATA_PATH):
		push_error("CityMap: missing %s" % DATA_PATH)
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("CityMap: %s is not valid JSON" % DATA_PATH)
		return {}
	_doc = parsed
	return _doc


static func nodes() -> Array:
	return _data().get("nodes", [])


static func node(id: String) -> Dictionary:
	for entry in nodes():
		if entry.get("id", "") == id:
			return entry
	return {}


static func selectable() -> Array:
	## The only nodes the player may travel to right now.
	return nodes().filter(func(n): return bool(n.get("unlocked", false)))


static func selectable_ids() -> Array:
	return selectable().map(func(n): return String(n["id"]))


static func start_nodes() -> Array:
	return _data().get("start_nodes", [])


static func can_travel(id: String) -> bool:
	var entry := node(id)
	if entry.is_empty():
		return false
	return bool(entry.get("unlocked", false))


static func travel(id: String) -> Dictionary:
	## A locked node is refused with the reason, so a UI can say why instead of doing nothing.
	if node(id).is_empty():
		return {"ok": false, "reason": "unknown location: %s" % id}
	if not can_travel(id):
		return {"ok": false, "reason": "location not yet discovered: %s" % id}
	return {"ok": true, "node": node(id)}


static func forbidden_terms_in_text() -> Array:
	## Scan the human-facing text of every node for terms that break the grounding contract.
	var found: Array = []
	for entry in nodes():
		var text := JSON.stringify(entry).to_lower()
		for term in FORBIDDEN_TERMS:
			if text.contains(term):
				found.append("%s: %s" % [entry.get("id", "?"), term])
	return found


static func districts() -> Array:
	var seen: Array = []
	for entry in nodes():
		var district := String(entry.get("district", ""))
		if district != "" and not seen.has(district):
			seen.append(district)
	return seen
