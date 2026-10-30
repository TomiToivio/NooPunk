class_name CWNCombatEffects
extends RefCounted

## CWN SRD combat damage, trauma, shock and encumbrance.
## Source: cwn.quadrifons.com/rules-of-the-game/combat/damage-trauma-shock/
## and /rules-of-the-game/encumbrance/
## Does not adjudicate attacks, death, major injury or ammunition.

static func resolve_hit(raw_damage: int, trauma_die: int, trauma_target: int,
		trauma_rating: int, trauma_applicable: bool, nonlethal: bool,
		shock_damage: int, shock_eligible: bool, soak_remaining: int) -> Dictionary:
	if raw_damage < 0 or trauma_die < 1 or trauma_target < 1 or trauma_rating < 1 or soak_remaining < 0:
		return {"ok": false}
	var trauma := trauma_applicable and not nonlethal and trauma_die >= trauma_target
	var damage := raw_damage * (trauma_rating if trauma else 1)
	if shock_eligible:
		damage = maxi(damage, shock_damage)
	var absorbed := mini(damage, soak_remaining)
	return {"ok": true, "traumatic": trauma, "damage": damage - absorbed,
		"soak_used": absorbed, "soak_remaining": soak_remaining - absorbed,
		"damage_before_soak": damage}

static func resolve_miss_shock(shock_damage: int, shock_ac_limit: int,
		target_melee_ac: int, immune: bool, unconditional: bool,
		attribute_modifier: int = 0, explicit_shock_bonus: int = 0) -> int:
	if immune or shock_damage <= 0:
		return 0
	if not unconditional and target_melee_ac > shock_ac_limit:
		return 0
	return maxi(0, shock_damage + attribute_modifier + explicit_shock_bonus)

static func carrying(strength: int, ready_points: int, stowed_points: int) -> Dictionary:
	if strength < 3 or strength > 18 or ready_points < 0 or stowed_points < 0:
		return {"ok": false}
	var ready_limit := strength / 2
	var stowed_limit := strength
	var extra_ready := ready_points - ready_limit
	var extra_stowed := stowed_points - stowed_limit
	var overload := 0
	if extra_ready > 0 or extra_stowed > 0:
		overload = 1 if extra_ready <= 2 and extra_stowed <= 4 else 2
	if extra_ready > 4 or extra_stowed > 8:
		return {"ok": true, "legal": false, "movement_meters": 0.0}
	return {"ok": true, "legal": true, "overload": overload,
		"movement_meters": [10.0, 7.0, 5.0][overload],
		"readied_limit": ready_limit, "stowed_limit": stowed_limit}

static func can_add_strain(constitution: int, current: float, permanent: float, additional: float) -> bool:
	return constitution >= 3 and constitution <= 18 and current >= 0.0 and permanent >= 0.0 and additional >= 0.0 and current + permanent + additional <= constitution

static func rest_strain(current: float, permanent: float, rested_eight_hours: bool, sheltered_and_fed: bool) -> float:
	if not rested_eight_hours or not sheltered_and_fed:
		return current
	return maxf(permanent, current - 1.0)
