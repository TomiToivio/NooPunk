## One vertical slice, composed: character → flow → hacking → optional combat → debrief (#749).
##
## The session is the only object a UI needs to talk to. It owns the four pieces and their
## persistence, so a scene can ask "can I travel?" or "can I act on this node?" without
## re-implementing a rule.
##
## It does not render anything and does not know about scenes: the Godot scenes read this state.
extends RefCounted
class_name NoopunkSession

const PLAYER_ID := "pc"
const DATA_DIR := "res://godot/scenarios/mvp_romppainen/"
const SAVE_VERSION := 1

var adapter: RulesAdapter
var flow: NoopunkSceneFlow
var character: Dictionary = {}
var mission: Dictionary = {}
var hacking: NoopunkHacking
var combat: NoopunkCombat = null
var hp: int = 0
## #806/#809: the active party (1..4). The PC is the protagonist; Romppainen is a companion.
var party: CwnParty = null
var member_hp: Dictionary = {}
var log: Array = []

func _init(rules_adapter: RulesAdapter, data_dir: String = DATA_DIR) -> void:
	adapter = rules_adapter
	flow = NoopunkSceneFlow.new()
	character = _load_json(data_dir + "character.json")
	mission = _load_json(data_dir + "mission.json")
	hp = int(character.get("hp_max", 1))
	log.append({"event": "new_session"})

func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("NoopunkSession: missing data at %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return parsed if typeof(parsed) == TYPE_DICTIONARY else {}

# -- travel and briefing -------------------------------------------------------------

func travel(to: String) -> Dictionary:
	var verdict := flow.travel(to)
	if bool(verdict["ok"]) and to == NoopunkSceneFlow.MISSION:
		_open_network()
	log.append({"event": "travel", "to": to, "ok": verdict["ok"]})
	return verdict

func brief() -> void:
	flow.complete_briefing()
	log.append({"event": "briefed"})

func open_network() -> void:
	_open_network()

func _open_network() -> void:
	if hacking != null:
		return
	hacking = NoopunkHacking.new(adapter, mission.get("network", {}), mission.get("deck", {}))
	log.append({"event": "network_open", "entry": String(mission.get("network", {}).get("entry", ""))})

# -- hacking -------------------------------------------------------------------------

func hack_connect(node_id: String) -> Dictionary:
	if hacking == null:
		return {"ok": false, "reason": "network_not_open"}
	var result := hacking.connect_node(node_id)
	log.append({"event": "hack_connect", "node": node_id, "ok": result.get("ok", false)})
	return result

func hack_act(node_id: String, verb: String) -> Dictionary:
	if hacking == null:
		return {"ok": false, "reason": "network_not_open"}
	var result := hacking.act(node_id, verb)
	if bool(result.get("success", false)) and verb == "query" and node_id == "manifest":
		flow.achieve("manifest")
	log.append({"event": "hack_act", "node": node_id, "verb": verb,
		"success": result.get("success", false)})
	return result

# -- optional combat ------------------------------------------------------------------

func start_encounter() -> bool:
	if combat != null:
		return false
	combat = NoopunkCombat.new(adapter)
	var spec: Dictionary = mission.get("encounter", {})
	for enemy in spec.get("actors", []):
		var pos: Array = enemy.get("pos", [0, 0])
		combat.add_actor({
			"id": String(enemy.get("id", "enemy")), "side": "enemy",
			"pos": Vector2i(int(pos[0]), int(pos[1])),
			"hp": int(enemy.get("hp", 5)), "ac": int(enemy.get("ac", 12)),
			"dex": int(enemy.get("dex", 10)),
			"combat_rank": int(enemy.get("combat_rank", 0)),
			"attack_bonus": int(enemy.get("attack_bonus", 0)),
			"damage": enemy.get("damage", [1, 6, 0]),
			"cover": int(enemy.get("cover", 0)),
			"weapon_kind": String(enemy.get("weapon_kind", "melee")),
			"ac_melee": int(enemy.get("ac_melee", enemy.get("ac", 12))),
			"ac_ranged": int(enemy.get("ac_ranged", enemy.get("ac", 12))),
			"trauma_rating": int(enemy.get("trauma_rating", 1)),
			"trauma_target": int(enemy.get("trauma_target", 6)),
			"shock_value": int(enemy.get("shock_value", 0)),
			"shock_ac": int(enemy.get("shock_ac", -1)),
			"lethal": bool(enemy.get("lethal", true)),
			"ammo": int(enemy.get("ammo", -1)),
		})
	var attack: Dictionary = character.get("attack", {})
	# #809: every party member is an actor. The PC is no longer Romppainen, and a solo party of one
	# must work exactly like a four-person squad - so this loops rather than naming a protagonist.
	var pc_ids: Array = []
	if party != null and party.size() > 0:
		for member in party.members:
			pc_ids.append(str(member.get("id", "")))
	else:
		# No party configured: the character record is the protagonist, whatever its id. This keeps
		# existing single-protagonist scenarios working without naming a specific person here.
		pc_ids.append(str(character.get("id", PLAYER_ID)))
	var slot := 0
	for actor_id in pc_ids:
		var member_hp_value := int(member_hp.get(actor_id, hp))
		member_hp[actor_id] = member_hp_value
		combat.add_actor({
		"id": actor_id, "side": "pc", "pos": Vector2i(1, 3 + slot),
		"hp": hp, "ac": int(character.get("ac", 10)),
		"dex": int(character.get("attributes", {}).get("DEX", 10)),
		"attack_attribute": int(character.get("attributes", {}).get(String(attack.get("attribute", "DEX")), 10)),
		"combat_rank": int(attack.get("combat_rank", 0)),
		"attack_bonus": int(attack.get("attack_bonus", 0)),
		"damage": attack.get("damage", [1, 6, 0]),
		"weapon_kind": String(attack.get("weapon_kind", "ranged")),
		"ac_melee": int(character.get("ac_melee", character.get("ac", 10))),
		"ac_ranged": int(character.get("ac_ranged", character.get("ac", 10))),
		"trauma_rating": int(attack.get("trauma_rating", 1)),
		"trauma_target": int(attack.get("trauma_target", 6)),
		"shock_value": int(attack.get("shock_value", 0)),
		"shock_ac": int(attack.get("shock_ac", -1)),
		"lethal": bool(attack.get("lethal", true)),
		"ammo": int(attack.get("ammo", -1)),
		"ammo_max": int(attack.get("ammo_max", attack.get("ammo", -1))),
		})
		slot += 1
	combat.start()
	log.append({"event": "encounter_start"})
	return true

func combat_attack(actor_id: String, target_id: String) -> Dictionary:
	if combat == null:
		return {"ok": false, "reason": "no_encounter"}
	var result := combat.attack(actor_id, target_id)
	if bool(result.get("hit", false)) and member_hp.has(target_id):
		member_hp[target_id] = max(0, int(member_hp[target_id]) - int(result.get("damage", 0)))
		# The controlled member's hit points stay mirrored on `hp` for callers written against the
		# single-protagonist slice; the roster is the source of truth.
		if party == null or target_id == party.controlled_id:
			hp = member_hp[target_id]
	log.append({"event": "combat_attack", "actor": actor_id, "target": target_id,
		"hit": result.get("hit", false)})
	return result

func combat_end_turn() -> void:
	if combat != null:
		combat.end_turn()

func encounter_over() -> bool:
	return combat != null and combat.is_over()

# -- resolution ----------------------------------------------------------------------

## Resolve the mission. A mission with no fight is a legitimate success, not a partial one.
func resolve(path: String, result: String) -> Dictionary:
	var verdict := flow.resolve(path, result)
	if bool(verdict["ok"]):
		flow.achieve("exit")
	log.append({"event": "resolve", "path": path, "result": result, "ok": verdict["ok"]})
	return verdict

func objectives_done() -> Array:
	return flow.objectives.keys()

# -- persistence ---------------------------------------------------------------------

func to_dict() -> Dictionary:
	var combat_state := {}
	if combat != null:
		var actors := {}
		for id in combat.actors.keys():
			var a: Dictionary = combat.actors[id]
			actors[id] = {"hp": int(a["hp"]), "alive": bool(a["alive"]),
				"pos": [int(a["pos"].x), int(a["pos"].y)]}
		combat_state = {"actors": actors, "round": combat.round_number,
			"turn": combat.turn, "over": combat.over, "outcome": combat.outcome()}
	var hack_state := {}
	if hacking != null:
		hack_state = {"connected": hacking.connected.duplicate(), "failures": hacking.failures, "alert_actions": hacking.alert_actions,
			"alarm": hacking.alarm, "cpu": int(hacking.deck["cpu"]),
			"verbs_done": hacking.verbs_done.duplicate()}
	return {
		"version": SAVE_VERSION,
		"flow": flow.to_dict(),
		"hp": hp,
		"hacking": hack_state,
		"combat": combat_state,
		"log": log.duplicate(true),
	}

func from_dict(data: Dictionary) -> bool:
	if int(data.get("version", 0)) != SAVE_VERSION:
		push_error("NoopunkSession: unsupported save version")
		return false
	var flow_data: Dictionary = data.get("flow", {})
	if not flow.from_dict(flow_data):
		return false
	hp = int(data.get("hp", character.get("hp_max", 1)))
	var hack_state: Dictionary = data.get("hacking", {})
	hacking = null
	if not hack_state.is_empty():
		_open_network()
		hacking.connected = Array(hack_state.get("connected", [])).duplicate()
		hacking.failures = int(hack_state.get("failures", 0))
		hacking.alert_actions = int(hack_state.get("alert_actions", 0))
		hacking.alarm = bool(hack_state.get("alarm", false))
		hacking.deck["cpu"] = int(hack_state.get("cpu", hacking.deck["cpu"]))
		hacking.verbs_done = Dictionary(hack_state.get("verbs_done", {})).duplicate()
	var combat_state: Dictionary = data.get("combat", {})
	combat = null
	if not combat_state.is_empty():
		start_encounter()
		for id in Dictionary(combat_state.get("actors", {})).keys():
			if combat.actors.has(id):
				var saved: Dictionary = combat_state["actors"][id]
				combat.actors[id]["hp"] = int(saved.get("hp", 1))
				combat.actors[id]["alive"] = bool(saved.get("alive", true))
				var pos: Array = saved.get("pos", [0, 0])
				combat.actors[id]["pos"] = Vector2i(int(pos[0]), int(pos[1]))
		combat.round_number = int(combat_state.get("round", 1))
		combat.turn = int(combat_state.get("turn", 0))
		combat.over = bool(combat_state.get("over", false))
	log = Array(data.get("log", [])).duplicate(true)
	return true

func save_to(path: String) -> Error:
	var handle := FileAccess.open(path, FileAccess.WRITE)
	if handle == null:
		return FileAccess.get_open_error()
	handle.store_string(JSON.stringify(to_dict(), "  "))
	handle.close()
	return OK

func load_from(path: String) -> Error:
	if not FileAccess.file_exists(path):
		return ERR_FILE_NOT_FOUND
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return ERR_FILE_CORRUPT
	return OK if from_dict(parsed) else ERR_INVALID_DATA
