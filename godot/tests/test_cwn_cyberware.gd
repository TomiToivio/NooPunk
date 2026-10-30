## CWN cyberware systems (#848): every SRD implant table, strain totals and the Major Injury rule.
extends RefCounted

const Cyber := preload("res://godot/core/cwn_cyberware.gd")


func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]


func run() -> Array:
	var rows: Array = []
	var cyber := Cyber.new()

	rows.append(_eq("seven SRD tables are present", cyber.table_names().size(), 7))
	rows.append(_eq("all 80 implants are transcribed", cyber.all().size(), 80))
	for table in cyber.table_names():
		rows.append(["table %s has entries" % table, cyber.by_type(table).size() > 0,
			"got %d" % cyber.by_type(table).size()])

	var dermal := cyber.implant("dermal_armor_i")
	rows.append(_eq("Dermal Armor I cost", dermal.get("cost"), 40000))
	rows.append(_eq("Dermal Armor I strain", dermal.get("strain"), 1.0))
	rows.append(_eq("Dermal Armor I concealment", dermal.get("concealment"), "Medical"))
	rows.append(_eq("Dermal Armor I type", dermal.get("type"), "Skin"))

	# Two headware entries are priced "as cyber" by the SRD; the record keeps that note rather than
	# inventing a credit value.
	var cranial := cyber.implant("cranial_jack")
	rows.append(["cranial jack has no invented cost", cranial.get("cost") == null, str(cranial.get("cost"))])
	rows.append(["cranial jack keeps the SRD note", cranial.has("cost_note"), str(cranial.get("cost_note"))])

	rows.append(_eq("strain adds across implants",
		cyber.total_strain(["dermal_armor_i", "body_blades_i"]), 2.0))
	var priced := cyber.total_cost(["dermal_armor_i", "body_blades_i"])
	rows.append(_eq("priced total", priced["cost"], 50000))
	rows.append(_eq("no unpriced entries in that set", priced["unpriced"].size(), 0))
	var mixed := cyber.total_cost(["dermal_armor_i", "cranial_jack"])
	rows.append(["an unpriced implant is reported, not counted as zero", mixed["unpriced"] == ["cranial_jack"], str(mixed["unpriced"])])

	rows.append(_eq("nerve table count", cyber.by_type("nerve").size(), 13))
	rows.append(_eq("limb implants destroyed by a limb Major Injury",
		cyber.destroyed_by_major_injury("limb").size(), 12))
	rows.append(_eq("body implants destroyed by a torso Major Injury",
		cyber.destroyed_by_major_injury("body").size(), 18))

	var levels := cyber.concealment_levels()
	rows.append(_eq("four concealment levels occur", levels.size(), 4))
	for level in ["Medical", "Obvious", "Sight", "Touch"]:
		rows.append(["concealment %s is used" % level, levels.has(level), str(levels)])

	for row in cyber.all():
		rows.append(["negative strain on %s" % row["id"], float(row["strain"]) >= 0.0, str(row["strain"])])
		rows.append(["cost is a number or explicitly unpriced on %s" % row["id"],
			row.get("cost") is float or (row.get("cost") == null and row.has("cost_note")),
			str(row.get("cost"))])
	return rows
