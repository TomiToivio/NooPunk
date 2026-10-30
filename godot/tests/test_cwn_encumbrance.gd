extends RefCounted

## Encumbrance tiers and movement costs, checked against the SRD rules ported in
## `src/rules/cwn_encumbrance.py`.
const Encumbrance := preload("res://src/godot/cwn/cwn_encumbrance.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	# Strength 10: 10 Stowed, 5 Readied.
	rows.append(_eq("stowed capacity is Strength", Encumbrance.stowed_capacity(10), 10))
	rows.append(_eq("readied capacity is half Strength", Encumbrance.readied_capacity(11), 5))

	rows.append(_eq("an empty load is normal", Encumbrance.tier_for(10, 0, 0), "normal"))
	rows.append(_eq("filling both limits stays normal", Encumbrance.tier_for(10, 10, 5), "normal"))
	rows.append(_eq("one point over is heavy", Encumbrance.tier_for(10, 11, 5), "heavy"))
	rows.append(_eq("the first push allows +4 stowed", Encumbrance.tier_for(10, 14, 7), "heavy"))
	rows.append(_eq("beyond the first push is overloaded", Encumbrance.tier_for(10, 15, 7), "overloaded"))
	rows.append(_eq("the second push allows +8 stowed", Encumbrance.tier_for(10, 18, 9), "overloaded"))
	rows.append(_eq("beyond the second push is immobile", Encumbrance.tier_for(10, 19, 9), "immobile"))
	rows.append(_eq("readied alone can overload", Encumbrance.tier_for(10, 0, 8), "overloaded"))
	rows.append(_eq("readied beyond the second push is immobile", Encumbrance.tier_for(10, 0, 10), "immobile"))

	rows.append(_eq("normal load keeps full speed", Encumbrance.move_speed(10, 10, 5), 10.0))
	rows.append(_eq("heavy load moves seven", Encumbrance.move_speed(10, 11, 5), 7.0))
	rows.append(_eq("overloaded load moves five", Encumbrance.move_speed(10, 15, 7), 5.0))
	rows.append(_eq("immobile is zero, not a fraction", Encumbrance.move_speed(10, 19, 9), 0.0))
	rows.append(_eq("base speed is a parameter", Encumbrance.move_speed(10, 11, 5, 8.0), 5.6))

	rows.append(_eq("an immobile load cannot be hauled", Encumbrance.can_haul(10, 19, 9), false))
	rows.append(_eq("an overloaded load can", Encumbrance.can_haul(10, 15, 7), true))

	rows.append(_eq("three items bundle to one point", Encumbrance.bundled_points(3), 1))
	rows.append(_eq("four items need two bundles", Encumbrance.bundled_points(4), 2))
	rows.append(_eq("no items is no points", Encumbrance.bundled_points(0), 0))

	rows.append(_eq("25 kg is ten points", Encumbrance.kilograms_to_points(25.0), 10.0))
	rows.append(_eq("50 kg is twenty points", Encumbrance.kilograms_to_points(50.0), 20.0))

	return rows
