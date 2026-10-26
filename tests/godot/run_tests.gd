extends SceneTree

## Headless test runner for the playable slice. Run with:
##   godot --headless --path . --script res://tests/godot/run_tests.gd
## Exits non-zero on any failure, so CI can gate on it.

var failures := 0
var checks := 0

func check(condition: bool, label: String) -> void:
	checks += 1
	if condition:
		print("  ok   ", label)
	else:
		failures += 1
		print("  FAIL ", label)

func _initialize() -> void:
	print("== case state ==")
	_test_state()
	print("== without number adapter ==")
	_test_rules()
	print("== case data ==")
	_test_data()
	print("== scene builds ==")
	_test_scene()
	print("")
	print("%d checks, %d failure(s)" % [checks, failures])
	quit(1 if failures > 0 else 0)

func _test_state() -> void:
	var CaseState = load("res://src/godot/case_state.gd")
	var state = CaseState.new("lakkahaltia")
	check(state.add_evidence("ev_trial"), "first evidence is new")
	check(not state.add_evidence("ev_trial"), "duplicate evidence is refused")
	check(state.evidence.size() == 1, "evidence stored once")
	state.set_flag("talked_doctor", true)
	check(state.get_flag("talked_doctor") == true, "flag round-trips in memory")
	check(not state.can_end(4), "cannot end below the threshold")
	for id in ["a", "b", "c"]:
		state.add_evidence(id)
	check(state.can_end(4), "can end at the threshold")
	state.finish("publish")
	check(state.ending == "publish", "ending recorded")
	state.finish("contain")
	check(state.ending == "publish", "first ending wins")

	var path := "user://test_state_%d.json" % Time.get_ticks_usec()
	check(state.save_to(path), "save writes")
	var restored = CaseState.new("lakkahaltia")
	check(restored.load_from(path), "load reads")
	check(restored.evidence.size() == state.evidence.size(), "evidence survives save/load")
	check(restored.get_flag("talked_doctor") == true, "flags survive save/load")
	check(restored.ending == "publish", "ending survives save/load")

	var other = CaseState.new("some_other_case")
	check(not other.load_from(path), "a save from another case is refused")

func _test_rules() -> void:
	var WnRules = load("res://src/godot/wn_rules.gd")
	var rules = WnRules.new()
	check(rules.attribute_modifier(3) == -2, "score 3 -> -2")
	check(rules.attribute_modifier(8) == 0, "score 8 -> 0")
	check(rules.attribute_modifier(18) == 2, "score 18 -> +2")
	var explicit: Dictionary = rules.skill_check(14, 2, 8, null, [3, 5])
	check(int(explicit.get("total", -1)) == 3 + 5 + 1 + 2, "2d6 + modifier + skill")
	var rng_a := RandomNumberGenerator.new()
	rng_a.seed = 631
	var rng_b := RandomNumberGenerator.new()
	rng_b.seed = 631
	var roll_a: Dictionary = rules.skill_check(12, 1, 8, rng_a)
	var roll_b: Dictionary = rules.skill_check(12, 1, 8, rng_b)
	check(roll_a.get("total") == roll_b.get("total"), "same seed replays exactly")

func _test_data() -> void:
	var file := FileAccess.open("res://data/godot/lakkahaltia_case.json", FileAccess.READ)
	check(file != null, "case data opens")
	if file == null:
		return
	var data: Dictionary = JSON.parse_string(file.get_as_text())
	check(data.has("npcs") and data["npcs"].size() >= 3, "at least three conversational NPCs")
	check(data.has("clues") and data["clues"].size() >= 4, "clue table present")
	check(data.has("endings") and data["endings"].size() >= 2, "two ambiguous endings")
	var stats: Dictionary = data["player"]["stats"]
	check(stats.has("Strength") and stats.has("Charisma"), "Without Number attribute names")
	check(not stats.has("PSY"), "the superseded NooPunk stat set is not used here")

func _test_scene() -> void:
	var packed = load("res://scenes/case/lakkahaltia.tscn")
	check(packed != null, "case scene loads")
	if packed == null:
		return
	var instance = packed.instantiate()
	get_root().add_child(instance)
	# Nodes added during SceneTree._initialize() are not yet processed, so _ready() has not run.
	# Calling it explicitly keeps this smoke test deterministic instead of frame-timing dependent.
	if instance.get_child_count() == 0:
		instance._ready()
	check(instance.get_child_count() > 8, "level, player and NPCs were built")
	check(instance.player != null, "player exists")
	check(instance.camera != null, "camera exists")
	check(instance.ui_text != null, "dialogue UI exists")
	check(instance.state != null, "case state attached")
	instance.queue_free()
