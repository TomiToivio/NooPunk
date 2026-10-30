## CWN drones (#848): models, hardpoint classes, mod-derived stats and fitting prices.
extends RefCounted

const Drones := preload("res://godot/core/cwn_drones.gd")


func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]


func run() -> Array:
	var rows: Array = []
	var d := Drones.new()

	rows.append(_eq("nine SRD models", d.models.size(), 9))
	rows.append(_eq("thirty fittings", d.fittings.size(), 30))
	rows.append(_eq("eight mods", d.mods.size(), 8))

	var mouse := d.model("mouse")
	rows.append(_eq("Mouse AC", mouse.get("ac"), 13))
	rows.append(_eq("Mouse HP", mouse.get("hp"), 1))
	rows.append(_eq("Mouse encumbrance", mouse.get("encumbrance"), 1))
	rows.append(_eq("Mouse move", mouse.get("move", {}).get("rate"), 5))

	var kerberos := d.model("kerberos")
	rows.append(["Kerberos is not man-portable", kerberos.get("portable") == false, str(kerberos.get("portable"))])
	rows.append(["Kerberos has no Encumbrance rating", kerberos.get("encumbrance") == null, str(kerberos.get("encumbrance"))])

	rows.append(_eq("Mouse has no hardpoints", d.hardpoint_class("mouse"), "none"))
	rows.append(_eq("Pitbull takes rifles", d.hardpoint_class("pitbull"), "rifle"))
	rows.append(_eq("portable drones at Enc 3 or less would take pistols",
		d.rules().get("hardpoint_capacity", {}).get("portable_max_enc_for_pistols"), 3))
	rows.append(_eq("Kerberos takes heavy weapons", d.hardpoint_class("kerberos"), "heavy"))
	rows.append(_eq("a model with no hardpoints mounts none", d.hardpoint_class("roach"), "none"))

	var plated := d.with_mods("roach", ["heavy_plating"])
	rows.append(_eq("heavy plating adds 2 AC", plated.get("ac"), 15))
	rows.append(_eq("heavy plating costs 5 m of move", plated.get("move", {}).get("rate"), 5))
	rows.append(_eq("heavy plating adds 1 Enc", plated.get("encumbrance"), 4))

	var redundant := d.with_mods("roach", ["redundant_systems"])
	rows.append(_eq("redundant systems add 25% HP rounded up", redundant.get("hp"), 10))

	var boosted := d.with_mods("hummingbird", ["boosted_engine"])
	rows.append(_eq("boosted engine adds 10 m", boosted.get("move", {}).get("rate"), 20))

	var stripped := d.with_mods("roach", ["stripped_fittings"])
	rows.append(_eq("stripped fittings remove one fitting", stripped.get("fittings"), 2))
	rows.append(_eq("stripped fittings remove one Enc", stripped.get("encumbrance"), 2))

	rows.append(_eq("a fitting costs a percentage of the model, rounded up",
		d.fitting_cost("roach", "Improved Armor"), 250))
	rows.append(_eq("no fitting, no cost", d.fitting_cost("roach", "Not A Fitting"), 0))

	var rules := d.rules()
	rows.append(_eq("safe control range", rules.get("control_range_m", {}).get("safe"), 1000))
	rows.append(_eq("maximum control range", rules.get("control_range_m", {}).get("maximum"), 8000))
	rows.append(_eq("battery life", rules.get("battery_hours"), 1))
	rows.append(_eq("deploying online takes a Main and a Move", rules.get("deploy", {}).get("online"), ["main", "move"]))
	rows.append(["melee weapons cannot be mounted", rules.get("melee_mountable") == false, str(rules.get("melee_mountable"))])
	return rows
