## Drones and vehicles, checked against the CWN SRD (#848 baseline).
##
## Every expected value is quoted from `gear-vehicles-cyberware/drones`,
## `gear-vehicles-cyberware/vehicles` and `rules-of-the-game/combat/vehicle-combat` at
## https://cwn.quadrifons.com/ rather than from the implementation, so a changed rule fails here.
extends RefCounted

const Vehicles := preload("res://godot/core/cwn_srd_vehicles.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]

func run() -> Array:
	var rows: Array = []
	var v: Vehicles = Vehicles.new()
	rows.append(_eq("the catalogue loads", v.load_catalogue(), true))

	# --- drones catalogue -------------------------------------------------------
	rows.append(_eq("nine common drones", v.drone_names().size(), 9))
	var mouse: Dictionary = v.drone("Mouse")
	rows.append(_eq("Mouse costs $500", mouse["cost"], 500))
	rows.append(_eq("Mouse AC is 13", mouse["ac"], 13))
	rows.append(_eq("Mouse has 1 HP", mouse["hp"], 1))
	rows.append(_eq("Mouse carries no fittings", mouse["fittings"], 0))
	rows.append(_eq("Mouse is a ground drone", mouse["flies"], false))
	var hum: Dictionary = v.drone("Hummingbird")
	rows.append(_eq("Hummingbird flies", hum["flies"], true))
	rows.append(_eq("Hummingbird AC is 15", hum["ac"], 15))
	rows.append(_eq("every drone has a trauma target of at least 6",
		v.drone("Roach")["trauma_target"] >= 6, true))

	# --- drone operation limits -------------------------------------------------
	rows.append(_eq("1000 m is inside the safe control range", v.control_range(1000.0)["reason"], "safe"))
	rows.append(_eq("beyond 1000 m the drone is hijackable", v.control_range(5000.0)["hijack_auto"], true))
	rows.append(_eq("beyond 1000 m control is still possible", v.control_range(5000.0)["ok"], true))
	rows.append(_eq("beyond 8000 m control fails", v.control_range(9000.0)["ok"], false))
	rows.append(_eq("1000 m altitude is legal for a flying drone", v.flight_legal(1000.0), true))
	rows.append(_eq("1001 m altitude is not", v.flight_legal(1001.0), false))
	rows.append(_eq("charging is one hour per Encumbrance", v.charge_hours(3), 3.0))
	rows.append(_eq("charging is capped at six hours", v.charge_hours(20), 6.0))
	rows.append(_eq("a drone's action cost to unpack is a Main action",
		v.DEPLOY_ACTIONS["unpack"], ["main"]))
	rows.append(_eq("bringing a drone online costs a Main and a Move",
		v.DEPLOY_ACTIONS["bring_online"], ["main", "move"]))

	# --- hardpoint weapon class -------------------------------------------------
	rows.append(_eq("Enc 3 or less carries pistol-sized weapons", v.hardpoint_weapon_class(3), "pistol"))
	rows.append(_eq("Enc 4 carries rifle-sized weapons", v.hardpoint_weapon_class(4), "rifle"))
	rows.append(_eq("beyond man-portable the SRD defers to the GM",
		v.hardpoint_weapon_class(9), "heavy_gm_discretion"))

	# --- fitting capacity -------------------------------------------------------
	rows.append(_eq("Hummingbird has room for two fittings",
		v.fittings_legal("Hummingbird", ["Ablative Code Buffer", "Altitude Boost Unit"])["ok"], true))
	rows.append(_eq("a third fitting does not fit",
		v.fittings_legal("Hummingbird", ["a", "b", "c"])["reason"], "over_fitting_capacity"))

	# --- vehicles catalogue -----------------------------------------------------
	rows.append(_eq("ten common vehicles", v.vehicle_names().size(), 10))
	var moto: Dictionary = v.vehicle("Motorcycle")
	rows.append(_eq("Motorcycle AC is 13", moto["ac"], 13))
	rows.append(_eq("Motorcycle armor is 4", moto["armor"], 4))
	rows.append(_eq("Motorcycle has 10 HP", moto["hp"], 10))
	rows.append(_eq("Motorcycle is size S", moto["size"], "S"))
	rows.append(_eq("Motorcycle has 1 Power", moto["power"], 1))
	rows.append(_eq("Motorcycle has 3 Mass", moto["mass"], 3))
	var truck: Dictionary = v.vehicle("Truck")
	rows.append(_eq("a Truck is size L", truck["size"], "L"))
	var tank: Dictionary = v.vehicle("Tank")
	rows.append(_eq("a Tank prints a footnote instead of an Armor number",
		tank["armor_note"], "**"))

	# --- money parsing ----------------------------------------------------------
	rows.append(_eq("$7.5K parses", v.money("$7.5K"), 7500))
	rows.append(_eq("$500K@ parses", v.money("$500K@"), 500000))
	rows.append(_eq("$1,000 parses", v.money("$1,000"), 1000))
	rows.append(_eq("a percentage cost is flagged, not guessed",
		v.is_percentage_cost("10%"), true))

	# --- vehicle AC -------------------------------------------------------------
	rows.append(_eq("a stationary vehicle takes -4 AC",
		v.vehicle_ac("Motorcycle", false), 9))
	rows.append(_eq("a moving vehicle adds the driver's Drive skill",
		v.vehicle_ac("Motorcycle", true, 2), 15))

	# --- damage, destruction and occupants --------------------------------------
	var d1: Dictionary = v.apply_damage("Motorcycle", 10)
	rows.append(_eq("armor is subtracted from all damage", d1["through"], 6))
	rows.append(_eq("armor absorbed the difference", d1["armor_absorbed"], 4))
	rows.append(_eq("10 damage does not destroy a 10 HP motorcycle", d1["destroyed_by"], false))
	var d2: Dictionary = v.apply_damage("Motorcycle", 14)
	rows.append(_eq("14 damage reaches 10 and destroys it", d2["destroyed_by"], true))
	rows.append(_eq("a made Luck save halves occupant damage", v.occupant_damage(18, true), 9))
	rows.append(_eq("a failed Luck save takes it all", v.occupant_damage(18, false), 18))

	# --- crash -------------------------------------------------------------------
	var both: Dictionary = v.crash_damage(20, true, true)
	rows.append(_eq("both saves: unscathed", both["damage"], 0))
	var one: Dictionary = v.crash_damage(20, true, false)
	rows.append(_eq("one save failed: half maximum HP", one["damage"], 10))
	rows.append(_eq("one save failed: Mortally Wounded", one["mortally_wounded"], true))
	var neither: Dictionary = v.crash_damage(20, false, false)
	rows.append(_eq("both failed: Major Injury if they survive", neither["major_injury"], true))

	# --- ramming -----------------------------------------------------------------
	var ram_miss: Dictionary = v.ram_target(10, 15, false, 30)
	rows.append(_eq("a lost opposed check is not a ram", ram_miss["rammed"], false))
	var ram_hit: Dictionary = v.ram_target(15, 10, false, 30)
	rows.append(_eq("a won opposed check deals maximum HP", ram_hit["damage"], 30))
	rows.append(_eq("the ram's Trauma Die is 1d12/x3",
		[ram_hit["trauma_die_faces"], ram_hit["trauma_rating"]], [12, 3]))
	var ram_dodged: Dictionary = v.ram_target(15, 10, true, 30)
	rows.append(_eq("an Evasion save negates it", ram_dodged["damage"], 0))
	var vram: Dictionary = v.ram_vehicle(15, 10, 30)
	rows.append(_eq("ramming a vehicle damages it", vram["damage"], 30))
	rows.append(_eq("and the rammer takes the same", vram["counter_damage"], 30))

	# --- fitting legality --------------------------------------------------------
	# "Crash Pod" carries Min. Size M; a Motorcycle is size S.
	rows.append(_eq("a size-M fitting cannot go on a size-S hull",
		v.can_mount("Motorcycle", "Crash Pod")["reason"], "too_small"))
	rows.append(_eq("a size-L fitting cannot go on a size-M hull either",
		v.can_mount("Car", "Living Quarters")["reason"], "too_small"))
	rows.append(_eq("a size-S fitting fits a larger hull",
		v.can_mount("Car", "Armor Plating")["ok"], true))
	rows.append(_eq("a fitting within Power and Mass is allowed",
		v.can_mount("Car", "Advanced Sensors")["ok"], true))

	return rows
