extends "res://tests/godot/godot_test.gd"

## SWN psionics in the engine: the Effort pool, Torching, and the package gate (#751).
##
## Mechanics only. Stars Without Number Revised has no verified SRD licence, so no power name or
## description appears here — the technique catalogue is NoöPunk-authored (`data/rules/
## psionics_techniques.json`, `is_canonical: false`).

const Effort := preload("res://godot/core/psychic_effort.gd")
const Psionics := preload("res://godot/core/psionics.gd")

func _psychic(wis: int, con: int, ranks: Dictionary) -> Object:
	return Effort.new(wis, con, ranks)

func test_effort_is_one_plus_the_best_modifier_plus_the_highest_skill() -> void:
	var p: Object = _psychic(9, 18, {"Telepathy": 1, "Precognition": 0})
	check_eq(p.capacity(), 4, "1 + CON +2 + highest psionic skill 1")
	var plain: Object = _psychic(10, 11, {"Telepathy": 0})
	check_eq(plain.capacity(), 1, "a qualified psychic always has at least one Effort")

func test_commitment_holds_effort_and_returns_it_on_schedule() -> void:
	var p: Object = _psychic(14, 10, {"Telepathy": 1})
	check_eq(p.commit("contact", "Telepathy", 0, "active"), true, "an active commitment")
	check_eq(p.commit("insight", "Telepathy", 0, "scene"), true, "a scene commitment")
	check_eq(p.commit("vision", "Telepathy", 0, "day"), true, "a day commitment")
	check_eq(p.available_effort(), 0, "all three points are committed")
	check_eq(p.release("vision"), false, "scene and day Effort cannot be refunded early")
	check_eq(p.release("contact"), true, "active Effort can")
	p.end_scene()
	check_eq(p.available_effort(), 2, "the scene point returns; only the day point stays committed")
	p.rest()
	check_eq(p.available_effort(), p.capacity(), "a night's rest returns everything")

func test_torching_buys_a_point_over_the_maximum_for_the_scene() -> void:
	var p: Object = _psychic(12, 12, {"Telepathy": 2})
	var base: int = p.capacity()
	var result: Dictionary = p.torch(6, 1)
	check_eq(result["ok"], true, "a six burns nothing")
	check_eq(result["status"], "ok", "and the psychic is unharmed")
	check_eq(p.capacity(), base + 1, "but the Effort was still granted, over the maximum")
	p.end_scene()
	check_eq(p.capacity(), base, "and it lasts only for that scene")

func test_a_burn_costs_the_attribute_the_table_names() -> void:
	var p: Object = _psychic(12, 14, {"Telepathy": 1})
	var burned: Dictionary = p.torch(3, 1)
	check_eq(burned["effect"], "constitution", "3-4 costs Constitution")
	check_eq(p.constitution, 13, "one point of it")
	check_eq(burned["status"], "ok", "with the pool intact")
	var q: Object = _psychic(12, 12, {"Telepathy": 1})
	check_eq(q.torch(5, 1)["ok"], false, "a choice result with no attribute named is refused")
	var named: Dictionary = q.torch(5, 1, "DEX")
	check_eq(named["attribute_lost"], "DEX", "and honoured when it is named")
	check_eq(named["sheet_must_apply"], "DEX", "the sheet applies attributes this pool does not hold")

func test_torching_is_once_per_round() -> void:
	var p: Object = _psychic(12, 12, {"Telepathy": 1})
	check_eq(p.torch(6, 4)["ok"], true, "the first torch in a round")
	check_eq(p.torch(6, 4)["reason"], "already_torched_this_round", "the second is refused")
	check_eq(p.torch(6, 5)["ok"], true, "a new round is a new torch")

func test_below_the_attribute_floor_the_character_is_lost() -> void:
	var p: Object = _psychic(4, 12, {"Telepathy": 1})
	check_eq(p.torch(1, 1)["status"], "ok", "Wisdom 4 survives one burn")
	check_eq(p.torch(2, 2)["status"], "feral", "Wisdom 2 is a feral psychic")
	check_eq(p.capacity(), 0, "and there is no usable pool left")
	var q: Object = _psychic(12, 3, {"Telepathy": 1})
	check_eq(q.torch(4, 1)["status"], "dead", "Constitution below 3 is death")

func test_an_unrestricted_psychic_may_raise_any_discipline() -> void:
	var p: Object = _psychic(12, 12, {"Telepathy": 1})
	for discipline in Effort.DISCIPLINES:
		check_eq(p.can_learn(discipline), true, "the Psychic package may study %s" % discipline)
	check_eq(p.can_learn("NotADiscipline"), false, "but only the six that exist")

func test_a_partial_psychic_may_master_one_discipline_only() -> void:
	var p: Object = Psionics.new(12, 12, {"Telepathy": 1}, ["swn_partial_psychic"])
	check_eq(p.authorized(), true, "the package authorizes psionics at all")
	check_eq(p.commit("contact", "Telepathy", 0, "scene"), true, "its own discipline is open")
	check_eq(p.commit("hunch", "Precognition", 0, "scene"), false,
		"another discipline is closed to a restricted psychic")

func test_an_unauthorized_character_spends_nothing() -> void:
	var p: Object = Psionics.new(12, 12, {"Telepathy": 1}, [])
	check_eq(p.authorized(), false, "no psychic package, no authorization")
	check_eq(p.commit("contact", "Telepathy", 0, "scene"), false, "and the commitment is refused")
	check_eq(p.available_effort(), p.capacity(), "with the pool untouched")

func test_the_pool_and_its_torch_survive_a_save() -> void:
	var p: Object = Psionics.new(12, 12, {"Telepathy": 1}, ["swn_psychic"])
	p.commit("contact", "Telepathy", 0, "day")
	p.torch(6, 1)
	var saved: Dictionary = p.snapshot()
	var restored: Object = Psionics.new(10, 10, {}, [])
	check_eq(restored.restore(saved), true, "the snapshot loads")
	check_eq(restored.capacity(), p.capacity(), "with the torched point intact")
	check_eq(restored.available_effort(), p.available_effort(), "and its commitments")
