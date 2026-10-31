extends RefCounted

## #873: pharmaceuticals and street drugs, SRD 3.5.0 — the table and the three general rules.
const Drugs := preload("res://godot/core/cwn_drugs.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	rows.append(_eq("sixteen published chems", Drugs.all_drugs().size(), 16))
	rows.append(_eq("Sand is 2", Drugs.price("sand"), 2))
	rows.append(_eq("Avalanche is 100", Drugs.price("avalanche"), 100))
	rows.append(_eq("Panacea is 200", Drugs.price("panacea"), 200))
	rows.append(_eq("Reset is 1000", Drugs.price("reset"), 1000))

	# "None" in the SRD is not Heal 0
	rows.append(_eq("Panacea needs Heal 1", Drugs.min_heal("panacea"), 1))
	rows.append(_eq("Avalanche needs Heal 0", Drugs.min_heal("avalanche"), 0))
	rows.append(_eq("Boneshaker needs no skill at all", Drugs.min_heal("boneshaker"), -1))
	rows.append(_eq("anyone can administer Boneshaker", Drugs.anyone_can_administer("boneshaker"), true))
	rows.append(_eq("Heal 0 is not anyone", Drugs.anyone_can_administer("avalanche"), false))

	# administration gate
	rows.append(_eq("Heal 0 cannot give Panacea", Drugs.can_administer("panacea", 0), false))
	rows.append(_eq("Heal 1 can give Panacea", Drugs.can_administer("panacea", 1), true))
	rows.append(_eq("Heal 0 can give Avalanche", Drugs.can_administer("avalanche", 0), true))
	rows.append(_eq("no Heal can still give Boneshaker", Drugs.can_administer("boneshaker", 0), true))

	# rarity footnote
	rows.append(_eq("Reset is rare", Drugs.is_rare("reset"), true))
	rows.append(_eq("Avalanche is not", Drugs.is_rare("avalanche"), false))

	# only the highest bonus applies
	rows.append(_eq("one bonus passes through", Drugs.stacking_bonus([2]), 2))
	rows.append(_eq("bonuses do not add", Drugs.stacking_bonus([2, 3]), 3))
	rows.append(_eq("no bonuses is zero", Drugs.stacking_bonus([]), 0))

	# strain overflow: no benefit, but the harm remains
	rows.append(_eq("within the maximum grants the benefit", Drugs.applies_benefit(4, 2, 10), true))
	rows.append(_eq("exactly at the maximum still grants it", Drugs.applies_benefit(8, 2, 10), true))
	rows.append(_eq("over the maximum grants nothing", Drugs.applies_benefit(9, 2, 10), false))

	return rows
