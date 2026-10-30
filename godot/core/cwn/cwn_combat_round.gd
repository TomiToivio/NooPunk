class_name CWNCombatRound
extends RefCounted

## CWN Deluxe p.33-34: side initiative and action budgets.
## This is a portable rules procedure, not a tactical scene or custom action system.
## Full CWN combat also requires equipment, weapon effects, movement geometry,
## Morale, special maneuvers, healing and cyberware modules.
const HUMAN_MOVE_METERS := 10.0
var round_number: int = 1
var side_order: Array[String] = []
var active_side_index: int = 0
var participants: Dictionary = {}
var sides: Dictionary = {}

## Each entry is {id, side, dexterity_modifier?, movement_meters?}.
## pcs_side marks the PC side to break ties in its favor.
func initialize(actors: Array, pcs_side: String, dice_by_side: Dictionary) -> bool:
	var next_actors: Dictionary = {}
	var next_sides: Dictionary = {}
	for raw in actors:
		if not raw is Dictionary:
			return false
		var id := str(raw.get("id", ""))
		var side := str(raw.get("side", ""))
		if id.is_empty() or side.is_empty() or next_actors.has(id):
			return false
		var dex: int = int(raw.get("dexterity_modifier", 0))
		var speed: float = float(raw.get("movement_meters", HUMAN_MOVE_METERS))
		if speed < 0.0 or not is_finite(speed):
			return false
		next_actors[id] = {"side": side, "main": true, "move": true,
			"moved_meters": 0.0, "movement_meters": speed, "done": false}
		if not next_sides.has(side):
			next_sides[side] = {"best_dex": dex}
		else:
			next_sides[side]["best_dex"] = maxi(int(next_sides[side]["best_dex"]), dex)
	if not next_sides.has(pcs_side) or dice_by_side.size() != next_sides.size():
		return false
	var next_order: Array[String] = []
	for side in next_sides:
		if not dice_by_side.has(side):
			return false
		var die: int = int(dice_by_side[side])
		if die < 1 or die > 8:
			return false
		next_sides[side]["initiative"] = die + int(next_sides[side]["best_dex"])
		next_order.append(side)
	next_order.sort_custom(func(a: String, b: String) -> bool:
		var score_a: int = int(next_sides[a]["initiative"])
		var score_b: int = int(next_sides[b]["initiative"])
		if score_a == score_b:
			return a == pcs_side
		return score_a > score_b
	)
	participants = next_actors
	sides = next_sides
	side_order = next_order
	active_side_index = 0
	round_number = 1
	return true

func active_side() -> String:
	return side_order[active_side_index] if not side_order.is_empty() else ""

func may_act(id: String) -> bool:
	return participants.has(id) and str(participants[id]["side"]) == active_side() and not bool(participants[id]["done"])

## Main or Move may be spent once each. A Main can supply a second Move.
## Actual named CWN maneuvers and their additional requirements remain in their own procedures.
func spend_action(id: String, category: String) -> bool:
	if not may_act(id):
		return false
	var actor: Dictionary = participants[id]
	match category:
		"Main":
			if not bool(actor["main"]):
				return false
			actor["main"] = false
		"Move":
			if bool(actor["move"]):
				actor["move"] = false
			elif bool(actor["main"]):
				actor["main"] = false
			else:
				return false
		"On Turn", "Instant":
			# Plausibility and any source-defined costs belong to the action definition.
			return true
		_:
			return false
	return true

func move_actor(id: String, meters: float) -> bool:
	if meters <= 0.0 or not is_finite(meters) or not may_act(id):
		return false
	var actor: Dictionary = participants[id]
	if meters > float(actor["movement_meters"]):
		return false
	if not spend_action(id, "Move"):
		return false
	actor["moved_meters"] = float(actor["moved_meters"]) + meters
	return true

func finish_actor(id: String) -> bool:
	if not may_act(id):
		return false
	participants[id]["done"] = true
	return true

func advance_side() -> bool:
	if side_order.is_empty():
		return false
	for id in participants:
		if str(participants[id]["side"]) == active_side() and not bool(participants[id]["done"]):
			return false
	active_side_index += 1
	if active_side_index >= side_order.size():
		active_side_index = 0
		round_number += 1
		for id in participants:
			participants[id]["main"] = true
			participants[id]["move"] = true
			participants[id]["moved_meters"] = 0.0
			participants[id]["done"] = false
	return true

func snapshot() -> Dictionary:
	return {"round_number": round_number, "side_order": side_order.duplicate(),
		"active_side_index": active_side_index, "participants": participants.duplicate(true),
		"sides": sides.duplicate(true)}
