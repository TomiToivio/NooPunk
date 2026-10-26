## The hospital slice (#631): builds the level from `level_hospital.json`, spawns the player, the three
## NPCs and the inspectable props, and wires interactions to the dialogue runner and the HUD.
##
## Everything visible here is a placeholder primitive (BoxMesh + StandardMaterial3D): no third-party
## asset is committed. `docs/godot/ASSET_MANIFEST.md` records which CC0 packs are intended for the next
## milestone and why none of them ships yet.
extends Node3D

const LEVEL_PATH := "res://godot/scenarios/lakkahaltia/level_hospital.json"
const DIALOGUE_PATH := "res://godot/scenarios/lakkahaltia/dialogue.json"
const PLAYER_SPEED := 3.2
const INTERACT_RANGE := 2.6

var layout: Dictionary = {}
var dialogue: Dictionary = {}
var runner: DialogueRunner
var hud: CanvasLayer
var player: CharacterBody3D
var _interactables: Array = []
var _active: Node3D = null

func _ready() -> void:
	layout = _load_json(LEVEL_PATH)
	dialogue = _load_json(DIALOGUE_PATH)
	if GameState.scenario.is_empty():
		GameState.new_case(GameState.run_seed)
	runner = DialogueRunner.new(dialogue.get("nodes", {}), GameState)

	_build_rooms()
	_build_environment()
	_build_props()
	_build_npcs()
	_build_player()
	_build_hud()

func _process(_delta: float) -> void:
	if player == null:
		return
	_active = _nearest_interactable()
	if _active == null:
		hud.set_prompt("")
	elif String(_active.get_meta("kind", "npc")) == "npc":
		hud.set_prompt("Press E to talk to %s" % String(_active.get_meta("label", "someone")))
	else:
		hud.set_prompt("Press E to inspect %s" % String(_active.get_meta("label", "this")))

func _unhandled_input(event: InputEvent) -> void:
	# While a panel is open, 1-9 pick its choices so the keyboard is as usable as the mouse.
	if hud != null and hud.is_dialogue_open() and event is InputEventKey and event.pressed and not event.echo:
		var number := int(event.keycode) - int(KEY_1)
		if number >= 0 and number < hud.choice_count():
			_on_dialogue_choice(number)
			return
	if event is InputEventMouseButton and event.pressed and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		# Clicking back into the world returns look control; clicking a button must not.
		if hud == null or not hud.has_modal_open():
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		return
	if hud != null and hud.has_modal_open():
		return
	if event.is_action_pressed("interact"):
		interact()
	elif event.is_action_pressed("toggle_journal"):
		hud.toggle_journal()
	elif event.is_action_pressed("save_case"):
		var err := GameState.save_to_file()
		GameState.add_journal("Case saved (%s)." % ("ok" if err == OK else "failed: %d" % err))
	elif event.is_action_pressed("end_case"):
		_offer_ending()

## Talk to an NPC or inspect a prop. A prop is a piece of the case: what it yields is data, not script.
func interact() -> void:
	if _active == null or (hud != null and hud.has_modal_open()):
		return
	var kind := String(_active.get_meta("kind", "npc"))
	if kind == "npc":
		var entry := String(_active.get_meta("entry_node", ""))
		if entry == "":
			return
		var node := runner.start(entry)
		hud.show_dialogue(node, runner.choices())
		return

	var interaction := String(_active.get_meta("interaction", ""))
	match interaction:
		"terminal":
			GameState.add_evidence("E1")
			GameState.add_evidence("E5")
			GameState.add_journal("The roster and the 1987 permit register disagree with the study's file.")
		"records":
			if GameState.has_flag("annex_hinted") or GameState.has_evidence("E1"):
				GameState.add_evidence("E4")
				GameState.add_journal("The sealed annex belongs to a research ethics board.")
			else:
				GameState.add_journal("The cabinet is locked; the administrator wants a reason.")
		"drawing":
			GameState.add_evidence("E2")
			GameState.add_journal("A red door, a bog road, a low ridge — drawn twice, by two patients.")

## The choice the player clicked in the dialogue panel.
func _on_dialogue_choice(index: int) -> void:
	var node := runner.choose(index)
	if node.is_empty():
		hud.close_dialogue()
	else:
		hud.show_dialogue(node, runner.choices())

func _offer_ending() -> void:
	if not GameState.ending.is_empty() or (hud != null and hud.has_modal_open()):
		return
	var endings := GameState.available_endings()
	if endings.is_empty():
		GameState.add_journal("The case is not ready to close: the file is still sealed.")
		return
	hud.close_dialogue()
	hud.offer_endings(endings)

func _on_ending_chosen(ending_id: String) -> void:
	GameState.reach_ending(ending_id)
	GameState.add_journal("Case closed: %s" % ending_id)

func _nearest_interactable() -> Node3D:
	var best: Node3D = null
	var best_distance := INTERACT_RANGE
	for candidate in _interactables:
		var node := candidate as Node3D
		if node == null or not is_instance_valid(node):
			continue
		var distance := player.global_position.distance_to(node.global_position)
		if distance < best_distance:
			best = node
			best_distance = distance
	return best

# --- construction -------------------------------------------------------------------------------

func _build_rooms() -> void:
	for room in layout.get("rooms", []):
		var center := _vec(room["center"])
		var size := _vec(room["size"])
		_add_box("Floor_" + String(room["id"]), center - Vector3(0, size.y * 0.5, 0),
			Vector3(size.x, 0.2, size.z), _color(room.get("floor_color", [0.16, 0.16, 0.18])), true)
		_add_box("Ceiling_" + String(room["id"]), center + Vector3(0, size.y * 0.5, 0),
			Vector3(size.x, 0.2, size.z), Color(0.09, 0.09, 0.11), true)
		_build_walls(room)

## Builds the four walls of a room, leaving a real opening wherever `doorways` says a door is.
##
## Two bugs made the first version of this level unplayable: the "gap" segments were sized to exactly
## tile the wall (so every room was sealed), and the corridor's own side walls were solid (so the side
## rooms could not be entered even through a gap). Doors are now data, and every wall is split around
## them.
func _build_walls(room: Dictionary) -> void:
	var room_id := String(room["id"])
	var center := _vec(room["center"])
	var size := _vec(room["size"])
	for wall in ["north", "south", "west", "east"]:
		_build_wall(room_id, center, size, wall, _openings(room_id, wall))

func _openings(room_id: String, wall: String) -> Array:
	var out: Array = []
	for door in layout.get("doorways", []):
		if String(door.get("room", "")) == room_id and String(door.get("wall", "")) == wall:
			out.append({ "offset": float(door.get("offset", 0.0)), "width": float(door.get("width", 1.8)) })
	return out

func _build_wall(room_id: String, center: Vector3, size: Vector3, wall: String, openings: Array) -> void:
	var horizontal := wall == "north" or wall == "south"
	var length := size.x if horizontal else size.z
	var thickness := 0.2
	var fixed := 0.0
	match wall:
		"north": fixed = center.z - size.z * 0.5
		"south": fixed = center.z + size.z * 0.5
		"west": fixed = center.x - size.x * 0.5
		"east": fixed = center.x + size.x * 0.5

	# Openings as intervals measured from the wall's centre, clipped to the wall.
	var cuts: Array = []
	for opening in openings:
		var half := float(opening["width"]) * 0.5
		var offset := float(opening["offset"])
		var a := maxf(-length * 0.5, offset - half)
		var b := minf(length * 0.5, offset + half)
		if b > a:
			cuts.append(Vector2(a, b))
	cuts.sort_custom(func(left: Vector2, right: Vector2) -> bool: return left.x < right.x)

	# Solid runs between the openings.
	var spans: Array = []
	var cursor := -length * 0.5
	for cut in cuts:
		if cut.x > cursor + 0.01:
			spans.append(Vector2(cursor, cut.x))
		cursor = maxf(cursor, cut.y)
	if cursor < length * 0.5 - 0.01:
		spans.append(Vector2(cursor, length * 0.5))

	var wall_color := Color(0.24, 0.25, 0.28)
	var index := 0
	# Lintel above each opening: without it the door is a floor-to-ceiling hole.
	var door_height := 2.15
	var lintel_height := maxf(0.0, size.y - door_height)
	for cut in cuts:
		if lintel_height <= 0.01:
			continue
		var opening_length: float = cut.y - cut.x
		var middle: float = (cut.x + cut.y) * 0.5
		var lintel_y: float = center.y + size.y * 0.5 - lintel_height * 0.5
		var lintel_position := Vector3(center.x + middle, lintel_y, fixed) if horizontal else Vector3(fixed, lintel_y, center.z + middle)
		var lintel_box := Vector3(opening_length, lintel_height, thickness) if horizontal else Vector3(thickness, lintel_height, opening_length)
		_add_box("%s_%s_lintel_%d" % [room_id, wall, index], lintel_position, lintel_box, wall_color, true)
	for span in spans:
		var segment_length: float = span.y - span.x
		var middle: float = (span.x + span.y) * 0.5
		var position := Vector3(center.x + middle, center.y, fixed) if horizontal else Vector3(fixed, center.y, center.z + middle)
		var box := Vector3(segment_length, size.y, thickness) if horizontal else Vector3(thickness, size.y, segment_length)
		_add_box("%s_%s_%d" % [room_id, wall, index], position, box, wall_color, true)
		index += 1

## Ward lighting: without this the whole level rendered black, because nothing lit the meshes.
func _build_environment() -> void:
	var world := WorldEnvironment.new()
	world.name = "WardEnvironment"
	var environment := Environment.new()
	environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color(0.045, 0.05, 0.062)
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color(0.52, 0.57, 0.68)
	environment.ambient_light_energy = 0.42
	world.environment = environment
	add_child(world)

	var sun := DirectionalLight3D.new()
	sun.name = "WardSun"
	sun.light_energy = 0.30
	sun.rotation_degrees = Vector3(-52, -35, 0)
	add_child(sun)

	for room in layout.get("rooms", []):
		var center := _vec(room["center"])
		var size := _vec(room["size"])
		var lamp := OmniLight3D.new()
		lamp.name = "Lamp_" + String(room["id"])
		lamp.position = Vector3(center.x, center.y + size.y * 0.4, center.z)
		lamp.light_energy = 3.2
		lamp.omni_range = maxf(size.x, size.z) * 1.25
		lamp.light_color = Color(0.86, 0.92, 1.0)
		add_child(lamp)

func _build_props() -> void:
	for prop in layout.get("props", []):
		var body := StaticBody3D.new()
		body.name = "Prop_" + String(prop["id"])
		body.position = _vec(prop["position"])
		add_child(body)
		var mesh := MeshInstance3D.new()
		var box := BoxMesh.new()
		box.size = _vec(prop["size"])
		mesh.mesh = box
		var material := StandardMaterial3D.new()
		material.albedo_color = Color(0.38, 0.36, 0.30)
		mesh.material_override = material
		body.add_child(mesh)
		var collider := CollisionShape3D.new()
		var shape := BoxShape3D.new()
		shape.size = box.size
		collider.shape = shape
		body.add_child(collider)
		body.set_meta("kind", "prop")
		body.set_meta("label", String(prop.get("label", prop["id"])))
		body.set_meta("interaction", String(prop.get("interaction", "")))
		_interactables.append(body)

func _build_npcs() -> void:
	for npc in layout.get("npcs", []):
		var body := StaticBody3D.new()
		body.name = "NPC_" + String(npc["id"])
		body.position = _vec(npc["position"]) + Vector3(0, 0.9, 0)
		add_child(body)
		var mesh := MeshInstance3D.new()
		var capsule := CapsuleMesh.new()
		capsule.radius = 0.28
		capsule.height = 1.8
		mesh.mesh = capsule
		var material := StandardMaterial3D.new()
		material.albedo_color = _color(npc.get("color", [0.6, 0.6, 0.6]))
		mesh.material_override = material
		body.add_child(mesh)
		var collider := CollisionShape3D.new()
		var shape := CapsuleShape3D.new()
		shape.radius = 0.28
		shape.height = 1.8
		collider.shape = shape
		body.add_child(collider)

		var label := Label3D.new()
		label.text = String(npc.get("name", npc["id"]))
		label.position = Vector3(0, 1.32, 0)
		label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		label.font_size = 28
		# Explicit pixel size: the default made the names enormous, overlapping each other and the HUD.
		label.pixel_size = 0.0022
		label.outline_size = 8
		label.modulate = Color(0.88, 0.92, 1.0, 0.92)
		label.visibility_range_begin = 2.2
		label.visibility_range_begin_margin = 0.4
		label.visibility_range_end = 9.0
		label.visibility_range_end_margin = 1.5
		label.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
		body.add_child(label)

		body.set_meta("kind", "npc")
		body.set_meta("label", String(npc.get("name", npc["id"])))
		body.set_meta("entry_node", String(dialogue.get("npcs", {}).get(String(npc["id"]), "")))
		_interactables.append(body)

func _build_player() -> void:
	player = CharacterBody3D.new()
	player.name = "Player"
	var spawn: Dictionary = layout.get("spawn", {})
	player.position = _vec(spawn.get("position", [0, 1, 6]))
	# The script goes on before the node enters the tree: `_ready` runs on add_child and needs the camera.
	player.set_script(load("res://godot/scenes/player.gd"))
	player.set("speed", PLAYER_SPEED)

	var collider := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.35
	shape.height = 1.7
	collider.shape = shape
	collider.position = Vector3(0, 0.85, 0)
	player.add_child(collider)

	var camera := Camera3D.new()
	camera.position = Vector3(0, 1.62, 0)
	camera.rotation_degrees = Vector3(-14, float(spawn.get("yaw_degrees", 180.0)), 0)
	camera.current = true
	player.add_child(camera)
	player.set("camera", camera)
	add_child(player)

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.name = "HUD"
	var hud_script := load("res://godot/ui/hud.gd")
	hud.set_script(hud_script)
	add_child(hud)
	# The HUD builds its controls in _ready; connect after it has entered the tree.
	hud.connect("_dialogue_choice", _on_dialogue_choice)
	hud.connect("ending_chosen", _on_ending_chosen)

# --- helpers ------------------------------------------------------------------------------------

func _add_box(node_name: String, center: Vector3, size: Vector3, color: Color, collide: bool) -> void:
	var mesh := MeshInstance3D.new()
	mesh.name = node_name
	var box := BoxMesh.new()
	box.size = size
	mesh.mesh = box
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	mesh.material_override = material
	mesh.position = center
	add_child(mesh)
	if collide:
		var body := StaticBody3D.new()
		body.position = center
		var collider := CollisionShape3D.new()
		var shape := BoxShape3D.new()
		shape.size = size
		collider.shape = shape
		body.add_child(collider)
		add_child(body)

func _add_wall_segment(node_name: String, center: Vector3, size: Vector3, color: Color) -> void:
	_add_box(node_name, center, size, color, true)

func _vec(values: Array) -> Vector3:
	if values.size() < 3:
		return Vector3.ZERO
	return Vector3(float(values[0]), float(values[1]), float(values[2]))

func _color(values: Array) -> Color:
	if values.size() < 3:
		return Color(0.5, 0.5, 0.5)
	return Color(float(values[0]), float(values[1]), float(values[2]))

func _load_json(path: String) -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("level_builder: %s is not a JSON object" % path)
		return {}
	return parsed
