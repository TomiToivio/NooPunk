class_name CWNInjury
extends RefCounted

## Major Injuries and the zero-hit-point procedure.
##
## Ported from `src/rules/cwn_major_injury.py` and `src/rules/cwn_injury_procedure.py`.
##
## The sequence is the part a runtime cannot guess, and the part three modules previously each half
## owned: reaching zero hit points is **not automatically** a Major Injury. The risk predicate tests
## three conditions — lethal damage, zero hit points, and a Traumatic Hit in the same scene. Drop to
## zero from an ordinary beating and you are unconscious; drop to zero in a fight where trauma
## landed and you owe a Physical save, and failing it sends you to the d12 table.
##
## A passed save does not undo the wound: the character is still Mortally Wounded and still needs
## stabilising. It only keeps them off the table.

const MIN_ROLL := 1
const MAX_ROLL := 12
const HOURS_TO_DEATH_WITHOUT_CARE := 1

## The twelve outcomes. Rows 11 and 12 share one result in the SRD.
const MAJOR_INJURY_TABLE := {
	1: {"id": "instant_death", "label": "Instant Death", "lethal": true,
		"summary": "Dead; no recovery."},
	2: {"id": "internal_damage", "label": "Internal Damage", "coma_until_prosthetic": true,
		"dies_within_hours": 1, "requires_prosthetic": true,
		"damaged_cyber_locations": ["Body", "Nerves"],
		"summary": "Coma until Prosthetic Cyber; dead in an hour without a street doc."},
	3: {"id": "brain_damage", "label": "Brain Damage", "coma_until_prosthetic": true,
		"requires_prosthetic": true, "damaged_cyber_locations": ["Head", "Nerves"],
		"summary": "Coma until a Prosthetic Cyber is installed."},
	4: {"id": "eye_damage", "label": "Eye Damage", "blinded_until_cybereyes": true,
		"requires_prosthetic": true,
		"summary": "Blind until cybereyes; existing cybereyes and their implants are destroyed."},
	5: {"id": "gut_wound", "label": "Gut Wound", "dies_within_hours": 1,
		"requires_prosthetic": true,
		"summary": "-1 to the Constitution modifier until Prosthetic Cyber; dead in an hour without care."},
	6: {"id": "right_leg_ruined", "label": "Right Leg Ruined", "ruined_limb": "right leg",
		"requires_prosthetic": true, "damaged_cyber_locations": ["right leg"],
		"summary": "Can crawl at best once stabilised."},
	7: {"id": "left_leg_ruined", "label": "Left Leg Ruined", "ruined_limb": "left leg",
		"requires_prosthetic": true, "damaged_cyber_locations": ["left leg"],
		"summary": "Can crawl at best once stabilised."},
	8: {"id": "right_arm_ruined", "label": "Right Arm Ruined", "ruined_limb": "right arm",
		"requires_prosthetic": true, "damaged_cyber_locations": ["right arm"],
		"summary": "One functional hand only."},
	9: {"id": "left_arm_ruined", "label": "Left Arm Ruined", "ruined_limb": "left arm",
		"requires_prosthetic": true, "damaged_cyber_locations": ["left arm"],
		"summary": "One functional hand only."},
	10: {"id": "system_damage", "label": "System Damage",
		"damaged_most_expensive_implant": true,
		"summary": "The most System Strain-expensive implant is critically damaged."},
	11: {"id": "flesh_wound", "label": "Just a Flesh Wound", "flesh_wound": true,
		"summary": "Not as bad as it looked."},
	12: {"id": "flesh_wound", "label": "Just a Flesh Wound", "flesh_wound": true,
		"summary": "Not as bad as it looked."},
}

## A roll below 1 counts as 1 and above 12 as 12, per the SRD.
static func clamp_roll(roll: int) -> int:
	return clampi(roll, MIN_ROLL, MAX_ROLL)

static func injury_for_roll(roll: int) -> Dictionary:
	return MAJOR_INJURY_TABLE[clamp_roll(roll)]

static func resolve_major_injury(roll: int, modifier: int = 0) -> Dictionary:
	return injury_for_roll(roll + modifier)

static func is_lethal(injury: Dictionary) -> bool:
	return bool(injury.get("lethal", false))

static func requires_prosthetic(injury: Dictionary) -> bool:
	return bool(injury.get("requires_prosthetic", false))

static func damaged_cyber_locations(injury: Dictionary) -> Array:
	return injury.get("damaged_cyber_locations", [])

## Hours to death without a street doc, or -1 when the injury does not have that clock.
static func dies_without_care_within(injury: Dictionary) -> int:
	return int(injury.get("dies_within_hours", -1))

## Stabilisation is not enough to restore the character for these outcomes.
static func is_permanent_without_treatment(injury: Dictionary) -> bool:
	return (is_lethal(injury)
		or bool(injury.get("coma_until_prosthetic", false))
		or bool(injury.get("blinded_until_cybereyes", false))
		or injury.has("ruined_limb")
		or bool(injury.get("damaged_most_expensive_implant", false)))

## The risk predicate: all three conditions, not the weaker two-condition version.
static func major_injury_risk(hit_points_after: int, traumatic_in_fight: bool,
		lethal: bool = true) -> bool:
	return lethal and hit_points_after <= 0 and traumatic_in_fight

## A d20 save: meet the target, natural 1 always fails, natural 20 always succeeds.
static func save_succeeds(d20: int, target: int) -> bool:
	assert(d20 >= 1 and d20 <= 20, "saves are rolled on a d20")
	if d20 == 1:
		return false
	if d20 == 20:
		return true
	return d20 >= target

## The zero-hit-point procedure. Dice are explicit arguments; each is required only on the branch
## that uses it, so a knockout never consults a table it did not reach.
##
## Returns {mortally_wounded, risked_major_injury, save: {...} or {}, injury: {...} or {}}.
static func resolve_zero_hit_points(params: Dictionary) -> Dictionary:
	var hit_points_after: int = int(params.get("hit_points_after", 1))
	var traumatic: bool = bool(params.get("traumatic_in_fight", false))
	var lethal: bool = bool(params.get("lethal", true))
	var level: int = int(params.get("level", 1))
	var modifiers: Dictionary = params.get("modifiers", {})

	if hit_points_after > 0:
		return {"mortally_wounded": false, "risked_major_injury": false, "save": {}, "injury": {}}

	if not major_injury_risk(hit_points_after, traumatic, lethal):
		return {"mortally_wounded": true, "risked_major_injury": false, "save": {}, "injury": {}}

	var target := CWNCharacter.save_target("physical", level, modifiers)
	var die: int = int(params.get("save_die", 0))
	assert(die >= 1 and die <= 20, "a risked Major Injury needs its Physical save roll")
	var passed := save_succeeds(die, target)
	var save := {"die": die, "target": target, "success": passed}
	if passed:
		return {"mortally_wounded": true, "risked_major_injury": true, "save": save, "injury": {}}

	var roll: int = int(params.get("injury_roll", 0))
	assert(roll >= 1, "a failed save needs its d12 Major Injury roll")
	var injury := resolve_major_injury(roll, int(params.get("injury_modifier", 0)))
	return {"mortally_wounded": true, "risked_major_injury": true, "save": save, "injury": injury}
