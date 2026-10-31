## Noösphere and ontological apocalypse: optional narrative layer (#943).
## Inspired by the *ideas* of The Veil and Apocalypse World; original implementation.
## CWN remains responsible for dice, hacking, saves, combat and character progression.
extends RefCounted
class_name NoopunkNoosphere

const CHANNELS := ["physical", "cybernetic", "psychic", "social"]
const EMOTIONS := ["mad", "sad", "scared", "joyful", "powerful", "peaceful"]
const MAX_CLOCK := 6

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

func interpret(perception_id: String, hypothesis: String) -> bool:
    if not evidence.has(perception_id) or hypothesis.strip_edges().is_empty():
        return false
    interpretations[perception_id] = hypothesis
    return true

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

## OPEN YOUR MIND: describes access and delegates risky action to the established CWN/PSI
## rules. An untrained rookie cannot gain active psychic power from a narrative prompt.
## Caller supplies resolved CWN/PSI outcome only after its own legitimate check.
func open_mind(channel: String, access_authorized: bool, active_psi: bool = false,
        risky: bool = false, resolved: bool = false, succeeded: bool = false) -> Dictionary:
    if not CHANNELS.has(channel):
        return {"ok": false, "reason": "unknown_channel"}
    if channel == "psychic" and not active_psi:
        return {"ok": false, "reason": "psi_capability_required"}
    if not access_authorized:
        return {"ok": false, "reason": "access_required"}
    if risky and not resolved:
        return {"ok": true, "requires_core_resolution": true, "engine": "cwn",
            "observation_only": true}
    if risky and not succeeded:
        return {"ok": true, "observation_only": true, "complication_allowed": true,
            "result": "risk_failed"}
    return {"ok": true, "observation_only": true, "result": "contact_possible",
        "engine": "cwn", "grants_power": false}

## A clock stores a visible, reversible state. It cannot advance automatically.
func add_clock(id: String, actor: String, motivation: String) -> bool:
    if id.is_empty() or actor.is_empty() or motivation.is_empty() or clocks.has(id):
        return false
    clocks[id] = {"actor": actor, "motivation": motivation, "stage": 0,
        "history": []}
    return true

## The GM supplies a fictionally grounded trigger. No ticking from mere passage of time.
func change_clock(id: String, amount: int, trigger: String, countermeasure: String = "") -> Dictionary:
    if not clocks.has(id):
        return {"ok": false, "reason": "unknown_clock"}
    if amount == 0 or trigger.strip_edges().is_empty():
        return {"ok": false, "reason": "grounded_trigger_required"}
    if abs(amount) > 1:
        return {"ok": false, "reason": "single_step_only"}
    var before := int(clocks[id]["stage"])
    var after := clampi(before + amount, 0, MAX_CLOCK)
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
