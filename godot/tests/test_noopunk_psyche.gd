## The Psyche overlay: exposure is a narrative meter, not an illness (#897).
extends RefCounted

const Psyche := preload("res://mods/noopunk/psyche.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func run() -> Array:
	var rows: Array = []

	# --- exposure -----------------------------------------------------------
	rows.append(_eq("exposure raises the meter", Psyche.expose(2, 3)["exposure"], 5))
	rows.append(_eq("resilience dampens the gain", Psyche.expose(2, 3, 2)["exposure"], 3))
	rows.append(_eq("resilience cannot negate exposure entirely",
		Psyche.expose(2, 3, 9)["gained"], 0))
	rows.append(_eq("exposure is capped", Psyche.expose(9, 5)["exposure"], 10))
	rows.append(_eq("negative exposure is refused", Psyche.expose(-1, 1)["ok"], false))
	rows.append(_eq("exposure is reported as a narrative event, not damage",
		Psyche.expose(1, 1)["narrative_event"], true))

	# --- tiers and consequences ---------------------------------------------
	rows.append(_eq("zero exposure is calm", Psyche.tier(0), 0))
	rows.append(_eq("low exposure is attunement", Psyche.tier(2), 1))
	rows.append(_eq("mid exposure is intrusion", Psyche.tier(5), 2))
	rows.append(_eq("high exposure is dissociation", Psyche.tier(8), 3))
	rows.append(_eq("maximum exposure is overwhelm", Psyche.tier(10), 4))
	rows.append(_eq("overwhelm owes a scene, not a penalty", Psyche.owes_narrative_beat(10), true))
	rows.append(_eq("attunement owes no scene", Psyche.owes_narrative_beat(2), false))

	# --- recovery -----------------------------------------------------------
	rows.append(_eq("recovery lowers exposure", Psyche.recover(5, 2)["exposure"], 3))
	rows.append(_eq("recovery cannot go negative", Psyche.recover(1, 5)["exposure"], 0))
	rows.append(_eq("recovery reports what it removed", Psyche.recover(3, 2)["recovered"], 2))

	# --- the open design question -------------------------------------------------
	var undecided := Psyche.active_psi_status()
	rows.append(_eq("active PSI is undecided by default", undecided["status"], "undecided"))
	rows.append(_eq("the open question is stated, not silently answered",
		String(undecided["note"]).contains("open design question"), true))
	rows.append(_eq("a campaign may allow it explicitly",
		Psyche.active_psi_status("allowed")["status"], "allowed"))
	rows.append(_eq("a campaign may deny it explicitly",
		Psyche.active_psi_status("denied")["status"], "denied"))
	rows.append(_eq("an unknown flag is refused", Psyche.active_psi_status("maybe")["ok"], false))

	return rows
