extends "res://tests/godot/godot_test.gd"

func _scores() -> Dictionary:
	return {"STR": 10, "DEX": 10, "CON": 14, "INT": 10, "WIS": 12, "CHA": 10}

func _psychic() -> SWNPsionics:
	var psi := SWNPsionics.new()
	check(psi.setup(SWNPsionics.FULL, _scores(), {"Biopsionics": 1, "Telepathy": 0}), "valid full psychic")
	return psi

func test_class_gates_and_effort() -> void:
	var p := SWNPsionics.new()
	check(not p.setup("", _scores(), {"Biopsionics": 0}), "nonpsychic refused")
	check(not p.setup(SWNPsionics.PARTIAL, _scores(), {"Biopsionics": 0, "Telepathy": 0}), "partial limited to one discipline")
	check(p.setup(SWNPsionics.PARTIAL, _scores(), {"Biopsionics": 0}), "partial psychic valid")
	check(not p.learn_discipline("Telepathy"), "second partial discipline refused")
	check_eq(p.max_effort(), 2, "CON modifier raises Effort")
	check(not p.set_advanced_rank("Biopsionics", 1, false), "advancement requires authorization")
	check(p.set_advanced_rank("Biopsionics", 1, true), "legal authorized advance")
	check_eq(p.max_effort(), 3, "increased discipline grants Effort")

func test_technique_access_commitment_and_lifecycle() -> void:
	var p := _psychic()
	check(not p.learn_technique("training", "Telepathy", 1, true), "reject unmet prerequisite")
	check(not p.learn_technique("training", "Biopsionics", 1, false), "cannot bypass earned technique")
	check(p.learn_technique("training", "Biopsionics", 1, true), "learn authorized technique")
	check(p.activate("training", "one", "scene"), "commit scene Effort")
	check(not p.activate("training", "one", "scene"), "unique commitment key")
	check(not p.release_active("one"), "scene Effort cannot be released early")
	check_eq(p.free_effort(), 2, "one Effort committed")
	p.end_scene()
	check_eq(p.free_effort(), 3, "scene Effort refunded")
	check(p.activate("training", "two", "day"), "commit for day")
	p.end_scene()
	check_eq(p.free_effort(), 2, "day commitment survives scene")
	p.rest()
	check_eq(p.free_effort(), 3, "rest restores pool")

func test_torch_uses_d6_and_damages_attributes() -> void:
	var p := _psychic()
	check_eq(p.torch(1, 1).get("damage_attribute"), "WIS", "torch 1 harms WIS")
	check_eq(p.attributes["WIS"], 11, "one attribute point lost")
	check(not p.torch(1, 6).get("ok"), "cannot torch twice per round")
	check_eq(p.torch(2, 6).get("damage_attribute"), "", "six is harmless")
	check_eq(p.free_effort(), p.max_effort() + 2, "temporary over-cap Effort")
	check(not p.torch(3, 5, "INVALID").get("ok"), "choice required on five")
	p.end_scene()
	check_eq(p.free_effort(), p.max_effort(), "torch bonus expires with scene")

func test_succor_and_teleport_core() -> void:
	var result := SWNPsionics.psychic_succor(1, [4], 2, 12, 0, 12, false)
	check(result.get("ok", false), "legal healing")
	check_eq(result.get("hp"), 7, "1d6+1 recovery")
	check_eq(result.get("strain"), 1, "strain increases")
	check(not SWNPsionics.psychic_succor(0, [], 2, 12, 0, 12, false).get("ok"), "rank zero cannot heal ordinary HP")
	check(SWNPsionics.psychic_succor(0, [], 0, 12, 0, 12, true).get("stabilized", false), "rank zero stabilizes")
	check(not SWNPsionics.psychic_succor(1, [4], 2, 12, 12, 12, false).get("ok"), "strain ceiling applies")
	check_eq(SWNPsionics.teleport_range_meters(0), 10.0, "rank zero range")
	check_eq(SWNPsionics.teleport_range_meters(3), 1000000.0, "rank three range")

func test_snapshot_roundtrip() -> void:
	var p := _psychic()
	p.learn_technique("training", "Biopsionics", 1, true)
	p.activate("training", "one", "day")
	p.torch(1, 6)
	var saved := p.snapshot()
	var restored := SWNPsionics.new()
	check(restored.restore(saved), "restore legal psychic")
	check_eq(restored.snapshot(), saved, "roundtrip lossless")
	var invalid := saved.duplicate(true)
	invalid["skills"] = {"UnknownDiscipline": 4}
	check(not restored.restore(invalid), "unknown discipline rejected")
	check_eq(restored.snapshot(), saved, "invalid load is atomic")
