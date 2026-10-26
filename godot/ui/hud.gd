## HUD for the slice (#631): objective, evidence/journal panel, the skill-check readout and the ending
## screen. Built in code so the layout lives next to the signals it listens to and can be tested
## headlessly; the scene only carries the CanvasLayer.
extends CanvasLayer

signal ending_chosen(ending_id: String)

var _objective: Label
var _journal: RichTextLabel
var _evidence: RichTextLabel
var _prompt: Label
var _dialogue_panel: PanelContainer
var _speaker: Label
var _line: Label
var _choices: VBoxContainer
var _check_panel: PanelContainer
var _check_text: Label
var _ending_panel: PanelContainer
var _ending_title: Label
var _ending_body: Label
var _ending_buttons: HBoxContainer
var _side: VBoxContainer

func _ready() -> void:
	_build()
	if GameState.has_signal("evidence_added"):
		GameState.evidence_added.connect(func(_id: String) -> void: _refresh_case())
		GameState.journal_updated.connect(func(_line: String) -> void: _refresh_case())
		GameState.objective_changed.connect(func(_id: String) -> void: _refresh_case())
		GameState.check_resolved.connect(_on_check_resolved)
		GameState.ending_reached.connect(_on_ending)
	_refresh_case()

func _build() -> void:
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)

	var top := VBoxContainer.new()
	top.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top.offset_left = 16
	top.offset_top = 12
	top.offset_right = -16
	root.add_child(top)

	_objective = Label.new()
	_objective.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	top.add_child(_objective)

	_prompt = Label.new()
	_prompt.modulate = Color(1, 0.92, 0.6)
	top.add_child(_prompt)

	var side_panel := PanelContainer.new()
	side_panel.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	side_panel.offset_left = -332
	side_panel.offset_right = -16
	side_panel.offset_top = 84
	var side_style := StyleBoxFlat.new()
	side_style.bg_color = Color(0.04, 0.05, 0.07, 0.74)
	side_style.set_corner_radius_all(6)
	side_style.set_content_margin_all(12)
	side_panel.add_theme_stylebox_override("panel", side_style)
	root.add_child(side_panel)

	var side := VBoxContainer.new()
	_side = side
	side.custom_minimum_size = Vector2(300, 0)
	side.add_theme_constant_override("separation", 10)
	side_panel.add_child(side)

	_evidence = RichTextLabel.new()
	_evidence.bbcode_enabled = true
	_evidence.fit_content = true
	_evidence.custom_minimum_size = Vector2(300, 0)
	side.add_child(_evidence)

	_journal = RichTextLabel.new()
	_journal.bbcode_enabled = true
	_journal.scroll_following = true
	_journal.fit_content = true
	_journal.custom_minimum_size = Vector2(300, 90)
	side.add_child(_journal)

	_dialogue_panel = PanelContainer.new()
	_dialogue_panel.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_dialogue_panel.offset_left = 24
	_dialogue_panel.offset_right = -24
	_dialogue_panel.offset_top = -260
	_dialogue_panel.offset_bottom = -24
	_dialogue_panel.visible = false
	root.add_child(_dialogue_panel)

	var dialogue_box := VBoxContainer.new()
	_dialogue_panel.add_child(dialogue_box)
	_speaker = Label.new()
	_speaker.modulate = Color(0.75, 0.85, 1.0)
	dialogue_box.add_child(_speaker)
	_line = Label.new()
	_line.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_line.custom_minimum_size = Vector2(0, 60)
	dialogue_box.add_child(_line)
	_choices = VBoxContainer.new()
	dialogue_box.add_child(_choices)

	_check_panel = PanelContainer.new()
	_check_panel.set_anchors_preset(Control.PRESET_CENTER)
	_check_panel.offset_left = -260
	_check_panel.offset_right = 260
	_check_panel.offset_top = -90
	_check_panel.offset_bottom = 90
	_check_panel.visible = false
	root.add_child(_check_panel)
	_check_text = Label.new()
	_check_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_check_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_check_text.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_check_panel.add_child(_check_text)

	_ending_panel = PanelContainer.new()
	_ending_panel.set_anchors_preset(Control.PRESET_CENTER)
	_ending_panel.offset_left = -340
	_ending_panel.offset_right = 340
	_ending_panel.offset_top = -230
	_ending_panel.offset_bottom = 230
	_ending_panel.visible = false
	root.add_child(_ending_panel)
	var ending_box := VBoxContainer.new()
	_ending_panel.add_child(ending_box)
	_ending_title = Label.new()
	_ending_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ending_box.add_child(_ending_title)
	_ending_body = Label.new()
	_ending_body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_ending_body.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ending_box.add_child(_ending_body)
	_ending_buttons = HBoxContainer.new()
	_ending_buttons.alignment = BoxContainer.ALIGNMENT_CENTER
	ending_box.add_child(_ending_buttons)

func _refresh_case() -> void:
	_objective.text = "Objective: " + GameState.objective_text()

	var evidence_lines: Array = ["[b]Evidence[/b]"]
	for evidence_id in GameState.evidence:
		var item: Dictionary = GameState.evidence_items.get(String(evidence_id), {})
		evidence_lines.append("• [%s] %s (%s)" % [
			String(evidence_id), String(item.get("label", "?")), String(item.get("provenance", "other"))
		])
	if GameState.evidence.is_empty():
		evidence_lines.append("• none yet")
	_evidence.text = "\n".join(evidence_lines)

	var journal_lines: Array = ["[b]Case journal[/b]"]
	if GameState.journal.is_empty():
		journal_lines.append("[i]no entries yet[/i]")
	for line in GameState.journal.slice(max(0, GameState.journal.size() - 12)):
		journal_lines.append("• " + String(line))
	_journal.text = "\n".join(journal_lines)

func set_prompt(text: String) -> void:
	_prompt.text = text

## J toggles the evidence/journal column, not the whole HUD.
##
## The level used to flip `visible` on the CanvasLayer, which hid the objective, the prompt and the
## dialogue along with the journal, leaving a black screen with no way to read what was said.
func toggle_journal() -> void:
	if _side != null:
		_side.visible = not _side.visible

func show_dialogue(node: Dictionary, offered: Array) -> void:
	if node.is_empty():
		close_dialogue()
		return
	# With the mouse captured for first-person look, the player cannot click a choice button.
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	_dialogue_panel.visible = true
	_speaker.text = String(node.get("speaker", ""))
	_line.text = String(node.get("text", ""))
	for child in _choices.get_children():
		child.queue_free()
	if offered.is_empty():
		var close := Button.new()
		close.text = "End the conversation"
		close.pressed.connect(func() -> void: close_dialogue())
		_choices.add_child(close)
	for i in offered.size():
		var choice: Dictionary = offered[i]
		var button := Button.new()
		var label := String(choice.get("text", "…"))
		if choice.has("check"):
			var spec: Dictionary = choice["check"]
			label += "  (%s %s vs %d)" % [
				String(spec.get("attribute", "")), String(spec.get("skill", "")), int(spec.get("difficulty", 8))
			]
		button.text = label
		button.pressed.connect(_on_choice_pressed.bind(i))
		_choices.add_child(button)

func close_dialogue() -> void:
	_dialogue_panel.visible = false
	for child in _choices.get_children():
		child.queue_free()
	if not _ending_panel.visible:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func is_dialogue_open() -> bool:
	return _dialogue_panel.visible

## True while a panel owns the pointer: the level must not re-capture the mouse under it.
func has_modal_open() -> bool:
	return _dialogue_panel.visible or _ending_panel.visible

func choice_count() -> int:
	return _choices.get_child_count()

func _on_choice_pressed(index: int) -> void:
	_dialogue_choice.emit(index)

signal _dialogue_choice(index: int)

## Called by the level when a choice was taken: shows the roll for a moment, then the next node.
func _on_check_resolved(result: Dictionary) -> void:
	var faces := ", ".join(result["dice"].map(func(face): return str(face)))
	_check_text.text = "%s %s\nrolled [%s] %+d modifier %+d skill = %d\nvs %d (%s) — %s" % [
		String(result.get("stat", "")),
		String(result.get("skill", "")),
		faces,
		int(result["attribute_modifier"]),
		int(result["skill_level"]),
		int(result["total"]),
		int(result["difficulty"]),
		String(result.get("difficulty_name", "")),
		"SUCCESS" if bool(result["success"]) else "FAILURE",
	]
	_check_panel.visible = true
	await get_tree().create_timer(1.6).timeout
	_check_panel.visible = false

func _on_ending(candidate: Dictionary) -> void:
	close_dialogue()
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	_ending_panel.visible = true
	_ending_title.text = String(candidate.get("title", "Ending"))
	_ending_body.text = String(candidate.get("text", ""))
	for child in _ending_buttons.get_children():
		child.queue_free()
	var restart := Button.new()
	restart.text = "Return to the title screen"
	restart.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://scenes/main.tscn"))
	_ending_buttons.add_child(restart)

func offer_endings(endings: Array) -> void:
	close_dialogue()
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	_ending_panel.visible = true
	_ending_title.text = "How does the case end?"
	_ending_body.text = "Both outcomes are defensible. Neither states what the phenomenon was."
	for child in _ending_buttons.get_children():
		child.queue_free()
	var back := Button.new()
	back.text = "Not yet"
	back.pressed.connect(func() -> void:
		_ending_panel.visible = false
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED)
	_ending_buttons.add_child(back)
	for candidate in endings:
		var button := Button.new()
		button.text = String(candidate.get("title", String(candidate.get("id", "ending"))))
		button.pressed.connect(func() -> void: ending_chosen.emit(String(candidate.get("id", ""))))
		_ending_buttons.add_child(button)
