extends RefCounted

## #858: cyberware Alienation, SRD 3.6.8.
##
## The failures worth guarding: rounding down a 0.5 system to zero Alienation, forgetting the Nerve
## surcharge, treating "equal to Wisdom" as breakdown, and collapsing the save's two outcomes into one.
const Alienation := preload("res://godot/core/cwn_alienation.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	# rounding up, not down
	rows.append(_eq("cost 1 is 1", Alienation.alienation_for_system(1.0), 1))
	rows.append(_eq("cost 0.5 rounds up to 1", Alienation.alienation_for_system(0.5), 1))
	rows.append(_eq("cost 2 is 2", Alienation.alienation_for_system(2.0), 2))

	# nerve surcharge is per system
	rows.append(_eq("nerve adds 2", Alienation.alienation_for_system(1.0, true), 3))
	rows.append(_eq("nerve adds 2 to a fractional system", Alienation.alienation_for_system(0.5, true), 3))

	# totals across systems
	var systems := [
		{"strain_cost": 1.0, "nerve": false},
		{"strain_cost": 0.5, "nerve": true},
		{"strain_cost": 2.0, "nerve": false},
	]
	rows.append(_eq("permanent total", Alienation.permanent_total(systems), 1 + 3 + 2))
	rows.append(_eq("no systems means zero", Alienation.permanent_total([]), 0))

	# the threshold is strictly greater than Wisdom
	rows.append(_eq("at Wisdom is functional", Alienation.is_psychotic(10, 10), false))
	rows.append(_eq("above Wisdom breaks down", Alienation.is_psychotic(11, 10), true))

	# the check: 1d20 <= current
	rows.append(_eq("zero alienation cannot trigger", Alienation.check_gains_point(1, 0), false))
	rows.append(_eq("equal to the roll triggers", Alienation.check_gains_point(7, 7), true))
	rows.append(_eq("below the roll does not", Alienation.check_gains_point(8, 7), false))
	rows.append(_eq("twenty against a high score triggers", Alienation.check_gains_point(20, 20), true))

	# two distinct outcomes from the save
	rows.append(_eq("success picks a syndrome",
		Alienation.resolve_over_maximum(true), Alienation.Outcome.PICK_SYNDROME))
	rows.append(_eq("failure is psychosis",
		Alienation.resolve_over_maximum(false), Alienation.Outcome.PSYCHOSIS))
	rows.append(_eq("the outcomes differ",
		Alienation.Outcome.PICK_SYNDROME != Alienation.Outcome.PSYCHOSIS, true))

	# therapy: one point per week, floored by remaining chrome
	rows.append(_eq("therapy reduces by one", Alienation.after_therapy(8, 3), 7))
	rows.append(_eq("therapy cannot pass the floor", Alienation.after_therapy(3, 3), 3))
	rows.append(_eq("therapy cost is 2000 per week", Alienation.THERAPY_COST_PER_WEEK, 2000))

	return rows
