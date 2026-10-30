class_name CWNCharacter
extends RefCounted

## Character creation and progression arithmetic for the CWN implementation.
##
## Dice are arguments, never rolled here: a table roll and its replay must agree, which is
## impossible if the module reaches for its own RNG. `cwn_progression.gd` already owns the
## advancement side; this file adds what creation needs and delegates the rest.

const ATTRIBUTES := ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
const ARRAY_METHOD := [14, 12, 11, 10, 9, 7]
const SUBSTITUTION := 14

## 3d6 in order, once per attribute. `substitute_at` picks which rolled score is replaced by 14;
## pass -1 for none. A score may be substituted only before the free-skill step, which is why the
## caller has to say so explicitly rather than having the module do it silently.
static func from_rolls(rolls: Array, substitute_at: int = -1) -> Dictionary:
	assert(rolls.size() == 6, "six attributes need six rolls")
	var scores: Array = []
	var substituted := false
	for i in rolls.size():
		var score: int = int(rolls[i])
		assert(score >= 3 and score <= 18, "3d6 cannot leave 3..18")
		if i == substitute_at and not substituted:
			score = max(score, SUBSTITUTION) if score < SUBSTITUTION else score
			substituted = true
		scores.append(score)
	var attributes := {}
	var modifiers := {}
	for i in ATTRIBUTES.size():
		attributes[ATTRIBUTES[i]] = scores[i]
		modifiers[ATTRIBUTES[i]] = CWNRules.ability_modifier(scores[i])
	return {"attributes": attributes, "modifiers": modifiers, "substituted": substituted}

## The optional array. Taking the array forfeits the 14 substitution, so this returns
## `substituted: true` to record that the option was spent.
static func from_array(order: Array = ARRAY_METHOD) -> Dictionary:
	assert(order.size() == 6, "the array has six values")
	var pool: Array = ARRAY_METHOD.duplicate()
	var attributes := {}
	var modifiers := {}
	for i in ATTRIBUTES.size():
		var value: int = int(order[i])
		assert(pool.has(value), "array values are 14,12,11,10,9,7 - got %s" % value)
		pool.erase(value)
		attributes[ATTRIBUTES[i]] = value
		modifiers[ATTRIBUTES[i]] = CWNRules.ability_modifier(value)
	return {"attributes": attributes, "modifiers": modifiers, "substituted": true}

## Creation-time skill picks: the first pick is level-0, the second level-1, and from the third
## pick onward the player must pick a different skill. Nothing may begin above level-1.
static func creation_skill_pick(current_rank: int) -> Dictionary:
	if current_rank < 0:
		return {"rank": 0, "allowed": true, "reason": "first pick"}
	if current_rank == 0:
		return {"rank": 1, "allowed": true, "reason": "second pick"}
	return {"rank": current_rank, "allowed": false, "reason": "already level-1 at creation"}

## 1d6 + Constitution modifier, never below 1; Hard to Kill adds +2 to the roll.
static func max_hit_points(roll: int, con_modifier: int, hard_to_kill: bool = false) -> int:
	assert(roll >= 1 and roll <= 6, "hit points are rolled on 1d6")
	var total := roll + (2 if hard_to_kill else 0) + con_modifier
	return max(1, total)

## Target is 15 minus the better of two modifiers at level 1, and one lower per level after that.
static func save_target(kind: String, level: int, modifiers: Dictionary) -> int:
	assert(level >= 1, "levels start at 1")
	var best := 0
	match kind.to_lower():
		"physical":
			best = max(int(modifiers.get("STR", 0)), int(modifiers.get("CON", 0)))
		"evasion":
			best = max(int(modifiers.get("DEX", 0)), int(modifiers.get("INT", 0)))
		"mental":
			best = max(int(modifiers.get("WIS", 0)), int(modifiers.get("CHA", 0)))
		"luck":
			best = 0
		_:
			assert(false, "unknown save type: %s" % kind)
	return 15 - (level - 1) - best

## NPCs use one target instead: 15 minus half their hit dice, rounded down.
static func npc_save_target(hit_dice: int) -> int:
	assert(hit_dice >= 1, "NPCs have at least one hit die")
	return 15 - int(floor(float(hit_dice) / 2.0))

## Extra languages: level-0 grants one, level-1 grants two, per skill.
static func extra_languages(know_rank: int, connect_rank: int) -> int:
	var count := 0
	if know_rank >= 1:
		count += 2
	elif know_rank == 0:
		count += 1
	if connect_rank >= 1:
		count += 2
	elif connect_rank == 0:
		count += 1
	return count
