extends SceneTree
## Run: godot --headless --path . --script godot/tests/test_cwn_program_rules.gd

func _initialize() -> void:
	assert(CwnProgramRules.VERBS.size() == 24)
	var info := CwnProgramRules.verb_info("Analyze")
	assert(info["access_cost"] == 0)
	assert(info["self_terminating"])
	assert(info["check_modifier"] == 1)
	var loaded_v := ["Analyze", "Blind", "Defend"]
	var loaded_s := ["Camera"]
	var p := CwnProgramRules.preflight("Blind", "Device", 2, 0, 2, loaded_v, loaded_s, "Camera")
	assert(p["ok"])
	var run := CwnProgramRules.resolve(p, 2, 0, true, "blind-camera")
	assert(run["access"] == 1 and run["cpu_used"] == 1)
	assert(run["running_program"] == "blind-camera")
	var failed := CwnProgramRules.resolve(p, 2, 0, false)
	assert(failed["access"] == 1 and failed["cpu_used"] == 0)
	assert(not CwnProgramRules.preflight("Blind", "Data", 2, 0, 2, loaded_v, loaded_s, "Camera")["ok"])
	assert(CwnProgramRules.preflight("Blind", "Device", 0, 0, 2, loaded_v, loaded_s, "Camera")["reason"] == "insufficient_access")
	assert(CwnProgramRules.preflight("Blind", "Device", 2, 2, 2, loaded_v, loaded_s, "Camera")["reason"] == "no_cpu")
	assert(CwnProgramRules.preflight("Hijack", "Device", 2, 0, 2, loaded_v, loaded_s, "Camera")["reason"] == "not_loaded")
	assert(CwnProgramRules.preflight("Defend", "Device", 2, 0, 2, loaded_v, loaded_s, "Camera", false)["reason"] == "defend_requires_ally")
	assert(CwnProgramRules.terminate_on_disconnect(false, false, false, true))
	assert(not CwnProgramRules.terminate_on_disconnect(true, false, false, true))
	assert(CwnProgramRules.terminate_on_disconnect(true, false, true, false))
	print("CWN program verbs: PASS")
	quit(0)
