## NoöPunk's tag-based attributes, skills and statuses (#821).
##
## Port of `src/rules/noopunk_tags.py`; every number comes from `data/rules/noopunk_tags.json`, which
## `tests/test_noopunk_tags_contract.py` pins to the Python layer of record. CWN/SWN supply the 3d6
## chassis and the 0-4 skill scale — the seven attributes, their meanings and the skill names are
## NoöPunk's own.
##
## What binds here:
##
## * **Everything is a typed tag.** Attributes, skills, statuses and traits share one record with an
##   explicit `kind` and `sign`, so `Shoot-1` (skill rank 1) is never read as a penalty.
## * **Only the modifier is stored.** Generation rolls 3d6 and keeps the band value; the raw score
##   never reaches a sheet.
## * **The bands are the draft's**: 3 -> -2, 4-7 -> -1, 8-13 -> 0, 14-17 -> +1, 18 -> +2.
## * **Empathy -3 is not human and not a player character**, and the generator cannot produce it.
##
## Undecided in the draft and therefore not decided here: which skills are impossible untrained, the
## Connect design, remaining Know/Work uses, alignment thresholds, and character migration. The
## contract's `open_questions` list carries them.
extends RefCounted
class_name NoopunkTags

const CONTRACT_PATH := "res://data/rules/noopunk_tags.json"

static var _contract: Dictionary = {}

static func contract() -> Dictionary:
	if _contract.is_empty() and FileAccess.file_exists(CONTRACT_PATH):
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CONTRACT_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_contract = parsed
	return _contract

static func attributes() -> Array:
	return contract().get("attributes", {}).get("order", [])

static func human_min() -> int:
	return int(contract().get("attributes", {}).get("human_range", [-2, 2])[0])

static func human_max() -> int:
	return int(contract().get("attributes", {}).get("human_range", [-2, 2])[1])

static func store_min() -> int:
	return int(contract().get("attributes", {}).get("storage_range", {}).get("min", -3))

static func store_max() -> int:
	return int(contract().get("attributes", {}).get("storage_range", {}).get("max", 6))

static func empathy_floor() -> int:
	return int(contract().get("attributes", {}).get("empathy_floor", {}).get("value", -3))

static func untrained_penalty() -> int:
	return int(contract().get("skills", {}).get("untrained", {}).get("penalty", -1))

static func skill_names() -> Array:
	return contract().get("skills", {}).get("list", {}).keys()

## The draft's 3d6 bands, as inclusive lower bounds: the last band at or below the score wins.
static func modifier_for_score(score: int) -> int:
	if score < 3 or score > 18:
		return 0
	var value := -2
	for band in contract().get("attributes", {}).get("generation", {}).get("bands", []):
		if score >= int(band[0]):
			value = int(band[1])
	return value

## A typed tag. `display()` is the sheet syntax, and `kind`/`sign` keep the two meanings apart.
class Tag extends RefCounted:
	var kind: String = "attribute"
	var name: String = ""
	var value: int = 0
	var sign: String = "+"
	var duration: String = "permanent"
	var source: String = ""
	var stacking: String = "replace"
	var exclusive_with: Array = []

	func _init(tag_kind: String = "attribute", tag_name: String = "", tag_value: int = 0,
			tag_sign: String = "+", tag_duration: String = "permanent", tag_source: String = "",
			tag_stacking: String = "replace", tag_exclusive: Array = []) -> void:
		kind = tag_kind
		name = tag_name
		value = tag_value
		sign = tag_sign
		duration = tag_duration
		source = tag_source
		stacking = tag_stacking
		exclusive_with = tag_exclusive.duplicate()

	func display() -> String:
		match kind:
			"trait":
				return name
			"attribute":
				return "%s%s%d" % [name, sign, absi(value)]
			_:
				return "%s-%d" % [name, value]

	func to_dict() -> Dictionary:
		return {"kind": kind, "name": name, "value": value, "sign": sign,
			"duration": duration, "source": source, "stacking": stacking,
			"exclusive_with": exclusive_with.duplicate()}

	static func from_dict(data: Dictionary) -> Tag:
		return Tag.new(String(data.get("kind", "attribute")), String(data.get("name", "")),
			int(data.get("value", 0)), String(data.get("sign", "+")),
			String(data.get("duration", "permanent")), String(data.get("source", "")),
			String(data.get("stacking", "replace")), data.get("exclusive_with", []))

static func attribute_tag(attribute_name: String, value: int) -> Tag:
	return Tag.new("attribute", attribute_name, value, "+" if value >= 0 else "-")

static func skill_tag(skill_name: String, rank: int) -> Tag:
	return Tag.new("skill", skill_name, rank, "+")

static func status_tag(status_name: String, penalty: int, tag_duration: String = "scene",
		tag_source: String = "", tag_stacking: String = "highest", tag_exclusive: Array = []) -> Tag:
	return Tag.new("status", status_name, absi(penalty), "-", tag_duration, tag_source,
		tag_stacking, tag_exclusive)

## The sheet: seven attribute tags plus skill, status and trait tags, serialisable as one record.
class Sheet extends RefCounted:
	var attributes: Dictionary = {}
	var skills: Dictionary = {}
	var statuses: Array = []
	var traits: Array = []

	func _init(attribute_values: Dictionary = {}, skill_ranks: Dictionary = {}) -> void:
		for name in NoopunkTags.attributes():
			attributes[String(name)] = int(attribute_values.get(name, 0))
		for name in attribute_values.keys():
			if not attributes.has(String(name)):
				attributes[String(name)] = int(attribute_values[name])
		skills = skill_ranks.duplicate()

	## Why the sheet is illegal, or "" when it is.
	func validate() -> String:
		for name in attributes.keys():
			var value := int(attributes[name])
			if value < NoopunkTags.store_min() or value > NoopunkTags.store_max():
				return "%s_%d_outside_the_storable_range" % [name, value]
		for name in skills.keys():
			var rank := int(skills[name])
			if not NoopunkTags.skill_names().has(String(name)):
				return "unknown_skill_%s" % name
			if rank < 0 or rank > 4:
				return "skill_rank_outside_0_4"
		return ""

	func empathy() -> int:
		return int(attributes.get("Empathy", 0))

	## Empathy -3 is outside the human range: no longer human.
	func is_human() -> bool:
		return empathy() > NoopunkTags.empathy_floor()

	func pc_eligible() -> bool:
		return is_human()

	## Any tag above the human baseline. The draft sets no ceiling and no further rule.
	func is_transhuman() -> bool:
		for name in attributes.keys():
			if int(attributes[name]) > NoopunkTags.human_max():
				return true
		return false

	func tags() -> Array:
		var out: Array = []
		for name in attributes.keys():
			out.append(NoopunkTags.attribute_tag(String(name), int(attributes[name])))
		for name in skills.keys():
			out.append(NoopunkTags.skill_tag(String(name), int(skills[name])))
		out.append_array(statuses)
		out.append_array(traits)
		return out

	func sheet_lines() -> Array:
		var lines: Array = []
		for tag in tags():
			lines.append(tag.display())
		lines.sort()
		return lines

	func attribute(attribute_name: String) -> int:
		return int(attributes.get(attribute_name, 0))

	func skill_rank(skill_name: String) -> int:
		return int(skills.get(skill_name, NoopunkTags.untrained_penalty()))

	## Summed status penalty, honouring stacking. One mode governs one status name: the mode of the
	## newest tag for that name, so mixing modes is never ambiguous.
	func status_penalty() -> int:
		var grouped: Dictionary = {}
		for tag in statuses:
			if not grouped.has(tag.name):
				grouped[tag.name] = []
			grouped[tag.name].append(tag)
		var total := 0
		for status_name in grouped.keys():
			var tags: Array = grouped[status_name]
			var mode := String(tags[tags.size() - 1].stacking)
			match mode:
				"stack":
					for tag in tags:
						total += int(tag.value)
				"highest":
					var best := 0
					for tag in tags:
						best = maxi(best, int(tag.value))
					total += best
				_:
					total += int(tags[tags.size() - 1].value)
		return total

	func add_status(tag) -> void:
		for other in statuses:
			if tag.exclusive_with.has(other.name) or other.exclusive_with.has(tag.name):
				statuses.erase(other)
		statuses.append(tag)

	## Drop the statuses whose duration ran out. Permanent tags never expire.
	func expire(tag_duration: String) -> Array:
		if tag_duration == "permanent":
			return []
		var gone: Array = []
		var kept: Array = []
		for tag in statuses:
			if String(tag.duration) == tag_duration:
				gone.append(tag)
			else:
				kept.append(tag)
		statuses = kept
		return gone

	## 2d6 + attribute tag + skill rank + situational, against a difficulty. An untrained action uses
	## the draft's untrained penalty; a skill the draft marks impossible without training refuses.
	func check(attribute_name: String, skill_name: String, roll: int, difficulty: int = 8,
			situational: int = 0) -> Dictionary:
		if roll < 2 or roll > 12:
			return {"ok": false, "reason": "a_2d6_check_is_2_12"}
		var entry: Dictionary = NoopunkTags.contract().get("skills", {}).get("list", {}).get(skill_name, {})
		if entry.is_empty():
			return {"ok": false, "reason": "unknown_skill", "skill": skill_name}
		if String(entry.get("attribute", "")) == "contextual" \
				and not (entry.get("attribute_options", []) as Array).has(attribute_name):
			return {"ok": false, "reason": "contextual_skill_wrong_attribute", "skill": skill_name}
		var impossible: Array = NoopunkTags.contract().get("skills", {}).get("untrained", {}).get("impossible_without", [])
		if not skills.has(skill_name) and impossible.has(skill_name):
			return {"ok": false, "reason": "trained_only", "skill": skill_name}
		var rank := skill_rank(skill_name)
		var total := roll + attribute(attribute_name) + rank + situational - status_penalty()
		return {"ok": true, "total": total, "success": total >= difficulty,
			"difficulty": difficulty, "rank": rank, "attribute_value": attribute(attribute_name)}

	func to_dict() -> Dictionary:
		var status_dicts: Array = []
		for tag in statuses:
			status_dicts.append(tag.to_dict())
		var trait_dicts: Array = []
		for tag in traits:
			trait_dicts.append(tag.to_dict())
		return {"attributes": attributes.duplicate(true), "skills": skills.duplicate(true),
			"statuses": status_dicts, "traits": trait_dicts}

	static func from_dict(data: Dictionary) -> Sheet:
		var sheet := Sheet.new(Dictionary(data.get("attributes", {})), Dictionary(data.get("skills", {})))
		for entry in data.get("statuses", []):
			sheet.statuses.append(Tag.from_dict(entry))
		for entry in data.get("traits", []):
			sheet.traits.append(Tag.from_dict(entry))
		return sheet
