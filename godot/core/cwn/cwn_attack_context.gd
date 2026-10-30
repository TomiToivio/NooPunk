class_name CWNAttackContext
extends RefCounted

## CWN SRD: Rules of the Game > Combat > Attacks in Combat.
## Computes published situational modifiers and eligibility for an ordinary attack.
## The attacker chooses the relevant weapon attribute; CWNRules evaluates the d20.
## Callers must validate weapon-specific restrictions, ammunition and targets.

static func assess(context: Dictionary) -> Dictionary:
	var mode := str(context.get("mode", "ranged"))
	if not ["ranged", "melee", "thrown"].has(mode):
		return {"allowed": false, "reason": "invalid mode"}
	var adjacent := bool(context.get("adjacent", false))
	var target_prone := bool(context.get("target_prone", false))
	var attacker_prone := bool(context.get("attacker_prone", false))
	var visible := bool(context.get("visible", true))
	var position_known := bool(context.get("position_known", true))
	var cover := str(context.get("cover", "none"))
	var long_range := bool(context.get("long_range", false))
	var one_handed := bool(context.get("one_handed", false))
	var gunlink := bool(context.get("gunlink", false))
	var gun_in_melee := bool(context.get("gun_in_melee", false))
	if not ["none", "half", "almost_complete"].has(cover):
		return {"allowed": false, "reason": "invalid cover"}
	if not visible and not position_known:
		return {"allowed": false, "reason": "target location unknown"}
	if mode == "ranged" and gun_in_melee and not one_handed:
		return {"allowed": false, "reason": "two-handed gun in melee"}
	var modifier := 0
	var breakdown: Dictionary = {}
	if target_prone:
		var prone_mod := 2 if adjacent else -2
		modifier += prone_mod
		breakdown["target_prone"] = prone_mod
	if attacker_prone and mode == "melee":
		modifier -= 4
		breakdown["attacker_prone"] = -4
	if long_range and mode == "ranged" and not gunlink:
		modifier -= 2
		breakdown["long_range"] = -2
	var cover_penalty := {"none": 0, "half": -2, "almost_complete": -4}[cover] as int
	if gunlink and mode == "ranged":
		cover_penalty = mini(0, cover_penalty + 2)
	if cover_penalty != 0:
		modifier += cover_penalty
		breakdown["cover"] = cover_penalty
	if mode == "thrown" and adjacent:
		modifier -= 4
		breakdown["thrown_in_melee"] = -4
	if mode == "ranged" and gun_in_melee and one_handed:
		modifier -= 4
		breakdown["one_handed_gun_in_melee"] = -4
	if not visible:
		modifier -= 4
		breakdown["unseen_target"] = -4
	return {"allowed": true, "modifier": modifier, "breakdown": breakdown}

static func evaluate(die: int, base_attack: int, attribute_bonus: int, skill_rank: int,
		armor_class: int, context: Dictionary) -> Dictionary:
	var situation := assess(context)
	if not situation.get("allowed", false):
		return situation
	if die < 1 or die > 20 or skill_rank < -2 or skill_rank > 4 or armor_class < 0:
		return {"allowed": false, "reason": "invalid attack inputs"}
	var result := CWNRules.evaluate_attack(die, base_attack, attribute_bonus,
		skill_rank, armor_class)
	result["total"] = int(result["total"]) + int(situation["modifier"])
	result["hit"] = int(result["total"]) >= armor_class
	result["allowed"] = true
	result["modifier"] = situation["modifier"]
	result["breakdown"] = situation["breakdown"]
	return result
