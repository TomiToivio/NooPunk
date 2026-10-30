## Dialogue behaviour: choices apply their effects, checks branch on the roll, and the safeguarding-first
## path never has to pass a check to be worth taking.
extends RefCounted

const GameStateScript := preload("res://godot/core/game_state.gd")
const RunnerScript := preload("res://godot/narrative/dialogue.gd")

func run() -> Array:
	var rows: Array = []
	var state = _state()
	state.new_case(31)
	var runner = RunnerScript.new(state.dialogue_nodes, state)

	var opening: Dictionary = runner.start("doctor_1")
	rows.append(_eq("doctor opens", String(opening.get("speaker", "")), "Dr. Laine"))
	rows.append(_eq("doctor offers four entry choices", runner.choices().size(), 4))

	# The consent path: a flag, no dice, and the conversation closes.
	var closing: Dictionary = runner.choose(3)
	rows.append(_eq("safeguarding flag set", state.has_flag("safeguarding_first"), true))
	rows.append(_eq("the consent line closes on its own node", String(closing.get("id", "")), "doctor_end"))
	rows.append(_eq("that node offers no further choices", runner.choices().size(), 0))

	# The check path is deterministic for a fixed seed, and success records evidence.
	var seeded = _state()
	seeded.new_case(31)
	var seeded_runner = RunnerScript.new(seeded.dialogue_nodes, seeded)
	seeded_runner.start("doctor_1")
	var after: Dictionary = seeded_runner.choose(0)
	var result: Dictionary = seeded_runner.last_result
	rows.append(_eq("check published", result.is_empty(), false))
	rows.append(_eq("the branch matches the roll",
		String(after.get("id", "")), "doctor_record" if bool(result["success"]) else "doctor_deflect"))
	if bool(result["success"]):
		rows.append(_eq("success added E1", seeded.has_evidence("E1"), true))

	# The patient will not talk about the place until the account has been taken down.
	var patient = _state()
	patient.new_case(31)
	var patient_runner = RunnerScript.new(patient.dialogue_nodes, patient)
	patient_runner.start("patient_1")
	patient_runner.choose(0) # consent
	var body: Dictionary = patient_runner.choose(2) # "is the place somewhere you have been"
	rows.append(_eq("the drawing is recorded", patient.has_evidence("E2"), true))
	rows.append(_eq("the place node follows", String(body.get("id", "")), "patient_place"))

	# A choice index that does not exist is a no-op rather than a crash.
	rows.append(_eq("out-of-range choice is empty", runner.choose(99).is_empty(), true))


	# The psionic path (#652): the package-and-rank gate runs *before* the dice, so an unauthorized
	# character takes the failure branch without a roll and without spending Effort.
	var psychic = _state()
	psychic.new_case(31)
	var psychic_runner = RunnerScript.new(psychic.dialogue_nodes, psychic)
	psychic_runner.start("patient_1")
	psychic_runner.choose(0) # consent
	var psi_node: Dictionary = psychic_runner.choose(1) # Surface Read
	rows.append(_eq("Effort maximum comes from the sheet", psychic.effort_maximum(), 3))
	rows.append(_eq("an authorized technique is recorded",
		psychic.journal.any(func(line): return String(line).begins_with("Psionic technique used")), true))
	rows.append(_eq("a trained reading reaches the psi node or the plain one",
		["patient_psi", "patient_plain"].has(String(psi_node.get("id", ""))), true))

	var unauthorized = _state()
	unauthorized.new_case(31)
	unauthorized.psionics = NoopunkPsionics.new(10, 10, {}, [])
	var unauthorized_runner = RunnerScript.new(unauthorized.dialogue_nodes, unauthorized)
	unauthorized_runner.start("patient_1")
	unauthorized_runner.choose(0)
	var refused: Dictionary = unauthorized_runner.choose(1)
	rows.append(_eq("an unauthorized technique takes the failure branch",
		String(refused.get("id", "")), "patient_plain"))
	rows.append(_eq("and the journal says why",
		unauthorized.journal.any(func(line): return String(line).contains("not available")), true))

	_free_owned()
	return rows

# GameState extends Node, so every instance must be freed by hand or the headless run exits with
# leaked ObjectDB instances (#883). Track them here and release them before `run()` returns.
var _owned: Array[Node] = []


func _state() -> Node:
	var instance: Node = GameStateScript.new()
	_owned.append(instance)
	return instance


func _free_owned() -> void:
	for instance in _owned:
		if is_instance_valid(instance):
			instance.free()
	_owned.clear()


func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]
