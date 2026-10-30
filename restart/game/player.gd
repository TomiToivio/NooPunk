extends CharacterBody2D

## The player placeholder: a shape that moves. Nothing here knows about rules.
##
## Movement is a pure function of the input vector so the headless smoke test can check it without
## faking key events — and so the first rule that touches movement has one place to change.

const SPEED := 220.0


func movement_velocity(direction: Vector2, speed: float = SPEED) -> Vector2:
	# A diagonal must not be faster than a straight line.
	return direction.normalized() * speed if direction.length() > 0.0 else Vector2.ZERO


func _physics_process(_delta: float) -> void:
	var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = movement_velocity(direction)
	move_and_slide()
