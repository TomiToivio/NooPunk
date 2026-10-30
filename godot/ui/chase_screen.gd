## Minimal playable CWN §2.6 pursuit console. All outcomes come from CwnChases.
extends Control

const Chases := preload("res://godot/core/cwn_chases.gd")

var mode_select: OptionButton
var pace_input: SpinBox
var pursuit_input: SpinBox
var hinder_input: SpinBox
var botch_input: SpinBox
var result_label: Label
var last_result: Dictionary = {}

func _ready() -> void:
	var panel := VBoxContainer.new()
	panel.set_anchors_preset(Control.PRESET_CENTER)
	panel.position = Vector2(90, 65)
	panel.custom_minimum_size = Vector2(550, 450)
	add_child(panel)
	var title := Label.new()
	title.text = "CWN §2.6 — Chases and pursuit"
	panel.add_child(title)
	mode_select = OptionButton.new()
	mode_select.add_item("Foot chase")
	mode_select.add_item("Vehicle chase (one pursuer)")
	panel.add_child(mode_select)
	pace_input = _number(panel, "Fugitive Exert / Drive total", 10)
	pursuit_input = _number(panel, "Pursuer Exert / Drive total", 10)
	hinder_input = _number(panel, "Successful hindrances (foot only)", 0)
	botch_input = _number(panel, "Botched hindrances (foot only)", 0)
	var go := Button.new()
	go.text = "Resolve pursuit"
	go.pressed.connect(_resolve)
	panel.add_child(go)
	result_label = Label.new()
	result_label.text = "Enter the check totals, then resolve."
	panel.add_child(result_label)
	var back := Button.new()
	back.text = "Back to menu"
	back.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://scenes/main.tscn"))
	panel.add_child(back)

func _number(panel: VBoxContainer, caption: String, initial: int) -> SpinBox:
	var label := Label.new()
	label.text = caption
	panel.add_child(label)
	var input := SpinBox.new()
	input.min_value = -30
	input.max_value = 100
	input.step = 1
	input.value = initial
	panel.add_child(input)
	return input

func resolve_values(vehicle: bool, fugitive: int, pursuer: int, hindrances: int = 0, botches: int = 0) -> Dictionary:
	if vehicle:
		return Chases.vehicle(fugitive, [pursuer])
	return Chases.foot(fugitive, pursuer, hindrances, botches)

func _resolve() -> void:
	var vehicle := mode_select.selected == 1
	last_result = resolve_values(vehicle, int(pace_input.value), int(pursuit_input.value), int(hinder_input.value), int(botch_input.value))
	if not bool(last_result.get("ok", false)):
		result_label.text = "Cannot resolve: %s" % String(last_result.get("reason", "invalid inputs"))
		return
	var caught := bool(last_result["any_caught"]) if vehicle else bool(last_result["caught"])
	result_label.text = "Pursuer catches target." if caught else "Target escapes pursuit."
	result_label.text += "  Pace: %d; modifier: %d." % [int(last_result["pace"]), int(last_result["modifier"])]
