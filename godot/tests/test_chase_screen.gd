## §2.6 presentation adapter invokes the existing chase kernel, not a second ruleset.
extends RefCounted
const Screen := preload("res://godot/ui/chase_screen.gd")

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "got %s, expected %s" % [str(actual), str(expected)]]

func run() -> Array:
	var rows: Array = []
	var screen := Screen.new()
	var foot: Dictionary = screen.resolve_values(false, 10, 11, 0, 0)
	rows.append(_eq("foot pursuer exceeds pace", foot["caught"], true))
	var tie: Dictionary = screen.resolve_values(false, 10, 10)
	rows.append(_eq("foot tie escapes", tie["escaped"], true))
	var hinder: Dictionary = screen.resolve_values(false, 10, 12, 3)
	rows.append(_eq("hindrances raise foot pace", hinder["pace"], 13))
	rows.append(_eq("hindrances prevent capture", hinder["caught"], false))
	var vehicle: Dictionary = screen.resolve_values(true, 10, 10)
	rows.append(_eq("vehicle tie remains in chase", vehicle["any_caught"], true))
	var dropped: Dictionary = screen.resolve_values(true, 10, 9)
	rows.append(_eq("vehicle slower pursuer drops out", dropped["any_caught"], false))
	return rows
