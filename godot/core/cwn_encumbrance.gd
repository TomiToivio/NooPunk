## Cities Without Number: encumbrance, load tiers and the speed they cost.
##
## Port of `src/rules/cwn_encumbrance.py`. Stowed capacity is the Strength score; readied capacity is
## half of it. Exceeding either is a **heavy** load (70% speed), pushing twice is **overloaded**
## (50%), and beyond that the character cannot move at all. Bundles and kilograms convert at the
## rates the book gives, so a table can use either unit.
extends RefCounted
class_name CwnEncumbrance

const READIED_DIVISOR := 2
const OVERLOAD_READIED_BONUS := 2
const OVERLOAD_STOWED_BONUS := 4
const HEAVY_LOAD_SPEED_FACTOR := 0.70
const OVERLOADED_SPEED_FACTOR := 0.50
const BASE_MOVE_METRES := 10.0
const BUNDLE_SIZE := 3
const KILOGRAMS_PER_TEN_POINTS := 25.0

static func stowed_capacity(strength: int) -> int:
	return maxi(0, strength)

static func readied_capacity(strength: int) -> int:
	return maxi(0, strength) / READIED_DIVISOR

## "normal", "heavy", "overloaded" or "immobile".
static func tier_for(strength: int, stowed: int, readied: int) -> String:
	var stowed_limit := stowed_capacity(strength)
	var readied_limit := readied_capacity(strength)
	if stowed <= stowed_limit and readied <= readied_limit:
		return "normal"
	if stowed <= stowed_limit + OVERLOAD_STOWED_BONUS \
			and readied <= readied_limit + OVERLOAD_READIED_BONUS:
		return "heavy"
	if stowed <= stowed_limit + 2 * OVERLOAD_STOWED_BONUS \
			and readied <= readied_limit + 2 * OVERLOAD_READIED_BONUS:
		return "overloaded"
	return "immobile"

## The Move action's distance, in metres, at this load.
static func move_speed(tier: String, base_metres: float = BASE_MOVE_METRES) -> float:
	match tier:
		"normal":
			return base_metres
		"heavy":
			return base_metres * HEAVY_LOAD_SPEED_FACTOR
		"overloaded":
			return base_metres * OVERLOADED_SPEED_FACTOR
		_:
			return 0.0

static func can_haul(strength: int, stowed: int, readied: int) -> bool:
	return tier_for(strength, stowed, readied) != "immobile"

## Three items to a bundle.
static func bundled_points(item_count: int) -> int:
	return int(ceil(float(maxi(0, item_count)) / float(BUNDLE_SIZE)))

## Ten encumbrance points weigh 25 kg.
static func kilograms_to_points(kilograms: float) -> float:
	return maxf(0.0, kilograms) / KILOGRAMS_PER_TEN_POINTS * 10.0
