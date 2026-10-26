## Psionics for the Godot runtime: Effort, commitment, torching and the training gate.
##
## The mirror of `src/rules/psionics.py`. Both read the same authored catalogue
## (`data/rules/psionics_techniques.json`) and the same kernel (`data/rules/wn_core.json`), so the
## game and the tabletop cannot drift into two different psychics.
##
## The catalogue is PROVISIONAL NoöPunk content: every number in it belongs to the author. Stars
## Without Number has no verified SRD licence, so no power text, name or table from it is reproduced
## here — the mechanics are an independent expression of its shape.
class_name NoopunkPsionics
extends RefCounted

const CATALOGUE_PATH := "res://data/rules/psionics_techniques.json"

## The six adopted disciplines. They are specialist skills, never a class feature.
const DISCIPLINES := [
	"Biopsionics",
	"Metapsionics",
	"Precognition",
	"Telekinesis",
	"Telepathy",
	"Teleportation",
]

const TORCH_RESULTS := {
	1: "lose_1_wisdom",
	2: "lose_1_wisdom",
	3: "lose_1_constitution",
	4: "lose_1_constitution",
	5: "lose_1_chosen_attribute",
	6: "no_harm",
}

const FERAL_WISDOM := 3
const UNTRAINED := -1

var catalogue: Dictionary = {}
var rules: RulesAdapter


## An Effort pool: named commitments held for an active effect, a scene, or a day.
##
## Named keys (rather than bare counters) are what makes a held power releasable: a caller commits
## "thread" and later releases "thread". Torched Effort is extra capacity for the rest of the scene
## and is not part of the maximum. This carries over the semantics of the model #648 introduced and
## this module supersedes.
class EffortPool:
	const DURATIONS := ["active", "scene", "day"]

	var maximum: int = 0
	var reservations: Dictionary = {}
	var torched: int = 0

	func _init(p_maximum: int = 0) -> void:
		maximum = p_maximum

	func committed() -> int:
		var total := 0
		for entry in reservations.values():
			total += int(entry["amount"])
		return total

	## Everything that ends when the scene does: active and scene commitments.
	func committed_scene() -> int:
		var total := 0
		for entry in reservations.values():
			if String(entry["duration"]) != "day":
				total += int(entry["amount"])
		return total

	func committed_day() -> int:
		return committed() - committed_scene()

	func available() -> int:
		return maxi(0, maximum - committed()) + torched

	func can_commit(amount: int = 1) -> bool:
		return amount >= 1 and available() >= amount

	func commit(key: String, duration: String = "scene", amount: int = 1) -> bool:
		if key.is_empty() or reservations.has(key):
			return false
		if not DURATIONS.has(duration):
			return false
		if amount < 1 or not can_commit(amount):
			return false
		# Torched Effort is spent first: it is the loosest, shortest-lived point in the pool.
		torched -= mini(torched, amount)
		reservations[key] = {"amount": amount, "duration": duration}
		return true

	## Release a commitment. Only an "active" one may end early.
	func release(key: String) -> bool:
		if not reservations.has(key):
			return false
		if String(reservations[key]["duration"]) != "active":
			return false
		reservations.erase(key)
		return true

	## A scene ends: active and scene commitments return; torched Effort is gone.
	func end_scene() -> void:
		for key in reservations.keys():
			if String(reservations[key]["duration"]) != "day":
				reservations.erase(key)
		torched = 0

	## A good night's rest returns everything.
	func rest() -> void:
		reservations.clear()
		torched = 0

	func night_rest() -> void:
		rest()

	func snapshot() -> Dictionary:
		var saved: Dictionary = {}
		for key in reservations.keys():
			saved[key] = {
				"amount": int(reservations[key]["amount"]),
				"duration": String(reservations[key]["duration"]),
			}
		return {"maximum": maximum, "torched": torched, "reservations": saved}

	## Rebuild from a save. A malformed record returns false and leaves the pool untouched.
	func restore(data: Dictionary) -> bool:
		if not data.has("maximum") or not data.has("reservations"):
			return false
		var rebuilt: Dictionary = {}
		var raw: Dictionary = data.get("reservations", {})
		for key in raw.keys():
			var entry: Dictionary = raw[key]
			if not entry.has("amount") or not entry.has("duration"):
				return false
			if not DURATIONS.has(String(entry["duration"])):
				return false
			var amount := int(entry["amount"])
			if amount < 1:
				return false
			rebuilt[String(key)] = {"amount": amount, "duration": String(entry["duration"])}
		var rebuilt_maximum := int(data["maximum"])
		if rebuilt_maximum < 0:
			return false
		var total := 0
		for entry in rebuilt.values():
			total += int(entry["amount"])
		if total > rebuilt_maximum + int(data.get("torched", 0)):
			return false
		maximum = rebuilt_maximum
		torched = int(data.get("torched", 0))
		reservations = rebuilt
		return true


func _init(p_rules: RulesAdapter = null) -> void:
	rules = p_rules if p_rules != null else RulesAdapter.new()
	catalogue = _load_catalogue()


func _load_catalogue() -> Dictionary:
	if not FileAccess.file_exists(CATALOGUE_PATH):
		push_error("NoopunkPsionics: catalogue not found at %s" % CATALOGUE_PATH)
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CATALOGUE_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("NoopunkPsionics: catalogue is not a JSON object")
		return {}
	return parsed


func disciplines() -> Array:
	return catalogue.get("disciplines", DISCIPLINES) if catalogue.has("disciplines") else DISCIPLINES


## A technique by id, whether it is a discipline core or a learned pick. Empty when unknown.
##
## A core entry is stored under its discipline in the data, so the returned copy carries that
## discipline explicitly — callers should never have to know which of the two shapes they got.
func technique(technique_id: String) -> Dictionary:
	for entry in catalogue.get("techniques", []):
		if String(entry.get("id", "")) == technique_id:
			return entry
	var cores: Dictionary = catalogue.get("discipline_cores", {})
	for discipline in cores.keys():
		var core: Dictionary = cores[discipline]
		if String(core.get("id", "")) == technique_id:
			var resolved: Dictionary = core.duplicate()
			resolved["discipline"] = String(discipline)
			return resolved
	return {}


func core_for(discipline: String) -> Dictionary:
	var cores: Dictionary = catalogue.get("discipline_cores", {})
	if not cores.has(discipline):
		return {}
	var core: Dictionary = (cores[discipline] as Dictionary).duplicate()
	core["discipline"] = discipline
	return core


func technique_count() -> int:
	return (catalogue.get("techniques", []) as Array).size()


## ``1 + max(WIS modifier, CON modifier) + the highest psionic skill level``.
func max_effort(attributes: Dictionary, skills: Dictionary) -> int:
	var wisdom := rules.attribute_modifier(int(attributes.get("WIS", 10)))
	var constitution := rules.attribute_modifier(int(attributes.get("CON", 10)))
	var best := 0
	for discipline in DISCIPLINES:
		if skills.has(discipline):
			best = maxi(best, int(skills[discipline]))
	return 1 + maxi(wisdom, constitution) + best


## The training gate: a permission check, not a difficulty. Untrained characters cannot do it.
func may_use(technique_data: Dictionary, skills: Dictionary) -> bool:
	if technique_data.is_empty():
		return false
	var discipline := String(technique_data.get("discipline", ""))
	if discipline == "":
		return false
	var level := int(skills.get(discipline, UNTRAINED))
	return level >= maxi(0, int(technique_data.get("min_skill", 0)))


## ``none``, ``scene`` or ``day``: what using this technique does to the pool.
func effort_duration(technique_data: Dictionary) -> String:
	var cost := String(technique_data.get("effort", "none"))
	if cost == "commit_scene":
		return "scene"
	if cost == "commit_day":
		return "day"
	return "none"


## Use a technique: refuses when the character was never trained for it, otherwise commits Effort.
func use(technique_id: String, skills: Dictionary, pool: EffortPool) -> Dictionary:
	var data := technique(technique_id)
	if data.is_empty():
		return {"ok": false, "reason": "unknown technique"}
	if not may_use(data, skills):
		return {"ok": false, "reason": "the character was never trained in %s" % String(data.get("name", technique_id))}
	var duration := effort_duration(data)
	if duration != "none":
		if not pool.commit(_reservation_key(pool, technique_id), duration):
			return {"ok": false, "reason": "not enough Effort"}
	return {"ok": true, "technique": data, "committed": duration}


## A unique commitment name, so the same technique can be held twice.
func _reservation_key(pool: EffortPool, base: String) -> String:
	if not pool.reservations.has(base):
		return base
	var index := 2
	while pool.reservations.has("%s#%d" % [base, index]):
		index += 1
	return "%s#%d" % [base, index]


## Gain one Effort for the rest of the scene and pay for it on the d6 table.
func torch(die: int, attributes: Dictionary) -> Dictionary:
	if die < 1 or die > 6:
		return {}
	var harm := String(TORCH_RESULTS[die])
	var lost := ""
	if harm == "lose_1_wisdom":
		lost = "WIS"
	elif harm == "lose_1_constitution":
		lost = "CON"
	elif harm == "lose_1_chosen_attribute":
		lost = "any"
	if lost != "" and lost != "any":
		attributes[lost] = int(attributes.get(lost, 10)) - 1
	return {
		"roll": die,
		"harm": harm,
		"attribute_lost": lost,
		"feral": int(attributes.get("WIS", 10)) < FERAL_WISDOM,
	}
