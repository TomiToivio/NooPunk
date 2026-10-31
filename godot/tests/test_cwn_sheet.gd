extends RefCounted

## #897 item 21 with item 3: the CWN sheet composes the kernel and keeps the core intact.
const Sheet := preload("res://godot/core/cwn_sheet.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func _member(overrides: Dictionary = {}) -> Dictionary:
	var m := {
		"name": "Test Agent",
		"level": 1,
		"attributes": {"strength": 12, "dexterity": 10, "constitution": 14,
			"intelligence": 9, "wisdom": 13, "charisma": 8},
		"skills": {"shoot": 1, "notice": 1},
		"background": "soldier",
		"edges": ["hard_to_kill"],
		"foci": [],
	}
	m.merge(overrides, true)
	return m

func run() -> Array:
	var rows: Array = []

	var sheet := Sheet.build(_member(), {"equipment": [{"name": "pistol", "points": 1},
			{"name": "armour", "points": 2}], "xp": 0})

	# item 3: six attributes on the CWN scale, with modifiers derived from the scores
	rows.append(_eq("six attributes", sheet["attributes"].size(), 6))
	for name in Sheet.ATTRIBUTES:
		var score: int = sheet["attributes"][name]["score"]
		rows.append(["%s within 3-18" % name, score >= 3 and score <= 18, str(score)])
	rows.append(_eq("str 12 gives +0", sheet["attributes"]["STR"]["modifier"], 0))
	rows.append(_eq("con 14 gives +1", sheet["attributes"]["CON"]["modifier"], 1))
	# The modifier is whatever the kernel says for that score - asserting a hardcoded number here would
	# make the test the rule instead of the sheet.
	rows.append(_eq("CHA modifier matches the kernel",
		sheet["attributes"]["CHA"]["modifier"], Sheet.modifier_for(8)))

	# saves, HP, attack and strain come from the kernel, not from the sheet
	rows.append(_eq("four saves", sheet["saves"].size(), 4))
	rows.append(["hp is positive", int(sheet["hp"]["max"]) > 0, str(sheet["hp"]["max"])])
	rows.append(_eq("level 1 attack bonus", sheet["attack"]["bonus"], 0))
	rows.append(["strain capacity present", float(sheet["strain"]["capacity"]) > 0.0,
		str(sheet["strain"]["capacity"])])

	# equipment and encumbrance
	rows.append(_eq("equipment points sum", sheet["encumbrance"]["stowed"], 3))
	rows.append(["encumbrance tier named", String(sheet["encumbrance"]["tier"]) != "",
		String(sheet["encumbrance"]["tier"])])

	# advancement
	rows.append(_eq("zero xp is level 1", sheet["advancement"]["level_from_xp"], 1))

	# the sheet validates as CWN
	rows.append(_eq("a good sheet validates", Sheet.validate(sheet), []))

	# and a broken one does not
	var broken := Sheet.build(_member({"attributes": {"strength": 22}}), {})
	var problems := Sheet.validate(broken)
	rows.append(["an out-of-range score is caught",
		problems.any(func(p): return String(p).contains("STR")), str(problems)])
	rows.append(["missing attributes are caught",
		problems.any(func(p): return String(p).contains("missing attribute")), str(problems)])

	# item 3's boundary: a NoöPunk mod may add sections but may not edit CWN numbers
	var modded := Sheet.build(_member(), {"mods": {"psyche": {"instability": 2}}})
	rows.append(_eq("a legal mod keeps the sheet valid", Sheet.validate(modded), []))
	rows.append(_eq("the mod is carried in its own section", modded["mods"].has("psyche"), true))

	var illegal := Sheet.build(_member(), {"mods": {"attributes": {"strength": 18}}})
	var illegal_problems := Sheet.validate(illegal)
	rows.append(["a mod editing CWN attributes is refused",
		illegal_problems.any(func(p): return String(p).contains("override")), str(illegal_problems)])

	return rows
