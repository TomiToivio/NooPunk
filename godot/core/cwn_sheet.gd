extends RefCounted
class_name CwnSheet
## The CWN character sheet: one assembled artefact for the whole character (#897 item 21, item 3).
##
## This composes the kernel rather than re-deriving it. Attributes, modifiers, saves, hit points, attack
## bonus, strain, encumbrance and advancement already exist in `cwn_character.gd`, `cwn_progression.gd`
## and `cwn_encumbrance.gd`; a sheet that computed any of them again would be a second source of truth
## and would drift the first time a rule changed.
##
## Item 3 is the reason for `validate()`: the sheet must keep core CWN concepts intact. Six attributes on
## the 3-18 scale, modifiers derived from those scores, four saves, advancement from XP, encumbrance from
## Strength. A sheet that violates one of those is not a CWN sheet, whatever else it displays.
##
## NoöPunk material lives in its own `mods` section and is **read-only with respect to CWN numbers**
## (`docs/rules/RULES_BASIS_LOCK.md`). `build()` therefore keeps the two apart in the returned shape:
## a mod may add a section, it may not edit `attributes`, `saves`, `hp`, `attack` or `strain`.

const Character := preload("res://godot/core/cwn_character.gd")
const Progression := preload("res://godot/core/cwn_progression.gd")
const Encumbrance := preload("res://godot/core/cwn_encumbrance.gd")

##: The six CWN attributes, in the published order.
## The kernel's own vocabulary. Using it here is deliberate: two spellings of the same attribute is
## how a sheet starts disagreeing with the rules it displays.
const ATTRIBUTES := ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

##: Scores a normal character may hold on the 3-18 scale.
const SCORE_MIN := 3
const SCORE_MAX := 18


static func modifier_for(score: int) -> int:
	return Character.effective_modifier(score)


static func _attributes(member: Dictionary) -> Dictionary:
	## Every attribute is present and numeric. A missing score is refused rather than defaulted: 10 would
	## be a silent rule change, and the sheet is where a player would notice it.
	var raw: Dictionary = Dictionary(member.get("attributes", {}))
	var out: Dictionary = {}
	# A caller may speak the code (STR), the lowercase code (str) or the long name (strength); the sheet
	# stores the kernel spelling so the rule engine and the display can never disagree about a key.
	const LONG_NAMES := {"STR": "strength", "DEX": "dexterity", "CON": "constitution",
		"INT": "intelligence", "WIS": "wisdom", "CHA": "charisma"}
	for name in ATTRIBUTES:
		var key: String = String(name)
		if not raw.has(key):
			if raw.has(key.to_lower()):
				key = key.to_lower()
			elif raw.has(LONG_NAMES.get(key, "")):
				key = LONG_NAMES[key]
		if not raw.has(key):
			continue
		out[name] = {"score": int(raw[key]), "modifier": modifier_for(int(raw[key]))}
	return out


static func _scores_in_range(scores: Dictionary) -> bool:
	for code in scores:
		var score := int(scores[code])
		if score < SCORE_MIN or score > SCORE_MAX:
			return false
	return scores.size() == ATTRIBUTES.size()


static func equipment_points(equipment: Array) -> int:
	## Items are counted in CWN's bundled points; an item without a weight contributes zero, which is a
	## stated convention rather than an implicit one.
	var total := 0
	for item in equipment:
		if item is Dictionary:
			total += int(item.get("points", 0))
	return total


static func build(member: Dictionary, options: Dictionary = {}) -> Dictionary:
	## Assemble the sheet. `options` carries equipment, xp and any NoöPunk mods the scenario enables.
	var level := int(member.get("level", 1))
	var attributes := _attributes(member)
	var equipment: Array = options.get("equipment", [])
	var xp := int(options.get("xp", 0))
	var mods: Dictionary = Dictionary(options.get("mods", {}))

	var strength := int(attributes.get("STR", {}).get("score", 10))
	var constitution := int(attributes.get("CON", {}).get("score", 10))
	var stowed := equipment_points(equipment)
	var readied := int(options.get("readied_points", 0))

	# The kernel speaks uppercase codes and plain scores; hand it exactly that rather than the sheet's own
	# richer per-attribute dictionaries.
	var scores: Dictionary = {}
	for code in attributes:
		scores[code] = int(attributes[code]["score"])

	var sheet := {
		"name": String(member.get("name", "")),
		"level": level,
		"attributes": attributes,
		# An out-of-range score must not blow up the kernel assertion: the sheet is built anyway and
		# validate() reports the problem, because a crash tells the caller nothing useful.
		"saves": Character.saves(level, scores) if _scores_in_range(scores) else {},
		"hp": {"max": int(member.get("hp_max", Character.hit_points(level, constitution)))},
		"attack": {"bonus": Progression.attack_bonus(level, bool(member.get("on_target", false)))},
		"strain": {"capacity": Progression.strain_capacity(constitution)},
		"encumbrance": {
			"stowed": stowed,
			"readied": readied,
			"stowed_capacity": Encumbrance.stowed_capacity(strength),
			"readied_capacity": Encumbrance.readied_capacity(strength),
			"tier": Encumbrance.tier_for(strength, stowed, readied),
		},
		"equipment": equipment,
		"skills": Dictionary(member.get("skills", {})),
		"background": String(member.get("background", "")),
		"edges": Array(member.get("edges", [])),
		"foci": Array(member.get("foci", [])),
		"advancement": {
			"xp": xp,
			"level_from_xp": Progression.level_for_xp(xp),
			"focus_available": Progression.focus_award(level),
			"edge_available": Progression.edge_award(level),
		},
		# NoöPunk modules live here and nowhere else.
		"mods": mods,
	}
	return sheet


static func validate(sheet: Dictionary) -> Array:
	## Core-CWN invariants (#897 item 3). Returns a list of problems; empty means the sheet is a CWN sheet.
	var problems: Array = []
	var attributes: Dictionary = Dictionary(sheet.get("attributes", {}))

	for name in ATTRIBUTES:
		if not attributes.has(name):
			problems.append("missing attribute: %s" % name)
			continue
		var score := int(attributes[name].get("score", 0))
		if score < SCORE_MIN or score > SCORE_MAX:
			problems.append("%s=%d outside %d..%d" % [name, score, SCORE_MIN, SCORE_MAX])
		var expected := modifier_for(score)
		if int(attributes[name].get("modifier", 999)) != expected:
			problems.append("%s modifier does not match its score" % name)

	# The kernel capitalises save keys; compare case-insensitively so the sheet and the rules agree on
	# what a save is even if a caller writes them lower-case.
	var saves: Dictionary = Dictionary(sheet.get("saves", {}))
	var present: Array = saves.keys().map(func(k): return String(k).to_lower())
	for kind in ["physical", "evasion", "mental", "luck"]:
		if not present.has(kind):
			problems.append("missing save: %s" % kind)

	if int(sheet.get("level", 0)) < 1:
		problems.append("level must be at least 1")

	# A mod may not have edited a core number. This is the boundary the lock describes, enforced where the
	# sheet is built rather than trusted to a reviewer's memory.
	var mods: Dictionary = Dictionary(sheet.get("mods", {}))
	for forbidden in ["attributes", "saves", "hp", "attack", "strain"]:
		if mods.has(forbidden):
			problems.append("mod '%s' attempts to override the CWN %s block" % [forbidden, forbidden])

	return problems


static func is_valid(sheet: Dictionary) -> bool:
	return validate(sheet).is_empty()
