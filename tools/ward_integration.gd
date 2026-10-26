extends SceneTree

## Headless integration driver for the ward scene (issue #631).
##
## Boots the real scene, then exercises the same calls the input handler makes: walk to an
## NPC, start a dialogue, take a choice, examine the record (a real 1d10 check), and save.
## It proves the playable loop is wired, not merely that the scene constructs.

var ward: Node
var frame := 0
var problems: Array[String] = []

func _initialize() -> void:
	ward = load("res://scenes/lakkahaltia/ward.tscn").instantiate()
	root.add_child(ward)

func _find(kind: String, id: String) -> Dictionary:
	for item in ward.interactables:
		if item["kind"] == kind and item["id"] == id:
			return item
	return {}

func _process(_delta: float) -> bool:
	frame += 1
	if frame < 4:
		return false

	if ward.state == null:
		problems.append("case state was not created")
		return _finish()

	var doctor := _find("npc", "doctor")
	if doctor.is_empty():
		problems.append("doctor interactable missing")
		return _finish()

	ward.player.position = doctor["position"] + Vector3(0, 0, 0.9)
	ward._interact(doctor)
	if not ward.dialogue_active:
		problems.append("talking to the doctor did not open a dialogue")
	if ward.state.last_speaker.find("Kivi") < 0:
		problems.append("the doctor dialogue did not start at her node")
	ward._choose(0)
	if not ward.state.has_flag("met_doctor"):
		problems.append("taking a choice did not apply its effect")
	if ward.state.in_dialogue():
		ward.state.end_dialogue()
		ward._close_dialogue()
	if ward.dialogue_active:
		problems.append("the dialogue did not close")

	var record := _find("object", "record")
	if record.is_empty():
		problems.append("record interactable missing")
		return _finish()
	ward.player.position = record["position"] + Vector3(0, 0, 0.9)
	ward._interact(record)
	if not ward.state.has_clue("record-1601"):
		problems.append("examining the record did not produce its clue (pass or fail both grant it)")

	if not ward.state.save_to("user://ward_integration_save.json"):
		problems.append("the scene could not save")
	if not ward.state.available_endings().has("closed_by_evidence"):
		problems.append("the case cannot be closed after finding the record")

	return _finish()

func _finish() -> bool:
	if problems.is_empty():
		print("INTEGRATION_OK clues=%d flags=%d" % [ward.state.clues.size(), ward.state.flags.size()])
		quit(0)
	else:
		for problem in problems:
			print("  FAIL " + problem)
		print("INTEGRATION_FAILED %d problem(s)" % problems.size())
		quit(1)
	return true
