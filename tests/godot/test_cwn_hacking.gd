extends "res://tests/godot/godot_test.gd"

## The CWN hacking kernel, checked against the source's own arithmetic (#752).
##
## Every expectation here is a number the SRD fixes, not a calibration: the recorded security
## ladder, the two flat connection penalties, "two failures count as one Alert action, and the
## second Alert action alerts the network", `7 + ceil(HD/3)`, and access as a spent pool.

const Rules := preload("res://godot/core/cwn_hacking.gd")

func test_the_recorded_security_ladder_is_the_only_one_accepted() -> void:
	check_eq(Rules.security_levels(), [7, 8, 9, 10, 12], "the SRD's five recorded levels")
	var good := Rules.security_difficulty(9)
	check_eq(good["ok"], true, "9 is a recorded level")
	check_eq(good["difficulty"], 9, "a plain network's difficulty is its level")
	var bad := Rules.security_difficulty(6)
	check_eq(bad["ok"], false, "an unrecorded level is refused, not guessed")
	check_eq(bad["reason"], "unrecorded_security_level", "and says why")

func test_situation_modifiers_move_the_target_exactly_once_each() -> void:
	check_eq(Rules.security_difficulty(9, true)["difficulty"], 10, "an alerted network is +1")
	check_eq(Rules.security_difficulty(9, false, true)["difficulty"], 10, "an important device is +1")
	check_eq(Rules.security_difficulty(9, true, true)["difficulty"], 11, "and they stack")
	check_eq(Rules.security_difficulty(9, false, false, -2)["difficulty"], 7, "tech quality -2")
	check_eq(Rules.security_difficulty(9, false, false, 0, 3)["difficulty"], 6,
		"inside information worth 3 lowers the target by 3")
	check_eq(Rules.security_difficulty(9, false, false, 0, 9)["difficulty"], 6,
		"and its magnitude is clamped to the declared 1..3, not trusted")
	check_eq(Rules.security_difficulty(9, false, false, 0, 0)["difficulty"], 9,
		"no informant is a plain network, not an invented one")
	check_eq(Rules.security_difficulty(9, false, false, 9)["difficulty"], 11,
		"tech quality is clamped to the recorded +2, not trusted")

func test_access_is_a_pool_of_int_program_and_deck_bonus() -> void:
	check_eq(Rules.access_pool(1, 2), 3, "INT mod + Program")
	check_eq(Rules.access_pool(2, 1, 1), 4, "plus the deck's Bonus Access")
	check_eq(Rules.access_pool(-2, 0), 0, "never negative")

func test_connection_penalties_are_flat_and_stack() -> void:
	var wired := Rules.hacking_check([3, 3], 1, 2, 8)
	check_eq(wired["connection_penalty"], 0, "a jacked-in run pays nothing")
	check_eq(wired["total"], 9, "2d6 (6) + INT modifier 1 + Program 2")
	check_eq(wired["success"], true, "9 meets difficulty 8")
	var wireless := Rules.hacking_check([3, 3], 1, 2, 8, true)
	check_eq(wireless["connection_penalty"], -2, "a wireless link is -2")
	check_eq(wireless["total"], 7, "and the point is not swallowed by the circumstance clamp")
	check_eq(wireless["success"], false, "7 misses difficulty 8 — the wireless link cost the run")
	var both := Rules.hacking_check([3, 3], 1, 2, 8, true, true)
	check_eq(both["connection_penalty"], -3, "wireless plus VR crown is -3")
	check_eq(both["total"], 6, "both penalties stack on the same roll")

func test_circumstances_stay_inside_the_kernel_bound() -> void:
	var check := Rules.hacking_check([3, 3], 0, 0, 8, false, false, 0, 5)
	check_eq(check["situational"], 2, "circumstances clamp at +2")
	var harsh := Rules.hacking_check([3, 3], 0, 0, 8, false, false, 0, -5)
	check_eq(harsh["situational"], -2, "and at -2")

func test_untrained_program_is_minus_one() -> void:
	var check := Rules.hacking_check([3, 3], 0, -1, 8)
	check_eq(check["untrained"], true, "rank -1 is untrained")
	check_eq(check["total"], 5, "2d6 with no rank and the untrained -1")
	check_eq(check["success"], false, "and the check fails honestly")

func test_two_failures_are_one_alert_action_and_the_second_action_alerts() -> void:
	var clock := Rules.new_alert_clock()
	check_eq(clock.record_failure(), false, "one failure is not an Alert action")
	check_eq(clock.record_failure(), true, "the second failure counts as one")
	check_eq(clock.alerted(), false, "one Alert action does not alert the network")
	check_eq(clock.record_failure(), false, "the third failure is not an action")
	check_eq(clock.record_failure(), true, "the fourth is the second action")
	check_eq(clock.alerted(), true, "and the network is now alerted")

func test_a_defender_can_alert_the_network_without_a_failure() -> void:
	var clock := Rules.new_alert_clock()
	check_eq(clock.record_alert_action(), false, "a demon's first main action is not enough")
	check_eq(clock.record_alert_action(), true, "the second alerts it")

func test_the_alert_clock_round_trips_through_a_save() -> void:
	var clock := Rules.new_alert_clock()
	clock.record_failure()
	var restored := Rules.new_alert_clock()
	restored.from_dict(clock.to_dict())
	check_eq(restored.failures, 1, "failures survive serialisation")
	check_eq(restored.alerted(), clock.alerted(), "and so does the alert state")

func test_cyberware_and_drones_use_seven_plus_a_third_of_hit_dice() -> void:
	check_eq(Rules.cyberware_difficulty(1)["difficulty"], 8, "1 HD rounds up to one third")
	check_eq(Rules.cyberware_difficulty(3)["difficulty"], 8, "3 HD is still one third")
	check_eq(Rules.cyberware_difficulty(4)["difficulty"], 9, "4 HD rounds to two thirds")
	check_eq(Rules.cyberware_difficulty(12)["difficulty"], 11, "12 HD reaches the cap of the table")
	check_eq(Rules.cyberware_difficulty(4, true)["difficulty"], 9, "an operated drone uses its HD")
	check_eq(Rules.cyberware_difficulty(4, false)["difficulty"], 8,
		"a drone with no operator is difficulty 8 regardless of HD")
	check_eq(Rules.cyberware_difficulty(0)["ok"], false, "hit dice must be positive")

func test_a_bad_die_is_refused_rather_than_coerced() -> void:
	check_eq(Rules.hacking_check([0, 3], 0, 0, 8)["ok"], false, "a zero die is not a die")
	check_eq(Rules.hacking_check([7, 3], 0, 0, 8)["ok"], false, "and neither is a seven")
	check_eq(Rules.hacking_check([3], 0, 0, 8)["ok"], false, "two dice are required")
