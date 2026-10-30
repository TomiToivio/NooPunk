extends RefCounted

## #809: the player is a created level-1 field agent; Romppainen is a recruitable senior companion.
##
## These rows test the integration, not just a factory: a legal sheet in the shape the session and
## the scene code already consume, seated through the merged `NoopunkParty` roster, at every party
## size from solo to four, and persisted across a changing composition.

const Agent := preload("res://godot/core/field_agent.gd")
const Party := preload("res://godot/core/party.gd")
const Session := preload("res://godot/core/session.gd")
const Adapter := preload("res://godot/core/rules_adapter.gd")

const ARRAY := {"STR": 9, "DEX": 12, "CON": 11, "INT": 14, "WIS": 10, "CHA": 7}
const ROLLS := [3, 3, 3, 4, 4, 4, 5, 5, 5, 2, 2, 6, 6, 1, 1, 4, 3, 2]

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func _agent(member_name: String = "Kenttäagentti", agency: String = "Suojelupoliisi") -> Dictionary:
	return Agent.create(member_name, agency, [], ARRAY, {"Investigate": 1}, 4)

func _romppainen() -> Dictionary:
	return {"id": "romppainen", "name": "Dr. Harri S. Romppainen", "level": 5, "kind": "npc",
		"hp_max": 24, "attributes": {"INT": 15}}

func run() -> Array:
	var rows: Array = []

	# --- the sheet is legal and session-shaped ---
	var made := _agent()
	rows.append(_eq("a field agent is created", bool(made.get("ok", false)), true))
	var sheet: Dictionary = made["sheet"]
	rows.append(_eq("at level one", int(sheet.get("level", 0)), 1))
	rows.append(_eq("for an agency", String(sheet.get("agency", "")), "Suojelupoliisi"))
	rows.append(_eq("as the protagonist kind", String(sheet.get("kind", "")), "pc"))
	for key in ["attributes", "saves", "skills", "attack", "hp_max", "ac", "ac_melee", "ac_ranged",
			"strain", "gear", "psionics"]:
		rows.append(_eq("the sheet carries `%s` for the session" % key, sheet.has(key), true))
	rows.append(_eq("hit points are 1d6 + CON (11 is +0)", int(sheet.get("hp_max", 0)), 4))
	rows.append(_eq("the sidearm is a ranged weapon", String(sheet["attack"].get("weapon_kind", "")), "ranged"))
	rows.append(_eq("Investigate is trained from the build", int(sheet["skills"].get("Investigate", -1)), 1))
	rows.append(_eq("an unknown agency is refused",
		bool(Agent.create("X", "KGB", [], ARRAY).get("ok", true)), false))
	rows.append(_eq("a nameless agent is refused",
		bool(Agent.create("   ", "Europol", [], ARRAY).get("ok", true)), false))
	rows.append(_eq("an out-of-range hit die is refused",
		bool(Agent.create("X", "UNSA", [], ARRAY, {}, 9).get("ok", true)), false))
	rows.append(_eq("dice build the same sheet shape",
		bool(Agent.create("Rolled", "Europol", ROLLS, {}, {}, 3).get("ok", false)), true))

	# --- the roster seats the agent and recruits Romppainen ---
	var party = Party.new()
	rows.append(_eq("the agent is seated", party.create_agent("pc", "Kenttäagentti", "Suojelupoliisi", sheet), true))
	rows.append(_eq("only once", party.create_agent("pc2", "Impostor", "Europol", sheet), false))
	rows.append(_eq("the protagonist is player-kind", String(party.protagonist.get("kind", "")), "pc"))
	rows.append(_eq("Romppainen joins", party.join(_romppainen()), true))
	var joined: Dictionary = party.members.back() if not party.members.is_empty() else {}
	rows.append(_eq("as an npc", String(joined.get("kind", "")), "npc"))
	rows.append(_eq("at a higher level than the PC",
		int(joined.get("level", 0)) > int(party.protagonist.get("level", 0)), true))
	rows.append(_eq("joining twice is refused", party.join(_romppainen()), false))
	rows.append(_eq("the protagonist cannot leave", party.leave("pc"), false))
	rows.append(_eq("a companion can leave", party.leave("romppainen"), true))

	# --- every size from solo to four ---
	for size in [1, 2, 3, 4]:
		var roster = Party.new()
		roster.create_agent("pc", "Agent", "UNSA", sheet)
		for index in range(size - 1):
			roster.join({"id": "c%d" % index, "name": "Ally %d" % index, "level": 2, "kind": "npc"})
		rows.append(_eq("a party of %d is legal" % size, roster.members.size(), size))
		rows.append(_eq("a party of %d has its protagonist selected" % size,
			String(roster.selected().get("id", "")), "pc"))
	var full = Party.new()
	full.create_agent("pc", "Agent", "UNSA", sheet)
	for index in range(3):
		full.join({"id": "a%d" % index, "name": "Ally %d" % index, "level": 2, "kind": "npc"})
	rows.append(_eq("four members fill the party", full.members.size(), 4))
	rows.append(_eq("a fifth member is refused", full.join({"id": "a3", "name": "Ally 3", "level": 2}), false))

	# --- selection drives whose sheet answers ---
	var crew = Party.new()
	crew.create_agent("pc", "Agent", "Suojelupoliisi", sheet)
	crew.join(_romppainen())
	rows.append(_eq("the PC is selected at start", String(crew.selected().get("id", "")), "pc"))
	rows.append(_eq("a companion can be selected", crew.select_member("romppainen"), true))
	rows.append(_eq("and reports its own sheet", int(crew.selected().get("level", 0)), 5))
	rows.append(_eq("a companion leaves", crew.leave("romppainen"), true))
	rows.append(_eq("leaving reseats the protagonist", String(crew.selected_id), "pc"))

	# --- persistence across a changing roster ---
	crew.join(_romppainen())
	var saved: Dictionary = crew.to_dict()
	crew.join({"id": "temp", "name": "Temp", "level": 2, "kind": "npc"})
	crew.leave("temp")
	var restored = Party.new()
	rows.append(_eq("a roster round-trips", restored.from_dict(saved), true))
	rows.append(_eq("with the same members", restored.members.size(), saved["members"].size()))
	rows.append(_eq("and the same protagonist", String(restored.protagonist.get("id", "")), "pc"))
	rows.append(_eq("a roster with a level-2 protagonist is refused",
		Party.new().from_dict({"version": 1, "protagonist": {"id": "pc", "level": 2, "kind": "pc", "agency": "UNSA"},
			"members": [{"id": "pc", "level": 2, "kind": "pc", "agency": "UNSA"}], "selected_id": "pc"}), false))

	# --- the slice takes its player-side actor id from the character, not from a literal ---
	var session = Session.new(Adapter.new(Adapter.DEFAULT_KERNEL_PATH, 7))
	var pc_sheet: Dictionary = sheet.duplicate(true)
	pc_sheet["id"] = "agent_007"
	session.character = pc_sheet
	rows.append(_eq("the session reads the generated character id", String(session.character.get("id", "")), "agent_007"))
	rows.append(_eq("and the legacy slice still names Romppainen",
		String(Session.new(Adapter.new(Adapter.DEFAULT_KERNEL_PATH, 7)).character.get("id", "")), "romppainen"))

	return rows
