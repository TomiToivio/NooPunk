class_name CWNStrain
extends RefCounted

## System Strain: permanent cyberware load plus temporary, recoverable load.
##
## Ported from `src/rules/cwn_strain.py` so the Godot game and the Python layer cannot drift.
##
## The rule as the SRD states it: a healthy character starts at 0, may never exceed their
## Constitution score, and cyberware installation adds *permanent* — possibly fractional — Strain
## that removal takes back. A drug or an implant that would pass the maximum simply cannot be used.
## An **unavoidable** effect that forces the character past the maximum does not raise the total
## (the SRD says the total cannot exceed it) — it knocks them out for at least an hour instead.
## One point is shed after each qualifying night's rest.
##
## This is biochemical load, not a generic currency: pricing a records pull in Strain would blur
## the one track the injury rules depend on.

const RECOVERY_PER_NIGHT := 1.0
const REST_HOURS_REQUIRED := 8.0
const FORCED_OVERFLOW_UNCONSCIOUS_HOURS := 1.0

var constitution: int = 0
var temporary: float = 0.0
var permanent: float = 0.0
var unconscious_hours: float = 0.0

func _init(constitution_score: int = 10, temporary_strain: float = 0.0,
		permanent_strain: float = 0.0) -> void:
	constitution = constitution_score
	temporary = temporary_strain
	permanent = permanent_strain
	assert(constitution >= 0, "Constitution cannot be negative")
	assert(temporary >= 0.0 and permanent >= 0.0, "Strain cannot be negative")
	assert(total() <= maximum(), "Strain exceeds the Constitution maximum")

func maximum() -> float:
	return float(constitution)

func total() -> float:
	return permanent + temporary

func available() -> float:
	return maxf(0.0, maximum() - total())

func can_absorb(amount: float) -> bool:
	assert(amount >= 0.0, "Strain additions cannot be negative")
	return total() + amount <= maximum()

## Add Strain if it fits. Returns true when taken.
## When it does not fit: `forced` false leaves the character unable to use the ability and changes
## nothing; `forced` true clamps at the maximum and records the unconsciousness.
func absorb(amount: float, forced: bool = false) -> bool:
	assert(amount >= 0.0, "Strain additions cannot be negative")
	if can_absorb(amount):
		temporary += amount
		return true
	if forced:
		temporary = maxf(0.0, maximum() - permanent)
		unconscious_hours = maxf(unconscious_hours, FORCED_OVERFLOW_UNCONSCIOUS_HOURS)
	return false

## One point after a qualifying night's rest: at least eight hours, warm, fed and comfortable.
func rest_night(hours: float = REST_HOURS_REQUIRED, warm_fed_comfortable: bool = true) -> float:
	if not warm_fed_comfortable or hours < REST_HOURS_REQUIRED:
		return 0.0
	var recovered := minf(RECOVERY_PER_NIGHT, temporary)
	temporary -= recovered
	unconscious_hours = 0.0
	return recovered

## Cyberware: permanent load, taken from the ceiling and kept while the implant stays.
func install_cyber(strain: float) -> bool:
	assert(strain >= 0.0, "Cyberware Strain cannot be negative")
	if total() + strain > maximum():
		return false
	permanent += strain
	return true

func remove_cyber(strain: float) -> void:
	assert(strain >= 0.0, "Cyberware Strain cannot be negative")
	permanent = maxf(0.0, permanent - strain)

func to_dict() -> Dictionary:
	return {
		"constitution": constitution,
		"temporary": temporary,
		"permanent": permanent,
		"unconscious_hours": unconscious_hours,
	}

static func from_dict(data: Dictionary) -> CWNStrain:
	return CWNStrain.new(
		int(data.get("constitution", 10)),
		float(data.get("temporary", 0.0)),
		float(data.get("permanent", 0.0)))
