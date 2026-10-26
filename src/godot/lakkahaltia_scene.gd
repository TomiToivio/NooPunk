extends Node3D

## First playable slice of *Etsivä Romppainen ja Lakkahaltian Salaisuus* (issue #631).
##
## The level is built in code on purpose: a hand-written .tscn with dozens of nodes could not be
## verified without an editor session, whereas this file is checked by a headless run. Content
## (NPCs, topics, clues, endings) lives in data/godot/lakkahaltia_case.json, not here.

const CASE_PATH := "res://data/godot/lakkahaltia_case.json"
const SAVE_PATH := "user://lakkahaltia_save.json"
const WnRulesScript := preload("res://src/godot/wn_rules.gd")
const CaseStateScript := preload("res://src/godot/case_state.gd")

const WALK_SPEED := 4.0
const REACH := 3.0

var case_data: Dictionary = {}
var state: RefCounted
var rules: RefCounted
var rng := RandomNumberGenerator.new()

var player: CharacterBody3D
var camera: Camera3D
var ui_text: Label
var ui_hint: Label
var journal_visible := false
var active_npc: Dictionary = {}
var dialogue_open := false
var dialogue_topics: Array[Dictionary] = []

func _ready() -> void:
	rng.seed = 20261026
	rules = WnRulesScript.new()
	var file := FileAccess.open(CASE_PATH, FileAccess.READ)
	if file == null:
		push_error("cannot open case data")
		return
	case_data = JSON.parse_string(file.get_as_text())
	state = CaseStateScript.new(String(case_data.get("id", "")))
	_build_level()
	_build_player()
	_build_npcs()
	_build_ui()
	_show("Ward 3, Helsinki. E: talk  ·  J: evidence  ·  F5: save  ·  F9: load")

func _build_level() -> void:
	_add_box(Vector3(0, -0.1, -2), Vector3(24, 0.2, 26), Color(0.55, 0.56, 0.58))     # floor
	_add_box(Vector3(0, 1.5, -15), Vector3(24, 3, 0.3), Color(0.72, 0.73, 0.75))      # north wall
	_add_box(Vector3(-12, 1.5, -2), Vector3(0.3, 3, 26), Color(0.72, 0.73, 0.75))
	_add_box(Vector3(12, 1.5, -2), Vector3(0.3, 3, 26), Color(0.72, 0.73, 0.75))
	# A reception desk and a corridor pillar: enough geometry to read as a ward, not a void.
	_add_box(Vector3(0, 0.5, -9), Vector3(6, 1, 1), Color(0.45, 0.35, 0.28))
	_add_box(Vector3(-6, 1, -3), Vector3(0.8, 2, 0.8), Color(0.6, 0.6, 0.62))

func _add_box(pos: Vector3, size: Vector3, color: Color) -> void:
	var body := StaticBody3D.new()
	body.position = pos
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size
	mesh.mesh = box
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	mesh.material_override = material
	body.add_child(mesh)
	var shape := CollisionShape3D.new()
	var box_shape := BoxShape3D.new()
	box_shape.size = size
	shape.shape = box_shape
	body.add_child(shape)
	add_child(body)

func _build_player() -> void:
	player = CharacterBody3D.new()
	player.position = Vector3(0, 1, 8)
	var shape := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.35
	capsule.height = 1.6
	shape.shape = capsule
	player.add_child(shape)
	camera = Camera3D.new()
	camera.position = Vector3(0, 0.7, 0)
	camera.rotation_degrees = Vector3(-8, 0, 0)
	player.add_child(camera)
	add_child(player)

func _build_npcs() -> void:
	for npc in case_data.get("npcs", []):
		var body := StaticBody3D.new()
		var pos: Array = npc.get("pos", [0, 0, 0])
		body.position = Vector3(float(pos[0]), float(pos[1]) + 0.9, float(pos[2]))
		var mesh := MeshInstance3D.new()
		var capsule := CapsuleMesh.new()
		capsule.radius = 0.35
		capsule.height = 1.8
		mesh.mesh = capsule
		var material := StandardMaterial3D.new()
		material.albedo_color = Color(0.35, 0.45, 0.55)
		mesh.material_override = material
		body.add_child(mesh)
		var shape := CollisionShape3D.new()
		var capsule_shape := CapsuleShape3D.new()
		capsule_shape.radius = 0.35
		capsule_shape.height = 1.8
		shape.shape = capsule_shape
		body.add_child(shape)
		var label := Label3D.new()
		label.text = String(npc.get("display", "?"))
		label.position = Vector3(0, 1.3, 0)
		label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		label.font_size = 48
		body.add_child(label)
		body.set_meta("npc", npc)
		add_child(body)

func _build_ui() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var background := ColorRect.new()
	background.color = Color(0.06, 0.07, 0.09, 0.88)
	background.position = Vector2(24, 24)
	background.size = Vector2(900, 300)
	layer.add_child(background)
	ui_text = Label.new()
	ui_text.position = Vector2(40, 36)
	ui_text.size = Vector2(868, 276)
	ui_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layer.add_child(ui_text)
	ui_hint = Label.new()
	ui_hint.position = Vector2(24, 340)
	layer.add_child(ui_hint)

func _show(text: String) -> void:
	ui_text.text = text

func _process(delta: float) -> void:
	_move_player(delta)
	if dialogue_open:
		_handle_dialogue_keys()
		return
	_find_active_npc()
	if Input.is_key_pressed(KEY_E) and not active_npc.is_empty():
		_open_npc(active_npc)
	if Input.is_key_pressed(KEY_J):
		_toggle_journal()
	if Input.is_key_pressed(KEY_F5):
		_show("Saved." if state.save_to(SAVE_PATH) else "Save failed.")
	if Input.is_key_pressed(KEY_F9):
		_show("Loaded." if state.load_from(SAVE_PATH) else "No save to load.")
	if state.can_end(int(case_data.get("ending_threshold", 4))):
		if Input.is_key_pressed(KEY_P):
			_finish("publish")
		elif Input.is_key_pressed(KEY_C):
			_finish("contain")

func _move_player(delta: float) -> void:
	var direction := Vector3.ZERO
	if Input.is_key_pressed(KEY_W):
		direction.z -= 1.0
	if Input.is_key_pressed(KEY_S):
		direction.z += 1.0
	if Input.is_key_pressed(KEY_A):
		direction.x -= 1.0
	if Input.is_key_pressed(KEY_D):
		direction.x += 1.0
	if direction != Vector3.ZERO:
		direction = direction.normalized()
	player.velocity.x = direction.x * WALK_SPEED
	player.velocity.z = direction.z * WALK_SPEED
	player.velocity.y = -0.5
	player.move_and_slide()
	if camera != null:
		camera.rotation_degrees.y = 0.0

func _find_active_npc() -> void:
	active_npc = {}
	var nearest := REACH
	for child in get_children():
		if not child.has_meta("npc"):
			continue
		var distance := player.global_position.distance_to(child.global_position)
		if distance < nearest:
			nearest = distance
			active_npc = child.get_meta("npc")
	ui_hint.text = "" if active_npc.is_empty() else "E: talk to %s" % String(active_npc.get("display", "?"))

func _open_npc(npc: Dictionary) -> void:
	dialogue_open = true
	active_npc = npc
	dialogue_topics = npc.get("topics", [])
	var lines: Array[String] = ["%s" % String(npc.get("display", "?")), ""]
	var index := 1
	for topic in dialogue_topics:
		lines.append("%d. %s" % [index, String(topic.get("label", "?"))])
		index += 1
	lines.append("")
	lines.append("0. Leave")
	_show("\n".join(lines))

func _handle_dialogue_keys() -> void:
	for i in range(dialogue_topics.size()):
		if Input.is_key_pressed(KEY_1 + i):
			_choose_topic(dialogue_topics[i])
			return
	if Input.is_key_pressed(KEY_0) or Input.is_key_pressed(KEY_ESCAPE):
		dialogue_open = false
		_show("...")

func _choose_topic(topic: Dictionary) -> void:
	var npc_id := String(active_npc.get("id", ""))
	var topic_id := String(topic.get("id", ""))
	state.mark_visited(npc_id, topic_id)
	var lines: Array[String] = [String(topic.get("text", "")), ""]
	var added: bool = state.add_evidence(String(topic.get("evidence", "")))
	if added:
		lines.append("[Evidence added: %s]" % String(topic.get("evidence", "")))
	if topic.has("check"):
		lines.append("")
		lines.append(_resolve_check(topic["check"]))
	lines.append("")
	lines.append("1..%d: another topic   ·   0: leave" % dialogue_topics.size())
	_show("\n".join(lines))

func _resolve_check(check: Dictionary) -> String:
	var attribute := String(check.get("attribute", "Intelligence"))
	var skill_name := String(check.get("skill", "Investigation"))
	var stats: Dictionary = case_data["player"]["stats"]
	var skills: Dictionary = case_data["player"]["skills"]
	var attribute_score := int(stats.get(attribute, 10))
	var skill_level := int(skills.get(skill_name, 0))
	var difficulty := int(check.get("difficulty", 8))
	var result: Dictionary = rules.skill_check(attribute_score, skill_level, difficulty, rng)
	if result.is_empty():
		return "The check could not be resolved."
	var total := int(result.get("total", 0))
	var success := bool(result.get("success", total >= difficulty))
	var dice: Array = result.get("dice", [])
	state.record_roll({"attribute": attribute, "skill": skill_name, "dice": dice,
		"total": total, "difficulty": difficulty, "success": success})
	var header := "%s + %s (%dd6=%s) → %d vs %d — %s" % [
		attribute, skill_name, dice.size(), str(dice), total, difficulty,
		"SUCCESS" if success else "FAILURE"]
	var body := String(check.get("on_success", "")) if success else String(check.get("on_failure", ""))
	return "%s\n%s" % [header, body]

func _toggle_journal() -> void:
	journal_visible = not journal_visible
	if not journal_visible:
		_show("...")
		return
	var clues: Dictionary = case_data.get("clues", {})
	var lines: Array[String] = ["EVIDENCE (%d)" % state.evidence.size(), ""]
	for evidence_id in state.evidence:
		lines.append("· %s" % String(clues.get(evidence_id, evidence_id)))
	if lines.size() == 2:
		lines.append("Nothing yet. Ask someone.")
	_show("\n".join(lines))

func _finish(ending_id: String) -> void:
	if not state.ending.is_empty():
		return
	state.finish(ending_id)
	state.save_to(SAVE_PATH)
	var endings: Dictionary = case_data.get("endings", {})
	var entry: Dictionary = endings.get(ending_id, {})
	_show("%s\n\n%s" % [String(entry.get("title", "Ending")), String(entry.get("text", ""))])
	dialogue_open = true
