extends RefCounted
const Stress := preload("res://godot/core/awn_stress.gd")

func check(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "got %s; expected %s" % [actual, expected]]

func run() -> Array:
	var rows: Array = []
	var s := Stress.new(true)
	s.queue_event("kill")
	s.end_scene(10, 15, 20)
	rows.append(check("AWN kill adds two at scene end", s.stress, 2))
	rows.append(check("no check at threshold", s.failed_check_count, 0))
	s.queue_event("ontological_shock")
	rows.append(check("Noopunk event recognized", s.pending_events.size(), 1))
	s.end_scene(3, 15, 20)
	rows.append(check("above Wisdom initiates first check", s.failed_check_count, 1))
	s.queue_event("atrocity_witness")
	var result: Dictionary = s.end_scene(3, 15, 1)
	rows.append(check("failed check offers choice", result.get("status"), "need_choice"))
	rows.append(check("second save penalty stacks", result.get("penalty"), -4))
	rows.append(check("harden clears Stress", s.harden("nightmares"), true))
	rows.append(check("harden reset", s.stress, 0))
	rows.append(check("hardening grants one immunity per scene", s.hardening_count, 1))
	s.queue_event("atrocity_witness")
	s.end_scene(3, 15, 20)
	rows.append(check("hardening prevents one Stress", s.stress, 0))
	rows.append(check("nightmares affects saves", s.effects(2).get("save_penalty"), -2))
	var snap := s.snapshot()
	var recovered := Stress.new()
	recovered.restore(snap)
	rows.append(check("snapshot persists scars", recovered.scars, ["nightmares"]))
	var b := Stress.new(true)
	b.queue_event("kill")
	b.end_scene(1, 15, 1)
	rows.append(check("breakdown choice", b.choose_breakdown("withdrawal"), true))
	b.queue_event("kill")
	b.end_scene(1, 15, 1)
	rows.append(check("breakdown stops further stress", b.stress, 2))
	b.recover(1, 1)
	rows.append(check("breakdown ends at Wisdom", b.breakdown, ""))
	var strain := {"max": 10, "used": 0.0}
	rows.append(check("indulgence costs strain", b.indulgence(1, strain), true))
	rows.append(check("indulgence modifies strain", strain["used"], 1.0))
	rows.append(check("module defaults disabled", Stress.new().enabled, false))
	return rows
