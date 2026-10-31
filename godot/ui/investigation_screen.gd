## Investigation screen: abilities, clues and benefits, driven by the GUMSHOE overlay (#933).
##
## The screen decides nothing. Whether a clue can be gathered, what a benefit costs, how many points remain —
## all of it comes from `mods/noopunk/gumshoe_investigation.gd`. This node asks and draws.
##
## The one rule a player will notice: **Gather always works.** There is no roll, no failure animation, no
## "try again". If the investigator has the ability, the information is theirs.
##
## Built in `setup()`/`_ensure_build()`, never `_ready()` — a `--script` runner adds nodes before the main loop
## starts, so `_ready` does not fire and a test would measure an empty screen.
extends Control

const Gumshoe := preload("res://mods/noopunk/gumshoe_investigation.gd")

var gumshoe: Object = null
var scene_data: Dictionary = {}
var found: Array = []
var log_lines: Array = []

var _built := false
var _title: Label
var _body: RichTextLabel
var _abilities: VBoxContainer
var _benefits: VBoxContainer
var _log: RichTextLabel
var _status: Label


func setup(sheet: Dictionary, scene: Dictionary) -> void:
	gumshoe = Gumshoe.from_sheet(sheet)
	scene_data = scene
	_ensure_build()
	_refresh()


func _ready() -> void:
	if not _built:
		_ensure_build()
		_refresh()


func _ensure_build() -> void:
	if _built:
		return
	_built = true
	if gumshoe == null:
		gumshoe = Gumshoe.shipped()
	set_anchors_preset(Control.PRESET_FULL_RECT)

	var background := ColorRect.new()
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	background.color = Color(0.10, 0.086, 0.07)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	_title = Label.new()
	_title.position = Vector2(24, 16)
	_title.add_theme_font_size_override("font_size", 26)
	add_child(_title)

	_status = Label.new()
	_status.position = Vector2(24, 50)
	add_child(_status)

	_body = RichTextLabel.new()
	_body.position = Vector2(24, 82)
	_body.size = Vector2(560, 150)
	_body.bbcode_enabled = false
	_body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(_body)

	_abilities = VBoxContainer.new()
	_abilities.position = Vector2(24, 246)
	_abilities.custom_minimum_size = Vector2(440, 260)
	add_child(_abilities)

	_benefits = VBoxContainer.new()
	_benefits.position = Vector2(500, 246)
	_benefits.custom_minimum_size = Vector2(320, 260)
	add_child(_benefits)

	_log = RichTextLabel.new()
	_log.position = Vector2(24, 520)
	_log.size = Vector2(800, 150)
	_log.bbcode_enabled = false
	_log.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(_log)


func _refresh() -> void:
	if not _built:
		return
	_title.text = String(scene_data.get("name", "Investigation"))
	_status.text = "clues %d/%d · abilities %d" % [found.size(), _clues().size(), gumshoe.order.size()]
	_body.text = String(scene_data.get("summary", ""))

	for child in _abilities.get_children():
		_abilities.remove_child(child)
		child.free()
	for ability_id in gumshoe.order:
		if gumshoe.rating(ability_id) < 1:
			continue  # an ability nobody has is not a menu entry
		var button := Button.new()
		button.text = "%s  (%d)" % [String(gumshoe.abilities[ability_id]["name"]),
			int(gumshoe.pool(ability_id))]
		button.pressed.connect(_gather.bind(String(ability_id)))
		_abilities.add_child(button)

	for child in _benefits.get_children():
		_benefits.remove_child(child)
		child.free()
	var heading := Label.new()
	heading.text = "Benefits (points)"
	_benefits.add_child(heading)
	for benefit in Array(scene_data.get("benefits", [])):
		var cost := int(benefit.get("cost", 1))
		var button := Button.new()
		button.text = "%s — %d" % [String(benefit.get("text", benefit.get("id", ""))), cost]
		button.disabled = gumshoe.pool(String(benefit.get("ability", ""))) < cost
		button.pressed.connect(_buy.bind(String(benefit.get("id", "")),
			String(benefit.get("ability", "")), cost))
		_benefits.add_child(button)


func _clues() -> Array:
	return Array(scene_data.get("clues", []))


## Gather the first clue of this scene that uses this ability and is not yet known. There is deliberately no
## failure branch: the ability is the whole requirement.
func _gather(ability_id: String) -> void:
	for clue in _clues():
		if String(clue.get("ability", "")) != ability_id:
			continue
		if found.has(String(clue.get("id", ""))):
			_append("Already known: " + String(clue.get("id", "")))
			return
		var result: Dictionary = gumshoe.gather(ability_id, clue)
		if not bool(result.get("ok", false)):
			_append("Cannot gather: " + String(result.get("reason", "?")))
			return
		found.append(String(clue.get("id", "")))
		_append("Found: " + String(clue.get("text", clue.get("id", ""))))
		_refresh()
		return
	_append("%s has nothing to find here" % ability_id)


func _buy(benefit_id: String, ability_id: String, cost: int) -> void:
	var result: Dictionary = gumshoe.buy_benefit(ability_id, benefit_id, cost)
	if bool(result.get("ok", false)):
		_append("Spent %d on %s" % [cost, benefit_id])
	else:
		_append("Cannot buy %s: %s" % [benefit_id, String(result.get("reason", "?"))])
	_refresh()


func _append(line: String) -> void:
	log_lines.append(line)
	if _log != null:
		_log.text = "\n".join(log_lines)
