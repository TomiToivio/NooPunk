extends Node2D
## One minimal character sheet over the existing walking scene.
const Attributes = preload("res://attributes.gd")
var rng := RandomNumberGenerator.new()
var values: Dictionary = {}
var overlay: ColorRect
var entries: VBoxContainer
var sheet_open := true

func _ready() -> void:
	Attributes.ensure_loaded()
	rng.randomize()
	_build_sheet()
	roll_attributes()
	show_sheet(true)

func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_C:
		show_sheet(not sheet_open)
		get_viewport().set_input_as_handled()

func roll_attributes() -> void:
	values = Attributes.roll_character(rng)
	_refresh_sheet()

func _refresh_sheet() -> void:
	if entries == null:
		return
	for child in entries.get_children():
		child.queue_free()
	for i in range(Attributes.NAMES.size()):
		var row := Label.new()
		var name: String = Attributes.NAMES[i]
		row.text = "%s: %s  |  %s" % [name, Attributes.display_value(values[name]), Attributes.DEFINITIONS[i]]
		entries.add_child(row)

func show_sheet(open: bool) -> void:
	# _ready() may not have run yet when a test or an early caller asks for the sheet.
	_build_sheet()
	sheet_open = open
	overlay.visible = open
	$Player.set_physics_process(not open)

func _build_sheet() -> void:
	if overlay != null:
		return
	var layer := CanvasLayer.new()
	layer.name = "CharacterSheetLayer"
	layer.layer = 10
	add_child(layer)
	overlay = ColorRect.new()
	overlay.name = "CharacterSheet"
	overlay.color = Color(0.045, 0.055, 0.09, 0.97)
	layer.add_child(overlay)
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var column := VBoxContainer.new()
	column.position = Vector2(20, 16)
	column.custom_minimum_size = Vector2(600, 0)
	overlay.add_child(column)
	var title := Label.new()
	title.text = "UNSA ACADEMY GRADUATE | CHARACTER SHEET"
	column.add_child(title)
	var info := Label.new()
	info.text = "Roll 3d6 for each attribute; shown values are -3 to +3."
	column.add_child(info)
	entries = VBoxContainer.new()
	column.add_child(entries)
	var reroll := Button.new()
	reroll.text = "Reroll seven attributes"
	reroll.pressed.connect(roll_attributes)
	column.add_child(reroll)
	var continue_button := Button.new()
	continue_button.text = "Continue to test room (C to reopen sheet)"
	continue_button.pressed.connect(func() -> void: show_sheet(false))
	column.add_child(continue_button)
