class_name CWNCatalogue
extends RefCounted

## Source-faithful access to the CWN SRD catalogues for the Godot game.
##
## The data in `data/rules/cwn/srd_tables.json` is extracted from the CC0 SRD by
## `tools/extract_cwn_srd.py`; this class only reads it and normalises the columns. It never
## hard-codes a weapon, an armour line or a program: if the SRD gains a row and the extractor is
## re-run, the engine sees it. That is the difference between implementing a system and recalling
## one.
##
## Column names differ between SRD pages (`Dmg`, `Damage`, `Cost`, `Cost (Cr)`), so every accessor
## reads through `_cell()` with a list of accepted spellings rather than assuming one.

const DATA_PATH := "res://data/rules/cwn/srd_tables.json"

static var _cache: Dictionary = {}

static func _data() -> Dictionary:
	if _cache.is_empty():
		var file := FileAccess.open(DATA_PATH, FileAccess.READ)
		assert(file != null, "CWN SRD tables missing: run tools/extract_cwn_srd.py")
		var parsed: Variant = JSON.parse_string(file.get_as_text())
		file.close()
		assert(typeof(parsed) == TYPE_DICTIONARY, "CWN SRD tables are not a JSON object")
		_cache = parsed
	return _cache

static func tables() -> Dictionary:
	var explicit: Dictionary = _data().get("tables", {})
	if not explicit.is_empty():
		return explicit
	# The extractor stores flat arrays at the top level (`weapons`, `armor`, `cyberware`, ...).
	# Wrap them in the block shape rows() expects so lookups work against either layout instead of
	# silently returning nothing.
	var wrapped: Dictionary = {}
	for key in _data().keys():
		if _data()[key] is Array:
			wrapped[key] = [{"rows": _data()[key]}]
	return wrapped

static func licence() -> String:
	return str(_data().get("licence", ""))

static func source() -> String:
	return str(_data().get("source", ""))

## Every table stored under a catalogue key, flattened to rows. Keys match `PAGES` in the extractor.
static func rows(key: String) -> Array:
	var out: Array = []
	for block in tables().get(key, []):
		out.append_array(block.get("rows", []))
	return out

static func _row_label(row: Dictionary) -> String:
	# SRD tables head the first column with the table's own name ("Civilian Armor", "Firearm", ...),
	# so the row's first string value is its label. Falling back to it makes lookups work regardless
	# of what that header happens to be called.
	for column in row.keys():
		var value := str(row[column])
		if value.strip_edges() != "":
			return value.strip_edges()
	return ""

static func _cell(row: Dictionary, names: Array) -> String:
	for name in names:
		if row.has(name):
			return str(row[name]).strip_edges()
	# Case-insensitive fallback: the extractor preserves SRD capitalisation exactly.
	for column in row.keys():
		for name in names:
			if str(column).to_lower() == str(name).to_lower():
				return str(row[column]).strip_edges()
	return ""

static func _int(text: String, fallback: int = 0) -> int:
	var digits := ""
	for i in text.length():
		var ch := text[i]
		if ch >= "0" and ch <= "9":
			digits += ch
		elif digits != "":
			break
	return int(digits) if digits != "" else fallback

static func _money(text: String) -> int:
	return _int(text.replace(",", ""))

## "1d10+2" -> {"count": 1, "sides": 10, "bonus": 2}. "-" and "" mean no die.
static func parse_dice(text: String) -> Dictionary:
	var clean := text.strip_edges().to_lower().replace(" ", "")
	if clean == "" or clean == "-":
		return {"count": 0, "sides": 0, "bonus": 0}
	var bonus := 0
	var plus := clean.find("+")
	if plus >= 0:
		bonus = _int(clean.substr(plus + 1))
		clean = clean.substr(0, plus)
	var minus := clean.find("-")
	if minus > 0:
		bonus -= _int(clean.substr(minus + 1))
		clean = clean.substr(0, minus)
	var parts := clean.split("d")
	var count := 1
	if parts.size() == 2 and parts[0] != "":
		count = _int(parts[0], 1)
	var sides := _int(parts[parts.size() - 1]) if parts.size() > 0 else 0
	return {"count": count, "sides": sides, "bonus": bonus}

## "2/15" -> {"amount": 2, "max_ac": 15}; "5/-" means unconditional Shock.
static func parse_shock(text: String) -> Dictionary:
	var clean := text.strip_edges()
	if clean == "" or clean == "-":
		return {"amount": 0, "max_ac": -99}
	var parts := clean.split("/")
	var amount := _int(parts[0])
	if parts.size() < 2:
		return {"amount": amount, "max_ac": -99}
	var ac := parts[1].strip_edges()
	if ac == "-" or ac == "":
		return {"amount": amount, "max_ac": 99}
	return {"amount": amount, "max_ac": _int(ac)}

static func weapon(name: String, groups: Array = ["firearms", "melee", "heavy"]) -> Dictionary:
	for group in groups:
		for row in rows(group):
			if _cell(row, ["Firearm", "Weapon", "Name"]).to_lower() == name.to_lower():
				var damage_text := _cell(row, ["Dmg", "Damage"])
				var trauma_die := _cell(row, ["TD", "Trauma Die"])
				var trauma_rating := _cell(row, ["TR", "Trauma Rating", "Trauma"])
				return {
					"name": _cell(row, ["Firearm", "Weapon", "Name"]),
					"group": group,
					"damage": parse_dice(damage_text),
					"damage_text": damage_text,
					"range": _cell(row, ["Range"]),
					"cost": _money(_cell(row, ["Cost"])),
					"magazine": _int(_cell(row, ["Mag", "Magazine"])),
					"attribute": _cell(row, ["Attr.", "Attribute"]),
					"encumbrance": _int(_cell(row, ["Enc.", "Encumbrance"])),
					"trauma_die": parse_dice(trauma_die),
					"trauma_rating": _int(trauma_rating.replace("x", ""), 1),
					"shock": parse_shock(_cell(row, ["Shock"])),
					"notes": _cell(row, ["Notes", "Note"]),
				}
	return {}

static func armour(name: String) -> Dictionary:
	var wanted := name.to_lower()
	for row in rows("armor"):
		var label := _row_label(row).to_lower()
		var ident := str(row.get("id", "")).to_lower()
		# Exact id or name first; then a substring either way, so "leathers" finds "street_leathers".
		var hit: bool = label == wanted or ident == wanted
		if not hit and wanted != "":
			hit = label.contains(wanted) or ident.contains(wanted)
		if not hit:
			continue
		# The catalogue JSON carries typed numeric columns; the SRD tables carry text. Read the typed
		# value when present and fall back to the parsed cell otherwise.
		return {
			"name": _row_label(row) if label != "" else str(row.get("id", "")),
			"ranged_ac": int(row.get("ranged_ac", _int(_cell(row, ["Ranged AC"])))),
			"melee_ac": int(row.get("melee_ac", _int(_cell(row, ["Melee AC"])))),
			"soak": int(row.get("soak", _int(_cell(row, ["Damage Soak", "Soak"])))),
			"encumbrance": int(row.get("enc", _int(_cell(row, ["Enc.", "Encumbrance"])))),
			"trauma_mod": int(row.get("trauma_mod", _int(_cell(row, ["Trauma Target Mod", "Trauma Mod"])))),
			"subtle": bool(row.get("subtle", _cell(row, ["Subtle?"]).to_lower() == "subtle")),
			"cost": int(row.get("cost", _money(_cell(row, ["Cost"])))),
		}
	return {}

static func cyberdeck(name: String) -> Dictionary:
	for row in rows("cyberdecks"):
		if _cell(row, ["Deck", "Cyberdeck", "Name"]).to_lower() == name.to_lower():
			return {
				"name": _cell(row, ["Deck", "Cyberdeck", "Name"]),
				"cost": _money(_cell(row, ["Cost"])),
				"cpu": _int(_cell(row, ["CPU"])),
				"access": _int(_cell(row, ["Access"])),
				"weight": _cell(row, ["Enc.", "Weight", "Encumbrance"]),
			}
	return {}

static func program(verb: String) -> Dictionary:
	for row in rows("verbs"):
		if _cell(row, ["Verb", "Program", "Name"]).to_lower() == verb.to_lower():
			return {
				"name": _cell(row, ["Verb", "Program", "Name"]),
				"cost": _money(_cell(row, ["Cost"])),
				"target": _cell(row, ["Target"]),
				"access_cost": _int(_cell(row, ["Access Cost"])),
				"skill_mod": _int(_cell(row, ["Skill Check Mod", "Mod"])),
			}
	return {}

static func background(name: String) -> Dictionary:
	for entry in _data().get("backgrounds", []):
		if str(entry.get("name", "")).to_lower() == name.to_lower():
			return entry
	return {}

static func background_names() -> Array:
	var out: Array = []
	for entry in _data().get("backgrounds", []):
		out.append(str(entry.get("name", "")))
	return out

## Weapon names the engine can resolve, for UI lists and for tests that pin the catalogue.
static func weapon_names(group: String = "firearms") -> Array:
	var out: Array = []
	for row in rows(group):
		var name := _cell(row, ["Firearm", "Weapon", "Name"])
		if name != "":
			out.append(name)
	return out
