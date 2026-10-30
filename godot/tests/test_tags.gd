extends RefCounted

## #821 parity suite: typed tags, seven attributes, skill tags, statuses and the Empathy boundary.
const Tags := preload("res://godot/core/cwn_tags.gd")
const Character := preload("res://godot/core/cwn_character.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	# --- the 3d6 bands are exact and are not a normal distribution ---
	var bands := {3: -2, 4: -1, 7: -1, 8: 0, 13: 0, 14: 1, 17: 1, 18: 2}
	for score in bands.keys():
		rows.append(_eq("3d6 %d -> %+d" % [score, bands[score]],
			Tags.attribute_value_for_3d6(score), bands[score]))
	rows.append(_eq("no human roll reaches -3", Tags.attribute_value_for_3d6(3), -2))

	# --- seven attributes, generated, modifier-only ---
	rows.append(_eq("there are seven attributes", Tags.ATTRIBUTES.size(), 7))
	var made: Dictionary = Character.generate_noopunk_attributes([3, 10, 14, 18, 8, 12, 15])
	rows.append(_eq("seven rolls produce seven tags", made.get("tags", []).size(), 7))
	rows.append(_eq("Fitness from a 3 is -2", made["values"]["Fitness"], -2))
	rows.append(_eq("Cognition from 10 is 0", made["values"]["Cognition"], 0))
	rows.append(_eq("Awareness from 14 is +1", made["values"]["Awareness"], 1))
	rows.append(_eq("Agency from 18 is +2", made["values"]["Agency"], 2))
	rows.append(_eq("six rolls are refused",
		Character.generate_noopunk_attributes([3, 10, 14, 18, 8, 12]).get("ok"), false))

	# --- display syntax: sign for attributes and statuses, level for skills ---
	rows.append(_eq("attribute formats with a sign",
		Tags.format(Tags.make("attribute", "Fitness", -2)), "Fitness-2"))
	rows.append(_eq("positive attribute shows +",
		Tags.format(Tags.make("attribute", "Cognition", 2)), "Cognition+2"))
	rows.append(_eq("zero attribute shows +0",
		Tags.format(Tags.make("attribute", "Awareness", 0)), "Awareness+0"))
	rows.append(_eq("skill formats as a level",
		Tags.format(Tags.make("skill", "Firearms", 1)), "Firearms-1"))
	rows.append(_eq("status formats with a sign",
		Tags.format(Tags.make("status", "wounded", -1)), "wounded-1"))
	rows.append(_eq("unicode names survive",
		Tags.format(Tags.make("skill", "Noöware", 2)), "Noöware-2"))

	# --- parsing round-trips, and the kind is required because the text is ambiguous ---
	rows.append(_eq("parse a skill", Tags.parse("Noöware-2", "skill").get("name"), "Noöware"))
	rows.append(_eq("parse an attribute", Tags.parse("Agency+1", "attribute").get("value"), 1))
	rows.append(_eq("parse a status", Tags.parse("wounded-1", "status").get("value"), -1))
	rows.append(_eq("a skill above 4 is not a skill tag", Tags.parse("Firearms-5", "skill"), {}))
	rows.append(_eq("garbage does not parse", Tags.parse("nonsense", "skill"), {}))

	# --- skills: names, defaults, aliases ---
	rows.append(_eq("the skill list has 21 entries", Tags.SKILLS.size(), 21))
	rows.append(_eq("Firearms replaces Shoot", Tags.SKILL_ALIASES["Shoot"], "Firearms"))
	rows.append(_eq("Melee replaces Stab", Tags.SKILL_ALIASES["Stab"], "Melee"))
	rows.append(_eq("Unarmed replaces Punch", Tags.SKILL_ALIASES["Punch"], "Unarmed"))
	rows.append(_eq("Hardware replaces Fix", Tags.SKILL_ALIASES["Fix"], "Hardware"))
	rows.append(_eq("Wetware replaces Heal", Tags.SKILL_ALIASES["Heal"], "Wetware"))
	rows.append(_eq("Software replaces Program", Tags.SKILL_ALIASES["Program"], "Software"))
	rows.append(_eq("Firearms defaults to Reflexes", Character.skill_attribute("Firearms"), "Reflexes"))
	rows.append(_eq("Software defaults to Cyber", Character.skill_attribute("Software"), "Cyber"))
	rows.append(_eq("Noöware defaults to Empathy", Character.skill_attribute("Noöware"), "Empathy"))

	# --- Talk is contextual: the same skill, different attributes, by approach ---
	rows.append(_eq("Talk by rapport uses Empathy",
		Character.skill_attribute("Talk", "rapport"), "Empathy"))
	rows.append(_eq("Talk by authority uses Agency",
		Character.skill_attribute("Talk", "authority"), "Agency"))
	rows.append(_eq("Talk with no approach is left open",
		Character.skill_attribute("Talk"), ""))
	rows.append(_eq("Know is left open pending the author",
		Character.skill_attribute("Know"), ""))
	rows.append(_eq("Work is left open pending the author",
		Character.skill_attribute("Work"), ""))

	# --- skill tags: 0..4, and untrained is -1 or prohibited, never silently zero ---
	rows.append(_eq("skill level 0 is legal", Character.skill_tag("Firearms", 0).get("value"), 0))
	rows.append(_eq("skill level 4 is legal", Character.skill_tag("Firearms", 4).get("value"), 4))
	rows.append(_eq("skill level 5 is refused", Character.skill_tag("Firearms", 5), {}))
	rows.append(_eq("unknown skills are refused", Character.skill_tag("Basketweaving", 1), {}))
	rows.append(_eq("untrained attempts at -1",
		Character.untrained_outcome(false), {"allowed": true, "modifier": -1, "reason": ""}))
	rows.append(_eq("untrained prohibited is refused",
		Character.untrained_outcome(true)["allowed"], false))

	# --- statuses: temporary, stacking, exclusivity, expiry ---
	var tags: Array = []
	tags = Tags.apply_status(tags, Tags.make("status", "wounded", -1, {"temporary": true, "duration": 3}))
	rows.append(_eq("a status applies", Tags.total_for(tags, "status", "wounded"), -1))
	var worse: Array = Tags.apply_status(tags, Tags.make("status", "wounded", -2, {"temporary": true, "duration": 2}))
	rows.append(_eq("a worse status replaces the weaker", Tags.total_for(worse, "status", "wounded"), -2))
	var milder: Array = Tags.apply_status(tags, Tags.make("status", "wounded", -1, {"temporary": true}))
	rows.append(_eq("a milder status does not cancel the worse", Tags.total_for(milder, "status", "wounded"), -1))
	var stacking: Array = Tags.apply_status(tags, Tags.make("status", "wounded", -1,
		{"temporary": true, "stacking": "add"}))
	rows.append(_eq("additive statuses stack", Tags.total_for(stacking, "status", "wounded"), -2))

	var exclusive: Array = [Tags.make("status", "frightened", -1, {"temporary": true, "exclusive_group": "mood"})]
	exclusive = Tags.apply_status(exclusive, Tags.make("status", "calm", 1,
		{"temporary": true, "exclusive_group": "mood"}))
	rows.append(_eq("an exclusive status clears its group",
		Tags.total_for(exclusive, "status", "frightened"), 0))

	var ticking: Array = Tags.apply_status([], Tags.make("status", "stunned", -1,
		{"temporary": true, "duration": 2}))
	ticking = Tags.tick_statuses(ticking, 1)
	rows.append(_eq("a status ticks down", int(ticking[0].get("duration", 0)), 1))
	ticking = Tags.tick_statuses(ticking, 1)
	rows.append(_eq("an expired status is removed", ticking.size(), 0))

	var permanent: Array = [Tags.make("trait", "cyberware", 0, {"permanent": true})]
	rows.append(_eq("permanent traits do not expire", Tags.tick_statuses(permanent, 99).size(), 1))

	# --- Empathy -3: not human, not a player character ---
	var human: Dictionary = Character.generate_noopunk_attributes([10, 10, 10, 10, 10, 10, 10])
	rows.append(_eq("a normal human is PC-eligible", human["eligible_as_pc"], true))
	var inhuman: Array = CwnTags.attributes_from_rolls([10, 10, 10, 10, 10, 10, 3])
	rows.append(["the generator cannot produce Empathy -3",
		int(CwnTags.total_for(inhuman, "attribute", "Empathy")) == -2, ""])
	rows.append(_eq("an Empathy -3 character is not PC-eligible",
		CwnTags.is_player_character_eligible([Tags.make("attribute", "Empathy", -3)]), false))
	rows.append(_eq("Empathy -2 is still human",
		CwnTags.is_player_character_eligible([Tags.make("attribute", "Empathy", -2)]), true))

	# --- transhuman values are representable, never generated ---
	var transhuman: Array = [Tags.make("attribute", "Cognition", 3)]
	rows.append(_eq("above +2 is not a human attribute", Tags.is_human_attribute(transhuman[0]), false))
	rows.append(_eq("but the sheet can still show it", Tags.format(transhuman[0]), "Cognition+3"))

	# --- crosswalk reports ambiguity instead of inventing an assignment ---
	var cross: Dictionary = Character.crosswalk_legacy_attributes(
		{"WIS": 1, "STR": 1, "CON": 0, "DEX": 2, "INT": 1, "CHA": -1})
	# Agency is fed by Wisdom *and* Charisma, which is exactly the ambiguity the crosswalk is meant
	# to surface rather than resolve.
	rows.append(_eq("Agency is fed by two old attributes",
		cross["proposed"]["Agency"].size(), 2))
	rows.append(_eq("the crosswalk flags attributes fed by several old scores",
		cross["needs_author_decision"].has("Fitness"), true))
	rows.append(["the crosswalk does not assign a final value",
		not cross.has("assigned"), ""])

	return rows
