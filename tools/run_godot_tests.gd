extends SceneTree

## Headless test runner: `godot --headless --path . --script res://tools/run_godot_tests.gd`
## Loads every tests/godot/test_*.gd, runs its `test_*` methods and exits non-zero on failure.

func _initialize() -> void:
	var total_checks := 0
	var failures: Array[String] = []
	var tests_run := 0

	var dir := DirAccess.open("res://tests/godot")
	if dir == null:
		print("GODOT_TESTS: cannot open res://tests/godot")
		quit(2)
		return

	var files: Array[String] = []
	for file_name in dir.get_files():
		if file_name.begins_with("test_") and file_name.ends_with(".gd"):
			files.append("res://tests/godot/" + file_name)
	files.sort()

	for path in files:
		var script: GDScript = load(path)
		if script == null:
			failures.append("%s: could not load" % path)
			continue
		for method in script.get_script_method_list():
			var method_name: String = method["name"]
			if not method_name.begins_with("test_"):
				continue
			var instance = script.new()
			instance.call(method_name)
			tests_run += 1
			total_checks += instance.checks
			for failure in instance.failures:
				failures.append("%s::%s — %s" % [path.get_file(), method_name, failure])

	print("GODOT_TESTS: %d tests, %d checks, %d failure(s)" % [tests_run, total_checks, failures.size()])
	for failure in failures:
		print("  FAIL " + failure)
	quit(1 if failures.size() > 0 else 0)
