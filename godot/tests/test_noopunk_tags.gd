extends RefCounted

## #821: NoöPunk tag-based attributes, skills and statuses — the engine half.
##
## The rows mirror `tests/test_noopunk_tags.py` where a rule exists on both sides, so a divergence
## between the tabletop layer of record and the engine shows up as a failing row rather than a
## discovery at the table.

const Tags := preload("res://godot/core/noopunk_tags.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	# --- the seven attributes, in the draft's order ---
	rows.append(_eq("seven attributes", Tags.attributes().size(), 7))
	rows.append(_eq("Fitness is first", String(Tags.attributes()[0]), "Fitness"))
	rows.append(_eq("Empathy is last", String(Tags.attributes()[6]), "Empathy"))
	rows.append(_eq("Cyber is its own attribute", Tags.attributes().has("Cyber"), true))

	# --- the 3d6 bands are the draft's, exactly ---
	for pair in [[3, -2], [4, -1], [7, -1], [8, 0], [13, 0], [14, 1], [17, 1], [18, 2]]:
		rows.append(_eq("a %d rolls to %d" % [pair[0], pair[1]], Tags.modifier_for_score(pair[0]), pair[1]))
	rows.append(_eq("the human range is -2..+2", [Tags.human_min(), Tags.human_max()], [-2, 2]))
	rows.append(_eq("the non-human floor is -3", Tags.empathy_floor(), -3))
	rows.append(_eq("the untrained penalty is -1", Tags.untrained_penalty(), -1))

	# --- tags keep skill ranks and penalties apart ---
	var shoot := Tags.skill_tag("Firearms", 1)
	rows.append(_eq("a skill tag displays its rank", shoot.display(), "Firearms-1"))
	var wounded := Tags.status_tag("wounded", 1)
	rows.append(_eq("a status tag displays its penalty", wounded.display(), "wounded-1"))
	rows.append(_eq("an attribute tag shows its sign", Tags.attribute_tag("Cognition", 2).display(), "Cognition+2"))
	rows.append(_eq("a negative attribute shows a minus", Tags.attribute_tag("Fitness", -2).display(), "Fitness-2"))
	rows.append(_eq("a Unicode skill name is kept", Tags.skill_tag("Noöware", 2).display(), "Noöware-2"))
	rows.append(_eq("a trait is bare", Tags.Tag.new("trait", "Noögenetic").display(), "Noögenetic"))

	# --- a sheet, its humanity and its PC eligibility ---
	var human := Tags.Sheet.new({"Fitness": 1, "Empathy": 0}, {"Firearms": 1})
	rows.append(_eq("a human sheet validates", human.validate(), ""))
	rows.append(_eq("a human is human", human.is_human(), true))
	rows.append(_eq("and may be a player character", human.pc_eligible(), true))
	rows.append(_eq("and is not transhuman", human.is_transhuman(), false))
	var nonhuman := Tags.Sheet.new({"Empathy": -3})
	rows.append(_eq("Empathy -3 is not human", nonhuman.is_human(), false))
	rows.append(_eq("and is not a player character", nonhuman.pc_eligible(), false))
	var trans := Tags.Sheet.new({"Cyber": 3})
	rows.append(_eq("above +2 is transhuman", trans.is_transhuman(), true))
	rows.append(_eq("and still a player character", trans.pc_eligible(), true))
	rows.append(_eq("the storable floor stops at -4", Tags.Sheet.new({"Empathy": -4}).validate(),
		"Empathy_-4_outside_the_storable_range"))
	rows.append(_eq("an unknown skill is refused", Tags.Sheet.new({}, {"Basketweaving": 1}).validate(),
		"unknown_skill_Basketweaving"))

	# --- the sheet prints as tags, and never as raw scores ---
	var lines := human.sheet_lines()
	rows.append(_eq("the sheet prints tags", lines.has("Firearms-1"), true))
	rows.append(_eq("attribute tags carry a sign", lines.has("Empathy+0"), true))
	rows.append(_eq("no raw 3d6 score leaks onto the sheet", lines.has("11"), false))

	# --- checks: trained, untrained, contextual, statuses ---
	var armed := Tags.Sheet.new({"Reflexes": 2}, {"Firearms": 1})
	var hit := armed.check("Reflexes", "Firearms", 7, 10)
	rows.append(_eq("a trained check totals dice+attribute+rank", int(hit.get("total", 0)), 10))
	rows.append(_eq("and meets difficulty 10", bool(hit.get("success", false)), true))
	var raw := Tags.Sheet.new({"Cognition": 0})
	var untrained := raw.check("Cognition", "Research", 7, 8)
	rows.append(_eq("an untrained action uses -1", int(untrained.get("rank", 0)), -1))
	rows.append(_eq("so 2d6+0-1 misses difficulty 8", bool(untrained.get("success", true)), false))
	rows.append(_eq("a contextual skill refuses the wrong attribute",
		String(Tags.Sheet.new({}, {"Talk": 1}).check("Reflexes", "Talk", 7).get("reason", "")),
		"contextual_skill_wrong_attribute"))
	rows.append(_eq("Talk+Empathy is allowed",
		bool(Tags.Sheet.new({}, {"Talk": 1}).check("Empathy", "Talk", 7).get("ok", false)), true))
	rows.append(_eq("Talk+Agency is allowed",
		bool(Tags.Sheet.new({}, {"Talk": 1}).check("Agency", "Talk", 7).get("ok", false)), true))
	rows.append(_eq("an unknown skill refuses the check",
		String(raw.check("Cognition", "Astrology", 7).get("reason", "")), "unknown_skill"))

	# --- statuses: stacking, exclusivity, expiry ---
	var hurt := Tags.Sheet.new({"Fitness": 1})
	hurt.add_status(Tags.status_tag("wounded", 1))
	hurt.add_status(Tags.status_tag("wounded", 2))
	rows.append(_eq("highest stacking keeps the worse penalty", hurt.status_penalty(), 2))
	hurt.add_status(Tags.status_tag("wounded", 1, "scene", "", "stack"))
	rows.append(_eq("stacking adds them", hurt.status_penalty(), 4))
	var exclusive := Tags.Sheet.new({})
	exclusive.add_status(Tags.status_tag("stunned", 2, "scene", "", "replace"))
	exclusive.add_status(Tags.status_tag("panicked", 1, "scene", "", "replace", ["stunned"]))
	rows.append(_eq("an exclusive status replaces its rival", exclusive.statuses.size(), 1))
	rows.append(_eq("the survivor is the new one", String(exclusive.statuses[0].name), "panicked"))
	var timed := Tags.Sheet.new({})
	timed.add_status(Tags.status_tag("wounded", 1, "scene", "", "replace"))
	timed.add_status(Tags.status_tag("marked", 1, "permanent", "", "replace"))
	rows.append(_eq("a scene ends and takes its statuses", timed.expire("scene").size(), 1))
	rows.append(_eq("permanent tags survive", timed.statuses.size(), 1))
	rows.append(_eq("and are never expired", timed.expire("permanent").size(), 0))

	# --- serialisation round-trip ---
	var saved := armed.to_dict()
	saved["statuses"] = [Tags.status_tag("wounded", 1).to_dict()]
	var restored := Tags.Sheet.from_dict(saved)
	rows.append(_eq("attributes survive the round-trip", restored.attributes, armed.attributes))
	rows.append(_eq("skills survive", restored.skills, armed.skills))
	rows.append(_eq("statuses survive", restored.statuses.size(), 1))
	rows.append(_eq("and still display as tags", String(restored.statuses[0].display()), "wounded-1"))

	# --- the draft's undecided points stay undecided ---
	var questions: Array = Tags.contract().get("open_questions", [])
	rows.append(_eq("the open questions are carried, not answered", questions.size() >= 6, true))
	rows.append(_eq("and the impossible-untrained list is empty until Tomi rules",
		(Tags.contract().get("skills", {}).get("untrained", {}).get("impossible_without", []) as Array).size(), 0))

	return rows
