## The node-link screen: does a player actually reach the hacking rules?
##
## The kernel has its own tests; these rows prove the *screen* wires them up — that a node press spends
## CPU and Access, that an unreachable node is refused with the kernel's reason, and that the alert clock
## reaches the presentation rather than staying inside the kernel.
extends RefCounted

const Screen := preload("res://godot/ui/hacking_screen.gd")
const Rules := preload("res://godot/core/cwn_hacking.gd")


class StubAdapter:
	var face := 4
	func attribute_modifier(score: int) -> int:
		return (score - 10) / 2
	func roll_die(sides: int) -> int:
		return face


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _network() -> Dictionary:
	return {
		"entry": "entry",
		"nodes": {
			"entry": {"links": ["records"], "verbs": [], "pos": [0, 0]},
			"records": {"links": ["entry", "vault"], "verbs": ["query"], "security": 7, "pos": [1, 0]},
			"vault": {"links": ["records"], "verbs": ["control"], "security": 9, "access_required": 2, "pos": [2, 0]},
			"isolated": {"links": [], "verbs": [], "pos": [3, 0]},
		},
	}


func _deck() -> Dictionary:
	return {"cpu": 6, "access": 3, "programs": ["query", "control"], "program_rank": 1, "int": 12}


func _screen() -> Object:
	var screen: Object = Screen.new()
	screen.setup(StubAdapter.new(), _network(), _deck())
	return screen


func run() -> Array:
	var rows: Array = []
	var screen := _screen()
	var kernel: Object = screen.kernel

	rows.append(_eq("every network node gets a button", screen._buttons.size(), 4))
	rows.append(_eq("the entry node starts connected", kernel.is_node_connected("entry"), true))
	rows.append(_eq("a node with no path is not connected", kernel.is_node_connected("vault"), false))
	rows.append(_eq("links are drawn for the network", screen._nodes_layer.get_child_count() > 4, true))

	# Pressing a reachable node connects it and spends a CPU point.
	var cpu_before := int(kernel.deck["cpu"])
	screen._buttons["records"].emit_signal("pressed")
	rows.append(_eq("pressing a reachable node connects it", kernel.is_node_connected("records"), true))
	rows.append(_eq("connecting spends CPU", int(kernel.deck["cpu"]) < cpu_before, true))
	rows.append(_eq("the node shows as connected", screen._buttons["records"].modulate.g > 0.9, true))

	# Pressing an unreachable node is refused, and the kernel's own reason is surfaced.
	screen._buttons["isolated"].emit_signal("pressed")
	rows.append(_eq("an unreachable node stays disconnected", kernel.is_node_connected("isolated"), false))
	rows.append(_eq("the refusal reaches the log", screen._log_label.get_parsed_text().contains("no_path"), true))

	# A verb button exists for a connected node's verbs, and running it reaches the kernel.
	screen._on_node_pressed("records")
	rows.append(_eq("verbs are offered once connected", screen._verbs_panel.get_child_count() >= 1, true))
	var access_before := int(kernel.deck["access"])
	screen._on_verb_pressed("records", "query")
	rows.append(_eq("a verb spends Access", int(kernel.deck["access"]) < access_before, true))
	rows.append(_eq("the verb is recorded in the kernel log", kernel.log.size() >= 2, true))

	# A verb the deck does not carry is refused with the kernel's reason.
	var no_program := _screen()
	no_program.kernel.deck["programs"] = []
	no_program._on_node_pressed("records")
	no_program._on_verb_pressed("records", "query")
	rows.append(_eq("a missing program is refused", no_program._log_label.get_parsed_text().contains("no_program"), true))

	# The alert clock reaches the presentation.
	kernel.failures = 3
	kernel.alert_actions = 1
	screen._refresh()
	rows.append(_eq("the alert clock is shown", screen._status.text.contains("alert 1/2"), true))
	kernel.alarm = true
	screen._refresh()
	rows.append(_eq("an alarm is shown", screen._status.text.contains("ALARM"), true))
	rows.append(_eq("an alarm disables the nodes", screen._buttons["records"].disabled, true))

	# The screen must be reachable from the menu path, not only from a test fixture.
	var from_mission: Object = Screen.new()
	rows.append(_eq("the warehouse mission opens on the screen",
		from_mission.open_mission("res://godot/scenarios/mvp_romppainen/mission.json", 7), true))
	rows.append(_eq("the mission's nodes are drawn", from_mission._buttons.size() >= 2, true))
	rows.append(_eq("the mission entry point is connected",
		from_mission.kernel.is_node_connected("lobby"), true))
	rows.append(_eq("a missing mission file is refused",
		from_mission.open_mission("res://godot/scenarios/nope/mission.json"), false))

	# Teardown: both screens are Controls that never enter the tree, and a Control owns Labels, buttons
	# and rich-text buffers. Without this the headless run exits with ~140 leaked ObjectDB instances and
	# leaked CanvasItem/text RIDs (#883).
	screen.free()
	no_program.free()
	from_mission.free()
	return rows
