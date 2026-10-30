extends RefCounted

## #869: the node-link hacking screen — SRD 4.1–4.5 driven headlessly.
##
## The run below is the same procedure a player performs with the mouse: jack in, gain Access node by
## node, run a Verb on a Subject, watch the alert clock. Every expectation is either a published number
## read from the contract or a legality the SRD states in words.

const NodeLink = preload("res://godot/core/cwn_node_link.gd")
const Rules = preload("res://godot/core/cwn_hacking.gd")

var _rows: Array = []
var _checks := 0


func _eq(label: String, got: Variant, want: Variant) -> void:
	_checks += 1
	if got != want:
		_rows.append([label, false, "got %s want %s" % [got, want]])


func _ok(label: String, condition: bool, note: String = "") -> void:
	_checks += 1
	if not condition:
		_rows.append([label, false, note])


func _network() -> Dictionary:
	return NodeLink.network([
		NodeLink.node("entrance", "Public Terminal", 7, "Camera", ["archive"]),
		NodeLink.node("archive", "Records Archive", 12, "Datafile", []),
	], "entrance")


func run() -> Array:
	_rows = []
	_checks = 0

	# --- the catalogue the screen offers is the verified one (24 Verbs, 12 Subjects) ---
	_eq("verbs in the catalogue", NodeLink.verbs().size(), 24)
	_eq("subjects in the catalogue", NodeLink.subjects().size(), 12)
	_ok("a Verb carries its Access cost", NodeLink.verbs()["Activate"].has("access_cost"))
	_ok("a Verb lists its target types", NodeLink.verbs()["Activate"].get("target_types", []).size() > 0)
	_ok("a Subject carries its type", NodeLink.subjects()["Camera"].has("subject_type"))

	# --- nothing is legal before jacking in ---
	var net := _network()
	_ok("cannot access before jacking in", NodeLink.attempt_access(net, [6, 6], 2, 2).has("error"))
	_ok("cannot run a Verb before jacking in", NodeLink.run_verb(net, "Activate", "Camera").has("error"))

	# --- jacking in sets the deck's Access pool from the published formula ---
	var expected_pool := int(Rules.access_pool(2, 2, 1))
	var jacked := NodeLink.jack_in(net, 2, 2, 1)
	_ok("jack in succeeds", bool(jacked.get("ok", false)))
	_eq("Access pool is INT mod + Program + deck bonus", int(net["access"]), expected_pool)
	_eq("alert starts at zero", int(net["alert"]), 0)
	_eq("you start on the entry node", String(net["current"]), "entrance")

	# --- an unreachable node cannot be attacked first ---
	_ok("a deep node is not reachable yet",
		NodeLink.attempt_access(net, [6, 6], 5, 4, "archive").has("error"))

	# --- a failed Access raises the alert instead of succeeding quietly ---
	var weak := _network()
	NodeLink.jack_in(weak, 0, 0, 0)
	var failed := NodeLink.attempt_access(weak, [1, 1], -1, 0, "entrance")
	_ok("a failed Access is reported", not bool(failed.get("success", true)))
	_eq("a failed Access raises the alert", int(weak["alert"]), 1)
	_ok("and the node stays unaccessed", not bool(weak["nodes"][0]["accessed"]))

	# --- a successful Access opens the node and its links ---
	var strong := _network()
	NodeLink.jack_in(strong, 4, 4, 2)
	var opened := NodeLink.attempt_access(strong, [6, 6], 4, 4, "entrance")
	_ok("a strong Access succeeds", bool(opened.get("success", false)), str(opened))
	_ok("the node is marked accessed", bool(strong["nodes"][0]["accessed"]))
	var deep_ok := NodeLink.attempt_access(strong, [6, 6], 4, 4, "archive")
	_ok("the linked node is now reachable", bool(deep_ok.get("success", false)), str(deep_ok))
	_ok("re-accessing an accessed node is refused",
		NodeLink.attempt_access(strong, [6, 6], 4, 4, "entrance").has("error"))

	# --- Verbs are gated by the Subject's type, not by the player's optimism ---
	var verb_gated := _network()
	NodeLink.jack_in(verb_gated, 4, 4, 2)
	NodeLink.attempt_access(verb_gated, [6, 6], 4, 4, "entrance")
	var wrong_subject := NodeLink.run_verb(verb_gated, "Activate", "Datafile", [6, 6], 4, 4)
	_ok("a Verb refuses a Subject it cannot target", wrong_subject.has("error"), str(wrong_subject))
	var right_subject := NodeLink.run_verb(verb_gated, "Activate", "Camera", [6, 6], 4, 4)
	_ok("the matching Subject is allowed", not right_subject.has("error"), str(right_subject))
	_ok("the run logs what happened", Array(verb_gated["log"]).size() >= 3)

	# --- a Verb whose cost exceeds the pool is refused, not silently discounted ---
	var broke := _network()
	NodeLink.jack_in(broke, 0, 0, 0)
	NodeLink.attempt_access(broke, [6, 6], 6, 4, "entrance")
	broke["access"] = 0
	var costly := NodeLink.run_verb(broke, "Activate", "Camera", [6, 6], 6, 4)
	_ok("no Access, no Verb", costly.has("error"), str(costly))

	# --- disconnecting ends the run and keeps the log for the screen ---
	var finished := NodeLink.disconnect_deck(strong)
	_ok("disconnect succeeds", bool(finished.get("ok", false)))
	_ok("the run is finished", bool(strong["finished"]))
	_ok("and no longer jacked in", not bool(strong["jacked_in"]))
	_ok("the log survives", Array(strong["log"]).size() > 0)

	# --- what the screen draws ---
	var drawn := NodeLink.visible_nodes(_network())
	_eq("every node is offered to the screen", drawn.size(), 2)
	_ok("the entry is reachable before any check", bool(drawn[0]["reachable"]))
	_ok("a linked node is not reachable yet", not bool(drawn[1]["reachable"]))

	# --- the screen itself builds, and its buttons reflect the state ---
	var scene: PackedScene = load("res://scenes/node_link.tscn")
	_ok("the node-link scene exists", scene != null)
	if scene != null:
		var screen: Node = scene.instantiate()
		Engine.get_main_loop().root.add_child(screen)
		screen.build()
		_ok("the screen starts disconnected", String(screen._status.text).contains("disconnected"))
		screen._on_jack_in()
		_ok("jacking in updates the screen", String(screen._status.text).contains("connected"))
		_ok("the network rows are drawn", screen._node_rows.get_child_count() == 4)
		screen.queue_free()

	return _rows


func checks() -> int:
	return _checks
