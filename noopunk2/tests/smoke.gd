extends SceneTree

## Headless sanity check for the restart starter (#827).
##
## Run from the repository root:
##   godot --headless --path noopunk2 --script res://tests/smoke.gd
##
## It checks the things a manual launch would show but a headless run cannot see: the scene loads,
## the player exists at the centre of the room, movement moves it, the room bounds hold, and the
## camera is present. It is deliberately not a test framework - this project has one scene.

var failures: Array[String] = []

func _check(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)

func _initialize() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	_check(packed != null, "main.tscn does not load")
	if packed == null:
		_finish()
		return

	var scene: Node = packed.instantiate()
	root.add_child(scene)

	var player: Node = scene.get_node_or_null("Player")
	_check(player != null, "Player node is missing")
	var camera: Node = scene.get_node_or_null("Camera2D")
	_check(camera != null, "Camera2D node is missing")
	var hint: Node = scene.get_node_or_null("UI/Hint")
	_check(hint != null, "UI/Hint node is missing")

	if player != null:
		# Centred means centre-minus-half-size, not the centre coordinate.
		var expected: Vector2 = Vector2(480.0, 270.0) - Vector2(12.0, 12.0)
		var start: Vector2 = player.position
		_check(start.distance_to(expected) < 1.0,
			"player does not start centred, got %s want %s" % [start, expected])

		var moved: Vector2 = player.apply_movement(Vector2.RIGHT, 0.5)
		_check(moved.x > start.x, "moving right did not change x")

		var clamped: Vector2 = player.apply_movement(Vector2.RIGHT, 100.0)
		_check(clamped.x <= player.room.end.x - player.size.x + 0.001,
			"player left the room on the right: %s" % clamped)

		var up: Vector2 = player.apply_movement(Vector2.UP, 100.0)
		_check(up.y >= player.room.position.y - 0.001,
			"player left the room at the top: %s" % up)

	_finish()

func _finish() -> void:
	if failures.is_empty():
		print("PASS: noopunk2 starter — scene loads, player moves, bounds hold, camera present")
		quit(0)
	else:
		for failure in failures:
			printerr("FAIL: " + failure)
		quit(1)
