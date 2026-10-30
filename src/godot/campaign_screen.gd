extends Control

## Gate 1 prototype: navigation and persistent narrative state only.
## CWN operator creation, combat and hacking views belong to later gates.
var campaign := NooPunkCampaignState.new()
var status: Label
var actions: VBoxContainer
var journal_label: Label

func _ready() -> void:
	var wrapper := MarginContainer.new()
	wrapper.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	wrapper.add_theme_constant_override("margin_left", 48)
	wrapper.add_theme_constant_override("margin_top", 32)
	add_child(wrapper)
	var layout := VBoxContainer.new()
	layout.add_theme_constant_override("separation", 14)
	wrapper.add_child(layout)
	status = Label.new()
	layout.add_child(status)
	actions = VBoxContainer.new()
	layout.add_child(actions)
	journal_label = Label.new()
	layout.add_child(journal_label)
	_draw()

func _action(label: String, callback: Callable) -> void:
	var button := Button.new()
	button.text = label
	button.custom_minimum_size = Vector2(340, 40)
	button.pressed.connect(callback)
	actions.add_child(button)

func _draw() -> void:
	for child in actions.get_children():
		child.queue_free()
	status.text = "NoöPunk · campaign prototype · " + campaign.current_location.to_upper()
	match campaign.current_location:
		"home":
			_action("Read case note", func(): _record("home_note", "A note points to UNSA headquarters."))
			_action("Travel to UNSA HQ", func(): _travel("hq"))
		"hq":
			_action("Accept investigation", func(): _record("mission_accepted", "An investigation has been assigned."))
			if bool(campaign.flags.get("mission_accepted", false)):
				_action("Visit investigation site", func(): _travel("mission"))
			if bool(campaign.flags.get("mission_visited", false)):
				_action("File debrief", func(): _record("debrief_complete", "Debrief recorded at UNSA HQ."))
			_action("Return home", func(): _travel("home"))
		"mission":
			_action("Examine scene", func(): _record("mission_visited", "Investigation site visited; initial observation recorded."))
			_action("Return to HQ", func(): _travel("hq"))
	_action("Save campaign", func(): _save())
	_action("Load campaign", func(): _load())
	_action("Back to title", func(): get_tree().change_scene_to_file("res://scenes/main.tscn"))
	journal_label.text = "Journal:\n" + "\n".join(campaign.journal)

func _travel(destination: String) -> void:
	if campaign.travel(destination):
		_draw()

func _record(flag: String, line: String) -> void:
	campaign.record_once(flag, line)
	_draw()

func _save() -> void:
	if not campaign.save():
		status.text = "Unable to save campaign."

func _load() -> void:
	if campaign.load_save():
		_draw()
	else:
		status.text = "No valid campaign save. Older versions are not silently migrated."
