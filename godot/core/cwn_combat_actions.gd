## Cities Without Number: the combat action economy.
##
## Port of `src/rules/cwn_combat_actions.py`. One **Main** and one **Move** action per round; the
## Main may be spent for a second Move. **On Turn** and **Instant** actions are as many as the
## referee finds plausible — deliberately not a number here.
##
## The named actions that modify the budget:
## * **Snap Attack** (Instant): give up the Main action for an attack at -4, only if unspent.
## * **Swarm Attack** (Main): +2 to hit and +1 damage per other assailant, capped at +6/+3.
## * **Charge** (Main + Move): at least 3 m in a straight line, +2 to hit, -2 AC for the round.
## * **Total Defense** (Instant): give up the Main action for +2 AC and immunity to Shock.
extends RefCounted
class_name CwnCombatActions

const MAIN_ACTIONS_PER_ROUND := 1
const MOVE_ACTIONS_PER_ROUND := 1
const SNAP_ATTACK_PENALTY := -4
const SWARM_PER_OTHER_HIT := 2
const SWARM_PER_OTHER_DAMAGE := 1
const SWARM_MAX_OTHER_ASSAILANTS := 3
const CHARGE_TO_HIT_BONUS := 2
const CHARGE_AC_PENALTY := -2
const CHARGE_MIN_DISTANCE_METRES := 3.0
const CHARGE_SPEED_MULTIPLIER := 2
const TOTAL_DEFENSE_AC_BONUS := 2

## Main/Move bookkeeping for one combatant in one round.
class TurnBudget extends RefCounted:
	var main_used := false
	var moves_used := 0
	var extra_moves := 0

	func main_available() -> bool:
		return not main_used

	func moves_available() -> int:
		return maxi(0, CwnCombatActions.MOVE_ACTIONS_PER_ROUND + extra_moves - moves_used)

	func take_main() -> bool:
		if main_used:
			return false
		main_used = true
		return true

	func take_move() -> bool:
		if moves_available() <= 0:
			return false
		moves_used += 1
		return true

	## Spend the Main action to gain a second Move action.
	func convert_main_to_move() -> bool:
		if not take_main():
			return false
		extra_moves += 1
		return true

	func reset() -> void:
		main_used = false
		moves_used = 0
		extra_moves = 0

## The Snap Attack penalty, or nothing when the Main action is already spent.
static func snap_attack_penalty(main_used: bool) -> Dictionary:
	if main_used:
		return {"ok": false, "reason": "main_action_already_spent"}
	return {"ok": true, "penalty": SNAP_ATTACK_PENALTY}

## Bonuses for a Swarm Attack, capped at four attackers in total.
static func swarm_bonus(other_assailants: int) -> Dictionary:
	if other_assailants < 0:
		return {"ok": false, "reason": "other_assailants_cannot_be_negative"}
	var counted := mini(other_assailants, SWARM_MAX_OTHER_ASSAILANTS)
	return {"ok": true, "to_hit": SWARM_PER_OTHER_HIT * counted,
		"damage": SWARM_PER_OTHER_DAMAGE * counted, "counted": counted}

## A Charge costs both the Main and the Move action and needs momentum to build.
static func charge(distance_metres: float, budget: TurnBudget = null) -> Dictionary:
	if distance_metres < CHARGE_MIN_DISTANCE_METRES:
		return {"ok": false, "reason": "a_charge_needs_at_least_three_metres"}
	if budget != null:
		if not budget.main_available():
			return {"ok": false, "reason": "charge_costs_the_main_action"}
		if budget.moves_available() <= 0:
			return {"ok": false, "reason": "charge_costs_a_move_action"}
	return {"ok": true, "to_hit_bonus": CHARGE_TO_HIT_BONUS, "ac_penalty": CHARGE_AC_PENALTY,
		"speed_multiplier": CHARGE_SPEED_MULTIPLIER}

## Total Defense gives up the Main action for +2 AC and immunity to Shock until the next turn.
static func total_defense(main_used: bool) -> Dictionary:
	if main_used:
		return {"ok": false, "reason": "main_action_already_spent"}
	return {"ok": true, "ac_bonus": TOTAL_DEFENSE_AC_BONUS, "shock_immune": true}
