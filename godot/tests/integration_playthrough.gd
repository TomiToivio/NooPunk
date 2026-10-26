extends SceneTree

## Headless integration playthrough of the real hospital scene (issue #631).
##
## Unit suites call the state directly; this script boots the scene the player boots, walks the
## first-person body to each prop and NPC by moving it, and checks that the interactions the level
## wires actually reach the game state. It exists because the slice once passed its data suite while
## being unplayable: sealed rooms, an unlit level, skills that never reached a roll, and evidence whose
## flags were never applied.
##
##   godot --headless --path . --script res://godot/tests/integration_playthrough.gd

var ward: Node = null
var state: Node = null
var frame := 0
var step := 0
var problems: Array[String] = []

func _initialize() -> void:
	change_scene_to_file("res://godot/scenes/hospital.tscn")

func _problem(text: String) -> void:
	problems.append(text)

func _place_near(node: Node3D) -> void:
	# Stand a step away from the target, inside interaction range, and let the level's _process pick it.
	ward.player.global_position = node.global_position + Vector3(0.0, 0.0, 1.2)

func _find(kind: String, interaction_or_name: String) -> Node3D:
	for item in ward._interactables:
		if String(item.get_meta("kind", "")) == kind and String(item.get_meta("interaction", item.get_meta("label", ""))) == interaction_or_name:
			return item
		if String(item.get_meta("kind", "")) == kind and String(item.name).ends_with(interaction_or_name):
			return item
	return null

func _process(_delta: float) -> bool:
	frame += 1
	match step:
		0:
			if frame < 6:
				return false
			ward = current_scene
			state = root.get_node_or_null("GameState")
			if ward == null or state == null:
				_problem("the hospital scene or GameState did not load")
				return _finish()
			if ward._interactables.size() != 6:
				_problem("expected 3 NPCs and 3 props, found %d interactables" % ward._interactables.size())
			if ward.player.global_position.y < -1.0:
				_problem("the player fell out of the level (y=%.2f)" % ward.player.global_position.y)
			step = 1
			frame = 0
		1:
			if frame < 3:
				return false
			var terminal := _find("prop", "terminal")
			if terminal == null:
				_problem("the reception terminal is missing")
				return _finish()
			_place_near(terminal)
			step = 2
			frame = 0
		2:
			if frame < 3:
				return false
			if ward._active == null:
				_problem("walking up to the terminal did not make it the active interactable")
			else:
				ward.interact()
			if not state.has_evidence("E1"):
				_problem("reading the terminal did not produce E1")
			if not state.has_evidence("E5"):
				_problem("reading the terminal did not produce E5")
			if not state.has_flag("place_anchored"):
				_problem("E5 did not apply its place_anchored flag")
			var cabinet := _find("prop", "records")
			if cabinet == null:
				_problem("the records cabinet is missing")
				return _finish()
			_place_near(cabinet)
			step = 3
			frame = 0
		3:
			if frame < 3:
				return false
			ward.interact()
			if not state.has_evidence("E4"):
				_problem("the unlocked cabinet did not produce E4")
			if not state.has_flag("annex_seen"):
				_problem("E4 did not apply annex_seen, so no ending can unlock")
			var desk := _find("prop", "drawing")
			if desk == null:
				_problem("the consultation desk is missing")
				return _finish()
			_place_near(desk)
			step = 4
			frame = 0
		4:
			if frame < 3:
				return false
			ward.interact()
			if not state.has_evidence("E2"):
				_problem("the patient drawing did not produce E2")
			var doctor := _find("npc", "doctor")
			if doctor == null:
				_problem("the doctor is missing")
				return _finish()
			_place_near(doctor)
			step = 5
			frame = 0
		5:
			if frame < 3:
				return false
			ward.interact()
			if not ward.hud.is_dialogue_open():
				_problem("talking to the doctor did not open the dialogue panel")
			if ward.hud.choice_count() < 2:
				_problem("the doctor offered %d choices, expected at least 2" % ward.hud.choice_count())
			ward.hud.close_dialogue()
			var endings: Array = state.available_endings()
			if endings.size() != 2:
				_problem("expected both ambiguous endings, found %d" % endings.size())
			ward._offer_ending()
			if ward.hud._ending_buttons.get_child_count() < 3:
				_problem("the ending panel did not offer endings and a way to back out")
			# A modal must stop world interaction, even if interact() is called directly.
			var count_before: int = state.journal.size()
			ward.interact()
			if state.journal.size() != count_before:
				_problem("world interaction remained active behind the ending panel")
			# Backing out must not permanently consume the opportunity to end the case.
			ward.hud._ending_buttons.get_child(0).pressed.emit()
			if ward.hud.has_modal_open():
				_problem("Not yet did not close the ending panel")
			ward._offer_ending()
			if not ward.hud.has_modal_open() or ward.hud._ending_buttons.get_child_count() < 3:
				_problem("ending selection cannot be reopened after Not yet")
			step = 6
			frame = 0
		6:
			if frame < 3:
				return false
			return _finish()
	return false

func _finish() -> bool:
	if problems.is_empty():
		print("PLAYTHROUGH_OK evidence=%d endings=%d" % [state.evidence.size(), state.available_endings().size()])
		print("PLAYTHROUGH_EVIDENCE %s" % str(state.evidence))
		quit(0)
	else:
		for problem in problems:
			print("  FAIL " + problem)
		print("PLAYTHROUGH_FAILED %d problem(s)" % problems.size())
		quit(1)
	return true
