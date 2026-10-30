extends ColorRect

## The player placeholder.
##
## Movement is deliberately trivial: this milestone exists so that the next rule Tomi writes has
## somewhere to be played. No stats, no collision layers, no physics body - a rectangle that stays
## inside the room.
##
## `apply_movement` is a separate function from `_process` so the behaviour can be checked headlessly:
## a smoke test cannot press keys, but it can call the movement step directly.

const SPEED := 220.0
const SIZE := Vector2(24.0, 24.0)

@export var room := Rect2(0.0, 0.0, 960.0, 540.0)

func _ready() -> void:
	size = SIZE
	# The starting position lives in `main.tscn` rather than here: a headless smoke test can see a
	# scene's placement but not a _ready() assignment made only in code, and the run that matters
	# most is the one that can fail.

func _process(delta: float) -> void:
	var direction := Vector2(
		Input.get_axis("ui_left", "ui_right"),
		Input.get_axis("ui_up", "ui_down")
	)
	apply_movement(direction, delta)

## Move by `direction` (each axis -1..1) for `delta` seconds, keeping the rectangle inside `room`.
## Returns the resulting position so a test can assert it without reading the node afterwards.
func apply_movement(direction: Vector2, delta: float) -> Vector2:
	if direction.length() > 1.0:
		direction = direction.normalized()
	position += direction * SPEED * delta
	position.x = clampf(position.x, room.position.x, room.end.x - SIZE.x)
	position.y = clampf(position.y, room.position.y, room.end.y - SIZE.y)
	return position
