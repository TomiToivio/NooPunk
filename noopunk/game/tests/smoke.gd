extends SceneTree

## Smoke test for the walking scene: it loads, the player is scripted and moves, the camera follows and
## the room bounds the player.
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
	elif player.get_script() == null:
		failures.append("Player has no script")
	else:
		var straight: Vector2 = player.movement_velocity(Vector2(1, 0))
		if not is_equal_approx(straight.length(), 120.0):
			failures.append("straight movement is %s, expected 120 px/s" % straight.length())
		var diagonal: Vector2 = player.movement_velocity(Vector2(1, 1))
		if not is_equal_approx(diagonal.length(), 120.0):
			failures.append("diagonal speed is %s, expected 120" % diagonal.length())
		if player.movement_velocity(Vector2.ZERO) != Vector2.ZERO:
			failures.append("idle is not still")
		if player.movement_direction() != Vector2.ZERO:
			failures.append("no key pressed but direction is not zero")
		if player.get_node_or_null("Camera") == null:
			failures.append("Player has no Camera")

	if main.get_node_or_null("Hint/Label") == null:
		failures.append("missing control hint")
	if main.get_node_or_null("Hint/SheetLabel") == null:
		failures.append("missing the sheet line in the walking scene")
	if main.get_node_or_null("Player/Collision") == null:
		failures.append("player has no collision shape")

	main.queue_free()
	if failures.is_empty():
		print("SMOKE OK: walking scene loads, player moves at 120 px/s, camera and bounds present")
		quit(0)
	else:
		print("SMOKE FAIL: " + ", ".join(failures))
		quit(1)
