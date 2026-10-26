class_name CWNRules
extends RefCounted
## Portable CWN SRD mechanics. No copy of source prose/content.
## Current NoöPunk baseline: data/rules/without_number.json

const DATA_PATH := "res://data/rules/without_number.json"
const ATTRIBUTES := ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

static func ability_modifier(score: int) -> int:
	assert(score >= 3 and score <= 18, "CWN attributes are 3..18")
	if score == 3:
		return -2
	if score <= 7:
		return -1
	if score <= 13:
		return 0
	if score <= 17:
		return 1
	return 2

static func roll_skill(rng: RandomNumberGenerator, score: int, rank: int, difficulty: int, circumstances: int = 0, aid: int = 0) -> Dictionary:
	assert(rank >= -1 and rank <= 4, "Untrained is -1; trained ranks 0..4")
	assert(circumstances >= -2 and circumstances <= 2, "Circumstances cap at +/-2")
	assert(aid >= 0 and aid <= 1, "Assistance is capped at +1")
	var first := rng.randi_range(1, 6)
	var second := rng.randi_range(1, 6)
	return evaluate_skill(first, second, score, rank, difficulty, circumstances, aid)

static func evaluate_skill(first: int, second: int, score: int, rank: int, difficulty: int, circumstances: int = 0, aid: int = 0) -> Dictionary:
	assert(first >= 1 and first <= 6 and second >= 1 and second <= 6)
	assert(rank >= -1 and rank <= 4)
	assert(circumstances >= -2 and circumstances <= 2)
	assert(aid >= 0 and aid <= 1)
	var total := first + second + ability_modifier(score) + rank + circumstances + aid
	return {"dice": [first, second], "total": total, "difficulty": difficulty, "success": total >= difficulty}

static func opposed_result(pc_total: int, opponent_total: int) -> Dictionary:
	# CWN opposed ties favor the PC.
	return {"pc_wins": pc_total >= opponent_total, "tie": pc_total == opponent_total}

static func saving_throw_target(kind: String, level: int, attributes: Dictionary) -> int:
	assert(level >= 1)
	var best := 0
	match kind:
		"Physical":
			best = maxi(ability_modifier(int(attributes["STR"])), ability_modifier(int(attributes["CON"])))
		"Evasion":
			best = maxi(ability_modifier(int(attributes["DEX"])), ability_modifier(int(attributes["INT"])))
		"Mental":
			best = maxi(ability_modifier(int(attributes["WIS"])), ability_modifier(int(attributes["CHA"])))
		"Luck":
			pass
		_:
			assert(false, "Unknown saving throw type")
	return 16 - level - best

static func evaluate_save(die: int, target: int, modifier: int = 0) -> bool:
	assert(die >= 1 and die <= 20)
	if die == 1:
		return false
	if die == 20:
		return true
	return die + modifier >= target

static func evaluate_attack(die: int, attack_bonus: int, attribute_bonus: int, combat_rank: int, armor_class: int) -> Dictionary:
	assert(die >= 1 and die <= 20)
	assert(combat_rank >= -2 and combat_rank <= 4)
	var total := die + attack_bonus + attribute_bonus + combat_rank
	return {"die": die, "total": total, "armor_class": armor_class, "hit": total >= armor_class}

static func check_hacking_reach(is_connected: bool, within_wireless_range: bool, has_line_of_sight: bool, available_cpu: int, available_access: int, required_access: int, uses_vr_crown: bool = false) -> Dictionary:
	# Prerequisites only; actual programs, node security, costs and alarms
	# remain governed by the source material, not fabricated here.
	var reachable := is_connected or (within_wireless_range and has_line_of_sight)
	var wireless := not is_connected and reachable
	var allowed := reachable and available_cpu > 0 and available_access >= required_access
	return {"allowed": allowed, "reachable": reachable, "wireless": wireless, "check_modifier": (-2 if wireless else 0) - (1 if uses_vr_crown else 0)}
