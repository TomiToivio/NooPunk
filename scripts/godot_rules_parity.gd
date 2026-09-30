# Godot-side parity check for the canonical NoöPunk rules (issue #11).
#
# Run headless:
#   godot --headless --path . --script scripts/godot_rules_parity.gd
#
# This does NOT re-declare any rule. It loads data/rules/core.json through the
# Godot adapter and asserts the results against the author-specified table, so a
# rename applied to only one runtime fails here rather than silently reinterpreting
# an old difficulty. The label "Hard" changed target from 12 to 15 in issue #11;
# that is the specific change this exists to catch.
extends SceneTree

const EXPECTED_DIFFICULTIES := {
	"Easiest": 3, "Easier": 6, "Easy": 9,
	"Normal": 12, "Hard": 15, "Impossible": 18,
}

const EXPECTED_ORDER := ["Easiest", "Easier", "Easy", "Normal", "Hard", "Impossible"]

const EXPECTED_MODIFIERS := {
	3: -3, 4: -2, 5: -2, 6: -1, 7: -1, 8: -1,
	9: 0, 10: 0, 11: 0, 12: 0,
	13: 1, 14: 1, 15: 1, 16: 2, 17: 2, 18: 3,
}


func _fail(failures: Array, message: String) -> void:
	failures.append(message)


func _init() -> void:
	var failures: Array = []
	var rules = load("res://src/godot/core_rules.gd").new()
	var no_extras: Array[int] = []

	# --- difficulty names and targets, including order (display parity) ---
	if rules.difficulty_names() != EXPECTED_ORDER:
		_fail(failures, "difficulty names/order mismatch: %s" % [rules.difficulty_names()])
	for name in EXPECTED_DIFFICULTIES.keys():
		var got: int = rules.difficulty_target(name)
		if got != EXPECTED_DIFFICULTIES[name]:
			_fail(failures, "%s -> %d (want %d)" % [name, got, EXPECTED_DIFFICULTIES[name]])
	# the rename itself: Hard is 15 now, Normal is 12
	if rules.difficulty_target("Hard") != 15:
		_fail(failures, "Hard is not 15; the #11 rename did not reach the Godot adapter")
	if rules.difficulty_target("Normal") != 12:
		_fail(failures, "Normal is not 12")
	# removed names must not be present
	for removed in ["Harder", "Hardest"]:
		if EXPECTED_DIFFICULTIES.has(removed):
			_fail(failures, "removed name %s still expected" % removed)

	# --- human generation: every value 3..18 and the boundaries ---
	for raw in range(3, 19):
		var got: int = rules.human_modifier(raw)
		if got != EXPECTED_MODIFIERS[raw]:
			_fail(failures, "human_modifier(%d)=%d want %d" % [raw, got, EXPECTED_MODIFIERS[raw]])
	# out-of-range must be rejected (returns 0 with a pushed error)
	for raw_out in [2, 19]:
		if rules.human_modifier(raw_out) != 0:
			_fail(failures, "human_modifier(%d) should be rejected" % raw_out)

	# --- resolution arithmetic, via the shared adapter ---
	var rng := RandomNumberGenerator.new()
	rng.seed = 20260930

	# Impossible (18) must be resolved numerically, not blocked.
	var impossible = rules.resolve_check(
		rng, 3, rules.difficulty_target("Impossible"), no_extras, true, false
	)
	if impossible["attempted"] != true:
		_fail(failures, "target 18 was blocked instead of resolved")
	if impossible["target"] != 18:
		_fail(failures, "target 18 did not resolve to 18")
	if impossible["total"] != impossible["dice_total"] + 3:
		_fail(failures, "target 18 arithmetic is wrong: %s" % [impossible])

	# skill-required without the skill: blocked BEFORE rolling, no total.
	var blocked = rules.resolve_check(rng, 3, 18, no_extras, false, true)
	if blocked["attempted"] != false:
		_fail(failures, "trained-only without skill was not blocked")
	if blocked["blocked_reason"] != "trained_only_without_skill":
		_fail(failures, "wrong blocked_reason: %s" % [blocked["blocked_reason"]])
	if blocked["total"] != null:
		_fail(failures, "a blocked attempt produced a total")

	# unskilled penalty applies exactly once, and only when unskilled.
	# has_skill=false / trained_only=false is the "unskilled allowed" category.
	var unskilled = rules.resolve_check(rng, 0, 9, no_extras, false, false)
	if unskilled["unskilled_modifier"] != -1:
		_fail(failures, "unskilled modifier is not -1: %s" % [unskilled["unskilled_modifier"]])
	if unskilled["total"] != unskilled["dice_total"] - 1:
		_fail(failures, "unskilled total is wrong: %s" % [unskilled])
	var skilled = rules.resolve_check(rng, 0, 9, no_extras, true, false)
	if skilled["unskilled_modifier"] != 0:
		_fail(failures, "skilled check carried an unskilled penalty")
	if skilled["total"] != skilled["dice_total"]:
		_fail(failures, "skilled total is wrong: %s" % [skilled])

	# extra modifiers, positive and negative, are summed
	var extras: Array[int] = [3, -3]
	var mixed = rules.resolve_check(rng, 0, 12, extras, true, false)
	if mixed["total"] != mixed["dice_total"]:
		_fail(failures, "extra modifiers did not cancel: %s" % [mixed])

	# meeting the target succeeds; totals are compared with >=
	if not rules.compare_opposed(12, 9)["winner"] == "left":
		_fail(failures, "opposed check regressed")
	if not rules.compare_opposed(12, 12)["unresolved_tie"]:
		_fail(failures, "opposed tie is no longer unresolved")

	if failures.is_empty():
		var names: Array = rules.difficulty_names()
		print("GODOT_RULES_PARITY_OK %s Hard=%d Normal=%d Impossible=%d" % [
			names, rules.difficulty_target("Hard"),
			rules.difficulty_target("Normal"), rules.difficulty_target("Impossible"),
		])
	else:
		for failure in failures:
			print("GODOT_RULES_PARITY_FAIL ", failure)
	quit(0 if failures.is_empty() else 1)
