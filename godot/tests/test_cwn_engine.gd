extends RefCounted

## Behavioural checks for the canonical CWN engine (#791: the compatibility tree is gone, so these
## now pin `godot/core/` — the single implementation).
const Catalogue := preload("res://godot/core/cwn_catalogue.gd")
const Character := preload("res://godot/core/cwn_character.gd")
const Combat := preload("res://godot/core/cwn_combat_rules.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	# --- catalogue: the SRD-extracted data, not a recollection ---
	rows.append(_eq("SRD licence recorded", Catalogue.srd_licence(), "CC0 (verified-public-domain)"))
	rows.append(_eq("twelve firearms extracted", Catalogue.srd_rows("firearms").size(), 12))
	var rifle: Dictionary = Catalogue.srd_weapon("Rifle")
	rows.append(_eq("rifle damage parsed", rifle.get("damage"), {"count": 1, "sides": 10, "bonus": 2}))
	rows.append(_eq("rifle trauma rating", rifle.get("trauma_rating"), 3))
	rows.append(_eq("rifle cost", rifle.get("cost"), 1000))
	rows.append(["melee weapon resolves", not Catalogue.srd_weapon("Knife", ["melee"]).is_empty(), ""])
	var leathers: Dictionary = Catalogue.srd_armour("Street Leathers")
	rows.append(_eq("armour soak", leathers.get("soak"), 3))
	rows.append(_eq("armour ranged AC", leathers.get("ranged_ac"), 13))
	rows.append(_eq("twenty backgrounds", Catalogue.srd_background_names().size(), 20))
	rows.append(_eq("background free skill",
		Catalogue.srd_background("Bum").get("free_skill"), "Survive-0"))

	# --- character creation ---
	var rolled: Dictionary = Character.from_rolls([3, 7, 10, 13, 17, 18])
	rows.append(_eq("modifier floor at score 3", rolled["modifiers"]["STR"], -2))
	rows.append(_eq("modifier at 18", rolled["modifiers"]["CHA"], 2))
	var substituted: Dictionary = Character.from_rolls([3, 7, 10, 13, 17, 18], 0)
	rows.append(_eq("14 substituted for one score", substituted["attributes"]["STR"], 14))
	rows.append(_eq("substitution recorded", substituted["substituted"], true))
	var arrayed: Dictionary = Character.from_array([14, 12, 11, 10, 9, 7])
	rows.append(_eq("array assigns in order", arrayed["attributes"]["STR"], 14))
	rows.append(_eq("array is a spent option", arrayed["substituted"], true))

	rows.append(_eq("first creation pick is rank 0", Character.creation_skill_pick(-1)["rank"], 0))
	rows.append(_eq("second pick reaches rank 1", Character.creation_skill_pick(0)["rank"], 1))
	rows.append(_eq("third pick refused", Character.creation_skill_pick(1)["allowed"], false))

	rows.append(_eq("hit points floor at one", Character.max_hit_points(1, -2), 1))
	rows.append(_eq("hard to kill adds two", Character.max_hit_points(1, 0, true), 3))
	# The defect the merge fixed: a new character rolls 1d6, so a roll of 1 with no Con modifier is
	# 1 hit point, not the 6 that a fixed allowance would hand out.
	rows.append(_eq("a 1d6 roll of 1 stays 1", Character.max_hit_points(1, 0), 1))
	rows.append(_eq("a 1d6 roll of 6 gives 6", Character.max_hit_points(6, 0), 6))

	var mods := {"STR": 1, "DEX": 2, "CON": -1, "INT": 0, "WIS": 1, "CHA": -2}
	rows.append(_eq("physical save at level 1", Character.save_target("physical", 1, mods), 14))
	rows.append(_eq("evasion save at level 1", Character.save_target("evasion", 1, mods), 13))
	rows.append(_eq("mental save at level 1", Character.save_target("mental", 1, mods), 14))
	rows.append(_eq("luck save ignores attributes", Character.save_target("luck", 1, mods), 15))
	rows.append(_eq("saves improve with level", Character.save_target("evasion", 3, mods), 11))
	rows.append(_eq("NPC save from hit dice", Character.npc_save_target(3), 14))
	rows.append(_eq("languages from Know and Connect", Character.extra_languages(1, 0), 3))

	# The modifier-based target must agree with the score-based `saves()` or the two drift.
	var scores := {"STR": 12, "DEX": 15, "CON": 9, "INT": 11, "WIS": 13, "CHA": 8}
	var from_scores: Dictionary = Character.saves(1, scores)
	rows.append(_eq("save_target agrees with saves() : Physical",
		Character.save_target("physical", 1, rolled_modifiers(scores)), int(from_scores["Physical"])))

	# --- combat ---
	# resolve_attack is the canonical entry point: it computes the Shock the miss would have dealt,
	# then uses it as the floor on the hit branch.
	var miss: Dictionary = Combat.resolve_attack(false, 0, -1, 1, 6, 2, 15, 13, 1)
	rows.append(_eq("a miss deals its shock", int(miss["damage"]), 3))
	rows.append(_eq("a miss is not traumatic", miss["trauma"], false))

	var traumatic_hit: Dictionary = Combat.resolve_attack(true, 7, 6, 3, 6, 2, 15, 13, 1)
	rows.append(_eq("trauma triples the hit", int(traumatic_hit["damage"]), 21))
	rows.append(_eq("trauma flagged", traumatic_hit["trauma"], true))

	var floored: Dictionary = Combat.resolve_attack(true, 1, -1, 1, 6, 2, 15, 13, 1)
	rows.append(_eq("a weak hit is floored at its shock", int(floored["damage"]), 3))

	# Shock: value 2 against AC 15 or less, +1 attribute modifier.
	rows.append(_eq("shock on a miss within AC",
		Combat.shock_damage(false, 2, 15, 13, 1), 3))
	rows.append(_eq("shock stops above its AC",
		Combat.shock_damage(false, 2, 15, 16, 1), 0))
	rows.append(_eq("shock does not apply on a hit",
		Combat.shock_damage(true, 2, 15, 13, 1), 0))
	rows.append(_eq("hit damage floored by shock", Combat.damage_floor(1, 3), 3))
	rows.append(_eq("hit damage above the floor stands", Combat.damage_floor(9, 3), 9))

	rows.append(_eq("trauma at or above target", Combat.is_traumatic_hit(6, 6), true))
	rows.append(_eq("trauma below target", Combat.is_traumatic_hit(5, 6), false))
	rows.append(_eq("trauma multiplies the whole hit", Combat.trauma_damage(6, 3, true), 18))
	rows.append(_eq("a miss is never traumatic", Combat.is_traumatic_hit(12, 6) and not Combat.is_traumatic_hit(9, 20), true))

	return rows

func rolled_modifiers(scores: Dictionary) -> Dictionary:
	var out := {}
	for key in scores.keys():
		out[key] = CWNRules.ability_modifier(int(scores[key]))
	return out
