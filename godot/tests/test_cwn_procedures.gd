## CWN procedures the kernel records (#749/#751): creation rolls, strain, advancement,
## encumbrance, major injury and the action economy. Every expected number below comes from
## data/rules/wn_core.json, which cites its SRD section.
extends RefCounted

const Adapter := preload("res://godot/core/rules_adapter.gd")
const Dice := preload("res://godot/core/dice.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]

func run() -> Array:
	var rows: Array = []
	var rules := Adapter.new("res://data/rules/wn_core.json", 7)
	var dice := Dice.new(7)

	# --- character creation ---------------------------------------------------------
	var rolled: Dictionary = rules.roll_attributes(dice)
	rows.append(_eq("six attributes in kernel order", rolled["scores"].keys(), rules.attribute_names()))
	var in_range := true
	for stat in rolled["scores"]:
		var score := int(rolled["scores"][stat])
		if score < 3 or score > 18:
			in_range = false
		if int(rolled["modifiers"][stat]) != rules.attribute_modifier(score):
			in_range = false
	rows.append(_eq("3d6 lands in 3..18 and derives the kernel modifier", in_range, true))
	var again: Dictionary = Adapter.new("res://data/rules/wn_core.json", 7).roll_attributes(Dice.new(7))
	rows.append(_eq("creation rolls replay from the seed", again["scores"], rolled["scores"]))

	# --- System Strain --------------------------------------------------------------
	rows.append(_eq("strain maximum is Constitution", rules.strain_max(11), 11))
	rows.append(_eq("absorbing within the maximum is allowed", rules.strain_absorb(4.0, 3.0, 11)["total"], 7.0))
	var refuse := rules.strain_absorb(10.0, 3.0, 11)
	rows.append(_eq("overflow is refused without force", refuse["ok"], false))
	rows.append(_eq("a refused overflow does not move the total", refuse["total"], 10.0))
	var forced := rules.strain_absorb(10.0, 3.0, 11, true)
	rows.append(_eq("forcing clamps at the maximum", forced["total"], 11.0))
	rows.append(_eq("forcing costs an hour of consciousness", forced["unconscious_hours"], 1))
	rows.append(_eq("a night's rest removes one point", rules.strain_recover(3.0), 2.0))
	rows.append(_eq("a bad night removes none", rules.strain_recover(3.0, false), 3.0))

	# --- advancement ----------------------------------------------------------------
	rows.append(_eq("fast ladder: level 2 at 3 XP", rules.xp_threshold(2, "fast"), 3))
	rows.append(_eq("fast ladder: level 10 at 93 XP", rules.xp_threshold(10, "fast"), 93))
	rows.append(_eq("slow ladder differs from fast", rules.xp_threshold(10, "slow"), 139))
	rows.append(_eq("12 XP is level 4 on the fast ladder", rules.level_for_xp(12, "fast"), 4))
	rows.append(_eq("7 XP is still level 3", rules.level_for_xp(7, "fast"), 3))
	rows.append(_eq("attack bonus is half level", rules.attack_bonus_for_level(5), 2))
	rows.append(_eq("On Target gives the full level", rules.attack_bonus_for_level(5, true), 5))
	rows.append(_eq("skill points are three per level", rules.skill_points_for_level(2), 6))
	rows.append(_eq("Educated adds one", rules.skill_points_for_level(2, true), 7))
	rows.append(_eq("rank 2 needs character level 3", rules.skill_rank_allowed(2, 2), false))
	rows.append(_eq("rank 2 opens at level 3", rules.skill_rank_allowed(2, 3), true))
	var hp := rules.hp_gain(2, 0)
	rows.append(_eq("two hit dice cannot fall below two points", hp >= 2, true))

	# --- encumbrance and speed ------------------------------------------------------
	var load := rules.encumbrance(12)
	rows.append(_eq("stowed equals Strength", load["stowed"], 12))
	rows.append(_eq("readied is half Strength", load["readied"], 6))
	rows.append(_eq("heavy load is 70 % of base speed", rules.speed_for_load(10.0, true, false), 7.0))
	rows.append(_eq("overloaded is 50 % of base speed", rules.speed_for_load(10.0, false, true), 5.0))
	rows.append(_eq("heavy and overloaded stack", rules.speed_for_load(10.0, true, true), 3.5))

	# --- major injury ---------------------------------------------------------------
	rows.append(_eq("row 1 is instant death", rules.major_injury(1)["injury"], "instant_death"))
	rows.append(_eq("row 2 is internal damage", rules.major_injury(2)["injury"], "internal_damage"))
	rows.append(_eq("modifiers clamp below 1", rules.major_injury(1, -3)["result"], 1))
	rows.append(_eq("modifiers clamp above 12", rules.major_injury(12, 5)["result"], 12))
	rows.append(_eq("row 12 is a flesh wound", rules.major_injury(12)["injury"], "flesh_wound"))

	# --- action economy -------------------------------------------------------------
	var economy: Dictionary = rules.action_economy()
	rows.append(_eq("one Main and one Move per round", [int(economy["main_per_round"]), int(economy["move_per_round"])], [1, 1]))
	rows.append(_eq("a second Move can be bought with Main", economy["main_can_buy_second_move"], true))
	rows.append(_eq("snap attack is -4", economy["snap_attack_penalty"], -4))
	var charge: Dictionary = rules.combat_action_modifier("charge")
	rows.append(_eq("charge is +2 to hit and -2 AC", [int(charge["to_hit"]), int(charge["ac_penalty"])], [2, -2]))
	rows.append(_eq("total defence denies shock", rules.combat_action_modifier("total_defense")["shock_immune"], true))
	return rows
