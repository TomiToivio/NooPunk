extends SceneTree

## The character-creation slice (#835): table boundaries, seven attributes, human range, reroll
## behaviour and retention across the scene change.
##
##   godot --headless --path noopunk/game --script res://tests/character_test.gd

var _failures: Array = []
var _checks := 0


func _check(name: String, got: Variant, want: Variant) -> void:
	_checks += 1
	if got != want:
		_failures.append("%s: got %s want %s" % [name, got, want])


func _initialize() -> void:
	# --- the conversion table, every boundary the issue names ---
	var expected := {3: -3, 4: -3, 5: -2, 6: -2, 7: -1, 8: -1, 9: 0, 12: 0,
		13: 1, 14: 1, 15: 2, 16: 2, 17: 3, 18: 3}
	for total in expected.keys():
		_check("total %d" % total, NoopunkAttributes.value_for_total(int(total)), int(expected[total]))
	# the gaps inside the 0 band
	for total in [10, 11]:
		_check("total %d" % total, NoopunkAttributes.value_for_total(total), 0)
	# out-of-range totals are refused, not clamped
	_check("total 2 is invalid", NoopunkAttributes.is_valid_total(2), false)
	_check("total 19 is invalid", NoopunkAttributes.is_valid_total(19), false)

	# --- seven attributes, in the author's order ---
	_check("seven attributes", NoopunkAttributes.names().size(), 7)
	_check("first is Fitness", String(NoopunkAttributes.names()[0]), "Fitness")
	_check("last is Empathy", String(NoopunkAttributes.names()[6]), "Empathy")
	for name in NoopunkAttributes.names():
		_check("definition for %s" % name, NoopunkAttributes.definition(String(name)) != "", true)

	# --- the sheet: exactly seven converted values, all inside the human range ---
	var rng := RandomNumberGenerator.new()
	rng.seed = 20261030
	var rolls := NoopunkAttributes.roll_all(rng)
	_check("a sheet is seven rolls", rolls.size(), 7)
	var human: Array = NoopunkAttributes.human_range()
	for roll in rolls:
		var value := int(roll["value"])
		_check("%s inside human range" % roll["name"], value >= int(human[0]) and value <= int(human[1]), true)
		_check("%s total is a real 3d6" % roll["name"], int(roll["total"]) >= 3 and int(roll["total"]) <= 18, true)
		_check("%s displays signed" % roll["name"],
			NoopunkAttributes.display(String(roll["name"]), value).contains("%+d" % value), true)

	# --- the same seed reproduces the same sheet; a new seed is a reroll ---
	var again := NoopunkAttributes.roll_all(rng)
	rng.seed = 20261030
	var same := NoopunkAttributes.roll_all(rng)
	_check("same seed, same sheet", NoopunkAttributes.sheet_lines(same), NoopunkAttributes.sheet_lines(rolls))
	var second_rng := RandomNumberGenerator.new()
	second_rng.seed = 7
	var rerolled := NoopunkAttributes.roll_all(second_rng)
	_check("a reroll is a fresh sheet", NoopunkAttributes.sheet_lines(rerolled) != NoopunkAttributes.sheet_lines(rolls), true)

	# --- difficulty labels come from the same contract ---
	_check("difficulty 6", NoopunkAttributes.difficulty_label(6), "Easiest")
	_check("difficulty 12", NoopunkAttributes.difficulty_label(12), "Average")
	_check("difficulty 18", NoopunkAttributes.difficulty_label(18), "Hardest")
	_check("no label for 7", NoopunkAttributes.difficulty_label(7), "")

	# --- retention: the rolled sheet survives a scene change ---
	var state: Node = load("res://character_state.gd").ensure(self)
	if state == null:
		_failures.append("CharacterState autoload missing")
	else:
		state.clear()
		_check("empty sheet is not complete", state.is_complete(), false)
		state.store(rolls)
		_check("the sheet is retained", state.is_complete(), true)
		_check("retained values match", state.sheet_text(), "\n".join(NoopunkAttributes.sheet_lines(rolls)))

	# --- the creation scene rolls on open and can continue ---
	var creation: PackedScene = load("res://character_creation.tscn")
	if creation == null:
		_failures.append("character_creation.tscn did not load")
	else:
		var ui := creation.instantiate()
		root.add_child(ui)
		await process_frame
		_check("opening creation rolls a sheet", state != null and state.is_complete(), true)
		var sheet_container := ui.get_node_or_null("Panel/Sheet")
		_check("the sheet shows seven rows", sheet_container.get_child_count() if sheet_container else -1, 7)
		var cont := ui.get_node_or_null("Panel/Continue")
		_check("continue is available once rolled", cont != null and not cont.disabled, true)
		ui.queue_free()

	# --- and the walking scene still works afterwards ---
	var walking: PackedScene = load("res://main.tscn")
	var world := walking.instantiate()
	root.add_child(world)
	await process_frame
	var label := world.get_node_or_null("Hint/SheetLabel") as Label
	_check("the walking scene shows the retained sheet", label != null and not label.text.is_empty(), true)
	var player := world.get_node_or_null("Player")
	_check("the player still moves", player != null and player.movement_velocity(Vector2(1, 0)).length() > 0.0, true)
	world.queue_free()

	if _failures.is_empty():
		print("CHARACTER OK: %d checks" % _checks)
		quit(0)
	else:
		for failure in _failures:
			print("  FAIL " + failure)
		print("CHARACTER FAIL: %d of %d checks" % [_failures.size(), _checks])
		quit(1)
