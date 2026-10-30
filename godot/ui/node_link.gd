extends Control
## The node-link screen (#869, SRD 4.1–4.5): the one place a player actually decks.
##
## The screen owns nothing about the rules — every legality question and every number comes from
## `CwnNodeLink`, which in turn defers to `CwnHackingRules` and `CwnProgramRules`. That is what lets the
## same run be replayed headlessly in `godot/tests/test_node_link.gd`.

const NodeLink := preload("res://godot/core/cwn_node_link.gd")

var net: Dictionary = {}
var _node_rows: VBoxContainer
var _status: Label
var _log: Label
var _verbs: OptionButton
var _subjects: OptionButton
var _int_modifier := 2
var _program_rank := 2
var _deck_bonus := 1
var _rng := RandomNumberGenerator.new()


func _ready() -> void:
	build()


## Build the network and the widgets. Separate from `_ready` so a headless test can drive the screen in
## the same frame it instantiates it, instead of waiting for the tree to tick.
func build() -> void:
	if not net.is_empty():
		return
	_rng.randomize()
	_build_sample_network()
	_build_ui()
	_refresh()


## A small network that exercises every rule: a low-security entry, a linked mid node and a deep one
## whose Subject is only reachable after both. Scenario data can replace this later; the rules do not
## change with the network.
func _build_sample_network() -> void:
	net = NodeLink.network([
		NodeLink.node("entrance", "Public Terminal", 7, "Camera", ["archive", "conference"]),
		NodeLink.node("archive", "Records Archive", 9, "Datafile", ["vault"]),
		NodeLink.node("conference", "Conference Room", 8, "Camera", []),
		NodeLink.node("vault", "Vault Controller", 12, "Device", []),
	], "entrance")


func _build_ui() -> void:
	var background := ColorRect.new()
	background.color = Color(0.04, 0.05, 0.08, 1.0)
	background.set_anchors_preset(PRESET_FULL_RECT)
	add_child(background)

	var root := VBoxContainer.new()
	root.set_anchors_preset(PRESET_FULL_RECT)
	root.add_theme_constant_override("separation", 6)
	root.offset_left = 20
	root.offset_top = 16
	root.offset_right = -20
	root.offset_bottom = -16
	add_child(root)

	var title := Label.new()
	title.text = "CYBERSPACE — NODE LINK"
	root.add_child(title)

	_status = Label.new()
	root.add_child(_status)

	_node_rows = VBoxContainer.new()
	root.add_child(_node_rows)

	var controls := HBoxContainer.new()
	controls.add_theme_constant_override("separation", 8)
	root.add_child(controls)

	_verbs = OptionButton.new()
	for verb_name in NodeLink.verbs().keys():
		_verbs.add_item(String(verb_name))
	controls.add_child(_verbs)

	_subjects = OptionButton.new()
	for subject_name in NodeLink.subjects().keys():
		_subjects.add_item(String(subject_name))
	controls.add_child(_subjects)

	var run_button := Button.new()
	run_button.text = "Run"
	run_button.pressed.connect(_on_run)
	controls.add_child(run_button)

	var jack_button := Button.new()
	jack_button.text = "Jack in"
	jack_button.pressed.connect(_on_jack_in)
	controls.add_child(jack_button)

	var out_button := Button.new()
	out_button.text = "Disconnect"
	out_button.pressed.connect(_on_disconnect)
	controls.add_child(out_button)

	_log = Label.new()
	_log.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	root.add_child(_log)


func _on_jack_in() -> void:
	var result := NodeLink.jack_in(net, _int_modifier, _program_rank, _deck_bonus)
	if result.has("error"):
		_flash(String(result["error"]))
	_refresh()


func _on_disconnect() -> void:
	NodeLink.disconnect_deck(net, "operator's choice")
	_refresh()


func _on_attempt(node_id: String) -> void:
	var dice := [_rng.randi_range(1, 6), _rng.randi_range(1, 6)]
	var result := NodeLink.attempt_access(net, dice, _int_modifier, _program_rank, node_id,
		_deck_bonus)
	if result.has("error"):
		_flash(String(result["error"]))
	_refresh()


func _on_run() -> void:
	var verb_name := _verbs.get_item_text(_verbs.selected)
	var subject_name := _subjects.get_item_text(_subjects.selected)
	var dice := [_rng.randi_range(1, 6), _rng.randi_range(1, 6)]
	var result := NodeLink.run_verb(net, verb_name, subject_name, dice, _int_modifier, _program_rank)
	if result.has("error"):
		_flash(String(result["error"]))
	_refresh()


func _flash(message: String) -> void:
	_status.text = "Refused: " + message.replace("_", " ")


func _refresh() -> void:
	if _node_rows == null:
		return
	for child in _node_rows.get_children():
		_node_rows.remove_child(child)
		child.free()
	for entry in NodeLink.visible_nodes(net):
		var row := Button.new()
		var marks: Array = []
		if bool(entry["current"]):
			marks.append("you are here")
		if bool(entry["accessed"]):
			marks.append("accessed")
		elif bool(entry["reachable"]):
			marks.append("reachable")
		else:
			marks.append("hidden")
		row.text = "%s  [security %d, %s]  %s" % [entry["name"], int(entry["security"]),
			entry["subject"], ", ".join(marks)]
		row.disabled = bool(entry["accessed"]) or not bool(entry["reachable"]) \
			or not bool(net.get("jacked_in", false))
		var node_id := String(entry["id"])
		row.pressed.connect(func() -> void: _on_attempt(node_id))
		_node_rows.add_child(row)
	_status.text = "Access %d   Alert %d   %s" % [int(net.get("access", 0)), int(net.get("alert", 0)),
		"connected" if bool(net.get("jacked_in", false)) else "disconnected"]
	var log: Array = net.get("log", [])
	_log.text = "\n".join(log.slice(maxi(0, log.size() - 6)))
