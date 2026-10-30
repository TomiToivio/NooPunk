extends "res://tests/godot/godot_test.gd"

## SWN psychic advancement in the engine (#753): disciplines, picks, the free core technique.
##
## Mechanics only — the technique identifiers here are NoöPunk placeholders, because SWN's power
## catalogue is not reproduced (no verified SRD licence).

const Training := preload("res://godot/core/swn_progression.gd")

func test_a_full_psychic_may_train_several_disciplines() -> void:
	var p: Object = Training.new("swn_psychic")
	check_eq(p.learn_discipline("Telepathy"), true, "the first discipline")
	check_eq(p.learn_discipline("Precognition"), true, "and a second, unrestricted")
	check_eq(p.validate(), "", "a legal sheet")
	check_eq(p.learn_discipline("Telepathy"), false, "re-learning a discipline is not a training")

func test_a_partial_psychic_is_restricted_to_one_discipline() -> void:
	var p: Object = Training.new("swn_partial_psychic")
	check_eq(p.learn_discipline("Telepathy"), true, "its one discipline")
	check_eq(p.learn_discipline("Teleportation"), false, "and no second")
	var two: Object = Training.new("swn_partial_psychic", {"Telepathy": 0, "Teleportation": 0})
	check_eq(two.validate(), "too_many_disciplines_for_a_partial_psychic", "nor on load")

func test_an_unknown_package_has_no_disciplines_at_all() -> void:
	var p: Object = Training.new("warrior")
	check_eq(p.validate(), "a_psychic_package_is_required", "a psychic package is required")

func test_the_core_technique_is_free_and_spends_no_pick() -> void:
	var p: Object = Training.new("swn_psychic", {"Precognition": 0})
	check_eq(p.core_available("Precognition"), true, "rank 0 grants the core technique")
	check_eq(p.core_available("Telepathy"), false, "an untrained discipline grants nothing")
	check_eq(p.pending_pick, "", "and it opens no pick")
	check_eq(p.learn_technique("noo_hunch", "Precognition", 0), false,
		"so a rank-0 technique still needs an improvement to be chosen")

func test_one_improvement_buys_exactly_one_technique() -> void:
	var p: Object = Training.new("swn_psychic", {"Telepathy": 0})
	check_eq(p.learn_technique("noo_sense", "Telepathy", 0), false, "nothing improved yet")
	var step: Dictionary = p.advance("Telepathy")
	check_eq(step["ok"], true, "the first improvement")
	check_eq(p.pending_pick, "Telepathy", "opens the discipline's pick")
	check_eq(p.learn_technique("noo_sense", "Telepathy", 1), true, "which the technique spends")
	check_eq(p.pending_pick, "", "leaving none open")
	check_eq(p.learn_technique("noo_second", "Telepathy", 1), false, "a second pick needs an improvement")

func test_a_pick_cannot_be_banked_across_an_improvement() -> void:
	var p: Object = Training.new("swn_psychic", {"Telepathy": 0})
	p.advance("Telepathy")
	var blocked: Dictionary = p.advance("Telepathy")
	check_eq(blocked["ok"], false, "the open pick blocks the next improvement")
	check_eq(blocked["reason"], "spend_the_open_pick_first", "and says which discipline is waiting")

func test_a_technique_never_exceeds_the_trained_rank() -> void:
	var p: Object = Training.new("swn_psychic", {"Biopsionics": 0})
	p.advance("Biopsionics")
	check_eq(p.learn_technique("noo_heal", "Biopsionics", 2), false, "rank 2 is not taught yet")
	check_eq(p.learn_technique("noo_mend", "Biopsionics", 1), true, "rank 1 is")
	p.advance("Biopsionics")
	check_eq(p.learn_technique("noo_heal", "Biopsionics", 2), true, "and rank 2 after the next improvement")
	check_eq(p.technique_access("noo_heal"), true, "the technique is now usable")

func test_rank_four_is_the_ceiling() -> void:
	var p: Object = Training.new("swn_psychic", {"Telepathy": 4})
	check_eq(p.advance("Telepathy")["reason"], "discipline_already_at_rank_four", "rank four is the top")

func test_training_survives_a_save() -> void:
	var p: Object = Training.new("swn_psychic", {"Telepathy": 1}, {"noo_sense": ["Telepathy", 1]})
	var restored: Object = Training.new("swn_psychic")
	check_eq(restored.restore(p.snapshot()), true, "the snapshot loads")
	check_eq(restored.snapshot(), p.snapshot(), "with disciplines and techniques intact")

func test_an_invalid_save_is_refused_rather_than_believed() -> void:
	var bad: Object = Training.new("swn_partial_psychic", {"Telepathy": 0, "Teleportation": 0})
	check_eq(bad.restore({"package": "swn_partial_psychic", "skills": {"Telepathy": 0, "Teleportation": 0}}),
		false, "a restricted psychic with two disciplines is refused")
	var rank: Object = Training.new("swn_psychic")
	check_eq(rank.restore({"package": "swn_psychic", "skills": {"Telepathy": 9}}), false,
		"and so is an impossible rank")
	check_eq(rank.restore({"package": "swn_psychic", "skills": {}, "techniques": {"bad": ["Telepathy", 0]}}),
		false, "an unqualified technique is refused too")
