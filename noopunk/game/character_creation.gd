extends Control

## Character creation: roll seven 3d6 values, see each converted attribute, then walk into the game.
##
## The UNSA rookie premise is the whole of the character concept at this step: no specialisation, no
## profession, no equipment. Anything more is Tomi's next instruction.

## The rolled sheet lives in an autoload; it is fetched by path rather than by its global name so this
## script also works under `--script` test runs, where autoload identifiers are not registered.
@onready var _state: Node = load("res://character_state.gd").ensure(self)
@onready var _sheet: VBoxContainer = $Panel/Sheet
@onready var _continue: Button = $Panel/Continue
@onready var _reroll: Button = $Panel/Reroll
@onready var _status: Label = $Panel/Status

var _rng := RandomNumberGenerator.new()


func _ready() -> void:
	_rng.randomize()
	_reroll.pressed.connect(_roll)
	_continue.pressed.connect(_continue_to_game)
	if _state.rolls.is_empty():
		_roll()
	else:
		_show()
	_refresh()


func _roll() -> void:
	_state.store(NoopunkAttributes.roll_all(_rng))
	_show()
	_refresh()


func _show() -> void:
	for child in _sheet.get_children():
		child.queue_free()
	for roll in _state.rolls:
		var row := Label.new()
		row.text = "%s   (%d on 3d6)" % [
			NoopunkAttributes.display(String(roll["name"]), int(roll["value"])), int(roll["total"])]
		_sheet.add_child(row)


func _refresh() -> void:
	var range_values := NoopunkAttributes.human_range()
	_status.text = "UNSA agent, fresh from the academy. Human range %d to %+d. Seven rolls of 3d6." % [
		int(range_values[0]), int(range_values[1])]
	_continue.disabled = not _state.is_complete()


func _continue_to_game() -> void:
	get_tree().change_scene_to_file("res://main.tscn")
