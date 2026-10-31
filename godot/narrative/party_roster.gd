## UNSA field party and authority rules (#920).
##
## Party membership is 1-4 including Tony; remote controller/AI never take a slot. Recruitment is
## situational (mission tag, trust, authorization), active PSI belongs only to designated assets and
## only in scripted scenes, and no AI action runs without a named human approval on the record.
class_name NoopunkPartyRoster
extends RefCounted

const DATA := "res://data/scenarios/party_roster.json"

var data: Dictionary = {}
var members: Dictionary = {}
var active: Array = []
var trust: Dictionary = {}
var approvals: Array = []
var log_lines: Array = []


func _init(path: String = DATA) -> void:
	data = _load(path)
	for entry in data.get("members", []):
		members[String(entry["id"])] = entry
		trust[String(entry["id"])] = 0
	var pc := String(data.get("pc", ""))
	if not pc.is_empty() and not active.has(pc):
		active.append(pc)


func _load(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("party_roster: cannot open %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func cap() -> int:
	return int(data.get("cap", 4))


func member(id: String) -> Dictionary:
	return members.get(id, {})


func is_active(id: String) -> bool:
	return active.has(id)


func size() -> int:
	return active.size()


func active_members() -> Array:
	var rows: Array = []
	for id in active:
		rows.append(member(String(id)))
	return rows


## Recruit a situational ally. `context` carries the mission tags, the member's trust, and any
## authorisation token the mission grants. A fifth member is refused, never silently dropped.
func recruit(id: String, context: Dictionary = {}) -> Dictionary:
	var entry := member(id)
	if entry.is_empty():
		return _fail("No such agent is available.")
	if is_active(id):
		return _fail("Already in the party.")
	if size() >= cap():
		return _fail("A mission party is at most four agents, including Tony.")
	var required_tags: Array = entry.get("prerequisites", {}).get("mission_tags", [])
	if not required_tags.is_empty():
		var offered: Array = Array(context.get("mission_tags", []))
		if not required_tags.any(func(tag): return offered.has(String(tag))):
			return _fail("%s is not available for this mission." % entry.get("name", id))
	var required_authorization := String(entry.get("prerequisites", {}).get("authorization", ""))
	if not required_authorization.is_empty() and String(context.get("authorization", "")) != required_authorization:
		return _fail("%s needs %s authorisation." % [entry.get("name", id), required_authorization])
	var minimum := int(entry.get("prerequisites", {}).get("min_trust", 0))
	if int(context.get("trust", trust.get(id, 0))) < minimum:
		return _fail("%s does not trust you enough yet." % entry.get("name", id))
	active.append(id)
	trust[id] = int(context.get("trust", trust.get(id, 0)))
	_log("%s joins the party." % entry.get("name", id))
	return {"ok": true, "message": "%s joins the party." % entry.get("name", id)}


func dismiss(id: String, reason: String = "") -> Dictionary:
	if id == String(data.get("pc", "")):
		return _fail("Tony cannot leave his own party.")
	if not is_active(id):
		return _fail("Not in the party.")
	active.erase(id)
	_log("%s leaves the party%s." % [member(id).get("name", id), ": " + reason if reason else ""])
	return {"ok": true, "message": "left"}


func set_trust(id: String, value: int) -> void:
	if members.has(id):
		trust[id] = value


## Record a named human approval for an action. The approver must exist and the authority must be
## one of Supo/Europol/UNSA and be the authority the action is brought under.
func approve(approver: String, authority: String, action: String) -> Dictionary:
	if approver.strip_edges().is_empty():
		return _fail("An action needs a named human approver.")
	if not Array(data.get("authorities", [])).has(authority):
		return _fail("Unknown authority: %s" % authority)
	var record := {"approver": approver, "authority": authority, "action": action}
	approvals.append(record)
	_log("%s approved %s under %s authority." % [approver, action, authority])
	return {"ok": true, "approval": record}


func is_approved(action: String) -> bool:
	return approvals.any(func(entry): return String(entry.get("action", "")) == action)


## An AI recommendation alone never executes. It becomes executable only after a matching approval.
func execute_ai_action(action: String) -> Dictionary:
	if not is_approved(action):
		return _fail("No named human approval for: %s" % action)
	_log("Executed with approval: %s" % action)
	return {"ok": true}


## Active PSI is restricted to a designated asset, in a scripted scene, with psi-office authority.
func use_active_psi(actor_id: String, scene_id: String) -> Dictionary:
	var entry := member(actor_id)
	if entry.is_empty() or not is_active(actor_id):
		return _fail("No such active asset.")
	if not bool(entry.get("active_psi", false)):
		return _fail("%s has no active PSI capability." % entry.get("name", actor_id))
	if not Array(data.get("scripted_psi_scenes", [])).has(scene_id):
		return _fail("No scripted PSI beat here.")
	var psi_approval := approvals.any(func(row): return String(row.get("authority", "")) == "unsa_psi_office")
	if not psi_approval:
		return _fail("No psi-office authorisation on record.")
	_log("%s uses scripted PSI in %s." % [entry.get("name", actor_id), scene_id])
	return {"ok": true, "actor": actor_id, "scene": scene_id}


func pc_has_active_psi() -> bool:
	var pc := member(String(data.get("pc", "")))
	return bool(pc.get("active_psi", false))


func to_dict() -> Dictionary:
	return {"active": active.duplicate(), "trust": trust.duplicate(), "approvals": approvals.duplicate()}


func from_dict(state: Dictionary) -> bool:
	var pc := String(data.get("pc", ""))
	var incoming: Array = Array(state.get("active", [pc]))
	if incoming.is_empty() or not incoming.has(pc) or incoming.size() > cap():
		return false
	for id in incoming:
		if not members.has(String(id)):
			return false
	active = incoming.duplicate()
	trust = Dictionary(state.get("trust", trust))
	approvals = Array(state.get("approvals", []))
	return true


func _fail(message: String) -> Dictionary:
	return {"ok": false, "message": message}


func _log(line: String) -> void:
	log_lines.append(line)
	if log_lines.size() > 40:
		log_lines.pop_front()
