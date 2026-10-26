extends SceneTree

const Case = preload("res://src/godot/investigation/case_state.gd")
const Rules = preload("res://src/godot/wn_rules.gd")
var failures := 0

func check(condition: bool, message: String) -> void:
	if not condition:
		push_error(message)
		failures += 1

func _initialize() -> void:
	var rules := Rules.new()
	check(rules.skill_check(14, 1, 8, null, [3, 3]).success, "Threshold success")
	check(not rules.skill_check(14, 1, 8, null, [2, 3]).success, "Threshold failure")
	for score in [3, 7, 8, 13, 14, 17, 18]:
		check(rules.attribute_modifier(score) == int(rules.contract.stats.modifier_table[str(score)]), "Modifier boundary")
	var first := RandomNumberGenerator.new()
	var second := RandomNumberGenerator.new()
	first.seed = 631
	second.seed = 631
	check(rules.skill_check(11, 0, 8, first) == rules.skill_check(11, 0, 8, second), "Seed reproducibility")
	for dice in [[1, 1], [6, 6]]:
		var c := Case.new()
		check(not c.encounter() and not c.can_finish(), "Progression gated")
		c.finish("mundane")
		check(c.state.ending == "", "Premature ending rejected")
		for id in c.content.interviews:
			c.interview(id, 0)
			c.interview(id, 0)
		check(c.state.journal.size() == 3, "Interview entries deduplicated")
		var roll := c.inspect_record(dice)
		check(c.inspect_record([6, 6]) == roll, "No reroll farming")
		check(("audit" in c.state.evidence) == roll.success, "Check changes evidence")
		check(c.encounter() and c.can_finish(), "Both roll paths can finish")
		for ending in ["mundane", "anomalous"]:
			c.finish(ending)
			check(c.state.ending == ending, "Both endings reachable")
		check(c.save_game("user://test-case.json") == OK, "Save succeeds")
		var loaded := Case.new()
		check(loaded.load_game("user://test-case.json") == OK, "Load succeeds")
		check(loaded.state == JSON.parse_string(JSON.stringify(c.state)), "Full state roundtrip")
		var old := loaded.state.duplicate(true)
		var file := FileAccess.open("user://test-case.json", FileAccess.WRITE)
		file.store_string('{"version":99}')
		file.close()
		check(loaded.load_game("user://test-case.json") == ERR_INVALID_DATA and loaded.state == old, "Invalid save leaves state intact")
	DirAccess.remove_absolute("user://test-case.json")
	call_deferred("scene_test")

func scene_test() -> void:
	var scene = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	check(scene.player != null and scene.points.size() == 6, "World loaded")
	scene.active = true
	scene.close_panel()
	for id in ["doctor", "nurse", "patient"]:
		scene.interact(id)
		var choice = scene.stack.get_child(2)
		choice.pressed.emit()
		check(scene.case.state.flags.has(id), "Dialogue button updates state")
		scene.close_panel()
	scene.interact("record")
	scene.interact("window")
	scene.interact("report")
	scene.stack.get_child(2).pressed.emit()
	check(scene.case.state.ending == "mundane", "Report UI completes case")
	scene.player.position = Vector3(0, 0, 7.7)
	scene.close_panel()
	for i in range(30):
		scene.player.velocity = Vector3(0, 0, 5)
		scene.player.move_and_slide()
		await physics_frame
	check(scene.player.position.z < 8, "Boundary collision")
	scene.queue_free()
	await process_frame
	print("Slice tests: %s failures" % failures)
	quit(1 if failures else 0)
