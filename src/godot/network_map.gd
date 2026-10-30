class_name NooPunkNetworkMap
extends Control

## Read-only node/edge presentation. Not a CWN hacking procedure.
## A future, source-verified CWN rules adapter will own all actions.
var graph: Dictionary = {}

func set_graph(value: Dictionary) -> void:
	graph = value.duplicate(true)
	queue_redraw()

func _draw() -> void:
	var nodes: Array = graph.get("nodes", [])
	var edges: Array = graph.get("edges", [])
	var positions: Dictionary = {}
	var font := ThemeDB.fallback_font
	for raw in nodes:
		if typeof(raw) != TYPE_DICTIONARY:
			continue
		var id := str(raw.get("id", ""))
		var location: Array = raw.get("position", [])
		if id.is_empty() or location.size() != 2:
			continue
		positions[id] = Vector2(float(location[0]), float(location[1]))
	for edge in edges:
		if not edge is Array or edge.size() != 2:
			continue
		var a := str(edge[0])
		var b := str(edge[1])
		if positions.has(a) and positions.has(b):
			draw_line(positions[a], positions[b], Color(0.43, 0.75, 0.64), 3.0)
	for raw in nodes:
		if typeof(raw) != TYPE_DICTIONARY:
			continue
		var id := str(raw.get("id", ""))
		if not positions.has(id):
			continue
		var pos: Vector2 = positions[id]
		draw_circle(pos, 24.0, Color(0.09, 0.28, 0.25))
		draw_arc(pos, 24.0, 0.0, TAU, 32, Color(0.55, 0.94, 0.78), 2.0)
		draw_string(font, pos + Vector2(-20, 42), str(raw.get("label", id)), HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color(0.9, 0.96, 0.9))
