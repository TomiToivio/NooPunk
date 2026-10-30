extends "res://tests/godot/godot_test.gd"

func test_trauma_soak_and_nonlethal() -> void:
	var hit := CWNCombatEffects.resolve_hit(9, 8, 6, 3, true, false, 0, false, 5)
	check(hit.ok, "hit resolved")
	check(hit.traumatic, "trauma occurs")
	check_eq(hit.damage, 22, "27 damage minus five soak")
	check_eq(hit.soak_remaining, 0, "soak depleted")
	var safe := CWNCombatEffects.resolve_hit(9, 8, 6, 3, true, true, 0, false, 5)
	check(not safe.traumatic, "nonlethal forbids trauma")
	check_eq(safe.damage, 4, "nonlethal damage applies soak")

func test_shock_and_attack_floor() -> void:
	check_eq(CWNCombatEffects.resolve_miss_shock(2, 15, 13, false, false), 2, "eligible melee shock")
	check_eq(CWNCombatEffects.resolve_miss_shock(2, 15, 16, false, false), 0, "armored target resists shock")
	check_eq(CWNCombatEffects.resolve_miss_shock(2, 15, 16, false, true), 2, "unconditional shock")
	check_eq(CWNCombatEffects.resolve_miss_shock(2, 15, 13, true, true), 0, "immunity")
	var hit := CWNCombatEffects.resolve_hit(1, 1, 6, 2, true, false, 3, true, 0)
	check_eq(hit.damage, 3, "hit damage cannot be lower than eligible shock")

func test_encumbrance_and_system_strain() -> void:
	check_eq(CWNCombatEffects.carrying(11, 5, 11).movement_meters, 10.0, "normal movement")
	check_eq(CWNCombatEffects.carrying(11, 7, 15).movement_meters, 7.0, "first overload")
	check_eq(CWNCombatEffects.carrying(11, 9, 19).movement_meters, 5.0, "second overload")
	check(not CWNCombatEffects.carrying(11, 10, 19).legal, "excessive load rejected")
	check(CWNCombatEffects.can_add_strain(10, 3.0, 2.0, 5.0), "strain at ceiling")
	check(not CWNCombatEffects.can_add_strain(10, 3.0, 2.0, 6.0), "strain over ceiling")
	check_eq(CWNCombatEffects.rest_strain(5.0, 2.0, true, true), 4.0, "rest recovery")
