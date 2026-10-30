extends SceneTree

## Headless smoke test for the restart starter: the scene must load, hold a moving player and a
## camera, and the movement must be a pure function of the input vector.
##
##   godot --headless --path restart/game --script res://tests/smoke.gd

func _initialize() -> void:
	var failures: Array = []
	var scene: PackedScene = load("res://main.tscn")
	if scene == null:
		print("SMOKE FAIL: main.tscn did not load")
		quit(1)
		return
	var main := scene.instantiate()
	root.add_child(main)

	var player := main.get_node_or_null("Player")
	if player == null:
		failures.append("no Player node")
	else:
		if player.get_script() == null:
			failures.append("Player has no script")
		else:
			var straight: Vector2 = player.movement_velocity(Vector2(1, 0))
			if not is_equal_approx(straight.x, 220.0) or not is_equal_approx(straight.y, 0.0):
				failures.append("straight movement is %s, expected (220, 0)" % straight)
			var diagonal: Vector2 = player.movement_velocity(Vector2(1, 1))
			if not is_equal_approx(diagonal.length(), 220.0):
				failures.append("diagonal speed is %s, expected 220" % diagonal.length())
			if player.movement_velocity(Vector2.ZERO) != Vector2.ZERO:
				failures.append("idle is not still")
		if player.get_node_or_null("Camera") == null:
			failures.append("Player has no Camera")

	for wall in ["WallTop", "WallBottom", "WallLeft", "WallRight"]:
		if main.get_node_or_null(wall) == null:
			failures.append("missing %s" % wall)
	if main.get_node_or_null("Hint") == null:
		failures.append("missing Hint label")

	main.queue_free()
	if failures.is_empty():
		print("SMOKE OK: scene loads, player moves, camera and bounds present")
		quit(0)
	else:
		print("SMOKE FAIL: " + ", ".join(failures))
		quit(1)
