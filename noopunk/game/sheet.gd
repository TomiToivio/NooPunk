extends CanvasLayer
## Displays the generated agent. R rolls a new one; everything else is static.

@onready var _title: Label = $Panel/VBox/Title
@onready var _body: Label = $Panel/VBox/Body
@onready var _hint: Label = $Panel/VBox/Hint


func _ready() -> void:
	_roll()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_R:
		_roll()


func _roll() -> void:
	var rows := Agent.roll_sheet()
	_title.text = "UNSA AGENT — ACADEMY GRADUATE"
	var lines := PackedStringArray()
	for row in rows:
		lines.append("%-10s %s" % [row[0], Agent.signed(row[2])])
	_body.text = "\n".join(lines)
	_hint.text = "R — roll a new agent   ·   WASD / arrows — move"
