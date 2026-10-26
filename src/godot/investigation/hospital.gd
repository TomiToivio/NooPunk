extends Node3D

const Case = preload("res://src/godot/investigation/case_state.gd")
var case := Case.new()
var player: CharacterBody3D
var camera: Camera3D
var points: Dictionary = {}
var panel: PanelContainer
var stack: VBoxContainer
var prompt: Label
var active := false

func _ready() -> void:
	build_world()
	build_ui()
	menu()

func box(at: Vector3, size: Vector3, color: Color, solid: bool = true) -> void:
	var mesh := MeshInstance3D.new()
	var shape := BoxMesh.new()
	shape.size = size
	mesh.mesh = shape
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	mesh.material_override = material
	mesh.position = at
	add_child(mesh)
	if solid:
		var body := StaticBody3D.new()
		var collision := CollisionShape3D.new()
		var bounds := BoxShape3D.new()
		bounds.size = size
		collision.shape = bounds
		body.position = at
		body.add_child(collision)
		add_child(body)

func label_at(text: String, at: Vector3) -> void:
	var label := Label3D.new()
	label.text = text
	label.position = at
	label.font_size = 36
	label.pixel_size = 0.008
	label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(label)

func build_world() -> void:
	box(Vector3(0, -0.3, 0), Vector3(18, 0.5, 16), Color("b3b8b0"))
	for wall in [[Vector3(-9, 1, 0), Vector3(0.3, 2, 16)], [Vector3(9, 1, 0), Vector3(0.3, 2, 16)], [Vector3(0, 1, -8), Vector3(18, 2, 0.3)], [Vector3(0, 0.3, 8), Vector3(18, 0.6, 0.3)]]:
		box(wall[0], wall[1], Color("657970"))
	# Open doorways connect the rooms to a central corridor.
	for x in [-2.5, 2.5]:
		for z in [-5.5, 5.5]:
			box(Vector3(x, 0.5, z), Vector3(0.2, 1, 4.5), Color("798b82"))
	for x in [-5.8, 5.8]:
		box(Vector3(x, 0.5, 0), Vector3(6, 1, 0.2), Color("798b82"))
	label_at("RECEPTION", Vector3(-5, 0.2, 6))
	label_at("CONSULTATION", Vector3(5, 0.2, -6))
	label_at("RECORDS", Vector3(-5, 0.2, -6))
	label_at("ENTRANCE", Vector3(0, 0.2, 7))
	for id in case.content.interviews:
		var npc: Dictionary = case.content.interviews[id]
		var pos := Vector3(npc.position[0], 0.7, npc.position[2])
		points[id] = pos
		box(pos, Vector3(0.65, 1.4, 0.65), Color("647d91"))
		label_at(npc.name, pos + Vector3(0, 1.2, 0))
	points.record = Vector3(-7, 0.6, -5)
	points.window = Vector3(7, 0.6, -5)
	points.report = Vector3(5, 0.6, 4)
	for id in ["record", "window", "report"]:
		box(points[id], Vector3(1.2, 1, 0.6), Color("b69d70"))
		label_at(id.capitalize(), points[id] + Vector3(0, 1, 0))
	player = CharacterBody3D.new()
	var collision := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.3
	capsule.height = 1.6
	collision.shape = capsule
	collision.position.y = 0.8
	player.add_child(collision)
	var visual := MeshInstance3D.new()
	var mesh := CapsuleMesh.new()
	mesh.radius = 0.3
	mesh.height = 1.6
	visual.mesh = mesh
	visual.position.y = 0.8
	player.add_child(visual)
	add_child(player)
	player.position = Vector3(0, 0, 6)
	camera = Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 23
	camera.position = Vector3(17, 22, 22)
	add_child(camera)
	camera.look_at(Vector3.ZERO)
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-60, -30, 0)
	add_child(light)
	var env := WorldEnvironment.new()
	env.environment = Environment.new()
	env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.environment.ambient_light_color = Color.WHITE
	env.environment.ambient_light_energy = 0.7
	add_child(env)

func build_ui() -> void:
	var canvas := CanvasLayer.new()
	add_child(canvas)
	prompt = Label.new()
	prompt.position = Vector2(24, 20)
	canvas.add_child(prompt)
	panel = PanelContainer.new()
	panel.position = Vector2(260, 120)
	panel.custom_minimum_size = Vector2(760, 0)
	canvas.add_child(panel)
	stack = VBoxContainer.new()
	stack.add_theme_constant_override("separation", 12)
	panel.add_child(stack)

func show_text(title: String, body: String) -> void:
	for child in stack.get_children():
		stack.remove_child(child)
		child.queue_free()
	panel.show()
	var heading := Label.new()
	heading.text = title
	heading.add_theme_font_size_override("font_size", 24)
	stack.add_child(heading)
	var text := RichTextLabel.new()
	text.text = body
	text.custom_minimum_size = Vector2(720, 170)
	stack.add_child(text)

func button(text: String, action: Callable) -> void:
	var control := Button.new()
	control.text = text
	control.pressed.connect(action)
	stack.add_child(control)

func close_panel() -> void:
	panel.hide()

func menu() -> void:
	show_text("NoöPunk", case.content.title + "\nA hospital investigation before the NHI Crisis.\nDraft playable case • offline • Without Number baseline\n\nInterview the doctor, nurse and patient. Inspect the authorized record, visit the window, then file a report.")
	button("New case", func(): case.reset(); player.position = Vector3(0, 0, 6); active = true; close_panel())
	button("Load case", load_case)
	if active:
		button("Resume", close_panel)

func nearest() -> String:
	var result := ""
	var distance := 2.2
	for id in points:
		var delta: float = player.position.distance_to(points[id])
		if delta < distance:
			distance = delta
			result = id
	return result

func _physics_process(_delta: float) -> void:
	if not active or panel.visible:
		return
	var input := Vector2(float(Input.is_physical_key_pressed(KEY_D)) - float(Input.is_physical_key_pressed(KEY_A)), float(Input.is_physical_key_pressed(KEY_S)) - float(Input.is_physical_key_pressed(KEY_W)))
	input += Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var right := camera.global_basis.x
	var forward := camera.global_basis.z
	right.y = 0
	forward.y = 0
	var direction := (right.normalized() * input.x + forward.normalized() * input.y).limit_length()
	player.velocity = direction * 4
	player.velocity.y = -2
	player.move_and_slide()
	prompt.text = "WASD / arrows: move   E: interact   J: journal   C: character   F5: save   F9: load   Esc: menu\n" + ("E — " + nearest().capitalize() if nearest() != "" else "Find witnesses and compare their accounts.")

func _unhandled_key_input(event: InputEvent) -> void:
	if not event.is_pressed() or event.is_echo():
		return
	if event.keycode == KEY_ESCAPE:
		menu()
	elif active and event.keycode == KEY_F5:
		case.state.position = [player.position.x, player.position.y, player.position.z]
		var error := case.save_game()
		show_text("Save", "Case saved." if error == OK else "Save failed: " + error_string(error))
		button("Continue", close_panel)
	elif event.keycode == KEY_F9:
		load_case()
	elif active and not panel.visible:
		match event.keycode:
			KEY_E: interact(nearest())
			KEY_J: journal()
			KEY_C:
				show_text("Harri Romppainen • demo investigation sheet", JSON.stringify(case.state.character, "  "))
				button("Continue", close_panel)

func load_case() -> void:
	var error := case.load_game()
	if error == OK:
		var p: Array = case.state.position
		player.position = Vector3(p[0], p[1], p[2])
		active = true
		close_panel()
	else:
		show_text("Load", "No usable save: " + error_string(error))
		button("Back", menu)

func interact(id: String) -> void:
	if case.content.interviews.has(id):
		var npc: Dictionary = case.content.interviews[id]
		show_text(npc.name, npc.intro)
		for index in range(npc.choices.size()):
			button(npc.choices[index].label, func():
				show_text(npc.name, case.interview(id, index))
				button("Continue", close_panel))
		button("Leave the interview", close_panel)
	elif id == "record":
		var roll := case.inspect_record()
		show_text("Authorized record • INT / Program", case.content.evidence.record.text + "\n\n2d6 %s + modifier %s + skill %s = %s vs %s\n%s" % [roll.dice, roll.modifier, roll.skill_level, roll.total, roll.difficulty, "Success: clock discrepancy preserved in journal." if roll.success else "Inconclusive: ask the nurse; no repeat roll."])
		button("Continue", close_panel)
	elif id == "window":
		show_text("Consultation-room window", case.content.evidence.reflection.text if case.encounter() else "Streetlights and your reflection. Interview the patient and read the record before comparing this view with their account.")
		button("Continue", close_panel)
	elif id == "report":
		show_text("Case report", case.content.endings[case.state.ending] if case.state.ending != "" else "Choose a working interpretation. Neither report establishes the nature of the event.")
		for kind in ["mundane", "anomalous"]:
			button("File " + kind + " hypothesis", func(): show_text("Case report", case.finish(kind)); button("Continue investigating", close_panel))
		button("Continue investigating", close_panel)

func journal() -> void:
	var text := ""
	for id in case.state.evidence:
		var clue: Dictionary = case.content.evidence[id]
		text += clue.title + "\n" + clue.text + "\nMundane: " + clue.mundane + "\nAnomalous: " + clue.anomalous + "\n\n"
	for line in case.state.journal:
		text += line + "\n\n"
	show_text("Evidence & witness journal", text if text != "" else "No evidence collected yet.")
	button("Continue", close_panel)
