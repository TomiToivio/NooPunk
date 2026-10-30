## Scene flow for the #749 vertical slice: home → UNSA HQ → mission → debrief.
##
## This is the piece that makes the slice a *game* rather than three test fixtures. It owns which
## location is legal to enter, what has to be true before the mission opens, and how the mission
## ends. It does not own dialogue, combat or hacking — those report into it.
##
## Design rule taken from the issue: the core evidence must remain reachable. A mission therefore
## can be resolved through an investigative approach, a tactical one, or both, and the flow
## records which was used for the debrief instead of scoring one as the "real" path.
extends RefCounted
class_name NoopunkSceneFlow

const HOME := "home"
const HQ := "hq"
const MISSION := "mission"
const DEBRIEF := "debrief"

const LOCATIONS := [HOME, HQ, MISSION, DEBRIEF]

var location := HOME
var briefed := false
var mission_open := false
var resolved := false
var approach := ""          ## "investigative", "tactical" or "mixed"
var conclusion := ""        ## "success", "failure" or "complication"
var objectives: Dictionary = {}   ## id -> true when achieved
var flags: Dictionary = {}
var history: Array = []

func _init() -> void:
	history.append({"location": location, "event": "start"})

## Legal transitions, checked rather than assumed.
func can_travel(to: String) -> Dictionary:
	if not (to in LOCATIONS):
		return {"ok": false, "reason": "unknown_location"}
	if to == location:
		return {"ok": false, "reason": "already_there"}
	if location == MISSION and not resolved:
		return {"ok": false, "reason": "mission_unresolved"}
	match to:
		HQ:
			if location == DEBRIEF:
				return {"ok": true}
			if location == HOME:
				return {"ok": true}
			return {"ok": false, "reason": "no_route"}
		MISSION:
			if location != HQ:
				return {"ok": false, "reason": "mission_is_briefed_at_hq"}
			if not briefed:
				return {"ok": false, "reason": "not_briefed"}
			return {"ok": true}
		DEBRIEF:
			if location != MISSION:
				return {"ok": false, "reason": "debrief_follows_mission"}
			if not resolved:
				return {"ok": false, "reason": "mission_unresolved"}
			return {"ok": true}
		HOME:
			if location in [HQ, DEBRIEF]:
				return {"ok": true}
			return {"ok": false, "reason": "no_route"}
	return {"ok": false, "reason": "no_route"}

func travel(to: String) -> Dictionary:
	var verdict := can_travel(to)
	if not bool(verdict["ok"]):
		return verdict
	location = to
	if to == MISSION:
		mission_open = true
	history.append({"location": location, "event": "travel", "from": history[-1]["location"] if not history.is_empty() else ""})
	return {"ok": true, "location": location}

## The HQ briefing is what opens the mission; without it the mission node stays locked.
func complete_briefing() -> void:
	briefed = true
	history.append({"location": location, "event": "briefed"})

func achieve(objective_id: String) -> bool:
	if objective_id.is_empty() or bool(objectives.get(objective_id, false)):
		return false
	objectives[objective_id] = true
	history.append({"location": location, "event": "objective", "id": objective_id})
	return true

func achieved(objective_id: String) -> bool:
	return bool(objectives.get(objective_id, false))

## Resolve the mission. `path` records how it was done, so the debrief and any later comparison
## can distinguish a nonviolent solution from a firefight without ranking them.
func resolve(path: String, result: String) -> Dictionary:
	if location != MISSION:
		return {"ok": false, "reason": "not_on_mission"}
	if resolved:
		return {"ok": false, "reason": "already_resolved"}
	if not (path in ["investigative", "tactical", "mixed"]):
		return {"ok": false, "reason": "unknown_path"}
	if not (result in ["success", "failure", "complication"]):
		return {"ok": false, "reason": "unknown_result"}
	approach = path
	conclusion = result
	resolved = true
	history.append({"location": location, "event": "resolved", "path": path, "result": result})
	return {"ok": true}

func ending() -> Dictionary:
	return {"approach": approach, "conclusion": conclusion, "objectives": objectives.keys()}

func to_dict() -> Dictionary:
	return {
		"location": location, "briefed": briefed, "mission_open": mission_open,
		"resolved": resolved, "approach": approach, "conclusion": conclusion,
		"objectives": objectives.duplicate(), "flags": flags.duplicate(),
		"history": history.duplicate(true),
	}

func from_dict(data: Dictionary) -> bool:
	if not data.has("location") or not (String(data["location"]) in LOCATIONS):
		# Invalid caller input, not an internal failure: the call refuses and returns false, which is
		# what the suite asserts. Logged as a warning so a shutdown gate can treat every `ERROR:` as
		# genuinely unexpected (#883).
		push_warning("NoopunkSceneFlow: unusable save data (refused)")
		return false
	location = String(data["location"])
	briefed = bool(data.get("briefed", false))
	mission_open = bool(data.get("mission_open", false))
	resolved = bool(data.get("resolved", false))
	approach = String(data.get("approach", ""))
	conclusion = String(data.get("conclusion", ""))
	objectives = Dictionary(data.get("objectives", {})).duplicate()
	flags = Dictionary(data.get("flags", {})).duplicate()
	history = Array(data.get("history", [])).duplicate(true)
	return true
