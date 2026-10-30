extends RefCounted

## Strain, Major Injury and healing procedures (#752/#751 surface), checked against the SRD rules
## as ported in `src/rules/cwn_{strain,major_injury,injury_procedure,healing}.py`.
const Strain := preload("res://godot/core/cwn_strain.gd")
const Injury := preload("res://godot/core/cwn/cwn_injury.gd")
const Healing := preload("res://src/godot/cwn/cwn_healing.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	# --- System Strain ---
	var strain := Strain.new(10)
	rows.append(_eq("strain starts empty", strain.total(), 0.0))
	rows.append(_eq("maximum is Constitution", strain.maximum(), 10.0))
	rows.append(_eq("strain can be taken", strain.absorb(3.0), true))
	rows.append(_eq("strain accumulates", strain.total(), 3.0))
	rows.append(_eq("available shrinks", strain.available(), 7.0))

	var full := Strain.new(5, 5.0)
	rows.append(_eq("a full body refuses more", full.absorb(1.0), false))
	rows.append(_eq("refusal changes nothing", full.total(), 5.0))
	rows.append(_eq("forced overflow still refuses", full.absorb(1.0, true), false))
	rows.append(_eq("forced overflow cannot pass the cap", full.total(), 5.0))
	rows.append(_eq("forced overflow knocks out", full.unconscious_hours, 1.0))

	var rested := Strain.new(10, 3.0)
	rows.append(_eq("a short night recovers nothing", rested.rest_night(6.0), 0.0))
	rows.append(_eq("an uncomfortable night recovers nothing",
		rested.rest_night(8.0, false), 0.0))
	rows.append(_eq("a proper night recovers one", rested.rest_night(), 1.0))
	rows.append(_eq("recovered strain is gone", rested.temporary, 2.0))

	var implanted := Strain.new(6)
	rows.append(_eq("fractional cyberware installs", implanted.install_cyber(0.5), true))
	rows.append(_eq("permanent strain is not shed", implanted.rest_night(), 0.0))
	rows.append(_eq("permanent strain stays", implanted.permanent, 0.5))
	rows.append(_eq("implant beyond the ceiling refused", implanted.install_cyber(9.0), false))
	implanted.remove_cyber(0.5)
	rows.append(_eq("removal takes the load back", implanted.permanent, 0.0))

	# --- Major Injury table ---
	rows.append(_eq("twelve outcomes", Injury.MAJOR_INJURY_TABLE.size(), 12))
	rows.append(_eq("below-range roll clamps up", Injury.injury_for_roll(0)["id"], "instant_death"))
	rows.append(_eq("above-range roll clamps down", Injury.injury_for_roll(13)["id"], "flesh_wound"))
	rows.append(_eq("instant death is lethal", Injury.is_lethal(Injury.injury_for_roll(1)), true))
	rows.append(_eq("gut wound kills in an hour",
		Injury.dies_without_care_within(Injury.injury_for_roll(5)), 1))
	rows.append(_eq("ruined leg needs a prosthetic",
		Injury.requires_prosthetic(Injury.injury_for_roll(6)), true))
	rows.append(_eq("ruined leg names its cyber",
		Injury.damaged_cyber_locations(Injury.injury_for_roll(6)), ["right leg"]))
	rows.append(_eq("flesh wound needs no prosthetic",
		Injury.requires_prosthetic(Injury.injury_for_roll(11)), false))
	rows.append(_eq("modifier shifts the row", Injury.resolve_major_injury(1, 1)["id"], "internal_damage"))

	# --- the zero-hit-point procedure ---
	rows.append(_eq("risk needs trauma", Injury.major_injury_risk(0, false), false))
	rows.append(_eq("risk needs lethal damage", Injury.major_injury_risk(0, true, false), false))
	rows.append(_eq("all three conditions risk injury", Injury.major_injury_risk(0, true, true), true))

	var alive: Dictionary = Injury.resolve_zero_hit_points({"hit_points_after": 4})
	rows.append(_eq("positive hit points are unharmed", alive["mortally_wounded"], false))

	var knockout: Dictionary = Injury.resolve_zero_hit_points({
		"hit_points_after": 0, "traumatic_in_fight": false, "level": 1,
	})
	rows.append(_eq("zero without trauma is a knockout", knockout["risked_major_injury"], false))
	rows.append(_eq("a knockout takes no save", knockout["save"], {}))
	rows.append(_eq("a knockout is still dying", knockout["mortally_wounded"], true))

	var nonlethal: Dictionary = Injury.resolve_zero_hit_points({
		"hit_points_after": 0, "traumatic_in_fight": true, "lethal": false, "level": 1,
	})
	rows.append(_eq("a non-lethal beating is a knockout", nonlethal["risked_major_injury"], false))

	# level 1, no modifiers: Physical target is 15.
	var passed: Dictionary = Injury.resolve_zero_hit_points({
		"hit_points_after": 0, "traumatic_in_fight": true, "level": 1,
		"save_die": 15, "modifiers": {},
	})
	rows.append(_eq("a passed save avoids the table", passed["injury"], {}))
	rows.append(_eq("a passed save still leaves the wound", passed["mortally_wounded"], true))
	rows.append(_eq("the save is reported", passed["save"]["success"], true))

	var failed: Dictionary = Injury.resolve_zero_hit_points({
		"hit_points_after": 0, "traumatic_in_fight": true, "level": 1,
		"save_die": 9, "modifiers": {}, "injury_roll": 6,
	})
	rows.append(_eq("a failed save rolls the table", failed["injury"]["id"], "right_leg_ruined"))
	rows.append(_eq("a natural 1 always fails", Injury.save_succeeds(1, 2), false))
	rows.append(_eq("a natural 20 always succeeds", Injury.save_succeeds(20, 30), true))

	# --- healing ---
	rows.append(_eq("death arrives on round six", Healing.rounds_until_death(3, 3), 6))
	rows.append(_eq("the clock runs down", Healing.rounds_until_death(3, 7), 2))
	rows.append(_eq("the clock never goes negative", Healing.rounds_until_death(3, 20), 0))
	rows.append(_eq("stabilising starts at 8", Healing.stabilize_difficulty(0), 8))
	rows.append(_eq("each round adds one", Healing.stabilize_difficulty(2), 10))
	rows.append(_eq("no medkit is two harder", Healing.stabilize_difficulty(0, false), 10))

	var stabilised: Dictionary = Healing.stabilize({"hit_points": 0, "frail": false})
	rows.append(_eq("stabilising wakes at one", stabilised["hit_points"], 1))
	rows.append(_eq("surviving costs frailty", stabilised["frail"], true))

	rows.append(_eq("the frail do not heal naturally", Healing.natural_healing(3, true), 0))
	rows.append(_eq("others heal their level", Healing.natural_healing(3, false), 3))
	rows.append(_eq("care ends frailty", Healing.frail_week(true), "recovered"))
	rows.append(_eq("no care and a failed save is dying", Healing.frail_week(false, false), "dying"))
	rows.append(_eq("no care and a passed save buys a month",
		Healing.frail_week(false, true), "month_more"))
	rows.append(_eq("one attempt only", Healing.remove_frailty(12, 10, true)["allowed"], false))
	rows.append(_eq("a good roll clears frailty", Healing.remove_frailty(10, 10)["succeeded"], true))

	rows.append(_eq("first aid without Heal is 1d6-1", Healing.first_aid(4, 0)["healed"], 3))
	rows.append(_eq("first aid with Heal adds the rank", Healing.first_aid(4, 2)["healed"], 6))
	rows.append(_eq("first aid cannot heal below zero", Healing.first_aid(1, 0)["healed"], 0))

	var aid_strain := Strain.new(4)
	var aided: Dictionary = Healing.first_aid(5, 1, true, aid_strain)
	rows.append(_eq("first aid costs a strain point", aided["strain_added"], 1))
	rows.append(_eq("the strain lands", aid_strain.total(), 1.0))
	var exhausted := Strain.new(2, 2.0)
	rows.append(_eq("a body at its maximum refuses care",
		Healing.first_aid(5, 1, true, exhausted)["refused"], true))

	return rows
