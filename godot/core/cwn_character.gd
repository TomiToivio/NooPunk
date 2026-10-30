## Cities Without Number: character creation, as the engine needs it.
##
## Port of `src/rules/cwn_character.py` (source of record). CWN SRD is CC0; the paid book's prose is
## not reproduced here — this file states procedures and cites the chapter, nothing more.
##
## Creation (CWN "Character Creation", p8-31 of the deluxe edition):
## * six attributes, 3..18, rolled 3d6 in order; or the fixed array 14/12/11/10/9/7;
## * a rolled set may replace **one** score with 14, and a set built from the array may not —
##   the array is itself the concession;
## * six skill picks, and **the third and later pick of one skill is not a level**: during creation
##   no skill may exceed rank 1, so the pick has to go elsewhere;
## * modifiers run -2..+2; a Focus or cyberware bonus may not push past those caps unless the
##   source says so explicitly.
extends RefCounted
class_name CwnCharacter

const ATTRIBUTES := ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
const ARRAY := [14, 12, 11, 10, 9, 7]
const SUBSTITUTE_SCORE := 14
const MAX_CREATION_SKILL_LEVEL := 1
const MODIFIER_FLOOR := -2
const MODIFIER_CEILING := 2
const ATTRIBUTE_MIN := 3
const ATTRIBUTE_MAX := 18

const Kernel := preload("res://src/godot/cwn_rules.gd")

## Six 3d6 rolls taken in order, one per attribute. Dice enter as values, so a table roll and a
## replay agree; this function never rolls anything itself.
static func roll_attributes(dice: Array) -> Dictionary:
	if dice.size() != ATTRIBUTES.size() * 3:
		return {"ok": false, "reason": "eighteen_dice_required"}
	var scores := {}
	for index in range(ATTRIBUTES.size()):
		var chunk := dice.slice(index * 3, index * 3 + 3)
		var total := 0
		for die in chunk:
			if int(die) < 1 or int(die) > 6:
				return {"ok": false, "reason": "each_die_is_1_to_6", "got": int(die)}
			total += int(die)
		scores[ATTRIBUTES[index]] = total
	return {"ok": true, "scores": scores}

## Replace one rolled score with 14: once, and never when the array was used.
static func substitute_fourteen(scores: Dictionary, attribute: String,
		already_substituted: bool = false, array_used: bool = false) -> Dictionary:
	if not (attribute in ATTRIBUTES):
		return {"ok": false, "reason": "unknown_attribute", "attribute": attribute}
	if array_used:
		return {"ok": false, "reason": "the_array_forfeits_the_substitute_fourteen_option"}
	if already_substituted:
		return {"ok": false, "reason": "only_one_score_may_be_substituted"}
	for name in ATTRIBUTES:
		if not scores.has(name):
			return {"ok": false, "reason": "all_six_attributes_are_required", "missing": name}
	var result := scores.duplicate()
	result[attribute] = SUBSTITUTE_SCORE
	return {"ok": true, "scores": result}

## The fixed array must be a permutation: no inventing a better spread, no dropping the low score.
static func assign_array(assignment: Dictionary) -> Dictionary:
	for name in ATTRIBUTES:
		if not assignment.has(name):
			return {"ok": false, "reason": "all_six_attributes_are_required", "missing": name}
	var given: Array = []
	for name in ATTRIBUTES:
		given.append(int(assignment[name]))
	given.sort()
	var expected := ARRAY.duplicate()
	expected.sort()
	if given != expected:
		return {"ok": false, "reason": "attributes_must_be_a_permutation_of_the_array",
			"expected": ARRAY}
	var out := {}
	for name in ATTRIBUTES:
		out[name] = int(assignment[name])
	return {"ok": true, "scores": out}

## The attribute modifier plus any bonus, capped at -2..+2 unless the source says otherwise.
static func effective_modifier(base_score: int, bonus: int = 0, uncapped: bool = false) -> int:
	var modifier: int = Kernel.ability_modifier(base_score) + bonus
	if uncapped:
		return modifier
	return clampi(modifier, MODIFIER_FLOOR, MODIFIER_CEILING)

## Hit points at level 1: 1d6 + CON modifier, minimum 1. Later levels add their roll + CON mod.
static func hit_points(level: int, constitution: int, rolls: Array = []) -> int:
	var con_mod := Kernel.ability_modifier(constitution)
	var total := maxi(1, 6 + con_mod) if level >= 1 else 0
	for roll in rolls:
		total += maxi(1, int(roll) + con_mod)
	return total

## The four saves, by the Without Number formula the baseline adopted.
static func saves(level: int, attributes: Dictionary) -> Dictionary:
	return {
		"Physical": Kernel.saving_throw_target("Physical", level, attributes),
		"Evasion": Kernel.saving_throw_target("Evasion", level, attributes),
		"Mental": Kernel.saving_throw_target("Mental", level, attributes),
		"Luck": Kernel.saving_throw_target("Luck", level, attributes),
	}

## The six creation skill picks. Tracking the cap here stops a caller from quietly handing out
## rank 2 at creation.
class SkillPool extends RefCounted:
	var levels: Dictionary = {}

	func can_pick(skill: String) -> bool:
		if not levels.has(skill):
			return true
		if int(levels[skill]) < CwnCharacter.MAX_CREATION_SKILL_LEVEL:
			return true
		for name in levels.keys():
			if String(name) != skill and int(levels[name]) < CwnCharacter.MAX_CREATION_SKILL_LEVEL:
				return true
		return false

	## Spend one pick; returns the resulting rank, or -1 when the pick is refused.
	func pick(skill: String) -> int:
		if skill.is_empty():
			return -1
		if not levels.has(skill):
			levels[skill] = 0
			return 0
		var current := int(levels[skill])
		if current < CwnCharacter.MAX_CREATION_SKILL_LEVEL:
			levels[skill] = current + 1
			return int(levels[skill])
		return -1  # already at the creation cap: the pick must go elsewhere

## --- Creation and consequence helpers merged from the compatibility tree (#791) ---------------
## These are views over the same rules above, not a second implementation: `from_rolls` delegates to
## `roll_attributes`, `from_array` to `assign_array`. They exist because callers and tests written
## against the `src/godot/` copy used this shape, and a merge should not make working call sites
## rewrite themselves for no rules reason.

## Six rolls taken in order, with the optional single 14 substitution applied.
static func from_rolls(rolls: Array, substitute_at: int = -1) -> Dictionary:
	var scores := {}
	for index in range(mini(rolls.size(), ATTRIBUTES.size())):
		var score := int(rolls[index])
		if index == substitute_at:
			score = maxi(score, SUBSTITUTE_SCORE)
		scores[ATTRIBUTES[index]] = score
	var modifiers := {}
	for name in ATTRIBUTES:
		modifiers[name] = Kernel.ability_modifier(int(scores.get(name, 10)))
	return {"attributes": scores, "modifiers": modifiers,
		"substituted": substitute_at >= 0}

## The fixed array assigned in attribute order, which forfeits the substitution.
static func from_array(order: Array = ARRAY) -> Dictionary:
	var assignment := {}
	for index in range(mini(order.size(), ATTRIBUTES.size())):
		assignment[ATTRIBUTES[index]] = int(order[index])
	var result := assign_array(assignment)
	return {"attributes": result.get("scores", {}), "modifiers": {},
		"substituted": true, "ok": result.get("ok", false)}

## The creation-time pick rule: first pick rank 0, second rank 1, third refused.
static func creation_skill_pick(current_rank: int) -> Dictionary:
	if current_rank < 0:
		return {"rank": 0, "allowed": true, "reason": "first pick"}
	if current_rank == 0:
		return {"rank": 1, "allowed": true, "reason": "second pick"}
	return {"rank": current_rank, "allowed": false, "reason": "already level-1 at creation"}

## A new character's maximum hit points: **1d6** plus the Constitution modifier, never below 1.
## `hit_points()` above answers a different question (total at a level, with average allowance);
## this one exists because assuming a 6 at level 1 hands every character three extra hit points and
## is not what the source says.
static func max_hit_points(roll: int, con_modifier: int, hard_to_kill: bool = false) -> int:
	var total := clampi(roll, 1, 6) + (2 if hard_to_kill else 0) + con_modifier
	return maxi(1, total)

## A save target from modifiers rather than scores, for callers holding a modifier set.
## Must agree with `saves()`; `test_cwn_engine` asserts the agreement so they cannot drift.
static func save_target(kind: String, level: int, modifiers: Dictionary) -> int:
	var best := 0
	match kind.to_lower():
		"physical":
			best = maxi(int(modifiers.get("STR", 0)), int(modifiers.get("CON", 0)))
		"evasion":
			best = maxi(int(modifiers.get("DEX", 0)), int(modifiers.get("INT", 0)))
		"mental":
			best = maxi(int(modifiers.get("WIS", 0)), int(modifiers.get("CHA", 0)))
		"luck":
			best = 0
		_:
			return 15 - (level - 1)
	return 15 - (level - 1) - best

## NPCs use one target: 15 minus half their hit dice, rounded down.
static func npc_save_target(hit_dice: int) -> int:
	return 15 - int(floor(float(maxi(1, hit_dice)) / 2.0))

## Extra languages beyond the campaign lingua franca: level-0 grants one, level-1 grants two.
static func extra_languages(know_rank: int, connect_rank: int) -> int:
	var count := 0
	count += 2 if know_rank >= 1 else (1 if know_rank == 0 else 0)
	count += 2 if connect_rank >= 1 else (1 if connect_rank == 0 else 0)
	return count
