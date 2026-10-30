## Cities Without Number: System Strain — the body's price for cyberware and chemistry.
##
## Port of `src/rules/cwn_strain.py`. Strain is **permanent** (installed cyberware) plus
## **temporary** (drugs, abilities, emergencies); the maximum is the character's Constitution score.
## A character who cannot fit an addition simply cannot use it. Forced overflow clamps at the
## maximum and costs at least an hour of unconsciousness.
extends RefCounted
class_name CwnStrain

const RECOVERY_PER_NIGHT := 1.0
const REST_HOURS_REQUIRED := 8.0
const FORCED_OVERFLOW_UNCONSCIOUS_HOURS := 1.0

var constitution := 0
var temporary := 0.0
var permanent := 0.0
var unconscious_hours := 0.0

func _init(constitution_score: int, temporary_strain: float = 0.0, permanent_strain: float = 0.0) -> void:
	constitution = constitution_score
	temporary = temporary_strain
	permanent = permanent_strain

func maximum() -> int:
	return constitution

func total() -> float:
	return permanent + temporary

func available() -> float:
	return maxf(0.0, float(maximum()) - total())

func can_absorb(amount: float) -> bool:
	if amount < 0.0:
		return false
	return total() + amount <= float(maximum())

## Returns true when the Strain was taken. With `forced`, an overflow clamps at the maximum and
## leaves the character unconscious; without it, nothing changes and the item cannot be used.
func absorb(amount: float, forced: bool = false) -> bool:
	if amount < 0.0:
		return false
	if can_absorb(amount):
		temporary += amount
		return true
	if forced:
		temporary = maxf(0.0, float(maximum()) - permanent)
		unconscious_hours = maxf(unconscious_hours, FORCED_OVERFLOW_UNCONSCIOUS_HOURS)
	return false

## One point back after a qualifying night (eight hours, warm, fed, comfortable).
func rest_night(hours: float = REST_HOURS_REQUIRED, warm_fed_comfortable: bool = true) -> float:
	if hours < REST_HOURS_REQUIRED or not warm_fed_comfortable:
		return 0.0
	var recovered := minf(RECOVERY_PER_NIGHT, temporary)
	temporary -= recovered
	unconscious_hours = 0.0
	return recovered

## Cyberware consumes permanent Strain; removal restores the available ceiling.
func install_cyber(strain: float) -> bool:
	if strain < 0.0 or total() + strain > float(maximum()):
		return false
	permanent += strain
	return true

func remove_cyber(strain: float) -> void:
	if strain < 0.0:
		return
	permanent = maxf(0.0, permanent - strain)

func to_dict() -> Dictionary:
	return {"constitution": constitution, "temporary": temporary, "permanent": permanent,
		"unconscious_hours": unconscious_hours}

func from_dict(data: Dictionary) -> void:
	constitution = int(data.get("constitution", constitution))
	temporary = float(data.get("temporary", temporary))
	permanent = float(data.get("permanent", permanent))
	unconscious_hours = float(data.get("unconscious_hours", unconscious_hours))
