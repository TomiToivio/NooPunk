class_name UNSAFieldOperations
extends RefCounted
## Mission-level UNSA overlay. Base CWN party and resolution remain unchanged (#920).
const PartyScript := preload("res://godot/core/party.gd")
const FORMAT_VERSION := 1
const AGENCIES := ["Suojelupoliisi", "Europol", "UNSA"]
var party = PartyScript.new()
var availability: Dictionary = {}
var trust: Dictionary = {}
var approvals: Array = []
var psi_events: Array = []

func start_agent(id: String, name: String, sheet: Dictionary = {}) -> bool:
	return party.create_agent(id, name, "UNSA", sheet)

func set_available(id: String, condition_met: bool) -> void:
	availability[id] = condition_met

func recruit(spec: Dictionary) -> Dictionary:
	var id := str(spec.get("id", ""))
	if not bool(availability.get(id, false)):
		return {"ok": false, "reason": "not_available"}
	if not party.join(spec):
		return {"ok": false, "reason": "roster_rejected"}
	return {"ok": true, "size": party.members.size()}

func release(id: String) -> bool:
	return party.leave(id)

func alter_trust(id: String, amount: int) -> void:
	trust[id] = clampi(int(trust.get(id, 0)) + amount, -10, 10)

func authorize(agency: String, officer: String, action: String, approved: bool) -> bool:
	if not AGENCIES.has(agency) or officer.strip_edges().is_empty() or action.strip_edges().is_empty():
		return false
	approvals.append({"agency": agency, "officer": officer, "action": action, "approved": approved})
	return true

func can_execute(action: String) -> bool:
	## A denial or disputed authorization cannot be overridden by AI suggestions.
	var has_approval := false
	for record in approvals:
		if str(record.get("action", "")) == action:
			if not bool(record.get("approved", false)):
				return false
			has_approval = true
	return has_approval

func scripted_psi(asset: Dictionary, scene_id: String, approved_action: String) -> Dictionary:
	if not bool(asset.get("designated_psi_asset", false)):
		return {"ok": false, "reason": "not_authorized_asset"}
	if scene_id.is_empty() or not can_execute(approved_action):
		return {"ok": false, "reason": "missing_human_approval"}
	var event := {"asset_id": str(asset.get("id", "")), "scene": scene_id, "approved_action": approved_action}
	if event["asset_id"].is_empty():
		return {"ok": false, "reason": "missing_asset_id"}
	psi_events.append(event)
	return {"ok": true, "event": event.duplicate(true)}

func to_dict() -> Dictionary:
	return {"version": FORMAT_VERSION, "party": party.to_dict(), "availability": availability.duplicate(true),
		"trust": trust.duplicate(true), "approvals": approvals.duplicate(true), "psi_events": psi_events.duplicate(true)}

func from_dict(data: Dictionary) -> bool:
	if int(data.get("version", -1)) != FORMAT_VERSION:
		return false
	if not (data.get("party") is Dictionary and data.get("availability") is Dictionary and data.get("trust") is Dictionary):
		return false
	if not (data.get("approvals") is Array and data.get("psi_events") is Array):
		return false
	var candidate = PartyScript.new()
	if not candidate.from_dict(data["party"]):
		return false
	for id in data["trust"]:
		if typeof(data["trust"][id]) != TYPE_INT or absi(int(data["trust"][id])) > 10:
			return false
	for record in data["approvals"]:
		if not record is Dictionary or not AGENCIES.has(str(record.get("agency", ""))):
			return false
	party = candidate
	availability = data["availability"].duplicate(true)
	trust = data["trust"].duplicate(true)
	approvals = data["approvals"].duplicate(true)
	psi_events = data["psi_events"].duplicate(true)
	return true
