extends "res://tests/godot/godot_test.gd"

func test_attack_context_prone_cover_range_and_visibility() -> void:
	check_eq(CWNAttackContext.assess({"target_prone": true}).modifier, -2, "prone ranged target")
	check_eq(CWNAttackContext.assess({"target_prone": true, "adjacent": true, "mode": "melee"}).modifier, 2, "adjacent prone target")
	check_eq(CWNAttackContext.assess({"attacker_prone": true, "mode": "melee"}).modifier, -4, "prone melee attacker")
	check_eq(CWNAttackContext.assess({"cover": "half", "long_range": true}).modifier, -4, "half cover and long range")
	check_eq(CWNAttackContext.assess({"cover": "almost_complete", "long_range": true, "gunlink": true}).modifier, -2, "gunlink ignores long range and two cover penalty")
	check_eq(CWNAttackContext.assess({"visible": false, "position_known": true}).modifier, -4, "unseen known target")

func test_unsafe_or_impossible_attacks_are_rejected() -> void:
	check(not CWNAttackContext.assess({"visible": false, "position_known": false}).allowed, "unknown position")
	check(not CWNAttackContext.assess({"mode": "ranged", "gun_in_melee": true}).allowed, "two-handed gun in melee")
	check_eq(CWNAttackContext.assess({"mode": "ranged", "gun_in_melee": true, "one_handed": true}).modifier, -4, "one-handed gun")
	check_eq(CWNAttackContext.assess({"mode": "thrown", "adjacent": true}).modifier, -4, "thrown weapon in melee")
	check(not CWNAttackContext.assess({"cover": "incorrect"}).allowed, "invalid cover")

func test_attack_d20_uses_context() -> void:
	var result := CWNAttackContext.evaluate(12, 1, 1, 1, 13, {"cover": "half"})
	check(result.allowed, "attack is allowed")
	check_eq(result.total, 13, "12+1+1+1-2")
	check(result.hit, "equal to AC hits")
	check(not CWNAttackContext.evaluate(12, 1, 1, 1, 13, {"cover": "almost_complete"}).hit, "greater cover can cause miss")
