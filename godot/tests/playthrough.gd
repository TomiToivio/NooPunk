## Headless playthrough of the real scene graph (#631).
##
##   godot --headless --path . res://godot/tests/playthrough.tscn
##
## It runs as a *scene* rather than through `--script`, because a `--script` main loop is not a normal
## game start: the project's autoloads (GameState) are not registered, and a playthrough that cannot see
## the autoload would be testing a different program.
##
## Unit suites test the pieces; this drives the assembled level: it instantiates `hospital.tscn`, walks the
## player to a prop and to an NPC, takes the consent branch, and closes the case. It exists because "the
## project opens" is not the same claim as "the case can be played", and CI should be able to tell them
## apart.
extends Node

var _scene: Node = null
var _frame := 0
var _checks: Array = []
var _failures := 0

func _ready() -> void:
	var packed: PackedScene = load("res://godot/scenes/hospital.tscn")
	if packed == null:
		_fail("hospital.tscn could not be loaded")
		_finish()
		return
	_scene = packed.instantiate()
	add_child(_scene)

func _process(_delta: float) -> void:
	_frame += 1
	match _frame:
		2:
			_check("level builds floors", _count_prefix("Floor_") >= 4, "floors=%d" % _count_prefix("Floor_"))
			_check("level builds walls", _count_walls() >= 8, "wall segments=%d" % _count_walls())
			_check("three NPCs", _count_prefix("NPC_") == 3, "npcs=%d" % _count_prefix("NPC_"))
			_check("three props", _count_prefix("Prop_") == 3, "props=%d" % _count_prefix("Prop_"))
			_check("player spawned", _scene.get("player") != null, "player missing")
			_check("HUD present", _scene.get("hud") != null, "hud missing")
			_check("dialogue runner wired", _scene.get("runner") != null, "runner missing")
		3:
			_walk_to("Prop_reception_terminal")
		4:
			_scene.call("interact")
		5:
			_check("terminal grants E1", GameState.has_evidence("E1"), "E1 missing")
			_check("terminal grants the permit record", GameState.has_evidence("E5"), "E5 missing")
			_check("evidence reached the journal", GameState.journal.size() >= 1, "journal empty")
			_walk_to("NPC_doctor")
		6:
			_scene.call("interact")
		7:
			var runner = _scene.get("runner")
			_check("talking to the doctor opens his node",
				String(runner.get("current_id")) == "doctor_1", String(runner.get("current_id")))
		8:
			# Choice 2 is the consent line: no dice, a flag, and a closing node.
			_scene.call("_on_dialogue_choice", 2)
		9:
			_check("consent recorded", GameState.has_flag("safeguarding_first"), "flag missing")
		10:
			GameState.set_flag("annex_seen")
			GameState.set_flag("place_anchored")
			_scene.call("_offer_ending")
		11:
			var hud = _scene.get("hud")
			_check("both endings offered", GameState.available_endings().size() == 2,
				"endings=%d" % GameState.available_endings().size())
			_check("ending panel is visible", bool(hud.get("_ending_panel").visible), "panel hidden")
			_scene.call("_on_ending_chosen", "anomalous")
		12:
			_check("ending recorded", String(GameState.ending.get("id", "")) == "anomalous",
				String(GameState.ending.get("id", "")))
			_finish()

func _walk_to(node_name: String) -> void:
	var target := _find(node_name)
	var player: Node3D = _scene.get("player")
	if target == null or player == null:
		_fail("could not walk to %s" % node_name)
		return
	player.global_position = target.global_position + Vector3(0, 1.0, 0.8)

func _find(node_name: String) -> Node3D:
	for child in _scene.get_children():
		if String(child.name) == node_name:
			return child as Node3D
	return null

## Walls are the unnamed StaticBody3D children the builder creates per room side; floors, NPCs and props
## have their own prefixes, so they are excluded rather than counted twice.
func _count_walls() -> int:
	var count := 0
	for child in _scene.get_children():
		var child_name := String(child.name)
		if child_name.begins_with("Floor_") or child_name.begins_with("Ceiling_"):
			continue
		if child_name.begins_with("NPC_") or child_name.begins_with("Prop_"):
			continue
		if child is StaticBody3D:
			count += 1
	return count

func _count_prefix(prefix: String) -> int:
	var count := 0
	for child in _scene.get_children():
		var child_name := String(child.name)
		if child_name.begins_with(prefix):
			count += 1
	return count

func _check(label: String, ok: bool, detail: String = "") -> void:
	_checks.append([label, ok, detail])
	if not ok:
		_failures += 1
	print("  %s  %s%s" % ["PASS" if ok else "FAIL", label, "" if ok else "  — " + detail])

func _fail(label: String) -> void:
	_checks.append([label, false, label])
	_failures += 1
	print("  FAIL  %s" % label)

func _finish() -> void:
	print("%d checks, %d failed" % [_checks.size(), _failures])
	get_tree().quit(1 if _failures > 0 else 0)
