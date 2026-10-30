## Turn-based tactical combat kernel for the #749 vertical slice.
##
## Scope: one controllable PC plus enemies, on a grid, with the CWN action economy cut down to
## what the slice actually uses — one Move and one Main action per turn.
##
## It deliberately does NOT implement Trauma/Shock, mortal injuries, suppressive fire, automatic
## weapons, vehicles or morale. Those exist in the Python rules layer (`src/rules/`) and are
## listed as `later` in `docs/GODOT_MVP_AUDIT.md`. Inventing a second, thinner version of them
## here would be exactly the drift the audit warns about.
##
## Determinism: every roll goes through `RulesAdapter`, which owns the seeded `NoopunkDice`. A
## combat started from the same seed and given the same calls produces the same log.
extends RefCounted
class_name NoopunkCombat

## One square is 2 m, so CWN's 10 m Move action is five squares.
const SQUARE_METRES := 2.0
const DEFAULT_MOVE_SQUARES := 5

var adapter: RulesAdapter
var bounds := Vector2i(12, 12)
var actors: Dictionary = {}
var order: Array = []
var round_number := 1
var turn := 0
var log: Array = []
var over := false
var _outcome := ""

func _init(rules_adapter: RulesAdapter) -> void:
	adapter = rules_adapter

## Register a combatant. Returns false and records why if the spec is unusable.
func add_actor(spec: Dictionary) -> bool:
	var id := String(spec.get("id", ""))
	if id.is_empty() or actors.has(id):
		push_error("NoopunkCombat: missing or duplicate actor id")
		return false
	var side := String(spec.get("side", ""))
	if side != "pc" and side != "enemy":
		push_error("NoopunkCombat: side must be 'pc' or 'enemy'")
		return false
	var hp := int(spec.get("hp", 0))
	if hp <= 0:
		push_error("NoopunkCombat: hp must be positive")
		return false
	actors[id] = {
		"id": id,
		"side": side,
		"pos": spec.get("pos", Vector2i.ZERO),
		"hp_max": hp,
		"hp": hp,
		"ac": int(spec.get("ac", 10)),
		"dex": int(spec.get("dex", 10)),
		"attack_attribute": int(spec.get("attack_attribute", spec.get("dex", 10))),
		"combat_rank": int(spec.get("combat_rank", 0)),
		"attack_bonus": int(spec.get("attack_bonus", 0)),
		"damage": spec.get("damage", [1, 6, 0]),
		"move_squares": int(spec.get("move_squares", DEFAULT_MOVE_SQUARES)),
		"cover": int(spec.get("cover", 0)),
		"alive": true,
		"moved": false,
		"acted": false,
	}
	return true

## Roll initiative (1d8 + DEX modifier), highest first. Ties break on DEX, then on id.
func start() -> Array:
	order.clear()
	var scored: Array = []
	for id in actors.keys():
		var actor: Dictionary = actors[id]
		var roll := adapter.roll_die(8)
		var initiative := roll + adapter.attribute_modifier(int(actor["dex"]))
		scored.append({"id": id, "initiative": initiative, "dex": int(actor["dex"])})
	scored.sort_custom(func(a, b):
		if int(a["initiative"]) != int(b["initiative"]):
			return int(a["initiative"]) > int(b["initiative"])
		if int(a["dex"]) != int(b["dex"]):
			return int(a["dex"]) > int(b["dex"])
		return String(a["id"]) < String(b["id"])
	)
	for row in scored:
		order.append(String(row["id"]))
	turn = 0
	round_number = 1
	_refresh_over()
	return order

func current_id() -> String:
	if order.is_empty() or over:
		return ""
	return String(order[turn % order.size()])

func current() -> Dictionary:
	var id := current_id()
	return actors.get(id, {})

## Chebyshev distance: diagonal steps cost one square, which keeps the slice's movement simple
## without pretending to be CWN's metre-level rule.
func distance(a: Vector2i, b: Vector2i) -> int:
	return max(abs(a.x - b.x), abs(a.y - b.y))

func occupied(pos_key: Vector2i, ignore_id: String = "") -> bool:
	for id in actors.keys():
		if String(id) == ignore_id:
			continue
		if bool(actors[id]["alive"]) and actors[id]["pos"] == pos_key:
			return true
	return false

func move(actor_id: String, to: Vector2i) -> Dictionary:
	var actor: Dictionary = actors.get(actor_id, {})
	if actor.is_empty() or not bool(actor.get("alive", false)):
		return {"ok": false, "reason": "no_such_actor"}
	if actor_id != current_id():
		return {"ok": false, "reason": "not_this_actors_turn"}
	if bool(actor["moved"]):
		return {"ok": false, "reason": "move_already_used"}
	if to.x < 0 or to.y < 0 or to.x >= bounds.x or to.y >= bounds.y:
		return {"ok": false, "reason": "out_of_bounds"}
	if occupied(to, actor_id):
		return {"ok": false, "reason": "square_occupied"}
	var steps := distance(actor["pos"], to)
	if steps > int(actor["move_squares"]):
		return {"ok": false, "reason": "beyond_move", "steps": steps}
	actor["pos"] = to
	actor["moved"] = true
	var entry := {"actor": actor_id, "action": "move", "to": to, "steps": steps}
	log.append(entry)
	return {"ok": true, "steps": steps}

## Attack resolution goes through `RulesAdapter.attack_roll`; cover is added to the target's AC.
func attack(actor_id: String, target_id: String) -> Dictionary:
	var actor: Dictionary = actors.get(actor_id, {})
	var target: Dictionary = actors.get(target_id, {})
	if actor.is_empty() or target.is_empty():
		return {"ok": false, "reason": "no_such_actor"}
	if actor_id != current_id():
		return {"ok": false, "reason": "not_this_actors_turn"}
	if not bool(target.get("alive", false)):
		return {"ok": false, "reason": "target_already_down"}
	if bool(actor["acted"]):
		return {"ok": false, "reason": "action_already_used"}
	var ac := int(target["ac"]) + int(target.get("cover", 0))
	var roll := adapter.attack_roll(
		int(actor["attack_attribute"]),
		int(actor["combat_rank"]),
		int(actor["attack_bonus"]),
		ac
	)
	actor["acted"] = true
	var entry := {
		"actor": actor_id, "action": "attack", "target": target_id,
		"roll": roll, "hit": bool(roll.get("hit", false)),
	}
	if bool(roll.get("hit", false)):
		var damage_spec: Array = actor["damage"]
		var dice_total := adapter.roll_dice(int(damage_spec[0]), int(damage_spec[1]))
		var dealt: int = max(1, dice_total + int(damage_spec[2]))
		target["hp"] = max(0, int(target["hp"]) - dealt)
		if int(target["hp"]) == 0:
			target["alive"] = false
		entry["damage"] = dealt
		entry["target_hp"] = target["hp"]
	log.append(entry)
	_refresh_over()
	return entry

func end_turn() -> void:
	if over or order.is_empty():
		return
	var guard := 0
	while guard < order.size():
		guard += 1
		turn += 1
		if turn % order.size() == 0:
			round_number += 1
		var id := String(order[turn % order.size()])
		var actor: Dictionary = actors[id]
		if bool(actor["alive"]):
			actor["moved"] = false
			actor["acted"] = false
			return
	# Nobody alive left to act.
	_refresh_over()

func _refresh_over() -> void:
	var pcs := 0
	var enemies := 0
	for id in actors.keys():
		if not bool(actors[id]["alive"]):
			continue
		if String(actors[id]["side"]) == "pc":
			pcs += 1
		else:
			enemies += 1
	if enemies == 0:
		over = true
		_outcome = "pcs_win"
	elif pcs == 0:
		over = true
		_outcome = "enemies_win"

func is_over() -> bool:
	return over

func outcome() -> String:
	return _outcome

func living(side: String) -> Array:
	var out: Array = []
	for id in actors.keys():
		if bool(actors[id]["alive"]) and String(actors[id]["side"]) == side:
			out.append(id)
	return out
