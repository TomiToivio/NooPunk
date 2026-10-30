extends RefCounted
## Canonical character creation data for NoöPunk #835; see rulebook Characters.
const NAMES: Array[String] = ["Fitness", "Reflexes", "Cognition", "Cyber", "Awareness", "Agency", "Empathy"]
const DEFINITIONS: Array[String] = [
	"Your physical strength and constitution",
	"Your physical dexterity, agility and coordination",
	"Your ability to process language and data",
	"Your ability to interface with technology",
	"Your intuition, perception and awareness",
	"Your free will",
	"Your loving kindness and humanity",
]
const DIFFICULTIES: Dictionary = {6: "Easiest", 8: "Easier", 10: "Easy", 12: "Average", 14: "Hard", 16: "Harder", 18: "Hardest"}

static func modifier(total: int) -> int:
	assert(total >= 3 and total <= 18, "3d6 total must be within 3..18")
	if total <= 4:
		return -3
	if total <= 6:
		return -2
	if total <= 8:
		return -1
	if total <= 12:
		return 0
	if total <= 14:
		return 1
	if total <= 16:
		return 2
	return 3

static func roll_character(rng: RandomNumberGenerator) -> Dictionary:
	var values := {}
	for name in NAMES:
		var total := rng.randi_range(1, 6) + rng.randi_range(1, 6) + rng.randi_range(1, 6)
		values[name] = modifier(total)
	return values

static func display_value(value: int) -> String:
	return "%+d" % value
