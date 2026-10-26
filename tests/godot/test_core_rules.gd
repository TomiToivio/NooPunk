extends "res://tests/godot/godot_test.gd"

## The rules adapter must match data/rules/core.json and the #566 ruling: STAT + Skill + 1d10.

func test_ranges_come_from_canonical_data() -> void:
	var rules := NooPunkCoreRules.new()
	check_eq(rules.stat_range(), [1, 10] as Array[int], "STAT range is 1..10")
	check_eq(rules.skill_level_range(), [1, 10] as Array[int], "Skill range is 1..10")
	check(rules.difficulty_ladder().size() >= 3, "difficulty ladder has entries")

func test_a_check_is_stat_plus_skill_plus_one_d10() -> void:
	var rules := NooPunkCoreRules.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	for _i in 50:
		var result := rules.resolve_check(rng, 7, 3, 12)
		check(result["die"] >= 1 and result["die"] <= 10, "1d10 is in 1..10")
		check_eq(result["total"], result["stat"] + result["skill"] + result["die"], "total adds STAT + Skill + die")
		check_eq(result["success"], result["total"] >= 12, "success is total >= DV")

func test_dice_are_seeded_and_replayable() -> void:
	var first := RandomNumberGenerator.new()
	first.seed = 20261026
	var second := RandomNumberGenerator.new()
	second.seed = 20261026
	var rolls_a: Array[int] = []
	var rolls_b: Array[int] = []
	for _i in 12:
		rolls_a.append(first.randi_range(1, 10))
		rolls_b.append(second.randi_range(1, 10))
	check_eq(rolls_a, rolls_b, "the same seed produces the same rolls")

func test_overrides_are_honoured_for_tests_and_playtest() -> void:
	var rules := NooPunkCoreRules.new()
	var rng := RandomNumberGenerator.new()
	var result := rules.resolve_check(rng, 4, 2, 10, 5)
	check_eq(result["die"], 5, "an explicit die is used")
	check_eq(result["total"], 11, "the explicit die is added")

func test_opposed_checks_report_ties_instead_of_inventing_a_winner() -> void:
	var rules := NooPunkCoreRules.new()
	check_eq(rules.compare_opposed(9, 9)["unresolved_tie"], true, "a tie stays unresolved")
	check_eq(rules.compare_opposed(10, 9)["winner"], "left", "higher total wins")
