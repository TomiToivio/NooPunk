## Cities Without Number: hacking, as a rules kernel the engine can call.
##
## This is the Godot side of a procedure that already exists in Python
## (`src/rules/cwn_hacking.py`). The two are pinned to one another by
## `data/rules/cwn_hacking.json` and by `tests/test_cwn_hacking_contract.py`: change a number in the
## contract and both runtimes move, or the Python suite fails. Nothing here may invent a cost.
##
## What the source fixes, and what this file therefore implements:
##
## * **Access is a pool, not a bonus.** `INT modifier + Program rank + the deck's Bonus Access`,
##   spent per Verb and refreshed by an hour of deck work, once a day. Folding it into the roll
##   would delete the reason to prepare (SRD `hacking/cyberspace-basics/#access`).
## * **Security is a recorded ladder** — 7, 8, 9, 10, 12 — plus situation modifiers for an alerted
##   network, an important device, referee-judged tech quality and inside information.
##   A value that is not on the ladder is refused rather than guessed
##   (`hacking/hacking-mechanics/#common-cyberspace-security-levels`).
## * **Connection penalties are flat, not circumstances.** Wireless (-2) and a VR crown (-1) stack
##   to -3. The skill-check bound of -2..+2 covers *circumstances*; routing these through it would
##   silently swallow a point (`hacking/cyberspace-basics/#connecting-to-cyberspace`).
## * **Two failed checks against a node count as one Alert the Network action, and the network
##   alerts on the second such action** (`hacking/hacking-mechanics/#hacking-a-device-or-server`).
## * **Cyberware and drones:** `7 + ceil(HD or level / 3)`, or 8 for a drone with no operator
##   (`hacking/hacking-mechanics/#hacking-cyberware-or-drones`).
##
## What this file deliberately does not model: the Verb / Subject / program catalogue, deck
## hardware, ICE and demons. A Verb is a row with an Access cost and a check modifier — the caller
## supplies those from scenario data, because no catalogue has been author-ruled. The node graph is
## scenario state, not a rules object.
extends RefCounted
class_name CwnHackingRules

const CONTRACT_PATH := "res://data/rules/cwn_hacking.json"

static var _contract: Dictionary = {}

static func contract() -> Dictionary:
	if not _contract.is_empty():
		return _contract
	if not FileAccess.file_exists(CONTRACT_PATH):
		push_error("CwnHackingRules: missing contract at %s" % CONTRACT_PATH)
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CONTRACT_PATH))
	_contract = parsed if typeof(parsed) == TYPE_DICTIONARY else {}
	return _contract

## The recorded ladder, as integers. Anything else is a referee's call, not this file's.
static func security_levels() -> Array:
	var out: Array = []
	for key in contract().get("security_levels", {}).keys():
		out.append(int(key))
	out.sort()
	return out

## `INT modifier + Program rank + the deck's Bonus Access`, never negative.
## The caller supplies the modifier from the kernel of record (`rules_adapter.gd`) so this file
## holds no second attribute table.
static func access_pool(int_modifier: int, program_rank: int, deck_bonus: int = 0) -> int:
	if program_rank < 0:
		push_error("CwnHackingRules: Program rank cannot be negative (untrained is 0 with -1 penalty)")
		return 0
	var minimum := int(contract().get("access_pool", {}).get("minimum", 0))
	return maxi(minimum, int_modifier + program_rank + deck_bonus)

## The network's security target. `tech_quality` is the referee's -2..+2, `inside_info` the -3..-1
## an informant buys. Returns {"ok": true, "difficulty": n} or {"ok": false, "reason": ...}.
static func security_difficulty(
	security: int,
	alerted: bool = false,
	important_device: bool = false,
	tech_quality: int = 0,
	inside_info: int = 0
) -> Dictionary:
	if not security_levels().has(security):
		return {"ok": false, "reason": "unrecorded_security_level",
			"expected": security_levels(), "got": security}
	var modifiers: Dictionary = contract().get("security_modifiers", {})
	var quality_range: Array = modifiers.get("tech_quality_range", [-2, 2])
	var inside_range: Array = modifiers.get("inside_information_range", [1, 3])
	var difficulty := security
	difficulty += int(modifiers.get("alerted", 1)) if alerted else 0
	difficulty += int(modifiers.get("important_device", 1)) if important_device else 0
	# Both ranges are declared in the contract and enforced identically by the Python module
	# (`TECH_QUALITY_RANGE`, `INSIDE_INFORMATION_RANGE`), so an out-of-range caller cannot make the
	# two runtimes disagree. `inside_info` is a positive 1..3 that *lowers* the target; an honest 0
	# means no informant and must not be clamped up into one.
	difficulty += clampi(tech_quality, int(quality_range[0]), int(quality_range[1]))
	if inside_info != 0:
		difficulty -= clampi(inside_info, int(inside_range[0]), int(inside_range[1]))
	return {"ok": true, "difficulty": difficulty}

## `7 + ceil(HD or level / 3)`; a drone with no connected operator is difficulty 8.
static func cyberware_difficulty(level_or_hit_dice: int, has_operator: bool = true) -> Dictionary:
	var spec: Dictionary = contract().get("cyberware", {})
	if not has_operator:
		return {"ok": true, "difficulty": int(spec.get("unoperated_drone_difficulty", 8))}
	if level_or_hit_dice < 1:
		return {"ok": false, "reason": "level_or_hit_dice_must_be_positive"}
	var base := int(spec.get("base_difficulty", 7))
	var divisor := int(spec.get("hit_dice_divisor", 3))
	return {"ok": true, "difficulty": base + int(ceil(float(level_or_hit_dice) / float(divisor)))}

## One Int/Program check behind a Verb. `program_rank` -1 means untrained (-1 penalty, exactly as
## the skill kernel records it). Connection penalties enter as flat modifiers, never as
## circumstances, and circumstances are clamped to the kernel's -2..+2.
static func hacking_check(
	dice: Array,
	int_modifier: int,
	program_rank: int,
	difficulty: int,
	wireless: bool = false,
	vr_crown: bool = false,
	verb_modifier: int = 0,
	situational: int = 0
) -> Dictionary:
	if dice.size() != 2:
		return {"ok": false, "reason": "two_dice_required"}
	var first := int(dice[0])
	var second := int(dice[1])
	if first < 1 or first > 6 or second < 1 or second > 6:
		return {"ok": false, "reason": "each_die_is_1_to_6"}
	if program_rank < -1:
		return {"ok": false, "reason": "program_rank_must_be_-1_to_4"}
	var untrained := program_rank < 0
	var skill_level := 0 if untrained else program_rank
	var connection: Dictionary = contract().get("connection", {})
	var penalty := (int(connection.get("wireless_penalty", -2)) if wireless else 0) \
		+ (int(connection.get("vr_crown_penalty", -1)) if vr_crown else 0)
	var circumstance := clampi(situational, -2, 2)
	var total := first + second + int_modifier + skill_level + int(verb_modifier) \
		+ penalty + circumstance - (1 if untrained else 0)
	return {
		"ok": true,
		"dice": [first, second],
		"attribute_modifier": int_modifier,
		"program_skill": skill_level,
		"untrained": untrained,
		"verb_modifier": int(verb_modifier),
		"connection_penalty": penalty,
		"situational": circumstance,
		"difficulty": int(difficulty),
		"total": total,
		"success": total >= int(difficulty),
	}

## The intruder clock: two failed checks per Alert action, two Alert actions to alert.
class AlertClock extends RefCounted:
	var failures := 0
	var alert_actions := 0
	var _failures_per_action := 2
	var _actions_to_alert := 2

	func _init(failures_per_action: int = 2, actions_to_alert: int = 2) -> void:
		_failures_per_action = maxi(1, failures_per_action)
		_actions_to_alert = maxi(1, actions_to_alert)

	## True when this failure completes another Alert action (callers log it; the network is not
	## yet necessarily alerted).
	func record_failure() -> bool:
		failures += 1
		if failures % _failures_per_action == 0:
			alert_actions += 1
			return true
		return false

	## A defender spent its Main action alerting. True when the network is now alerted.
	func record_alert_action() -> bool:
		alert_actions += 1
		return alerted()

	func alerted() -> bool:
		return alert_actions >= _actions_to_alert

	func to_dict() -> Dictionary:
		return {"failures": failures, "alert_actions": alert_actions}

	func from_dict(data: Dictionary) -> void:
		failures = int(data.get("failures", 0))
		alert_actions = int(data.get("alert_actions", 0))

static func new_alert_clock() -> AlertClock:
	var spec: Dictionary = contract().get("alert", {})
	return AlertClock.new(
		int(spec.get("failures_per_alert_action", 2)),
		int(spec.get("alert_actions_to_alert", 2))
	)
