class_name GodotTest
extends RefCounted

## Minimal assertion base for the Godot test runner (tools/run_godot_tests.gd).
## Test methods are named `test_*`; each failure is collected rather than raised so one
## run reports every broken expectation.

var failures: Array[String] = []
var checks: int = 0

func check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures.append(message)

func check_eq(actual: Variant, expected: Variant, message: String) -> void:
	check(actual == expected, "%s (expected %s, got %s)" % [message, str(expected), str(actual)])
