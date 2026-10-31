## Noösphere and ontological apocalypse: optional narrative layer (#943).
##
## Inspired by the *ideas* of The Veil and Apocalypse World; the implementation, wording and
## state model are original. CWN remains responsible for dice, hacking, saves, combat and
## character progression; GUMSHOE's core-clue rule remains the only authority on whether a
## necessary clue can be found; Stress, Psyche and the condition layer remain the only
## authorities on what exposure costs.
##
## What this module is allowed to do, stated as code because prose cannot enforce it:
##
## * It **keeps records**. A perceived fact, the channel it arrived on, the source, and the
##   hypotheses somebody has about it are separate fields, and no field is derived from another.
## * It **reads and writes clock state**. A clock moves one segment per adjudicated event with a
##   written trigger, and a countermeasure walks it back. Nothing ticks on its own.
## * It **delegates**. `open_mind()` never resolves anything: it says whether contact is even
##   possible and hands the risky part to the CWN / approved-PSI procedure.
##
## What it may not do, and there is no code path here that could: roll dice, produce a modifier,
## set a difficulty, keep a mental-health meter, grant a psychic power, or decide what a
## character believes.
extends RefCounted
class_name NoopunkNoosphere

##: The converged channels of §1 of the design module. `hybrid` is a channel, not a fifth
##: mechanical subsystem: it exists so a contradictory overlay can be recorded as what it is
##: instead of being forced into one of the four that produced it.
const CHANNELS := ["physical", "cybernetic", "psychic", "social", "hybrid"]

##: Descriptive only. A state colours what a scene sounds like; it never adds to a roll.
const EMOTIONS := ["mad", "sad", "scared", "joyful", "powerful", "peaceful"]

##: #689 Stage 2 fixes clocks at four or six segments. Anything else is a second clock game.
const CLOCK_SEGMENTS := [4, 6]

##: Named, never implemented here: the authorities this layer defers to.
const RESOLVING_ENGINE := "cwn"
const CORE_CLUE_AUTHORITY := "src/rules/investigation.py"
const EXPOSURE_AUTHORITY := "src/rules/mental_load.py"
const PSI_AUTHORITY := "src/rules/psionics.py"

var evidence: Dictionary = {}
var interpretations: Dictionary = {}
var emotional_state: String = ""
var identity_choices: Array = []
var clocks: Dictionary = {}
var events: Array = []

## The player, never this module, selects the current emotion and an identity choice.
func choose_emotion(emotion: String) -> bool:
	if not EMOTIONS.has(emotion):
		return false
	emotional_state = emotion
	return true

func record_choice(choice_id: String, description: String) -> bool:
	if choice_id.strip_edges().is_empty() or description.strip_edges().is_empty():
		return false
	identity_choices.append({"id": choice_id, "description": description})
	return true

## A reported perception is not automatically a fact about its cause.
##
## Deliberately ungated: there is no competence, authorisation or roll argument, because a
## character whose senses work records what they perceived. What the record is *worth* is the
## `confidence` string and the provenance, not a permission check.
func record_perception(spec: Dictionary) -> bool:
	var id := str(spec.get("id", "")).strip_edges()
	var channel := str(spec.get("channel", ""))
	var source := str(spec.get("source", "")).strip_edges()
	if id.is_empty() or evidence.has(id) or not CHANNELS.has(channel) or source.is_empty():
		return false
	if str(spec.get("observation", "")).strip_edges().is_empty():
		return false
	evidence[id] = {
		"id": id, "channel": channel, "source": source,
		"observation": str(spec["observation"]),
		"confidence": str(spec.get("confidence", "unverified")),
		"reliability_note": str(spec.get("reliability_note", "")),
	}
	return true

## A hypothesis is the player's. Several may be held at once, and recording one never edits the
## perception it is about: the two records are separate on purpose (see the module doc, §4).
func interpret(perception_id: String, hypothesis: String) -> bool:
	if not evidence.has(perception_id) or hypothesis.strip_edges().is_empty():
		return false
	if not interpretations.has(perception_id):
		interpretations[perception_id] = []
	if interpretations[perception_id].has(hypothesis):
		return true
	interpretations[perception_id].append(hypothesis)
	return true

func hypotheses(perception_id: String) -> Array:
	return (interpretations.get(perception_id, []) as Array).duplicate()

## Counts channels, and says so. It is not a verdict: two reports from one compromised sensor
## still count as two unless somebody checks common-mode failure, which is a table judgement.
func triangulate(ids: Array) -> Dictionary:
	var channels: Array = []
	var missing: Array = []
	for id in ids:
		var key := str(id)
		if not evidence.has(key):
			missing.append(key)
			continue
		var channel := str(evidence[key]["channel"])
		if not channels.has(channel):
			channels.append(channel)
	return {"channels": channels, "independent_channels": channels.size(),
		"missing": missing, "requires_corroboration": channels.size() < 2}

## OPEN YOUR MIND: describes access and delegates the risky action to the established CWN/PSI
## rules. An untrained rookie cannot gain active psychic power from a narrative prompt.
## The caller supplies an already-resolved CWN/PSI outcome; this function resolves nothing.
func open_mind(channel: String, access_authorized: bool, active_psi: bool = false,
		risky: bool = false, resolved: bool = false, succeeded: bool = false) -> Dictionary:
	if not CHANNELS.has(channel):
		return {"ok": false, "reason": "unknown_channel"}
	if channel == "psychic" and not active_psi:
		return {"ok": false, "reason": "psi_capability_required"}
	if not access_authorized:
		return {"ok": false, "reason": "access_required"}
	if risky and not resolved:
		return {"ok": true, "requires_core_resolution": true, "engine": RESOLVING_ENGINE,
			"observation_only": true}
	if risky and not succeeded:
		return {"ok": true, "observation_only": true, "complication_allowed": true,
			"result": "risk_failed"}
	return {"ok": true, "observation_only": true, "result": "contact_possible",
		"engine": RESOLVING_ENGINE, "grants_power": false}

## A clock stores visible, reversible pressure. `segments` is 4 or 6 (#689 Stage 2) and is a
## property of the clock, not of the campaign.
func add_clock(id: String, actor: String, motivation: String, segments: int = 6) -> bool:
	if id.is_empty() or actor.is_empty() or motivation.is_empty() or clocks.has(id):
		return false
	if not CLOCK_SEGMENTS.has(segments):
		return false
	clocks[id] = {"actor": actor, "motivation": motivation, "segments": segments,
		"stage": 0, "history": []}
	return true

## The GM supplies a fictionally grounded trigger. No ticking from mere passage of time, one
## segment per event, and a negative step is a legal countermeasure rather than an error.
func change_clock(id: String, amount: int, trigger: String, countermeasure: String = "") -> Dictionary:
	if not clocks.has(id):
		return {"ok": false, "reason": "unknown_clock"}
	if amount == 0 or trigger.strip_edges().is_empty():
		return {"ok": false, "reason": "grounded_trigger_required"}
	if abs(amount) > 1:
		return {"ok": false, "reason": "single_step_only"}
	var before := int(clocks[id]["stage"])
	var after := clampi(before + amount, 0, int(clocks[id]["segments"]))
	if before == after:
		return {"ok": false, "reason": "clock_boundary"}
	clocks[id]["stage"] = after
	var event := {"clock": id, "from": before, "to": after, "trigger": trigger,
		"countermeasure": countermeasure}
	clocks[id]["history"].append(event.duplicate(true))
	events.append(event)
	return {"ok": true, "stage": after, "event": event}

func to_dict() -> Dictionary:
	return {"evidence": evidence.duplicate(true), "interpretations": interpretations.duplicate(true),
		"emotion": emotional_state, "identity_choices": identity_choices.duplicate(true),
		"clocks": clocks.duplicate(true), "events": events.duplicate(true)}
