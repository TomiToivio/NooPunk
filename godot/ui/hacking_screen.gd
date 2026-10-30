## Playable node-link hacking screen (CWN SRD §4.5, over the §4.2 kernel).
##
## The rules were already implemented in `godot/core/hacking.gd`; what was missing was any way for a
## player to *reach* them. This screen is presentation and input only — every legality decision
## (reachability, Access, CPU, the 2d6 check, the alert clock) is asked of the kernel, never re-derived
## here. If a verb is refused, the refusal is the kernel's own `reason` string.
##
## Layout comes from the network data: each node may carry `pos: [col, row]`; nodes without one are laid
## out in reading order. Links are drawn between node centres.
extends Control

const Hacking := preload("res://godot/core/hacking.gd")

const CELL := Vector2(150, 96)
const MARGIN := Vector2(28, 36)
const NODE_SIZE := Vector2(124, 60)

var kernel: Object = null
var network: Dictionary = {}
var deck_spec: Dictionary = {}

var _built := false
var _nodes_layer: Control
var _status: Label
var _log_label: RichTextLabel
var _verbs_panel: VBoxContainer
var _verbs_title: Label
var _buttons: Dictionary = {}      # node_id -> Button
var _selected := ""


## Bind a rules adapter, a network and a deck, then build the screen.
##
## Building here rather than in `_ready` is deliberate: a `--script` runner adds nodes before the main
## loop starts, so `_ready` does not run and a screen that waits for it would look empty to every test.
func setup(rules_adapter: Object, network_data: Dictionary, deck: Dictionary) -> void:
	network = network_data
	deck_spec = deck
	kernel = Hacking.new(rules_adapter, network_data, deck)
	_build()
	_refresh()


## Open the network recorded in a mission file. Used by the menu so the screen is reachable without a
## scenario author wiring it up; the mission's `network` and `deck` are the scenario's own data.
func open_mission(path: String, roll_seed: int = 1) -> bool:
	var text := FileAccess.get_file_as_string(path)
	if text.is_empty():
		return false
	var parsed: Variant = JSON.parse_string(text)
	if not (parsed is Dictionary):
		return false
	var mission: Dictionary = parsed
	if not mission.has("network"):
		return false
	var adapter: Object = load("res://godot/core/rules_adapter.gd").new(
		"res://data/rules/wn_core.json", roll_seed)
	setup(adapter, Dictionary(mission["network"]), Dictionary(mission.get("deck", {})))
	return true


func _ready() -> void:
	if not _built:
		_build()
		_refresh()


func _build() -> void:
	if _built:
		return
	_built = true
	set_anchors_preset(Control.PRESET_FULL_RECT)

	var background := ColorRect.new()
	background.color = Color(0.04, 0.05, 0.07)
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	_nodes_layer = Control.new()
	_nodes_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_nodes_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_nodes_layer)
	_build_nodes()

	_status = Label.new()
	_status.position = Vector2(MARGIN.x, 6)
	_status.add_theme_color_override("font_color", Color(0.55, 0.85, 0.95))
	add_child(_status)

	_verbs_title = Label.new()
	_verbs_title.text = "Select a node"
	_verbs_title.position = Vector2(MARGIN.x, _canvas_size().y - 210)
	add_child(_verbs_title)

	_verbs_panel = VBoxContainer.new()
	_verbs_panel.position = Vector2(MARGIN.x, _canvas_size().y - 186)
	_verbs_panel.custom_minimum_size = Vector2(240, 120)
	add_child(_verbs_panel)

	_log_label = RichTextLabel.new()
	_log_label.bbcode_enabled = true
	_log_label.position = Vector2(_canvas_size().x - 320, 40)
	_log_label.custom_minimum_size = Vector2(300, 260)
	_log_label.scroll_active = true
	add_child(_log_label)


## Grid position for a node: explicit `pos` wins, otherwise reading order by key.
func _canvas_size() -> Vector2:
	return size if size.x > 1.0 else Vector2(1152, 648)


func _node_position(node_id: String, index: int) -> Vector2:
	var node: Dictionary = network.get("nodes", {}).get(node_id, {})
	var pos: Array = node.get("pos", [])
	var col := index % 4
	var row := index / 4
	if pos.size() >= 2:
		col = int(pos[0])
		row = int(pos[1])
	return MARGIN + Vector2(col * CELL.x, row * CELL.y) + Vector2(0, 24)


func _build_nodes() -> void:
	for child in _nodes_layer.get_children():
		child.queue_free()
	_buttons.clear()
	var ids: Array = network.get("nodes", {}).keys()
	for index in ids.size():
		var node_id := String(ids[index])
		var button := Button.new()
		button.text = node_id
		button.size = NODE_SIZE
		button.position = _node_position(node_id, index)
		button.pressed.connect(_on_node_pressed.bind(node_id))
		_nodes_layer.add_child(button)
		_buttons[node_id] = button
	_draw_links(ids)


func _draw_links(ids: Array) -> void:
	var drawn: Dictionary = {}
	for node_id in ids:
		var node: Dictionary = network["nodes"][node_id]
		for link in node.get("links", []):
			var other := String(link)
			var key := "%s|%s" % [node_id, other]
			var reverse := "%s|%s" % [other, node_id]
			if drawn.has(key) or drawn.has(reverse) or not _buttons.has(other):
				continue
			drawn[key] = true
			var line := Line2D.new()
			var a: Button = _buttons[node_id]
			var b: Button = _buttons[other]
			line.points = PackedVector2Array([
				a.position + NODE_SIZE * 0.5,
				b.position + NODE_SIZE * 0.5,
			])
			line.width = 2.0
			line.default_color = Color(0.35, 0.55, 0.75, 0.55)
			line.z_index = -1
			_nodes_layer.add_child(line)


func _on_node_pressed(node_id: String) -> void:
	if kernel == null:
		return
	_selected = node_id
	if not kernel.is_node_connected(node_id):
		var result: Dictionary = kernel.connect_node(node_id)
		if not bool(result.get("ok", false)):
			_append_log("connect %s refused: %s" % [node_id, String(result.get("reason", "?"))])
		else:
			_append_log("connected to %s (cpu %d, access %d)" % [node_id, int(result["cpu"]), int(result["access"])])
	_refresh()


func _on_verb_pressed(node_id: String, verb: String) -> void:
	if kernel == null:
		return
	if not kernel.is_node_connected(node_id):
		_append_log("%s is not connected" % node_id)
		return
	var result: Dictionary = kernel.act(node_id, verb)
	if not bool(result.get("ok", kernel.done(node_id, verb))):
		_append_log("%s/%s refused: %s" % [node_id, verb, String(result.get("reason", "?"))])
	elif bool(result.get("success", false)):
		_append_log("%s/%s succeeded" % [node_id, verb])
	else:
		_append_log("%s/%s failed (alert %d)" % [node_id, verb, int(result.get("alert_actions", 0))])
	_refresh()


func _refresh() -> void:
	if kernel == null:
		return
	for node_id in _buttons:
		var button: Button = _buttons[node_id]
		var connected: bool = kernel.is_node_connected(node_id)
		button.modulate = Color(0.55, 1.0, 0.65) if connected else Color(0.82, 0.82, 0.9)
		button.disabled = bool(kernel.alarm)
	var deck: Dictionary = kernel.deck
	var alert_text := "ALARM" if bool(kernel.alarm) else "alert %d/2" % int(kernel.alert_actions)
	_status.text = "CPU %d/%d   Access %d   failures %d   %s" % [
		int(deck["cpu"]), int(deck["cpu_max"]), int(deck["access"]), int(kernel.failures), alert_text]
	_status.add_theme_color_override("font_color", Color(1.0, 0.45, 0.45) if bool(kernel.alarm) else Color(0.55, 0.85, 0.95))
	_refresh_verbs()


func _refresh_verbs() -> void:
	# Free immediately rather than `queue_free()`: the screen is also built outside the scene tree (a
	# headless suite constructs it, presses buttons and inspects it), and `queue_free()` on a tree-less
	# node errors with "Cannot get path of node as it is not in a scene tree" and never actually frees —
	# which is where #883's 15 leaked CanvasItem RIDs and ~67 ObjectDB instances came from.
	for child in _verbs_panel.get_children():
		_verbs_panel.remove_child(child)
		child.free()
	if _selected.is_empty():
		_verbs_title.text = "Select a node"
		return
	_verbs_title.text = "%s — %s" % [_selected, "connected" if kernel.is_node_connected(_selected) else "reach it first"]
	var node: Dictionary = network.get("nodes", {}).get(_selected, {})
	for verb in node.get("verbs", []):
		var button := Button.new()
		button.text = String(verb) + ("  (done)" if kernel.done(_selected, String(verb)) else "")
		button.pressed.connect(_on_verb_pressed.bind(_selected, String(verb)))
		_verbs_panel.add_child(button)


func _append_log(message: String) -> void:
	if _log_label == null:
		return
	_log_label.append_text(message + "\n")
