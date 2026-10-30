class_name CwnTags
extends RefCounted

## Typed tags for the NoöPunk customization (#821, child of #814).
##
## Everything a character has is a tag: attributes, skills, temporary statuses and permanent traits.
## The point of a *typed* model is that `Shoot-1` and `wounded-1` must never be confused: one is a
## skill at level 1, the other is a penalty. Storing them as bare strings with a trailing number makes
## that ambiguity unavoidable, so every tag carries its kind explicitly and the display string is
## derived, never parsed back as the source of truth.
##
## Human attribute range is -2..+2; above +2 is transhuman and is representable but never generated.
## Empathy -3 is below the human range and means the character is not a player character.
##
## **Numbers come from `NoopunkTags`** (and through it `data/rules/noopunk_tags.json`). This module
## keeps the formatting, parsing and status-stacking helpers; it does not hold a second copy of the
## bands, the skill names or the Empathy floor. Two modules agreeing by construction is worth more
## than two modules agreeing by review.

const TYPE_ATTRIBUTE := "attribute"
const TYPE_SKILL := "skill"
const TYPE_STATUS := "status"
const TYPE_TRAIT := "trait"

## The seven NoöPunk attributes, in sheet order.
const ATTRIBUTES := ["Fitness", "Cognition", "Awareness", "Agency", "Reflexes", "Cyber", "Empathy"]

## The three-band table from the draft: a 3d6 score becomes a modifier, and only the modifier is
## stored or shown. This is not to be replaced with another distribution.
const ATTRIBUTE_MIN_HUMAN := -2
const ATTRIBUTE_MAX_HUMAN := 2
const EMPATHY_INHUMAN := -3

const SKILL_MIN := 0
const SKILL_MAX := 4
const UNTRAINED_MODIFIER := -1

## Skill names and their default attributes, exactly as the draft specifies. `"attribute": ""` means
## the draft leaves the binding open (Talk is contextual; Know and Work are pending review) and the
## caller must supply one rather than this module inventing a default.
const SKILLS := {
	"Administer": "Cognition",
	"Connect": "Empathy",
	"Drive": "Reflexes",
	"Strength": "Fitness",
	"Stamina": "Fitness",
	"Hardware": "Cyber",
	"Wetware": "Empathy",
	"Software": "Cyber",
	"Noöware": "Empathy",
	"Research": "Cognition",
	"Know": "",
	"Lead": "Agency",
	"Notice": "Awareness",
	"Unarmed": "Reflexes",
	"Melee": "Reflexes",
	"Firearms": "Reflexes",
	"Sneak": "Awareness",
	"Survive": "Agency",
	"Talk": "",
	"Trade": "Agency",
	"Work": "",
}

## CWN skill names that map onto a NoöPunk name. Recorded so imported characters and old tests can be
## read without renaming anything silently in place.
const SKILL_ALIASES := {
	"Punch": "Unarmed",
	"Stab": "Melee",
	"Shoot": "Firearms",
	"Fix": "Hardware",
	"Heal": "Wetware",
	"Program": "Software",
	"Exert": "Strength",   # when raw muscular power is required; Stamina when endurance is
}

## The draft's conceptual mapping. Several old attributes feed more than one new tag, so this is a
## crosswalk for a *decision*, not a copy rule: migration must not duplicate one old value into every
## new attribute it touches.
const ATTRIBUTE_CROSSWALK := {
	"WIS": ["Agency", "Empathy", "Awareness"],
	"STR": ["Fitness"],
	"CON": ["Fitness"],
	"DEX": ["Reflexes"],
	"INT": ["Cognition", "Cyber"],
	"CHA": ["Empathy", "Awareness", "Agency"],
}

## 3d6 -> attribute tag value. Bands are exact; anything outside 3..18 is not a generated human score.
static func attribute_value_for_3d6(total: int) -> int:
	if total < 3 or total > 18:
		return 0
	# The band table lives in the contract; this delegates so the two implementations cannot drift.
	return NoopunkTags.modifier_for_score(total)

## Build a tag. `kind` is one of the TYPE_* constants; the value's legality depends on the kind.
static func make(kind: String, name: String, value: int, extra: Dictionary = {}) -> Dictionary:
	var tag := {"type": kind, "name": name, "value": value}
	tag.merge(extra.duplicate(true), true)
	return tag

static func is_human_attribute(tag: Dictionary) -> bool:
	if tag.get("type") != TYPE_ATTRIBUTE:
		return false
	var value := int(tag.get("value", 0))
	return value >= ATTRIBUTE_MIN_HUMAN and value <= ATTRIBUTE_MAX_HUMAN

## A character with Empathy -3 is no longer human and is not eligible as a player character. This is
## a rule, so it is a function rather than a note: the sheet, the creator and the save loader all ask
## the same question instead of re-deciding it.
static func is_player_character_eligible(tags: Array) -> bool:
	for tag in tags:
		if tag.get("type") == TYPE_ATTRIBUTE and str(tag.get("name", "")) == "Empathy":
			return int(tag.get("value", 0)) > NoopunkTags.empathy_floor()
	return true

## Display syntax. Attributes and statuses carry a sign, skills do not (a skill is a level, not a
## bonus): `Fitness-2`, `Agency+1`, `Shoot-1`, `wounded-1`.
static func format(tag: Dictionary) -> String:
	var kind := str(tag.get("type", ""))
	var name := str(tag.get("name", ""))
	var value := int(tag.get("value", 0))
	if kind == TYPE_SKILL:
		return "%s-%d" % [name, value]
	if kind == TYPE_ATTRIBUTE:
		return "%s%s%d" % [name, "+" if value >= 0 else "", value]
	if kind == TYPE_STATUS:
		return "%s%s%d" % [name, "+" if value >= 0 else "", value]
	return "%s%s%d" % [name, "+" if value >= 0 else "", value]

## Parse a display string back into a tag. The kind is a required argument rather than a guess:
## `wounded-1` and `Shoot-1` are indistinguishable as text, which is the whole reason the model is
## typed. Returns {} when the text does not match the expected shape.
static func parse(text: String, kind: String) -> Dictionary:
	var pattern := "^(?<name>.+?)(?<value>[+-]?\\d+)$" if kind != TYPE_SKILL else "^(?<name>.+?)-(?<value>\\d+)$"
	var regex := RegEx.new()
	if regex.compile(pattern) != OK:
		return {}
	var found := regex.search(text.strip_edges())
	if found == null:
		return {}
	var name := found.get_string("name").strip_edges()
	var value := int(found.get_string("value"))
	if name.is_empty():
		return {}
	if kind == TYPE_SKILL and (value < SKILL_MIN or value > SKILL_MAX):
		return {}
	return make(kind, name, value)

## Every attribute tag for a rolled set of seven 3d6 scores, in sheet order.
static func attributes_from_rolls(rolls: Array) -> Array:
	if rolls.size() != ATTRIBUTES.size():
		return []
	var tags: Array = []
	for index in ATTRIBUTES.size():
		tags.append(make(TYPE_ATTRIBUTE, ATTRIBUTES[index], attribute_value_for_3d6(int(rolls[index]))))
	return tags

## Apply a temporary status. Stacking is explicit: `stacking` of "replace" keeps the stronger
## magnitude, "add" sums, and "exclusive:<group>" drops the other members of that group first. The
## draft leaves the catalogue open, so this models the mechanics and invents no status list.
static func apply_status(tags: Array, incoming: Dictionary) -> Array:
	var out: Array = []
	var merged := false
	var group := str(incoming.get("exclusive_group", ""))
	for tag in tags:
		if tag.get("type") != TYPE_STATUS:
			out.append(tag)
			continue
		if str(tag.get("name", "")) == str(incoming.get("name", "")):
			merged = true
			match str(incoming.get("stacking", "replace")):
				"add":
					out.append(make(TYPE_STATUS, str(incoming["name"]),
						int(tag.get("value", 0)) + int(incoming.get("value", 0)),
						{"temporary": true, "duration": incoming.get("duration", 0)}))
				_:
					# Replace keeps the stronger magnitude: a worse wounded-2 is not cancelled by a
					# later wounded-1, and a milder one does not erase it either.
					var kept: Dictionary = tag
					if absi(int(incoming.get("value", 0))) > absi(int(tag.get("value", 0))):
						kept = incoming
					out.append(kept)
			continue
		if group != "" and str(tag.get("exclusive_group", "")) == group:
			continue
		out.append(tag)
	if not merged:
		out.append(incoming)
	return out

## Expire temporary statuses after a turn/round count. Permanent traits never expire.
static func tick_statuses(tags: Array, elapsed: int = 1) -> Array:
	var out: Array = []
	for tag in tags:
		if tag.get("type") == TYPE_STATUS and bool(tag.get("temporary", false)):
			var remaining := int(tag.get("duration", 0)) - elapsed
			if remaining > 0:
				var next: Dictionary = tag.duplicate(true)
				next["duration"] = remaining
				out.append(next)
			continue
		out.append(tag)
	return out

## Total modifier contributed by tags of a kind, for a named tag (sum across duplicates).
static func total_for(tags: Array, kind: String, name: String) -> int:
	var total := 0
	for tag in tags:
		if tag.get("type") == kind and str(tag.get("name", "")) == name:
			total += int(tag.get("value", 0))
	return total
