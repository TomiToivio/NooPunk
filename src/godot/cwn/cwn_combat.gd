class_name CWNCombat
extends RefCounted

## Attack, damage, Shock and Traumatic Hit arithmetic (CWN SRD).
##
## Everything here is a pure function of explicit dice. The parts that are easy to get subtly wrong
## are the ones this file exists for:
##
## - **a hit never does less than the Shock it would have inflicted on a miss** — the counterfactual
##   is computed and used as a floor, not skipped when the attack happens to hit;
## - **Shock only applies on a miss**, and only against targets whose AC the Shock rating reaches
##   (`2/15` means AC 15 or less; `5/-` means unconditional);
## - **Damage Soak is a pool for one fight**, spent before hit points, and refreshed after it;
## - **Trauma multiplies the whole hit**, not the weapon die.
##
## Nothing in this file reads a catalogue: the caller passes the weapon's own numbers, so a changed
## SRD row cannot drift away from the resolver.

## Side initiative: 1d8 plus the best Dexterity modifier on that side. PCs win ties.
static func initiative(pc_roll: int, pc_best_dex: int, npc_roll: int, npc_best_dex: int) -> Dictionary:
	assert(pc_roll >= 1 and pc_roll <= 8 and npc_roll >= 1 and npc_roll <= 8, "initiative is 1d8")
	var pc_total := pc_roll + pc_best_dex
	var npc_total := npc_roll + npc_best_dex
	var winner := "pc"
	if npc_total > pc_total:
		winner = "npc"
	return {"pc_total": pc_total, "npc_total": npc_total, "winner": winner}

## Attack roll: d20 + attack bonus + attribute modifier + combat skill, against AC.
## `situational` is the sum of cover and positioning penalties (negative) already adjudicated.
static func attack(d20: int, attack_bonus: int, attribute_modifier: int, skill_rank: int,
		armor_class: int, situational: int = 0) -> Dictionary:
	assert(d20 >= 1 and d20 <= 20, "attack rolls are on a d20")
	var total := d20 + attack_bonus + attribute_modifier + skill_rank + situational
	return {
		"total": total,
		"hit": total >= armor_class,
		"natural_one": d20 == 1,
		"natural_twenty": d20 == 20,
	}

## Weapon damage: die + the weapon's attribute modifier + explicit bonuses. Never negative.
static func damage(die_roll: int, attribute_modifier: int, bonus: int = 0) -> int:
	assert(die_roll >= 0, "damage dice cannot roll below zero")
	return max(0, die_roll + attribute_modifier + bonus)

## Shock damage on a miss. `max_ac` of 99 encodes the unconditional `5/-` form.
static func shock_damage(shock: Dictionary, attribute_modifier: int, target_melee_ac: int,
		shock_bonus: int = 0) -> int:
	var amount := int(shock.get("amount", 0))
	if amount <= 0:
		return 0
	var max_ac := int(shock.get("max_ac", -99))
	if max_ac < 0:
		return 0
	if max_ac < 99 and target_melee_ac > max_ac:
		return 0
	return max(0, amount + attribute_modifier + shock_bonus)

## A successful attack can never deal less than the Shock it would have dealt on a miss. The
## counterfactual has to be computed even though the attack hit, or the floor silently never
## engages on the only branch where it matters.
static func hit_damage_with_shock_floor(rolled_damage: int, shock: Dictionary,
		attribute_modifier: int, target_melee_ac: int, shock_bonus: int = 0) -> int:
	var floor_damage := shock_damage(shock, attribute_modifier, target_melee_ac, shock_bonus)
	return max(rolled_damage, floor_damage)

## Trauma Die at or above the Trauma Target is a Traumatic Hit.
static func is_traumatic_hit(trauma_roll: int, trauma_target: int = 6) -> bool:
	assert(trauma_roll >= 1, "Trauma Die rolls at least 1")
	return trauma_roll >= trauma_target

## A Traumatic Hit multiplies the total damage of the hit by the weapon's Trauma Rating.
static func traumatic_damage(total_damage: int, trauma_rating: int) -> int:
	assert(trauma_rating >= 1, "Trauma Rating is x1 or better")
	return total_damage * trauma_rating

## Damage Soak is spent before hit points and lasts one fight. Returns the new pool and the damage
## that reached the character; a pool can absorb at most what it has left.
static func apply_soak(damage: int, soak_remaining: int) -> Dictionary:
	assert(damage >= 0 and soak_remaining >= 0)
	var absorbed: int = min(damage, soak_remaining)
	return {
		"soak_remaining": soak_remaining - absorbed,
		"damage_taken": damage - absorbed,
		"absorbed": absorbed,
	}

## One attack resolved end to end. `trauma_roll` may be -1 to skip the Trauma Die (non-lethal
## attacks do not roll it). Returns everything a log line needs.
static func resolve_attack(params: Dictionary) -> Dictionary:
	var weapon: Dictionary = params.get("weapon", {})
	var target_melee_ac: int = int(params.get("target_melee_ac", 10))
	var shock: Dictionary = weapon.get("shock", {"amount": 0, "max_ac": -99})
	var attribute_modifier: int = int(params.get("attribute_modifier", 0))

	var attack_result := attack(
		int(params.get("d20", 10)),
		int(params.get("attack_bonus", 0)),
		attribute_modifier,
		int(params.get("skill_rank", 0)),
		int(params.get("armor_class", 10)),
		int(params.get("situational", 0)),
	)

	if not bool(attack_result["hit"]):
		return {
			"hit": false,
			"attack": attack_result,
			"damage": shock_damage(shock, attribute_modifier, target_melee_ac,
				int(params.get("shock_bonus", 0))),
			"traumatic": false,
			"source": "shock",
		}

	var rolled := damage(int(params.get("damage_die_roll", 1)), attribute_modifier,
		int(params.get("damage_bonus", 0)))
	var dealt := hit_damage_with_shock_floor(rolled, shock, attribute_modifier, target_melee_ac,
		int(params.get("shock_bonus", 0)))

	var trauma_roll: int = int(params.get("trauma_roll", -1))
	var traumatic := false
	if trauma_roll > 0:
		traumatic = is_traumatic_hit(trauma_roll, int(params.get("trauma_target", 6)))
		if traumatic:
			dealt = traumatic_damage(dealt, int(weapon.get("trauma_rating", 1)))

	return {
		"hit": true,
		"attack": attack_result,
		"damage": dealt,
		"rolled": rolled,
		"traumatic": traumatic,
		"source": "hit",
	}
