extends SceneTree
# Run: godot --headless --path . --script tests/godot/test_lakkahaltia.gd
func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	assert(scene != null, "Main Godot scene must load")
	var game = scene.instantiate()
	root.add_child(game)
	assert(game.clues.size() == 0, "New case starts without evidence")
	game._note("Evidence A")
	game._note("Evidence A")
	assert(game.clues.size() == 1, "Evidence must be deduplicated")
	game._command("Save")
	game.clues.clear()
	game._command("Load")
	assert(game.clues.size() == 1, "Evidence must survive save/load")
	assert(game.clues[0] == "Evidence A")
	game._act("end_mundane")
	assert(game.outcome != "", "Report selection completes case")
	game.queue_free()
	print("PASS: #631 hospital scene, evidence and save/load")
	quit(0)
