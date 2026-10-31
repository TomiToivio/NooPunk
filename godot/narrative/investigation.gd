## Investigation notebook and clue graph (#897 §4, GUMSHOE-inspired).
##
## The rule that shapes everything: **an essential clue is never gated behind a single failed roll.** In an
## investigative game a missed essential clue stops the story, and no amount of good roleplay recovers it.
## So a failed check on an essential clue costs time, attention or a complication — not the clue.
##
## Non-essential clues do gate on the roll, and may be missed. The notebook records what was found, what
## it contradicts, and what it opens, so the player can assemble the case instead of being told it.
extends RefCounted
class_name NoopunkInvestigation

##: clue id -> {essential: bool, requires: Array[flag], opens: Array[location id], contradicts: Array}
var clues: Dictionary = {}
var found: Array = []
var contradictions: Array = []
var leads: Array = []


static func from_data(data: Dictionary) -> NoopunkInvestigation:
	var notebook := NoopunkInvestigation.new()
	for entry in Array(data.get("clues", [])):
		var clue: Dictionary = entry
		notebook.clues[String(clue.get("id", ""))] = clue
	return notebook


## Attempt to gather a clue.
##
## `success` is the outcome of whatever check the core resolved — this module never rolls. An essential
## clue is granted even on failure, and the result says so plainly, because a silent grant would look like
## the check did not matter.
func gather(clue_id: String, success: bool, flags: Dictionary = {}) -> Dictionary:
	if not clues.has(clue_id):
		return {"ok": false, "reason": "unknown_clue"}
	if found.has(clue_id):
		return {"ok": false, "reason": "already_found"}
	var clue: Dictionary = clues[clue_id]
	for flag in Array(clue.get("requires", [])):
		if not bool(flags.get(String(flag), false)):
			return {"ok": false, "reason": "requirements_not_met", "flag": String(flag)}
	var essential := bool(clue.get("essential", false))
	if not success and not essential:
		return {"ok": true, "found": false, "reason": "missed",
			"essential": false, "clue": clue_id}
	found.append(clue_id)
	for other in Array(clue.get("contradicts", [])):
		if not contradictions.has(String(other)):
			contradictions.append(String(other))
	for location in Array(clue.get("opens", [])):
		if not leads.has(String(location)):
			leads.append(String(location))
	return {
		"ok": true,
		"found": true,
		"essential": essential,
		# A failed roll on an essential clue is not free: the caller owes a complication.
		"owes_complication": essential and not success,
		"clue": clue_id,
		"contradicts": Array(clue.get("contradicts", [])),
		"opens": Array(clue.get("opens", [])),
	}


func has(clue_id: String) -> bool:
	return found.has(clue_id)


func count() -> int:
	return found.size()


## Leads are locations a found clue has opened. Kept as a list, not a set, so ordering is stable in UI.
func open_leads() -> Array:
	return leads.duplicate()


func contradicted() -> Array:
	return contradictions.duplicate()


## Whether the case can be closed: every essential clue found. Non-essential clues are optional by design.
func can_conclude() -> bool:
	for clue_id in clues:
		if bool(clues[clue_id].get("essential", false)) and not found.has(clue_id):
			return false
	return true


func missing_essential() -> Array:
	var missing: Array = []
	for clue_id in clues:
		if bool(clues[clue_id].get("essential", false)) and not found.has(clue_id):
			missing.append(clue_id)
	missing.sort()
	return missing
