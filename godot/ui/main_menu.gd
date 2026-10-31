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

	# #878: Alternate node-link interface over the warehouse mission hacking kernel.
	var hacking := Button.new()
	hacking.text = "Hacking — node link (warehouse network)"
	hacking.pressed.connect(func() -> void:
		var screen: Node = load("res://scenes/node_link.tscn").instantiate()
		if not screen.open_mission("res://godot/scenarios/mvp_romppainen/mission.json", 2, 2, 2):
			screen.queue_free()
			return
		get_tree().root.add_child(screen)
		get_tree().current_scene = screen)
	stack.add_child(hacking)

	# #873: CWN chase console via the existing kernel.
	var chase := Button.new()
	chase.text = "CWN — chase and pursuit"
	chase.pressed.connect(func() -> void:
		get_tree().change_scene_to_file("res://scenes/chase_screen.tscn"))
	stack.add_child(chase)

	# #897: location-based narrative mode (Citizen Sleeper-style, CWN underneath, no tactical view).
	var narrative := Button.new()
	narrative.text = "Helsinki — narrative case (no tactical view)"
	narrative.pressed.connect(func() -> void:
		get_tree().change_scene_to_file("res://godot/ui/narrative_screen.tscn"))
	stack.add_child(narrative)

	# #897 §4: the narrative campaign's first playable surface.
	var locations_button := Button.new()
	locations_button.text = "Narrative — Helsinki locations"
	locations_button.pressed.connect(func() -> void:
		var screen: Node = load("res://scenes/narrative/location_screen.tscn").instantiate()
		var map_script: Script = load("res://godot/narrative/location_map.gd")
		var book_script: Script = load("res://godot/narrative/investigation.gd")
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(
			"res://data/world/lakkahaltia_clues.json"))
		var clues: Dictionary = parsed if parsed is Dictionary else {}
		screen.setup(map_script.from_data(map_script.load_data()),
			book_script.from_data(clues),
			{})
		get_tree().root.add_child(screen)
		get_tree().current_scene = screen)
	stack.add_child(locations_button)

	# #928: the optional AWN Stress ledger, an overlay on the CWN core.
	var stress_button := Button.new()
	stress_button.text = "CWN — stress ledger (optional AWN module)"
	stress_button.pressed.connect(func() -> void:
		get_tree().change_scene_to_file("res://scenes/stress_screen.tscn"))
	stack.add_child(stress_button)

	var images_button := Button.new()
	images_button.text = "Images — portrait and encounter layouts"
	images_button.pressed.connect(func() -> void:
		var preview: Node = load("res://scenes/images/preview.tscn").instantiate()
		get_tree().root.add_child(preview)
		get_tree().current_scene = preview)
	stack.add_child(images_button)


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
