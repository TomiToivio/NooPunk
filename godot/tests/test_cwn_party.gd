extends RefCounted

## #806: the player is a created level-1 field agent, the party is 1..4, and Romppainen is an
## experienced companion rather than the protagonist.
const Party := preload("res://godot/core/cwn_party.gd")
const Character := preload("res://godot/core/cwn_character.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func _agent(id: String = "pc") -> Dictionary:
	var made: Dictionary = Character.create_field_agent({
		"id": id, "name": "Agent Virtanen", "agency": "Suojelupoliisi",
		"rolls": [10, 12, 11, 13, 9, 10], "hp_roll": 4,
	})
	return made.get("member", {})

func run() -> Array:
	var rows: Array = []

	# --- the player character is created, not Romppainen ---
	var agent := _agent()
	rows.append(_eq("field agent is level 1", int(agent.get("level", 0)), 1))
	rows.append(_eq("field agent is the PC", bool(agent.get("is_pc", false)), true))
	rows.append(_eq("field agent carries an agency", str(agent.get("agency", "")), "Suojelupoliisi"))
	rows.append(_eq("hit points came from the d6 roll", int(agent.get("hit_points", 0)), 4))
	rows.append(_eq("an unknown agency is refused",
		Character.create_field_agent({"agency": "KGB", "rolls": [10, 10, 10, 10, 10, 10]}).get("ok"),
		false))
	rows.append(_eq("all three agencies are allowed",
		Character.create_field_agent({"agency": "Europol", "rolls": [10, 10, 10, 10, 10, 10]}).get("ok"),
		true))

	# --- Romppainen is experienced and not the protagonist ---
	var romppainen: Dictionary = Character.romppainen_companion()
	rows.append(["Romppainen is above level 1", int(romppainen["level"]) > 1, ""])
	rows.append(_eq("Romppainen is not the PC", romppainen["is_pc"], false))
	rows.append(_eq("Romppainen is controllable", romppainen["controllable"], true))
	rows.append(_eq("Romppainen cannot be forced to level 1",
		int(Character.romppainen_companion(1)["level"]), 2))

	# --- party size 1..4 ---
	var solo := Party.new()
	rows.append(_eq("a solo party takes one member", solo.add_member(agent)["ok"], true))
	rows.append(_eq("solo party size", solo.size(), 1))
	rows.append(_eq("the PC cannot leave", solo.remove_member("pc")["ok"], false))
	rows.append(_eq("the PC survives the attempt", solo.size(), 1))

	var team := Party.new()
	team.add_member(_agent())
	rows.append(_eq("a second member joins", team.add_member(Character.romppainen_companion())["ok"], true))
	rows.append(_eq("a third joins", team.add_member({"id": "ally1", "name": "Ally", "level": 2})["ok"], true))
	rows.append(_eq("a fourth joins", team.add_member({"id": "ally2", "name": "Ally 2", "level": 2})["ok"], true))
	rows.append(_eq("party is full at four", team.size(), 4))
	rows.append(_eq("a fifth is refused", team.add_member({"id": "ally3", "level": 2})["ok"], false))
	rows.append(_eq("refusal names the limit",
		team.add_member({"id": "ally3", "level": 2})["reason"], "party_is_full"))

	# --- join, leave, control ---
	rows.append(_eq("a companion leaves", team.remove_member("romppainen")["ok"], true))
	rows.append(_eq("the party shrinks", team.size(), 3))
	rows.append(_eq("control falls back to the PC", team.controlled_id, "pc"))

	rows.append(_eq("control passes to a companion", team.set_controlled("ally1")["ok"], true))
	rows.append(_eq("the controlled member is the companion", team.controlled_id, "ally1"))
	rows.append(_eq("control does not change who the PC is",
		team.player_character()["id"], "pc"))
	rows.append(_eq("control of a non-member is refused",
		team.set_controlled("nobody")["ok"], false))

	rows.append(_eq("duplicate ids are refused", team.add_member({"id": "ally1", "level": 2})["ok"], false))
	rows.append(_eq("a second PC is refused", team.add_member({"id": "pc2", "level": 1, "is_pc": true})["reason"],
		"party_already_has_a_player_character"))

	# --- persistence across changing composition ---
	var saved: Dictionary = team.to_dict()
	var restored := Party.new()
	rows.append(_eq("a party save loads", restored.from_dict(saved), true))
	rows.append(_eq("size survives", restored.size(), team.size()))
	rows.append(_eq("control survives", restored.controlled_id, "ally1"))
	rows.append(_eq("the PC survives", restored.player_character()["id"], "pc"))
	rows.append(_eq("inventory survives", typeof(restored.player_character()["inventory"]), TYPE_ARRAY))

	# Solo play must persist too — the smallest party is the easiest to break.
	var solo_saved: Dictionary = solo.to_dict()
	var solo_restored := Party.new()
	rows.append(_eq("a solo party loads", solo_restored.from_dict(solo_saved), true))
	rows.append(_eq("solo size survives", solo_restored.size(), 1))

	# --- corrupt saves are refused, not half-applied ---
	var no_pc: Dictionary = team.to_dict()
	for member in no_pc["members"]:
		member["is_pc"] = false
	rows.append(_eq("a party with no PC is corrupt", restored.from_dict(no_pc), false))

	var two_pcs: Dictionary = team.to_dict()
	two_pcs["members"][1]["is_pc"] = true
	rows.append(_eq("a party with two PCs is corrupt", restored.from_dict(two_pcs), false))

	var too_many: Dictionary = team.to_dict()
	while too_many["members"].size() <= 4:
		too_many["members"].append({"id": "extra%s" % too_many["members"].size(), "level": 1})
	rows.append(_eq("an oversized party is corrupt", restored.from_dict(too_many), false))

	var bad_version: Dictionary = team.to_dict()
	bad_version["version"] = 99
	rows.append(_eq("a foreign version is refused", restored.from_dict(bad_version), false))
	rows.append(_eq("a refused load leaves the party intact", restored.size(), team.size()))

	return rows
