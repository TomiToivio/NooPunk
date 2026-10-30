extends SceneTree
const Attributes = preload("res://attributes.gd")
var failures: Array[String] = []

func check(ok: bool, description: String) -> void:
	if not ok:
		failures.append(description)

func _initialize() -> void:
	var totals := [3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18]
	var expected := [-3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3]
	for i in range(totals.size()):
		check(Attributes.modifier(totals[i]) == expected[i], "incorrect boundary %d" % totals[i])
	check(Attributes.NAMES.size() == 7, "must have exactly seven attributes")
	check(Attributes.DEFINITIONS.size() == 7, "must have exactly seven definitions")
	check(Attributes.DIFFICULTIES.size() == 7, "difficulty reference incomplete")
	var rng := RandomNumberGenerator.new()
	rng.seed = 835
	var first: Dictionary = Attributes.roll_character(rng)
	check(first.size() == 7, "roll must have seven values")
	for value in first.values():
		check(value >= -3 and value <= 3, "out of basic human range")
	var second: Dictionary = Attributes.roll_character(rng)
	check(second.size() == 7, "reroll must keep seven attributes")
	var scene := load("res://main.tscn") as PackedScene
	check(scene != null, "main scene load")
	if scene != null:
		var instance := scene.instantiate()
		root.add_child(instance)
		check(instance.has_method("roll_attributes"), "character creation not present")
		check(instance.get_node_or_null("Player") != null, "movement player missing")
		check(instance.get_node_or_null("CharacterSheetLayer/CharacterSheet") != null, "character sheet missing")
		if instance.has_method("show_sheet"):
			instance.show_sheet(false)
			check(not instance.sheet_open, "continue does not close sheet")
			var chosen: Dictionary = instance.values.duplicate()
			instance.show_sheet(true)
			instance.show_sheet(false)
			check(instance.values == chosen, "attributes not retained through scene navigation")
			instance.roll_attributes()
			check(instance.values.size() == 7, "reroll lost attributes")
	if failures.is_empty():
		print("PASS: #835 seven attributes, conversions, reroll and scene")
		quit(0)
	else:
		for failure in failures:
			printerr("FAIL: " + failure)
		quit(1)
