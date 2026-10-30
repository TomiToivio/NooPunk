## Drones and vehicles, as the Cities Without Number SRD states them.
##
## Source: https://cwn.quadrifons.com/ (CC0 1.0) — pages `gear-vehicles-cyberware/drones`,
## `gear-vehicles-cyberware/vehicles` and `rules-of-the-game/combat/vehicle-combat`. Every number below
## is quoted from those pages; where the SRD leaves a judgement to the GM, this file says so instead of
## inventing a rule (see `hardpoint_weapon_class` and `can_inflict_traumatic_hit`).
##
## Catalogue rows come from `data/rules/cwn/srd_tables.json`, extracted mechanically by
## `tools/cwn_srd_extract.py`. Nothing here hard-codes a drone, a vehicle or a fitting: re-running the
## extractor is enough to pick up a changed table.
##
## It holds no dice. Where a roll is needed the caller passes the result, so the game keeps one seeded
## stream and a save can reproduce a fight.
extends RefCounted
class_name CwnVehicles

const DATA_PATH := "res://data/rules/cwn/srd_tables.json"

## `drones`: "all drones have a safe default control range of 1,000 meters … theoretical maximum
## control range is 8,000 meters."
const DRONE_SAFE_RANGE_M := 1000.0
const DRONE_MAX_RANGE_M := 8000.0
## "Flying drones have an operational altitude maximum of 1,000 meters."
const DRONE_MAX_ALTITUDE_M := 1000.0
## "Drones operate for one hour on a full battery charge … one hour of charging per Encumbrance, or six
## hours at most."
const DRONE_BATTERY_HOURS := 1.0
const DRONE_CHARGE_HOURS_PER_ENC := 1.0
const DRONE_CHARGE_HOURS_MAX := 6.0

## Action economy, verbatim from the drones page.
const DEPLOY_ACTIONS := {"unpack": ["main"], "bring_online": ["main", "move"], "pack": ["main"]}

## `vehicle-combat`: "Firing personal weapons out the window is done at a -4 hit penalty while the
## vehicle is moving." "A stationary vehicle takes a -4 penalty, while a moving one adds its driver's
## Drive skill to its AC."
const FIRING_FROM_MOVING_VEHICLE_PENALTY := -4
const STATIONARY_VEHICLE_AC_PENALTY := -4

## Sizes are ordered so a fitting's "Min. Size" can be compared.
const SIZE_ORDER := ["S", "M", "L"]

var _drones: Array = []
var _drone_fittings: Array = []
var _vehicles: Array = []
var _vehicle_fittings: Array = []
var _vehicle_weapons: Array = []
var _vehicle_mods: Array = []

func _init() -> void:
	load_catalogue()

func load_catalogue() -> bool:
	if not FileAccess.file_exists(DATA_PATH):
		push_error("CwnVehicles: missing %s" % DATA_PATH)
		return false
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("CwnVehicles: %s is not a JSON object" % DATA_PATH)
		return false
	var tables: Variant = (parsed as Dictionary).get("tables", {})
	if typeof(tables) != TYPE_DICTIONARY:
		return false
	for block in Array((tables as Dictionary).get("drones", [])):
		var cols: Array = block.get("columns", [])
		var first := String(cols[0]) if not cols.is_empty() else ""
		if first == "Drone":
			_drones = block.get("rows", [])
		elif first == "Drone Fitting":
			_drone_fittings = block.get("rows", [])
	for block in Array((tables as Dictionary).get("vehicles", [])):
		var cols: Array = block.get("columns", [])
		var first := String(cols[0]) if not cols.is_empty() else ""
		if first == "Vehicle":
			_vehicles = block.get("rows", [])
		elif first == "Fitting":
			_vehicle_fittings = block.get("rows", [])
		elif first == "Weapon":
			_vehicle_weapons = block.get("rows", [])
		elif first == "Mod":
			_vehicle_mods = block.get("rows", [])
	return not _drones.is_empty() and not _vehicles.is_empty()

# --- parsing helpers -------------------------------------------------------------------------

static func _int(text: String, fallback: int = 0) -> int:
	var digits := ""
	for ch in text:
		if ch.is_valid_int() or ch == "-":
			digits += ch
		elif digits != "":
			break
	return int(digits) if digits != "" and digits != "-" else fallback

## "$1,000" -> 1000; "$7.5K" -> 7500; "$500K@" -> 500000; "10%" -> -1 (a percentage of the base).
static func money(text: String) -> int:
	var t := text.strip_edges().replace("$", "").replace(",", "").replace("@", "")
	var multiplier := 1
	if t.ends_with("K") or t.ends_with("k"):
		multiplier = 1000
		t = t.substr(0, t.length() - 1)
	elif t.ends_with("M") or t.ends_with("m"):
		multiplier = 1000000
		t = t.substr(0, t.length() - 1)
	if t.ends_with("%"):
		return -1
	return int(round(float(t) * multiplier))

static func is_percentage_cost(text: String) -> bool:
	return text.strip_edges().ends_with("%")

# --- drones ----------------------------------------------------------------------------------

func drone(name: String) -> Dictionary:
	for row in _drones:
		if String(row.get("Drone", "")).to_lower() == name.to_lower():
			return {
				"name": String(row.get("Drone", "")),
				"cost": money(String(row.get("Cost", ""))),
				"ac": _int(String(row.get("AC", ""))),
				"trauma_target": _int(String(row.get("Trauma Target", ""))),
				"hp": _int(String(row.get("HP", ""))),
				"fittings": _int(String(row.get("Fittings", ""))),
				"move": String(row.get("Move", "")),
				"hardpoints": _int(String(row.get("Hardpoints", ""))),
				"encumbrance": _int(String(row.get("Encumbrance", ""))),
				"flies": String(row.get("Move", "")).to_lower().contains("fly"),
			}
	return {}

func drone_names() -> Array:
	var out: Array = []
	for row in _drones:
		out.append(String(row.get("Drone", "")))
	return out

## "Drones with a base, unmodified Encumbrance of 3 or less can mount only pistol-sized weapons, while
## larger man-portable drones can mount rifle-sized ones. Non-portable drones can mount heavy weapons
## that the GM finds plausible. Melee weapons cannot be practically mounted."
func hardpoint_weapon_class(encumbrance: int) -> String:
	if encumbrance <= 3:
		return "pistol"
	if encumbrance <= 5:
		return "rifle"
	# Beyond man-portable the SRD hands the decision to the GM rather than giving a number.
	return "heavy_gm_discretion"

## Control range: safe, hijackable, or beyond the theoretical maximum.
func control_range(metres: float) -> Dictionary:
	if metres <= DRONE_SAFE_RANGE_M:
		return {"ok": true, "hijack_auto": false, "reason": "safe"}
	if metres <= DRONE_MAX_RANGE_M:
		# "Beyond this range … all wireless hack or jamming attempts against them are automatically
		# successful."
		return {"ok": true, "hijack_auto": true, "reason": "beyond_safe_range"}
	return {"ok": false, "hijack_auto": true, "reason": "beyond_max_range"}

func flight_legal(metres_above_ground: float) -> bool:
	return metres_above_ground <= DRONE_MAX_ALTITUDE_M

## Charging time for a drone: one hour per point of Encumbrance, six hours at most.
func charge_hours(encumbrance: int) -> float:
	return minf(DRONE_CHARGE_HOURS_PER_ENC * float(maxi(0, encumbrance)), DRONE_CHARGE_HOURS_MAX)

## Fittings the drone can carry, as a count and as a legality check.
func fittings_legal(name: String, fitted: Array) -> Dictionary:
	var d := drone(name)
	if d.is_empty():
		return {"ok": false, "reason": "no_such_drone"}
	var capacity := int(d["fittings"])
	var count := fitted.size()
	return {"ok": count <= capacity, "capacity": capacity, "used": count,
		"reason": "" if count <= capacity else "over_fitting_capacity"}

func drone_fitting(name: String) -> Dictionary:
	for row in _drone_fittings:
		if String(row.get("Drone Fitting", "")).to_lower() == name.to_lower():
			var cost := String(row.get("Cost", ""))
			return {"name": String(row.get("Drone Fitting", "")),
				"cost": money(cost), "percentage": is_percentage_cost(cost)}
	return {}

# --- vehicles --------------------------------------------------------------------------------

func vehicle(name: String) -> Dictionary:
	for row in _vehicles:
		if String(row.get("Vehicle", "")).to_lower() == name.to_lower():
			return {
				"name": String(row.get("Vehicle", "")),
				"cost": money(String(row.get("Cost", ""))),
				"speed": _int(String(row.get("Speed", ""))),
				# The Tank and APC print `**` and `*` instead of a number: a footnote, not a value.
				# Parsing that as 0 would silently make them unarmoured, so the marker is kept.
				"armor": _int(String(row.get("Armor", ""))),
				"armor_note": (String(row.get("Armor", "")).strip_edges()
					if _int(String(row.get("Armor", ""))) == 0
					and not String(row.get("Armor", "")).strip_edges().is_valid_int() else ""),
				"trauma_target": _int(String(row.get("Trauma Target", ""))),
				"ac": _int(String(row.get("AC", ""))),
				"hp": _int(String(row.get("HP", ""))),
				"crew": _int(String(row.get("Crew", ""))),
				"power": _int(String(row.get("Power", ""))),
				"mass": _int(String(row.get("Mass", ""))),
				"size": String(row.get("Size", "")),
				"hardpoints": _int(String(row.get("Hardpoints", ""))),
			}
	return {}

func vehicle_names() -> Array:
	var out: Array = []
	for row in _vehicles:
		out.append(String(row.get("Vehicle", "")))
	return out

func vehicle_fitting(name: String) -> Dictionary:
	for row in _vehicle_fittings:
		if String(row.get("Fitting", "")).to_lower() == name.to_lower():
			var cost := String(row.get("Cost", ""))
			return {"name": String(row.get("Fitting", "")), "cost": money(cost),
				"percentage": is_percentage_cost(cost),
				"power": _int(String(row.get("Power", ""))),
				"mass": _int(String(row.get("Mass", ""))),
				"min_size": String(row.get("Min. Size", ""))}
	return {}

static func size_rank(size: String) -> int:
	return SIZE_ORDER.find(size)

## Whether a fitting may be installed: enough free Power and Mass, and large enough a hull.
func can_mount(vehicle_name: String, fitting_name: String, used_power: int = 0,
		used_mass: int = 0) -> Dictionary:
	var v := vehicle(vehicle_name)
	var f := vehicle_fitting(fitting_name)
	if v.is_empty():
		return {"ok": false, "reason": "no_such_vehicle"}
	if f.is_empty():
		return {"ok": false, "reason": "no_such_fitting"}
	var need_size := String(f["min_size"])
	if size_rank(String(v["size"])) < size_rank(need_size):
		return {"ok": false, "reason": "too_small", "min_size": need_size}
	var power_left := int(v["power"]) - used_power
	var mass_left := int(v["mass"]) - used_mass
	if int(f["power"]) > power_left:
		return {"ok": false, "reason": "insufficient_power", "needed": int(f["power"]),
			"free": power_left}
	if int(f["mass"]) > mass_left:
		return {"ok": false, "reason": "insufficient_mass", "needed": int(f["mass"]),
			"free": mass_left}
	return {"ok": true, "power": int(f["power"]), "mass": int(f["mass"])}

## The vehicle's AC in a fight: a stationary vehicle takes -4; a moving one adds the driver's Drive.
func vehicle_ac(vehicle_name: String, moving: bool, driver_drive_skill: int = 0) -> int:
	var v := vehicle(vehicle_name)
	if v.is_empty():
		return 0
	if moving:
		return int(v["ac"]) + driver_drive_skill
	return int(v["ac"]) + STATIONARY_VEHICLE_AC_PENALTY

## Damage to a vehicle: Armor is subtracted from all damage, then HP is reduced; zero destroys it.
func apply_damage(vehicle_name: String, damage: int) -> Dictionary:
	var v := vehicle(vehicle_name)
	if v.is_empty():
		return {"ok": false, "reason": "no_such_vehicle"}
	var through: int = maxi(0, damage - int(v["armor"]))
	return {"armor_absorbed": damage - through, "through": through,
		"destroyed_by": through >= int(v["hp"])}

## "Any occupants take damage as if they were also hit by whatever took out the vehicle, with a Luck save
## for half."
func occupant_damage(incoming_damage: int, luck_save_made: bool) -> int:
	return int(floor(incoming_damage / 2.0)) if luck_save_made else incoming_damage

## Crash damage when the vehicle was moving: each passenger rolls Physical and Luck.
##   both made   -> unscathed
##   one failed  -> half maximum hit points, which may leave them Mortally Wounded
##   both failed -> Mortally Wounded, and a Major Injury if they survive
func crash_damage(max_hp: int, physical_made: bool, luck_made: bool) -> Dictionary:
	if physical_made and luck_made:
		return {"damage": 0, "mortally_wounded": false, "major_injury": false}
	if physical_made or luck_made:
		return {"damage": int(floor(max_hp / 2.0)), "mortally_wounded": true, "major_injury": false}
	return {"damage": int(floor(max_hp / 2.0)), "mortally_wounded": true, "major_injury": true}

## Ramming a human-sized target: opposed Dex/Drive vs Dex/Exert; on the driver's win the target makes an
## Evasion save or takes the vehicle's maximum HP with a 1d12/x3 Trauma Die.
func ram_target(driver_total: int, target_total: int, evasion_save_made: bool,
		vehicle_max_hp: int) -> Dictionary:
	var wins := driver_total > target_total
	if not wins:
		return {"rammed": false, "damage": 0}
	if evasion_save_made:
		return {"rammed": true, "damage": 0, "dodged": true}
	return {"rammed": true, "damage": vehicle_max_hp, "dodged": false,
		"trauma_die_faces": 12, "trauma_rating": 3}

## Ramming a vehicle takes an opposed check with no Evasion save, and "the ramming vehicle also takes
## damage as if the target vehicle rammed it in turn."
func ram_vehicle(driver_total: int, target_total: int, target_max_hp: int) -> Dictionary:
	var wins := driver_total > target_total
	if not wins:
		return {"rammed": false, "damage": 0, "counter_damage": 0}
	return {"rammed": true, "damage": target_max_hp, "counter_damage": target_max_hp}

## "Some weapons can reasonably inflict Traumatic Hits on a given vehicle, at the GM's discretion."
## The SRD sets no rule, so this returns the question rather than an answer.
func trauma_target(vehicle_name: String) -> int:
	return _int(String(vehicle(vehicle_name).get("trauma_target", 0)))
