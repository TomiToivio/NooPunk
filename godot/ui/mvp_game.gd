## Playable MVP slice for #749 — Romppainen's home → UNSA HQ → one test mission.
##
## This file is *presentation and input only*. Every rule lives in `godot/core/session.gd` and the
## kernels behind it; nothing here rolls dice, mutates HP or decides legality. That split is what
## keeps the Godot layer from inventing a second rule set.
##
## Art is drawn procedurally (rectangles and a small palette) so no third-party asset enters the
## repository: the slice's look is original by construction.
extends Control

const SESSION_PATH := "user://mvp_romppainen.json"

const COLOUR_BG := Color("12141c")
const COLOUR_GRID := Color("242938")
const COLOUR_FLOOR := Color("2f3a4f")
const COLOUR_PC := Color("7fd1ff")
const COLOUR_NPC := Color("ffd479")
const COLOUR_ENEMY := Color("ff7a7a")
const COLOUR_TERMINAL := Color("9cff9c")
const COLOUR_TEXT := Color("d7dbe6")
const COLOUR_DIM := Color("8892a6")

const TILE := 28
const GRID_W := 12
const GRID_H := 8

var session: NoopunkSession
var player := Vector2i(2, 4)
var hacking_open := false
var selected_node := 0
var selected_verb := 0
var encounter_open := false
var status := ""

var _status_label: Label
var _info_label: Label

func _ready() -> void:
	session = NoopunkSession.new(RulesAdapter.new("res://data/rules/wn_core.json", int(Time.get_unix_time_from_system()) % 100000))
	_build_labels()
	set_process_input(true)
	_update_labels()

func _build_labels() -> void:
	_status_label = Label.new()
	_status_label.position = Vector2(GRID_W * TILE + 24, 16)
	_status_label.size = Vector2(420, 460)
	_status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_status_label.modulate = COLOUR_TEXT
	add_child(_status_label)

	_info_label = Label.new()
	_info_label.position = Vector2(16, GRID_H * TILE + 20)
	_info_label.size = Vector2(GRID_W * TILE, 80)
	_info_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_info_label.modulate = COLOUR_DIM
	add_child(_info_label)

func _update_labels() -> void:
	var lines: Array = []
	var loc := session.flow.location
	lines.append("Location: %s" % loc.capitalize())
	lines.append("HP %d/%d   AC %d" % [session.hp, int(session.character.get("hp_max", 1)), int(session.character.get("ac", 10))])
	if session.hacking != null:
		lines.append("CPU %d   failures %d/4   alerts %d/2%s" % [int(session.hacking.deck["cpu"]), session.hacking.failures, session.hacking.alert_actions, "   ALARM" if session.hacking.alarm else ""])
	if hacking_open and session.hacking != null:
		lines.append_array(_network_lines())
	lines.append("Objectives: %s" % str(session.objectives_done()))
	if session.flow.resolved:
		lines.append("Debrief: %s, %s" % [session.flow.approach, session.flow.conclusion])
	lines.append("")
	lines.append("WASD move · E interact · H network · C fight · F5 save · F9 load")
	if not status.is_empty():
		lines.append("")
		lines.append(status)
	_status_label.text = "\n".join(lines)

func _announce(text: String) -> void:
	status = text
	_info_label.text = text
	_update_labels()

# -- input ---------------------------------------------------------------------------

func _input(event: InputEvent) -> void:
	if not (event is InputEventKey) or not event.pressed or event.echo:
		return
	if hacking_open and _network_input(event.keycode):
		queue_redraw()
		return
	match event.keycode:
		KEY_W, KEY_UP: _step(Vector2i(0, -1))
		KEY_S, KEY_DOWN: _step(Vector2i(0, 1))
		KEY_A, KEY_LEFT: _step(Vector2i(-1, 0))
		KEY_D, KEY_RIGHT: _step(Vector2i(1, 0))
		KEY_E: _interact()
		KEY_H: _toggle_network()
		KEY_C: _toggle_fight()
		KEY_F5: _save()
		KEY_F9: _load()
	queue_redraw()

func _step(delta: Vector2i) -> void:
	var target := player + delta
	if target.x < 0 or target.y < 0 or target.x >= GRID_W or target.y >= GRID_H:
		return
	player = target

# -- interactions ---------------------------------------------------------------------

func _on_exit_tile() -> bool:
	return player.x >= GRID_W - 2 and player.y >= GRID_H - 2

func _interact() -> void:
	# The network view is modal: E closes it, so a player is never stuck with a panel open and no
	# obvious way back to the room.
	if hacking_open:
		hacking_open = false
		_announce("Network view closed.")
		return
	if encounter_open:
		return
	match session.flow.location:
		"home":
			if _on_exit_tile():
				session.travel("hq")
				player = Vector2i(1, 4)
				_announce("UNSA HQ. Find the captain for a briefing.")
			else:
				_announce("Romppainen's desk: case journal, sidearm, cyberdeck. Nothing yet that cannot wait.")
		"hq":
			session.brief()
			session.travel("mission")
			player = Vector2i(1, 4)
			_announce("The Kallas warehouse. A guard watches the loading bay; a terminal stands behind him.")
		"mission":
			if _on_exit_tile():
				var path := "investigative" if session.flow.achieved("manifest") else "mixed"
				var verdict := session.resolve(path, "success")
				if bool(verdict["ok"]):
					session.travel("debrief")
					_announce("Debrief at HQ: the manifest is on the captain's desk.")
				else:
					_announce("Not yet: %s" % String(verdict.get("reason", "")))
			elif player.x <= 3 and player.y <= 3:
				session.hack_connect("shipping")
				hacking_open = true
				_announce("Cyberdeck open. The shipping node is reachable.")
			else:
				_announce("The guard blocks the bay. Talk, sneak, or fight — the manifest is behind him.")

func _toggle_network() -> void:
	if session.flow.location != "mission":
		_announce("No network worth entering here.")
		return
	hacking_open = not hacking_open
	if hacking_open:
		selected_node = 0
		selected_verb = 0
	if hacking_open and session.hacking == null:
		session.open_network()
	_announce("Network view open." if hacking_open else "Network view closed.")

func _toggle_fight() -> void:
	if session.flow.location != "mission":
		_announce("Nothing to fight here.")
		return
	if encounter_open:
		session.combat_end_turn()
		return
	if session.start_encounter():
		encounter_open = true
		_announce("The guard moves. Your turn: C attacks, C again ends the turn.")

# -- save / load ------------------------------------------------------------------------

func _save() -> void:
	var err := session.save_to(SESSION_PATH)
	_announce("Saved." if err == OK else "Save failed (%d)." % err)

func _load() -> void:
	var err := session.load_from(SESSION_PATH)
	_announce("Loaded." if err == OK else "Load failed (%d)." % err)

# -- drawing ------------------------------------------------------------------------------

func _draw() -> void:
	var rect := Rect2(Vector2.ZERO, Vector2(GRID_W * TILE, GRID_H * TILE))
	draw_rect(rect, COLOUR_BG)
	for x in range(GRID_W):
		for y in range(GRID_H):
			var cell := Rect2(Vector2(x * TILE + 1, y * TILE + 1), Vector2(TILE - 2, TILE - 2))
			draw_rect(cell, COLOUR_FLOOR if (x + y) % 2 == 0 else COLOUR_GRID)
	# exit tile
	draw_rect(Rect2(Vector2((GRID_W - 2) * TILE, (GRID_H - 2) * TILE), Vector2(TILE * 2, TILE * 2)), Color(COLOUR_TERMINAL, 0.18))
	# terminal on the mission map
	if session.flow.location == "mission":
		draw_rect(Rect2(Vector2(4 * TILE + 4, 4 * TILE + 4), Vector2(TILE - 8, TILE - 8)), COLOUR_TERMINAL)
	# player
	draw_rect(Rect2(Vector2(player.x * TILE + 6, player.y * TILE + 6), Vector2(TILE - 12, TILE - 12)), COLOUR_PC)
	# enemies
	if session.combat != null:
		for id in session.combat.actors.keys():
			var a: Dictionary = session.combat.actors[id]
			if String(a["side"]) != "enemy" or not bool(a["alive"]):
				continue
			var pos: Vector2i = a["pos"]
			draw_rect(Rect2(Vector2(pos.x * TILE + 6, pos.y * TILE + 6), Vector2(TILE - 12, TILE - 12)), COLOUR_ENEMY)
	# network graph
	if hacking_open and session.hacking != null:
		_draw_network()

func _draw_network() -> void:
	var origin := Vector2(GRID_W * TILE + 24, 380)
	var spacing := 90.0
	var i := 0
	for node_id in session.hacking.nodes.keys():
		var pos := origin + Vector2(spacing * i, 0)
		for link in session.hacking.nodes[node_id].get("links", []):
			var j := session.hacking.nodes.keys().find(String(link))
			if j > i:
				draw_line(pos + Vector2(10, 10), origin + Vector2(spacing * j + 10, 10), COLOUR_DIM, 1.0)
		var colour := COLOUR_TERMINAL if session.hacking.is_node_connected(String(node_id)) else COLOUR_DIM
		draw_rect(Rect2(pos, Vector2(20, 20)), colour)
		i += 1


# Network controls use the session's rules API. Selection alone never spends resources.
func _node_ids() -> Array:
	if session.hacking == null:
		return []
	var ids := session.hacking.nodes.keys()
	ids.sort()
	return ids

func _selected_node_id() -> String:
	var ids := _node_ids()
	if ids.is_empty():
		return ""
	return String(ids[clampi(selected_node, 0, ids.size() - 1)])

func _node_verbs() -> Array:
	var id := _selected_node_id()
	if id.is_empty():
		return []
	return Array(session.hacking.nodes[id].get("verbs", []))

func _network_lines() -> Array:
	var lines: Array = ["", "NETWORK  J/K: node  U/I: verb  ENTER: connect  SPACE: run"]
	var ids := _node_ids()
	for i in range(ids.size()):
		var id := String(ids[i])
		var connected := session.hacking.is_node_connected(id)
		var marker := ">" if i == selected_node else " "
		lines.append("%s %s %s  [%s]" % [marker, id, "ONLINE" if connected else "LOCKED",
			", ".join(session.hacking.nodes[id].get("links", []))])
	var selected := _selected_node_id()
	if not selected.is_empty():
		var node: Dictionary = session.hacking.nodes[selected]
		lines.append("Selected: %s  Security %s  Access required %s" % [
			selected, str(node.get("security", "?")), str(node.get("access_required", "?"))])
		var verbs := _node_verbs()
		for i in range(verbs.size()):
			var verb := String(verbs[i])
			var ready := session.hacking.can_act(selected, verb)
			lines.append("%s %s (%s)" % [
				">" if i == selected_verb else " ", verb,
				"ready" if ready else "unavailable"])
		lines.append("Access %d  CPU %d" % [int(session.hacking.deck["access"]),
			int(session.hacking.deck["cpu"])])
	return lines

func _network_input(key: Key) -> bool:
	if session.hacking == null:
		return false
	var ids := _node_ids()
	match key:
		KEY_J:
			selected_node = maxi(0, selected_node - 1)
			selected_verb = 0
		KEY_K:
			selected_node = mini(ids.size() - 1, selected_node + 1)
			selected_verb = 0
		KEY_U:
			selected_verb = maxi(0, selected_verb - 1)
		KEY_I:
			selected_verb = mini(_node_verbs().size() - 1, selected_verb + 1)
		KEY_ENTER, KEY_KP_ENTER:
			var result := session.hack_connect(_selected_node_id())
			_announce("Connect: %s" % ("connected" if result.get("ok", false) else str(result.get("reason", "failed"))))
		KEY_SPACE:
			var verbs := _node_verbs()
			if verbs.is_empty():
				_announce("This node offers no actions.")
			else:
				var result := session.hack_act(_selected_node_id(), String(verbs[clampi(selected_verb, 0, verbs.size() - 1)]))
				_announce("Program: %s" % ("success" if result.get("success", false) else str(result.get("reason", "check failed"))))
		_:
			return false
	_update_labels()
	return true
