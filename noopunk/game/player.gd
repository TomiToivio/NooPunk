extends CharacterBody2D
## Placeholder player. Moves with WASD or the arrow keys; nothing else yet.
##
## Keys are read directly rather than through an InputMap so the starter has no hidden configuration to
## learn. When a real input system arrives, this is the one file it replaces.

const SPEED := 120.0
const HALF := 12.0


## Where the keys are asking the player to go. Split out from `_physics_process` so the headless test
## can verify movement without faking key events, and so the first movement rule has one place to
## change.
func movement_direction() -> Vector2:
	var direction := Vector2.ZERO
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		direction.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		direction.x += 1.0
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		direction.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		direction.y += 1.0
	return direction


## A diagonal must not be faster than a straight line, and no input must mean no motion at all.
func movement_velocity(direction: Vector2) -> Vector2:
	return direction.normalized() * SPEED if direction.length() > 0.0 else Vector2.ZERO


func _physics_process(_delta: float) -> void:
	velocity = movement_velocity(movement_direction())
	move_and_slide()

	# Stay inside the room instead of drifting off-screen.
	var size := get_viewport_rect().size
	position = position.clamp(Vector2(HALF, HALF), size - Vector2(HALF, HALF))
