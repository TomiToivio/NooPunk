## SWN psionic Effort accounting for Godot: the pool, the Commitments, and Torching.
##
## The numbers are read from `data/rules/swn_psionics.json`, which is pinned to
## `src/rules/swn_psionics.py` by `tests/test_swn_psionics_contract.py`. Stars Without Number Revised
## has no verified SRD licence, so this file holds mechanics only — no power names, tables or prose.
##
## Effort maximum = one + the higher of the Wisdom or Constitution modifier + the highest psychic
## skill rank. Effort is **Committed** (never spent) for as long as the power lasts, for the scene, or
## until rest; everything returns after a good night's sleep. **Torching** buys one more point for the
## rest of the scene, may take the psychic over the maximum, and costs an attribute point on a d6 roll.
class_name PsychicEffort
extends RefCounted

const DISCIPLINES := ["Biopsionics", "Metapsionics", "Precognition", "Telekinesis", "Telepathy", "Teleportation"]
const CONTRACT_PATH := "res://data/rules/swn_psionics.json"
const ATTRIBUTE_FLOOR := 3

static var _contract: Dictionary = {}

static func contract() -> Dictionary:
	if not _contract.is_empty():
		return _contract
	if FileAccess.file_exists(CONTRACT_PATH):
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CONTRACT_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_contract = parsed
	return _contract

## The d6 torching table: what a burn costs.
static func torching_table() -> Dictionary:
	var table: Dictionary = contract().get("torching", {}).get("table", {})
	if table.is_empty():
		return {"1": "wisdom", "2": "wisdom", "3": "constitution",
			"4": "constitution", "5": "choice", "6": "none"}
	return table

var wisdom: int
var constitution: int
var ranks: Dictionary
var commitments: Dictionary = {}
var scene: int = 0
## A Partial Psychic may master exactly one discipline; empty means unrestricted.
var restricted_discipline: String = ""
## Effort bought by torching. It may exceed the maximum and lasts only for the scene.
var torch_bonus: int = 0
var torched_round: int = -1

func _init(wis: int = 10, con: int = 10, skills: Dictionary = {}) -> void:
	wisdom = wis
	constitution = con
	ranks = skills.duplicate(true)

func capacity() -> int:
	# Feral (Wisdom below 3) or dead (any other attribute below 3) characters have no usable pool,
	# and the kernel refuses to price a score below 3 at all.
	if wisdom < ATTRIBUTE_FLOOR or constitution < ATTRIBUTE_FLOOR:
		return 0
	var kernel := RulesAdapter.new()
	var highest := 0
	for name in ranks:
		if name in DISCIPLINES:
			highest = maxi(highest, int(ranks[name]))
	if not bool(contract().get("effort", {}).get("plus_highest_psychic_skill", true)):
		highest = 0
	var base := maxi(1, 1 + maxi(kernel.attribute_modifier(wisdom), kernel.attribute_modifier(constitution)) + highest)
	return base + torch_bonus

func available_effort() -> int:
	var used := 0
	for commitment in commitments.values():
		used += int(commitment["amount"])
	return capacity() - used

func commit(key: String, discipline: String, rank: int = 0, duration: String = "scene", amount: int = 1) -> bool:
	if key.is_empty() or commitments.has(key) or not ranks.has(discipline) or not discipline in DISCIPLINES:
		return false
	if int(ranks[discipline]) < rank or rank < 0 or not duration in ["active", "scene", "day"]:
		return false
	if amount < 1 or amount > available_effort():
		return false
	commitments[key] = {"amount": amount, "duration": duration, "discipline": discipline}
	return true

## Whether this psychic may study the discipline at all: unrestricted may raise any, a restricted
## (Partial Psychic) one may master a single discipline and no other.
func can_learn(discipline: String) -> bool:
	if not (discipline in DISCIPLINES):
		return false
	return restricted_discipline.is_empty() or discipline == restricted_discipline

## Burn past the Effort limit: an Instant action, once per round, that buys one point for the rest of
## the scene and takes an attribute point on the d6 table. Returns the effect and the resulting status
## (`ok`, `feral` at Wisdom below 3, `dead` at any other attribute below 3). There is no cure.
func torch(die: int, round_number: int, choice: String = "") -> Dictionary:
	if die < 1 or die > 6:
		return {"ok": false, "reason": "the_torching_die_is_a_d6"}
	if round_number == torched_round:
		return {"ok": false, "reason": "already_torched_this_round"}
	var effect := String(torching_table().get(str(die), "none"))
	if effect == "choice" and not (choice in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]):
		return {"ok": false, "reason": "a_choice_result_needs_one_of_the_six_attributes"}
	torched_round = round_number
	torch_bonus += int(contract().get("torching", {}).get("grants_effort", 1))
	var lost := ""
	match effect:
		"wisdom":
			wisdom -= 1
			lost = "WIS"
		"constitution":
			constitution -= 1
			lost = "CON"
		"choice":
			lost = choice
			if choice == "WIS":
				wisdom -= 1
			elif choice == "CON":
				constitution -= 1
	var status := "ok"
	if wisdom < ATTRIBUTE_FLOOR:
		status = "feral"
	elif constitution < ATTRIBUTE_FLOOR:
		status = "dead"
	return {"ok": true, "granted": torch_bonus, "effect": effect, "attribute_lost": lost,
		"status": status, "capacity": capacity(),
		"sheet_must_apply": lost if not (lost in ["WIS", "CON", ""]) else ""}

func release(key: String) -> bool:
	if not commitments.has(key) or String(commitments[key]["duration"]) != "active":
		return false
	commitments.erase(key)
	return true

func end_scene() -> void:
	scene += 1
	for key in commitments.keys():
		if String(commitments[key]["duration"]) != "day":
			commitments.erase(key)
	# Torched Effort was paid for with an attribute point; it lasts only for its scene.
	torch_bonus = 0

func rest() -> void:
	commitments.clear()
	torch_bonus = 0

func snapshot() -> Dictionary:
	return {
		"wisdom": wisdom, "constitution": constitution,
		"ranks": ranks.duplicate(true), "commitments": commitments.duplicate(true),
		"scene": scene, "restricted_discipline": restricted_discipline,
		"torch_bonus": torch_bonus, "torched_round": torched_round,
	}

func restore(saved: Dictionary) -> bool:
	var candidate := PsychicEffort.new(int(saved.get("wisdom", 10)), int(saved.get("constitution", 10)), saved.get("ranks", {}))
	var kept: Dictionary = saved.get("commitments", {})
	for key in kept:
		var entry: Dictionary = kept[key]
		if not candidate.commit(String(key), String(entry.get("discipline", "")),
				0, String(entry.get("duration", "scene")), int(entry.get("amount", 0))):
			# Older snapshots may lack discipline. Do not invent a valid authorization.
			return false
	wisdom = candidate.wisdom
	constitution = candidate.constitution
	ranks = candidate.ranks
	commitments = candidate.commitments
	scene = int(saved.get("scene", 0))
	restricted_discipline = String(saved.get("restricted_discipline", ""))
	torch_bonus = int(saved.get("torch_bonus", 0))
	torched_round = int(saved.get("torched_round", -1))
	return true
