## Scene-flow checks for #749: the Home → HQ → Mission → Debrief chain, its gates and its save.
extends RefCounted

const Flow := preload("res://godot/core/scene_flow.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]

func run() -> Array:
	var rows: Array = []

	# --- the chain -----------------------------------------------------------------
	var f: NoopunkSceneFlow = Flow.new()
	rows.append(_eq("a new game starts at home", f.location, "home"))
	rows.append(_eq("home reaches HQ directly", f.travel("hq")["ok"], true))
	rows.append(_eq("the mission is locked before the briefing", f.travel("mission")["reason"], "not_briefed"))

	f.complete_briefing()
	rows.append(_eq("the briefing opens the mission", f.travel("mission")["ok"], true))
	rows.append(_eq("a mission cannot be skipped from home", Flow.new().travel("mission")["ok"], false))

	rows.append(_eq("an unresolved mission cannot be debriefed", f.travel("debrief")["reason"], "mission_unresolved"))
	rows.append(_eq("an unresolved mission cannot be left", f.travel("hq")["reason"], "mission_unresolved"))

	# --- objectives and resolution --------------------------------------------------
	rows.append(_eq("an objective is recorded once", f.achieve("find_terminal"), true))
	rows.append(_eq("achieving it twice changes nothing", f.achieve("find_terminal"), false))
	rows.append(_eq("the objective reads back as achieved", f.achieved("find_terminal"), true))

	rows.append(_eq("an unknown path is refused", f.resolve("bribery", "success")["reason"], "unknown_path"))
	rows.append(_eq("an unknown result is refused", f.resolve("investigative", "victory")["reason"], "unknown_result"))
	rows.append(_eq("the investigative path resolves the mission", f.resolve("investigative", "success")["ok"], true))
	rows.append(_eq("resolving twice is refused", f.resolve("tactical", "failure")["reason"], "already_resolved"))

	rows.append(_eq("a resolved mission can be debriefed", f.travel("debrief")["ok"], true))
	var ending := f.ending()
	rows.append(_eq("the ending records the path taken", ending["approach"], "investigative"))
	rows.append(_eq("the ending records the conclusion", ending["conclusion"], "success"))
	rows.append(_eq("the ending carries the objectives", ending["objectives"].has("find_terminal"), true))

	# --- a tactical resolution is equally valid -------------------------------------
	var g: NoopunkSceneFlow = Flow.new()
	g.travel("hq")
	g.complete_briefing()
	g.travel("mission")
	g.resolve("tactical", "complication")
	rows.append(_eq("a tactical path may end in a complication", g.ending()["conclusion"], "complication"))
	rows.append(_eq("a complication still allows the debrief", g.travel("debrief")["ok"], true))
	rows.append(_eq("the debrief returns to HQ", g.travel("hq")["ok"], true))

	# --- save round trip -------------------------------------------------------------
	var saved := f.to_dict()
	var restored: NoopunkSceneFlow = Flow.new()
	restored.from_dict(saved)
	rows.append(_eq("a restored flow keeps the location", restored.location, f.location))
	rows.append(_eq("a restored flow keeps the resolution", restored.resolved, true))
	rows.append(_eq("a restored flow keeps the approach", restored.approach, "investigative"))
	rows.append(_eq("a restored flow keeps the objectives", restored.achieved("find_terminal"), true))
	rows.append(_eq("a restored flow keeps the history length", restored.history.size(), f.history.size()))

	var broken: NoopunkSceneFlow = Flow.new()
	rows.append(_eq("unusable save data is refused", broken.from_dict({"location": "moon"}), false))

	return rows
