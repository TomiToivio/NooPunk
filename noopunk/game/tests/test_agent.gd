extends SceneTree
## Pins the author's 3d6 -> attribute table (#835). Run:
##   godot --headless --path noopunk/game --script res://tests/test_agent.gd

var failures := 0


func check(label: String, got, want) -> void:
	if got != want:
		failures += 1
		print("FAIL %s: got %s want %s" % [label, got, want])


func _init() -> void:
	var bands := {3: -3, 4: -3, 5: -2, 6: -2, 7: -1, 8: -1, 9: 0, 10: 0, 11: 0, 12: 0,
		13: 1, 14: 1, 15: 2, 16: 2, 17: 3, 18: 3}
	for total in bands:
		check("total %d" % total, Agent.value_for_total(total), bands[total])

	check("human min", Agent.HUMAN_MIN, -3)
	check("human max", Agent.HUMAN_MAX, 3)
	check("signed positive", Agent.signed(2), "+2")
	check("signed negative", Agent.signed(-3), "-3")
	check("signed zero", Agent.signed(0), "+0")

	var rows := Agent.roll_sheet()
	check("seven attributes", rows.size(), 7)
	var names := PackedStringArray()
	for row in rows:
		names.append(row[0])
		if row[2] < -3 or row[2] > 3:
			failures += 1
			print("FAIL value out of human range: %s=%d" % [row[0], row[2]])
	check("attribute names", names, PackedStringArray(
		["Fitness", "Reflexes", "Cognition", "Cyber", "Awareness", "Agency", "Empathy"]))

	# a rolled sheet is never transhuman, and 200 rolls stay inside the table
	for i in 200:
		if Agent.is_transhuman(Agent.roll_sheet()):
			failures += 1
			print("FAIL rolled sheet reported transhuman")

	print("checks done, failures: %d" % failures)
	quit(0 if failures == 0 else 1)
