## CWN SRD program-verb catalogue and deterministic execution preflight.
## Source: https://cwn.quadrifons.com/hacking/programs/program-verbs/
##         https://cwn.quadrifons.com/hacking/programs/
## This is a vanilla CWN component; NoöPunk powers belong in separate adapters.
class_name CwnProgramRules
extends RefCounted

## Each entry is [allowed targets, access cost, roll modifier, self-terminating].
## null modifier means the Verb is not resolved with the ordinary skill check.
const VERBS := {
	"Activate": [["Device", "Cyber"], 1, 1, true],
	"Analyze": [["Device", "Data"], 0, 1, true],
	"Append": [["Data"], 1, 0, true],
	"Blind": [["Device", "Cyber"], 1, 0, false],
	"Deactivate": [["Device", "Cyber"], 1, 1, true],
	"Decrypt": [["Data"], 1, 0, true],
	"Defend": [["Device", "Cyber"], 0, null, false],
	"Delude": [["Device"], 1, -1, false],
	"Erase": [["Data"], 1, 1, true],
	"Frisk": [["Cyber"], 0, 1, true],
	"Ghost": [["Avatar"], 1, 0, false],
	"Glitch": [["Device", "Cyber"], 0, 2, false],
	"Hijack": [["Device"], 1, -1, false],
	"Kill": [["Avatar"], 1, 0, true],
	"Lock": [["Device", "Data"], 1, 1, false],
	"Paralyze": [["Avatar"], 1, -2, false],
	"Replace": [["Data"], 1, 0, true],
	"Sabotage": [["Device", "Cyber"], 1, -1, true],
	"Sense": [["Device", "Data"], 0, 0, false],
	"Siege": [["Device"], 1, -2, false],
	"Silence": [["Avatar"], 1, 1, false],
	"Stun": [["Avatar"], 0, 0, true],
	"Terminate": [["Program"], 1, 0, true],
	"Unlock": [["Device", "Data"], 1, 1, true],
}

static func verb_info(verb: String) -> Dictionary:
	if not VERBS.has(verb):
		return {}
	var row: Array = VERBS[verb]
	return {"targets": row[0].duplicate(), "access_cost": row[1],
		"check_modifier": row[2], "self_terminating": row[3]}

## Subject names such as Camera are resolved to their SRD target families by the caller.
## A valid pair must already be compiled into the deck's available Memory.
static func preflight(verb: String, target_family: String, access: int,
		cpu_used: int, cpu_total: int, loaded_verbs: Array, loaded_subjects: Array,
		subject: String, target_is_friendly: bool = true) -> Dictionary:
	var row := verb_info(verb)
	if row.is_empty():
		return {"ok": false, "reason": "unknown_verb"}
	if not row["targets"].has(target_family):
		return {"ok": false, "reason": "invalid_target"}
	if not loaded_verbs.has(verb) or not loaded_subjects.has(subject):
		return {"ok": false, "reason": "not_loaded"}
	if verb == "Defend" and not target_is_friendly:
		return {"ok": false, "reason": "defend_requires_ally"}
	if cpu_used < 0 or cpu_total < 0 or cpu_used >= cpu_total:
		return {"ok": false, "reason": "no_cpu"}
	if access < int(row["access_cost"]):
		return {"ok": false, "reason": "insufficient_access"}
	return {"ok": true, "access_cost": row["access_cost"],
		"check_modifier": row["check_modifier"],
		"self_terminating": row["self_terminating"]}

## Called AFTER the appropriate CWN check (or special opposed resolution).
## A failed check still consumes the action and the Access; auto-terminating
## verbs release CPU immediately. The caller applies game-world effects.
static func resolve(preflight_result: Dictionary, access: int, cpu_used: int,
		check_success: bool, program_id: String = "") -> Dictionary:
	if not bool(preflight_result.get("ok", false)):
		return {"ok": false, "reason": "failed_preflight"}
	var next_access := access - int(preflight_result["access_cost"])
	var persistent := check_success and not bool(preflight_result["self_terminating"])
	return {"ok": true, "success": check_success, "access": next_access,
		"cpu_used": cpu_used + (1 if persistent else 0),
		"running_program": program_id if persistent else "",
		"access_spent": int(preflight_result["access_cost"])}

## Running programs end when a wired connection is broken or the hacker
## becomes unconscious. Wireless programs can also end when range is lost.
static func terminate_on_disconnect(wireless: bool, unconscious: bool,
		out_of_range: bool, jacked_out: bool) -> bool:
	return unconscious or (out_of_range if wireless else jacked_out)
