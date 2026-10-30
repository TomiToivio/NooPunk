extends SceneTree

## Gate for #835: the seven 3d6 ranges, exactly seven attributes, the human range, reroll behaviour
## and retention of the rolled sheet while the player moves.
##
## Run from the repository root:
##   godot --headless --path noopunk/game --script res://tests/test_character.gd

var failures: Array[String] = []


func _check(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)


func _finish() -> void:
	if failures.is_empty():
		print("CHARACTER TESTS: all checks passed")
		quit(0)
	else:
		for failure in failures:
			print("  FAIL " + failure)
		print("CHARACTER TESTS: %d failure(s)" % failures.size())
		quit(1)


func _initialize() -> void:
	var character := RookieCharacter.new()
	_check(character.data.size() > 0, "attributes.json did not load")

	var expected := {
		3: -3, 4: -3, 5: -2, 6: -2, 7: -1, 8: -1, 9: 0, 10: 0,
		11: 0, 12: 0, 13: 1, 14: 1, 15: 2, 16: 2, 17: 3, 18: 3,
	}
	for total in expected:
		_check(character.convert_total(total) == expected[total],
			"3d6 total %d should convert to %d, got %d" % [total, expected[total], character.convert_total(total)])
		_check(character.is_valid_total(total), "total %d should be valid" % total)
	_check(not character.is_valid_total(2), "total 2 is outside 3d6")
	_check(not character.is_valid_total(19), "total 19 is outside 3d6")

	var ids := character.attribute_ids()
	_check(ids.size() == 7, "expected exactly seven attributes, got %d" % ids.size())
	_check(ids.has("empathy") and ids.has("agency") and ids.has("cyber"),
		"the attribute ids must be the seven the issue names")

	var rng := RandomNumberGenerator.new()
	rng.seed = 835
	var values := character.roll(rng)
	_check(values.size() == 7, "a roll must produce seven values")
	var human := character.human_range()
	for id in values:
		var value: int = values[id]
		_check(value >= human.x and value <= human.y, "%s=%d is outside the human range" % [id, value])
	var totals: Dictionary = character.totals.duplicate()
	for id in totals:
		_check(int(totals[id]) >= 3 and int(totals[id]) <= 18, "%s raw total %d is outside 3d6" % [id, totals[id]])

	var again := character.roll(_seeded(1))
	var changed := false
	for id in again:
		if int(again[id]) != int(values[id]):
			changed = true
	_check(changed, "rerolling with a different seed should change at least one value")

	var a := character.roll(_seeded(7)).duplicate()
	var b := character.roll(_seeded(7)).duplicate()
	_check(a == b, "the same seed must reproduce the same sheet")

	var packed: PackedScene = load("res://main.tscn")
	_check(packed != null, "main.tscn does not load")
	if packed == null:
		_finish()
		return
	var scene: Node = packed.instantiate()
	root.add_child(scene)
	var sheet: Node = scene.get_node_or_null("CharacterSheet")
	_check(sheet != null, "the character sheet is not in main.tscn")
	var player: Node = scene.get_node_or_null("Player")
	_check(player != null, "the walking scene's player is missing")
	if sheet == null or player == null:
		_finish()
		return
	var rolled: Dictionary = sheet.values().duplicate()
	_check(rolled.size() == 7, "the sheet should show seven values after startup")
	var start: Vector2 = player.position
	player.position += Vector2(16, 0)
	_check(player.position != start, "the player did not move")
	_check(sheet.values() == rolled, "the rolled sheet must be retained while the player moves")

	_finish()


func _seeded(value: int) -> RandomNumberGenerator:
	var rng := RandomNumberGenerator.new()
	rng.seed = value
	return rng
