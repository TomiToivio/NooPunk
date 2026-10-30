extends "res://tests/godot/godot_test.gd"

## CWN Deluxe 2023 pp. 33-34: tests for executable initiative/action logic.

func _round() -> CWNCombatRound:
	var encounter := CWNCombatRound.new()
	check(encounter.initialize([
		{"id": "romppainen", "side": "pcs", "dexterity_modifier": 1},
		{"id": "guard", "side": "guards", "dexterity_modifier": 0},
	], "pcs", {"pcs": 4, "guards": 5}), "initialize valid encounter")
	return encounter

func test_pc_initiative_wins_ties() -> void:
	var encounter := _round()
	check_eq(encounter.active_side(), "pcs", "PC side wins tied initiative")
	check_eq(encounter.round_number, 1, "round starts at one")

func test_main_and_move_budget_and_extra_move() -> void:
	var encounter := _round()
	check(encounter.move_actor("romppainen", 10.0), "first full move")
	check(not encounter.move_actor("romppainen", 11.0), "speed limit")
	check(encounter.move_actor("romppainen", 10.0), "second move spends main")
	check(not encounter.spend_action("romppainen", "Main"), "main is spent")
	check(not encounter.move_actor("romppainen", 1.0), "cannot move a third time")
	check_eq(encounter.participants["romppainen"]["moved_meters"], 20.0, "distance recorded")

func test_sides_and_rounds_do_not_skip_actors() -> void:
	var encounter := _round()
	check(not encounter.advance_side(), "cannot advance before action")
	check(not encounter.spend_action("guard", "Main"), "enemy may not act on PC turn")
	check(encounter.finish_actor("romppainen"), "PC finishes")
	check(encounter.advance_side(), "advance to guards")
	check_eq(encounter.active_side(), "guards", "guard side active")
	check(encounter.spend_action("guard", "Main"), "guard action")
	check(encounter.finish_actor("guard"), "guard finishes")
	check(encounter.advance_side(), "next round")
	check_eq(encounter.round_number, 2, "round advances")
	check(encounter.spend_action("romppainen", "Main"), "action refreshed")

func test_malformed_initiative_does_not_replace_state() -> void:
	var encounter := _round()
	var before := encounter.snapshot()
	check(not encounter.initialize([{"id": "x", "side": "pcs"}], "pcs", {"pcs": 9}), "reject d8 result outside 1..8")
	check_eq(encounter.snapshot(), before, "reject leaves previous encounter intact")
