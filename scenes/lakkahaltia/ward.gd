extends Node3D

## Lakkahaltia ward: the playable vertical slice (#631).
##
## The level is built procedurally from primitives so the repository carries no third-party
## art and the scene stays reviewable as code. Every rule number comes from
## res://data/rules/wn_core.json through NooPunkWnRules; every line of prose comes from
## res://data/scenarios/lakkahaltia/*.json through NooPunkCaseState. This script is glue and
## presentation only: it decides nothing about the game's rules.

const SAVE_PATH := "user://lakkahaltia_save.json"
const CASE_PATH := "res://data/scenarios/lakkahaltia/case.json"
const DIALOGUE_PATH := "res://data/scenarios/lakkahaltia/dialogue.json"

## Fixed so an automated run and a human run agree; documented in docs/GODOT.md.
const ROLL_SEED := 20261026

const WALL_HEIGHT := 3.0
const ROOM_WIDTH := 12.0
const WALK_SPEED := 4.2
const INTERACT_RANGE := 2.6

var state: NooPunkCaseState
var rules: NooPunkWnRules
var rng := RandomNumberGenerator.new()

var player: CharacterBody3D
var camera: Camera3D
var interactables: Array[Dictionary] = []
var nearest: Dictionary = {}
var dialogue_active := false
var ending_active := false

var status_label: Label
var prompt_label: Label
var toast_label: Label
var dialogue_panel: PanelContainer
var speaker_label: Label
var dialogue_text: RichTextLabel
var choices_box: VBoxContainer
var journal_panel: PanelContainer
var journal_text: RichTextLabel
var ending_panel: PanelContainer
var ending_title: Label
var ending_body: RichTextLabel
var ending_buttons: VBoxContainer

func _ready() -> void:
	rng.seed = ROLL_SEED
	state = NooPunkCaseState.new(CASE_PATH, DIALOGUE_PATH)
	rules = NooPunkWnRules.new()
	state.state_changed.connect(_refresh_status)
	_build_rooms()
	_build_player()
	_build_npcs()
	_build_objects()
	_build_hud()
	if Engine.has_meta("lakkahaltia_resume") and bool(Engine.get_meta("lakkahaltia_resume")):
		if state.load_from(SAVE_PATH):
			_restore_position()
			_toast("Resumed the saved case.")
	_refresh_status()
	print("WARD_READY npcs=%d objects=%d clues=%d" % [
		state.case_data.get("npcs", []).size(),
		state.case_data.get("objects", []).size(),
		state.case_data.get("clues", {}).size()
	])

# -- level ---------------------------------------------------------------------------------

func _material(colour: Color, roughness: float = 0.9) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_color = colour
	material.roughness = roughness
	return material

func _box(position: Vector3, size: Vector3, colour: Color, collide: bool = true) -> Node3D:
	var root: Node3D
	if collide:
		var body := StaticBody3D.new()
		var shape := CollisionShape3D.new()
		var box_shape := BoxShape3D.new()
		box_shape.size = size
		shape.shape = box_shape
		body.add_child(shape)
		root = body
	else:
		root = Node3D.new()
	root.position = position
	var mesh := MeshInstance3D.new()
	var box_mesh := BoxMesh.new()
	box_mesh.size = size
	mesh.mesh = box_mesh
	mesh.material_override = _material(colour)
	root.add_child(mesh)
	add_child(root)
	return root

func _build_rooms() -> void:
	# One ward corridor, four zones: entrance, corridor, reception, patient room.
	_box(Vector3(0, -0.1, -16), Vector3(ROOM_WIDTH, 0.2, 44), Color(0.16, 0.17, 0.19))
	_box(Vector3(0, WALL_HEIGHT, -16), Vector3(ROOM_WIDTH, 0.2, 44), Color(0.10, 0.11, 0.13), false)
	# Side walls.
	_box(Vector3(-ROOM_WIDTH / 2, WALL_HEIGHT / 2, -16), Vector3(0.3, WALL_HEIGHT, 44), Color(0.30, 0.31, 0.33))
	_box(Vector3(ROOM_WIDTH / 2, WALL_HEIGHT / 2, -16), Vector3(0.3, WALL_HEIGHT, 44), Color(0.30, 0.31, 0.33))
	# Back wall and front wall with the entrance gap.
	_box(Vector3(0, WALL_HEIGHT / 2, -38), Vector3(ROOM_WIDTH, WALL_HEIGHT, 0.3), Color(0.30, 0.31, 0.33))
	_box(Vector3(-3.5, WALL_HEIGHT / 2, 6), Vector3(5.0, WALL_HEIGHT, 0.3), Color(0.30, 0.31, 0.33))
	_box(Vector3(3.5, WALL_HEIGHT / 2, 6), Vector3(5.0, WALL_HEIGHT, 0.3), Color(0.30, 0.31, 0.33))
	# Partitions with a doorway on the left, one between each pair of zones.
	for z in [-5.0, -15.0, -25.0]:
		_box(Vector3(3.0, WALL_HEIGHT / 2, z), Vector3(6.0, WALL_HEIGHT, 0.25), Color(0.26, 0.27, 0.29))
	# Reception desk, bed, chairs: simple furniture that reads as a ward.
	_box(Vector3(2.0, 0.5, -20.5), Vector3(4.0, 1.0, 0.8), Color(0.22, 0.24, 0.27))
	_box(Vector3(0.6, 0.3, -31.0), Vector3(2.0, 0.6, 3.2), Color(0.24, 0.26, 0.28))
	_box(Vector3(-4.0, 0.45, -8.0), Vector3(1.2, 0.9, 1.2), Color(0.20, 0.21, 0.23))
	# Lighting: ward fluorescents plus one cold window light in the patient room.
	var sun := DirectionalLight3D.new()
	sun.light_energy = 0.45
	sun.rotation_degrees = Vector3(-55, -35, 0)
	add_child(sun)
	for z in [-2.0, -12.0, -22.0, -32.0]:
		var lamp := OmniLight3D.new()
		lamp.position = Vector3(0, 2.7, z)
		lamp.light_energy = 1.6
		lamp.omni_range = 9.0
		lamp.light_color = Color(0.85, 0.92, 1.0)
		add_child(lamp)

func _build_player() -> void:
	player = CharacterBody3D.new()
	player.name = "Romppainen"
	var shape := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.35
	capsule.height = 1.7
	shape.shape = capsule
	shape.position.y = 0.85
	player.add_child(shape)
	var mesh := MeshInstance3D.new()
	var body_mesh := CapsuleMesh.new()
	body_mesh.radius = 0.35
	body_mesh.height = 1.7
	mesh.mesh = body_mesh
	mesh.material_override = _material(Color(0.55, 0.62, 0.72))
	mesh.position.y = 0.85
	player.add_child(mesh)
	var spawn: Dictionary = state.case_data.get("spawn", {})
	player.position = Vector3(float(spawn.get("x", 0)), float(spawn.get("y", 0)), float(spawn.get("z", 2)))
	add_child(player)

	camera = Camera3D.new()
	camera.position = player.position + Vector3(7.0, 9.0, 7.0)
	camera.current = true
	add_child(camera)
	camera.look_at(player.position + Vector3(0, 1.0, 0))

func _build_npcs() -> void:
	for npc in state.case_data.get("npcs", []):
		var id := str(npc.get("id", ""))
		var pos: Dictionary = npc.get("position", {})
		var root := StaticBody3D.new()
		root.name = "NPC_" + id
		root.position = Vector3(float(pos.get("x", 0)), float(pos.get("y", 0)), float(pos.get("z", 0)))
		var shape := CollisionShape3D.new()
		var capsule := CapsuleShape3D.new()
		capsule.radius = 0.4
		capsule.height = 1.8
		shape.shape = capsule
		shape.position.y = 0.9
		root.add_child(shape)
		var mesh := MeshInstance3D.new()
		var body_mesh := CapsuleMesh.new()
		body_mesh.radius = 0.4
		body_mesh.height = 1.8
		mesh.mesh = body_mesh
		mesh.material_override = _material(Color(str(npc.get("colour", "#888888"))))
		mesh.position.y = 0.9
		root.add_child(mesh)
		if _labels_enabled():
			var label := Label3D.new()
			label.text = str(npc.get("name", id))
			label.position.y = 2.15
			label.font_size = 48
			label.pixel_size = 0.01
			label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			label.modulate = Color(0.92, 0.94, 0.98)
			root.add_child(label)
		add_child(root)
		interactables.append({
			"kind": "npc",
			"id": id,
			"name": str(npc.get("name", id)),
			"position": root.position,
			"node": root
		})

func _build_objects() -> void:
	for obj in state.case_data.get("objects", []):
		var id := str(obj.get("id", ""))
		var pos: Dictionary = obj.get("position", {})
		var position := Vector3(float(pos.get("x", 0)), float(pos.get("y", 0)), float(pos.get("z", 0)))
		var marker := MeshInstance3D.new()
		var box := BoxMesh.new()
		box.size = Vector3(0.45, 0.12, 0.32)
		marker.mesh = box
		marker.material_override = _material(Color(0.85, 0.72, 0.35), 0.4)
		marker.position = position
		add_child(marker)
		if _labels_enabled():
			var label := Label3D.new()
			label.text = str(obj.get("name", id))
			label.position = position + Vector3(0, 0.55, 0)
			label.font_size = 36
			label.pixel_size = 0.008
			label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			label.modulate = Color(0.95, 0.88, 0.6)
			add_child(label)
		interactables.append({
			"kind": "object",
			"id": id,
			"name": str(obj.get("name", id)),
			"position": position,
			"node": marker
		})

## Label3D needs a real renderer; the dummy headless driver logs a mesh error for it.
func _labels_enabled() -> bool:
	return DisplayServer.get_name() != "headless"

# -- hud -----------------------------------------------------------------------------------

func _label(text: String, size: int = 18) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", size)
	return label

func _panel() -> PanelContainer:
	var panel := PanelContainer.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.06, 0.08, 0.94)
	style.border_color = Color(0.35, 0.38, 0.45)
	style.set_border_width_all(1)
	style.set_content_margin_all(16)
	panel.add_theme_stylebox_override("panel", style)
	return panel

func _build_hud() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)

	status_label = _label("", 16)
	status_label.position = Vector2(24, 18)
	layer.add_child(status_label)

	var help := _label("WASD move · E interact · 1-9 choose · J journal · R close case · F5 save · F9 load", 14)
	help.position = Vector2(24, 44)
	help.modulate = Color(0.65, 0.68, 0.74)
	layer.add_child(help)

	prompt_label = _label("", 18)
	prompt_label.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	prompt_label.position = Vector2(-260, -70)
	prompt_label.set_deferred("size", Vector2(520, 32))
	prompt_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt_label.modulate = Color(0.95, 0.88, 0.6)
	layer.add_child(prompt_label)

	toast_label = _label("", 17)
	toast_label.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	toast_label.position = Vector2(-400, -170)
	toast_label.set_deferred("size", Vector2(800, 90))
	toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	toast_label.visible = false
	layer.add_child(toast_label)

	dialogue_panel = _panel()
	dialogue_panel.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	dialogue_panel.position = Vector2(0, -300)
	dialogue_panel.size = Vector2(0, 300)
	dialogue_panel.visible = false
	layer.add_child(dialogue_panel)
	var dialogue_box := VBoxContainer.new()
	dialogue_box.add_theme_constant_override("separation", 10)
	dialogue_panel.add_child(dialogue_box)
	speaker_label = _label("", 20)
	speaker_label.modulate = Color(0.85, 0.89, 1.0)
	dialogue_box.add_child(speaker_label)
	dialogue_text = RichTextLabel.new()
	dialogue_text.bbcode_enabled = false
	dialogue_text.fit_content = true
	dialogue_text.custom_minimum_size = Vector2(0, 90)
	dialogue_text.add_theme_font_size_override("normal_font_size", 17)
	dialogue_box.add_child(dialogue_text)
	choices_box = VBoxContainer.new()
	choices_box.add_theme_constant_override("separation", 6)
	dialogue_box.add_child(choices_box)

	journal_panel = _panel()
	journal_panel.set_anchors_preset(Control.PRESET_CENTER_RIGHT)
	journal_panel.position = Vector2(-440, -240)
	journal_panel.size = Vector2(420, 480)
	journal_panel.visible = false
	layer.add_child(journal_panel)
	var journal_box := VBoxContainer.new()
	journal_panel.add_child(journal_box)
	journal_box.add_child(_label("Evidence board", 20))
	journal_text = RichTextLabel.new()
	journal_text.bbcode_enabled = false
	journal_text.scroll_active = true
	journal_text.add_theme_font_size_override("normal_font_size", 16)
	journal_box.add_child(journal_text)

	ending_panel = _panel()
	ending_panel.set_anchors_preset(Control.PRESET_CENTER)
	ending_panel.position = Vector2(-340, -230)
	ending_panel.size = Vector2(680, 460)
	ending_panel.visible = false
	layer.add_child(ending_panel)
	var ending_box := VBoxContainer.new()
	ending_box.add_theme_constant_override("separation", 10)
	ending_panel.add_child(ending_box)
	ending_title = _label("", 22)
	ending_box.add_child(ending_title)
	ending_body = RichTextLabel.new()
	ending_body.custom_minimum_size = Vector2(0, 200)
	ending_body.add_theme_font_size_override("normal_font_size", 17)
	ending_box.add_child(ending_body)
	ending_buttons = VBoxContainer.new()
	ending_box.add_child(ending_buttons)

# -- loop ----------------------------------------------------------------------------------

func _process(delta: float) -> void:
	if camera and player:
		var target := player.position + Vector3(7.0, 9.0, 7.0)
		camera.position = camera.position.lerp(target, clampf(delta * 6.0, 0.0, 1.0))
		camera.look_at(player.position + Vector3(0, 1.0, 0))
	if not dialogue_active and not ending_active and not journal_panel.visible:
		_update_nearest()
		_refresh_status()

func _update_nearest() -> void:
	var best: Dictionary = {}
	var best_distance := INTERACT_RANGE
	for item in interactables:
		var distance := player.position.distance_to(item["position"])
		if distance < best_distance:
			best_distance = distance
			best = item
	nearest = best
	if best.is_empty():
		prompt_label.text = ""
	elif best["kind"] == "npc":
		prompt_label.text = "[E] Speak with %s" % best["name"]
	else:
		var definition: Dictionary = state.object_definition(str(best["id"]))
		prompt_label.text = "[E] %s" % str(definition.get("prompt", "Examine"))

func _physics_process(_delta: float) -> void:
	if dialogue_active or ending_active or journal_panel.visible:
		player.velocity = Vector3.ZERO
		player.move_and_slide()
		return
	var direction := Vector3.ZERO
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		direction.z -= 1
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		direction.z += 1
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		direction.x -= 1
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		direction.x += 1
	player.velocity = direction.normalized() * WALK_SPEED
	player.move_and_slide()

func _unhandled_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo:
		return
	var key: int = event.keycode
	if key == KEY_F5:
		state.player_position = [player.position.x, player.position.y, player.position.z]
		_toast("Saved." if state.save_to(SAVE_PATH) else "Save failed.")
		return
	if key == KEY_F9:
		if state.load_from(SAVE_PATH):
			_restore_position()
			_toast("Loaded.")
		else:
			_toast("No compatible save to load.")
		return
	if key == KEY_J and not ending_active:
		journal_panel.visible = not journal_panel.visible
		_refresh_status()
		return
	if key == KEY_ESCAPE:
		if dialogue_active:
			state.end_dialogue()
			_close_dialogue()
		else:
			journal_panel.visible = false
		return
	if ending_active:
		return
	if dialogue_active:
		if key >= KEY_1 and key <= KEY_9:
			_choose(key - KEY_1)
		return
	if key == KEY_E and not nearest.is_empty():
		_interact(nearest)
	elif key == KEY_R:
		_open_ending()

# -- interaction ---------------------------------------------------------------------------

func _interact(item: Dictionary) -> void:
	if item["kind"] == "npc":
		var npc: Dictionary = {}
		for candidate in state.case_data.get("npcs", []):
			if str(candidate.get("id", "")) == item["id"]:
				npc = candidate
		if state.start_dialogue(str(npc.get("dialogue", ""))):
			_open_dialogue()
		return
	var object_id := str(item["id"])
	if not state.can_use_object(object_id):
		_toast("You need to speak to the patient first.")
		return
	var definition: Dictionary = state.object_definition(object_id)
	var check: Dictionary = definition.get("check", {})
	var result: Dictionary = state.check_results.get(object_id, {})
	if result.is_empty():
		result = rules.skill_check(
			state.stat(str(check.get("stat", "INT"))),
			state.skill(str(check.get("skill", "Program"))),
			int(check.get("dv", 8)), rng
		)
		if result.is_empty():
			_toast("Invalid check configuration.")
			return
		state.check_results[object_id] = result

	var branch: Dictionary = definition.get("on_success", {}) if result["success"] else definition.get("on_failure", {})
	if branch.has("clue"):
		state.add_clue(str(branch["clue"]))
	if branch.has("flag"):
		state.set_flag(str(branch["flag"]))
	if branch.has("complication"):
		state.add_complication(str(branch["complication"]))
	var verdict := "SUCCESS" if result["success"] else "FAILURE"
	_toast("%s · %s modifier %d + %s %d + 2d6 %s = %d vs difficulty %d\n%s" % [
		verdict,
		str(check.get("stat", "INT")), result["modifier"],
		str(check.get("skill", "Program")), result["skill_level"],
		str(result["dice"]), result["total"], result["difficulty"],
		str(branch.get("text", ""))
	])
	_refresh_status()

func _open_dialogue() -> void:
	dialogue_active = true
	dialogue_panel.visible = true
	_refresh_dialogue()

func _refresh_dialogue() -> void:
	speaker_label.text = state.last_speaker
	dialogue_text.text = state.last_text
	for child in choices_box.get_children():
		child.queue_free()
	var available: Array = state.available_choices()
	for position in available.size():
		var button := Button.new()
		button.text = str(available[position]["text"])
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.pressed.connect(_choose.bind(position))
		choices_box.add_child(button)

func _choose(available_index: int) -> void:
	if not dialogue_active:
		return
	if not state.choose(available_index):
		return
	if state.in_dialogue():
		_refresh_dialogue()
	else:
		_close_dialogue()

func _close_dialogue() -> void:
	dialogue_active = false
	dialogue_panel.visible = false

func _open_ending() -> void:
	var endings: Array = state.available_endings()
	if endings.is_empty():
		_toast("The case is not ready to close. Find the medical record first.")
		return
	ending_active = true
	ending_panel.visible = true
	ending_title.text = str(state.case_data.get("resolution", {}).get("prompt", "How does the case end?"))
	for child in ending_buttons.get_children():
		child.queue_free()
	for ending_id in endings:
		var button := Button.new()
		button.text = state.ending_label(ending_id)
		button.pressed.connect(_pick_ending.bind(ending_id))
		ending_buttons.add_child(button)

func _pick_ending(ending_id: String) -> void:
	if not state.choose_ending(ending_id):
		return
	for child in ending_buttons.get_children():
		child.queue_free()
	ending_body.text = state.ending_prose(ending_id) + "\n\nCase state saved."
	state.save_to(SAVE_PATH)
	var restart := Button.new()
	restart.text = "Return to the title screen"
	restart.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://scenes/main.tscn"))
	ending_buttons.add_child(restart)

# -- status --------------------------------------------------------------------------------

func _refresh_status() -> void:
	if status_label == null or state == null:
		return
	var location := _current_location()
	status_label.text = "Dr. Harri Romppainen · %s   |   clues %d/%d   |   journal %d" % [
		location, state.clues.size(), state.case_data.get("clues", {}).size(), state.journal.size()
	]
	if journal_panel.visible:
		_refresh_journal()

func _current_location() -> String:
	for entry in state.case_data.get("locations", []):
		if absf(player.position.z - float(entry.get("z", 0.0))) < 5.5:
			return str(entry.get("name", ""))
	return "Ward"

func _refresh_journal() -> void:
	var lines: Array[String] = []
	lines.append("CHARACTER — " + str(state.character().get("name", "")))
	lines.append(JSON.stringify(state.character().get("stats", {})))
	lines.append(JSON.stringify(state.character().get("skills", {})))
	lines.append("")
	lines.append("CLUES")
	if state.clues.is_empty():
		lines.append("  (none yet)")
	for clue_id in state.clues:
		lines.append("  • %s — %s" % [state.clue_label(clue_id), str(state.case_data.get("clues", {}).get(clue_id, {}).get("prose", ""))])
	lines.append("")
	lines.append("NOTES")
	if state.journal.is_empty():
		lines.append("  (none yet)")
	for note in state.journal:
		lines.append("  • %s" % note)
	if not state.complications.is_empty():
		lines.append("")
		lines.append("COMPLICATIONS")
		for item in state.complications:
			lines.append("  • %s" % item)
	journal_text.text = "\n".join(lines)

func _toast(message: String) -> void:
	toast_label.text = message
	toast_label.visible = true
	var timer := get_tree().create_timer(7.0)
	timer.timeout.connect(func() -> void: toast_label.visible = false)

func _restore_position() -> void:
	var p := state.player_position
	player.position = Vector3(p[0], p[1], p[2])
