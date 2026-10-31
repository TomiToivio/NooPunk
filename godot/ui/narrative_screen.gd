## Helsinki narrative mode (#897). Location map, actions, investigation log, CWN sheet and party in
## one screen; no tactical view. The 1974 palette lives here as the first design-token pass.
extends Control

const Session := preload("res://godot/narrative/helsinki_session.gd")
const Adapter := preload("res://godot/core/rules_adapter.gd")

## Canonical 1974 tokens (#897 visual bible). The screen reads the shared file rather than keeping a
## second palette in code.
const TOKENS := "res://data/ui/noopunk_1974_tokens.json"
var palette: Dictionary = {}

var session: Object
var _map_box: VBoxContainer
var _action_box: VBoxContainer
var _log_label: RichTextLabel
var _sheet_label: Label
var _party_label: Label
var _title: Label
var _subtitle: Label


func _ready() -> void:
	palette = _load_tokens()
	session = Session.new(Session.DATA, Adapter.new("res://data/rules/wn_core.json", 1974))
	_build()
	_refresh()


func _load_tokens() -> Dictionary:
	var file := FileAccess.open(TOKENS, FileAccess.READ)
	if file == null:
		push_error("narrative_screen: cannot open %s" % TOKENS)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return Dictionary(parsed.get("colors", {})) if parsed is Dictionary else {}


func _tone(key: String, fallback: String) -> Color:
	return Color(String(palette.get(key, fallback)))


func _build() -> void:
	var bg := ColorRect.new()
	bg.color = _tone("void_plum", "#190E24")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var margin := MarginContainer.new()
	margin.set_anchors_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_bottom", 16)
	add_child(margin)

	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 10)
	margin.add_child(column)

	var header := Label.new()
	header.text = "NOÖPUNK — HELSINKI, 2045 (AS IMAGINED IN 1974)"
	header.add_theme_color_override("font_color", _tone("analog_amber", "#F2B45E"))
	header.add_theme_font_size_override("font_size", 22)
	column.add_child(header)

	_title = Label.new()
	_title.add_theme_color_override("font_color", _tone("paper_ivory", "#F5E8C9"))
	_title.add_theme_font_size_override("font_size", 18)
	column.add_child(_title)
	_subtitle = Label.new()
	_subtitle.add_theme_color_override("font_color", _tone("dim_lilac", "#BBAACA"))
	_subtitle.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	column.add_child(_subtitle)

	var body := HBoxContainer.new()
	body.add_theme_constant_override("separation", 14)
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(body)

	_map_box = _panel_column(body, "CITY", false, 240)
	var middle := _panel_column(body, "HERE", true, 320)
	_action_box = middle
	var log_heading := Label.new()
	log_heading.text = "LOG"
	log_heading.add_theme_color_override("font_color", _tone("mint_terminal", "#72E1B2"))
	log_heading.add_theme_font_size_override("font_size", 13)
	middle.add_child(log_heading)
	_log_label = RichTextLabel.new()
	_log_label.bbcode_enabled = false
	_log_label.fit_content = false
	_log_label.scroll_following = true
	_log_label.custom_minimum_size = Vector2(0, 160)
	_log_label.add_theme_color_override("default_color", _tone("dim_lilac", "#BBAACA"))
	middle.add_child(_log_label)
	var right := _panel_column(body, "AGENT", false, 260)
	_sheet_label = Label.new()
	_sheet_label.add_theme_color_override("font_color", _tone("paper_ivory", "#F5E8C9"))
	right.add_child(_sheet_label)
	_party_label = Label.new()
	_party_label.add_theme_color_override("font_color", _tone("mint_terminal", "#72E1B2"))
	_party_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	right.add_child(_party_label)


func _panel_column(parent: Control, heading: String, expand := false, width := 240) -> VBoxContainer:
	var panel := PanelContainer.new()
	var style := StyleBoxFlat.new()
	style.bg_color = _tone("midnight_ink", "#2C1837")
	style.border_color = _tone("danger_coral", "#F17570")
	style.set_border_width_all(1)
	style.set_corner_radius_all(2)
	panel.add_theme_stylebox_override("panel", style)
	panel.custom_minimum_size = Vector2(width, 0)
	if expand:
		panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(panel)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	panel.add_child(box)
	var label := Label.new()
	label.text = heading
	label.add_theme_color_override("font_color", _tone("mint_terminal", "#72E1B2"))
	label.add_theme_font_size_override("font_size", 13)
	box.add_child(label)
	return box


func _refresh() -> void:
	var here: Dictionary = session.current_location()
	_title.text = String(here.get("name", ""))
	_subtitle.text = String(here.get("subtitle", ""))
	for box in [_map_box, _action_box]:
		for child in box.get_children():
			if child is Button:
				child.queue_free()

	for entry in session.locations():
		var id := String(entry.get("id", ""))
		if not session.is_discovered(id):
			continue
		var button := _button(String(entry.get("name", id)))
		button.disabled = id == session.current
		button.pressed.connect(_on_travel.bind(id))
		_map_box.add_child(button)

	for entry in session.actions():
		var action := _button(String(entry.get("label", entry.get("id", ""))))
		action.pressed.connect(_on_action.bind(String(entry.get("id", ""))))
		_action_box.add_child(action)

	_log_label.text = "\n".join(session.log_lines.slice(maxi(0, session.log_lines.size() - 12)))
	_sheet_label.text = "STR 10  DEX 11  CON 10\nINT 12  WIS 11  CHA 09\nHP %d/10   Stress %d\nClues %d   Credits %d" % [
		session.player_hp, session.stress, session.clues.size(), session.credits]
	var names: Array = []
	for member in session.party:
		names.append("%s — %s" % [member.get("name", "?"), member.get("role", "")])
	_party_label.text = "Party %d/4\n%s" % [session.party.size(), "\n".join(names)]


func _button(text: String) -> Button:
	var button := Button.new()
	button.text = text
	button.alignment = HORIZONTAL_ALIGNMENT_LEFT
	button.add_theme_color_override("font_color", _tone("paper_ivory", "#F5E8C9"))
	var normal := StyleBoxFlat.new()
	normal.bg_color = _tone("midnight_ink", "#2C1837")
	normal.border_color = _tone("cosmic_magenta", "#E54B9B")
	normal.set_border_width_all(1)
	button.add_theme_stylebox_override("normal", normal)
	return button


func _on_travel(id: String) -> void:
	session.travel(id)
	_refresh()


func _on_action(id: String) -> void:
	session.act(id)
	_refresh()
