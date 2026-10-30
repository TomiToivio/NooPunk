extends RefCounted

## #858 / #869: cyberware Alienation, SRD 3.6.8 — tested against the single surviving implementation.
##
## This file used to test `cwn_alienation.gd`. That module duplicated `cwn_cyberware_ops.gd`, which also
## carries the syndrome rules and therapy, so it was deleted instead of kept in parallel. The behaviours
## worth guarding did not change: rounding up, the Nerve surcharge, the strictly-greater threshold, the
## 1d20 check, the therapy floor, and refusing the same syndrome twice.
const Ops := preload("res://godot/core/cwn_cyberware_ops.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	# rounding up, and the zero guard
	rows.append(_eq("cost 1 is 1", Ops.alienation_gain(1.0), 1))
	rows.append(_eq("cost 0.5 rounds up to 1", Ops.alienation_gain(0.5), 1))
	rows.append(_eq("nerve adds 2", Ops.alienation_gain(1.0, true), 3))
	rows.append(_eq("no strain means no alienation", Ops.alienation_gain(0.0), 0))

	# threshold is strictly greater than the maximum
	rows.append(_eq("at maximum is functional", Ops.is_psychotic(10, 10), false))
	rows.append(_eq("above maximum breaks down", Ops.is_psychotic(11, 10), true))

	# the check: 1d20 <= current
	rows.append(_eq("zero alienation cannot trigger", Ops.alienation_check(1, 0).get("gains_point"), false))
	rows.append(_eq("equal to the roll triggers", Ops.alienation_check(7, 7).get("gains_point"), true))
	rows.append(_eq("below the roll does not", Ops.alienation_check(8, 7).get("gains_point"), false))
	rows.append(_eq("an out-of-range die is refused", Ops.alienation_check(0, 5).get("ok"), false))

	# therapy reduces by one and is floored by the chrome still carried
	rows.append(_eq("therapy reduces by one", Ops.therapy_week(8, 3), 7))
	rows.append(_eq("therapy cannot pass the floor", Ops.therapy_week(3, 3), 3))

	# syndromes raise the maximum, and the same one cannot be taken twice
	var one := Ops.max_alienation(10, ["paranoia"] if Ops.SYNDROMES.has("paranoia") else [])
	rows.append(_eq("a known syndrome is accepted", one.get("ok"), true))
	var any_key: String = Ops.SYNDROMES.keys()[0] if not Ops.SYNDROMES.is_empty() else ""
	rows.append(_eq("the same syndrome twice is refused",
		Ops.max_alienation(10, [any_key, any_key]).get("ok"), false))
	rows.append(_eq("an unknown syndrome is reported, not silently ignored",
		Ops.max_alienation(10, ["not_a_syndrome"]).get("ok"), false))
	rows.append(_eq("no syndromes means maximum equals Wisdom", Ops.max_alienation(10, []).get("maximum"), 10))

	return rows
