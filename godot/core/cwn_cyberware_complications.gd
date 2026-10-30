## Cities Without Number — the d12 implant complication table.
##
## Transcribed from the SRD (CC0), ``gear-vehicles-cyberware/cyberware/implant-complications``.
## A complication is rolled when installation surgery fails by one or two points, when a removal
## damages the tech, or when secondhand cyber is re-implanted.
##
## SRD fallback rule: **if the rolled complication does not apply to the cyber, treat it as 12.**
## That instruction is easy to lose, and losing it leaves a caller applying an impossible effect, so
## the fallback is a function here rather than a note in a comment.
extends RefCounted
class_name CwnCyberwareComplications

##: d12 rows. `hook` names the mechanical consequence a rules consumer must implement.
const TABLE := {
	1: {"id": "unreliable", "name": "Unreliable", "hook": "first daily critical use: 1d6, on 1 nonfunctional until maintained", "extra_strain": 0.0},
	2: {"id": "inefficient", "name": "Inefficient", "hook": "costs an additional 0.5 System Strain", "extra_strain": 0.5},
	3: {"id": "loud", "name": "Loud", "hook": "audible five metres while operating; stealth impossible", "extra_strain": 0.0},
	4: {"id": "fussy", "name": "Fussy", "hook": "maintenance interval halved", "extra_strain": 0.0},
	5: {"id": "bad_connection", "name": "Bad Connection", "hook": "1 in 6 chance the activation wastes the action", "extra_strain": 0.0},
	6: {"id": "blatant", "name": "Blatant", "hook": "obvious on sight instead of requiring Medical or Touch detection", "extra_strain": 0.0},
	7: {"id": "debilitating", "name": "Debilitating", "hook": "a relevant attribute's base score drops by 1d2 while implanted", "extra_strain": 0.0},
	8: {"id": "uncooperative", "name": "Uncooperative", "hook": "+1 System Strain if another implant shares its category", "extra_strain": 1.0},
	9: {"id": "complicated", "name": "Complicated", "hook": "minimum maintenance skill becomes Fix-1 or Heal-1", "extra_strain": 0.0},
	10: {"id": "exhausting", "name": "Exhausting", "hook": "24 hours of downtime after maintenance, else 2 System Strain", "extra_strain": 0.0},
	11: {"id": "power_hungry", "name": "Power Hungry", "hook": "needs half an hour on grid or vehicle power daily, else inert", "extra_strain": 0.0},
	12: {"id": "petty_annoyance", "name": "Petty Annoyance", "hook": "a harmless quirk of fit", "extra_strain": 0.0},
}

const FALLBACK := 12


## The complication for a d12 roll.
##
## `applies` is whether the rolled complication can affect this particular implant (for example,
## "Loud" on a system that is always silent, or "Unpowered" on passive bone lacing). When it cannot,
## the SRD substitutes 12.
static func complication(roll: int, applies: bool = true) -> Dictionary:
	if roll < 1 or roll > 12:
		return {"ok": false, "reason": "the complication table is d12, got %d" % roll}
	var used := roll if applies else FALLBACK
	var row: Dictionary = TABLE[used]
	return {
		"ok": true,
		"roll": roll,
		"used": used,
		"substituted": used != roll,
		"id": String(row["id"]),
		"name": String(row["name"]),
		"hook": String(row["hook"]),
		"extra_strain": float(row["extra_strain"]),
	}


## Total System Strain a complication adds to an implant.
static func extra_strain(roll: int, shares_category: bool = false) -> float:
	var row := complication(roll, true)
	if not bool(row["ok"]):
		return 0.0
	var extra := float(row["extra_strain"])
	if String(row["id"]) == "uncooperative" and not shares_category:
		return 0.0
	return extra
