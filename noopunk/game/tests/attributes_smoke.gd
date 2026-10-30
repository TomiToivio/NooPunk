extends SceneTree

## Headless checks for #835: the 3d6 table, the seven attributes, and the creation screen.
##
##   godot --headless --path noopunk/game --script res://tests/attributes_smoke.gd
##
## Two phases. The rule checks run in `_initialize()`, but anything that instantiates a scene runs on
## the first frame: `add_child()` defers `_ready()` until the main loop iterates, so a Control would
## report zero children and the screen would look broken when it is not.

const Attributes = preload("res://attributes.gd")

var failures: Array[String] = []
var _scene_pending := false
var _finished := false

func check(ok: bool, description: String) -> void:
	if not ok:
		failures.append(description)

func _initialize() -> void:
	var totals := [3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18]
	var expected := [-3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3]
	for i in range(totals.size()):
		check(Attributes.modifier_for(totals[i]) == expected[i], "incorrect boundary %d" % totals[i])
	check(Attributes.attribute_names().size() == 7, "must have seven attributes")
	check(Attributes.difficulty_scale().size() == 7, "difficulty reference incomplete")

	var rng := RandomNumberGenerator.new()
	rng.seed = 835
	var rolled: Dictionary = Attributes.roll(rng)
	check(rolled.size() == 7, "roll must have seven attributes")
	var values := Attributes.sheet(rolled)
	for value in values.values():
		check(Attributes.is_human_value(value), "outside human range")

	_scene_pending = true

func _process(_delta: float) -> bool:
	if not _scene_pending or _finished:
		return false
	_scene_pending = false

	var creation := load("res://creation.tscn") as PackedScene
	check(creation != null, "creation scene load")
	if creation != null:
		var instance: Node = creation.instantiate()
		root.add_child(instance)
		check(instance.has_method("row_count"), "the creation screen has no script attached")
		check(instance.row_count() == 7, "seven attribute rows")
		check(instance.sheet_values().size() == 7, "creation must roll seven attributes")
		var shown: Dictionary = instance.sheet_values()
		for value in shown.values():
			check(Attributes.is_human_value(value), "creation showed a value outside the human range")
		instance.queue_free()

	var walking := load("res://main.tscn") as PackedScene
	check(walking != null, "walking scene load")
	if walking != null:
		var instance: Node = walking.instantiate()
		root.add_child(instance)
		check(instance.get_node_or_null("Player") != null, "movement player missing")
		instance.queue_free()

	_finish()
	return false

func _finish() -> void:
	_finished = true
	if failures.is_empty():
		print("PASS: #835 conversion, creation, and scene")
		quit(0)
	else:
		for failure in failures:
			printerr("FAIL: " + failure)
		quit(1)
