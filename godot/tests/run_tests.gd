## Headless test runner for the #631 slice.
##
##   godot --headless --path . --script res://godot/tests/run_tests.gd
##
## The runner is a `SceneTree` because that is what `--script` requires. Each suite is a plain object with
## a `run() -> Array` returning `[name, ok, detail]` rows; nothing here depends on the renderer, so the
## same command works in CI.
extends SceneTree

const SUITES := [
	"res://godot/tests/test_party.gd",
	"res://godot/tests/test_noopunk_tags.gd",
	"res://godot/tests/test_tags.gd",
	"res://godot/tests/test_member_sheet.gd",
	"res://godot/tests/test_field_agent.gd",
	"res://godot/tests/test_campaign_migration.gd",
	"res://godot/tests/test_cwn_party.gd",
	"res://godot/tests/test_campaign_state.gd",
	"res://godot/tests/test_cwn_engine.gd",
	"res://godot/tests/test_cwn_injury.gd",
	"res://godot/tests/test_cwn_alienation.gd",
	"res://godot/tests/test_rules_adapter.gd",
	"res://godot/tests/test_combat.gd",
	"res://godot/tests/test_hacking.gd",
	"res://godot/tests/test_cwn_hacking_catalogue.gd",
	"res://godot/tests/test_scene_flow.gd",
	"res://godot/tests/test_session.gd",
	"res://godot/tests/test_mvp_scene.gd",
	"res://godot/tests/test_psychic_effort.gd",
	"res://godot/tests/test_game_state.gd",
	"res://godot/tests/test_dialogue.gd",
	"res://godot/tests/test_scenario_data.gd",
	"res://godot/tests/test_cwn_procedures.gd",
	"res://godot/tests/test_cwn_catalogue.gd",
	"res://godot/tests/test_cwn_vehicles.gd",
	"res://godot/tests/test_cwn_srd_vehicles.gd",
	"res://godot/tests/test_level_doors.gd",
	"res://godot/tests/test_investigation_adapter.gd",
]

func _initialize() -> void:
	var failures := 0
	var total := 0
	print("NoöPunk Godot slice — headless tests")
	for path in SUITES:
		var script: Script = load(path)
		if script == null or not script.can_instantiate():
			print("  FAIL  could not load suite %s" % path)
			failures += 1
			continue
		var suite: Object = script.new()
		var rows: Array = suite.run()
		for row in rows:
			total += 1
			var ok := bool(row[1])
			if not ok:
				failures += 1
			print("  %s  %s%s" % ["PASS" if ok else "FAIL", String(row[0]),
				"" if ok else "  — " + String(row[2])])
	print("%d checks, %d failed" % [total, failures])
	quit(1 if failures > 0 else 0)
