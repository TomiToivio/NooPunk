## Cities Without Number — cyberware operations: installation, removal and Alienation.
##
## Transcribed from the SRD (CC0):
##   ``gear-vehicles-cyberware/cyberware/installing-cyberware``
##   ``gear-vehicles-cyberware/cyberware/removing-cyberware``
##   ``gear-vehicles-cyberware/cyberware/cyberware-alienation``
##
## Dice are arguments. This module never rolls; callers pass totals, so a scenario can be replayed.
extends RefCounted
class_name CwnCyberwareOps

##: Installation terms by the implant's System Strain cost. `max_strain` is inclusive.
const STRAIN_TIERS := [
	{"max_strain": 0.0, "cost": 100, "recovery": "1 hour", "difficulty": 7},
	{"max_strain": 0.5, "cost": 500, "recovery": "1 day", "difficulty": 8},
	{"max_strain": 1.0, "cost": 2500, "recovery": "4 days", "difficulty": 10},
	{"max_strain": 3.0, "cost": 12500, "recovery": "2 weeks", "difficulty": 11},
	{"max_strain": 999999.0, "cost": 50000, "recovery": "1 month", "difficulty": 12},
]

##: Surgical-equipment modifier by theatre level (0 = none, 1/2/3 as the SRD's table).
const THEATRE_MODIFIERS := {0: 0, 1: 0, 2: 1, 3: 2}

##: Room modifier; `lacks_room` is the SRD's −1.
const ROOM_MODIFIERS := {
	"lacks_room": -1,
	"clean_room": 0,
	"sterile": 1,
	"clinic": 2,
}

##: Chrome syndromes and their Alienation-maximum bonus. Each may be taken once.
const SYNDROMES := {
	"brutal": 4,
	"candid": 3,
	"cold": 4,
	"distant": 3,
	"exultant": 3,
	"fearless": 4,
	"hypervigilant": 3,
	"murderous": 6,
}


## Cost, recovery time and difficulty of implanting a system of the given System Strain cost.
static func install_terms(system_strain: float) -> Dictionary:
	if system_strain < 0.0:
		return {"ok": false, "reason": "System Strain cannot be negative"}
	for tier in STRAIN_TIERS:
		if system_strain <= float(tier["max_strain"]):
			return {
				"ok": true,
				"cost": int(tier["cost"]),
				"recovery": String(tier["recovery"]),
				"difficulty": int(tier["difficulty"]),
				"system_strain": system_strain,
			}
	return {"ok": false, "reason": "unreachable tier"}


## The surgeon's modifier: theatre equipment, room quality, and whether the cyber is new.
static func surgery_modifier(theatre_level: int = 1, room: String = "clean_room", new_cyber: bool = false) -> Dictionary:
	if not THEATRE_MODIFIERS.has(theatre_level):
		return {"ok": false, "reason": "theatre level must be 0-3"}
	if not ROOM_MODIFIERS.has(room):
		return {"ok": false, "reason": "unknown room quality: %s" % room}
	var total: int = int(THEATRE_MODIFIERS[theatre_level]) + int(ROOM_MODIFIERS[room]) + (1 if new_cyber else 0)
	return {"ok": true, "modifier": total}


## Installation outcome from the surgeon's total against the difficulty.
##
## SRD: failing by one or two points still succeeds but rolls an implant complication; failing by more
## than two maximises System Strain, drops the patient to 1 hit point, and marks the cyber as used.
static func resolve_installation(check_total: int, difficulty: int, complication: String = "") -> Dictionary:
	var margin := check_total - difficulty
	if margin >= 0:
		return {"ok": true, "outcome": "success", "margin": margin, "complication": ""}
	if margin >= -2:
		return {
			"ok": true,
			"outcome": "success_with_complication",
			"margin": margin,
			"complication": complication if not complication.is_empty() else "roll on the implant complication table",
		}
	return {
		"ok": true,
		"outcome": "failure",
		"margin": margin,
		"system_strain_maximised": true,
		"hit_points": 1,
		"cyber_becomes_used": true,
		"complication": "",
	}


## Safe removal takes an hour at the installation difficulty; a doc who does not care takes ten
## minutes and the patient almost always dies.
static func removal_terms(install_difficulty: int, gentle: bool = true) -> Dictionary:
	if install_difficulty <= 0:
		return {"ok": false, "reason": "installation difficulty must be positive"}
	return {
		"ok": true,
		"difficulty": install_difficulty,
		"minutes": 60 if gentle else 10,
		"patient_survives": gentle,
	}


## Gentle removal: success keeps the implant intact; failure ruins it but leaves the patient healthy.
## Either way the implant's permanent System Strain is gone.
static func resolve_removal(check_total: int, difficulty: int) -> Dictionary:
	return {
		"ok": true,
		"implant_intact": check_total >= difficulty,
		"patient_healthy": true,
		"system_strain_removed": true,
	}


## Salvaging from a body: difficulty 10, and nothing is recoverable after 24 hours.
static func resolve_salvage(check_total: int, hours_dead: float, difficulty: int = 10) -> Dictionary:
	if hours_dead > 24.0:
		return {"ok": true, "recovered": false, "reason": "dead more than 24 hours — unsalvageable"}
	return {"ok": true, "recovered": check_total >= difficulty, "reason": ""}


## After removal the doc re-checks at difficulty 10: success means used-but-functional, failure means
## secondhand cyber carrying an unavoidable implantation complication.
static func resolve_reuse(check_total: int, difficulty: int = 10) -> Dictionary:
	if check_total >= difficulty:
		return {"ok": true, "state": "used", "complication": ""}
	return {"ok": true, "state": "secondhand", "complication": "random implantation complication"}


## Alienation gained by implanting: the System Strain cost rounded up, plus 2 for Nerve cyberware.
static func alienation_gain(system_strain: float, nerve: bool = false) -> int:
	if system_strain <= 0.0:
		return 0
	return ceili(system_strain) + (2 if nerve else 0)


## A character's maximum Alienation: Wisdom plus the bonuses of the chrome syndromes they carry.
##
## Repeats are refused — the SRD says the same syndrome cannot be picked twice.
static func max_alienation(wisdom: int, syndromes: Array = []) -> Dictionary:
	var bonus := 0
	var seen: Array = []
	var unknown: Array = []
	for syndrome in syndromes:
		var key := String(syndrome)
		if not SYNDROMES.has(key):
			unknown.append(key)
		elif seen.has(key):
			return {"ok": false, "reason": "syndrome taken twice: %s" % key}
		else:
			seen.append(key)
			bonus += int(SYNDROMES[key])
	return {"ok": unknown.is_empty(), "maximum": wisdom + bonus, "unknown": unknown}


## The Alienation check: roll 1d20; equal to or under current Alienation gains one point.
static func alienation_check(roll: int, current: int) -> Dictionary:
	return {"ok": roll >= 1 and roll <= 20, "gains_point": roll <= current, "roll": roll}


## One week of therapy lowers Alienation by one, never below the permanent amount the cyber imposes.
static func therapy_week(current: int, permanent: int) -> int:
	return maxi(permanent, current - 1)


## Alienation above the character's maximum is cyber-induced psychosis; the character becomes an NPC.
static func is_psychotic(current: int, maximum: int) -> bool:
	return current > maximum
