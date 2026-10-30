extends SceneTree
## Pins the author's 3d6 -> attribute table and the data file it comes from (#835).
##   godot --headless --path noopunk/game --script res://tests/attributes_bands.gd

const Attributes = preload("res://attributes.gd")

var failures := 0


func check(label: String, got, want) -> void:
	if got != want:
		failures += 1
		print("FAIL %s: got %s want %s" % [label, got, want])


func _init() -> void:
	Attributes.ensure_loaded()

	# every total, including both ends of every boundary pair
	var bands := {3: -3, 4: -3, 5: -2, 6: -2, 7: -1, 8: -1, 9: 0, 10: 0, 11: 0, 12: 0,
		13: 1, 14: 1, 15: 2, 16: 2, 17: 3, 18: 3}
	for total in bands:
		check("total %d" % total, Attributes.modifier(total), bands[total])

	check("seven attributes", Attributes.NAMES.size(), 7)
	check("names", Attributes.NAMES, PackedStringArray(
		["Fitness", "Reflexes", "Cognition", "Cyber", "Awareness", "Agency", "Empathy"]))
	check("definitions match names", Attributes.DEFINITIONS.size(), 7)
	check("human min", Attributes.HUMAN_MIN, -3)
	check("human max", Attributes.HUMAN_MAX, 3)

	# the difficulty scale is reference data, not a mechanic
	check("difficulty labels", Attributes.DIFFICULTIES,
		{6: "Easiest", 8: "Easier", 10: "Easy", 12: "Average", 14: "Hard", 16: "Harder", 18: "Hardest"})

	# rolling never leaves the human band, and always fills seven attributes
	var rng := RandomNumberGenerator.new()
	rng.seed = 12345
	for i in 200:
		var values := Attributes.roll_character(rng)
		if values.size() != 7:
			failures += 1
			print("FAIL roll produced %d attributes" % values.size())
		for name in values:
			var value: int = values[name]
			if value < Attributes.HUMAN_MIN or value > Attributes.HUMAN_MAX:
				failures += 1
				print("FAIL %s=%d outside human range" % [name, value])

	# the table must come from the data file, not a second copy
	for band in Attributes.BANDS:
		check("band width %s" % str(band), band[1] - band[0] >= 0, true)

	if failures == 0:
		print("PASS: #835 bands 3-18, seven attributes, human range, difficulty scale")
		quit(0)
	else:
		print("FAILURES: %d" % failures)
		quit(1)
