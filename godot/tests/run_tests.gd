## Headless test runner for the #631 slice.
##
##   godot --headless --path . --script res://godot/tests/run_tests.gd
##
## The runner is a `SceneTree` because that is what `--script` requires. Each suite is a plain object with
## a `run() -> Array` returning `[name, ok, detail]` rows; nothing here depends on the renderer, so the
## same command works in CI.
extends SceneTree

const SUITES := [
	"res://godot/tests/test_unsa_field_operations_920.gd",
	"res://godot/tests/test_faction_intelligence_922.gd",
	"res://godot/tests/test_party.gd",
	"res://godot/tests/test_noopunk_tags.gd",
	"res://godot/tests/test_tags.gd",
	"res://godot/tests/test_member_sheet.gd",
	"res://godot/tests/test_field_agent.gd",
	"res://godot/tests/test_campaign_migration.gd",
	"res://godot/tests/test_cwn_party.gd",
	"res://godot/tests/test_node_link.gd",
	"res://godot/tests/test_campaign_state.gd",
	"res://godot/tests/test_cwn_engine.gd",
	"res://godot/tests/test_cwn_sheet.gd",
	"res://godot/tests/test_image_library.gd",
	"res://godot/tests/test_city_map.gd",
	"res://godot/tests/test_cwn_injury.gd",
	"res://godot/tests/test_cwn_alienation.gd",
	"res://godot/tests/test_cwn_lifestyles.gd",
	"res://godot/tests/test_cwn_wages.gd",
	"res://godot/tests/test_cwn_drugs.gd",
	"res://godot/tests/test_rules_adapter.gd",
	"res://godot/tests/test_combat.gd",
	"res://godot/tests/test_hacking.gd",
	"res://godot/tests/test_chase_screen.gd",
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
	"res://godot/tests/test_noopunk_psyche.gd",
	"res://godot/tests/test_helsinki_913.gd",
	"res://godot/tests/test_narrative_897.gd",
	"res://godot/tests/test_location_screen.gd",
	"res://godot/tests/test_images_908.gd",
	"res://godot/tests/test_cwn_vanilla.gd",
	"res://godot/tests/test_cwn_vehicles.gd",
	"res://godot/tests/test_cwn_srd_vehicles.gd",
	"res://godot/tests/test_cwn_cyberware.gd",
	"res://godot/tests/test_cwn_drones.gd",
	"res://godot/tests/test_narrative_slice.gd",
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
		# Release suite references before engine shutdown.
		suite = null
		rows.clear()
		script = null
	# Give queued Control frees and renderer cleanup a chance to run before the summary and quit.
	await process_frame
	await process_frame
	print("%d checks, %d failed" % [total, failures])

	# Free what the suites attached to the tree. Without this, every scene a test instantiated is still
	# alive when the process exits, Godot reports it as leaked, and the leak counter becomes background
	# noise - which is exactly how a real leak survives. Autoloads are left alone: they are the project's
	# own singletons, not test fixtures.
	for child in root.get_children():
		if child is Window:
			continue
		if child.name in _autoload_names():
			continue
		child.free()

	quit(1 if failures > 0 else 0)


func _autoload_names() -> Array:
	var names: Array = []
	for prop in ProjectSettings.get_property_list():
		var key: String = String(prop.get("name", ""))
		if key.begins_with("autoload/"):
			names.append(key.substr("autoload/".length()))
	return names
