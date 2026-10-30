extends RefCounted

## The bridge from a created member record to a playable session sheet (#809/#814 step 4).
##
## `create_field_agent()` makes a roster member; `session.gd` needs a sheet with `hp_max`, `ac`, an
## `attack` block and Strain. Until now the only sheet the slice could read was a hand-written JSON
## file, which is why the protagonist could not actually be *created* in the campaign.

const Character := preload("res://godot/core/cwn_character.gd")
const Session := preload("res://godot/core/session.gd")
const Adapter := preload("res://godot/core/rules_adapter.gd")

const ROLLS := [12, 9, 14, 11, 13, 8]

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func _member(level: int = 1) -> Dictionary:
	var made: Dictionary = Character.create_field_agent({
		"id": "pc", "name": "Kenttäagentti", "agency": "Suojelupoliisi",
		"rolls": ROLLS, "hp_roll": 4, "skills": {"Investigate": 1},
	})
	if level != 1:
		made["member"]["level"] = level
	return made["member"]

func run() -> Array:
	var rows: Array = []
	var member := _member()
	var sheet: Dictionary = Character.to_session_sheet(member)

	# --- every key the session, combat and scene code read ---
	for key in ["id", "name", "level", "attributes", "skills", "hp_max", "hp", "ac", "ac_melee",
			"ac_ranged", "attack", "saves", "strain", "gear", "psionics", "kind"]:
		rows.append(_eq("the sheet carries `%s`" % key, sheet.has(key), true))
	rows.append(_eq("identity survives the bridge", String(sheet.get("id", "")), "pc"))
	rows.append(_eq("the name survives", String(sheet.get("name", "")), "Kenttäagentti"))
	rows.append(_eq("the agency survives", String(sheet.get("agency", "")), "Suojelupoliisi"))
	rows.append(_eq("it is a player character", String(sheet.get("kind", "")), "pc"))
	rows.append(_eq("hit points match the member record",
		int(sheet.get("hp_max", 0)), int(member.get("hit_points", -1))))
	rows.append(_eq("current hit points start full", int(sheet.get("hp", 0)), int(sheet.get("hp_max", -1))))

	# --- AC follows the Dexterity modifier unless the build says otherwise ---
	var dex_score := int(member["attributes"].get("DEX", 10))
	var expected_ac := 10 + Character.effective_modifier(dex_score)
	rows.append(_eq("armour class follows DEX", int(sheet.get("ac", 0)), expected_ac))
	var armoured: Dictionary = Character.to_session_sheet(member, {"ac": 15, "ac_melee": 14})
	rows.append(_eq("a build may pin its armour", int(armoured.get("ac", 0)), 15))
	rows.append(_eq("and the melee class separately", int(armoured.get("ac_melee", 0)), 14))
	rows.append(_eq("ranged falls back to the pinned AC", int(armoured.get("ac_ranged", 0)), 15))

	# --- the attack block is always usable ---
	rows.append(_eq("a default attack exists", String(sheet["attack"].get("weapon_kind", "")), "ranged"))
	rows.append(_eq("with a damage line", (sheet["attack"].get("damage", []) as Array).size(), 3))
	var armed: Dictionary = Character.to_session_sheet(member, {"attack": {"name": "shotgun",
		"weapon_kind": "ranged", "attribute": "DEX", "combat_rank": 1, "attack_bonus": 2,
		"damage": [2, 6, 1], "lethal": true}})
	rows.append(_eq("a scenario may supply the weapon", String(armed["attack"].get("name", "")), "shotgun"))

	# --- strain, saves and gear ---
	rows.append(_eq("Strain capacity is Constitution",
		int(sheet["strain"].get("max", 0)), int(member["attributes"].get("CON", 0))))
	rows.append(_eq("no Strain is spent at creation", int(sheet["strain"].get("used", -1)), 0))
	rows.append(_eq("four saves are present", (sheet["saves"] as Dictionary).size(), 4))
	rows.append(_eq("psionics start empty",
		(sheet["psionics"].get("packages", []) as Array).size(), 0))

	# --- the session consumes the bridged sheet ---
	var session = Session.new(Adapter.new(Adapter.DEFAULT_KERNEL_PATH, 9))
	session.character = sheet
	session.hp = int(sheet.get("hp_max", 1))
	rows.append(_eq("the session reads the bridged sheet", int(session.hp), int(sheet["hp_max"])))
	rows.append(_eq("and takes the protagonist id from it", String(session.character.get("id", "")), "pc"))

	# --- a companion bridges to an npc sheet, not a protagonist ---
	var romppainen: Dictionary = Character.romppainen_companion(6)
	var companion: Dictionary = Character.to_session_sheet(romppainen)
	rows.append(_eq("a companion bridges as an npc", String(companion.get("kind", "")), "npc"))
	rows.append(_eq("at its own level", int(companion.get("level", 0)), int(romppainen.get("level", 0))))
	rows.append(_eq("and is never the protagonist", String(companion.get("id", "")) == "pc", false))

	return rows
