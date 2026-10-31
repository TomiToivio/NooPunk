## Narrative-mode session for the Helsinki case (#897).
##
## The rules are vanilla CWN: skill checks are the kernel's 2d6 check and violence is its d20 attack.
## This class only sequences location travel, discovery, clues, party and the case's narrative state.
class_name NoopunkHelsinkiSession
extends RefCounted

const DATA := "res://godot/narrative/helsinki_case.json"
const PARTY_CAP := 4
const PC := {"id": "pc", "name": "You", "role": "UNSA Academy graduate"}

var data: Dictionary = {}
var current := ""
var discovered: Array = []
var clues: Array = []
var party: Array = []
var flags: Dictionary = {}
var log_lines: Array = []
var credits := 3
var stress := 0
var player_hp := 10
var threat_hp := 12
var adapter: Object = null


func _init(path: String = DATA, rules_adapter: Object = null) -> void:
	data = _load(path)
	adapter = rules_adapter
	current = String(data.get("start", "home"))
	discovered = []
	for entry in locations():
		if bool(entry.get("discovered", false)):
			discovered.append(String(entry.get("id", "")))
	if not discovered.has(current):
		discovered.append(current)
	party = [PC.duplicate()]
	flags = {}
	_log("A new agent, a cold flat, and a signal that should not exist.")


func _load(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("helsinki: cannot open %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func locations() -> Array:
	return data.get("locations", [])


func location(id: String) -> Dictionary:
	for entry in locations():
		if String(entry.get("id", "")) == id:
			return entry
	return {}


func current_location() -> Dictionary:
	return location(current)


func is_discovered(id: String) -> bool:
	return discovered.has(id)


func discover(id: String) -> void:
	if not is_discovered(id) and not location(id).is_empty():
		discovered.append(id)
		_log("New location: %s" % location(id).get("name", id))


func travel(id: String) -> Dictionary:
	if location(id).is_empty():
		return {"ok": false, "reason": "no such location"}
	if not is_discovered(id):
		return {"ok": false, "reason": "you have not found this place yet"}
	current = id
	_log("Travelled to %s" % location(id).get("name", id))
	return {"ok": true, "location": current_location()}


func actions() -> Array:
	return current_location().get("actions", [])


func act(action_id: String) -> Dictionary:
	if not actions().any(func(entry): return String(entry.get("id", "")) == action_id):
		return {"ok": false, "reason": "that action is not available here"}
	match action_id:
		"rest", "treat_shock":
			stress = 0
			return _result(true, "The static recedes. For now.")
		"read_notes":
			return _result(true, "The file repeats one phrase: the sky is a door.")
		"briefing":
			flags["briefed"] = true
			discover("unsa_hq")
			discover("market")
			discover("harbor")
			return _result(true, "UNSA opens the Lakkahaltia file and assigns you a partner.")
		"case_board":
			return _result(true, "Three agents, one dream, eleven seconds of missing sky.")
		"recruit_romppainen":
			return recruit("romppainen")
		"interview_witness":
			var check := _check("Awareness", 0, 8)
			if bool(check.get("success", false)):
				_add_clue("witness")
				discover("clinic")
				return _result(true, "She talks. The sky opened at 03:14.", check)
			return _result(false, "She closes the shutters and turns up the radio.", check)
		"buy_stimulants":
			if credits < 2:
				return _result(false, "You cannot afford it.")
			credits -= 2
			stress = maxi(0, stress - 1)
			return _result(true, "Two credits for a paper envelope of amphetamine.")
		"search_terminal":
			var check := _check("Cognition", 1, 9)
			if bool(check.get("success", false)):
				_add_clue("terminal")
				discover("warehouse")
				return _result(true, "The manifest lists a container with no ship.", check)
			return _result(false, "The terminal logs you out and prints a warning in Finnish.", check)
		"confront_guard":
			var hit := _attack(12)
			if bool(hit.get("hit", false)):
				threat_hp = maxi(0, threat_hp - 5)
				discover("warehouse")
				return _result(true, "The guard goes down. The freezer door is behind him.", hit)
			player_hp = maxi(1, player_hp - 2)
			return _result(false, "He swings a torch; you lose two hit points.", hit)
		"interview_doctor":
			if not is_clue("witness"):
				return _result(false, "The doctor will not see you without a referral.")
			_add_clue("doctor")
			discover("warehouse")
			return _result(true, "Three agents, the same dream, one week.")
		"confront":
			var hit := _attack(13)
			if bool(hit.get("hit", false)):
				threat_hp = maxi(0, threat_hp - 5)
				if threat_hp == 0:
					flags["resolved"] = true
					return _result(true, "The thing behind the freezer stops singing.", hit)
				return _result(true, "You hit it. It keeps humming.", hit)
			player_hp = maxi(1, player_hp - 3)
			return _result(false, "The hum fills your teeth; you lose three hit points.", hit)
		"recover_device":
			if not bool(flags.get("resolved", false)):
				return _result(false, "Not while it is still singing.")
			_add_clue("device")
			flags["case_won"] = true
			return _result(true, "You carry the transmitter into the rain. The case is yours.")
	return _result(false, "Nothing happens.")


func recruit(id: String) -> Dictionary:
	if party.size() >= PARTY_CAP:
		return _result(false, "A mission party is at most four agents.")
	if party.any(func(member): return String(member.get("id", "")) == id):
		return _result(false, "Already in the party.")
	for entry in data.get("recruits", []):
		if String(entry.get("id", "")) == id:
			party.append(entry.duplicate())
			_log("%s joins the party." % entry.get("name", id))
			return _result(true, "%s joins the party." % entry.get("name", id))
	return _result(false, "No such agent is available.")


func _check(attribute: String, rank: int, difficulty: int) -> Dictionary:
	if adapter == null:
		return {"success": false, "reason": "no rules adapter"}
	var score := 10
	return adapter.skill_check(score, rank, difficulty)


func _attack(armor_class: int) -> Dictionary:
	if adapter == null:
		return {"hit": false, "reason": "no rules adapter"}
	return adapter.attack_roll(10, 0, 1, armor_class)


func _add_clue(id: String) -> void:
	if not is_clue(id):
		clues.append({"id": id, "text": String(data.get("clues", {}).get(id, ""))})
		_log("Clue: %s" % data.get("clues", {}).get(id, id))


func is_clue(id: String) -> bool:
	return clues.any(func(entry): return String(entry.get("id", "")) == id)


func _result(ok: bool, message: String, check: Dictionary = {}) -> Dictionary:
	_log(message)
	return {"ok": ok, "message": message, "check": check}


func _log(line: String) -> void:
	log_lines.append(line)
	if log_lines.size() > 40:
		log_lines.pop_front()


func summary() -> Dictionary:
	return {
		"location": current,
		"discovered": discovered.duplicate(),
		"clues": clues.size(),
		"party": party.size(),
		"stress": stress,
		"player_hp": player_hp,
		"threat_hp": threat_hp,
		"flags": flags.duplicate(),
		"credits": credits,
	}


func to_dict() -> Dictionary:
	return {
		"current": current, "discovered": discovered, "clues": clues,
		"party": party, "flags": flags, "credits": credits, "stress": stress,
		"player_hp": player_hp, "threat_hp": threat_hp,
	}


func from_dict(state: Dictionary) -> bool:
	if not state.has("current") or location(String(state["current"])).is_empty():
		return false
	current = String(state["current"])
	discovered = Array(state.get("discovered", [current]))
	clues = Array(state.get("clues", []))
	party = Array(state.get("party", [PC.duplicate()]))
	flags = Dictionary(state.get("flags", {}))
	credits = int(state.get("credits", 3))
	stress = int(state.get("stress", 0))
	player_hp = int(state.get("player_hp", 10))
	threat_hp = int(state.get("threat_hp", 12))
	return true
