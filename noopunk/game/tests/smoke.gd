extends SceneTree

## Headless smoke test for the starter: the scene loads, holds a moving player and a camera, the
## movement function is pure, and the room bounds clamp the player.
##
##   godot --headless --path noopunk/game --script res://tests/smoke.gd

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
			if not is_equal_approx(straight.x, 120.0) or not is_equal_approx(straight.y, 0.0):
				failures.append("straight movement is %s, expected (120, 0)" % straight)
			var diagonal: Vector2 = player.movement_velocity(Vector2(1, 1))
			if not is_equal_approx(diagonal.length(), 120.0):
				failures.append("diagonal speed is %s, expected 120" % diagonal.length())
			if player.movement_velocity(Vector2.ZERO) != Vector2.ZERO:
				failures.append("idle is not still")
		if player.get_node_or_null("Camera") == null:
			failures.append("Player has no Camera")
		# Bounds are a clamp in code, not wall nodes: push the player out and step once.
		player.position = Vector2(100000, 100000)
		player._physics_process(0.0)
		var size: Vector2 = player.get_viewport_rect().size
		if player.position.x > size.x or player.position.y > size.y:
			failures.append("player was not clamped inside the room")
	if main.get_node_or_null("Hint") == null:
		failures.append("missing Hint label")

	main.queue_free()
	if failures.is_empty():
		print("SMOKE OK: scene loads, player moves, camera and bounds present")
		quit(0)
	else:
		print("SMOKE FAIL: " + ", ".join(failures))
		quit(1)
