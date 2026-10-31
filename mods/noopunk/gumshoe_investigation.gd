## GUMSHOE investigative pools as a CWN overlay (#932).
##
## **Not a second resolution engine.** CWN remains the only core: attributes, saves, 2d6 skill checks, combat,
## hacking and progression are untouched. This module adds one thing GUMSHOE does better than any
## d20/2d6 game — *investigative abilities never fail when a clue is essential* — and it does so as pool
## accounting around CWN, not as a replacement for it.
##
## Source: GUMSHOE SRD (OGL). The rules encoded here:
##
## * "As long as you do these three things, you will never fail to gain a piece of necessary information.
##   It is never dependent on a die roll." (Gathering Clues)
## * "For each scene, the GM designates a core clue… It costs nothing." (Core Clues)
## * "Certain clues allow you to gain special benefits by spending points… Each benefit costs either 1 or 2
##   points." (Special Benefits)
## * "Spent points do not return until the next investigation begins." (Investigative Ratings)
##
## **No die is rolled here.** `gather()` cannot fail for a character with the ability, so there is no roll to
## make. Where the outcome is genuinely in doubt the caller asks CWN — see `delegate_to_cwn()`.
extends RefCounted
class_name NoopunkGumshoe

const DATA_PATH := "res://data/rules/gumshoe_investigative.json"
const MIN_COST := 1
const MAX_COST := 2

##: ability id -> {id, name, kind, cwn_skill, rating, pool}
var abilities: Dictionary = {}
var order: Array = []
##: Benefits already bought this investigation, so a scene cannot sell the same advantage twice.
var benefits: Array = []


static func load_data(path: String = DATA_PATH) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


## Build the overlay from the shipped ability list. `ratings` gives investigative ratings; the pool starts
## equal to the rating, which is how GUMSHOE characters begin an investigation.
static func from_data(data: Dictionary, ratings: Dictionary = {}) -> NoopunkGumshoe:
	var gumshoe := NoopunkGumshoe.new()
	for entry in Array(data.get("abilities", [])):
		var ability: Dictionary = entry
		var ability_id := String(ability.get("id", ""))
		if ability_id.is_empty():
			continue
		var rating := int(ratings.get(ability_id, 0))
		gumshoe.abilities[ability_id] = {
			"id": ability_id,
			"name": String(ability.get("name", ability_id)),
			"kind": String(ability.get("kind", "")),
			"cwn_skill": String(ability.get("cwn_skill", "")),
			"rating": maxi(rating, 0),
			"pool": maxi(rating, 0),
		}
		gumshoe.order.append(ability_id)
	return gumshoe


static func shipped(ratings: Dictionary = {}) -> NoopunkGumshoe:
	return from_data(load_data(), ratings)


# ---- queries -------------------------------------------------------------------------------------

func has(ability_id: String) -> bool:
	return abilities.has(ability_id)


func rating(ability_id: String) -> int:
	return int(abilities.get(ability_id, {}).get("rating", 0))


func pool(ability_id: String) -> int:
	return int(abilities.get(ability_id, {}).get("pool", 0))


## The CWN skill that covers this ground for a character without the ability. The overlay never demands
## that a player own GUMSHOE abilities to work a case.
func cwn_skill_for(ability_id: String) -> String:
	return String(abilities.get(ability_id, {}).get("cwn_skill", ""))


# ---- gathering -----------------------------------------------------------------------------------

## Whether this investigator can gather information with this ability. A rating of 1 is enough; an empty
## pool is not an obstacle, which is the whole point of the system.
func can_gather(ability_id: String) -> Dictionary:
	if not abilities.has(ability_id):
		return {"ok": false, "reason": "unknown_ability"}
	if rating(ability_id) < 1:
		return {"ok": false, "reason": "no_rating", "cwn_skill": cwn_skill_for(ability_id)}
	return {"ok": true, "reason": ""}


## Gather a clue. No roll, no spend: if the investigator has the ability and is in the scene, the
## information is theirs. `core` changes what the clue means (it moves the story), never whether it is found.
func gather(ability_id: String, clue: Dictionary = {}) -> Dictionary:
	var verdict := can_gather(ability_id)
	if not bool(verdict.get("ok", false)):
		return verdict
	var clue_id := String(clue.get("id", ""))
	return {
		"ok": true,
		"found": true,
		"clue": clue_id,
		"core": bool(clue.get("core", false)),
		"spent": 0,
		"reason": "",
	}


## Cost of a special benefit, as the SRD fixes it: one or two points.
static func cost_is_legal(cost: int) -> bool:
	return cost >= MIN_COST and cost <= MAX_COST


## Buy a special benefit. This is the ONLY place points leave a pool. A benefit is never required to solve
## the case, and never a core clue — buying one cannot be what makes the mystery solvable.
func buy_benefit(ability_id: String, benefit_id: String, cost: int = 1) -> Dictionary:
	if not abilities.has(ability_id):
		return {"ok": false, "reason": "unknown_ability"}
	if String(benefit_id).is_empty():
		return {"ok": false, "reason": "no_benefit"}
	if not cost_is_legal(cost):
		return {"ok": false, "reason": "illegal_cost", "min": MIN_COST, "max": MAX_COST}
	if pool(ability_id) < cost:
		return {"ok": false, "reason": "pool_empty", "pool": pool(ability_id), "cost": cost}
	if benefits.has(String(benefit_id)):
		return {"ok": false, "reason": "already_bought"}
	abilities[ability_id]["pool"] = pool(ability_id) - cost
	benefits.append(String(benefit_id))
	return {"ok": true, "reason": "", "spent": cost, "pool": pool(ability_id),
		"benefit": String(benefit_id)}


## A new investigation restores every pool to its rating. Between investigations, nothing else refreshes.
func refresh() -> Dictionary:
	var restored: Dictionary = {}
	for ability_id in order:
		abilities[ability_id]["pool"] = rating(ability_id)
		restored[ability_id] = rating(ability_id)
	benefits.clear()
	return restored


# ---- delegation ----------------------------------------------------------------------------------

## Where GUMSHOE would roll its own d6, the NoöPunk overlay asks CWN instead.
##
## The rule is not negotiable: introducing a d6 general system would be a second resolution engine, which
## the foundational lock forbids. This function therefore takes the CWN result as an argument and adds
## only what spending points can add — a bonus, never a replacement roll.
static func delegate_to_cwn(cwn_success: bool, spent: int = 0) -> Dictionary:
	if spent < 0:
		return {"ok": false, "reason": "negative_spend"}
	return {
		"ok": true,
		"success": cwn_success,
		"spent": spent,
		# Spending improves an attempt the CWN roll already resolved; it never re-rolls it.
		"engine": "cwn",
	}


# ---- persistence ---------------------------------------------------------------------------------

func to_dict() -> Dictionary:
	var pools: Dictionary = {}
	for ability_id in order:
		pools[ability_id] = pool(ability_id)
	return {"pools": pools, "benefits": benefits.duplicate()}


## Restore pools after a save. Ratings come from the character sheet, not the save, so a rebuilt sheet and a
## restored pool cannot disagree about the maximum.
func from_dict(data: Dictionary) -> void:
	for ability_id in Array(data.get("pools", {}).keys()):
		if abilities.has(String(ability_id)):
			var value := int(data["pools"][ability_id])
			abilities[String(ability_id)]["pool"] = clampi(value, 0, rating(String(ability_id)))
	benefits = []
	for benefit in Array(data.get("benefits", [])):
		benefits.append(String(benefit))
