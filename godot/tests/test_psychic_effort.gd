extends RefCounted

const Psi := preload("res://godot/core/psychic_effort.gd")

func run() -> Array:
	var rows: Array = []
	var psi := Psi.new(14, 10, {"Telepathy": 1})
	rows.append(_eq("SWN psychic effort is 1 + best modifier + rank", psi.capacity(), 3))
	rows.append(_eq("active contact commitment accepted", psi.commit("contact", "Telepathy", 0, "active"), true))
	rows.append(_eq("scene reading commitment accepted", psi.commit("reading", "Telepathy", 1, "scene"), true))
	rows.append(_eq("day vision commitment accepted", psi.commit("vision", "Telepathy", 1, "day"), true))
	rows.append(_eq("zero free effort", psi.free(), 0))
	rows.append(_eq("cannot commit additional effort", psi.commit("extra", "Telepathy"), false))
	rows.append(_eq("cannot prematurely release day commitment", psi.release("vision"), false))
	rows.append(_eq("can release active commitment", psi.release("contact"), true))
	var snapshot: Dictionary = psi.snapshot()
	var restored := Psi.new()
	rows.append(_eq("effort snapshot restores", restored.restore(snapshot), true))
	rows.append(_eq("restored free effort matches", restored.free(), psi.free()))
	restored.end_scene()
	rows.append(_eq("scene recovery leaves day reserve", restored.free(), 2))
	restored.rest()
	rows.append(_eq("rest restores effort", restored.free(), 3))
	rows.append(_eq("untrained discipline rejected", restored.commit("unknown", "Precognition"), false))
	rows.append(_eq("rank prerequisite enforced", restored.commit("advanced", "Telepathy", 2), false))
	return rows

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]
