extends Control

## Title screen for the Godot slice (#631). Keeps the foundation project's title and status
## wording, and adds the two entry points the playable build needs. All copy lives here; no
## rules are evaluated on this screen.

const CASE_SCENE := "res://scenes/lakkahaltia/ward.tscn"
const CAMPAIGN_SCENE := "res://scenes/campaign.tscn"

func _ready() -> void:
	var centre := CenterContainer.new()
	centre.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(centre)

	var stack := VBoxContainer.new()
	stack.add_theme_constant_override("separation", 12)
	stack.alignment = BoxContainer.ALIGNMENT_CENTER
	centre.add_child(stack)

	var title := Label.new()
	title.text = "NoöPunk"
	title.add_theme_font_size_override("font_size", 52)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stack.add_child(title)

	var case_line := Label.new()
	case_line.text = "Etsivä Romppainen ja Lakkahaltian Salaisuus"
	case_line.add_theme_font_size_override("font_size", 20)
	case_line.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stack.add_child(case_line)

	var status := Label.new()
	status.text = "RPG foundation scaffold · pre-Crisis Helsinki, 20XX"
	status.add_theme_font_size_override("font_size", 14)
	status.modulate = Color(0.68, 0.71, 0.78)
	status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stack.add_child(status)

	var spacer := Control.new()
	spacer.custom_minimum_size = Vector2(0, 16)
	stack.add_child(spacer)

	var campaign_button := Button.new()
	campaign_button.text = "New campaign (home / UNSA HQ prototype)"
	campaign_button.custom_minimum_size = Vector2(320, 44)
	campaign_button.pressed.connect(func() -> void: get_tree().change_scene_to_file(CAMPAIGN_SCENE))
	stack.add_child(campaign_button)

	var begin := Button.new()
	begin.text = "Begin the case"
	begin.custom_minimum_size = Vector2(240, 44)
	begin.pressed.connect(_begin)
	stack.add_child(begin)

	var resume := Button.new()
	resume.text = "Resume saved case (F9 in game)"
	resume.custom_minimum_size = Vector2(240, 44)
	resume.pressed.connect(_begin_saved)
	resume.disabled = not FileAccess.file_exists("user://lakkahaltia_save.json")
	stack.add_child(resume)

	var quit := Button.new()
	quit.text = "Quit"
	quit.custom_minimum_size = Vector2(240, 44)
	quit.pressed.connect(func() -> void: get_tree().quit())
	stack.add_child(quit)

	var note := Label.new()
	note.text = "Runs offline. No LLM, no network, no external service."
	note.add_theme_font_size_override("font_size", 13)
	note.modulate = Color(0.6, 0.63, 0.7)
	note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stack.add_child(note)

func _begin() -> void:
	Engine.set_meta("lakkahaltia_resume", false)
	get_tree().change_scene_to_file(CASE_SCENE)

func _begin_saved() -> void:
	Engine.set_meta("lakkahaltia_resume", true)
	get_tree().change_scene_to_file(CASE_SCENE)
