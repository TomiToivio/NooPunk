## Cities Without Number — chases and pursuit.
##
## Transcribed from the SRD (CC0), ``rules-of-the-game/chases-and-pursuit``. Two procedures:
##
## *Foot* — the best Dex/Exert or Con/Exert total in the fleeing group is its **pace**; each successful
## act of hindrance adds +1 (maximum +3), a botched one that actively harms applies −1. The pursuers
## then make one such check; beating the pace catches the quarry, tying or rolling less means the party
## escaped immediate pursuit.
##
## *Vehicle* — the fleeing driver's Dex/Drive check is the pace, one check per pursuing vehicle, and
## any pursuer that does not equal or exceed it drops out of the chase.
##
## Dice are arguments. This module never rolls.
extends RefCounted
class_name CwnChases

const MAX_HINDER_BONUS := 3
const TERRAIN_LIMIT := 2

##: Foot-chase pursuit modifiers, SRD table.
const FOOT_MODIFIERS := {
	"more_pursuers_than_pursued": -1,
	"no_head_start": 2,
	"one_round_head_start": 1,
	"less_than_a_minute_head_start": 0,
	"more_than_a_minute_head_start": -2,
	"half_hearted": -1,
	"enraged": 1,
}

##: Vehicle-pursuit modifiers, SRD table.
const VEHICLE_MODIFIERS := {
	"pursuer_cannot_see_target": -2,
	"pursuer_flying_not_pursued": 3,
	"pursued_flying_not_pursuer": -3,
	"spotter_relaying": 1,
	"half_hearted": -1,
	"enraged": 1,
}


## The fleeing group's foot pace: its best Exert total plus hindrance, capped at +3.
##
## `hinder_botches` counts efforts that actively harmed the escape; the SRD makes those −1 each.
static func foot_pace(best_exert_total: int, hinder_successes: int, hinder_botches: int = 0) -> int:
	var bonus := mini(maxi(hinder_successes, 0), MAX_HINDER_BONUS) - maxi(hinder_botches, 0)
	return best_exert_total + bonus


## Sum the SRD's pursuit modifiers. `terrain` is the "who knows the local terrain better" row, −2..+2.
static func pursuit_modifier(circumstances: Array, terrain: int = 0) -> Dictionary:
	var total := clampi(terrain, -TERRAIN_LIMIT, TERRAIN_LIMIT)
	var unknown: Array = []
	for circumstance in circumstances:
		var key := String(circumstance)
		if FOOT_MODIFIERS.has(key):
			total += int(FOOT_MODIFIERS[key])
		elif VEHICLE_MODIFIERS.has(key):
			total += int(VEHICLE_MODIFIERS[key])
		else:
			unknown.append(key)
	return {"ok": unknown.is_empty(), "modifier": total, "unknown": unknown}


## Compare one pursuit check with the quarry's pace. Ties escape, as the SRD says.
static func resolve(pace: int, check_total: int) -> Dictionary:
	return {
		"ok": true,
		"pace": pace,
		"check": check_total,
		"caught": check_total > pace,
		"escaped": check_total <= pace,
	}


## A whole foot chase: the quarry's pace and one pursuit check.
static func foot(
	best_exert_total: int,
	pursuit_check: int,
	hinder_successes: int = 0,
	hinder_botches: int = 0,
	circumstances: Array = [],
	terrain: int = 0
) -> Dictionary:
	var pace := foot_pace(best_exert_total, hinder_successes, hinder_botches)
	var mods := pursuit_modifier(circumstances, terrain)
	var result := resolve(pace, pursuit_check + int(mods["modifier"]))
	result["ok"] = bool(mods["ok"])
	result["unknown"] = mods["unknown"]
	result["modifier"] = int(mods["modifier"])
	return result


## A vehicle chase: the fleeing driver's check is the pace, then one check per pursuer.
##
## Returns `{ok, pace, caught_by}` where `caught_by` is one bool per pursuer in order; pursuers that
## fail fall out of the chase.
static func vehicle(
	fleeing_drive_total: int,
	pursuer_totals: Array,
	circumstances: Array = [],
	terrain: int = 0
) -> Dictionary:
	if pursuer_totals.is_empty():
		return {"ok": false, "reason": "a chase needs at least one pursuer", "caught_by": []}
	var mods := pursuit_modifier(circumstances, terrain)
	var caught_by: Array = []
	for total in pursuer_totals:
		caught_by.append(int(total) + int(mods["modifier"]) >= fleeing_drive_total)
	return {
		"ok": bool(mods["ok"]),
		"pace": fleeing_drive_total,
		"caught_by": caught_by,
		"any_caught": caught_by.has(true),
		"modifier": int(mods["modifier"]),
		"unknown": mods["unknown"],
	}
