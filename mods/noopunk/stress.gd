## Stress, Breakdowns and Hardening — a NoöPunk overlay (#928).
##
## Ashes Without Number's psychological Stress procedure, re-expressed as an **optional** overlay on
## Cities Without Number (`docs/design/FOUNDATIONAL_LOCK_897.md`). The mechanics and their values are
## in `res://data/rules/awn_stress.json`; this module is only the arithmetic and the state.
##
## ## What it may not do
##
## An overlay colours the game; it does not resolve it. So this module never rolls a die, never reads an
## attribute, never computes a save or a skill check, and never imports from `godot/core/`. When the
## rules call for a d20 Mental save or a Heal check, this module reports the **penalty it wants applied**
## and the caller — the screen, or the session that owns the core — asks the core, rolls, and hands the
## outcome back in. The same rule covers the dice inside this subsystem (`1d6` for a first kill, `-1d10`
## for a major goal, `1d4` per indulged day): the caller passes the number in.
##
## ## What it adds
##
## One integer meter, one escalating check penalty, a list of consequence codes, and an audit trail.
## CWN keeps its own WIS score, its own Mental save, its own System Strain and its own Alienation track;
## a character can be over the Stress ceiling and not Alienated, and the reverse. The two modules never
## read each other.
##
## ## Order of application
##
## 1. base value of the event, plus every selected modifier;
## 2. minus one point per active addiction;
## 3. at the end of the scene, minus the Hardening resistance (one point per Hardening, once per scene);
## 4. the remainder moves the meter, and only then is the Wisdom ceiling tested.
extends RefCounted
class_name NoopunkStress

const CONTRACT_PATH := "res://data/rules/awn_stress.json"
const TRACKER_FORMAT := "noopunk.stress_tracker"
const TRACKER_VERSION := 1

##: The audit log is for the table, not for a save file that must stay small.
const AUDIT_LIMIT := 200

static var _contract: Dictionary = {}


# --------------------------------------------------------------------------- #
# Contract
# --------------------------------------------------------------------------- #


## The shipped contract, parsed once. A missing or broken file is a hard failure rather than a
## silently empty rule set.
static func contract() -> Dictionary:
	if not _contract.is_empty():
		return _contract
	if not FileAccess.file_exists(CONTRACT_PATH):
		push_error("NoopunkStress: contract missing at %s" % CONTRACT_PATH)
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CONTRACT_PATH))
	if parsed is Dictionary:
		_contract = parsed
	else:
		push_error("NoopunkStress: contract at %s is not a JSON object" % CONTRACT_PATH)
	return _contract


static func default_enabled() -> bool:
	return bool(Dictionary(contract().get("module", {})).get("default_enabled", false))


static func event_ids() -> Array:
	return _ids(Dictionary(contract().get("gaining", {})).get("events", []))


static func noopunk_event_ids() -> Array:
	return _ids(Dictionary(contract().get("noopunk_events", {})).get("events", []))


static func breakdown_ids() -> Array:
	return _ids(Dictionary(contract().get("breakdowns", {})).get("options", []))


static func scar_ids() -> Array:
	return _ids(Dictionary(contract().get("scars", {})).get("options", []))


static func recovery_ids() -> Array:
	return _ids(Dictionary(contract().get("recovery", {})).get("events", []))


static func event(id: String) -> Dictionary:
	return _find(Dictionary(contract().get("gaining", {})).get("events", []), id)


static func noopunk_event(id: String) -> Dictionary:
	return _find(Dictionary(contract().get("noopunk_events", {})).get("events", []), id)


static func breakdown(id: String) -> Dictionary:
	return _find(Dictionary(contract().get("breakdowns", {})).get("options", []), id)


static func scar(id: String) -> Dictionary:
	return _find(Dictionary(contract().get("scars", {})).get("options", []), id)


static func recovery(id: String) -> Dictionary:
	return _find(Dictionary(contract().get("recovery", {})).get("events", []), id)


# --------------------------------------------------------------------------- #
# Tracker lifecycle
# --------------------------------------------------------------------------- #


## `options`: `level` (default 1), `enabled` (default: the contract's flag), `addiction` (bool),
## `scars`, `hardening_count`, `stress`.
static func new_tracker(wisdom: int, options: Dictionary = {}) -> Dictionary:
	var enabled: bool = bool(options.get("enabled", default_enabled()))
	var tracker: Dictionary = {
		"format": TRACKER_FORMAT,
		"version": TRACKER_VERSION,
		"enabled": enabled,
		"wisdom": maxi(1, wisdom),
		"level": maxi(1, int(options.get("level", 1))),
		"stress": maxi(0, int(options.get("stress", 0))),
		"hardening_count": maxi(0, int(options.get("hardening_count", 0))),
		"scars": Array(options.get("scars", [])).duplicate(),
		"active_breakdown": "",
		"checks_made": 0,
		"awaiting_breakdown": false,
		"pending_save": {"required": false, "kind": "mental", "penalty": 0},
		"last_check": {},
		"day": 1,
		"recovered_today": {},
		"scene": _empty_scene(),
		"addiction": {
			"enabled": bool(options.get("addiction", false)),
			"addictions": [],
			"system_strain": 0,
			"missed_today": false,
			"months_clean": 0,
			"weeks_clean": 0,
		},
		"audit": [],
		"seq": 0,
	}
	if not enabled:
		tracker["audit"].append(_entry(tracker, "module", {"enabled": false}))
	return tracker


static func is_enabled(tracker: Dictionary) -> bool:
	return bool(tracker.get("enabled", false))


static func stress(tracker: Dictionary) -> int:
	return int(tracker.get("stress", 0))


## The ceiling is the character's CWN WIS score, not a new attribute.
static func threshold(tracker: Dictionary) -> int:
	return int(tracker.get("wisdom", 1))


## How far over the ceiling the character is. Zero means "at or below", which is safe.
static func over_by(tracker: Dictionary) -> int:
	return maxi(0, stress(tracker) - threshold(tracker))


static func is_over(tracker: Dictionary) -> bool:
	return stress(tracker) > threshold(tracker)


static func hardening_count(tracker: Dictionary) -> int:
	return int(tracker.get("hardening_count", 0))


static func scars(tracker: Dictionary) -> Array:
	return Array(tracker.get("scars", [])).duplicate()


static func has_scar(tracker: Dictionary, id: String) -> bool:
	return Array(tracker.get("scars", [])).has(id)


static func active_breakdown(tracker: Dictionary) -> String:
	return String(tracker.get("active_breakdown", ""))


## Consequences currently in force, as contract rows rather than prose. Empty when nothing is active.
static func active_conditions(tracker: Dictionary) -> Array:
	var rows: Array = []
	var active: String = active_breakdown(tracker)
	if not active.is_empty():
		var row: Dictionary = breakdown(active)
		rows.append({"kind": "breakdown", "id": active, "label": row.get("label", active),
			"effects": row.get("effects", {})})
	for id in scars(tracker):
		var scar_row: Dictionary = scar(String(id))
		rows.append({"kind": "scar", "id": String(id), "label": scar_row.get("label", id),
			"effects": scar_row.get("effects", {})})
	return rows


# --------------------------------------------------------------------------- #
# Gaining Stress
# --------------------------------------------------------------------------- #


## Start a scene. Hardening resistance is *per scene*, so the scene is the unit that resets it.
static func begin_scene(tracker: Dictionary) -> Dictionary:
	tracker["scene"] = _empty_scene()
	_audit(tracker, "scene", {"opened": true})
	return {"ok": true}


## Record one stress-inducing event. Nothing moves the meter yet: the rules gain Stress at the end of
## the scene, so this accumulates and :func:`end_scene` applies it.
##
## `options`: `modifiers` (modifier ids), `rolls` ({id: total} for anything diced), `value` (for a
## ranged entry the table sets), `participated` (bool, default true).
static func award(tracker: Dictionary, event_id: String, options: Dictionary = {}) -> Dictionary:
	if not is_enabled(tracker):
		return {"ok": true, "enabled": false, "applied": 0, "pending": 0}

	var row: Dictionary = event(event_id)
	if row.is_empty():
		row = noopunk_event(event_id)
	if row.is_empty():
		return {"ok": false, "reason": "unknown stress event: %s" % event_id}

	if not bool(options.get("participated", true)):
		# Mere presence is not participation. The contract says so; this is where it is enforced.
		return {"ok": true, "applied": 0, "pending": 0, "skipped": "not_a_participant"}

	if not active_breakdown(tracker).is_empty():
		_audit(tracker, "suppressed", {"event": event_id, "reason": "breakdown"})
		return {"ok": true, "applied": 0, "pending": 0, "suppressed": "breakdown"}

	if has_scar(tracker, "bloodthirsty") and event_id == "kill_human":
		_audit(tracker, "suppressed", {"event": event_id, "reason": "bloodthirsty"})
		return {"ok": true, "applied": 0, "pending": 0, "suppressed": "bloodthirsty"}

	var base := _base_amount(row, options, event_id)
	if not bool(base.get("ok", false)):
		return base
	var raw: int = int(base["value"])

	var chosen: Array = Array(options.get("modifiers", []))
	var modifier_rows: Array = []
	for modifier in Array(row.get("modifiers", [])):
		var mod_row: Dictionary = modifier
		var mod_id := String(mod_row.get("id", ""))
		if not chosen.has(mod_id):
			continue
		var mod_amount := _amount(mod_row.get("stress", 0), options, mod_id)
		if not bool(mod_amount.get("ok", false)):
			return mod_amount
		raw += int(mod_amount["value"])
		modifier_rows.append({"id": mod_id, "value": int(mod_amount["value"])})

	# Each addiction blunts one incoming point of Stress. Applied before the scene-level resistance.
	var blunted := mini(raw, _addiction_count(tracker))
	raw = maxi(0, raw - blunted)

	var scene: Dictionary = tracker.get("scene", _empty_scene())
	var causes: Array = scene.get("causes", [])
	causes.append({"event": event_id, "raw": raw, "modifiers": modifier_rows,
		"system": String(row.get("system", "awn"))})
	scene["causes"] = causes
	scene["raw"] = int(scene.get("raw", 0)) + raw
	tracker["scene"] = scene

	var projected := _projected_gain(tracker)
	_audit(tracker, "gain", {"event": event_id, "raw": raw, "projected": projected, "blunted": blunted})
	return {"ok": true, "event": event_id, "raw": raw, "modifiers": modifier_rows,
		"blunted": blunted, "pending": projected, "resisted": int(scene.get("raw", 0)) - projected}


## Close the scene: apply the accumulated Stress, then test the ceiling.
static func end_scene(tracker: Dictionary) -> Dictionary:
	if not is_enabled(tracker):
		return {"ok": true, "enabled": false}
	var scene: Dictionary = tracker.get("scene", _empty_scene())
	var raw := int(scene.get("raw", 0))
	var resistance := _resistance_for_scene(tracker, scene)
	var resisted := mini(raw, resistance)
	var applied := raw - resisted
	tracker["stress"] = maxi(0, stress(tracker) + applied)
	tracker["scene"] = _empty_scene()

	var result: Dictionary = {
		"ok": true,
		"raw": raw,
		"resisted": resisted,
		"applied": applied,
		"stress": stress(tracker),
		"threshold": threshold(tracker),
		"save": pending_save(tracker),
	}
	# A new dose that leaves the total above WIS asks for a check. A dose that does not cross the
	# ceiling — and a scene that applied nothing — asks for nothing.
	if applied > 0 and is_over(tracker):
		result["save"] = _arm_check(tracker)
	_audit(tracker, "scene", {"closed": true, "applied": applied, "resisted": resisted,
		"stress": stress(tracker)})
	return result


## The check the character owes right now, if any.
static func pending_save(tracker: Dictionary) -> Dictionary:
	return Dictionary(tracker.get("pending_save", {"required": false, "kind": "mental", "penalty": 0})).duplicate()


## The penalty the next check carries, whatever the current pending state. Useful for a UI that shows
## the escalation before the next scene.
static func next_penalty(tracker: Dictionary) -> int:
	var rules: Dictionary = contract().get("threshold", {})
	return int(rules.get("first_penalty", -2)) + int(rules.get("penalty_step", -2)) \
		* int(tracker.get("checks_made", 0))


# --------------------------------------------------------------------------- #
# The check, and what happens when it fails
# --------------------------------------------------------------------------- #


## Hand the core's outcome back in. The overlay never rolls; `success` comes from the CWN Mental save.
static func resolve_save(tracker: Dictionary, success: bool) -> Dictionary:
	var pending: Dictionary = pending_save(tracker)
	if not bool(pending.get("required", false)):
		return {"ok": false, "reason": "no check is pending"}
	var penalty := int(pending.get("penalty", -2))
	tracker["checks_made"] = int(tracker.get("checks_made", 0)) + 1
	tracker["pending_save"] = {"required": false, "kind": "mental", "penalty": 0}
	tracker["last_check"] = {"success": success, "penalty": penalty}
	_audit(tracker, "save", {"success": success, "penalty": penalty})
	var result: Dictionary = {
		"ok": true,
		"success": success,
		"penalty": penalty,
		"checks_made": int(tracker["checks_made"]),
		# A successful check holds the line; it does not remove Stress, so the escalation continues.
		"next_penalty": next_penalty(tracker),
		"stress": stress(tracker),
	}
	if success:
		return result
	tracker["awaiting_breakdown"] = true
	result["awaiting_breakdown"] = true
	result["can_harden"] = true
	result["breakdowns"] = breakdown_ids()
	result["scars"] = _available_scars(tracker)
	return result


## The player picks a Breakdown. Its effects are returned as data for the caller to apply; the overlay
## does not edit a character sheet.
static func choose_breakdown(tracker: Dictionary, id: String) -> Dictionary:
	if not bool(tracker.get("awaiting_breakdown", false)):
		return {"ok": false, "reason": "no breakdown is owed"}
	var row: Dictionary = breakdown(id)
	if row.is_empty():
		return {"ok": false, "reason": "unknown breakdown: %s" % id}
	tracker["active_breakdown"] = id
	tracker["awaiting_breakdown"] = false
	_audit(tracker, "breakdown", {"id": id})
	return {"ok": true, "breakdown": id, "effects": row.get("effects", {}),
		"ends_when": "stress_at_or_below_wisdom", "label": row.get("label", id)}


## The alternative to a Breakdown: give something up, and come to terms with it.
static func harden(tracker: Dictionary, scar_id: String) -> Dictionary:
	if not bool(tracker.get("awaiting_breakdown", false)):
		return {"ok": false, "reason": "hardening is only available when a breakdown is owed"}
	var row: Dictionary = scar(scar_id)
	if row.is_empty():
		return {"ok": false, "reason": "unknown psychic scar: %s" % scar_id}
	if has_scar(tracker, scar_id):
		return {"ok": false, "reason": "a psychic scar can only be taken once: %s" % scar_id}
	var taken: Array = Array(tracker.get("scars", []))
	taken.append(scar_id)
	tracker["scars"] = taken
	tracker["hardening_count"] = hardening_count(tracker) + 1
	tracker["stress"] = 0
	tracker["awaiting_breakdown"] = false
	tracker["active_breakdown"] = ""
	# Stress is now zero, so the escalating penalty has nothing to escalate from.
	tracker["checks_made"] = 0
	tracker["pending_save"] = {"required": false, "kind": "mental", "penalty": 0}
	var addiction_opened := false
	if scar_id == "addicted" and not bool(Dictionary(tracker.get("addiction", {})).get("enabled", false)):
		var addiction: Dictionary = Dictionary(tracker.get("addiction", {}))
		addiction["enabled"] = true
		tracker["addiction"] = addiction
		addiction_opened = true
	_audit(tracker, "harden", {"scar": scar_id, "hardening_count": int(tracker["hardening_count"])})
	return {"ok": true, "hardening_count": int(tracker["hardening_count"]), "stress": 0,
		"scar": scar_id, "effects": row.get("effects", {}), "scene_resistance": _resistance(tracker),
		"addiction_opened": addiction_opened, "irreversible": true}


# --------------------------------------------------------------------------- #
# Recovery
# --------------------------------------------------------------------------- #


## Advance the calendar. Talk and safe days are limited per day, so the day is tracked here.
static func new_day(tracker: Dictionary) -> Dictionary:
	tracker["day"] = int(tracker.get("day", 1)) + 1
	tracker["recovered_today"] = {}
	var addiction: Dictionary = Dictionary(tracker.get("addiction", {}))
	if bool(addiction.get("enabled", false)):
		addiction["missed_today"] = false
		tracker["addiction"] = addiction
	_audit(tracker, "day", {"day": int(tracker["day"])})
	return {"ok": true, "day": int(tracker["day"])}


## `options`: `check_success` (bool, for the conversation entry), `roll` (the dice total for a ranged
## entry), `failed_chance` (bool, for a scar whose recovery has a flat chance to fail), `goal` (id).
static func recover(tracker: Dictionary, id: String, options: Dictionary = {}) -> Dictionary:
	if not is_enabled(tracker):
		return {"ok": true, "enabled": false}
	var row: Dictionary = recovery(id)
	if row.is_empty():
		return {"ok": false, "reason": "unknown recovery: %s" % id}

	var blocker := String(row.get("blocked_by_scar", ""))
	if not blocker.is_empty() and has_scar(tracker, blocker):
		return {"ok": false, "reason": "%s cannot use this recovery: %s" % [blocker, id]}

	var per_day := int(row.get("per_day", 0))
	var used: Dictionary = Dictionary(tracker.get("recovered_today", {}))
	if per_day > 0 and int(used.get(id, 0)) >= per_day:
		return {"ok": false, "reason": "%s is already used today" % id}

	if bool(options.get("failed_chance", false)) and has_scar(tracker, "bloodthirsty"):
		_audit(tracker, "recover", {"id": id, "failed_chance": true})
		return {"ok": true, "recovered": 0, "failed_chance": true, "stress": stress(tracker)}

	var check: Dictionary = Dictionary(row.get("check", {}))
	if not check.is_empty() and not bool(options.get("check_success", false)):
		used[id] = int(used.get(id, 0)) + 1
		tracker["recovered_today"] = used
		var helper := int(Dictionary(row.get("on_failure", {})).get("helper_stress", 0))
		_audit(tracker, "recover", {"id": id, "check": false, "helper_stress": helper})
		return {"ok": true, "recovered": 0, "check": false, "helper_stress": helper,
			"stress": stress(tracker),
			"note": "the helper carries the Stress; apply it to the helper's own tracker"}

	var amount := _amount(row.get("stress", 0), options, id)
	if not bool(amount.get("ok", false)):
		return amount

	used[id] = int(used.get(id, 0)) + 1
	tracker["recovered_today"] = used
	var before := stress(tracker)
	var after := maxi(0, before + int(amount["value"]))
	tracker["stress"] = after
	var ended := false
	# Back at or below the ceiling the escalating penalty resets, whether or not a Breakdown was
	# running; a Breakdown itself also ends there.
	if after <= threshold(tracker):
		tracker["checks_made"] = 0
		tracker["pending_save"] = {"required": false, "kind": "mental", "penalty": 0}
		if not active_breakdown(tracker).is_empty():
			tracker["active_breakdown"] = ""
			ended = true
	_audit(tracker, "recover", {"id": id, "recovered": before - after, "stress": after,
		"ended_breakdown": ended})
	return {"ok": true, "recovered": before - after, "stress": after,
		"breakdown_ended": ended,
		"system_strain": int(Dictionary(row.get("cost", {})).get("system_strain", 0)),
		"check": true}


static func can_recover(tracker: Dictionary, id: String) -> bool:
	var row: Dictionary = recovery(id)
	if row.is_empty():
		return false
	var blocker := String(row.get("blocked_by_scar", ""))
	if not blocker.is_empty() and has_scar(tracker, blocker):
		return false
	var per_day := int(row.get("per_day", 0))
	if per_day <= 0:
		return true
	var used: Dictionary = Dictionary(tracker.get("recovered_today", {}))
	return int(used.get(id, 0)) < per_day


# --------------------------------------------------------------------------- #
# Addiction — its own opt-in submodule, off unless the table says otherwise
# --------------------------------------------------------------------------- #


static func addiction_enabled(tracker: Dictionary) -> bool:
	return bool(Dictionary(tracker.get("addiction", {})).get("enabled", false))


## Open the submodule. It is never opened by enabling the Stress module.
static func enable_addiction(tracker: Dictionary, id: String = "") -> Dictionary:
	if not is_enabled(tracker):
		return {"ok": false, "reason": "the stress module is off"}
	var addiction: Dictionary = Dictionary(tracker.get("addiction", {}))
	addiction["enabled"] = true
	if not id.is_empty():
		var list: Array = Array(addiction.get("addictions", []))
		if not list.has(id):
			list.append(id)
		addiction["addictions"] = list
	tracker["addiction"] = addiction
	_audit(tracker, "addiction", {"enabled": true, "id": id})
	return {"ok": true, "enabled": true, "addictions": Array(addiction.get("addictions", [])).duplicate()}


static func addictions(tracker: Dictionary) -> Array:
	return Array(Dictionary(tracker.get("addiction", {})).get("addictions", [])).duplicate()


## One indulged day. `options.die` is the caller's 1d4.
static func indulge(tracker: Dictionary, options: Dictionary = {}) -> Dictionary:
	if not addiction_enabled(tracker):
		return {"ok": false, "reason": "the addiction submodule is off"}
	var count := _addiction_count(tracker)
	if count == 0:
		return {"ok": false, "reason": "no addiction to indulge"}
	var amount := _amount(Dictionary(contract().get("addiction", {})).get("effects_while_indulged", {}).get("daily_stress_removed", "1d4"), options, "daily")
	if not bool(amount.get("ok", false)):
		return amount
	var removed := int(amount["value"]) * count
	var before := stress(tracker)
	var after := maxi(0, before - removed)
	tracker["stress"] = after
	var addiction: Dictionary = Dictionary(tracker.get("addiction", {}))
	addiction["missed_today"] = false
	tracker["addiction"] = addiction
	var ended := false
	if not active_breakdown(tracker).is_empty() and after <= threshold(tracker):
		tracker["active_breakdown"] = ""
		tracker["checks_made"] = 0
		ended = true
	_audit(tracker, "addiction", {"indulged": true, "removed": before - after})
	return {"ok": true, "removed": before - after, "stress": after, "breakdown_ended": ended,
		"requires_strain_check": false}


## A day without the vice: privation, no rest recovery, and one point of Stress that Hardening does
## not resist.
static func miss_indulgence(tracker: Dictionary) -> Dictionary:
	if not addiction_enabled(tracker) or _addiction_count(tracker) == 0:
		return {"ok": false, "reason": "no active addiction"}
	var row: Dictionary = Dictionary(contract().get("addiction", {})).get("missed_day", {})
	var points := int(row.get("stress", 1))
	if not active_breakdown(tracker).is_empty():
		points = 0
	tracker["stress"] = maxi(0, stress(tracker) + points)
	var addiction: Dictionary = Dictionary(tracker.get("addiction", {}))
	addiction["missed_today"] = true
	tracker["addiction"] = addiction
	_audit(tracker, "addiction", {"missed": true, "stress": points})
	return {"ok": true, "stress": stress(tracker), "privation": bool(row.get("counts_as_privation", true)),
		"blocks_rest_recovery": bool(row.get("blocks_rest_recovery", true)), "gained": points}


## A night's rest cannot restore Strain while the day was missed. The caller asks before healing.
static func rest_recovery_blocked(tracker: Dictionary) -> bool:
	return bool(Dictionary(tracker.get("addiction", {})).get("missed_today", false))


## Monthly check. `success` comes from the core's Physical save.
static func monthly_check(tracker: Dictionary, success: bool) -> Dictionary:
	if not addiction_enabled(tracker):
		return {"ok": false, "reason": "the addiction submodule is off"}
	var addiction: Dictionary = Dictionary(tracker.get("addiction", {}))
	if success:
		addiction["months_clean"] = int(addiction.get("months_clean", 0)) + 1
		tracker["addiction"] = addiction
		_audit(tracker, "addiction", {"month": true, "success": true})
		return {"ok": true, "success": true, "system_strain": int(addiction.get("system_strain", 0))}
	addiction["system_strain"] = int(addiction.get("system_strain", 0)) + 1
	tracker["addiction"] = addiction
	_audit(tracker, "addiction", {"month": true, "success": false,
		"system_strain": int(addiction["system_strain"])})
	return {"ok": true, "success": false, "gained_strain": 1,
		"system_strain": int(addiction["system_strain"]),
		"death_window_days": int(Dictionary(contract().get("addiction", {})).get("monthly", {}).get("at_capacity_death_window_days", 30))}


## Weekly attempt to get clean. `success` comes from the core's save; a helper with Heal may add it.
static func break_addiction(tracker: Dictionary, id: String, success: bool) -> Dictionary:
	if not addiction_enabled(tracker):
		return {"ok": false, "reason": "the addiction submodule is off"}
	var addiction: Dictionary = Dictionary(tracker.get("addiction", {}))
	var list: Array = Array(addiction.get("addictions", []))
	if not list.has(id):
		return {"ok": false, "reason": "not addicted to %s" % id}
	if not success:
		addiction["weeks_clean"] = int(addiction.get("weeks_clean", 0)) + 1
		tracker["addiction"] = addiction
		_audit(tracker, "addiction", {"clean_attempt": id, "success": false})
		return {"ok": true, "success": false, "weeks_clean": int(addiction["weeks_clean"])}
	list.erase(id)
	addiction["addictions"] = list
	tracker["addiction"] = addiction
	_audit(tracker, "addiction", {"clean_attempt": id, "success": true})
	return {"ok": true, "success": true, "addictions": list.duplicate()}


# --------------------------------------------------------------------------- #
# Persistence
# --------------------------------------------------------------------------- #


## The overlay persists itself, beside the core's save rather than inside it: the core's schema is not
## this module's to migrate.
static func to_dict(tracker: Dictionary) -> Dictionary:
	var copy: Dictionary = tracker.duplicate(true)
	copy["format"] = TRACKER_FORMAT
	copy["version"] = TRACKER_VERSION
	return copy


## Read a saved tracker back. A tracker written by an older build is upgraded, not rejected, and a
## save from a build without this module yields a disabled tracker rather than an error.
static func from_dict(data: Dictionary) -> Dictionary:
	if data.is_empty() or String(data.get("format", "")) != TRACKER_FORMAT:
		return new_tracker(int(data.get("wisdom", 10)), {"enabled": false})
	var loaded: Dictionary = data.duplicate(true)
	var version := int(loaded.get("version", 0))
	if version < TRACKER_VERSION:
		loaded = _migrate(loaded, version)
	loaded["version"] = TRACKER_VERSION
	# Fill anything a partial file is missing rather than letting a null reach the arithmetic.
	var fresh := new_tracker(int(loaded.get("wisdom", 10)), {
		"enabled": bool(loaded.get("enabled", default_enabled())),
		"level": int(loaded.get("level", 1)),
	})
	for key in fresh:
		if not loaded.has(key):
			loaded[key] = fresh[key]
	loaded["stress"] = maxi(0, int(loaded.get("stress", 0)))
	loaded["hardening_count"] = maxi(0, int(loaded.get("hardening_count", 0)))
	loaded["checks_made"] = maxi(0, int(loaded.get("checks_made", 0)))
	return loaded


static func _migrate(data: Dictionary, from_version: int) -> Dictionary:
	## v0 -> v1: the first shipped shape had no addiction submodule and no per-day recovery log.
	if from_version < 1:
		if not data.has("addiction"):
			data["addiction"] = {"enabled": false, "addictions": [], "system_strain": 0,
				"missed_today": false, "months_clean": 0, "weeks_clean": 0}
		if not data.has("recovered_today"):
			data["recovered_today"] = {}
		if not data.has("day"):
			data["day"] = 1
	return data


# --------------------------------------------------------------------------- #
# Audit
# --------------------------------------------------------------------------- #


static func audit(tracker: Dictionary) -> Array:
	return Array(tracker.get("audit", [])).duplicate()


## The causes recorded in the scene that has not closed yet — what the screen shows as "why".
static func latest_causes(tracker: Dictionary) -> Array:
	return Array(Dictionary(tracker.get("scene", {})).get("causes", [])).duplicate()


static func _audit(tracker: Dictionary, kind: String, detail: Dictionary) -> void:
	var log: Array = Array(tracker.get("audit", []))
	log.append(_entry(tracker, kind, detail))
	while log.size() > AUDIT_LIMIT:
		log.pop_front()
	tracker["audit"] = log


static func _entry(tracker: Dictionary, kind: String, detail: Dictionary) -> Dictionary:
	var seq := int(tracker.get("seq", 0)) + 1
	tracker["seq"] = seq
	var entry: Dictionary = {"seq": seq, "kind": kind, "day": int(tracker.get("day", 1))}
	for key in detail:
		entry[key] = detail[key]
	return entry


# --------------------------------------------------------------------------- #
# Internals
# --------------------------------------------------------------------------- #


static func _empty_scene() -> Dictionary:
	return {"raw": 0, "causes": []}


static func _resistance(tracker: Dictionary) -> int:
	return hardening_count(tracker) * int(Dictionary(contract().get("hardening", {})).get("scene_resistance", 1))


## Hardening resistance, except where a scar says it does not apply.
static func _resistance_for_scene(tracker: Dictionary, scene: Dictionary) -> int:
	var resistance := _resistance(tracker)
	if not has_scar(tracker, "dependent"):
		return resistance
	var exempt := 0
	for cause in Array(scene.get("causes", [])):
		var row: Dictionary = cause
		if String(row.get("event", "")) == "friend_mortal_wound":
			exempt += int(row.get("raw", 0))
	return maxi(0, resistance - exempt)


static func _projected_gain(tracker: Dictionary) -> int:
	var scene: Dictionary = tracker.get("scene", _empty_scene())
	var raw := int(scene.get("raw", 0))
	return raw - mini(raw, _resistance_for_scene(tracker, scene))


static func _arm_check(tracker: Dictionary) -> Dictionary:
	var penalty := next_penalty(tracker)
	tracker["pending_save"] = {"required": true, "kind": "mental", "penalty": penalty}
	_audit(tracker, "check_owed", {"penalty": penalty, "checks_made": int(tracker.get("checks_made", 0))})
	return pending_save(tracker)


static func _addiction_count(tracker: Dictionary) -> int:
	var addiction: Dictionary = Dictionary(tracker.get("addiction", {}))
	if not bool(addiction.get("enabled", false)):
		return 0
	return Array(addiction.get("addictions", [])).size()


static func _available_scars(tracker: Dictionary) -> Array:
	var rows: Array = []
	for id in scar_ids():
		if not has_scar(tracker, String(id)):
			rows.append(String(id))
	return rows


## Resolve a contract value that may be a plain number or a dice expression. The module never rolls:
## a dice value must arrive in `options.rolls` (keyed by the entry id) or as `options.value`.
static func _amount(value: Variant, options: Dictionary, key: String) -> Dictionary:
	if value is int or value is float:
		return {"ok": true, "value": int(value)}
	var text := String(value)
	if text.is_empty():
		return {"ok": true, "value": 0}
	var sign := 1
	var body := text
	if body.begins_with("-"):
		sign = -1
		body = body.substr(1)
	var rolls: Dictionary = Dictionary(options.get("rolls", {}))
	if rolls.has(key):
		return {"ok": true, "value": sign * int(rolls[key])}
	if options.has("value"):
		return {"ok": true, "value": sign * int(options["value"])}
	return {"ok": false, "reason": "a roll is required for %s (%s): this module does not roll dice" % [key, text]}


## A ranged entry ("one to three") takes the value the table picked, clamped into the printed range;
## a fixed entry uses its own number.
static func _base_amount(row: Dictionary, options: Dictionary, key: String) -> Dictionary:
	var band: Variant = row.get("stress_range")
	if band is Array and Array(band).size() == 2 and options.has("value"):
		var low := int(Array(band)[0])
		var high := int(Array(band)[1])
		return {"ok": true, "value": clampi(int(options["value"]), low, high)}
	return _amount(row.get("stress", 0), options, key)


static func _find(rows: Variant, id: String) -> Dictionary:
	for row in Array(rows):
		var entry: Dictionary = row
		if String(entry.get("id", "")) == id:
			return entry
	return {}


static func _ids(rows: Variant) -> Array:
	var ids: Array = []
	for row in Array(rows):
		ids.append(String(Dictionary(row).get("id", "")))
	return ids
