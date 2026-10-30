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
const AltStrain := preload("res://src/godot/cwn/cwn_strain.gd")
const AltCombat := preload("res://src/godot/cwn/cwn_combat.gd")
const AltHealing := preload("res://src/godot/cwn/cwn_healing.gd")
const CanonStrain := preload("res://godot/core/cwn_strain.gd")
const CanonCombat := preload("res://godot/core/cwn_combat_rules.gd")
const CanonHealing := preload("res://godot/core/cwn_healing.gd")

func _row(name: String, left: Variant, right: Variant) -> Array:
	return [name, left == right, "canon=%s alt=%s" % [left, right]]

func run() -> Array:
	var rows: Array = []

	# --- System Strain: ceilings, absorb, forced overflow, rest recovery ---
	for con in [3, 6, 10, 14]:
		var a := CanonStrain.new(con)
		var b := AltStrain.new(con)
		rows.append(_row("strain maximum CON=%d" % con, a.maximum(), int(b.maximum())))
		rows.append(_row("strain empty total CON=%d" % con, a.total(), b.total()))
		rows.append(_row("absorb 2 fits CON=%d" % con, a.absorb(2.0), b.absorb(2.0)))
		rows.append(_row("absent the same CON=%d" % con, a.total(), b.total()))

	var ca := CanonStrain.new(5)
	var cb := AltStrain.new(5)
	ca.absorb(5.0)
	cb.absorb(5.0)
	rows.append(_row("full body refuses", ca.absorb(1.0), cb.absorb(1.0)))
	rows.append(_row("forced overflow refuses", ca.absorb(1.0, true), cb.absorb(1.0, true)))
	rows.append(_row("forced clamps at ceiling", ca.total(), cb.total()))
	rows.append(_row("forced knocks out", ca.unconscious_hours, cb.unconscious_hours))

	var ra := CanonStrain.new(10, 3.0)
	var rb := AltStrain.new(10, 3.0)
	rows.append(_row("short night recovers nothing", ra.rest_night(6.0), rb.rest_night(6.0)))
	rows.append(_row("comfortless night recovers nothing",
		ra.rest_night(8.0, false), rb.rest_night(8.0, false)))
	rows.append(_row("a real night recovers one", ra.rest_night(), rb.rest_night()))
	rows.append(_row("strain after rest", ra.total(), rb.total()))

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

	# --- Healing: stabilisation difficulty and natural healing ---
	for rounds in [0, 1, 3]:
		for medkit in [true, false]:
			var canon_diff: Dictionary = CanonHealing.stabilize_difficulty(rounds, medkit)
			var alt_diff: int = AltHealing.stabilize_difficulty(rounds, medkit)
			rows.append(_row("stabilise rounds=%d medkit=%s" % [rounds, medkit],
				int(canon_diff.get("difficulty", -1)), alt_diff))

	for frail in [true, false]:
		rows.append(_row("natural healing frail=%s" % frail,
			CanonHealing.natural_healing(3, frail), AltHealing.natural_healing(3, frail)))

	# --- Healing: a passed/failed week ---
	rows.append(_row("week with care",
		str(CanonHealing.frail_week(true).get("outcome", CanonHealing.frail_week(true).get("result", ""))),
		AltHealing.frail_week(true)))

	return rows
