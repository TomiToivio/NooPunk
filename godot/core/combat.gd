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

## The damage itself is not decided here: `godot/core/cwn_combat_rules.gd` owns Shock, Trauma and the
## damage floor, and is pinned to `src/rules/cwn_core.py`. This file owns the turn, the grid, the
## attacks and the bookkeeping.
const Injury := preload("res://godot/core/cwn_combat_rules.gd")

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
		# Two Armour Classes, because CWN gives a combatant one against melee and one against
		# ranged fire, and cover only ever modifies the one being attacked.
		"weapon_kind": String(spec.get("weapon_kind", "ranged")),
		"ac_melee": int(spec.get("ac_melee", spec.get("ac", 10))),
		"ac_ranged": int(spec.get("ac_ranged", spec.get("ac", 10))),
		# Shock and Trauma are weapon facts, and a non-lethal attack rolls no Trauma Die at all.
		"lethal": bool(spec.get("lethal", true)),
		"trauma_rating": int(spec.get("trauma_rating", 1)),
		"trauma_target": int(spec.get("trauma_target", Injury.DEFAULT_TRAUMA_TARGET)),
		"shock_value": int(spec.get("shock_value", 0)),
		"shock_ac": int(spec.get("shock_ac", Injury.SHOCK_ANY_AC)),
		# -1 is an unlimited magazine; 0 is an empty one that must be reloaded.
		"ammo": int(spec.get("ammo", -1)),
		"ammo_max": int(spec.get("ammo", -1)),
		"traumatic_this_scene": false,
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
	if int(actor["ammo"]) == 0:
		return {"ok": false, "reason": "empty_magazine"}
	var kind := String(actor.get("weapon_kind", "ranged"))
	var base_ac := int(target["ac_melee"]) if kind == "melee" else int(target["ac_ranged"])
	var ac := base_ac + int(target.get("cover", 0))
	var roll := adapter.attack_roll(
		int(actor["attack_attribute"]),
		int(actor["combat_rank"]),
		int(actor["attack_bonus"]),
		ac
	)
	actor["acted"] = true
	var hit := bool(roll.get("hit", false))
	if int(actor["ammo"]) > 0:
		actor["ammo"] = int(actor["ammo"]) - 1
	# A non-lethal attack rolls no Trauma Die (SRD), so it can never be Traumatic.
	var trauma_die := -1
	if hit and bool(actor["lethal"]):
		trauma_die = adapter.roll_die(6)
	var raw := 0
	if hit:
		var damage_spec: Array = actor["damage"]
		raw = adapter.roll_dice(int(damage_spec[0]), int(damage_spec[1])) + int(damage_spec[2])
	var resolved := Injury.resolve_attack(
		hit, raw, trauma_die, int(actor["trauma_rating"]), int(actor["trauma_target"]),
		int(actor["shock_value"]), int(actor["shock_ac"]), int(target["ac_melee"]),
		adapter.attribute_modifier(int(actor["attack_attribute"]))
	)
	var dealt := int(resolved["damage"])
	var entry := {
		"actor": actor_id, "action": "attack", "target": target_id,
		"roll": roll, "hit": hit, "armor_class": ac,
		"damage": dealt, "shock": int(resolved["shock"]), "trauma": bool(resolved["trauma"]),
		"trauma_die": int(resolved["trauma_die"]), "ammo": int(actor["ammo"]),
	}
	if dealt > 0:
		target["hp"] = max(0, int(target["hp"]) - dealt)
		if bool(resolved["trauma"]):
			# The victim stays vulnerable to a Major Injury for the rest of the scene.
			target["traumatic_this_scene"] = true
		if int(target["hp"]) == 0:
			target["alive"] = false
		entry["target_hp"] = target["hp"]
	log.append(entry)
	_refresh_over()
	return entry

## Spend the Main action reloading. A magazine is a resource; running dry mid-fight is a real state.
func reload(actor_id: String) -> Dictionary:
	var actor: Dictionary = actors.get(actor_id, {})
	if actor.is_empty() or not bool(actor.get("alive", false)):
		return {"ok": false, "reason": "no_such_actor"}
	if actor_id != current_id():
		return {"ok": false, "reason": "not_this_actors_turn"}
	if bool(actor["acted"]):
		return {"ok": false, "reason": "action_already_used"}
	if int(actor["ammo_max"]) < 0:
		return {"ok": false, "reason": "no_magazine"}
	actor["acted"] = true
	actor["ammo"] = int(actor["ammo_max"])
	var entry := {"actor": actor_id, "action": "reload", "ammo": actor["ammo"]}
	log.append(entry)
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
