## Investigative mode — the narrative half of the investigation layer (#897).
##
## Rule reference: `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md` §3, whose three-way split is:
##
##     **Finding information is not a roll. Interpreting it is not a roll. Acting on it is.**
##
## *Discovery* already has exactly one implementation, `godot/core/investigation_adapter.gd` (#718),
## which reads the same `noopunk-case-graph` JSON as `src/rules/investigation.py`. This overlay does not
## repeat it — a second copy of a clue rule is how the runtimes drift. What the core does not do, and what
## belongs to the narrative layer, is **interpretation**: which found clues bear on a hypothesis, which
## undercut it, and the refusal to decide.
##
## Hence the one thing this module must never do: announce a verdict or set the player's confidence. A
## wrong hypothesis is a legal game state, an anomaly may have an ordinary explanation, and the reading of
## evidence is the player's act, not the system's. Every function returns state; nothing rolls, nothing
## imports from `godot/core/`.
extends RefCounted
class_name NoopunkInvestigation

##: Interpretation stays open. There is deliberately no "confirmed"/"refuted" constant to reach for.
const VERDICT_OPEN := "open"

##: CWN costs a caller may be asked for when a clue needs work to reach. Names only; nothing is charged
##: here, and this is not a second currency — GUMSHOE's investigative pools are not imported (#704).
const COSTS: Array[String] = ["check_under_pressure", "scene_of_time", "favour"]


## What the found clues say about one hypothesis.
##
## `clue_tags` maps a clue id to its tags; the hypothesis names the tags it expects to support it and the
## tags that would undercut it. Returns the supporting and contradicting clue ids — and always the same
## open verdict, so no call site can mistake a summary for a decision.
static func interpret(hypothesis: Dictionary, clue_tags: Dictionary, found: Array,
		enabled: bool = true) -> Dictionary:
	if not enabled:
		return {"ok": true, "overlay": false, "verdict": VERDICT_OPEN, "confidence": null}
	var supports: Array[String] = []
	var contradicts: Array[String] = []
	for raw in found:
		var clue_id := String(raw)
		if not clue_tags.has(clue_id):
			continue
		var tags: Array = clue_tags[clue_id]
		if _carries(tags, hypothesis.get("supports", [])):
			supports.append(clue_id)
		if _carries(tags, hypothesis.get("contradicts", [])):
			contradicts.append(clue_id)
	return {
		"ok": true,
		"overlay": true,
		"hypothesis": String(hypothesis.get("id", "")),
		"supports": supports,
		"contradicts": contradicts,
		"verdict": VERDICT_OPEN,
		"confidence": null,
	}


## Which hypotheses are still live: any that no found clue contradicts. A hypothesis nobody can rule out
## stays open, which is the investigative game rather than a failure state.
static func open_hypotheses(hypotheses: Array, clue_tags: Dictionary, found: Array) -> Array[String]:
	var live: Array[String] = []
	for raw in hypotheses:
		var hypothesis: Dictionary = raw
		var reading := interpret(hypothesis, clue_tags, found)
		if reading["contradicts"].is_empty():
			live.append(String(hypothesis.get("id", "")))
	return live


## A cost name the narrative layer may ask for. Rejects anything else, so no caller invents a currency.
static func validate_cost(cost: String) -> bool:
	return cost.is_empty() or COSTS.has(cost)


static func _carries(tags: Array, wanted: Array) -> bool:
	for tag in wanted:
		if tags.has(tag):
			return true
	return false
