## Title screen (#631). The repository's existing `scenes/main.tscn` is kept as the launch scene; this
## script adds the entry points to it rather than replacing its layout, so nothing that was there before
## the slice disappears.
extends Control

func _ready() -> void:
	var stack := get_node_or_null("Center/Stack") as VBoxContainer
	if stack == null:
		push_error("main_menu: the scaffold's Center/Stack container is missing")
		return

	var subtitle := Label.new()
	subtitle.text = "Etsivä Romppainen ja Lakkahaltian Salaisuus — vertical slice"
	subtitle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	subtitle.modulate = Color(0.8, 0.85, 0.95)
	stack.add_child(subtitle)

	var start := Button.new()
	start.text = "Begin the case"
	start.pressed.connect(_on_start_pressed)
	stack.add_child(start)

	var controls := Label.new()
	controls.text = "WASD move · mouse look · E interact · J journal · F5 save · F6 end the case"
	controls.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	controls.modulate = Color(0.65, 0.68, 0.74)
	stack.add_child(controls)

func _on_start_pressed() -> void:
	get_tree().change_scene_to_file("res://godot/scenes/hospital.tscn")
