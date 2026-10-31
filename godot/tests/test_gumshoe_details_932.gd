extends RefCounted

const Investigation = preload("res://godot/narrative/investigation.gd")

func _check(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]

func run() -> Array:
	var rows: Array = []
	var notebook = Investigation.from_data({"clues": [
		{"id": "lead", "essential": true, "opens": ["records"]},
		{"id": "leveraged", "essential": false, "prerequisite_clues": ["lead"]},
		{"id": "timed", "essential": false, "available_after": 3}
	]})
	rows.append(_check("leveraged clue waits for earlier evidence",
		notebook.gather("leveraged", true).get("reason"), "prerequisite_not_found"))
	rows.append(_check("timed clue waits for case time",
		notebook.gather("timed", true, {"elapsed": 2}).get("reason"), "not_ready"))
	rows.append(_check("core clue ignores failed roll",
		notebook.gather("lead", false).get("found"), true))
	rows.append(_check("leveraged clue follows known evidence",
		notebook.gather("leveraged", true).get("found"), true))
	rows.append(_check("timed clue unlocks at threshold",
		notebook.gather("timed", true, {"elapsed": 3}).get("found"), true))
	notebook.set_expertise(["hospital_procedure", "cyber_forensics"])
	rows.append(_check("expertise descriptors are retained",
		notebook.expertise_tags.size(), 2))
	return rows
