## CWN drones (#848): the nine SRD models, their fittings and mods, and the derived stats those mods
## change. Values come from data/rules/cwn_drones.json, transcribed from the CC0 SRD.
class_name CwnDrones
extends RefCounted

const PATH := "res://data/rules/cwn_drones.json"

var data: Dictionary = {}
var models: Dictionary = {}
var fittings: Dictionary = {}
var mods: Dictionary = {}


func _init(path: String = PATH) -> void:
	data = _load(path)
	for row in data.get("models", []):
		models[String(row["id"])] = row
	for row in data.get("fittings", []):
		fittings[String(row["name"])] = row
	for row in data.get("mods", []):
		mods[String(row["id"])] = row


func _load(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("cwn_drones: cannot open %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func model(id: String) -> Dictionary:
	return models.get(id, {})


func rules() -> Dictionary:
	return data.get("rules", {})


## The largest weapon class a model can mount. Portable drones of Enc 3 or less take pistols; larger
## portable drones take rifles; non-portable drones take heavy weapons.
func hardpoint_class(id: String) -> String:
	var drone := model(id)
	if drone.is_empty():
		return ""
	var caps: Dictionary = rules().get("hardpoint_capacity", {})
	if int(drone.get("hardpoints", 0)) <= 0:
		return "none"
	if not bool(drone.get("portable", true)):
		return String(caps.get("non_portable", "heavy"))
	if int(drone.get("encumbrance", 0)) <= int(caps.get("portable_max_enc_for_pistols", 3)):
		return "pistol"
	return String(caps.get("portable", "rifle"))


## A model's stats after a set of mods. Only mods whose effect is a stat delta are applied here;
## narrative fittings (cargo, optics, command decks) are presence flags, not numbers.
func with_mods(id: String, mod_ids: Array) -> Dictionary:
	var base := model(id).duplicate(true)
	if base.is_empty():
		return {}
	var delta := {"ac": 0, "move": 0, "encumbrance": 0, "fittings": 0, "hardpoints": 0, "hp_pct": 0}
	for mod_id in mod_ids:
		var mod: Dictionary = mods.get(String(mod_id), {})
		for key in delta:
			delta[key] += int(mod.get(key, 0))
	base["ac"] = int(base.get("ac", 0)) + delta["ac"]
	var portable := bool(base.get("portable", true))
	var move: Dictionary = base.get("move", {})
	move["rate"] = int(move.get("rate", 0)) + delta["move"]
	base["move"] = move
	if portable:
		base["encumbrance"] = int(base.get("encumbrance", 0)) + delta["encumbrance"]
	else:
		base["encumbrance"] = null
	base["fittings"] = int(base.get("fittings", 0)) + delta["fittings"]
	base["hardpoints"] = int(base.get("hardpoints", 0)) + delta["hardpoints"]
	# Bonuses are percentages of the unmodified base, rounded up.
	if delta["hp_pct"] != 0:
		base["hp"] = int(ceil(float(base.get("hp", 0)) * (1.0 + float(delta["hp_pct"]) / 100.0)))
	base["mods"] = mod_ids.duplicate()
	return base


## Cost of a fitting as a percentage of the model's base cost, rounded up.
func fitting_cost(id: String, fitting_name: String) -> int:
	var drone := model(id)
	var fitting: Dictionary = fittings.get(fitting_name, {})
	if drone.is_empty() or fitting.is_empty():
		return 0
	return int(ceil(float(drone.get("cost", 0)) * float(fitting.get("cost_pct", 0)) / 100.0))
