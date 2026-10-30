## SWN psychic advancement: disciplines, technique picks, and the core technique.
##
## Port of `src/rules/swn_progression.py`, which the numbers in
## `data/rules/swn_psionics.json` are pinned to by `tests/test_swn_psionics_contract.py`. The book's
## rules, as they bind here (Psionics, printed pp.30-31):
##
## * **The core technique is free.** Level-0 proficiency in a discipline grants it, it improves with
##   the skill, and it is never bought or trained — so it never spends a pick.
## * **One improvement, one technique.** Each time a discipline's skill level improves, the psychic
##   picks one technique from *that* discipline, immediately. Picks cannot be banked, so an unspent
##   pick blocks the next improvement.
## * **A technique never exceeds its teacher's rank.** A technique whose minimum skill level is above
##   the character's current rank in the discipline cannot be picked.
## * **Restricted psychics stay restricted.** A Partial Psychic masters one discipline and may learn
##   no other.
##
## Learning is separate from activating: Effort reservations live in `psychic_effort.gd`. The
## catalogue is NoöPunk-authored; SWN's power list is not reproduced.
extends RefCounted
class_name CwnPsychicTraining

const Effort := preload("res://godot/core/psychic_effort.gd")
const CONTRACT_PATH := "res://data/rules/swn_psionics.json"
const FULL := "swn_psychic"
const PARTIAL := "swn_partial_psychic"
const CORE_TECHNIQUE_RANK := 0
const MAX_DISCIPLINE_RANK := 4

static var _contract: Dictionary = {}

static func contract() -> Dictionary:
	if not _contract.is_empty():
		return _contract
	if FileAccess.file_exists(CONTRACT_PATH):
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CONTRACT_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_contract = parsed
	return _contract

var package := ""
var skills: Dictionary = {}
var techniques: Dictionary = {}
## The discipline whose improvement is waiting for its technique. Never banked across improvements.
var pending_pick := ""

func _init(psionic_package: String, ranks: Dictionary = {}, known: Dictionary = {},
		pending: String = "") -> void:
	package = psionic_package
	skills = ranks.duplicate(true)
	techniques = known.duplicate(true)
	pending_pick = pending

## Returns "" when the package is legal, or the reason it is not.
func validate() -> String:
	if not (package in [FULL, PARTIAL]):
		return "a_psychic_package_is_required"
	var limit := int(contract().get("progression", {}).get("partial_psychic_discipline_limit", 1))
	if package == PARTIAL and skills.size() > limit:
		return "too_many_disciplines_for_a_partial_psychic"
	for name in skills.keys():
		if not (String(name) in disciplines()):
			return "invalid_psychic_discipline"
		var rank := int(skills[name])
		if rank < 0 or rank > MAX_DISCIPLINE_RANK:
			return "invalid_psychic_rank"
	if not pending_pick.is_empty() and not skills.has(pending_pick):
		return "a_pending_pick_needs_a_trained_discipline"
	for identifier in techniques.keys():
		var row: Array = techniques[identifier]
		if row.size() != 2 or not has_prerequisite(String(row[0]), int(row[1])):
			return "invalid_or_unqualified_learned_technique"
	return ""

## One home for the six disciplines: the Effort kernel already owns the list.
func disciplines() -> Array:
	return Effort.DISCIPLINES

func has_prerequisite(discipline: String, minimum_rank: int = 0) -> bool:
	if not skills.has(discipline) or minimum_rank < 0 or minimum_rank > MAX_DISCIPLINE_RANK:
		return false
	return int(skills[discipline]) >= minimum_rank

## The core technique is available from rank 0 and never spends a pick.
func core_available(discipline: String) -> bool:
	return skills.has(discipline) and int(skills[discipline]) >= CORE_TECHNIQUE_RANK

## Train a new discipline at rank 0. A Partial Psychic may never hold a second one.
func learn_discipline(discipline: String) -> bool:
	if not (discipline in disciplines()) or skills.has(discipline):
		return false
	if package == PARTIAL and not skills.is_empty():
		return false
	skills[discipline] = 0
	return true

## Improve a trained discipline by one, and open its technique pick. Refused while a pick is open.
func advance(discipline: String) -> Dictionary:
	if not pending_pick.is_empty():
		return {"ok": false, "reason": "spend_the_open_pick_first", "discipline": pending_pick}
	if not skills.has(discipline):
		return {"ok": false, "reason": "discipline_not_trained"}
	if int(skills[discipline]) >= MAX_DISCIPLINE_RANK:
		return {"ok": false, "reason": "discipline_already_at_rank_four"}
	skills[discipline] = int(skills[discipline]) + 1
	pending_pick = discipline
	return {"ok": true, "rank": int(skills[discipline]), "pick_open": discipline}

## Spend the open pick on a catalogue entry from the same discipline.
func learn_technique(identifier: String, discipline: String, required_rank: int) -> bool:
	if identifier.is_empty() or techniques.has(identifier):
		return false
	if not has_prerequisite(discipline, required_rank):
		return false
	if pending_pick != discipline:
		return false
	techniques[identifier] = [discipline, required_rank]
	pending_pick = ""
	return true

func technique_access(identifier: String) -> bool:
	if not techniques.has(identifier):
		return false
	var row: Array = techniques[identifier]
	return has_prerequisite(String(row[0]), int(row[1]))

func snapshot() -> Dictionary:
	return {"package": package, "skills": skills.duplicate(true),
		"pending_pick": pending_pick, "techniques": techniques.duplicate(true)}

func restore(saved: Dictionary) -> bool:
	# `get_script()` rather than the class name: a script cannot name itself as a global type.
	var candidate = (get_script() as GDScript).new(
		String(saved.get("package", "")),
		Dictionary(saved.get("skills", {})),
		Dictionary(saved.get("techniques", {})),
		String(saved.get("pending_pick", ""))
	)
	if not candidate.validate().is_empty():
		return false
	package = candidate.package
	skills = candidate.skills
	techniques = candidate.techniques
	pending_pick = candidate.pending_pick
	return true
