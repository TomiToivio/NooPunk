extends "res://tests/godot/godot_test.gd"

## The CWN rules core in the engine: creation, Strain, injury, the action economy and load (#751).
##
## Each case mirrors one the Python layer already pins, because a rule difference between the two
## runtimes is a defect, not a port.

const Character = preload("res://godot/core/cwn_character.gd")
const Strain = preload("res://godot/core/cwn_strain.gd")
const Healing = preload("res://godot/core/cwn_healing.gd")
const Actions = preload("res://godot/core/cwn_combat_actions.gd")
const Carry = preload("res://godot/core/cwn_encumbrance.gd")

func test_attributes_roll_three_d_six_in_order() -> void:
	var dice = [1, 2, 3, 6, 6, 6, 1, 1, 1, 4, 4, 4, 5, 5, 5, 2, 2, 2]
	var rolled = Character.roll_attributes(dice)
	check_eq(rolled["ok"], true, "eighteen dice make six scores")
	check_eq(rolled["scores"]["STR"], 6, "3d6 in order")
	check_eq(rolled["scores"]["DEX"], 18, "the second score is the second three dice")
	check_eq(rolled["scores"]["CHA"], 6, "and the last one is the last three")
	check_eq(Character.roll_attributes([1, 2, 3])["reason"], "eighteen_dice_required",
		"a short roll is refused")
	check_eq(Character.roll_attributes([1, 2, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])["reason"],
		"each_die_is_1_to_6", "a seven is not a d6")

func test_one_score_may_become_fourteen_but_the_array_forfeits_it() -> void:
	var scores = {"STR": 9, "DEX": 10, "CON": 11, "INT": 12, "WIS": 13, "CHA": 8}
	var raised = Character.substitute_fourteen(scores, "STR")
	check_eq(raised["scores"]["STR"], 14, "one score becomes 14")
	check_eq(raised["scores"]["CHA"], 8, "the others are untouched")
	check_eq(Character.substitute_fourteen(scores, "STR", true)["reason"],
		"only_one_score_may_be_substituted", "only once")
	check_eq(Character.substitute_fourteen(scores, "STR", false, true)["reason"],
		"the_array_forfeits_the_substitute_fourteen_option", "not with the array")

func test_the_array_must_be_a_permutation_of_itself() -> void:
	var good = Character.assign_array({"STR": 14, "DEX": 12, "CON": 11, "INT": 10, "WIS": 9, "CHA": 7})
	check_eq(good["ok"], true, "the printed array is legal")
	var bad = Character.assign_array({"STR": 14, "DEX": 12, "CON": 11, "INT": 10, "WIS": 9, "CHA": 9})
	check_eq(bad["reason"], "attributes_must_be_a_permutation_of_the_array",
		"a better spread invented by the player is refused")

func test_a_bonus_may_not_push_the_modifier_past_two() -> void:
	check_eq(Character.effective_modifier(14), 1, "14 is +1")
	check_eq(Character.effective_modifier(14, 2), 2, "a +2 bonus is capped at +2, not +3")
	check_eq(Character.effective_modifier(14, 2, true), 3, "unless the source says it may exceed")
	check_eq(Character.effective_modifier(3, -3), -2, "and the floor holds too")

func test_creation_picks_stop_at_rank_one() -> void:
	var pool: Object = Character.SkillPool.new()
	check_eq(pool.pick("Program"), 0, "the first pick is rank 0")
	check_eq(pool.pick("Program"), 1, "the second pick is rank 1")
	check_eq(pool.pick("Program"), -1, "a third pick of the same skill is refused at creation")
	check_eq(pool.can_pick("Program"), false, "and no further pick of it is available")
	check_eq(pool.pick("Notice"), 0, "while a different skill can still be picked")

func test_level_one_hit_points_are_a_d_six_plus_constitution() -> void:
	check_eq(Character.hit_points(1, 10), 6, "CON 10 is no modifier, so 1d6 with the average 6")
	check_eq(Character.hit_points(1, 3), 4, "a CON 3 character takes -2")
	check_eq(Character.hit_points(1, 18), 8, "and a CON 18 one +2")
	check_eq(Character.hit_points(2, 10, [4]), 10, "a second level adds its roll plus CON")

func test_the_four_saves_come_from_the_kernel() -> void:
	var attributes = {"STR": 9, "DEX": 12, "CON": 10, "INT": 14, "WIS": 12, "CHA": 8}
	var saves = Character.saves(1, attributes)
	check_eq(saves["Physical"], 15, "16 - level - STR/CON modifier (0)")
	check_eq(saves["Evasion"], 14, "16 - level - DEX/INT modifier (+1)")
	check_eq(saves["Mental"], 15, "16 - level - WIS/CHA modifier (0)")
	check_eq(saves["Luck"], 15, "16 - level")

func test_strain_is_capped_by_constitution_and_overflow_costs_an_hour() -> void:
	var strain: Object = Strain.new(10, 0.0, 4.0)
	check_eq(strain.maximum(), 10, "the maximum is the Constitution score")
	check_eq(strain.available(), 6.0, "installed cyberware is already spent")
	check_eq(strain.absorb(3.0), true, "three points fit")
	check_eq(strain.absorb(4.0), false, "a fourth does not, and nothing changes")
	var forced: Object = Strain.new(10, 6.0, 4.0)
	check_eq(forced.absorb(3.0, true), false, "a forced overflow is still refused")
	check_eq(forced.total(), 10.0, "but the total clamps at the maximum")
	check_eq(forced.unconscious_hours, 1.0, "and it costs at least an hour")

func test_strain_recovers_one_a_night_only() -> void:
	var strain: Object = Strain.new(10, 3.0, 0.0)
	check_eq(strain.rest_night(6.0), 0.0, "six hours is not a night")
	check_eq(strain.rest_night(8.0), 1.0, "eight warm comfortable hours restore one")
	check_eq(strain.total(), 2.0, "and exactly one")

func test_stabilizing_gets_harder_every_round() -> void:
	check_eq(Healing.stabilize_difficulty(0)["difficulty"], 8, "difficulty 8 at the fall")
	check_eq(Healing.stabilize_difficulty(2)["difficulty"], 10, "plus each full round")
	check_eq(Healing.stabilize_difficulty(2, false)["difficulty"], 12, "two harder without a medkit")
	check_eq(Healing.mortal_wound_expired(5), false, "five rounds is still survivable")
	check_eq(Healing.mortal_wound_expired(6), true, "the sixth ends it")

func test_a_stabilized_patient_is_frail_and_does_not_heal_naturally() -> void:
	var patient = {"mortally_wounded": true, "hit_points": 0, "frail": false}
	var stable = Healing.stabilize(patient)
	check_eq(stable["ok"], true, "a mortally wounded patient can be stabilized")
	check_eq(stable["patient"]["hit_points"], 1, "and wakes with one hit point")
	check_eq(stable["patient"]["frail"], true, "at the cost of Frailty")
	check_eq(Healing.natural_healing(3, true), 0, "the Frail do not heal by rest")
	check_eq(Healing.natural_healing(3, false), 3, "everyone else regains level-or-HD")

func test_the_week_of_bed_rest_decides_frailty() -> void:
	check_eq(Healing.frail_week(true)["outcome"], "recovered", "with care it simply ends")
	check_eq(Healing.frail_week(false)["reason"], "without_care_the_week_needs_its_physical_save",
		"without care the save is mandatory")
	check_eq(Healing.frail_week(false, true)["outcome"], "month_more", "a made save buys a month")
	check_eq(Healing.frail_week(false, false)["outcome"], "dying", "a failed one kills within days")

func test_the_action_economy_is_one_main_and_one_move() -> void:
	var budget: Object = Actions.TurnBudget.new()
	check_eq(budget.main_available(), true, "the Main action is available")
	check_eq(budget.take_move(), true, "the Move action too")
	check_eq(budget.take_move(), false, "but only once")
	check_eq(budget.take_main(), true, "the Main action is spent separately")
	check_eq(budget.take_main(), false, "and cannot be spent twice")
	var converted: Object = Actions.TurnBudget.new()
	check_eq(converted.convert_main_to_move(), true, "the Main action may buy a second Move")
	check_eq(converted.moves_available(), 2, "which is what the book allows")

func test_snap_swarm_charge_and_total_defence() -> void:
	check_eq(Actions.snap_attack_penalty(false)["penalty"], -4, "a Snap Attack is at -4")
	check_eq(Actions.snap_attack_penalty(true)["reason"], "main_action_already_spent",
		"and needs an unspent Main action")
	var swarm = Actions.swarm_bonus(2)
	check_eq(swarm["to_hit"], 4, "+2 to hit per other assailant")
	check_eq(swarm["damage"], 2, "+1 damage each")
	check_eq(Actions.swarm_bonus(9)["to_hit"], 6, "capped at four attackers in total")
	check_eq(Actions.charge(2.0)["reason"], "a_charge_needs_at_least_three_metres",
		"a Charge needs momentum")
	check_eq(Actions.charge(5.0)["to_hit_bonus"], 2, "and grants +2 to hit")
	check_eq(Actions.charge(5.0)["ac_penalty"], -2, "at -2 AC until the round ends")
	check_eq(Actions.total_defense(false)["ac_bonus"], 2, "Total Defense is +2 AC")
	check_eq(Actions.total_defense(true)["reason"], "main_action_already_spent",
		"and gives up the Main action")

func test_load_tiers_and_the_speed_they_cost() -> void:
	check_eq(Carry.stowed_capacity(10), 10, "stowed capacity is Strength")
	check_eq(Carry.readied_capacity(10), 5, "readied is half of it")
	check_eq(Carry.tier_for(10, 10, 5), "normal", "exactly at capacity is normal")
	check_eq(Carry.tier_for(10, 12, 6), "heavy", "one push past it is heavy")
	check_eq(Carry.tier_for(10, 15, 8), "overloaded", "two pushes is overloaded")
	check_eq(Carry.tier_for(10, 25, 9), "immobile", "beyond that you do not move")
	check_eq(Carry.move_speed("normal"), 10.0, "ten metres at a normal load")
	check_eq(Carry.move_speed("heavy"), 7.0, "seventy per cent when heavy")
	check_eq(Carry.move_speed("overloaded"), 5.0, "half when overloaded")
	check_eq(Carry.move_speed("immobile"), 0.0, "and none at all")
	check_eq(Carry.kilograms_to_points(25.0), 10.0, "ten points weigh twenty-five kilos")
	check_eq(Carry.bundled_points(7), 3, "three items to a bundle, rounded up")
