class_name SWNPsionics
extends RefCounted

## Stars Without Number Revised (2017), Psionics pp. 29-43.
## Source-mechanics engine for the legacy CWN-first NooPunk RPG.
## No power descriptions are redistributed. Technique effects remain explicit,
## source-reviewed callers, not unapproved NooPunk homebrew.
const DISCIPLINES := ["Biopsionics", "Metapsionics", "Precognition", "Telekinesis", "Telepathy", "Teleportation"]
const FULL := "swn_psychic"
const PARTIAL := "swn_partial_psychic"
const ATTRS := ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
const TELEPORT_METERS := [10.0, 100.0, 10000.0, 1000000.0, -1.0] # -1: planetary/near orbit

var package: String = ""
var attributes: Dictionary = {}
var skills: Dictionary = {}
var learned: Dictionary = {} # id -> {discipline, rank}; power definitions checked by source elsewhere
var commitments: Dictionary = {} # id -> {duration, amount}
var scene_number: int = 0
var last_torch_round: int = -1
var torch_bonus: int = 0
var incapacitated: bool = false

static func modifier(score: int) -> int:
	if score == 3: return -2
	if score <= 7: return -1
	if score <= 13: return 0
	if score <= 17: return 1
	return 2

func setup(kind: String, scores: Dictionary, disciplines: Dictionary) -> bool:
	if kind != FULL and kind != PARTIAL:
		return false
	for stat in ATTRS:
		if not scores.has(stat) or typeof(scores[stat]) != TYPE_INT or scores[stat] < 3 or scores[stat] > 18:
			return false
	if disciplines.is_empty() or (kind == PARTIAL and disciplines.size() > 1):
		return false
	for discipline in disciplines:
		if not DISCIPLINES.has(discipline) or typeof(disciplines[discipline]) != TYPE_INT or disciplines[discipline] < 0 or disciplines[discipline] > 4:
			return false
	package = kind
	attributes = scores.duplicate(true)
	skills = disciplines.duplicate(true)
	learned.clear()
	commitments.clear()
	scene_number = 0
	last_torch_round = -1
	torch_bonus = 0
	incapacitated = false
	return true

func max_effort() -> int:
	if package.is_empty(): return 0
	var highest := 0
	for value in skills.values():
		highest = maxi(highest, int(value))
	return maxi(1, 1 + maxi(modifier(int(attributes["WIS"])), modifier(int(attributes["CON"]))) + highest)

func free_effort() -> int:
	var spent := 0
	for row in commitments.values():
		spent += int(row["amount"])
	return max_effort() + torch_bonus - spent

func learn_discipline(name: String) -> bool:
	if package.is_empty() or not DISCIPLINES.has(name) or skills.has(name):
		return false
	if package == PARTIAL and not skills.is_empty():
		return false
	skills[name] = 0
	return true

## Raising ranks requires an externally-authorized CWN/SWN advancement purchase.
func set_advanced_rank(name: String, new_rank: int, paid_by_progression: bool) -> bool:
	if not paid_by_progression or not skills.has(name) or new_rank != int(skills[name]) + 1 or new_rank > 4:
		return false
	skills[name] = new_rank
	return true

func learn_technique(id: String, discipline: String, minimum_rank: int, authorized_choice: bool) -> bool:
	if not authorized_choice or id.is_empty() or learned.has(id) or not skills.has(discipline):
		return false
	if minimum_rank < 0 or minimum_rank > 4 or int(skills[discipline]) < minimum_rank:
		return false
	learned[id] = {"discipline": discipline, "rank": minimum_rank}
	return true

func can_use(id: String) -> bool:
	if incapacitated or not learned.has(id):
		return false
	var row: Dictionary = learned[id]
	return int(skills.get(str(row["discipline"]), -1)) >= int(row["rank"])

## The caller must establish the technique's published action, target, effect,
## and Effort duration before invoking this gate. No generic effect inference.
func activate(id: String, key: String, duration: String, amount: int = 1) -> bool:
	if not can_use(id) or amount != 1 or not ["none", "active", "scene", "day"].has(duration):
		return false
	if duration == "none":
		return true
	if key.is_empty() or commitments.has(key) or free_effort() < amount:
		return false
	commitments[key] = {"duration": duration, "amount": amount, "technique": id}
	return true

func release_active(key: String) -> bool:
	if not commitments.has(key) or str(commitments[key]["duration"]) != "active":
		return false
	commitments.erase(key)
	return true

func end_scene() -> void:
	scene_number += 1
	for key in commitments.keys():
		if str(commitments[key]["duration"]) != "day":
			commitments.erase(key)
	torch_bonus = 0

func rest() -> void:
	commitments.clear()
	torch_bonus = 0

## Torch: SWN Revised p.31. The bonus point lasts for this scene.
## Once each combat round; die 1-2 damages WIS, 3-4 CON, 5 chosen stat, 6 harmless.
## A score below 3 makes the PC nonviable and blocks further player actions.
func torch(round_index: int, d6: int, chosen_stat: String = "") -> Dictionary:
	if package.is_empty() or incapacitated or round_index <= last_torch_round or d6 < 1 or d6 > 6:
		return {"ok": false}
	var harmed := ""
	if d6 <= 2: harmed = "WIS"
	elif d6 <= 4: harmed = "CON"
	elif d6 == 5:
		if not ATTRS.has(chosen_stat): return {"ok": false}
		harmed = chosen_stat
	last_torch_round = round_index
	torch_bonus += 1
	if not harmed.is_empty():
		attributes[harmed] = int(attributes[harmed]) - 1
		if int(attributes[harmed]) < 3:
			incapacitated = true
	return {"ok": true, "damage_attribute": harmed, "incapacitated": incapacitated, "free_effort": free_effort()}

## SWN p.32: succor requires touch, grants System Strain 1 (2 if mortal).
## This resolves the numeric healing only; caller validates action, elapsed
## mortal-wound time and target contact. Effort is paid separately by activate().
static func psychic_succor(rank: int, dice: Array, target_hp: int, target_max: int, strain: int, con: int, mortal: bool) -> Dictionary:
	if rank < 0 or rank > 4 or con < 3 or con > 18 or target_max < 1 or target_hp < 0 or target_hp > target_max:
		return {"ok": false}
	var added_strain := 2 if mortal else 1
	if strain < 0 or strain + added_strain > con:
		return {"ok": false, "reason": "system_strain"}
	var die_count: int = int(([0, 1, 2, 2, 3] as Array)[rank])
	var bonus: int = int(([0, 1, 2, 6, 8] as Array)[rank])
	if dice.size() != die_count:
		return {"ok": false}
	var healed := bonus
	for die in dice:
		if typeof(die) != TYPE_INT or die < 1 or die > 6:
			return {"ok": false}
		healed += int(die)
	if rank == 0 and not mortal:
		return {"ok": false, "reason": "stabilization_only"}
	var new_hp: int = mini(target_max, healed if mortal else target_hp + healed)
	return {"ok": true, "hp": new_hp, "strain": strain + added_strain, "stabilized": mortal, "healed": healed}

static func teleport_range_meters(rank: int) -> float:
	if rank < 0 or rank > 4: return 0.0
	return TELEPORT_METERS[rank]

func snapshot() -> Dictionary:
	return {"version": 1, "package": package, "attributes": attributes.duplicate(true),
		"skills": skills.duplicate(true), "learned": learned.duplicate(true),
		"commitments": commitments.duplicate(true), "scene": scene_number,
		"last_torch_round": last_torch_round, "torch_bonus": torch_bonus, "incapacitated": incapacitated}

func restore(data: Dictionary) -> bool:
	if int(data.get("version", -1)) != 1 or not data.get("attributes") is Dictionary or not data.get("skills") is Dictionary:
		return false
	var candidate := SWNPsionics.new()
	if not candidate.setup(str(data.get("package", "")), data["attributes"], data["skills"]):
		return false
	if not data.get("learned") is Dictionary or not data.get("commitments") is Dictionary:
		return false
	for id in data["learned"]:
		var row = data["learned"][id]
		if not row is Dictionary or not candidate.learn_technique(str(id), str(row.get("discipline", "")), int(row.get("rank", -1)), true):
			return false
	var bonus := int(data.get("torch_bonus", 0))
	if bonus < 0 or bonus > 1000:
		return false
	candidate.torch_bonus = bonus
	for key in data["commitments"]:
		var row = data["commitments"][key]
		if not row is Dictionary or not candidate.activate(str(row.get("technique", "")), str(key), str(row.get("duration", "")), int(row.get("amount", 0))):
			return false
	# Check resources after restoring commitments.
	if candidate.free_effort() < 0:
		return false
	candidate.scene_number = int(data.get("scene", 0))
	candidate.last_torch_round = int(data.get("last_torch_round", -1))
	candidate.incapacitated = bool(data.get("incapacitated", false))
	package = candidate.package
	attributes = candidate.attributes
	skills = candidate.skills
	learned = candidate.learned
	commitments = candidate.commitments
	scene_number = candidate.scene_number
	last_torch_round = candidate.last_torch_round
	torch_bonus = candidate.torch_bonus
	incapacitated = candidate.incapacitated
	return true
