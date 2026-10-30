## CWN cyberware systems (#848): the seven SRD tables as one mechanical contract.
##
## Values are transcribed from the CC0 CWN SRD (per-table URLs in `data/rules/cwn_cyberware.json`).
## The SRD prose describing what each implant does stays in the SRD; this class exposes the facts the
## game needs: cost, body type, concealment level, permanent System Strain, and the Major Injury rule
## that destroys every implant of a type in the injured limb or torso.
class_name CwnCyberware
extends RefCounted

const PATH := "res://data/rules/cwn_cyberware.json"
const TABLES := ["body", "head", "skin", "limb", "sensory", "medical", "nerve"]

var data: Dictionary = {}
var implants: Array = []
var _by_id: Dictionary = {}
var _by_type: Dictionary = {}


func _init(path: String = PATH) -> void:
	data = _load(path)
	implants = data.get("tables", [])
	for row in implants:
		_by_id[String(row.get("id", ""))] = row
		# Group by the SRD table, not the "Type" column: the medical table lists prosthetics whose
		# type is the body part replaced ("None"), while the injury rule keys on the table itself.
		var body_type := String(row.get("table", ""))
		if not _by_type.has(body_type):
			_by_type[body_type] = []
		_by_type[body_type].append(row)


func _load(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("cwn_cyberware: cannot open %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func all() -> Array:
	return implants


func implant(id: String) -> Dictionary:
	return _by_id.get(id, {})


func by_type(body_type: String) -> Array:
	return _by_type.get(body_type, [])


func table_names() -> Array:
	return TABLES


## Permanent System Strain of a set of implants. A null cost is not an error: the SRD prices two
## headware items "as cyber", so the record keeps the note instead of inventing a number.
func total_strain(ids: Array) -> float:
	var total := 0.0
	for id in ids:
		total += float(implant(String(id)).get("strain", 0.0))
	return total


func total_cost(ids: Array) -> Dictionary:
	var total := 0
	var unpriced: Array = []
	for id in ids:
		var row := implant(String(id))
		if row.is_empty():
			continue
		if row.get("cost") == null:
			unpriced.append(String(id))
		else:
			total += int(row["cost"])
	return {"cost": total, "unpriced": unpriced}


## A Major Injury destroys all cyberware of the affected type in the injured limb or torso. The
## caller supplies the type; the game applies the consequence.
func destroyed_by_major_injury(body_type: String) -> Array:
	var ids: Array = []
	for row in by_type(body_type):
		ids.append(String(row["id"]))
	return ids


func concealment_levels() -> Array:
	var levels: Array = []
	for row in implants:
		var level := String(row.get("concealment", ""))
		if not levels.has(level):
			levels.append(level)
	levels.sort()
	return levels
