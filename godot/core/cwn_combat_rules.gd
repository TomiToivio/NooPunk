## Cities Without Number: one attack's damage, with the SRD's Shock and Trauma invariants.
##
## This is the Godot side of `src/rules/cwn_core.py` (`shock_applies`, `shock_damage`,
## `is_traumatic_hit`, `trauma_damage`, `damage_floor`, `resolve_attack`). The Python module is the
## reference of record; this file must not invent a number it does not have, and
## `tests/godot/test_cwn_combat_rules.gd` pins the cases the Python suite pins.
##
## The three invariants, in the order they apply:
##
## 1. **Shock lands on a miss**, and only if the target's Melee AC is within the rating.
##    `shock_ac = -1` is the SRD's `Shock n/-` form and applies regardless of Armour Class.
## 2. **A Traumatic Hit multiplies the attack's total damage** by the weapon's Trauma Rating — the
##    total, not the weapon die. Only lethal attacks roll the Trauma Die at all.
## 3. **A hit never deals less than the Shock that a miss would have dealt.** That floor is a
##    *counterfactual*: it is computed with `hit = false` even when the attack hit, or it can never
##    engage. Getting this wrong is invisible whenever damage exceeds Shock, which is almost always.
##
## Deliberately not here: cover, range bands, automatic fire, suppressive fire, morale, armour as
## Damage Soak and the Major Injury table. Cover is an AC modifier the caller supplies; the rest are
## separate procedures with their own modules.
extends RefCounted
class_name CwnCombatRules

## SRD: the default Trauma Target a Trauma Die is compared against.
const DEFAULT_TRAUMA_TARGET := 6
## `Shock n/-`: no Armour Class ceiling. Not the same as "no Shock".
const SHOCK_ANY_AC := -1

## Whether Shock lands: only on a miss, and only if the target's Melee AC is within the rating.
static func shock_applies(hit: bool, shock_ac: int, target_melee_ac: int) -> bool:
	if hit:
		return false
	if shock_ac == SHOCK_ANY_AC:
		return true
	return target_melee_ac <= shock_ac

## Shock inflicted on a miss, or 0. `explicit_bonus` is only for bonuses that *say* they add to
## Shock; a generic "+2 damage" mod does not qualify.
static func shock_damage(
	hit: bool,
	shock_value: int,
	shock_ac: int,
	target_melee_ac: int,
	attribute_modifier: int = 0,
	explicit_bonus: int = 0
) -> int:
	if shock_value < 0:
		return 0
	if not shock_applies(hit, shock_ac, target_melee_ac):
		return 0
	return maxi(0, shock_value + int(attribute_modifier) + int(explicit_bonus))

## SRD: the Trauma Die meeting or exceeding the Trauma Target. Non-lethal attacks must not call this.
static func is_traumatic_hit(trauma_die: int, trauma_target: int = DEFAULT_TRAUMA_TARGET) -> bool:
	return trauma_die >= trauma_target

## The attack's **total** damage times the weapon's Trauma Rating, on a Traumatic Hit.
static func trauma_damage(total_damage: int, trauma_rating: int, traumatic: bool) -> int:
	if trauma_rating < 1:
		return total_damage
	return total_damage * trauma_rating if traumatic else total_damage

## A hit never deals less than the Shock a miss would have dealt.
static func damage_floor(hit_damage: int, shock_that_would_have_applied: int) -> int:
	return maxi(hit_damage, shock_that_would_have_applied)

## Shock can never cause Trauma, exposed as a function so a caller cannot forget it.
static func shock_can_cause_trauma() -> bool:
	return false

## One attack, resolved. Returns why each number appeared so the UI can show it.
## `trauma_die = -1` means "no Trauma Die was rolled" (a non-lethal attack).
static func resolve_attack(
	hit: bool,
	total_damage: int = 0,
	trauma_die: int = -1,
	trauma_rating: int = 1,
	trauma_target: int = DEFAULT_TRAUMA_TARGET,
	shock_value: int = 0,
	shock_ac: int = SHOCK_ANY_AC,
	target_melee_ac: int = 10,
	attribute_modifier: int = 0,
	explicit_shock_bonus: int = 0
) -> Dictionary:
	var would_be_shock := shock_damage(false, shock_value, shock_ac, target_melee_ac,
		attribute_modifier, explicit_shock_bonus)
	if not hit:
		return {"damage": would_be_shock, "shock": would_be_shock,
			"shock_floor": would_be_shock, "trauma": false, "trauma_die": -1}
	var traumatic := false
	if trauma_die >= 1:
		traumatic = is_traumatic_hit(trauma_die, trauma_target)
	var damage := trauma_damage(int(total_damage), int(trauma_rating), traumatic)
	damage = damage_floor(damage, would_be_shock)
	return {"damage": damage, "shock": 0, "shock_floor": would_be_shock,
		"trauma": traumatic, "trauma_die": trauma_die}
