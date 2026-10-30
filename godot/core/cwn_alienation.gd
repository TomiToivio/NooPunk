extends RefCounted
class_name CwnAlienation
## Cyberware Alienation — CWN SRD §3.6.8 (3.6.8.1 gaining/losing, 3.6.8.2 psychosis).
##
## An optional rule, and this module says so rather than assuming it: the SRD's default cyber rules do not
## make chrome change a character mechanically. Campaigns that use Alienation follow the three rules below.
##
## The details that are easy to get subtly wrong, and are therefore pinned by tests:
##
## * A system's Alienation is its **System Strain cost rounded up**, so a 0.5-cost system is 1 — not 0.
## * **Nerve** cyberware adds **+2 per system** on top of that.
## * A user breaks down when their total **exceeds** Wisdom — equal to Wisdom is still functional.
## * The check is `1d20 <= current Alienation`, so a character at 0 can never gain from it.
## * Going over the maximum forces a Mental save: success lets them pick a new chrome syndrome,
##   failure means cyber-induced psychosis (CIP) — two different outcomes, not one.
## * Therapy drops the score by one per week and **cannot go below the permanent floor** set by the
##   cyberware they still carry. Removing cyberware lowers that floor.

const THERAPY_COST_PER_WEEK := 2000
const NERVE_SURCHARGE := 2

##: Chrome syndromes and the Alienation-maximum bonus each grants (§3.6.8.2). Each may be taken once.
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

enum Outcome { NONE, PICK_SYNDROME, PSYCHOSIS }


static func alienation_for_system(strain_cost: float, is_nerve: bool = false) -> int:
	## Ceil, because the SRD rounds up: eye and ear mods discounted by cybereyes/cyberears still cost 1.
	var points := int(ceil(strain_cost))
	if is_nerve:
		points += NERVE_SURCHARGE
	return points


static func permanent_total(systems: Array) -> int:
	## `systems` is an array of {strain_cost: float, nerve: bool}.
	var total := 0
	for system in systems:
		total += alienation_for_system(
			float(system.get("strain_cost", 0.0)),
			bool(system.get("nerve", false)))
	return total


static func maximum(wisdom: int, syndromes: Array = []) -> int:
	## The SRD allows a chrome syndrome to raise the ceiling; repeats are refused by the caller.
	var bonus := 0
	for syndrome in syndromes:
		bonus += int(SYNDROMES.get(String(syndrome), 0))
	return wisdom + bonus


## Validate a syndrome list: every name known, none repeated.
static func validate_syndromes(syndromes: Array) -> Dictionary:
	var seen: Array = []
	var unknown: Array = []
	for syndrome in syndromes:
		var key := String(syndrome)
		if not SYNDROMES.has(key):
			unknown.append(key)
		elif seen.has(key):
			return {"ok": false, "reason": "syndrome taken twice: %s" % key, "unknown": []}
		else:
			seen.append(key)
	return {"ok": unknown.is_empty(), "unknown": unknown}


static func is_psychotic(alienation: int, wisdom: int) -> bool:
	## Strictly greater: a character sitting exactly at their Wisdom limit is still themselves.
	return alienation > maximum(wisdom)


static func check_gains_point(d20: int, current_alienation: int) -> bool:
	if d20 < 1 or d20 > 20:
		raise_error(d20)
	return d20 <= current_alienation


static func resolve_over_maximum(mental_save_succeeds: bool) -> int:
	## Returning an enum rather than a bool keeps the two outcomes distinguishable at the call site.
	return Outcome.PICK_SYNDROME if mental_save_succeeds else Outcome.PSYCHOSIS


static func after_therapy(current_alienation: int, permanent_floor: int) -> int:
	## One point per week of therapy, never below the floor the remaining cyberware imposes.
	return max(permanent_floor, current_alienation - 1)


static func raise_error(d20: int) -> void:
	push_error("1d20 result %d outside 1..20" % d20)
