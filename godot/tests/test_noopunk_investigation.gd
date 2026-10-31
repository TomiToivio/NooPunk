## Investigation overlay (#897): the system reports evidence, the player decides what it means.
##
## Discovery has its own home (`godot/core/investigation_adapter.gd`, #718) and its own suite; nothing
## here re-tests it. These assertions cover the narrative half, and every one calls the overlay.
extends RefCounted

const Overlay := preload("res://mods/noopunk/investigation.gd")


func run() -> Array:
	var rows: Array = []
	var tags := {
		"signal_log": ["noosphere", "transmission"],
		"gossip": ["rumour"],
		"autopsy": ["mundane_explanation"],
	}
	var noetic := {"id": "signal_is_noetic", "supports": ["noosphere"],
		"contradicts": ["mundane_explanation"]}

	var reading := Overlay.interpret(noetic, tags, ["signal_log", "autopsy"])
	rows.append(["supporting clues are named", reading.get("supports", []) == ["signal_log"]])
	rows.append(["contradicting clues are named", reading.get("contradicts", []) == ["autopsy"]])
	rows.append(["the overlay never declares a verdict",
		String(reading.get("verdict", "")) == Overlay.VERDICT_OPEN])
	rows.append(["the overlay never sets confidence", reading.get("confidence", 0) == null])

	var unanimous := Overlay.interpret(noetic, tags, ["signal_log"])
	rows.append(["even unanimous evidence stays a reading, not a ruling",
		String(unanimous.get("verdict", "")) == Overlay.VERDICT_OPEN])
	rows.append(["unanimous evidence sets no confidence", unanimous.get("confidence", 0) == null])

	var unknown_clue := Overlay.interpret(noetic, tags, ["not_a_clue"])
	rows.append(["a clue it knows nothing about is ignored, not guessed",
		unknown_clue.get("supports", []) == [] and unknown_clue.get("contradicts", []) == []])

	var mundane := {"id": "it_was_drugs", "supports": ["mundane_explanation"],
		"contradicts": ["noosphere"]}
	var live := Overlay.open_hypotheses([noetic, mundane], tags, ["gossip"])
	rows.append(["both hypotheses survive evidence that touches neither",
		live == ["signal_is_noetic", "it_was_drugs"]])
	var narrowed := Overlay.open_hypotheses([mundane], tags, ["signal_log"])
	rows.append(["a contradicted hypothesis leaves the live set", narrowed == []])

	var off := Overlay.interpret(noetic, tags, ["signal_log"], false)
	rows.append(["the overlay can be switched off", off.get("overlay", true) == false])

	rows.append(["cost names are a closed vocabulary",
		Overlay.validate_cost("second_currency") == false])
	rows.append(["a CWN cost name is accepted", Overlay.validate_cost(Overlay.COSTS[0])])
	return rows
