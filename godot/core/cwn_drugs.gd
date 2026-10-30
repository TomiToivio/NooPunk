extends RefCounted
class_name CwnDrugs
## Pharmaceuticals and street drugs — CWN SRD 3.5.0.
##
## What is modelled: the published table (price, minimum Heal skill, rarity) and the three general rules
## the section states. What is NOT modelled: each drug's individual effect. Those descriptions are prose
## with their own saves, durations and damage, and inventing a shape for them here would be the same sin
## as inventing a rule — they belong in a later pass with their own tests.
##
## The three general rules are the ones that bite in play:
##
## * Administering a drug is a **Main Action**.
## * With several drugs active, **only the highest bonus applies** — bonuses do not add.
## * If the System Strain would exceed the maximum, the user gets **no benefit** but still suffers the
##   negative effects. That asymmetry is the point: a chem cannot be used as a free action economy.

const DATA_PATH := "res://data/rules/cwn/drugs.json"

static var _doc: Dictionary = {}


static func _data() -> Dictionary:
	if not _doc.is_empty():
		return _doc
	if not FileAccess.file_exists(DATA_PATH):
		push_error("CwnDrugs: missing %s" % DATA_PATH)
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("CwnDrugs: %s is not valid JSON" % DATA_PATH)
		return {}
	_doc = parsed
	return _doc


static func all_drugs() -> Array:
	return _data().get("drugs", [])


static func drug(id: String) -> Dictionary:
	for entry in all_drugs():
		if entry.get("id", "") == id:
			return entry
	return {}


static func price(id: String) -> int:
	return int(drug(id).get("price", 0))


static func min_heal(id: String) -> int:
	## `null` in the data means the SRD prints "None" — anyone can administer it. That is not the same as
	## Heal 0, so the sentinel is preserved rather than collapsed into a number.
	var entry := drug(id)
	if entry.is_empty():
		push_error("CwnDrugs: unknown drug '%s'" % id)
		return -1
	return -1 if entry.get("min_heal") == null else int(entry["min_heal"])


static func anyone_can_administer(id: String) -> bool:
	return min_heal(id) < 0


static func can_administer(id: String, heal_skill: int) -> bool:
	var required := min_heal(id)
	if required < 0:
		return true
	return heal_skill >= required


static func is_rare(id: String) -> bool:
	## Rare chems need a Contact or other street connection, per the SRD's footnote.
	return bool(drug(id).get("rare", false))


static func stacking_bonus(bonuses: Array) -> int:
	## Only the highest applies. Summing is the obvious wrong answer and the one this function exists to
	## make impossible at the call site.
	var best := 0
	for bonus in bonuses:
		best = maxi(best, int(bonus))
	return best


static func applies_benefit(current_strain: int, added_strain: int, maximum: int) -> bool:
	## Benefit requires staying within the maximum; negatives still apply either way.
	return current_strain + added_strain <= maximum
