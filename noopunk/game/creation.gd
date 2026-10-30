extends Control

## Character creation for a UNSA agent straight from the academy (#835).
##
## Seven attributes, each rolled as 3d6 and shown as the converted signed value. Roll again rerolls the
## whole set; Continue enters the walking scene. Nothing else is chosen here - no skills, equipment,
## specialisation or background, because the issue specifies none.

const MAIN_SCENE := "res://main.tscn"
## Preloaded rather than referenced by the global class name: the global class cache only exists after
## an import pass, so without this the screen cannot build on a clean checkout.
const Attributes := preload("res://attributes.gd")

var _rng := RandomNumberGenerator.new()
var _rows: VBoxContainer
var _values: Dictionary = {}

func _ready() -> void:
	_rng.randomize()
	var root := VBoxContainer.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_theme_constant_override("separation", 6)
	# Offsets, not `position`/`size`: with a full-rect preset the container's size is managed by the
	# anchor layout and any explicit size is overridden after `_ready()`.
	root.offset_left = 24
	root.offset_top = 16
	root.offset_right = -24
	root.offset_bottom = -16
	add_child(root)

	var title := Label.new()
	title.text = "UNSA agent - fresh from the academy"
	root.add_child(title)

	var premise := Label.new()
	premise.text = Attributes.premise()
	premise.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	root.add_child(premise)

	_rows = VBoxContainer.new()
	root.add_child(_rows)

	var buttons := HBoxContainer.new()
	root.add_child(buttons)

	var roll_button := Button.new()
	roll_button.text = "Roll 3d6 x7"
	roll_button.pressed.connect(_on_roll)
	buttons.add_child(roll_button)

	var continue_button := Button.new()
	continue_button.text = "Continue"
	continue_button.pressed.connect(_on_continue)
	buttons.add_child(continue_button)

	_on_roll()

func _on_roll() -> void:
	var rolled := Attributes.roll(_rng)
	_values = Attributes.sheet(rolled)
	# Autoloads do not exist when the project is run with `--script` (the headless checks), so the
	# lookup is guarded; in the running game the singleton is always there.
	var sheet := get_node_or_null("/root/Sheet")
	if sheet != null:
		sheet.set_roll(rolled)
	_render()

func _render() -> void:
	for child in _rows.get_children():
		child.queue_free()
	for definition in Attributes.attribute_definitions():
		var name := str(definition.get("name", ""))
		var value := int(_values.get(name, 0))
		var row := Label.new()
		row.text = "%-12s %s%d      %s" % [name, "+" if value >= 0 else "", value,
			str(definition.get("definition", ""))]
		_rows.add_child(row)

## The values currently on the sheet, for the headless check.
func sheet_values() -> Dictionary:
	return _values.duplicate()

## How many attribute rows the screen is showing.
func row_count() -> int:
	return _rows.get_child_count() if _rows != null else 0

func _on_continue() -> void:
	get_tree().change_scene_to_file(MAIN_SCENE)
