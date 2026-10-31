## AWN Stress as an optional CWN overlay (#928).
##
## Every assertion drives the overlay's published behaviour: the ceiling is *exceeded*, not reached; the
## check penalty escalates while the character stays above it and resets when they are back under; a
## Breakdown suppresses further Stress until it ends; Hardening stacks. Dice always arrive from the
## caller, because an overlay does not roll.
extends RefCounted

const Stress := preload("res://mods/noopunk/stress.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _fresh(wisdom: int = 5, extra: Dictionary = {}) -> Dictionary:
	var options: Dictionary = {"enabled": true}
	for key in extra:
		options[key] = extra[key]
	return Stress.new_tracker(wisdom, options)


## A tracker with a Breakdown owed: over the ceiling, checked, and the check failed.
func _owed(wisdom: int = 5, extra: Dictionary = {}) -> Dictionary:
	var tracker := _fresh(wisdom, extra)
	Stress.begin_scene(tracker)
	Stress.award(tracker, "witness_atrocity")
	Stress.end_scene(tracker)
	Stress.resolve_save(tracker, false)
	return tracker


func run() -> Array:
	var rows: Array = []

	# --- the module is optional ---------------------------------------------
	rows.append(_eq("the module is off unless the table enables it", Stress.default_enabled(), false))
	var off := Stress.new_tracker(5)
	rows.append(_eq("a disabled tracker starts disabled", Stress.is_enabled(off), false))
	Stress.award(off, "kill_human")
	rows.append(_eq("a disabled module gains nothing from a scene", Stress.end_scene(off)["enabled"], false))
	rows.append(_eq("a disabled module leaves Stress at zero", Stress.stress(off), 0))
	rows.append(_eq("the flag is a flag, not a rules change", Stress.contract()["module"]["precedence"].length() > 0, true))

	# --- the ceiling is exceeded, never merely reached -----------------------
	var at_ceiling := _fresh(5, {"stress": 4})
	Stress.award(at_ceiling, "witness_atrocity")
	rows.append(_eq("Stress equal to WIS is safe", Stress.end_scene(at_ceiling)["save"]["required"], false))
	rows.append(_eq("equal to the ceiling is not over it", Stress.is_over(at_ceiling), false))

	var over_ceiling := _fresh(5, {"stress": 5})
	Stress.award(over_ceiling, "witness_atrocity")
	rows.append(_eq("one point over WIS asks for a check", Stress.end_scene(over_ceiling)["save"]["required"], true))
	rows.append(_eq("the ceiling is the character's WIS", Stress.threshold(over_ceiling), 5))
	rows.append(_eq("the meter reports how far over it is", Stress.over_by(over_ceiling), 1))

	# --- the first check, and the escalation ---------------------------------
	rows.append(_eq("the first check is at -2", Stress.next_penalty(over_ceiling), -2))
	var failed_penalty: int = int(Stress.pending_save(over_ceiling)["penalty"])
	rows.append(_eq("the pending check carries -2", failed_penalty, -2))
	var held := Stress.resolve_save(over_ceiling, true)
	rows.append(_eq("a successful check holds the line", held["success"], true))
	rows.append(_eq("a successful check does not remove Stress", Stress.stress(over_ceiling), 6))
	rows.append(_eq("the next check escalates to -4", Stress.next_penalty(over_ceiling), -4))
	rows.append(_eq("one check has been made", held["checks_made"], 1))

	Stress.award(over_ceiling, "witness_atrocity")
	Stress.end_scene(over_ceiling)
	rows.append(_eq("a new dose while still over the ceiling asks again",
		Stress.pending_save(over_ceiling)["required"], true))
	rows.append(_eq("the second check is at -4", Stress.pending_save(over_ceiling)["penalty"], -4))
	var broke := Stress.resolve_save(over_ceiling, false)
	rows.append(_eq("a failed check owes a Breakdown", broke["awaiting_breakdown"], true))
	rows.append(_eq("the player may harden instead", broke["can_harden"], true))
	rows.append(_eq("all five Breakdowns are offered", Array(broke["breakdowns"]).size(), 5))

	# --- a scene may carry several causes, and the check is owed once --------
	var multi := _fresh(5)
	var first_kill := Stress.award(multi, "kill_human", {"modifiers": ["first_kill"], "rolls": {"first_kill": 4}})
	rows.append(_eq("a first kill adds the die the caller rolled", first_kill["raw"], 6))
	rows.append(_eq("the scene remembers why", Stress.latest_causes(multi).size(), 1))
	Stress.award(multi, "witness_atrocity")
	var closed := Stress.end_scene(multi)
	rows.append(_eq("causes accumulate within a scene", closed["applied"], 7))
	rows.append(_eq("several causes still owe one check", closed["save"]["required"], true))
	rows.append(_eq("and the check is the first one", int(closed["save"]["penalty"]), -2))

	# --- dice come from the caller ------------------------------------------
	var diced := _fresh(5)
	var no_roll := Stress.award(diced, "kill_human", {"modifiers": ["first_kill"]})
	rows.append(_eq("a diced modifier is refused without a roll", no_roll["ok"], false))
	rows.append(_eq("and it says the module does not roll",
		String(no_roll["reason"]).contains("does not roll dice"), true))
	var with_roll := Stress.award(diced, "kill_human", {"modifiers": ["first_kill"], "rolls": {"first_kill": 6}})
	rows.append(_eq("the same modifier applies when the roll is supplied", with_roll["raw"], 8))
	rows.append(_eq("a modifier that was not selected is ignored",
		Stress.award(_fresh(5), "kill_human", {"modifiers": []})["raw"], 2))

	var cruelty := _fresh(5)
	rows.append(_eq("a ranged entry takes the table's value",
		Stress.award(cruelty, "great_cruelty", {"value": 3})["raw"], 3))
	rows.append(_eq("and is clamped into the printed range",
		Stress.award(_fresh(5), "great_cruelty", {"value": 9})["raw"], 3))

	# --- participation is not presence --------------------------------------
	var witness := _fresh(5)
	rows.append(_eq("a bystander does not gain Stress",
		Stress.award(witness, "kill_human", {"participated": false})["skipped"], "not_a_participant"))
	rows.append(_eq("so nothing is applied at the end of the scene", Stress.end_scene(witness)["applied"], 0))

	# --- Hardening ----------------------------------------------------------
	var hardened := _fresh(5, {"stress": 6})
	Stress.award(hardened, "witness_atrocity")
	Stress.end_scene(hardened)
	Stress.resolve_save(hardened, false)
	var hard = Stress.harden(hardened, "nightmares")
	rows.append(_eq("hardening is accepted", hard["ok"], true))
	rows.append(_eq("hardening clears Stress to zero", Stress.stress(hardened), 0))
	rows.append(_eq("hardening records one scar", Stress.scars(hardened), ["nightmares"]))
	rows.append(_eq("hardening raises the count", Stress.hardening_count(hardened), 1))
	rows.append(_eq("the scar's effects come back as data", hard["effects"]["save_penalty"], -2))
	rows.append(_eq("a scar cannot be taken twice", Stress.harden(hardened, "nightmares")["ok"], false))
	rows.append(_eq("hardening needs a Breakdown to be owed", Stress.harden(hardened, "loner")["ok"], false))

	Stress.begin_scene(hardened)
	Stress.award(hardened, "kill_human")
	rows.append(_eq("hardening resists the first point of a scene", Stress.end_scene(hardened)["applied"], 1))

	# stack it: a second Hardening resists two points
	var twice := _fresh(5, {"stress": 6, "hardening_count": 1, "scars": ["loner"]})
	Stress.begin_scene(twice)
	Stress.award(twice, "kill_human")
	Stress.end_scene(twice)
	rows.append(_eq("one hardening already resists a point", Stress.stress(twice), 7))
	Stress.resolve_save(twice, false)
	var second := Stress.harden(twice, "self_destructive")
	rows.append(_eq("a second hardening is accepted", second["ok"], true))
	rows.append(_eq("a second hardening stacks", Stress.hardening_count(twice), 2))
	Stress.begin_scene(twice)
	Stress.award(twice, "witness_atrocity")
	rows.append(_eq("two hardenings resist two points of a scene", Stress.end_scene(twice)["applied"], 0))
	rows.append(_eq("hardening is irreversible",
		bool(Stress.contract()["hardening"]["irreversible"]), true))

	# --- a Breakdown suppresses further Stress ------------------------------
	var broken := _owed(5, {"stress": 5})
	rows.append(_eq("the player chooses the Breakdown", Stress.choose_breakdown(broken, "withdrawal")["ok"], true))
	rows.append(_eq("the Breakdown is active", Stress.active_breakdown(broken), "withdrawal"))
	rows.append(_eq("its effects are data", Stress.active_conditions(broken)[0]["effects"]["cannot_use_skill_checks"], true))
	rows.append(_eq("a Breakdown gains no further Stress",
		Stress.award(broken, "kill_human")["suppressed"], "breakdown"))
	rows.append(_eq("and the scene applies nothing", Stress.end_scene(broken)["applied"], 0))
	rows.append(_eq("so the meter does not move", Stress.stress(broken), 6))
	rows.append(_eq("an unknown Breakdown is refused", Stress.choose_breakdown(broken, "ennui")["ok"], false))

	# --- recovery, and the threshold it crosses -----------------------------
	var recovering := _owed(5, {"stress": 5})
	Stress.choose_breakdown(recovering, "cowardice")
	var safe_day := Stress.recover(recovering, "safe_day")
	rows.append(_eq("a safe day removes one point", safe_day["recovered"], 1))
	rows.append(_eq("Stress is back at the ceiling", Stress.stress(recovering), 5))
	rows.append(_eq("and the Breakdown ends there", safe_day["breakdown_ended"], true))
	rows.append(_eq("an ended Breakdown is cleared", Stress.active_breakdown(recovering), ""))
	var after_reset := _fresh(5, {"stress": 6})
	Stress.award(after_reset, "witness_atrocity")
	Stress.end_scene(after_reset)
	Stress.resolve_save(after_reset, true)
	Stress.recover(after_reset, "safe_day")
	Stress.new_day(after_reset)
	Stress.recover(after_reset, "safe_day")
	rows.append(_eq("dropping to the ceiling resets the penalty", Stress.next_penalty(after_reset), -2))
	rows.append(_eq("and clears the escalation count", int(after_reset["checks_made"]), 0))

	# recovery limits and costs
	var limited := _fresh(5, {"stress": 8})
	Stress.recover(limited, "talk", {"check_success": true})
	rows.append(_eq("a conversation needs the core's check",
		Stress.recover(limited, "talk", {"check_success": true})["ok"], false))
	var failed_talk := _fresh(5, {"stress": 8})
	var helper := Stress.recover(failed_talk, "talk", {"check_success": false})
	rows.append(_eq("a failed conversation costs the helper a point", helper["helper_stress"], 1))
	rows.append(_eq("and the subject recovers nothing", helper["recovered"], 0))
	rows.append(_eq("a new day re-opens the conversation", Stress.new_day(limited)["day"], 2))
	rows.append(_eq("after a new day it is available again",
		Stress.recover(limited, "talk", {"check_success": true})["ok"], true))

	var indulgence := _fresh(5, {"stress": 8})
	var drink := Stress.recover(indulgence, "indulgence")
	rows.append(_eq("indulgence removes one point", drink["recovered"], 1))
	rows.append(_eq("and costs a point of System Strain", drink["system_strain"], 1))
	rows.append(_eq("System Strain stays the core's number",
		bool(Stress.contract()["recovery"]["events"][1]["cost"]["system_strain"]), true))

	var goal := _fresh(5, {"stress": 8})
	rows.append(_eq("a major goal takes the caller's die",
		Stress.recover(goal, "major_goal", {"rolls": {"major_goal": 7}})["recovered"], 7))
	rows.append(_eq("recovery cannot go below zero",
		Stress.recover(goal, "major_goal", {"rolls": {"major_goal": 10}})["stress"], 0))

	var loner := _fresh(5, {"stress": 8, "scars": ["loner"]})
	rows.append(_eq("the Loner scar forbids the conversation", Stress.can_recover(loner, "talk"), false))
	var flat := Stress.recover(_fresh(5, {"stress": 8, "scars": ["bloodthirsty"]}), "safe_day", {"failed_chance": true})
	rows.append(_eq("the Bloodthirsty scar may void a recovery", flat["failed_chance"], true))

	# --- scars that change the Stress rules themselves ----------------------
	var thirst := _fresh(5, {"scars": ["bloodthirsty"]})
	rows.append(_eq("Bloodthirsty gains nothing from killing",
		Stress.award(thirst, "kill_human")["suppressed"], "bloodthirsty"))
	var dependent := _fresh(5, {"stress": 6, "hardening_count": 1, "scars": ["dependent"]})
	Stress.award(dependent, "friend_mortal_wound")
	rows.append(_eq("Dependent is not resisted by hardening", Stress.end_scene(dependent)["applied"], 1))
	var plain := _fresh(5, {"stress": 6, "hardening_count": 1})
	Stress.award(plain, "friend_mortal_wound")
	rows.append(_eq("another character's hardening does resist it", Stress.end_scene(plain)["applied"], 0))

	# --- addiction is a separate, opt-in submodule --------------------------
	var sober := _fresh(5, {"stress": 6})
	rows.append(_eq("addiction is off by default", Stress.addiction_enabled(sober), false))
	rows.append(_eq("and cannot be indulged", Stress.indulge(sober)["ok"], false))
	rows.append(_eq("nor does the Stress module turn it on", Stress.addiction_enabled(_fresh(5)), false))

	var addicted := _fresh(5, {"stress": 6})
	Stress.enable_addiction(addicted, "alcohol")
	rows.append(_eq("the table can opt in", Stress.addiction_enabled(addicted), true))
	rows.append(_eq("one addiction is recorded", Stress.addictions(addicted), ["alcohol"]))
	Stress.begin_scene(addicted)
	rows.append(_eq("each addiction blunts one incoming point",
		Stress.award(addicted, "kill_human")["blunted"], 1))
	Stress.end_scene(addicted)
	var indulged := Stress.indulge(addicted, {"rolls": {"daily": 3}})
	rows.append(_eq("indulging removes the caller's 1d4", indulged["removed"], 3))
	var missed := Stress.miss_indulgence(addicted)
	rows.append(_eq("a missed day adds a point of Stress", missed["gained"], 1))
	rows.append(_eq("a missed day blocks rest recovery", Stress.rest_recovery_blocked(addicted), true))
	rows.append(_eq("a missed day is privation", missed["privation"], true))
	rows.append(_eq("the monthly check costs System Strain on a failure",
		Stress.monthly_check(addicted, false)["gained_strain"], 1))
	rows.append(_eq("the monthly check is the core's save", Stress.monthly_check(addicted, true)["success"], true))
	rows.append(_eq("a clean week can end it", Stress.break_addiction(addicted, "alcohol", true)["addictions"], []))
	var relapsed := _fresh(5, {"addiction": true})
	Stress.enable_addiction(relapsed, "opium")
	rows.append(_eq("a failed week is a setback", Stress.break_addiction(relapsed, "opium", false)["success"], false))
	rows.append(_eq("the addiction survives the setback", Stress.addictions(relapsed), ["opium"]))

	# --- the NoöPunk triggers are separate, and labelled ---------------------
	rows.append(_eq("the AWN trigger list is the source's", Stress.event_ids().size(), 7))
	rows.append(_eq("the NooPunk triggers are their own list", Stress.noopunk_event_ids().size(), 7))
	rows.append(_eq("an AWN id is not in the NooPunk list",
		Stress.noopunk_event_ids().has("kill_human"), false))
	rows.append(_eq("an NHI trigger is not in the AWN list",
		Stress.event_ids().has("nhi_disclosure_confirmed"), false))
	rows.append(_eq("NooPunk values are marked as ours",
		Stress.noopunk_event("nhi_disclosure_confirmed")["system"], "noopunk"))
	rows.append(_eq("an NHI trigger carries its own rationale",
		String(Stress.noopunk_event("nhi_contact_personal")["rationale"]).length() > 0, true))
	var disclosure := _fresh(5)
	rows.append(_eq("a NooPunk trigger scores through the same meter",
		Stress.award(disclosure, "nhi_disclosure_confirmed")["raw"], 2))
	rows.append(_eq("an unknown trigger is refused", Stress.award(disclosure, "ennui")["ok"], false))

	# --- ontology shock belongs to the Psyche overlay -----------------------
	rows.append(_eq("the boundary names its owner",
		String(Stress.contract()["ontology_shock_boundary"]["owner"]).contains("psyche"), true))
	rows.append(_eq("Stress never scores the anomaly itself",
		String(Stress.contract()["ontology_shock_boundary"]["rule"]).contains("never scores"), true))

	# --- CWN stays the core -------------------------------------------------
	rows.append(_eq("CWN WIS is the ceiling, not a new attribute",
		Stress.contract()["threshold"]["attribute"], "WIS"))
	rows.append(_eq("the save is CWN's Mental save", Stress.contract()["threshold"]["save"], "mental"))
	rows.append(_eq("the caller owns the roll",
		String(Stress.contract()["threshold"]["save_owner"]).contains("CWN core"), true))
	rows.append(_eq("Alienation is a separate track",
		String(Stress.contract()["cwn_compatibility"]["adjacency_note"]).contains("Alienation"), true))
	rows.append(_eq("consent is required before play",
		bool(Stress.contract()["consent_and_tone"]["table_consent_required"]), true))
	rows.append(_eq("the intensity dials are listed",
		Array(Stress.contract()["consent_and_tone"]["intensity_dials"]).size(), 4))

	# --- persistence -------------------------------------------------------
	var saved := _owed(5, {"stress": 6})
	Stress.choose_breakdown(saved, "confusion")
	Stress.enable_addiction(saved, "sedatives")
	var payload := Stress.to_dict(saved)
	rows.append(_eq("the tracker names its own format",
		payload["format"] != "", true))
	var loaded := Stress.from_dict(payload)
	rows.append(_eq("Stress survives a save", Stress.stress(loaded), 7))
	rows.append(_eq("the active Breakdown survives it", Stress.active_breakdown(loaded), "confusion"))
	rows.append(_eq("the addiction survives it", Stress.addictions(loaded), ["sedatives"]))
	var versioned := Stress.from_dict({"format": Stress.TRACKER_FORMAT, "wisdom": 6, "stress": 3})
	rows.append(_eq("an older save is migrated, not refused", Stress.stress(versioned), 3))
	rows.append(_eq("migration adds the addiction submodule", versioned.has("addiction"), true))
	rows.append(_eq("an unrelated save yields a disabled tracker",
		Stress.from_dict({"wisdom": 6})["enabled"], false))
	rows.append(_eq("the audit log records what happened", Stress.audit(saved).size() > 0, true))
	rows.append(_eq("the audit log is bounded", Stress.audit(saved).size() <= Stress.AUDIT_LIMIT, true))

	return rows
