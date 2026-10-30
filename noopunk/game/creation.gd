extends Control

## Character creation for a UNSA agent straight from the academy (#835).
##
## Seven attributes, each rolled as 3d6 and shown as the converted signed value. Roll again rerolls the
## whole set; Continue enters the walking scene. Nothing else is chosen here - no skills, equipment,
## specialisation or background, because the issue specifies none.

const MAIN_SCENE := "res://main.tscn"

var _rng := RandomNumberGenerator.new()
var _rows: VBoxContainer
var _values: Dictionary = {}

func _ready() -> void:
	_rng.randomize()
	var root := VBoxContainer.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_theme_constant_override("separation", 6)
	root.position = Vector2(24, 16)
	# The layout is driven by anchors and the container itself; assigning `size` here makes Godot
	# refuse the layout ("container-managed"), which silently left the screen empty.
	root.custom_minimum_size = Vector2(592, 328)
	add_child(root)

	var title := Label.new()
	title.text = "UNSA agent - fresh from the academy"
	root.add_child(title)

	var premise := Label.new()
	premise.text = NoopunkAttributes.premise()
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
	var rolled := NoopunkAttributes.roll(_rng)
	_values = NoopunkAttributes.sheet(rolled)
	# Autoloads do not exist when the project is run with `--script` (the headless checks), so the
	# lookup is guarded; in the running game the singleton is always there.
	var sheet := get_node_or_null("/root/Sheet")
	if sheet != null:
		sheet.set_roll(rolled)
	_render()

func _render() -> void:
	# Freed immediately rather than queued: `row_count()` is asserted by the headless check, and a
	# queued free would leave the previous rows visible to it until the next idle frame.
	for child in _rows.get_children():
		_rows.remove_child(child)
		child.free()
	for definition in NoopunkAttributes.attribute_definitions():
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
