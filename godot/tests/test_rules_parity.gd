extends RefCounted

## Parity harness for #791: the same rule, implemented twice, compared on one matrix.
##
## This suite does not test a feature — it tests a *claim*: that `godot/core/` and
## `src/godot/cwn/` answer the same question the same way. Where they agree the duplicate can be
## deleted with confidence; where they disagree the disagreement is the finding, and it is reported
## rather than hidden behind whichever implementation a test happened to import.
##
## It is deliberately not an "agreement test" that legitimises two implementations — see
## docs/godot/ARCHITECTURE_CONSOLIDATION.md. It is the evidence a deletion requires.
const AltCombat := preload("res://src/godot/cwn/cwn_combat.gd")
const CanonStrain := preload("res://godot/core/cwn_strain.gd")
const CanonCombat := preload("res://godot/core/cwn_combat_rules.gd")
const CanonHealing := preload("res://godot/core/cwn_healing.gd")

func _row(name: String, left: Variant, right: Variant) -> Array:
	return [name, left == right, "canon=%s alt=%s" % [left, right]]

func run() -> Array:
	var rows: Array = []

	# --- System Strain: **retired duplicate**, so these are single-sided assertions ---
	# `src/godot/cwn/cwn_strain.gd` answered the same questions and is gone (#791): the comparison it
	# needed is below, kept as the canonical numbers so the deletion stays justified rather than
	# merely done.
	for con in [3, 6, 10, 14]:
		var a := CanonStrain.new(con)
		rows.append(_row("strain maximum is CON=%d" % con, a.maximum(), con))
		rows.append(_row("strain starts empty CON=%d" % con, a.total(), 0.0))
		rows.append(_row("absorb 2 fits CON=%d" % con, a.absorb(2.0), true))
		rows.append(_row("and is counted CON=%d" % con, a.total(), 2.0))

	var ca := CanonStrain.new(5)
	ca.absorb(5.0)
	rows.append(_row("full body refuses", ca.absorb(1.0), false))
	rows.append(_row("forced overflow refuses", ca.absorb(1.0, true), false))
	rows.append(_row("forced clamps at ceiling", ca.total(), 5.0))
	rows.append(_row("forced knocks out", ca.unconscious_hours, 1.0))

	var ra := CanonStrain.new(10, 3.0)
	rows.append(_row("short night recovers nothing", ra.rest_night(6.0), 0.0))
	rows.append(_row("comfortless night recovers nothing", ra.rest_night(8.0, false), 0.0))
	rows.append(_row("a real night recovers one", ra.rest_night(), 1.0))
	rows.append(_row("strain after rest", ra.total(), 2.0))
	rows.append(_row("cyberware installs as permanent strain", ca.install_cyber(0.0), true))
	rows.append(_row("and cannot exceed the ceiling", ca.install_cyber(1.0), false))

	# --- Combat: Shock, the hit floor, and trauma ---
	# Contract difference, recorded rather than papered over: the canonical kernel takes `hit` and
	# encodes "Shock only applies on a miss" in the function, while the alternative is miss-only by
	# contract and callers invoke it from the miss branch. Comparing them requires asking the
	# canonical kernel for the miss branch; asserting that its hit branch is zero is the other half
	# of the same rule and is checked below.
	for target_ac in [9, 13, 15, 18]:
		var canon_miss: int = CanonCombat.shock_damage(false, 2, 15, target_ac, 1)
		var alt_miss: int = AltCombat.shock_damage({"amount": 2, "max_ac": 15}, 1, target_ac)
		rows.append(_row("shock on a miss ac=%d" % target_ac, canon_miss, alt_miss))
		rows.append(_row("shock on a hit is nil ac=%d" % target_ac,
			CanonCombat.shock_damage(true, 2, 15, target_ac, 1), 0))

	for roll in [1, 5, 6, 7, 8, 12]:
		rows.append(_row("trauma threshold roll=%d" % roll,
			CanonCombat.is_traumatic_hit(roll), AltCombat.is_traumatic_hit(roll)))

	for dmg in [1, 3, 9]:
		rows.append(_row("shock floor dmg=%d" % dmg,
			CanonCombat.damage_floor(dmg, 3), AltCombat.hit_damage_with_shock_floor(dmg, {"amount": 2, "max_ac": 15}, 1, 13)))

	rows.append(_row("shock never causes trauma", CanonCombat.shock_can_cause_trauma(), false))

	# --- Healing: **retired duplicate**, so these are single-sided assertions ---
	# `src/godot/cwn/cwn_healing.gd` answered the same questions and is gone (#791). Its unique
	# procedures — `rounds_until_death`, `remove_frailty`, `first_aid` — were ported first, and are
	# asserted below alongside the numbers the comparison used to police.
	for rounds in [0, 1, 3]:
		for medkit in [true, false]:
			var expected: int = 8 + rounds + (0 if medkit else 2)
			rows.append(_row("stabilise rounds=%d medkit=%s" % [rounds, medkit],
				int(CanonHealing.stabilize_difficulty(rounds, medkit).get("difficulty", -1)), expected))

	rows.append(_row("rounds left at downing", CanonHealing.rounds_until_death(3, 3), 6))
	rows.append(_row("rounds left three rounds later", CanonHealing.rounds_until_death(3, 6), 3))
	rows.append(_row("the clock runs out", CanonHealing.rounds_until_death(3, 9), 0))
	rows.append(_row("and never runs backwards", CanonHealing.rounds_until_death(3, 1), -1))
	rows.append(_row("past the sixth round the patient is dead", CanonHealing.mortal_wound_expired(6), true))

	for frail in [true, false]:
		rows.append(_row("natural healing frail=%s" % frail,
			CanonHealing.natural_healing(3, frail), 0 if frail else 3))

	rows.append(_row("a week with care ends frailty",
		String(CanonHealing.frail_week(true).get("outcome", "")), "recovered"))
	rows.append(_row("without care and no save, the week refuses",
		bool(CanonHealing.frail_week(false).get("ok", true)), false))
	rows.append(_row("a passed save buys a month",
		String(CanonHealing.frail_week(false, true).get("outcome", "")), "month_more"))
	rows.append(_row("a failed save is death",
		String(CanonHealing.frail_week(false, false).get("outcome", "")), "dying"))

	rows.append(_row("frailty is removed by one check at difficulty 10",
		bool(CanonHealing.remove_frailty(10).get("removed", false)), true))
	rows.append(_row("and only once",
		String(CanonHealing.remove_frailty(15, 10, true).get("reason", "")),
		"frailty_removal_can_only_be_attempted_once"))

	rows.append(_row("first aid with Heal-0", int(CanonHealing.first_aid(4, 0).get("healed", -1)), 3))
	rows.append(_row("first aid with Heal-2", int(CanonHealing.first_aid(4, 2).get("healed", -1)), 6))
	rows.append(_row("first aid needs a medkit",
		bool(CanonHealing.first_aid(4, 2, false).get("ok", true)), false))
	var full_strain := CanonStrain.new(5)
	full_strain.absorb(5.0)
	rows.append(_row("a body at its Strain maximum gains nothing",
		bool(CanonHealing.first_aid(4, 2, true, full_strain).get("ok", true)), false))

	return rows
