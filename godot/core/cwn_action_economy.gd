## Vanilla CWN turn economy and common combat action accounting.
## https://cwn.quadrifons.com/rules-of-the-game/combat/combat-actions/
class_name CwnActionEconomy
extends RefCounted

const MAIN := "main"
const MOVE := "move"
const ON_TURN := "on_turn"
const INSTANT := "instant"
const COMMON := {
	"melee_attack": MAIN, "ranged_attack": MAIN, "swarm_attack": MAIN,
	"fighting_withdrawal": MAIN, "use_skill": MAIN, "ready_item": MAIN,
	"stow_item": MAIN, "reload_firearm": MAIN,
	"run": MOVE, "screen_ally": MOVE, "pick_up_item": MOVE,
	"stand_up": MOVE, "hold_action": MOVE,
	"go_prone": ON_TURN, "drop_item": INSTANT,
	"snap_attack": INSTANT, "total_defense": INSTANT,
	"charge": "both"
}
var main_remaining := 1
var move_remaining := 1
var held := false
var defense := false
var withdrawal := false
var prone := false

func new_round() -> void:
	main_remaining = 1
	move_remaining = 1
	held = false
	defense = false
	withdrawal = false

func can_act(action: String) -> bool:
	if not COMMON.has(action):
		return false
	match COMMON[action]:
		MAIN: return main_remaining > 0
		MOVE: return move_remaining > 0 or main_remaining > 0
		"both": return main_remaining > 0 and move_remaining > 0
		INSTANT:
			return main_remaining > 0 if action in ["snap_attack", "total_defense"] else true
		ON_TURN: return true
	return false

func take_action(action: String) -> Dictionary:
	if not can_act(action):
		return {"ok": false, "reason": "unavailable_action"}
	match COMMON[action]:
		MAIN: main_remaining -= 1
		MOVE:
			if move_remaining > 0:
				move_remaining -= 1
			else:
				main_remaining -= 1
		"both":
			main_remaining -= 1
			move_remaining -= 1
		INSTANT:
			if action in ["snap_attack", "total_defense"]:
				main_remaining -= 1
		ON_TURN: pass
	match action:
		"hold_action": held = true
		"total_defense": defense = true
		"fighting_withdrawal": withdrawal = true
		"go_prone": prone = true
		"stand_up": prone = false
	return {"ok": true, "main_remaining": main_remaining, "move_remaining": move_remaining}

func ranged_attack_allowed(two_handed: bool, enemy_in_melee: bool) -> Dictionary:
	if two_handed and enemy_in_melee:
		return {"allowed": false, "modifier": 0}
	return {"allowed": true, "modifier": -4 if enemy_in_melee else 0}

func movement_meters(base_speed: float = 10.0) -> float:
	return base_speed * (0.5 if prone else 1.0)

func armor_class_modifier(attack_is_melee: bool) -> int:
	return (2 if defense else 0) + ((-2 if attack_is_melee else 2) if prone else 0)

static func swarm_bonus(other_attackers: int) -> Dictionary:
	var allies := clampi(other_attackers, 0, 3)
	return {"attack": allies * 2, "damage": allies}

static func charge_modifier(distance_meters: float) -> Dictionary:
	if distance_meters < 3.0:
		return {"ok": false}
	return {"ok": true, "attack": 2, "armor_class": -2}
