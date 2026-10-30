extends CanvasLayer
## Displays the generated agent. R rolls a new one; everything else is static.

@onready var _title: Label = $Panel/VBox/Title
@onready var _body: Label = $Panel/VBox/Body
@onready var _hint: Label = $Panel/VBox/Hint
@onready var _continue: Button = $Panel/VBox/Continue
@onready var _reopen: Label = $Reopen


func _ready() -> void:
	_roll()
	if not _continue.pressed.is_connected(continue_to_world):
		_continue.pressed.connect(continue_to_world)


func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed):
		return
	match event.keycode:
		KEY_R:
			if $Panel.visible:
				_roll()
		KEY_ENTER, KEY_KP_ENTER, KEY_SPACE:
			continue_to_world()
		KEY_TAB:
			$Panel.visible = true
			_continue.grab_focus()


func continue_to_world() -> void:
	## The rolled sheet is kept: this only puts it away so the agent can walk.
	var panel := get_node_or_null("Panel")
	if panel != null:
		panel.visible = false
	var reopen := get_node_or_null("Reopen")
	if reopen != null:
		reopen.visible = true


func _roll() -> void:
	var rows := Agent.roll_sheet()
	_title.text = "UNSA AGENT — ACADEMY GRADUATE"
	var lines := PackedStringArray()
	for row in rows:
		lines.append("%-10s %s" % [row[0], Agent.signed(row[2])])
	_body.text = "\n".join(lines)
	_hint.text = "R — roll a new agent   ·   WASD / arrows — move"
