## The CWN chassis procedures, in the engine that plays them.
##
## These are property tests rather than a second copy of the Python suite: the adapter rolls its own
## dice from the seeded stream, so each test states the invariant that must hold whatever the dice
## said. The numbers come from `data/rules/wn_core.json`; `tests/test_cwn_procedures.py` pins the same
## contract on the Python side.
extends RefCounted

const SEED := 631

func run() -> Array:
	var rows: Array = []
	rows.append_array(_attack_rows())
	rows.append_array(_damage_rows())
	rows.append_array(_strain_rows())
	rows.append_array(_hacking_rows())
	rows.append_array(_advancement_rows())
	return rows

func _attack_rows() -> Array:
	var rows: Array = []
	var rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, SEED)
	var untrained_ok := true
	var total_ok := true
	var natural_ok := true
	var saw_natural_one := false
	var saw_natural_twenty := false
	for i in 200:
		var attack: Dictionary = rules.attack_roll(2, 14, 1, 15, false, 1)
		var die := int(attack["die"])
		var expected := die + 2 + int(attack["attribute_modifier"]) + 1 + 1
		if int(attack["total"]) != expected:
			total_ok = false
		if die == 1:
			saw_natural_one = true
			if bool(attack["success"]):
				natural_ok = false
		elif die == 20:
			saw_natural_twenty = true
			if not bool(attack["success"]):
				natural_ok = false
		elif bool(attack["success"]) != (int(attack["total"]) >= 15):
			natural_ok = false
		var untrained: Dictionary = rules.attack_roll(2, 14, 1, 15, true, 1)
		var untrained_expected := int(untrained["die"]) + 2 + int(untrained["attribute_modifier"]) + 1 + 1 - 2
		if int(untrained["total"]) != untrained_expected:
			untrained_ok = false
	rows.append(_check("attack total is die + bonus + attribute + skill + situation", total_ok))
	rows.append(_check("a natural 1 misses and a natural 20 hits", natural_ok))
	rows.append(_check("200 seeded attacks produced both natural extremes", saw_natural_one and saw_natural_twenty))
	rows.append(_check("an untrained attack takes the kernel's -2", untrained_ok))
	rows.append(_eq("attribute modifier for DEX 14 is +1", rules.attribute_modifier(14), 1))
	return rows

func _damage_rows() -> Array:
	var rows: Array = []
	var rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, SEED)

	var pistol := rules.weapon("light pistol", 1, 6, 0, 0, -1, 8, 2)
	var knife := rules.weapon("knife", 1, 4, 0, 1, 15, 6, 3)
	var unarmed := rules.weapon("unarmed", 1, 2, 0, 0, -1, 0, 1)

	var hits := {"success": true, "die": 15, "total": 15, "target_ac": 10}
	var misses := {"success": false, "die": 2, "total": 2, "target_ac": 17}

	var floor_ok := true
	var trauma_ok := true
	var positive := true
	for i in 60:
		var hit: Dictionary = rules.resolve_damage(hits, pistol, 14, 10)
		if not bool(hit["hit"]):
			floor_ok = false
		if int(hit["damage"]) < 1:
			positive = false
		if bool(hit["traumatic"]) and int(hit["trauma_roll"]) < int(hit["trauma_target"]):
			trauma_ok = false
		if not bool(hit["traumatic"]) and int(hit["trauma_roll"]) >= int(hit["trauma_target"]):
			trauma_ok = false
	rows.append(_check("every seeded attack connected", floor_ok))
	rows.append(_check("a hit always does at least one point", positive))
	rows.append(_check("a Traumatic Hit is exactly a Trauma Die at or over the target", trauma_ok))

	var shock_miss: Dictionary = rules.resolve_damage(misses, knife, 14, 14)
	rows.append(_eq("Shock lands on a miss within its AC rating (1 + STR +1)", int(shock_miss["total_damage"]), 2))
	var no_shock_miss: Dictionary = rules.resolve_damage(misses, knife, 14, 17)
	rows.append(_eq("Shock does not land on a well-armoured miss", int(no_shock_miss["total_damage"]), 0))

	var non_lethal: Dictionary = rules.resolve_damage(hits, pistol, 14, 10, -1, true)
	rows.append(_check("a non-lethal hit rolls no Trauma Die", non_lethal["trauma_roll"] == null and not bool(non_lethal["traumatic"])))
	var unarmed_hit: Dictionary = rules.resolve_damage(hits, unarmed, 14, 10, -1, true)
	rows.append(_check("unarmed strikes do not multiply damage", not bool(unarmed_hit["traumatic"])))

	rows.append(_eq("stabilization difficulty counts the rounds", rules.stabilize_difficulty(3), 11))
	rows.append(_eq("stabilization without tools is two harder", rules.stabilize_difficulty(0, false), 10))
	rows.append(_eq("a mortal wound kills at the end of round six", rules.mortal_rounds(), 6))
	return rows

func _strain_rows() -> Array:
	var rows: Array = []
	var rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, SEED)
	rows.append(_eq("System Strain's maximum is CON", rules.strain_maximum(11), 11))
	rows.append(_check("strain that would cross the maximum is refused", rules.strain_add(10, 9.0, 2.0) < 0.0))
	rows.append(_eq("strain within the maximum is accepted", rules.strain_add(10, 4.0, 1.0), 5.0))
	rows.append(_check("an unavoidable overload knocks the character out", rules.strain_forced_over_maximum(10, 9.0, 3.0)))
	rows.append(_eq("a night's rest removes one point", rules.strain_after_rest(3.0), 2.0))
	rows.append(_eq("natural healing is the character level", rules.natural_healing(4), 4))
	rows.append(_eq("Frail characters heal nothing", rules.natural_healing(4, true), 0))

	var heal_ok := true
	for i in 40:
		var trained := rules.first_aid_healing(2)
		var untrained := rules.first_aid_healing(0, true)
		if trained < 3 or trained > 8:
			heal_ok = false
		if untrained < 0 or untrained > 5:
			heal_ok = false
	rows.append(_check("first aid is 1d6 + Heal, and 1d6 - 1 untrained", heal_ok))
	return rows

func _hacking_rows() -> Array:
	var rows: Array = []
	var rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, SEED)
	rows.append(_eq("Access is INT modifier + Program + deck", rules.access_pool(14, 2, 1), 4))
	rows.append(_eq("Access never goes below zero", rules.access_pool(4, 0, 0), 0))
	rows.append(_eq("a private network is difficulty 7", rules.hacking_difficulty(7), 7))
	rows.append(_eq("an alerted network is one harder", rules.hacking_difficulty(8, true), 9))
	rows.append(_eq("inside information lowers the difficulty", rules.hacking_difficulty(9, false, false, 0, 2), 7))
	rows.append(_eq("cyberware difficulty is 7 + ceil(level / 3)", rules.cyber_hack_difficulty(4), 9))
	rows.append(_eq("an unoperated drone is difficulty 8", rules.cyber_hack_difficulty(9, false), 8))

	# Same seed, same dice: the only difference is the connection penalty.
	var wired_rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, 77)
	var wireless_rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, 77)
	var wired: Dictionary = wired_rules.hacking_check(14, 1, 9, false, false, false, 0)
	var wireless: Dictionary = wireless_rules.hacking_check(14, 1, 9, false, true, false, 0)
	rows.append(_eq("a wireless connection costs exactly 2", int(wired["total"]) - int(wireless["total"]), 2))

	var crown_rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, 77)
	var crown: Dictionary = crown_rules.hacking_check(14, 1, 9, false, true, true, 0)
	rows.append(_eq("wireless plus a VR crown costs 3, unclamped", int(wired["total"]) - int(crown["total"]), 3))

	var untrained_rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, 77)
	var untrained: Dictionary = untrained_rules.hacking_check(14, 0, 9, true, false, false, 0)
	rows.append(_eq("an untrained hacker takes -1", int(wired["total"]) - int(untrained["total"]), 2))
	return rows

func _advancement_rows() -> Array:
	var rows: Array = []
	var rules := RulesAdapter.new(RulesAdapter.DEFAULT_KERNEL_PATH, SEED)
	rows.append(_eq("0 XP is level 1", rules.level_for_xp(0), 1))
	rows.append(_eq("3 XP is level 2 on the fast track", rules.level_for_xp(3), 2))
	rows.append(_eq("93 XP is level 10", rules.level_for_xp(93), 10))
	rows.append(_eq("the slow track needs 6 for level 2", rules.level_for_xp(6, "slow"), 2))
	rows.append(_eq("attack bonus is half level", rules.attack_bonus(5), 2))
	rows.append(_eq("On Target makes it the full level", rules.attack_bonus(5, true), 5))
	rows.append(_eq("skill level 2 costs 3 points", rules.skill_point_cost(2), 3))
	rows.append(_eq("skill level 3 needs character level 6", rules.minimum_level_for_skill(3), 6))
	return rows

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]

func _check(label: String, ok: bool, detail: String = "") -> Array:
	return [label, ok, detail]
