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
var _message := ""
var _built := false


func _ready() -> void:
	build()


## Build the network and the widgets. Separate from `_ready` so a headless test can drive the screen in
## the same frame it instantiates it, instead of waiting for the tree to tick.
func build() -> void:
	if _built:
		return
	_built = true
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


## Load a mission's recorded network and rebuild the screen around it.
##
## The mission stores nodes keyed by id with `security`, `verbs` and `links`; this screen's subject model
## is the SRD's, so each node's verbs pick the Subject it exposes. A file that cannot be read leaves the
## current network untouched rather than showing an empty screen.
func open_mission(path: String, int_modifier: int = 2, program_rank: int = 2, deck_bonus: int = 1) -> bool:
	var text := FileAccess.get_file_as_string(path)
	if text.is_empty():
		return false
	var parsed: Variant = JSON.parse_string(text)
	if not (parsed is Dictionary) or not Dictionary(parsed).has("network"):
		return false
	var network: Dictionary = Dictionary(parsed)["network"]
	var nodes: Array = []
	for node_id in Dictionary(network.get("nodes", {})).keys():
		var row: Dictionary = Dictionary(network["nodes"][node_id])
		var subject := "Datafile"
		for verb in Array(row.get("verbs", [])):
			if String(verb) == "control":
				subject = "Device"
			elif String(verb) == "query":
				subject = "Datafile"
		nodes.append(NodeLink.node(String(node_id), String(node_id).capitalize(),
			int(row.get("security", 7)), subject, Array(row.get("links", []))))
	if nodes.is_empty():
		return false
	net = NodeLink.network(nodes, String(network.get("entry", nodes[0]["id"])))
	_int_modifier = int_modifier
	_program_rank = program_rank
	_deck_bonus = deck_bonus
	if not _built:
		_built = true
		_build_ui()
	_message = "Loaded " + path.get_file()
	_refresh()
	return true


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
	elif bool(result.get("success", false)):
		_message = ""
	_sync_subject_to_node()
	_sync_verb_to_node()
	_refresh()


func _on_run() -> void:
	var verb_name := _verbs.get_item_text(_verbs.selected)
	var subject_name := _subjects.get_item_text(_subjects.selected)
	var dice := [_rng.randi_range(1, 6), _rng.randi_range(1, 6)]
	var result := NodeLink.run_verb(net, verb_name, subject_name, dice, _int_modifier, _program_rank)
	if result.has("error"):
		_flash(String(result["error"]))
	_refresh()


## Point the Subject dropdown at what the current node actually exposes.
##
## `run_verb` acts on the current node, so a dropdown left on the catalogue's first entry guarantees the
## player's first Run is refused with a reason that does not say what was wanted.
func _sync_subject_to_node() -> void:
	if _subjects == null:
		return
	var current := String(net.get("current", ""))
	var wanted := ""
	for node in net.get("nodes", []):
		if String(node.get("id", "")) == current:
			wanted = String(node.get("subject", ""))
			break
	if wanted.is_empty():
		return
	for index in _subjects.item_count:
		if _subjects.get_item_text(index) == wanted:
			_subjects.select(index)
			return


## Point the Verb dropdown at something the node's Subject actually allows.
##
## Same defect as the Subject default: the catalogue's first Verb need not be able to target the
## Subject on the node, so the player's first click was refused for a reason they could not act on.
func _sync_verb_to_node() -> void:
	if _verbs == null or _subjects == null:
		return
	var subject_name := _subjects.get_item_text(_subjects.selected)
	var subject: Dictionary = NodeLink.subjects().get(subject_name, {})
	if subject.is_empty():
		return
	var wanted_type := String(subject.get("subject_type", ""))
	for index in _verbs.item_count:
		var verb: Dictionary = NodeLink.verbs().get(_verbs.get_item_text(index), {})
		if Array(verb.get("target_types", [])).has(wanted_type):
			_verbs.select(index)
			return


func _flash(message: String) -> void:
	## Kept in state rather than written straight to the label: `_refresh()` runs immediately after and
	## would overwrite it, so the player never saw why an attempt was refused.
	_message = "Refused: " + message.replace("_", " ")


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
	_status.text = "Access %d   Alert %d   %s%s" % [int(net.get("access", 0)), int(net.get("alert", 0)),
		"connected" if bool(net.get("jacked_in", false)) else "disconnected",
		("   — " + _message) if not _message.is_empty() else ""]
	var log: Array = net.get("log", [])
	_log.text = "\n".join(log.slice(maxi(0, log.size() - 6)))
