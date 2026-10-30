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

	# A finished case leaves GameState holding its ending; the autoload must be reset for a new run,
	# otherwise "Begin" silently resumes the old case with all its evidence.
	if FileAccess.file_exists("user://save_lakkahaltia.json"):
		var resume := Button.new()
		resume.text = "Continue the saved case"
		resume.pressed.connect(_on_resume_pressed)
		stack.add_child(resume)

	# #749: the vertical slice is launched from the same menu rather than replacing the case.
	var mvp := Button.new()
	mvp.text = "Romppainen — MVP (home → HQ → mission)"
	mvp.pressed.connect(func() -> void:
		get_tree().change_scene_to_file("res://godot/ui/mvp_game.tscn"))
	stack.add_child(mvp)

	# The campaign is an existing feature of the same root Godot project.
	# Keep it accessible here rather than requiring agents to maintain a rival title scene.
	var campaign := Button.new()
	campaign.text = "Campaign prototype (home / UNSA HQ)"
	campaign.pressed.connect(func() -> void:
		get_tree().change_scene_to_file("res://scenes/campaign.tscn"))
	stack.add_child(campaign)

	var controls := Label.new()
	controls.text = "WASD move · mouse look · E interact · J journal · F5 save · F6 end the case"
	controls.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	controls.modulate = Color(0.65, 0.68, 0.74)
	stack.add_child(controls)

func _on_start_pressed() -> void:
	GameState.new_case(GameState.run_seed)
	get_tree().change_scene_to_file("res://godot/scenes/hospital.tscn")

func _on_resume_pressed() -> void:
	GameState.new_case(GameState.run_seed)
	var err: int = GameState.load_from_file()
	if err != OK:
		push_error("main_menu: could not load the saved case (%d)" % err)
	get_tree().change_scene_to_file("res://godot/scenes/hospital.tscn")
