## The Stress ledger: a table-side console for the optional AWN Stress overlay (#928).
##
## This screen is the only place the overlay meets a human. It shows the meter against the character's
## WIS ceiling, what put the Stress there, which consequences are in force, and the choices the rules
## offer: recovery, a Breakdown, or Hardening.
##
## Two boundaries are visible in the interface on purpose:
##
## * **The overlay never rolls.** When the rules call for a Mental save or a Heal check, the GM rolls at
##   the table and records the outcome here — "the save held" / "the save failed". The same is true of the
##   dice inside the subsystem: the `die` control is the number the GM rolled, not a roll this screen makes.
## * **The overlay never edits the CWN sheet.** WIS is an input, not a lookup: the screen does not read or
##   write `godot/core/`. Effects come back as data and the table applies them.
##
## The tracker persists beside the core save (`user://awn_stress_state.json`), not inside it, so the core
## save schema stays the core's.
extends Control

const Stress := preload("res://mods/noopunk/stress.gd")
const SAVE_PATH := "user://awn_stress_state.json"

var tracker: Dictionary = {}

var _built := false
var _title: Label
var _status: Label
var _wisdom: SpinBox
var _enabled: CheckButton
var _trigger: OptionButton
var _modifier: OptionButton
var _die: SpinBox
var _value: SpinBox
var _participant: CheckBox
var _add: Button
var _causes: Label
var _end_scene: Button
var _save_ok: Button
var _save_fail: Button
var _breakdown: OptionButton
var _suffer: Button
var _scar: OptionButton
var _harden: Button
var _recovery: OptionButton
var _check_ok: CheckBox
var _recover: Button
var _new_day: Button
var _conditions: Label
var _log: Label


func _ready() -> void:
	if not _built:
		if tracker.is_empty():
			setup(10, Stress.default_enabled())
		else:
			_build()


## Open the ledger for a character. `wisdom` is the CWN WIS score the table copies in from the sheet.
func setup(wisdom: int = 10, enabled: bool = true) -> void:
	tracker = Stress.new_tracker(wisdom, {"enabled": enabled})
	_build()


func _build() -> void:
	_built = true
	var scroll := ScrollContainer.new()
	scroll.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(scroll)
	var page := VBoxContainer.new()
	page.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	page.add_theme_constant_override("separation", 8)
	scroll.add_child(page)

	_title = _label(page, "Stress — Ashes Without Number module (optional, over CWN)")
	_title.add_theme_font_size_override("font_size", 20)

	_status = _label(page, "")
	_status.add_theme_font_size_override("font_size", 16)

	# --- the module flag and the ceiling -------------------------------------
	var top := HBoxContainer.new()
	page.add_child(top)
	_enabled = CheckButton.new()
	_enabled.text = "AWN Stress module on"
	_enabled.button_pressed = Stress.is_enabled(tracker)
	_enabled.toggled.connect(_on_toggled)
	top.add_child(_enabled)
	top.add_child(_label_raw("    WIS"))
	_wisdom = SpinBox.new()
	_wisdom.min_value = 1
	_wisdom.max_value = 18
	_wisdom.value = Stress.threshold(tracker)
	_wisdom.value_changed.connect(_on_wisdom_changed)
	top.add_child(_wisdom)

	# --- gaining Stress ------------------------------------------------------
	_label_raw_section(page, "Scene — what happened (Stress is applied when the scene ends)")
	var row := HBoxContainer.new()
	page.add_child(row)
	_trigger = OptionButton.new()
	_trigger.custom_minimum_size = Vector2(340, 0)
	_trigger.item_selected.connect(_on_trigger_changed)
	row.add_child(_trigger)
	_modifier = OptionButton.new()
	_modifier.custom_minimum_size = Vector2(220, 0)
	row.add_child(_modifier)
	row.add_child(_label_raw("die"))
	_die = SpinBox.new()
	_die.min_value = 1
	_die.max_value = 10
	row.add_child(_die)
	row.add_child(_label_raw("value"))
	_value = SpinBox.new()
	_value.min_value = 1
	_value.max_value = 3
	row.add_child(_value)

	var row2 := HBoxContainer.new()
	page.add_child(row2)
	_participant = CheckBox.new()
	_participant.text = "the character took part (a bystander gains nothing)"
	_participant.button_pressed = true
	row2.add_child(_participant)
	_add = Button.new()
	_add.text = "Add to the scene"
	_add.pressed.connect(_on_add)
	row2.add_child(_add)

	_causes = _label(page, "")
	_end_scene = Button.new()
	_end_scene.text = "End the scene — apply the Stress"
	_end_scene.pressed.connect(_on_end_scene)
	page.add_child(_end_scene)

	# --- the check, and the two ways out of it ------------------------------
	_label_raw_section(page, "The check")
	var check_row := HBoxContainer.new()
	page.add_child(check_row)
	check_row.add_child(_label_raw("GM rolled a Mental save —"))
	_save_ok = Button.new()
	_save_ok.text = "it held"
	_save_ok.pressed.connect(func() -> void: _on_save(true))
	check_row.add_child(_save_ok)
	_save_fail = Button.new()
	_save_fail.text = "it failed"
	_save_fail.pressed.connect(func() -> void: _on_save(false))
	check_row.add_child(_save_fail)

	var choice_row := HBoxContainer.new()
	page.add_child(choice_row)
	_breakdown = OptionButton.new()
	_breakdown.custom_minimum_size = Vector2(220, 0)
	choice_row.add_child(_breakdown)
	_suffer = Button.new()
	_suffer.text = "Suffer this Breakdown"
	_suffer.pressed.connect(_on_suffer)
	choice_row.add_child(_suffer)

	var harden_row := HBoxContainer.new()
	page.add_child(harden_row)
	_scar = OptionButton.new()
	_scar.custom_minimum_size = Vector2(220, 0)
	harden_row.add_child(_scar)
	_harden = Button.new()
	_harden.text = "Harden instead — take this scar"
	_harden.pressed.connect(_on_harden)
	harden_row.add_child(_harden)

	# --- recovery ------------------------------------------------------------
	_label_raw_section(page, "Recovery")
	var rec_row := HBoxContainer.new()
	page.add_child(rec_row)
	_recovery = OptionButton.new()
	_recovery.custom_minimum_size = Vector2(340, 0)
	rec_row.add_child(_recovery)
	_check_ok = CheckBox.new()
	_check_ok.text = "the core's check succeeded"
	rec_row.add_child(_check_ok)
	_recover = Button.new()
	_recover.text = "Recover"
	_recover.pressed.connect(_on_recover)
	rec_row.add_child(_recover)
	_new_day = Button.new()
	_new_day.text = "Next day"
	_new_day.pressed.connect(_on_new_day)
	rec_row.add_child(_new_day)

	# --- state, log, persistence --------------------------------------------
	_label_raw_section(page, "In force")
	_conditions = _label(page, "")
	_label_raw_section(page, "Audit log")
	_log = _label(page, "")

	var save_row := HBoxContainer.new()
	page.add_child(save_row)
	var save_button := Button.new()
	save_button.text = "Save the ledger"
	save_button.pressed.connect(_on_save_file)
	save_row.add_child(save_button)
	var load_button := Button.new()
	load_button.text = "Load the ledger"
	load_button.pressed.connect(_on_load_file)
	save_row.add_child(load_button)
	var back := Button.new()
	back.text = "Back to the title"
	back.pressed.connect(_on_back)
	save_row.add_child(back)

	_refresh()


# --------------------------------------------------------------------------- #
# Controls
# --------------------------------------------------------------------------- #


func _on_toggled(on: bool) -> void:
	tracker["enabled"] = on
	_refresh()


func _on_wisdom_changed(value: float) -> void:
	# WIS is the ceiling. Changing it re-tests the ceiling but never rewrites the Stress already there.
	tracker["wisdom"] = int(value)
	_refresh()


func _on_trigger_changed(_index: int) -> void:
	_refresh_modifiers()


func _on_add() -> void:
	var event_id := _selected_id(_trigger)
	if event_id.is_empty():
		return
	var options: Dictionary = {"participated": _participant.button_pressed, "value": int(_value.value)}
	var modifiers: Array = []
	var modifier_id := _selected_id(_modifier)
	if not modifier_id.is_empty() and modifier_id != "none":
		modifiers.append(modifier_id)
		options["rolls"] = {modifier_id: int(_die.value)}
	options["modifiers"] = modifiers
	var result := Stress.award(tracker, event_id, options)
	_note(result)
	_refresh()


func _on_end_scene() -> void:
	var result := Stress.end_scene(tracker)
	_note(result)
	_refresh()


func _on_save(success: bool) -> void:
	var result := Stress.resolve_save(tracker, success)
	_note(result)
	_refresh()


func _on_suffer() -> void:
	var result := Stress.choose_breakdown(tracker, _selected_id(_breakdown))
	_note(result)
	_refresh()


func _on_harden() -> void:
	var result := Stress.harden(tracker, _selected_id(_scar))
	_note(result)
	_refresh()


func _on_recover() -> void:
	var id := _selected_id(_recovery)
	var options: Dictionary = {"check_success": _check_ok.button_pressed}
	if id == "major_goal":
		options["rolls"] = {id: int(_die.value)}
	var result := Stress.recover(tracker, id, options)
	_note(result)
	_refresh()


func _on_new_day() -> void:
	_note(Stress.new_day(tracker))
	_refresh()


func _on_save_file() -> void:
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		_note({"ok": false, "reason": "cannot write %s" % SAVE_PATH})
		_refresh()
		return
	file.store_string(JSON.stringify(Stress.to_dict(tracker)))
	file.close()
	_note({"ok": true, "written": SAVE_PATH})
	_refresh()


func _on_load_file() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		_note({"ok": false, "reason": "no ledger at %s" % SAVE_PATH})
		_refresh()
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
	if not parsed is Dictionary:
		_note({"ok": false, "reason": "the ledger file is not JSON"})
		_refresh()
		return
	tracker = Stress.from_dict(parsed)
	_wisdom.set_value_no_signal(Stress.threshold(tracker))
	_note({"ok": true, "loaded": SAVE_PATH})
	_refresh()


func _on_back() -> void:
	get_tree().change_scene_to_file("res://scenes/main.tscn")


# --------------------------------------------------------------------------- #
# Refresh
# --------------------------------------------------------------------------- #


func _refresh() -> void:
	var wisdom := Stress.threshold(tracker)
	var current := Stress.stress(tracker)
	_enabled.set_pressed_no_signal(Stress.is_enabled(tracker))
	_wisdom.set_value_no_signal(wisdom)
	if not Stress.is_enabled(tracker):
		_status.text = "Stress %d — the module is off. CWN runs unchanged." % current
	elif Stress.is_over(tracker):
		_status.text = "Stress %d / WIS %d — %d over the ceiling. Next check: Mental %+d." \
			% [current, wisdom, Stress.over_by(tracker), Stress.next_penalty(tracker)]
	else:
		_status.text = "Stress %d / WIS %d — %d to the ceiling." \
			% [current, wisdom, wisdom - current]

	var pending := Stress.pending_save(tracker)
	if bool(pending.get("required", false)):
		_status.text += "  A check is owed now: Mental %+d." % int(pending.get("penalty", -2))
	if not Stress.active_breakdown(tracker).is_empty():
		_status.text += "  Breakdown in force: %s." % Stress.active_breakdown(tracker)

	var causes: Array = Stress.latest_causes(tracker)
	if causes.is_empty():
		_causes.text = "Nothing recorded in this scene."
	else:
		var lines: PackedStringArray = []
		for cause in causes:
			var row: Dictionary = cause
			lines.append("  +%d  %s" % [int(row.get("raw", 0)), String(row.get("event", ""))])
		_causes.text = "This scene:\n" + "\n".join(lines)

	var conditions: Array = Stress.active_conditions(tracker)
	if conditions.is_empty():
		_conditions.text = "Nothing active."
	else:
		var rows: PackedStringArray = []
		for entry in conditions:
			var row: Dictionary = entry
			rows.append("  %s — %s" % [String(row.get("kind", "")), String(row.get("label", ""))])
		_conditions.text = "\n".join(rows)

	var log: Array = Stress.audit(tracker)
	var tail: Array = log.slice(maxi(0, log.size() - 12))
	var log_lines: PackedStringArray = []
	for entry in tail:
		var row: Dictionary = entry
		log_lines.append("  #%d %s %s" % [int(row.get("seq", 0)), String(row.get("kind", "")),
			JSON.stringify(row)])
	_log.text = "\n".join(log_lines)

	_populate_triggers()
	_refresh_modifiers()
	_populate_breakdowns()
	_populate_scars()
	_populate_recovery()

	_add.disabled = not Stress.is_enabled(tracker)
	_end_scene.disabled = not Stress.is_enabled(tracker)
	_save_ok.disabled = not bool(pending.get("required", false))
	_save_fail.disabled = _save_ok.disabled
	var owed := bool(tracker.get("awaiting_breakdown", false))
	_suffer.disabled = not owed
	_harden.disabled = not owed
	_recover.disabled = not Stress.is_enabled(tracker)


func _populate_triggers() -> void:
	var wanted := _selected_id(_trigger)
	_trigger.clear()
	for id in Stress.event_ids():
		_trigger.add_item("AWN · %s" % String(id))
		_trigger.set_item_metadata(_trigger.item_count - 1, String(id))
	for id in Stress.noopunk_event_ids():
		_trigger.add_item("NoöPunk · %s" % String(id))
		_trigger.set_item_metadata(_trigger.item_count - 1, String(id))
	_select(_trigger, wanted)


## The modifiers the selected trigger offers, plus "none". A modifier is what turns a 2 into a 2+die.
func _refresh_modifiers() -> void:
	var wanted := _selected_id(_modifier)
	_modifier.clear()
	_modifier.add_item("no modifier")
	_modifier.set_item_metadata(_modifier.item_count - 1, "none")
	var row: Dictionary = Stress.event(_selected_id(_trigger))
	if row.is_empty():
		row = Stress.noopunk_event(_selected_id(_trigger))
	for entry in Array(row.get("modifiers", [])):
		var modifier: Dictionary = entry
		var id := String(modifier.get("id", ""))
		_modifier.add_item("%s (%s)" % [id, str(modifier.get("stress", 0))])
		_modifier.set_item_metadata(_modifier.item_count - 1, id)
	_select(_modifier, wanted)


func _populate_breakdowns() -> void:
	var wanted := _selected_id(_breakdown)
	_breakdown.clear()
	for id in Stress.breakdown_ids():
		_breakdown.add_item(String(id))
		_breakdown.set_item_metadata(_breakdown.item_count - 1, String(id))
	_select(_breakdown, wanted)


func _populate_scars() -> void:
	var wanted := _selected_id(_scar)
	_scar.clear()
	for id in Stress.scar_ids():
		if Stress.has_scar(tracker, String(id)):
			continue
		_scar.add_item(String(id))
		_scar.set_item_metadata(_scar.item_count - 1, String(id))
	_select(_scar, wanted)


func _populate_recovery() -> void:
	var wanted := _selected_id(_recovery)
	_recovery.clear()
	for id in Stress.recovery_ids():
		var usable: bool = Stress.can_recover(tracker, String(id))
		_recovery.add_item(String(id) if usable else "%s (used or barred)" % String(id))
		_recovery.set_item_metadata(_recovery.item_count - 1, String(id))
		_recovery.set_item_disabled(_recovery.item_count - 1, not usable)
	_select(_recovery, wanted)


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #


func _selected_id(button: OptionButton) -> String:
	if button.selected < 0:
		return ""
	return String(button.get_item_metadata(button.selected))


func _select(button: OptionButton, id: String) -> void:
	if id.is_empty():
		return
	for index in button.item_count:
		if String(button.get_item_metadata(index)) == id:
			button.select(index)
			return


func _note(result: Dictionary) -> void:
	# Nothing here needs a modal: the audit log is the record, and the status line is the answer.
	if not bool(result.get("ok", false)):
		_status.text = "refused: %s" % String(result.get("reason", "unknown"))


func _label(parent: Node, text: String) -> Label:
	var label := _label_raw(text)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	parent.add_child(label)
	return label


func _label_raw(text: String) -> Label:
	var label := Label.new()
	label.text = text
	return label


func _label_raw_section(parent: Node, text: String) -> void:
	var label := _label_raw(text)
	label.modulate = Color(0.75, 0.8, 0.9)
	parent.add_child(label)
