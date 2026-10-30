extends "res://tests/godot/godot_test.gd"

## CWN Shock, Trauma and the damage floor — and the turn-level consequences of them (#751).
##
## The kernel cases mirror the ones `tests/test_cwn_trauma.py` and `tests/test_cwn_core.py` pin on the
## Python side, because a rule difference between the two runtimes is a defect, not a port.

const Injury = preload("res://godot/core/cwn_combat_rules.gd")

func test_shock_lands_only_on_a_miss_and_only_within_the_rating() -> void:
	check_eq(Injury.shock_applies(true, 13, 10), false, "a hit is not Shock")
	check_eq(Injury.shock_applies(false, 13, 13), true, "a miss at the rating's ceiling reaches")
	check_eq(Injury.shock_applies(false, 13, 14), false, "one point above the ceiling does not")
	check_eq(Injury.shock_applies(false, Injury.SHOCK_ANY_AC, 99), true,
		"Shock n/- reaches any Armour Class")

func test_shock_damage_is_zero_when_it_does_not_apply() -> void:
	check_eq(Injury.shock_damage(true, 2, 13, 10), 0, "no Shock on a hit")
	check_eq(Injury.shock_damage(false, 2, 13, 14), 0, "no Shock above the rating")
	check_eq(Injury.shock_damage(false, 2, 13, 12), 2, "Shock on a miss within the rating")

func test_a_traumatic_hit_multiplies_the_total_damage() -> void:
	check_eq(Injury.is_traumatic_hit(6), true, "the default Trauma Target is 6")
	check_eq(Injury.is_traumatic_hit(5), false, "5 is below the target")
	check_eq(Injury.trauma_damage(9, 3, true), 27, "the total, not the die, is multiplied")
	check_eq(Injury.trauma_damage(9, 3, false), 9, "a normal hit is not multiplied")
	check_eq(Injury.shock_can_cause_trauma(), false, "Shock never causes Trauma")

func test_a_hit_never_deals_less_than_the_shock_it_avoided() -> void:
	var resolved = Injury.resolve_attack(true, 1, -1, 1, 6, 5, 18, 10)
	check_eq(int(resolved["damage"]), 5, "a 1-damage hit against Shock 5 still deals 5")
	check_eq(int(resolved["shock"]), 0, "and it is damage, not Shock")
	check_eq(int(resolved["shock_floor"]), 5, "the floor is reported so the table can see it")

func test_a_miss_deals_its_shock_and_never_trauma() -> void:
	var resolved = Injury.resolve_attack(false, 0, 6, 3, 6, 4, 15, 12)
	check_eq(int(resolved["damage"]), 4, "a miss deals Shock")
	check_eq(bool(resolved["trauma"]), false, "and can never be Traumatic")

func test_a_non_lethal_attack_rolls_no_trauma_die() -> void:
	var resolved = Injury.resolve_attack(true, 6, -1, 1, 6, 0, 10, 10)
	check_eq(bool(resolved["trauma"]), false, "no Trauma Die means no Traumatic Hit")
	check_eq(int(resolved["damage"]), 6, "the damage is unaffected")
