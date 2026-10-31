## Location screen — the first playable surface of the narrative campaign (#897 §4).
##
## Presentation and input only. The map, the notebook and the palette decide everything; this screen asks
## them and draws the answer. If a rule is enforced here instead of in the model, it is in the wrong place.
##
## Built in `setup()` rather than `_ready()` for the same reason every other screen in this project is:
## a `--script` runner adds nodes before the main loop starts, so `_ready` never fires and a test would see
## an empty screen while a window showed a full one.
extends Control

const Map := preload("res://godot/narrative/location_map.gd")
const Notebook := preload("res://godot/narrative/investigation.gd")
const Tokens := preload("res://godot/ui/noopunk_theme.gd")

var map: Object = null
var book: Object = null
var flags: Dictionary = {}

var _built := false
var _title: Label
var _district: Label
var _actions: VBoxContainer
var _travel: VBoxContainer
var _log: RichTextLabel
var _clues: Label
var _status: Label
var _description: Label


func setup(location_map: Object, notebook: Object, campaign_flags: Dictionary = {}) -> void:
	map = location_map
	book = notebook
	flags = campaign_flags
	_build()
	_refresh()


func _ready() -> void:
	if not _built:
		_build()
		_refresh()


func _build() -> void:
	if _built:
		return
	_built = true
	set_anchors_preset(Control.PRESET_FULL_RECT)

	var theme_builder := Tokens.new()
	theme = theme_builder.build()

	var background := ColorRect.new()
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	background.color = theme_builder.color("ink")
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	_title = Label.new()
	_title.position = Vector2(24, 18)
	_title.add_theme_font_size_override("font_size", 28)
	add_child(_title)

	_district = Label.new()
	_district.position = Vector2(24, 52)
	add_child(_district)

	_status = Label.new()
	_status.position = Vector2(24, 78)
	add_child(_status)

	_actions = VBoxContainer.new()
	_description = Label.new()
	_description.position = Vector2(24, 112)
	_description.custom_minimum_size = Vector2(320, 110)
	_description.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(_description)

	_actions.position = Vector2(24, 238)
	_actions.custom_minimum_size = Vector2(320, 200)
	add_child(_actions)

	_travel = VBoxContainer.new()
	_travel.position = Vector2(380, 120)
	_travel.custom_minimum_size = Vector2(300, 240)
	add_child(_travel)

	_clues = Label.new()
	_clues.position = Vector2(380, 380)
	_clues.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_clues.custom_minimum_size = Vector2(300, 80)
	add_child(_clues)

	_log = RichTextLabel.new()
	_log.position = Vector2(24, 480)
	_log.custom_minimum_size = Vector2(660, 140)
	_log.bbcode_enabled = false
	_log.scroll_active = true
	add_child(_log)


func _refresh() -> void:
	if map == null:
		return
	var node: Dictionary = map.nodes.get(map.current, {})
	_title.text = String(node.get("name", "unknown place"))
	_district.text = String(node.get("district", ""))
	_description.text = String(node.get("description", ""))
	_status.text = "visited %d · clues %d" % [map.visited.size(), book.count() if book else 0]
	_clues.text = "leads: " + (", ".join(book.open_leads()) if book and book.open_leads().size() > 0
		else "none")

	# Free immediately, not deferred: `queue_free()` waits for the frame to end, so a rebuild in the same
	# frame leaves the old buttons in place beside the new ones and every list doubles.
	for child in _actions.get_children():
		_actions.remove_child(child)
		child.free()
	for action in map.actions_at(map.current, flags):
		var button := Button.new()
		button.text = String(action)
		button.pressed.connect(_on_action.bind(String(action)))
		_actions.add_child(button)

	for child in _travel.get_children():
		_travel.remove_child(child)
		child.free()
	var heading := Label.new()
	heading.text = "Travel"
	_travel.add_child(heading)
	# Undiscovered nodes are not instantiated at all. Even greyed-out labels would spoil the story.
	for place in map.visible(flags):
		var button := Button.new()
		button.text = "%s (%s)" % [String(place.get("name", "")), String(place.get("district", ""))]
		button.disabled = String(place.get("id", "")) == map.current
		button.pressed.connect(_on_travel.bind(String(place.get("id", ""))))
		_travel.add_child(button)


func _on_travel(node_id: String) -> void:
	var result: Dictionary = map.travel_to(node_id, flags)
	if not bool(result.get("ok", false)):
		_append("cannot travel: " + String(result.get("reason", "?")))
	else:
		_append("arrived at " + String(map.nodes[node_id].get("name", node_id)))
	_refresh()


func _on_action(action: String) -> void:
	# The screen does not invent outcomes. An action either has a model behind it or it is a placeholder,
	# and placeholders say so rather than pretending something happened.
	match action:
		"inspect_apartment":
			_append("You moved into this UNSA flat yesterday. Half-unpacked boxes; Helsinginkatu murmurs outside.")
		"check_messages":
			_append("The welcome packet contains three incompatible agency letterheads.")
		"reception":
			_append("A friendly clerk asks whether your badge is Supo, Europol or UNSA. Nobody agrees which form applies.")
		"rookie_welcome":
			_append("Romppainen's eyes twinkle: only the rookie wears that spectacular new UNSA uniform.")
			flags["met_romppainen"] = true
			flags["knows_putki"] = true
		"briefing":
			_append("The case points toward researchers at the University of Helsinki.")
			flags["knows_university"] = true
			flags["knows_kurvi"] = true
		"case_board":
			_append("Romppainen recommends his regular, Olutravintola Putki, near the university.")
			flags["knows_putki"] = true
		"journal":
			_append("The notebook awaits your first Helsinki investigation.")
		"explore":
			_append("A local contact mentions Kurvi, the bohemian crossroads up the street.")
			flags["knows_kurvi"] = true
		"investigate":
			_append("investigation: pick a lead in the notebook (not yet wired to a scene)")
		"interview":
			_append("interview: dialogue runner not yet wired to this screen")
		"rest", "recover":
			_append("recovered at " + String(map.nodes[map.current].get("name", "")))
		"travel":
			_append("choose a destination from the travel list")
		_:
			_append("%s: no model wired yet" % action)
	_refresh()


func _append(line: String) -> void:
	if _log != null:
		_log.append_text(line + "\n")
