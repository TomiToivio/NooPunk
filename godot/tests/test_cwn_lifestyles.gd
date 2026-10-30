extends RefCounted

## #869: lifestyle costs and System Strain ceilings, SRD 3.2.1.
const Lifestyles := preload("res://godot/core/cwn_lifestyles.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	rows.append(_eq("five published levels", Lifestyles.levels().size(), 5))
	rows.append(_eq("squatter costs nothing", Lifestyles.monthly_cost("squatter"), 0))
	rows.append(_eq("slum costs 300", Lifestyles.monthly_cost("slum"), 300))
	rows.append(_eq("middle-class costs 1000", Lifestyles.monthly_cost("middle_class"), 1000))
	rows.append(_eq("fine costs 5000", Lifestyles.monthly_cost("fine"), 5000))
	rows.append(_eq("luxury costs 20000", Lifestyles.monthly_cost("luxury"), 20000))

	rows.append(_eq("squatter is -2 strain", Lifestyles.strain_modifier("squatter"), -2))
	rows.append(_eq("slum is -1 strain", Lifestyles.strain_modifier("slum"), -1))
	rows.append(_eq("middle-class is zero, not missing", Lifestyles.strain_modifier("middle_class"), 0))
	rows.append(_eq("fine is +1 strain", Lifestyles.strain_modifier("fine"), 1))
	rows.append(_eq("luxury is +2 strain", Lifestyles.strain_modifier("luxury"), 2))

	# the ceiling is what actually changes: squatters carry less chrome
	rows.append(_eq("luxury raises the ceiling", Lifestyles.max_system_strain(10, "luxury"), 12))
	rows.append(_eq("squatter lowers the ceiling", Lifestyles.max_system_strain(10, "squatter"), 8))
	rows.append(_eq("the ceiling never goes negative", Lifestyles.max_system_strain(1, "squatter"), 0))

	# affordability
	rows.append(_eq("no money means squatter", Lifestyles.most_expensive_affordable(0), "squatter"))
	rows.append(_eq("299 cannot buy a 300 lifestyle", Lifestyles.most_expensive_affordable(299), "squatter"))
	rows.append(_eq("exactly 300 buys slum", Lifestyles.most_expensive_affordable(300), "slum"))
	rows.append(_eq("1000 buys middle-class", Lifestyles.most_expensive_affordable(1000), "middle_class"))
	rows.append(_eq("plenty buys luxury", Lifestyles.most_expensive_affordable(50000), "luxury"))

	return rows
