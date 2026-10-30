## CWN hacking kernel for the #749 vertical slice.
##
## The procedure is the source's: a character needs **access** to a node, must reach it through
## **connectivity** from an already-connected node, needs a **program** that provides the verb,
## pays **CPU**, and failed checks accumulate against network Security. The SRD's clock is not a
## trace meter: **every two failed checks count as one Alert the Network action**
## (hacking/hacking-mechanics/#hacking-a-device-or-server), and that action must be taken twice
## before the network is alerted (hacking/cyberspace-actions/#alert-the-network). This file
## implements that clock and refuses the invented trace die the first slice shipped.
##
## What this file does NOT do is assert the catalogue: Verb costs, CPU prices and Security values
## are loaded from data (`godot/scenarios/mvp_romppainen/hacking.json`) and remain slice
## calibration pending a source-by-source check against the CWN SRD.
##
## Deliberately out of scope for v0: cyberdeck hardware modifiers, program stacking, ICE/deadly
## countermeasures, and multiple simultaneous intruders.
extends RefCounted
class_name NoopunkHacking

var adapter: Object
var nodes: Dictionary = {}
var deck: Dictionary = {}
var costs: Dictionary = {}
var connected: Array = []
var failures := 0
var alert_actions := 0
var alarm := false
var log: Array = []
var verbs_done: Dictionary = {}

#: SRD: every two failed checks against network Security count as one Alert action.
const FAILURES_PER_ALERT_ACTION := 2
#: SRD: the Alert the Network action must be taken twice before the network is alerted.
const ALERT_ACTIONS_TO_TRIGGER := 2
#: SRD: wireless link -2 on every cyberspace check; a VR crown adds a further -1.
const WIRELESS_PENALTY := -2
const VR_CROWN_PENALTY := -1

const DEFAULT_COSTS := {
	"connect_cpu": 1,
	"verb_cpu": 1,
	"access_per_verb": 1,
	"program_skill": 1,
}

func _init(rules_adapter: Object, network: Dictionary, deck_spec: Dictionary = {}) -> void:
	adapter = rules_adapter
	nodes = network.get("nodes", {})
	costs = DEFAULT_COSTS.duplicate()
	for key in network.get("costs", {}):
		costs[key] = network.get("costs", {})[key]
	deck = {
		"cpu": int(deck_spec.get("cpu", 6)),
		"cpu_max": int(deck_spec.get("cpu", 6)),
		"access": int(deck_spec.get("access", 1)),
		"programs": deck_spec.get("programs", []),
		"int": int(deck_spec.get("int", 10)),
		"program_rank": int(deck_spec.get("program_rank", costs["program_skill"])),
		"wireless": bool(deck_spec.get("wireless", false)),
		"vr_crown": bool(deck_spec.get("vr_crown", false)),
	}
	var entry := String(network.get("entry", ""))
	if entry.is_empty() and not nodes.is_empty():
		entry = String(nodes.keys()[0])
	if entry != "" and nodes.has(entry):
		# The entry point is reached by physical access, not by a check.
		connected.append(entry)

func is_node_connected(node_id: String) -> bool:
	return connected.has(node_id)

## Reaching a node requires a path from something already connected. Access is checked here too,
## because a node you may not read is not a node you have reached.
func connect_node(node_id: String) -> Dictionary:
	if alarm:
		return {"ok": false, "reason": "alarm_active"}
	if not nodes.has(node_id):
		return {"ok": false, "reason": "no_such_node"}
	if is_node_connected(node_id):
		return {"ok": false, "reason": "already_connected"}
	var node: Dictionary = nodes[node_id]
	var reachable := false
	for link in node.get("links", []):
		if is_node_connected(String(link)):
			reachable = true
			break
	if not reachable:
		return {"ok": false, "reason": "no_path"}
	var cpu_cost := int(costs["connect_cpu"])
	if int(deck["cpu"]) < cpu_cost:
		return {"ok": false, "reason": "no_cpu"}
	var needed := int(node.get("access_required", 0))
	if int(deck["access"]) < needed:
		return {"ok": false, "reason": "insufficient_access", "needed": needed}
	deck["cpu"] = int(deck["cpu"]) - cpu_cost
	if needed > 0:
		# SRD: crossing a barrier is what Access is spent on; Jack In itself is a Move action.
		deck["access"] = int(deck["access"]) - needed
	connected.append(node_id)
	var entry := {"action": "connect", "node": node_id, "cpu": deck["cpu"], "access": deck["access"]}
	log.append(entry)
	return {"ok": true, "cpu": deck["cpu"], "access": deck["access"]}

## Perform a verb (query/control/…) against a connected node.
func act(node_id: String, verb: String) -> Dictionary:
	if alarm:
		return {"ok": false, "reason": "alarm_active"}
	if not nodes.has(node_id):
		return {"ok": false, "reason": "no_such_node"}
	if not is_node_connected(node_id):
		return {"ok": false, "reason": "not_connected"}
	var node: Dictionary = nodes[node_id]
	if not (verb in node.get("verbs", [])):
		return {"ok": false, "reason": "verb_unavailable"}
	if not (verb in deck["programs"]):
		return {"ok": false, "reason": "no_program"}
	var cpu_cost := int(costs["verb_cpu"])
	if int(deck["cpu"]) < cpu_cost:
		return {"ok": false, "reason": "no_cpu"}
	var access_cost := int(costs["access_per_verb"])
	if int(deck["access"]) < access_cost:
		return {"ok": false, "reason": "insufficient_access", "needed": access_cost}
	deck["cpu"] = int(deck["cpu"]) - cpu_cost
	deck["access"] = int(deck["access"]) - access_cost
	var penalty := 0
	if bool(deck["wireless"]):
		penalty += WIRELESS_PENALTY
	if bool(deck["vr_crown"]):
		penalty += VR_CROWN_PENALTY
	var check: Dictionary = adapter.skill_check(
		int(deck["int"]), int(deck["program_rank"]), int(node.get("security", 8)), penalty
	)
	var success := bool(check.get("success", false))
	if not success:
		# The SRD's clock: two failed checks are one Alert action; two Alert actions alert the net.
		failures += 1
		alert_actions = failures / FAILURES_PER_ALERT_ACTION
		if alert_actions >= ALERT_ACTIONS_TO_TRIGGER:
			alarm = true
	var key := "%s:%s" % [node_id, verb]
	if success:
		verbs_done[key] = true
	var entry := {
		"action": "verb", "node": node_id, "verb": verb, "check": check,
		"success": success, "cpu": deck["cpu"], "access": deck["access"],
		"failures": failures, "alert_actions": alert_actions, "alarm": alarm,
	}
	log.append(entry)
	return entry

func done(node_id: String, verb: String) -> bool:
	return bool(verbs_done.get("%s:%s" % [node_id, verb], false))

func can_act(node_id: String, verb: String) -> bool:
	if alarm or not is_node_connected(node_id) or not nodes.has(node_id):
		return false
	if not (verb in nodes[node_id].get("verbs", [])):
		return false
	if not (verb in deck["programs"]):
		return false
	return int(deck["cpu"]) >= int(costs["verb_cpu"])
