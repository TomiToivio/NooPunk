extends "res://tests/godot/godot_test.gd"

## SWN psionics in the engine: package gates, Effort, commitments, Torching, core techniques.
##
## There is exactly **one** psionics implementation in the engine — `godot/core/psionics.gd` on top of
## `psychic_effort.gd` — and this file is its behavioural suite. The parallel `src/godot/swn_psionics.gd`
## this suite used to cover was retired into it (#791): its two core-technique statics now live in the
## canonical kernel, so nothing it uniquely knew was lost.
##
## Mechanics only: SWN has no verified SRD licence, so no power name or description is reproduced.

const Psi := preload("res://godot/core/psionics.gd")
const Effort := preload("res://godot/core/psychic_effort.gd")
const Training := preload("res://godot/core/swn_progression.gd")

func _psychic(ranks: Dictionary = {"Biopsionics": 1, "Telepathy": 0}) -> Object:
	return Psi.new(12, 14, ranks, ["swn_psychic"])

func test_packages_gate_the_whole_system() -> void:
	var none: Object = Psi.new(12, 14, {"Telepathy": 1}, [])
	check_eq(none.authorized(), false, "no psychic package, no authorization")
	check_eq(none.commit("contact", "Telepathy", 0, "scene"), false, "and the commitment is refused")
	check_eq(none.available_effort(), none.capacity(), "with the pool untouched")

	var partial: Object = Psi.new(12, 14, {"Biopsionics": 0}, ["swn_partial_psychic"], "Biopsionics")
	check_eq(partial.authorized(), true, "a Partial Psychic is authorized")
	check_eq(partial.commit("heal", "Biopsionics", 0, "scene"), true, "in its one discipline")
	check_eq(partial.commit("read", "Telepathy", 0, "scene"), false, "and in no other")

func test_effort_is_one_plus_the_best_modifier_plus_the_highest_rank() -> void:
	var p: Object = _psychic({"Biopsionics": 1})
	check_eq(p.capacity(), 3, "1 + best(WIS +1, CON +1) + highest discipline 1")
	var bare: Object = Psi.new(10, 11, {"Telepathy": 0}, ["swn_psychic"])
	check_eq(bare.capacity(), 1, "a qualified psychic always has at least one")

func test_commitment_lifecycle_and_activation() -> void:
	var p: Object = _psychic()
	check_eq(p.activate("mending_touch", "one", "scene"), true, "activate a known core technique")
	check_eq(p.activate("mending_touch", "one", "scene"), false, "a commitment key is unique")
	check_eq(p.release_active("one"), false, "scene Effort cannot be released early")
	check_eq(p.available_effort(), 2, "one point committed")
	p.end_scene()
	check_eq(p.available_effort(), 3, "scene Effort returns at the scene's end")
	check_eq(p.activate("mending_touch", "two", "day"), true, "commit for the day")
	p.end_scene()
	check_eq(p.available_effort(), 2, "a day commitment survives the scene")
	p.rest()
	check_eq(p.available_effort(), 3, "and rest restores the pool")

func test_an_unknown_or_unauthorized_technique_spends_nothing() -> void:
	var p: Object = _psychic()
	check_eq(p.activate("not_a_technique", "x", "scene"), false, "an unknown id is refused")
	check_eq(p.available_effort(), p.capacity(), "and spends no Effort")
	var none: Object = Psi.new(12, 14, {"Telepathy": 1}, [])
	check_eq(none.activate("surface_read", "x", "scene"), false, "nor does it work unauthorized")

func test_torching_burns_attributes_and_buys_effort_for_the_scene() -> void:
	var p: Object = _psychic()
	var first: Dictionary = p.torch(1, 1)
	check_eq(first["attribute_lost"], "WIS", "a 1 costs Wisdom")
	check_eq(p.wisdom, 11, "one point of it")
	check_eq(p.torch(1, 1)["ok"], false, "and only once per round")
	check_eq(p.torch(6, 2)["effect"], "none", "a 6 is harmless")
	check_eq(p.torch(5, 3)["ok"], false, "a choice result needs an attribute")
	p.end_scene()
	check_eq(p.torch_bonus, 0, "the torched point expires with its scene")

func test_the_core_techniques_scale_with_the_discipline_rank() -> void:
	var heal: Dictionary = Psi.psychic_succor(1, [4], 6, 12, 0, 12, false)
	check_eq(heal["ok"], true, "rank 1 heals ordinary damage")
	check_eq(heal["hp"], 11, "1d6 + 1 on a roll of 4")
	check_eq(heal["strain"], 1, "adds one System Strain")
	check_eq(Psi.psychic_succor(0, [], 6, 12, 0, 12, false)["reason"], "stabilization_only",
		"rank 0 stabilizes and cannot heal ordinary wounds")
	check_eq(Psi.psychic_succor(0, [], 0, 12, 0, 12, true)["stabilized"], true, "but it does stabilize")
	check_eq(Psi.psychic_succor(1, [4], 6, 12, 12, 12, false)["reason"], "system_strain",
		"and Strain above Constitution refuses the power")
	check_eq(Psi.teleport_range_meters(0), 10.0, "rank zero teleports ten metres")
	check_eq(Psi.teleport_range_meters(3), 1000000.0, "rank three reaches far")

func test_one_home_for_the_disciplines() -> void:
	check_eq(Effort.DISCIPLINES, Training.new("swn_psychic").disciplines(),
		"the Effort kernel and the training kernel agree on the six disciplines")
