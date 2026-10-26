## Player controller for the slice (#631): first-person walk, mouse look, gravity, and nothing else.
##
## Deliberately small: combat, hacking, PSI and inventory are seams for later milestones, not unfinished
## features here. The camera is a child of the body, so movement and look stay in one place.
extends CharacterBody3D

const MOUSE_SENSITIVITY := 0.0022
const GRAVITY := 18.0

@export var speed: float = 3.2
var camera: Camera3D
var _pitch: float = -0.24

func _ready() -> void:
	camera = get("camera") as Camera3D
	if camera == null:
		camera = get_node_or_null("Camera3D") as Camera3D
	if camera != null:
		camera.rotation.x = _pitch
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * MOUSE_SENSITIVITY)
		_pitch = clampf(_pitch - event.relative.y * MOUSE_SENSITIVITY, -1.2, 0.6)
		if camera != null:
			camera.rotation.x = _pitch
	elif event.is_action_pressed("ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
	else:
		velocity.y = 0.0

	var input_vector := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction := (transform.basis * Vector3(input_vector.x, 0.0, input_vector.y)).normalized()
	velocity.x = direction.x * speed
	velocity.z = direction.z * speed
	move_and_slide()
