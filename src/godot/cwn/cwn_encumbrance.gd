class_name CWNEncumbrance
extends RefCounted

## Carried load: Stowed and Readied points, overload tiers, and what they do to movement.
##
## Ported from `src/rules/cwn_encumbrance.py`. Gear is either **Stowed** (packed; a Main Action to
## retrieve) or **Readied** (in hands or quick access; usable as part of an action). A character
## carries Stowed points equal to Strength and Readied points equal to half Strength.
##
## Pushing past that has a price the runtime has to charge: +2 Readied and +4 Stowed per overload
## step, the first step costing 30% of Move (10 m to 7 m) and the second 50% (10 m to 5 m). Beyond
## the second step the load is not hauled any meaningful distance at all.
##
## This module does not decide whether a particular object is 0, 1, 2 or 5+ points — the source
## leaves ambiguous objects to the referee. It answers what fits, which tier the load is in, and what
## that tier does to movement.

const READIED_DIVISOR := 2
const OVERLOAD_READIED_BONUS := 2
const OVERLOAD_STOWED_BONUS := 4
const HEAVY_LOAD_SPEED_FACTOR := 0.70
const OVERLOADED_SPEED_FACTOR := 0.50
const BASE_MOVE_METRES := 10.0
const BUNDLE_SIZE := 3
const KILOGRAMS_PER_TEN_POINTS := 25.0

static func stowed_capacity(strength: int) -> int:
	assert(strength >= 0, "Strength cannot be negative")
	return strength

static func readied_capacity(strength: int) -> int:
	assert(strength >= 0, "Strength cannot be negative")
	return strength / READIED_DIVISOR

## "normal" | "heavy" | "overloaded" | "immobile"
static func tier_for(strength: int, stowed: float, readied: float) -> String:
	assert(stowed >= 0.0 and readied >= 0.0, "encumbrance cannot be negative")
	var stowed_limit := stowed_capacity(strength)
	var readied_limit := readied_capacity(strength)
	if stowed <= stowed_limit and readied <= readied_limit:
		return "normal"
	if stowed <= stowed_limit + OVERLOAD_STOWED_BONUS and readied <= readied_limit + OVERLOAD_READIED_BONUS:
		return "heavy"
	if stowed <= stowed_limit + 2 * OVERLOAD_STOWED_BONUS and readied <= readied_limit + 2 * OVERLOAD_READIED_BONUS:
		return "overloaded"
	return "immobile"

## Move speed in metres for this load. An immobile load is zero, not a fraction.
static func move_speed(strength: int, stowed: float, readied: float,
		base: float = BASE_MOVE_METRES) -> float:
	assert(base > 0.0, "base speed must be positive")
	match tier_for(strength, stowed, readied):
		"normal":
			return base
		"heavy":
			return base * HEAVY_LOAD_SPEED_FACTOR
		"overloaded":
			return base * OVERLOADED_SPEED_FACTOR
		_:
			return 0.0

static func can_haul(strength: int, stowed: float, readied: float) -> bool:
	return tier_for(strength, stowed, readied) != "immobile"

## Small identical items tied into bundles of three, rounded up.
static func bundled_points(item_count: int) -> int:
	assert(item_count >= 0, "item count cannot be negative")
	return (item_count + BUNDLE_SIZE - 1) / BUNDLE_SIZE

## Bulk weight to encumbrance points (25 kg is about 10 points on the back).
static func kilograms_to_points(kilograms: float) -> float:
	assert(kilograms >= 0.0, "weight cannot be negative")
	return kilograms / KILOGRAMS_PER_TEN_POINTS * 10.0
