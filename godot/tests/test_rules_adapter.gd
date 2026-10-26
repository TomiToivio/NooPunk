## Rules adapter behaviour: the adapter must reproduce the kernel's numbers, and it must be obvious
## which die pool it used — #564's 3d6 proposal stays a data-level override, never a silent substitution.
extends RefCounted

const RulesAdapterScript := preload("res://godot/core/rules_adapter.gd")

func run() -> Array:
	var rows: Array = []
	var rules = RulesAdapterScript.new(RulesAdapterScript.DEFAULT_KERNEL_PATH, 7)

	rows.append(_eq("modifier at 3 is -2", rules.attribute_modifier(3), -2))
	rows.append(_eq("modifier at 7 is -1", rules.attribute_modifier(7), -1))
	rows.append(_eq("modifier at 13 is 0", rules.attribute_modifier(13), 0))
	rows.append(_eq("modifier at 17 is +1", rules.attribute_modifier(17), 1))
	rows.append(_eq("modifier at 18 is +2", rules.attribute_modifier(18), 2))

	rows.append(_eq("ladder 6", rules.difficulty_value(6), 6))
	rows.append(_eq("ladder by name", rules.difficulty_value("expert"), 10))
	rows.append(_eq("ladder name of 12", rules.difficulty_name(12), "Master"))

	rows.append(_eq("kernel die pool is 2d6", rules.die_pool_label(), "2d6 (kernel)"))

	# Determinism: same seed, same calls, same faces.
	var a = RulesAdapterScript.new(RulesAdapterScript.DEFAULT_KERNEL_PATH, 424242)
	var b = RulesAdapterScript.new(RulesAdapterScript.DEFAULT_KERNEL_PATH, 424242)
	var first_a: Dictionary = a.skill_check(14, 3, 10)
	var first_b: Dictionary = b.skill_check(14, 3, 10)
	rows.append(_eq("same seed gives the same faces", first_a["dice"], first_b["dice"]))
	rows.append(_eq("same seed gives the same total", first_a["total"], first_b["total"]))

	# The arithmetic, recomputed from the parts the result publishes.
	var dice_total := 0
	for face in first_a["dice"]:
		dice_total += int(face)
	var expected := dice_total + int(first_a["attribute_modifier"]) + int(first_a["skill_level"])
	rows.append(_eq("total is the sum of its published parts", first_a["total"], expected))

	# Untrained is passed explicitly as -1 and must enter the arithmetic as exactly minus one. Two
	# separate calls roll different faces, so the assertion is on the published parts, not on a re-roll.
	var untrained: Dictionary = a.skill_check(14, -1, 10)
	rows.append(_eq("untrained records skill level -1", int(untrained["skill_level"]), -1))
	rows.append(_eq("untrained subtracts exactly one",
		int(untrained["total"]),
		int(untrained["dice_total"]) + int(untrained["attribute_modifier"]) - 1))

	# The #564 seam: an approved override changes the pool, and the label says so.
	var overridden = RulesAdapterScript.new(RulesAdapterScript.DEFAULT_KERNEL_PATH, 5, {"count": 3, "sides": 6})
	rows.append(_eq("override label", overridden.die_pool_label(), "3d6 (approved override)"))
	rows.append(_eq("override rolls three dice", overridden.skill_check(10, 1, 8)["dice"].size(), 3))

	# Saves follow 16 - level - the higher of the pair; luck carries no attribute modifiers.
	rows.append(_eq("mental save", rules.save_target("mental", 3, {"WIS": 1, "CHA": 0}), 12))
	rows.append(_eq("physical save", rules.save_target("physical", 1, {"STR": 0, "CON": 2}), 13))
	rows.append(_eq("luck save", rules.save_target("luck", 2, {"WIS": 2}), 14))

	return rows

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]
