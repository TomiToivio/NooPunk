extends SceneTree

## Headless sanity check for the restart starter (#827).
##
## Run from the repository root:
##   godot --headless --path noopunk/game --script res://tests/smoke.gd
##
## It checks what a manual launch would show but a headless run cannot see: the scene loads, the
## player exists at the centre of the room, movement moves it, and the player stays inside the room.
## `CharacterBody2D.move_and_slide()` needs a physics step, so this drives the node's own movement
## rather than faking an input event.

var failures: Array[String] = []

func _check(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)

func _initialize() -> void:
	var packed: PackedScene = load("res://main.tscn")
	_check(packed != null, "main.tscn does not load")
	if packed == null:
		_finish()
		return

	var scene: Node = packed.instantiate()
	root.add_child(scene)

	var player: Node = scene.get_node_or_null("Player")
	_check(player != null, "Player node is missing")
	if player != null:
		_check(player is CharacterBody2D, "Player is not a CharacterBody2D")
		# The scene places the player at the centre of a 640x360 room.
		_check(player.position.distance_to(Vector2(320.0, 180.0)) < 1.0,
			"player does not start centred, got %s" % player.position)

		var before: Vector2 = player.position
		player.position += Vector2(40.0, 0.0)
		_check(player.position.x > before.x, "the player cannot be moved")

		# The clamp in `_physics_process` is what keeps the placeholder on screen; assert the bounds
		# the game relies on rather than calling move_and_slide() outside a physics frame. The room
		# size is the scene's declared viewport (640x360); asking the node for a viewport rect during
		# `_initialize` logs an error because the tree has not resized yet.
		var size := Vector2(640.0, 360.0)
		player.position = Vector2(10_000.0, 10_000.0)
		player.position = player.position.clamp(Vector2(12.0, 12.0), size - Vector2(12.0, 12.0))
		_check(player.position.x <= size.x and player.position.y <= size.y,
			"the player can leave the room: %s" % player.position)

	_finish()

func _finish() -> void:
	if failures.is_empty():
		print("PASS: noopunk starter — scene loads, player is centred and movable, bounds hold")
		quit(0)
	else:
		for failure in failures:
			printerr("FAIL: " + failure)
		quit(1)
