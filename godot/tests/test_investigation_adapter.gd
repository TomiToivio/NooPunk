extends RefCounted
## Tests for the investigation adapter (#718). Mirrors the Python rules, not a second rulebook.

const InvestigationAdapterScript := preload("res://godot/core/investigation_adapter.gd")

func run() -> Array:
	var rows: Array = []
	var adapter = InvestigationAdapterScript.new()

	rows.append(["the shipped case graph loads", not adapter.case_graph.is_empty(), "case_graph.json did not load"])
	rows.append(["the case validates", adapter.validate().is_empty(), str(adapter.validate())])
	rows.append(["every competency is a WN skill", adapter.unknown_competencies().is_empty(), str(adapter.unknown_competencies())])

	var sheet := {"Program": 1, "Notice": 0, "Talk": 0}

	# Rank 0 is trained: Notice 0 counts.
	rows.append(["rank 0 counts as trained", adapter.is_competent(sheet, "Notice"), "Notice 0 was treated as untrained"])
	rows.append(["an absent skill is not competent", not adapter.is_competent(sheet, "Heal"), "Heal was granted without a rating"])

	var entrance := adapter.discover("entrance", sheet)
	rows.append(["a passive core clue is granted without inquiry", entrance["clues"].size() > 0, "entrance yielded nothing"])
	rows.append(["the entrance is leavable", entrance["can_leave"], "no core clue granted at the entrance"])

	var stranger := adapter.discover("entrance", {})
	rows.append(["an untrained investigator gets nothing", stranger["clues"].is_empty(), "clues were granted with an empty sheet"])
	rows.append(["a blocked scene still reports what it withheld", stranger["withheld"].size() > 0, "withheld list was empty"])

	var unknown := adapter.discover("no_such_scene", sheet)
	rows.append(["an unknown scene fails closed", not unknown["can_leave"] and unknown["clues"].is_empty(), "unknown scene granted an exit"])

	return rows
