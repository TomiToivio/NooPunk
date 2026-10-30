extends RefCounted

## Behavioural checks for the CWN engine modules (#751 surface: creation, combat, catalogues).
##
## Preloaded rather than referenced by global class name: the class cache only exists after an
## import pass, so a clean checkout cannot resolve `CWNCatalogue` here.
const Catalogue := preload("res://godot/core/cwn/cwn_catalogue.gd")
const Character := preload("res://src/godot/cwn/cwn_character.gd")
const Combat := preload("res://src/godot/cwn/cwn_combat.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	# --- catalogue: the data must exist and must be the SRD's, not a recollection ---
	rows.append(_eq("SRD licence recorded", Catalogue.licence(), "CC0 (verified-public-domain)"))
	rows.append(_eq("twelve firearms extracted", Catalogue.rows("firearms").size(), 12))
	var rifle: Dictionary = Catalogue.weapon("Rifle")
	rows.append(_eq("rifle damage parsed", rifle.get("damage"), {"count": 1, "sides": 10, "bonus": 2}))
	rows.append(_eq("rifle trauma rating", rifle.get("trauma_rating"), 3))
	rows.append(_eq("rifle cost", rifle.get("cost"), 1000))
	var knife: Dictionary = Catalogue.weapon("Knife", ["melee"])
	rows.append(["melee weapon resolves", not knife.is_empty(), ""])
	var leathers: Dictionary = Catalogue.armour("Street Leathers")
	rows.append(_eq("armour soak", leathers.get("soak"), 3))
	rows.append(_eq("armour ranged AC", leathers.get("ranged_ac"), 13))
	rows.append(_eq("twenty backgrounds", Catalogue.background_names().size(), 20))
	rows.append(_eq("background free skill", Catalogue.background("Bum").get("free_skill"), "Survive-0"))

	# --- character creation ---
	var rolled: Dictionary = Character.from_rolls([3, 7, 10, 13, 17, 18])
	rows.append(_eq("modifier floor at score 3", rolled["modifiers"]["STR"], -2))
	rows.append(_eq("modifier at 18", rolled["modifiers"]["CHA"], 2))
	rows.append(_eq("no substitution leaves scores alone", rolled["attributes"]["STR"], 3))
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
	var mods := {"STR": 1, "DEX": 2, "CON": -1, "INT": 0, "WIS": 1, "CHA": -2}
	rows.append(_eq("physical save at level 1", Character.save_target("physical", 1, mods), 14))
	rows.append(_eq("evasion save at level 1", Character.save_target("evasion", 1, mods), 13))
	rows.append(_eq("mental save at level 1", Character.save_target("mental", 1, mods), 14))
	rows.append(_eq("luck save ignores attributes", Character.save_target("luck", 1, mods), 15))
	rows.append(_eq("saves improve with level", Character.save_target("evasion", 3, mods), 11))
	rows.append(_eq("NPC save from hit dice", Character.npc_save_target(3), 14))
	rows.append(_eq("languages from Know and Connect", Character.extra_languages(1, 0), 3))

	# --- combat ---
	var tie: Dictionary = Combat.initiative(5, 1, 4, 2)
	rows.append(_eq("PCs win initiative ties", tie["winner"], "pc"))
	rows.append(_eq("NPC wins on a higher total", Combat.initiative(2, 0, 8, 0)["winner"], "npc"))

	var hit: Dictionary = Combat.attack(12, 0, 1, 1, 13)
	rows.append(_eq("attack total", hit["total"], 14))
	rows.append(_eq("attack hits", hit["hit"], true))
	rows.append(_eq("situational penalties subtract", Combat.attack(12, 0, 1, 1, 13, -4)["hit"], false))

	# Shock 2/15 against AC 13 -> 2 + attribute modifier 1 = 3.
	var shock := {"amount": 2, "max_ac": 15}
	rows.append(_eq("shock applies within its AC", Combat.shock_damage(shock, 1, 13), 3))
	rows.append(_eq("shock stops above its AC", Combat.shock_damage(shock, 1, 16), 0))
	rows.append(_eq("unconditional shock ignores AC",
		Combat.shock_damage({"amount": 5, "max_ac": 99}, 0, 30), 5))

	# A hit can never deal less than the Shock it would have done: 1 rolled damage vs Shock 3.
	rows.append(_eq("hit damage floored by shock",
		Combat.hit_damage_with_shock_floor(1, shock, 1, 13), 3))
	rows.append(_eq("hit damage above the floor stands",
		Combat.hit_damage_with_shock_floor(9, shock, 1, 13), 9))

	rows.append(_eq("trauma at or above target", Combat.is_traumatic_hit(6, 6), true))
	rows.append(_eq("trauma below target", Combat.is_traumatic_hit(5, 6), false))
	rows.append(_eq("trauma multiplies the whole hit", Combat.traumatic_damage(6, 3), 18))
	rows.append(_eq("better armour raises the target", Combat.is_traumatic_hit(7, 9), false))

	var soak: Dictionary = Combat.apply_soak(5, 3)
	rows.append(_eq("soak absorbs first", soak["damage_taken"], 2))
	rows.append(_eq("soak pool is spent", soak["soak_remaining"], 0))
	rows.append(_eq("spent soak absorbs nothing", Combat.apply_soak(4, 0)["damage_taken"], 4))

	var nonlethal_weapon := {"shock": {"amount": 0, "max_ac": -99}, "trauma_rating": 1}
	var miss: Dictionary = Combat.resolve_attack({
		"d20": 2, "attack_bonus": 0, "attribute_modifier": 0, "skill_rank": 0,
		"armor_class": 13, "weapon": nonlethal_weapon, "target_melee_ac": 13,
	})
	rows.append(_eq("a natural 2 misses", miss["hit"], false))
	rows.append(_eq("a miss deals no damage without shock", miss["damage"], 0))

	var traumatic_hit: Dictionary = Combat.resolve_attack({
		"d20": 15, "attack_bonus": 1, "attribute_modifier": 1, "skill_rank": 1,
		"armor_class": 13, "weapon": {"shock": shock, "trauma_rating": 3},
		"damage_die_roll": 4, "damage_bonus": 2, "trauma_roll": 6, "target_melee_ac": 13,
	})
	rows.append(_eq("resolve reports a hit", traumatic_hit["hit"], true))
	rows.append(_eq("damage before trauma", traumatic_hit["rolled"], 7))
	rows.append(_eq("traumatic hit triples", traumatic_hit["damage"], 21))
	rows.append(_eq("trauma flagged", traumatic_hit["traumatic"], true))

	return rows
