## CWN catalogue procedures (#749): weapons, armour, cyberware strain, and the program
## Verb/Subject catalogue. Values come from data/rules/cwn_catalogue.json, transcribed from the
## CWN SRD tables (per-file `_source`). This class implements the *procedures* the tables feed:
## range bands, burst fire, ammo, trauma, shock, soak, strain totals and verb/subject legality.
class_name CwnCatalogue
extends RefCounted

const PATH := "res://data/rules/cwn_catalogue.json"
const DEFAULT_TRAUMA_TARGET := 6

var data: Dictionary = {}
var weapons: Dictionary = {}
var armor: Dictionary = {}
var cyberware: Dictionary = {}
var verbs: Dictionary = {}
var subjects: Dictionary = {}


func _init(path: String = PATH) -> void:
	data = _load(path)
	for row in data.get("weapons", []):
		weapons[String(row["id"])] = row
	for row in data.get("armor", []):
		armor[String(row["id"])] = row
	for row in data.get("cyberware", []):
		cyberware[String(row["id"])] = row
	for row in data.get("verbs", []):
		verbs[String(row["id"])] = row
	for row in data.get("subjects", []):
		subjects[String(row["id"])] = row


func _load(path: String) -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return parsed if parsed is Dictionary else {}


func weapon(id: String) -> Dictionary:
	return weapons.get(id, {})


func armor_piece(id: String) -> Dictionary:
	return armor.get(id, {})


func implant(id: String) -> Dictionary:
	return cyberware.get(id, {})


func verb(id: String) -> Dictionary:
	return verbs.get(id, {})


func subject(id: String) -> Dictionary:
	return subjects.get(id, {})


## -2 beyond normal range, and illegal beyond extreme range. Melee-only weapons have no bands.
func range_penalty(weapon_id: String, distance_metres: float) -> Dictionary:
	var w := weapon(weapon_id)
	if w.is_empty():
		return {"ok": false, "reason": "no_such_weapon"}
	var band: Variant = w.get("range")
	if band == null:
		return {"ok": distance_metres <= 1.0, "penalty": 0, "reason": "" if distance_metres <= 1.0 else "out_of_reach"}
	var normal := float(band[0])
	var extreme := float(band[1])
	if distance_metres <= normal:
		return {"ok": true, "penalty": 0}
	if distance_metres <= extreme:
		return {"ok": true, "penalty": -2}
	return {"ok": false, "penalty": 0, "reason": "beyond_extreme"}


func damage_spec(weapon_id: String) -> String:
	return String(weapon(weapon_id).get("dmg", "1d2"))


func roll_damage(weapon_id: String, attribute_modifier: int, dice: Object) -> int:
	var total := attribute_modifier
	var spec := damage_spec(weapon_id)
	for part in spec.split("+"):
		var token := part.strip_edges()
		if token == "":
			continue
		if token.contains("d"):
			var bits := token.split("d")
			var count := int(bits[0]) if bits[0] != "" else 1
			var sides := int(bits[1]) if bits.size() > 1 else 6
			for _i in count:
				total += int(dice.roll(sides)) if dice != null else 1
		else:
			total += int(token)
	return maxi(0, total)


## Weapon damage reduced by the armour's Damage Soak, never below zero.
func apply_soak(armor_id: String, damage: int) -> int:
	return maxi(0, damage - int(armor_piece(armor_id).get("soak", 0)))


## Shock applies on a miss when the target's melee AC is at or below the Shock AC.
func shock_damage(weapon_id: String, target_melee_ac: int, attribute_modifier: int) -> int:
	var shock: Variant = weapon(weapon_id).get("shock")
	if shock == null:
		return 0
	if target_melee_ac > int(shock["ac"]):
		return 0
	return maxi(0, int(shock["damage"]) + attribute_modifier)


## Trauma: roll the Trauma Die; >= (6 + armour trauma modifier) is a Traumatic Hit, and the
## weapon's Trauma Rating multiplies the damage. Non-lethal weapons roll no Trauma Die.
func trauma(weapon_id: String, dice: Object, armor_id: String = "") -> Dictionary:
	var w := weapon(weapon_id)
	var die_spec: Variant = w.get("trauma_die")
	if die_spec == null:
		return {"traumatic": false, "roll": 0, "rating": null, "reason": "nonlethal"}
	var target := DEFAULT_TRAUMA_TARGET + int(armor_piece(armor_id).get("trauma_mod", 0))
	var roll := 0
	var spec := String(die_spec)
	for part in spec.split("+"):
		var token := part.strip_edges()
		if token == "":
			continue
		if token.contains("d"):
			var bits := token.split("d")
			var count := int(bits[0]) if bits[0] != "" else 1
			var sides := int(bits[1]) if bits.size() > 1 else 6
			for _i in count:
				roll += int(dice.roll(sides)) if dice != null else 1
		else:
			roll += int(token)
	return {
		"traumatic": roll >= target, "roll": roll, "target": target,
		"rating": int(w.get("trauma_rating", 1)),
	}


## Full attack: range band, burst fire (+2 hit and damage), then the kernel's d20 resolution.
func attack(
	adapter: Object,
	weapon_id: String,
	attacker_attribute_score: int,
	attacker_level: int,
	target_ac: int,
	distance_metres: float,
	dice: Object,
	burst: bool = false,
) -> Dictionary:
	var band := range_penalty(weapon_id, distance_metres)
	if not bool(band.get("ok", false)):
		return {"ok": false, "reason": String(band.get("reason", "out_of_range"))}
	var w := weapon(weapon_id)
	if burst and not (w.get("tags", []) as Array).has("burst"):
		return {"ok": false, "reason": "weapon_cannot_burst"}
	var modifier := int(band.get("penalty", 0)) + (2 if burst else 0)
	var attr_modifier := int(adapter.attribute_modifier(int(attacker_attribute_score)))
	var roll: Dictionary = adapter.attack_roll(
		int(attacker_attribute_score), 1, int(attacker_level), target_ac, modifier
	)
	var result := {
		"ok": true, "hit": bool(roll.get("hit", false)), "roll": roll,
		"modifier": modifier, "burst": burst, "weapon": weapon_id,
	}
	if bool(result["hit"]):
		result["damage"] = roll_damage(weapon_id, attr_modifier, dice) + (2 if burst else 0)
	elif w.get("shock") != null:
		result["shock"] = shock_damage(weapon_id, target_ac, attr_modifier)
	return result


## Ammo: one round per attack, three for a burst; a reload is a Main Action by default.
func fire(state: Dictionary, weapon_id: String, burst: bool = false) -> Dictionary:
	var w := weapon(weapon_id)
	if w.get("mag") == null:
		return {"ok": true, "state": state, "rounds": null}
	var cost := 3 if burst else 1
	var rounds := int(state.get("rounds", int(w["mag"])))
	if rounds < cost:
		return {"ok": false, "reason": "empty", "state": state}
	return {"ok": true, "state": {"rounds": rounds - cost}, "rounds": rounds - cost}


func reload(weapon_id: String) -> Dictionary:
	var w := weapon(weapon_id)
	if w.get("mag") == null:
		return {"ok": false, "reason": "not_a_firearm"}
	return {"ok": true, "state": {"rounds": int(w["mag"])}, "rounds": int(w["mag"]), "action": "main"}


## Cyberware strain: permanent, fractional values allowed, and the baseline implant can ignore
## strain up to 12 - Constitution.
func strain_total(implant_ids: Array) -> float:
	var total := 0.0
	for id in implant_ids:
		total += float(implant(id).get("strain", 0.0))
	return total


func strain_with_baseline(implant_ids: Array, constitution: int) -> Dictionary:
	var total := strain_total(implant_ids)
	var ignored := 0.0
	if implant_ids.has("cybernetic_baseline"):
		ignored = float(maxi(0, 12 - int(constitution)))
	return {
		"raw": total, "ignored": ignored, "effective": maxf(0.0, total - ignored),
		"maximum": int(constitution), "over": maxf(0.0, total - ignored - float(constitution)),
	}


## Verb/Subject legality: every Verb lists the Subject types it can run against.
func can_pair(verb_id: String, subject_id: String) -> bool:
	var v := verb(verb_id)
	var s := subject(subject_id)
	if v.is_empty() or s.is_empty():
		return false
	return (v.get("targets", []) as Array).has(String(s.get("type", "")))


func program_cost(verb_id: String, subject_id: String) -> Dictionary:
	if not can_pair(verb_id, subject_id):
		return {"legal": false, "reason": "invalid_target"}
	var v := verb(verb_id)
	return {
		"legal": true,
		"access": int(v.get("access", 0)),
		"check_modifier": int(v.get("modifier", 0)),
		"self_terminating": bool(v.get("self_terminating", false)),
		"difficulty_modifier": int(subject(subject_id).get("difficulty_modifier", 0)),
	}

## --- SRD-extracted catalogue access, merged from the compatibility tree (#791) ----------------
## The instance API above reads the curated `data/rules/cwn_catalogue.json`. This static API reads
## `data/rules/cwn/srd_tables.json`, produced by `tools/extract_cwn_srd.py` from the CC0 SRD, so the
## game can see every catalogue row the source publishes rather than only the curated subset.
## One module, two data sources by design: the curated file is hand-checked content, the extracted
## file is completeness, and neither is a second implementation of a rule.
const SRD_PATH := "res://data/rules/cwn/srd_tables.json"
static var _srd_cache: Dictionary = {}

static func srd_data() -> Dictionary:
	if _srd_cache.is_empty():
		if not FileAccess.file_exists(SRD_PATH):
			push_error("CwnCatalogue: missing SRD tables at %s" % SRD_PATH)
			return {}
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SRD_PATH))
		_srd_cache = parsed if typeof(parsed) == TYPE_DICTIONARY else {}
	return _srd_cache

static func srd_licence() -> String:
	return str(srd_data().get("licence", ""))

static func srd_rows(key: String) -> Array:
	var out: Array = []
	for block in srd_data().get("tables", {}).get(key, []):
		out.append_array(block.get("rows", []))
	return out

static func _srd_cell(row: Dictionary, names: Array) -> String:
	for name in names:
		if row.has(name):
			return str(row[name]).strip_edges()
	for column in row.keys():
		for name in names:
			if str(column).to_lower() == str(name).to_lower():
				return str(row[column]).strip_edges()
	return ""

static func _srd_int(text: String, fallback: int = 0) -> int:
	var digits := ""
	for ch in text:
		if ch >= "0" and ch <= "9":
			digits += ch
		elif digits != "":
			break
	return int(digits) if digits != "" else fallback

## "1d10+2" -> {"count": 1, "sides": 10, "bonus": 2}
static func parse_dice(text: String) -> Dictionary:
	var clean := text.strip_edges().to_lower().replace(" ", "")
	if clean == "" or clean == "-":
		return {"count": 0, "sides": 0, "bonus": 0}
	var bonus := 0
	var plus := clean.find("+")
	if plus >= 0:
		bonus = _srd_int(clean.substr(plus + 1))
		clean = clean.substr(0, plus)
	var parts := clean.split("d")
	var count := 1 if parts.size() != 2 or parts[0] == "" else _srd_int(parts[0], 1)
	var sides := _srd_int(parts[parts.size() - 1]) if parts.size() > 0 else 0
	return {"count": count, "sides": sides, "bonus": bonus}

## "2/15" -> {"amount": 2, "max_ac": 15}; "5/-" is unconditional (max_ac 99)
static func parse_shock(text: String) -> Dictionary:
	var clean := text.strip_edges()
	if clean == "" or clean == "-":
		return {"amount": 0, "max_ac": -99}
	var parts := clean.split("/")
	var amount := _srd_int(parts[0])
	if parts.size() < 2:
		return {"amount": amount, "max_ac": -99}
	var ac := parts[1].strip_edges()
	return {"amount": amount, "max_ac": 99 if ac == "-" or ac == "" else _srd_int(ac)}

static func srd_weapon(name: String, groups: Array = ["firearms", "melee", "heavy"]) -> Dictionary:
	for group in groups:
		for row in srd_rows(group):
			var candidate := _srd_cell(row, ["Firearm", "Weapon", "Name"])
			if candidate == "":
				for key in row.keys():
					candidate = str(row[key]).strip_edges()
					break
			if candidate.to_lower() != name.to_lower():
				continue
			return {
				"name": candidate,
				"group": group,
				"damage_text": _srd_cell(row, ["Dmg", "Damage"]),
				"damage": parse_dice(_srd_cell(row, ["Dmg", "Damage"])),
				"range": _srd_cell(row, ["Range"]),
				"cost": _srd_int(_srd_cell(row, ["Cost"]).replace(",", "")),
				"magazine": _srd_int(_srd_cell(row, ["Mag", "Magazine"])),
				"attribute": _srd_cell(row, ["Attr.", "Attribute"]),
				"encumbrance": _srd_int(_srd_cell(row, ["Enc.", "Encumbrance"])),
				"trauma_die": parse_dice(_srd_cell(row, ["TD", "Trauma Die"])),
				"trauma_rating": _srd_int(_srd_cell(row, ["TR", "Trauma Rating"]).replace("x", ""), 1),
				"shock": parse_shock(_srd_cell(row, ["Shock"])),
			}
	return {}

static func srd_armour(name: String) -> Dictionary:
	for row in srd_rows("armor"):
		var candidate := _srd_cell(row, ["Armor", "Armour", "Name"])
		if candidate == "":
			for key in row.keys():
				candidate = str(row[key]).strip_edges()
				break
		if candidate.to_lower() != name.to_lower():
			continue
		return {
			"name": candidate,
			"ranged_ac": _srd_int(_srd_cell(row, ["Ranged AC"])),
			"melee_ac": _srd_int(_srd_cell(row, ["Melee AC"])),
			"soak": _srd_int(_srd_cell(row, ["Damage Soak", "Soak"])),
			"encumbrance": _srd_int(_srd_cell(row, ["Enc.", "Encumbrance"])),
			"trauma_mod": _srd_int(_srd_cell(row, ["Trauma Target Mod", "Trauma Mod"])),
			"cost": _srd_int(_srd_cell(row, ["Cost"]).replace(",", "")),
		}
	return {}

static func srd_background_names() -> Array:
	var out: Array = []
	for entry in srd_data().get("backgrounds", []):
		out.append(str(entry.get("name", "")))
	return out

static func srd_background(name: String) -> Dictionary:
	for entry in srd_data().get("backgrounds", []):
		if str(entry.get("name", "")).to_lower() == name.to_lower():
			return entry
	return {}
