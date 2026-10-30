class_name CWNHealing
extends RefCounted

## Mortal wounds, stabilisation, Frail, first aid and natural healing.
##
## Ported from `src/rules/cwn_healing.py`. This layer is about *time and consequence* rather than
## damage: being dropped starts a clock, stabilising stops the clock but costs a week of ability,
## and modern medicine is paid for in System Strain rather than money.

const MORTAL_WOUND_ROUNDS := 6
const STABILIZE_BASE_DIFFICULTY := 8
const NO_MEDKIT_PENALTY := 2
const FRAIL_REMOVAL_DIFFICULTY := 10
const STABILIZED_REST_MINUTES := 10
const FRAIL_BED_REST_WEEK := 7

## Rounds left before the sixth round after downing has passed.
static func rounds_until_death(downed_round: int, current_round: int) -> int:
	assert(current_round >= downed_round, "the current round cannot precede the downing")
	return maxi(0, MORTAL_WOUND_ROUNDS - (current_round - downed_round))

## Difficulty 8, plus one per elapsed round, two harder without a medkit.
static func stabilize_difficulty(rounds_since_downed: int, has_medkit: bool = true) -> int:
	assert(rounds_since_downed >= 0, "rounds since downing cannot be negative")
	return STABILIZE_BASE_DIFFICULTY + rounds_since_downed + (0 if has_medkit else NO_MEDKIT_PENALTY)

## A stabilised patient wakes with one hit point after ten minutes — and is Frail.
## Frailty is the price of surviving: normal activity, no natural healing, and death outright at
## zero until a week of bed rest has passed.
static func stabilize(patient: Dictionary) -> Dictionary:
	assert(int(patient.get("hit_points", 1)) <= 0, "only a mortally wounded patient needs stabilising")
	var next := patient.duplicate(true)
	next["hit_points"] = 1
	next["frail"] = true
	next["downed_round"] = -1
	return next

## One medkit, one hour, one roll — and only one chance per Frailty.
static func remove_frailty(skill_total: int, difficulty: int = FRAIL_REMOVAL_DIFFICULTY,
		already_attempted: bool = false) -> Dictionary:
	if already_attempted:
		return {"allowed": false, "succeeded": false}
	return {"allowed": true, "succeeded": skill_total >= difficulty}

## A night's rest restores level or hit dice in hit points — but never to the Frail.
static func natural_healing(level_or_hit_dice: int, frail: bool) -> int:
	if frail:
		return 0
	return level_or_hit_dice

## The week of bed rest that decides whether frailty ends or kills.
## With Heal-0 care and a medkit it simply ends; without care a Physical save decides:
## failure means death within days, success buys another month.
static func frail_week(has_medic_care: bool, physical_save_success: Variant = null) -> String:
	if has_medic_care:
		return "recovered"
	assert(physical_save_success != null, "without care, the week needs its Physical save")
	return "month_more" if bool(physical_save_success) else "dying"

## Minutes of care: 1d6 plus Heal rank, or 1d6-1 with no Heal skill at all.
## Each application costs one System Strain, and a body at its maximum gains nothing — the
## intervention is simply too much for it.
static func first_aid(die_roll: int, heal_skill: int = 0, has_medkit: bool = true,
		strain = null) -> Dictionary:
	assert(has_medkit, "first aid needs a medkit")
	assert(die_roll >= 1, "a die roll is at least 1")
	assert(heal_skill >= 0, "Heal skill cannot be negative")
	var healed := die_roll + heal_skill if heal_skill > 0 else die_roll - 1
	healed = maxi(0, healed)
	if strain != null and not strain.can_absorb(1.0):
		return {"healed": 0, "strain_added": 0, "refused": true}
	if strain != null:
		strain.absorb(1.0)
	return {"healed": healed, "strain_added": 1 if strain != null else 0, "refused": false}
