class_name CWNCombatTurn
extends RefCounted
## Vanilla CWN combat initiative and action budget.
## https://cwn.quadrifons.com/rules-of-the-game/combat/combat-initiative/
## https://cwn.quadrifons.com/rules-of-the-game/combat/combat-actions/
## Independent of UI; no NoöPunk-specific rule alterations.

var main_available: bool = true
var move_available: bool = true
var holding: bool = false

static func initiative_total(d8: int, best_dex_modifier: int) -> int:
	assert(d8 >= 1 and d8 <= 8)
	return d8 + best_dex_modifier

static func side_precedes(first_total: int, first_is_pc: bool, second_total: int, second_is_pc: bool) -> bool:
	if first_total != second_total:
		return first_total > second_total
	if first_is_pc != second_is_pc:
		return first_is_pc
	return false # Unresolved same-side tie; referee controls member order.

func reset_round() -> void:
	main_available = true
	move_available = true
	holding = false

func spend_main() -> bool:
	if holding or not main_available:
		return false
	main_available = false
	return true

func spend_move() -> bool:
	if holding:
		return false
	if move_available:
		move_available = false
		return true
	# Published rule: trade the Main action for another Move.
	return spend_main()

func can_snap_attack() -> bool:
	return main_available and not holding

func snap_attack() -> bool:
	if not can_snap_attack():
		return false
	main_available = false
	return true # Caller applies the published -4 hit modifier.

func total_defense() -> bool:
	if not main_available or holding:
		return false
	main_available = false
	return true # Caller applies +2 to both ACs and Shock immunity.

func charge() -> bool:
	if holding or not main_available or not move_available:
		return false
	main_available = false
	move_available = false
	return true # Caller enforces >=3m straight path, <=2x speed, +2 hit, -2 AC.

func hold_action() -> bool:
	if holding or not move_available:
		return false
	move_available = false
	holding = true
	return true

func release_held_actions() -> bool:
	if not holding:
		return false
	holding = false
	return true

func expire_held_actions() -> void:
	if holding:
		holding = false
		main_available = false
		move_available = false
