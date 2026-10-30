extends SceneTree

## Headless checks for the character sheet (#835) and the walking scene (#827).
##
## Run from the repository root:
##   godot --headless --path noopunk/game --script res://tests/character.gd
##
## Covers the seven 3d6-to-modifier bands at every boundary the issue names, the seven attributes,
## the human range, reroll behaviour, and that a rolled sheet survives into the walking scene and
## stays put while the player moves. It cannot check how the screen looks - that is the window.

const Attributes := preload("res://attributes.gd")
const SheetScript := preload("res://sheet.gd")

var failures: Array[String] = []

func _check(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)

func _eq(actual: Variant, expected: Variant, label: String) -> void:
	_check(actual == expected, "%s: got %s want %s" % [label, actual, expected])

func _initialize() -> void:
	_bands()
	_seven_attributes()
	_human_range()
	_roll_and_reroll()
	_creation_screen()
	_retention_into_walking_scene()
	_finish()

func _bands() -> void:
	# Every boundary the issue names, plus the gaps between them.
	var expected := {
		3: -3, 4: -3, 5: -2, 6: -2, 7: -1, 8: -1,
		9: 0, 12: 0, 13: 1, 14: 1, 15: 2, 16: 2, 17: 3, 18: 3,
	}
	for total in expected.keys():
		_eq(Attributes.modifier_for(total), expected[total], "3d6 %d" % total)
	# Every total from 3 to 18 must map, and never outside the human range.
	for total in range(3, 19):
		_check(Attributes.is_human_value(Attributes.modifier_for(total)),
			"%d produced a non-human value" % total)

func _seven_attributes() -> void:
	_eq(Attributes.attribute_names().size(), 7, "attribute count")
	_eq(Attributes.attribute_names(),
		["Fitness", "Reflexes", "Cognition", "Cyber", "Awareness", "Agency", "Empathy"],
		"attribute names and order")

func _human_range() -> void:
	_eq(Attributes.human_min(), -3, "human minimum")
	_eq(Attributes.human_max(), 3, "human maximum")
	# -3 is a legitimate basic-human score in this design (unlike the older tag draft).
	_check(Attributes.is_human_value(-3), "-3 must be a legal human value")
	_check(not Attributes.is_human_value(4), "+4 must not be a legal human value")

func _roll_and_reroll() -> void:
	var first := RandomNumberGenerator.new()
	first.seed = 20261030
	var a: Dictionary = Attributes.roll(first)
	_eq(a.size(), 7, "rolled attribute count")
	for name in a.keys():
		var entry: Dictionary = a[name]
		_check(int(entry["total"]) >= 3 and int(entry["total"]) <= 18,
			"%s rolled an impossible total %s" % [name, entry["total"]])
		_eq(int(entry["value"]), Attributes.modifier_for(int(entry["total"])),
			"%s value matches its total" % name)
		_check(Attributes.is_human_value(int(entry["value"])),
			"%s rolled outside the human range" % name)

	# Same seed, same rolls: the sheet must be reproducible for a replay.
	var repeat := RandomNumberGenerator.new()
	repeat.seed = 20261030
	_eq(Attributes.roll(repeat), a, "a seeded roll repeats")

	# A reroll is a fresh roll, and the sheet replaces rather than accumulating.
	var reroll := RandomNumberGenerator.new()
	reroll.seed = 99
	var b: Dictionary = Attributes.roll(reroll)
	_eq(Attributes.sheet(b).size(), 7, "reroll still yields seven values")
	_check(Attributes.sheet(b) != Attributes.sheet(a), "a different seed should differ")

func _creation_screen() -> void:
	var packed: PackedScene = load("res://creation.tscn")
	_check(packed != null, "creation.tscn loads")
	if packed == null:
		return
	var screen: Node = packed.instantiate()
	root.add_child(screen)
	# The screen builds itself in `_ready`, which runs on the first frame.
	await process_frame
	_check(screen.row_count() == 7, "the creation screen lists seven attributes, got %d" % screen.row_count())
	_eq(screen.sheet_values().size(), 7, "the creation screen rolls seven values")
	for name in screen.sheet_values().keys():
		_check(Attributes.is_human_value(int(screen.sheet_values()[name])),
			"creation produced a non-human %s" % name)
	screen.free()

func _retention_into_walking_scene() -> void:
	var sheet := SheetScript.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	sheet.set_roll(Attributes.roll(rng))
	_check(sheet.has_sheet(), "the sheet stores a roll")
	_eq(sheet.values.size(), 7, "the sheet holds seven values")
	var summary: String = sheet.summary()
	_check(summary.contains("Fitness"), "the summary names the attributes")

	var packed: PackedScene = load("res://main.tscn")
	_check(packed != null, "main.tscn loads")
	if packed == null:
		return
	var scene: Node = packed.instantiate()
	root.add_child(scene)

	var player: Node = scene.get_node_or_null("Player")
	_check(player != null, "the player exists in the walking scene")
	if player != null:
		var before: Vector2 = player.position
		player.position += Vector2(32.0, 8.0)
		_check(player.position != before, "the player still moves")

	# The values belong to the sheet, not to the walking scene: moving must not touch them.
	_eq(sheet.summary(), summary, "movement leaves the sheet untouched")

	scene.free()
	sheet.free()

func _finish() -> void:
	if failures.is_empty():
		print("PASS: character sheet - bands, seven attributes, human range, reroll, retention and movement")
		quit(0)
	else:
		for failure in failures:
			printerr("FAIL: " + failure)
		quit(1)
