extends CanvasLayer

## Minimal character sheet for the UNSA rookie (#835). It rolls seven 3d6 attributes, shows each
## converted modifier, and steps aside so the walking scene continues. The rolled values live on
## this node, so they survive moving around the room until the player rolls again.

const RookieCharacterScript := preload("res://character.gd")

var character: RookieCharacter
var rows: Dictionary = {}
var summary: Label


func _init() -> void:
	character = RookieCharacterScript.new()


func _ready() -> void:
	_build()
	roll()


func _build() -> void:
	var panel := ColorRect.new()
	panel.color = Color(0.05, 0.06, 0.09, 0.92)
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(panel)

	var title := Label.new()
	title.text = "UNSA Academy Graduate"
	title.position = Vector2(24, 18)
	title.add_theme_font_size_override("font_size", 20)
	add_child(title)

	var premise := Label.new()
	premise.text = "Seven attributes, each 3d6 converted to a signed value."
	premise.position = Vector2(24, 44)
	add_child(premise)

	var y := 78
	for id in character.attribute_ids():
		var name_label := Label.new()
		name_label.text = character.label_for(id)
		name_label.position = Vector2(24, y)
		add_child(name_label)

		var value_label := Label.new()
		value_label.position = Vector2(220, y)
		add_child(value_label)
		rows[id] = value_label
		y += 26

	var roll_button := Button.new()
	roll_button.text = "Roll attributes"
	roll_button.position = Vector2(24, y + 10)
	roll_button.pressed.connect(_on_roll)
	add_child(roll_button)

	var continue_button := Button.new()
	continue_button.text = "Continue"
	continue_button.position = Vector2(180, y + 10)
	continue_button.pressed.connect(_on_continue)
	add_child(continue_button)

	summary = Label.new()
	summary.position = Vector2(24, y + 48)
	add_child(summary)


func _on_roll() -> void:
	roll()


func _on_continue() -> void:
	visible = false


## Roll and refresh the displayed sheet. Public so a test can drive it without synthetic clicks.
func roll() -> Dictionary:
	var values := character.roll()
	for id in values:
		if rows.has(id):
			rows[id].text = character.signed(id)
	var human := character.human_range()
	summary.text = "Basic human range %+d to %+d. Above %+d is transhuman." % [human.x, human.y, human.y]
	return values


func values() -> Dictionary:
	if character == null:
		character = RookieCharacterScript.new()
	if character.values.is_empty():
		character.roll()
	return character.values.duplicate()
