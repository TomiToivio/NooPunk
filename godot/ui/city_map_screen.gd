## Helsinki city map screen (#913).
##
## Two views in one Control: the **map** (only discovered places are drawn — an undiscovered location is
## absent, not greyed out) and a **location menu** once a node is selected.
##
## The map art is not committed yet (#908 has no approved artwork), so the panel is drawn procedurally in
## the token palette and each location reports `art pending` instead of pretending. That is the honest
## placeholder the image contract asks for; swapping in `illustration` later changes nothing else.
##
## Built in `setup()`/`_ensure_build()`, never `_ready()`: a `--script` runner adds nodes before the main
## loop starts, so `_ready` does not fire and a test would measure an empty screen.
extends Control

const CityMap := preload("res://godot/narrative/location_map.gd")

const INK := Color(0.10, 0.086, 0.07)
const BONE := Color(0.91, 0.86, 0.77)
const OCHRE := Color(0.77, 0.54, 0.23)
const OLIVE := Color(0.42, 0.44, 0.23)
const DUSTY := Color(0.34, 0.42, 0.50)
const RUST := Color(0.61, 0.29, 0.17)

var map: Object = null
var flags: Dictionary = {}
var selected: String = ""
var problems: Array = []
##: Scripted beats already played, so the rookie prank happens once and not on every visit.
var beats_played: Array = []

var _built := false
var _map_panel: Control
var _title: Label
var _subtitle: Label
var _detail: RichTextLabel
var _actions: VBoxContainer
var _back_button: Button
var _nodes: Dictionary = {}


func setup(city_flags: Dictionary = {}) -> void:
	flags = city_flags.duplicate()
	map = CityMap.helsinki()
	_ensure_build()
	_show_map()


func _ready() -> void:
	if not _built:
		_ensure_build()
		_show_map()


func _ensure_build() -> void:
	if _built:
		return
	_built = true
	if map == null:
		map = CityMap.helsinki()
	set_anchors_preset(Control.PRESET_FULL_RECT)

	var background := ColorRect.new()
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	background.color = INK
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	_title = Label.new()
	_title.position = Vector2(24, 16)
	_title.add_theme_font_size_override("font_size", 26)
	_title.text = "Helsinki — January 1975"
	add_child(_title)

	_subtitle = Label.new()
	_subtitle.position = Vector2(24, 48)
	_subtitle.text = "Two places you know. The rest of the city is not on this map yet."
	add_child(_subtitle)

	_map_panel = Control.new()
	_map_panel.position = Vector2(24, 80)
	_map_panel.custom_minimum_size = Vector2(640, 480)
	_map_panel.clip_contents = true
	add_child(_map_panel)

	_detail = RichTextLabel.new()
	_detail.bbcode_enabled = false
	_detail.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(_detail)

	_actions = VBoxContainer.new()
	add_child(_actions)

	_back_button = Button.new()
	_back_button.text = "Back to the map"
	_back_button.visible = false
	_back_button.pressed.connect(_show_map)
	add_child(_back_button)


func _viewport() -> Vector2:
	var size := get_viewport_rect().size
	return size if size.x > 0.0 else Vector2(1280, 720)


func _show_map() -> void:
	selected = ""
	_back_button.visible = false
	_map_panel.visible = true
	_detail.visible = false
	_actions.visible = false
	_subtitle.text = "Two places you know. The rest of the city is not on this map yet."
	_rebuild_nodes()


## (Re)draw one button per visible node, positioned by its normalized coordinates.
func _rebuild_nodes() -> void:
	for node_id in _nodes.keys():
		var button: Button = _nodes[node_id]
		button.queue_free()
	_nodes.clear()
	for node in map.visible(flags):
		var node_id := String(node.get("id", ""))
		var button := Button.new()
		button.text = _marker_text(node, node_id)
		button.custom_minimum_size = Vector2(190, 34)
		var position: Array = node.get("position", [0.5, 0.5])
		var panel := _panel_rect()
		button.position = Vector2(
			panel.position.x + float(position[0]) * panel.size.x - 95.0,
			panel.position.y + float(position[1]) * panel.size.y - 17.0)
		button.pressed.connect(_open_location.bind(node_id))
		add_child(button)
		_nodes[node_id] = button


func _panel_rect() -> Rect2:
	return Rect2(_map_panel.position, Vector2(
		minf(_viewport().x - 360.0, 720.0),
		minf(_viewport().y - 140.0, 520.0)))


func _marker_text(node: Dictionary, node_id: String) -> String:
	var name := String(node.get("name", node_id))
	if map.has_visited(node_id):
		return "● " + name
	return "○ " + name


func _open_location(node_id: String) -> void:
	selected = node_id
	_map_panel.visible = false
	_back_button.visible = true
	_detail.visible = true
	_actions.visible = true

	var node: Dictionary = map.nodes[node_id]
	var travel: Dictionary = map.travel_to(node_id, flags)
	if not bool(travel.get("ok", false)):
		problems.append("travel refused: " + String(travel.get("reason", "?")))
		_show_map()
		return

	var lines: Array = []
	lines.append(String(node.get("name", node_id)))
	lines.append(String(node.get("district", "")))
	lines.append("")
	lines.append(String(node.get("description", "")))
	lines.append("")
	var illustration := String(node.get("illustration", ""))
	if illustration.is_empty() or not ResourceLoader.exists(illustration):
		lines.append("[art pending: %s]" % illustration.get_file() if not illustration.is_empty()
			else "[no illustration assigned]")
	_detail.text = "\n".join(lines)

	_detail.position = Vector2(_panel_rect().position.x, _panel_rect().position.y + _panel_rect().size.y + 12.0)
	_detail.size = Vector2(minf(_viewport().x - 48.0, 760.0), 150.0)
	_actions.position = Vector2(_detail.position.x + _detail.size.x + 16.0, _detail.position.y)
	_actions.custom_minimum_size = Vector2(200, 150)
	_back_button.position = Vector2(_detail.position.x, _detail.position.y + _detail.size.y + 8.0)

	for child in _actions.get_children():
		_actions.remove_child(child)
		child.free()
	for action in map.actions_at(node_id, flags):
		var button := Button.new()
		button.text = String(action).replace("_", " ")
		button.pressed.connect(_on_action.bind(node_id, String(action)))
		_actions.add_child(button)

	_maybe_play_rookie_welcome(node_id)


## The rookie-in-uniform prank: a scripted beat on the first HQ visit, not a random event.
func _maybe_play_rookie_welcome(node_id: String) -> void:
	if node_id != "unsa_hq_ratakatu" or beats_played.has("rookie_uniform"):
		return
	beats_played.append("rookie_uniform")
	_detail.text += "\n\n" + ("Reception, ground floor. Every agent in the room is in civilian clothes. "
		+ "You are not. A veteran looks up from a paper folder, takes in the uniform, and says, entirely "
		+ "without malice: «Ah. First day.» The room returns to its paperwork. Somebody at the back is "
		+ "smiling into a coffee cup.")


func _on_action(node_id: String, action: String) -> void:
	# The screen invents no outcomes. These are stubs, and they say so.
	match action:
		"inspect_boxes":
			_append_action("Boxes: kitchen things, three books, a coat that is not warm enough for January.")
		"rest":
			_append_action("You sleep. The trams start again at five.")
		"check_comms":
			_append_action("Agency channel: nothing, then a test tone, then nothing.")
		"reception":
			_append_action("Reception smiles. Three badge colours hang behind the desk.")
		"briefing":
			_append_action("Briefing room booked. The projector does not work. It never has.")
		"rookie_welcome":
			_append_action("You have already been welcomed.")
		_:
			_append_action("%s: no scene wired yet" % String(action).replace("_", " "))


func _append_action(line: String) -> void:
	if _detail != null:
		_detail.text += "\n\n" + line


# ---- persistence ---------------------------------------------------------------------------------

func save_state() -> Dictionary:
	var state: Dictionary = map.to_dict()
	state["beats_played"] = beats_played.duplicate()
	state["selected"] = selected
	return state


func load_state(state: Dictionary) -> void:
	map = CityMap.from_dict(state)
	beats_played = []
	for beat in Array(state.get("beats_played", [])):
		beats_played.append(String(beat))
	if _built:
		_show_map()
