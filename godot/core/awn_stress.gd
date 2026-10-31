## Optional AWN Stress module (#928). CWN remains the kernel.
## Source: Ashes Without Number Deluxe, printed pp. 56-58. Original implementation, not book text.
extends RefCounted
class_name AwnStress

const BREAKDOWNS := ["deathwish", "withdrawal", "indulgence", "cowardice", "confusion"]
const SCARS := ["self_destructive", "addicted", "self_doubting", "loner", "nightmares", "delusional", "bloodthirsty", "penitent", "dependent"]
const TRIGGERS := {
	"kill": 2, "multiple_kills": 1, "unthreatening_victim": 2,
	"helpless_victim": 2, "friend_mortally_wounded": 1,
	"friend_dies": 2, "self_mortally_wounded": 2,
	"major_injury": 2, "theft": 1, "fatal_theft": 1,
	"atrocity_witness": 1, "privation_week": 2
}
## NoöPunk additions, not AWN canonical triggers.
const NOOPUNK_TRIGGERS := {
	"nhi_disclosure": 1, "ontological_shock": 2,
	"psi_intrusion": 2, "rogue_agi_atrocity": 2,
	"unsa_moral_injury": 2
}

var enabled := false
var stress := 0
var hardening_count := 0
var scars: Array = []
var breakdown := ""
var failed_check_count := 0
var pending_breakdown := false
var pending_events: Array = []
var log: Array = []
var addiction_enabled := false
var addictions: Array = []

func _init(active: bool = false) -> void:
	enabled = active

func queue_event(id: String, extra: int = 0, custom_points: int = -1) -> bool:
	if not enabled or (not TRIGGERS.has(id) and not NOOPUNK_TRIGGERS.has(id) and custom_points < 0):
		return false
	var base: int = int(TRIGGERS.get(id, NOOPUNK_TRIGGERS.get(id, 0)))
	pending_events.append({"id": id, "points": maxi(0, custom_points if custom_points >= 0 else base + extra)})
	return true

## Call once at scene end. Save roll is the actual d20 and target is the CWN Mental save target.
## Returns need_choice after a failed save: UI/player must select a Breakdown or Hardening.
func end_scene(wisdom: int, mental_target: int, save_roll: int = 0) -> Dictionary:
	if not enabled:
		return {"status": "disabled"}
	var raw := 0
	for event in pending_events:
		raw += int(event.get("points", 0))
	pending_events.clear()
	if breakdown != "":
		return {"status": "breakdown_active", "stress": stress}
	var reduction := hardening_count + (addictions.size() if addiction_enabled else 0)
	var gain := maxi(0, raw - reduction)
	stress += gain
	log.append({"event": "scene_stress", "raw": raw, "gain": gain})
	if pending_breakdown:
		return {"status": "choice_pending", "stress": stress}
	if gain == 0 or stress <= wisdom:
		if stress <= wisdom:
			failed_check_count = 0
		return {"status": "stable", "stress": stress}
	var penalty := -2 * (failed_check_count + 1)
	failed_check_count += 1
	if save_roll < 1 or save_roll > 20:
		failed_check_count -= 1
		return {"status": "save_required", "penalty": penalty, "stress": stress}
	var passed := save_roll + penalty >= mental_target
	if passed:
		return {"status": "saved", "penalty": penalty, "stress": stress}
	pending_breakdown = true
	return {"status": "need_choice", "penalty": penalty, "stress": stress}

func choose_breakdown(id: String) -> bool:
	if not pending_breakdown or not BREAKDOWNS.has(id):
		return false
	breakdown = id
	pending_breakdown = false
	log.append({"event": "breakdown", "id": id})
	return true

func harden(scar: String) -> bool:
	if not pending_breakdown or not SCARS.has(scar) or scars.has(scar):
		return false
	hardening_count += 1
	scars.append(scar)
	stress = 0
	failed_check_count = 0
	pending_breakdown = false
	breakdown = ""
	log.append({"event": "harden", "scar": scar})
	return true

func recover(amount: int, wisdom: int, source: String = "") -> int:
	if not enabled or amount <= 0:
		return 0
	var removed := mini(stress, amount)
	stress -= removed
	if stress <= wisdom:
		breakdown = ""
		failed_check_count = 0
	log.append({"event": "recovery", "source": source, "removed": removed})
	return removed

func restful_day(wisdom: int, safe_and_comfortable: bool) -> int:
	return recover(1, wisdom, "safe_rest") if safe_and_comfortable else 0

## Indulgence trades one System Strain for one Stress, not both benefits.
func indulgence(wisdom: int, strain: Dictionary) -> bool:
	if not enabled:
		return false
	var used := float(strain.get("used", 0))
	if used + 1.0 > float(strain.get("max", 0)):
		return false
	strain["used"] = used + 1.0
	recover(1, wisdom, "indulgence")
	return true

## AWN Cha/Wis + Heal/Lead check, difficulty 9, once daily.
func talk(wisdom: int, roll_total: int, helper: AwnStress) -> bool:
	if not enabled or helper == null or scars.has("loner"):
		return false
	if roll_total >= 9:
		recover(1, wisdom, "supportive_talk")
		return true
	helper.stress += 1
	helper.log.append({"event": "supportive_talk_failed"})
	return false

func goal(wisdom: int, d10: int) -> int:
	return recover(clampi(d10, 1, 10), wisdom, "major_goal")

## Structured rules data for UI and downstream combat/check adapters.
func effects(level: int) -> Dictionary:
	var out := {"skill_penalty": 0, "save_penalty": 0, "max_hp_delta": 0,
		"con_modifier_delta": 0, "wisdom_delta": 0, "charisma_delta": 0,
		"cannot_lead": false, "cannot_social_recover": false,
		"cannot_kill": false, "combat_restricted": false,
		"must_be_prompted": false, "natural_12_auto_fail": false,
		"recovery_coin_flip": false}
	match breakdown:
		"deathwish": out["max_hp_delta"] -= 2 * level
		"withdrawal", "cowardice": out["combat_restricted"] = true
		"indulgence": out["skill_penalty"] -= 2
		"confusion": out["must_be_prompted"] = true
	if scars.has("self_destructive"):
		out["max_hp_delta"] -= 2 * level
	if scars.has("self_doubting"):
		out["natural_12_auto_fail"] = true
	if scars.has("loner"):
		out["cannot_lead"] = true
		out["cannot_social_recover"] = true
	if scars.has("nightmares"):
		out["con_modifier_delta"] -= 1
		out["save_penalty"] -= 2
	if scars.has("delusional"):
		out["wisdom_delta"] -= 3
	if scars.has("dependent"):
		out["charisma_delta"] -= 3
	if scars.has("penitent"):
		out["cannot_kill"] = true
	if scars.has("bloodthirsty"):
		out["recovery_coin_flip"] = true
	return out

func snapshot() -> Dictionary:
	return {"enabled": enabled, "stress": stress, "hardening_count": hardening_count,
		"scars": scars.duplicate(), "breakdown": breakdown, "failed_check_count": failed_check_count,
		"pending_breakdown": pending_breakdown, "pending_events": pending_events.duplicate(true),
		"log": log.duplicate(true), "addiction_enabled": addiction_enabled,
		"addictions": addictions.duplicate()}

func restore(data: Dictionary) -> void:
	enabled = bool(data.get("enabled", false))
	stress = maxi(0, int(data.get("stress", 0)))
	scars = (data.get("scars", []) as Array).duplicate()
	hardening_count = maxi(0, int(data.get("hardening_count", scars.size())))
	breakdown = str(data.get("breakdown", ""))
	failed_check_count = maxi(0, int(data.get("failed_check_count", 0)))
	pending_breakdown = bool(data.get("pending_breakdown", false))
	pending_events = (data.get("pending_events", []) as Array).duplicate(true)
	log = (data.get("log", []) as Array).duplicate(true)
	addiction_enabled = bool(data.get("addiction_enabled", false))
	addictions = (data.get("addictions", []) as Array).duplicate()
