class_name FactionIntelligence
extends RefCounted
## Human-centered investigative faction overlay (#922). Does not alter CWN mechanics.
const VERSION := 1
const STATUSES := ["rumor", "reported", "disputed", "verified", "unresolved", "denied"]
const LINKS := ["claimed_proxy", "confirmed_proxy", "cooperation", "funding", "antagonism", "competition"]
var factions: Dictionary = {}
var assertions: Dictionary = {}
var reputations: Dictionary = {}

func register_faction(spec: Dictionary) -> bool:
	var id := str(spec.get("id", "")).strip_edges()
	if id.is_empty() or factions.has(id) or str(spec.get("faction_type", "")).is_empty():
		return false
	var entry := spec.duplicate(true)
	entry["id"] = id
	factions[id] = entry
	reputations[id] = 0
	return true

func record_assertion(spec: Dictionary) -> bool:
	var id := str(spec.get("id", "")).strip_edges()
	var subject := str(spec.get("subject", ""))
	var status := str(spec.get("evidence_status", ""))
	if id.is_empty() or assertions.has(id) or not factions.has(subject) or not STATUSES.has(status):
		return false
	if str(spec.get("claim", "")).strip_edges().is_empty() or str(spec.get("source", "")).strip_edges().is_empty():
		return false
	if spec.has("relation") and not LINKS.has(str(spec["relation"])):
		return false
	var entry := spec.duplicate(true)
	entry["id"] = id
	assertions[id] = entry
	return true

func update_status(id: String, status: String, evidence_source: String) -> bool:
	if not assertions.has(id) or not STATUSES.has(status) or evidence_source.strip_edges().is_empty():
		return false
	var entry: Dictionary = assertions[id]
	var previous := str(entry["evidence_status"])
	var history: Array = entry.get("history", []).duplicate(true)
	history.append({"from": previous, "to": status, "source": evidence_source})
	entry["history"] = history
	entry["evidence_status"] = status
	assertions[id] = entry
	return true

func evidence_for(faction_id: String, include_unverified: bool = true) -> Array:
	var result: Array = []
	for id in assertions:
		var entry: Dictionary = assertions[id]
		if str(entry["subject"]) == faction_id and (include_unverified or str(entry["evidence_status"]) == "verified"):
			result.append(entry.duplicate(true))
	return result

func adjust_reputation(faction_id: String, delta: int) -> bool:
	if not factions.has(faction_id):
		return false
	reputations[faction_id] = clampi(int(reputations[faction_id]) + delta, -10, 10)
	return true

func to_dict() -> Dictionary:
	return {"version": VERSION, "factions": factions.duplicate(true),
		"assertions": assertions.duplicate(true), "reputations": reputations.duplicate(true)}

func from_dict(data: Dictionary) -> bool:
	if int(data.get("version", -1)) != VERSION:
		return false
	var fs: Variant = data.get("factions")
	var claims: Variant = data.get("assertions")
	var reps: Variant = data.get("reputations")
	if not (fs is Dictionary and claims is Dictionary and reps is Dictionary):
		return false
	for id in fs:
		if not fs[id] is Dictionary or str(fs[id].get("id", "")) != str(id):
			return false
		if not reps.has(id) or typeof(reps[id]) != TYPE_INT or int(reps[id]) < -10 or int(reps[id]) > 10:
			return false
	for id in claims:
		var claim: Variant = claims[id]
		if not claim is Dictionary or str(claim.get("id", "")) != str(id):
			return false
		if not fs.has(str(claim.get("subject", ""))) or not STATUSES.has(str(claim.get("evidence_status", ""))):
			return false
		if str(claim.get("source", "")).is_empty() or str(claim.get("claim", "")).is_empty():
			return false
		if claim.has("relation") and not LINKS.has(str(claim["relation"])):
			return false
	factions = fs.duplicate(true)
	assertions = claims.duplicate(true)
	reputations = reps.duplicate(true)
	return true
