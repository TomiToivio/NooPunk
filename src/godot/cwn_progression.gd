class_name CWNProgression
extends RefCounted
## CWN progression and physiological strain, separate from legacy mechanics.
const FAST_XP := [0, 0, 3, 6, 12, 18, 27, 39, 54, 72, 93]
const SLOW_XP := [0, 0, 6, 15, 24, 36, 51, 69, 87, 105, 139]
const SKILL_MIN_LEVEL := [1, 1, 3, 6, 9]

static func level_for_xp(xp: int, fast: bool = true) -> int:
	assert(xp >= 0)
	var thresholds := FAST_XP if fast else SLOW_XP
	var level := 1
	for next_level in range(2, 11):
		if xp >= thresholds[next_level]:
			level = next_level
	return level

static func skill_upgrade_cost(current_rank: int, new_rank: int, character_level: int) -> int:
	assert(current_rank >= -1 and current_rank <= 4)
	assert(new_rank >= 0 and new_rank <= 4)
	assert(character_level >= 1 and character_level <= 10)
	if new_rank <= current_rank or character_level < SKILL_MIN_LEVEL[new_rank]:
		return -1
	var price := 0
	for rank in range(current_rank + 1, new_rank + 1):
		if character_level < SKILL_MIN_LEVEL[rank]:
			return -1
		price += rank + 1
	return price

static func attack_bonus(level: int, on_target: bool = false) -> int:
	assert(level >= 1 and level <= 10)
	return level if on_target else floori(float(level) / 2.0)

static func focus_award(level: int) -> bool:
	return level in [2, 5, 7, 10]

static func edge_award(level: int) -> bool:
	return level == 5

static func roll_max_hp(rng: RandomNumberGenerator, level: int, constitution_modifier: int, hard_to_kill: bool = false) -> int:
	assert(level >= 1 and level <= 10)
	var hp := 0
	for i in range(level):
		hp += maxi(1, rng.randi_range(1, 6) + constitution_modifier + (2 if hard_to_kill else 0))
	return hp

static func improved_max_hp(old_maximum: int, rolled_maximum: int) -> int:
	assert(old_maximum >= 1 and rolled_maximum >= 1)
	return maxi(old_maximum + 1, rolled_maximum)

static func strain_capacity(constitution_score: int) -> float:
	assert(constitution_score >= 3 and constitution_score <= 18)
	return float(constitution_score)

static func can_apply_strain(current: float, permanent: float, additional: float, constitution_score: int) -> bool:
	assert(current >= 0.0 and permanent >= 0.0 and additional >= 0.0)
	return current + permanent + additional <= strain_capacity(constitution_score) + 0.00001

static func strain_after_rest(current: float, permanent: float, rested_eight_hours: bool, warm_fed_comfortable: bool) -> float:
	assert(current >= 0.0 and permanent >= 0.0)
	if rested_eight_hours and warm_fed_comfortable:
		return maxf(permanent, current - 1.0)
	return current

static func natural_healing(current_hp: int, maximum_hp: int, level: int, adequate_rest: bool, frail: bool = false) -> int:
	assert(current_hp >= 0 and maximum_hp >= 1 and level >= 1)
	if not adequate_rest or frail:
		return current_hp
	return mini(maximum_hp, current_hp + level)
