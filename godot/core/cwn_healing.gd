## Cities Without Number: injury, stabilization, natural healing and Frailty.
##
## Port of `src/rules/cwn_healing.py`. The book's sequence, in its own order:
##
## * A mortally wounded character dies at the end of the **sixth round** unless stabilized.
## * Stabilizing is a **Heal** check at difficulty **8 plus each full round since downing**, two
##   harder without a medkit.
## * A stabilized patient wakes with **one hit point** after ten minutes — and is **Frail**.
## * Frailty is the cost of surviving: no natural healing, and death outright at zero HP until a
##   week of bed rest has passed. With Heal-0 care and a medkit it ends; without care a Physical
##   save decides between another month and dying.
## * A night's rest restores HP equal to level or hit dice — never to the Frail.
extends RefCounted
class_name CwnHealing

const MORTAL_WOUND_ROUNDS := 6
const STABILIZE_BASE_DIFFICULTY := 8
const NO_MEDKIT_PENALTY := 2
const STABILIZED_REST_MINUTES := 10
const FRAIL_BED_REST_WEEK := 7

## Difficulty 8 plus each full round elapsed, two harder without a medkit.
static func stabilize_difficulty(rounds_since_downed: int, has_medkit: bool = true) -> Dictionary:
	if rounds_since_downed < 0:
		return {"ok": false, "reason": "rounds_since_downed_cannot_be_negative"}
	var difficulty := STABILIZE_BASE_DIFFICULTY + rounds_since_downed
	if not has_medkit:
		difficulty += NO_MEDKIT_PENALTY
	return {"ok": true, "difficulty": difficulty}

## Past this round the patient is dead, whatever the dice say.
static func mortal_wound_expired(rounds_since_downed: int) -> bool:
	return rounds_since_downed >= MORTAL_WOUND_ROUNDS

## A stabilized patient: one hit point, Frail, and no longer on the clock.
static func stabilize(patient: Dictionary) -> Dictionary:
	if not bool(patient.get("mortally_wounded", false)):
		return {"ok": false, "reason": "only_a_mortally_wounded_patient_needs_stabilizing"}
	var out := patient.duplicate(true)
	out["hit_points"] = 1
	out["frail"] = true
	out["mortally_wounded"] = false
	out["stabilized_rest_minutes"] = STABILIZED_REST_MINUTES
	return {"ok": true, "patient": out}

## A night's rest restores level-or-hit-dice HP — but never to the Frail.
static func natural_healing(level_or_hit_dice: int, frail: bool) -> int:
	if frail:
		return 0
	return maxi(0, level_or_hit_dice)

## The week of bed rest that decides whether frailty ends or kills.
static func frail_week(has_medic_care: bool, physical_save_success: Variant = null) -> Dictionary:
	if has_medic_care:
		return {"ok": true, "outcome": "recovered"}
	if physical_save_success == null:
		return {"ok": false, "reason": "without_care_the_week_needs_its_physical_save"}
	return {"ok": true, "outcome": "month_more" if bool(physical_save_success) else "dying"}
