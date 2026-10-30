extends RefCounted

## #848: the SRD hacking catalogue, transcribed rather than remembered.
##
## Two failures matter more than the counts. First, a Verb must not be usable on a Subject type the SRD
## forbids — Glitch is Device/Cyber, so Drone is legal and Datafile is not, which is the SRD's own
## example. Second, a Verb with no Security roll (Defend) must not report a modifier of 0 as though 0 were
## a rule; the check flag exists so callers cannot confuse "no roll" with "no change".
const Catalogue := preload("res://godot/core/cwn_hacking_catalogue.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	rows.append(_eq("twenty-four verbs from the SRD 4.3.2", Catalogue.verbs().size(), 24))
	rows.append(_eq("twelve subjects from the SRD 4.3.3", Catalogue.subjects().size(), 12))

	# the SRD's own worked example
	rows.append(_eq("Glitch may target a Drone", Catalogue.can_target("Glitch", "Drone"), true))
	rows.append(_eq("Glitch may not target a Datafile", Catalogue.can_target("Glitch", "Datafile"), false))
	rows.append(_eq("Glitch targets Device and Cyber",
		Catalogue.verb("Glitch").get("target_types"), ["Device", "Cyber"]))
	rows.append(_eq("Glitch modifier is +2", Catalogue.difficulty_modifier("Glitch"), 2))
	rows.append(_eq("Sabotage modifier is -1", Catalogue.difficulty_modifier("Sabotage"), -1))
	rows.append(_eq("Siege modifier is -2", Catalogue.difficulty_modifier("Siege"), -2))

	# Defend has no roll: N/A must not be read as a 0 modifier
	rows.append(_eq("Defend has no security check", Catalogue.has_security_check("Defend"), false))
	rows.append(_eq("a rollable verb has a security check", Catalogue.has_security_check("Glitch"), true))
	rows.append(_eq("Defend's non-modifier is not confused with zero",
		Catalogue.verb("Defend").get("difficulty_modifier"), null))

	# prices, as printed
	rows.append(_eq("Sabotage price", Catalogue.price("Sabotage"), 2000))
	rows.append(_eq("Glitch price", Catalogue.price("Glitch"), 1000))
	rows.append(_eq("Camera subject price", Catalogue.subject_price("Camera"), 500))
	rows.append(_eq("Turret subject price", Catalogue.subject_price("Turret"), 1000))

	# CPU retention: asterisked verbs keep their slot until terminated (4.2.1 step 4)
	rows.append(_eq("Sabotage keeps its CPU slot", Catalogue.occupies_cpu("Sabotage"), true))
	rows.append(_eq("Glitch self-terminates", Catalogue.occupies_cpu("Glitch"), false))

	# a Verb paired with an unknown Subject is a refusal, not a crash
	rows.append(_eq("unknown subject refused", Catalogue.can_target("Glitch", "Nonesuch"), false))
	rows.append(_eq("unknown verb refused", Catalogue.can_target("Nonesuch", "Drone"), false))

	# every Subject declares one of the SRD's target types
	var known: Array = Catalogue._data().get("target_types", [])
	for s in Catalogue.subjects():
		var ok: bool = str(s.get("target_type")) in known.map(func(v): return str(v))
		rows.append(["subject %s has a valid target type" % s.get("name"), ok, str(s.get("target_type"))])

	return rows
