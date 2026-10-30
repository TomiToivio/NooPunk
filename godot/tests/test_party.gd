extends RefCounted
const Party := preload("res://godot/core/party.gd")

func _eq(label: String, got: Variant, expected: Variant) -> Array:
	return [label, got == expected, "got %s expected %s" % [got, expected]]

func run() -> Array:
	var rows: Array = []
	var party := Party.new()
	rows.append(_eq("reject invalid academy affiliation", party.create_agent("pc", "Ada", "Unknown"), false))
	rows.append(_eq("create own level-1 law enforcer", party.create_agent("pc", "Ada", "Europol", {"skills": {"Notice": 0}, "inventory": ["badge"]}), true))
	rows.append(_eq("one agent solo", party.members.size(), 1))
	rows.append(_eq("created PC level", party.protagonist["level"], 1))
	rows.append(_eq("created PC background", party.protagonist["role"], "law_enforcer"))
	rows.append(_eq("PC cannot be removed", party.leave("pc"), false))
	rows.append(_eq("Romppainen is an optional higher-level companion", party.join({"id": "romppainen", "name": "Harri Romppainen", "level": 6}), true))
	rows.append(_eq("party of two", party.members.size(), 2))
	rows.append(_eq("NPC is directly controllable", party.select_member("romppainen"), true))
	rows.append(_eq("selected playable companion", party.selected()["id"], "romppainen"))
	rows.append(_eq("third character", party.join({"id": "medic", "level": 2}), true))
	rows.append(_eq("fourth character", party.join({"id": "analyst", "level": 1}), true))
	rows.append(_eq("maximum of four", party.members.size(), 4))
	rows.append(_eq("fifth slot rejected", party.join({"id": "extra", "level": 1}), false))
	rows.append(_eq("duplicate rejected", party.join({"id": "romppainen", "level": 6}), false))
	var saved: Dictionary = party.to_dict()
	var restored := Party.new()
	rows.append(_eq("save-load roundtrip", restored.from_dict(saved), true))
	rows.append(_eq("save-load matches original", restored.to_dict(), saved))
	rows.append(_eq("companion can leave", restored.leave("romppainen"), true))
	rows.append(_eq("selection returns to PC", restored.selected_id, "pc"))
	rows.append(_eq("PC character build survives roster changes", restored.protagonist["inventory"], ["badge"]))
	rows.append(_eq("invalid roster rejected", restored.from_dict({"version": 1, "protagonist": saved["protagonist"], "members": [], "selected_id": "pc"}), false))
	rows.append(_eq("invalid save leaves existing party intact", restored.members.size(), 3))
	return rows
