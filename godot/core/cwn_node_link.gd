extends RefCounted
class_name CwnNodeLink

## A playable node network for CWN hacking (SRD 4.1–4.5): cyberspace basics, Access, Verbs, Subjects,
## the security ladder and the alert clock.
##
## The rule arithmetic is NOT here. `CwnHackingRules` owns Access pools, security difficulty and the
## Int/Program check; `CwnProgramRules` owns Verbs and Subjects. This file is the network state machine
## that a screen drives: which node you are on, what you have reached, and what you may legally do next.
## Splitting it this way is what lets the same procedure be replayed headlessly.

const Rules := preload("res://godot/core/cwn_hacking.gd")
const Programs := preload("res://godot/core/cwn_program_rules.gd")

const CATALOGUE_PATH := "res://data/rules/cwn_program_catalogue.json"

static var _catalogue: Dictionary = {}


static func catalogue() -> Dictionary:
	if _catalogue.is_empty():
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CATALOGUE_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_catalogue = parsed
	return _catalogue


static func verbs() -> Dictionary:
	return catalogue().get("verbs", {})


static func subjects() -> Dictionary:
	return catalogue().get("subjects", {})


## A node the decker can see. `linked_to` lists the nodes reachable from here without a check beyond
## Access; an unlinked node is only visible once its neighbour is accessed.
static func node(node_id: String, node_name: String, security: int, subject: String,
		linked_to: Array = []) -> Dictionary:
	return {"id": node_id, "name": node_name, "security": security, "subject": subject,
		"linked_to": linked_to, "accessed": false}


## A network: the deck's starting state and its nodes.
static func network(nodes: Array, entry_node: String) -> Dictionary:
	return {
		"nodes": nodes,
		"entry": entry_node,
		"current": "",
		"access": 0,
		"alert": 0,
		"log": [],
		"jacked_in": false,
		"finished": false,
	}


static func _find(net: Dictionary, node_id: String) -> Dictionary:
	for node in net.get("nodes", []):
		if String(node.get("id", "")) == node_id:
			return node
	return {}


static func _say(net: Dictionary, message: String) -> void:
	var log: Array = net.get("log", [])
	log.append(message)
	net["log"] = log


## Jack in at the entry node. The deck's Access pool is INT modifier + Program rank + the deck's Bonus
## Access (SRD 4.1); it refreshes per round and Verbs spend it, so an empty pool is a real state.
static func jack_in(net: Dictionary, int_modifier: int = 0, program_rank: int = 0,
		deck_bonus: int = 0) -> Dictionary:
	if bool(net.get("jacked_in", false)):
		return {"error": "already_jacked_in"}
	var entry := _find(net, String(net.get("entry", "")))
	if entry.is_empty():
		return {"error": "entry_node_missing", "node": net.get("entry")}
	net["jacked_in"] = true
	net["current"] = entry["id"]
	net["alert"] = 0
	net["access"] = Rules.access_pool(int_modifier, program_rank, deck_bonus)
	_say(net, "Jacked in at %s. Access %d." % [entry["name"], int(net["access"])])
	return {"ok": true, "net": net}


## Attempt Access on the current node (or a linked node). The check is the SRD's Int/Program roll
## against the node's security; success marks the node accessed and opens its links.
static func attempt_access(net: Dictionary, dice: Array, int_modifier: int, program_rank: int,
		node_id: String = "", deck_bonus: int = 0) -> Dictionary:
	if not bool(net.get("jacked_in", false)):
		return {"error": "not_jacked_in"}
	var target_id := node_id if not node_id.is_empty() else String(net.get("current", ""))
	var target := _find(net, target_id)
	if target.is_empty():
		return {"error": "unknown_node", "node": target_id}
	if bool(target.get("accessed", false)):
		return {"error": "node_already_accessed", "node": target_id}
	if not _reachable(net, target_id):
		return {"error": "node_not_reachable", "node": target_id}

	var difficulty := Rules.security_difficulty(int(target.get("security", 0)),
		int(net.get("alert", 0)) > 0)
	if not bool(difficulty.get("ok", false)):
		return difficulty
	var check := Rules.hacking_check(dice, int_modifier, program_rank,
		int(difficulty["difficulty"]))
	if not bool(check.get("ok", false)):
		return check
	if not bool(check.get("success", false)):
		net["alert"] = int(net.get("alert", 0)) + 1
		_say(net, "Access to %s failed (%d vs %d). Alert %d." % [target["name"], int(check["total"]),
			int(difficulty["difficulty"]), int(net["alert"])])
		return {"ok": true, "success": false, "net": net, "check": check}

	target["accessed"] = true
	net["current"] = target_id
	_say(net, "Accessed %s (%d vs %d). Access pool %d." % [target["name"],
		int(check["total"]), int(difficulty["difficulty"]), int(net.get("access", 0))])
	return {"ok": true, "success": true, "net": net, "check": check}


## A node is reachable when it is the entry, the current node, or a link of an accessed node.
static func _reachable(net: Dictionary, node_id: String) -> bool:
	if node_id == String(net.get("entry", "")):
		return true
	for node in net.get("nodes", []):
		if bool(node.get("accessed", false)) and Array(node.get("linked_to", [])).has(node_id):
			return true
	return node_id == String(net.get("current", ""))


## Run a Verb against a Subject on a node. Legality first: the Verb must list the Subject's type, the
## node must be accessed, and the Access pool must cover the cost.
static func run_verb(net: Dictionary, verb_name: String, subject_name: String,
		dice: Array = [], int_modifier: int = 0, program_rank: int = 0) -> Dictionary:
	if not bool(net.get("jacked_in", false)):
		return {"error": "not_jacked_in"}
	var verb: Dictionary = verbs().get(verb_name, {})
	if verb.is_empty():
		return {"error": "unknown_verb", "verb": verb_name}
	var subject: Dictionary = subjects().get(subject_name, {})
	if subject.is_empty():
		return {"error": "unknown_subject", "subject": subject_name}

	var node_id := String(net.get("current", ""))
	var node := _find(net, node_id)
	if node.is_empty() or not bool(node.get("accessed", false)):
		return {"error": "no_access_on_current_node", "node": node_id}
	if not _subject_matches_node(node, subject_name):
		return {"error": "subject_not_present_on_node", "node": node_id, "subject": subject_name}

	var allowed: Array = verb.get("target_types", [])
	if not allowed.has(String(subject.get("subject_type", ""))):
		return {"error": "verb_cannot_target_this_subject", "verb": verb_name,
			"subject_type": subject.get("subject_type"), "allowed": allowed}

	var cost := int(verb.get("access_cost", 0))
	if int(net.get("access", 0)) < cost:
		return {"error": "insufficient_access", "needed": cost, "have": int(net.get("access", 0))}

	var outcome := {"ok": true, "verb": verb_name, "subject": subject_name, "net": net}
	if bool(verb.get("requires_check", true)):
		var difficulty := Rules.security_difficulty(int(node.get("security", 0)),
			int(net.get("alert", 0)) > 0)
		var check := Rules.hacking_check(dice, int_modifier, program_rank,
			int(difficulty.get("difficulty", 10)), false, false,
			int(verb.get("skill_modifier", 0)))
		outcome["check"] = check
		if not bool(check.get("success", false)):
			net["alert"] = int(net.get("alert", 0)) + 1
			_say(net, "%s on %s failed. Alert %d." % [verb_name, subject_name, int(net["alert"])])
			outcome["success"] = false
			return outcome

	net["access"] = int(net.get("access", 0)) - cost
	_say(net, "%s on %s succeeded%s." % [verb_name, subject_name,
		" (program terminated)" if bool(verb.get("self_terminating", false)) else ""])
	outcome["success"] = true
	return outcome


static func _subject_matches_node(node: Dictionary, subject_name: String) -> bool:
	return String(node.get("subject", "")) == subject_name


## Disconnect: the run is over. Named `disconnect_deck`, not `disconnect`, which would shadow the
## `Object` signal method and fail to resolve at the call site.
static func disconnect_deck(net: Dictionary, reason: String = "") -> Dictionary:
	if not bool(net.get("jacked_in", false)):
		return {"error": "not_jacked_in"}
	net["jacked_in"] = false
	net["finished"] = true
	_say(net, "Disconnected%s." % ((": " + reason) if not reason.is_empty() else ""))
	return {"ok": true, "net": net}


## Everything a screen needs to draw the network, without it reaching into the state itself.
static func visible_nodes(net: Dictionary) -> Array:
	var out: Array = []
	for node in net.get("nodes", []):
		var reachable := _reachable(net, String(node.get("id", "")))
		out.append({
			"id": node.get("id", ""),
			"name": node.get("name", ""),
			"security": int(node.get("security", 0)),
			"subject": node.get("subject", ""),
			"accessed": bool(node.get("accessed", false)),
			"reachable": reachable,
			"current": String(node.get("id", "")) == String(net.get("current", "")),
		})
	return out
