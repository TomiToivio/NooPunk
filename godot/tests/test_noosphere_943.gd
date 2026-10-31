## #943: the executable guards for the Noösphere / ontological-apocalypse overlay.
##
## Every row here answers a sentence the issue makes as a promise. The promises that matter are
## the ones a prose paragraph cannot keep, so they are asserted against the module's behaviour and
## its public surface: no second dice engine, no automatic psychic power, no belief changed by a
## die, no core-clue gate, no duplicate psychological track. The narrative content itself is the
## author's editorial material and is not asserted here.
extends RefCounted
const Noosphere = preload("res://mods/noopunk/noosphere.gd")

func _eq(name: String, value: Variant, expected: Variant) -> Array:
	return [name, value == expected, "got %s expected %s" % [str(value), str(expected)]]

## Method names that would mean the overlay had grown a resolution engine of its own.
func _forbidden_surface(m) -> Array:
	var hits: Array = []
	for entry in m.get_method_list():
		var name := str(entry.get("name", ""))
		for token in ["roll", "dice", "die_", "d20", "2d6", "modifier_d", "check"]:
			if name.contains(token):
				hits.append(name)
	return hits

## State keys that would mean the overlay had grown a second cost or harm track.
func _forbidden_state(m) -> Array:
	var hits: Array = []
	for key in m.to_dict().keys():
		for token in ["stress", "psyche", "sanity", "harm", "mental", "exposure"]:
			if str(key).contains(token):
				hits.append(str(key))
	return hits

func run() -> Array:
	var rows: Array = []
	var m = Noosphere.new()

	# --- the emotion channel is descriptive, never a stat -------------------------------
	rows.append(_eq("emotion is descriptive", m.choose_emotion("scared"), true))
	rows.append(_eq("unknown emotion refused", m.choose_emotion("omniscient"), false))
	rows.append(_eq("emotion has no attributes", m.to_dict().has("attribute_modifiers"), false))
	rows.append(_eq("emotions are never numeric", typeof(m.emotional_state), TYPE_STRING))

	# --- Open Your Mind delegates -------------------------------------------------------
	rows.append(_eq("unsupported psychic access refused",
		m.open_mind("psychic", true, false).get("reason"), "psi_capability_required"))
	rows.append(_eq("risky cyber operation delegates to core",
		m.open_mind("cybernetic", true, false, true).get("engine"), "cwn"))
	rows.append(_eq("contact does not grant powers",
		m.open_mind("psychic", true, true).get("grants_power"), false))
	rows.append(_eq("authorised psychic contact still grants no power",
		m.open_mind("psychic", true, true, true, true, true).get("grants_power"), false))
	rows.append(_eq("contact without access is refused",
		m.open_mind("physical", false).get("reason"), "access_required"))
	rows.append(_eq("unknown channel refused",
		m.open_mind("astral", true).get("reason"), "unknown_channel"))

	# --- the converged channels, including the contradictory one ------------------------
	rows.append(_eq("record physical observation",
		m.record_perception({"id": "a", "channel": "physical", "source": "lab", "observation": "trace"}), true))
	rows.append(_eq("record cyber observation",
		m.record_perception({"id": "b", "channel": "cybernetic", "source": "sensor", "observation": "log"}), true))
	rows.append(_eq("hybrid perception is a recordable channel",
		m.record_perception({"id": "c", "channel": "hybrid", "source": "two overlays",
			"observation": "the corridor is and is not there"}), true))
	rows.append(_eq("duplicate perception id refused",
		m.record_perception({"id": "a", "channel": "physical", "source": "lab",
			"observation": "again"}), false))
	rows.append(_eq("triangulation uses independent channels",
		m.triangulate(["a", "b"])["independent_channels"], 2))
	rows.append(_eq("triangulation counts a hybrid percept separately",
		m.triangulate(["a", "b", "c"])["independent_channels"], 3))
	rows.append(_eq("one channel invites corroboration, never refusal",
		m.triangulate(["a"])["requires_corroboration"], true))

	# --- a perception is not a verdict --------------------------------------------------
	rows.append(_eq("interpretation belongs to player", m.interpret("a", "possibly mundane"), true))
	rows.append(_eq("a second hypothesis is allowed", m.interpret("a", "a noetic residue"), true))
	rows.append(_eq("hypotheses accumulate", m.hypotheses("a").size(), 2))
	rows.append(_eq("adding an interpretation does not change the perception",
		m.evidence["a"].has("hypothesis"), false))
	rows.append(_eq("an interpretation cannot invent a perception", m.interpret("zzz", "anything"), false))
	rows.append(_eq("an empty hypothesis is refused", m.interpret("a", "  "), false))

	# --- no core-clue gate --------------------------------------------------------------
	rows.append(_eq("recording a perception is ungated by competence",
		m.record_perception({"id": "d", "channel": "social", "source": "witness",
			"observation": "the lift was out"}), true))
	rows.append(_eq("the module implements no clue procedure",
		m.get_method_list().filter(func(e): return str(e.get("name", "")).contains("clue")).size(), 0))
	rows.append(_eq("the clue authority is named, not reimplemented",
		Noosphere.CORE_CLUE_AUTHORITY, "src/rules/investigation.py"))

	# --- no second dice engine ----------------------------------------------------------
	rows.append(_eq("the module exposes no roll surface", _forbidden_surface(m), []))
	rows.append(_eq("the resolving engine is CWN", Noosphere.RESOLVING_ENGINE, "cwn"))

	# --- no duplicate psychological track -----------------------------------------------
	rows.append(_eq("no stress, psyche, harm or exposure key", _forbidden_state(m), []))
	rows.append(_eq("the exposure authority is named, not reimplemented",
		Noosphere.EXPOSURE_AUTHORITY, "src/rules/mental_load.py"))

	# --- identity is player-authored ----------------------------------------------------
	rows.append(_eq("player choice retained", m.record_choice("choice01", "refused order"), true))
	rows.append(_eq("blank choice refused", m.record_choice("", "x"), false))
	rows.append(_eq("identity is not rolled", m.to_dict().has("roll"), false))

	# --- clocks: visible, event-driven, reversible --------------------------------------
	rows.append(_eq("create threat clock", m.add_clock("nhi", "NHI cell", "disclosure"), true))
	rows.append(_eq("a six-segment clock is legal", m.clocks["nhi"]["segments"], 6))
	rows.append(_eq("a four-segment clock is legal",
		m.add_clock("local", "clinic", "quiet", 4), true))
	rows.append(_eq("a five-segment clock is not", m.add_clock("odd", "x", "y", 5), false))
	rows.append(_eq("no arbitrary ticks",
		m.change_clock("nhi", 1, "").get("reason"), "grounded_trigger_required"))
	rows.append(_eq("no multi-segment jumps",
		m.change_clock("nhi", 2, "two things at once").get("reason"), "single_step_only"))
	rows.append(_eq("clock advances for documented event",
		m.change_clock("nhi", 1, "verified leak").get("stage"), 1))
	rows.append(_eq("countermeasure reverses progress",
		m.change_clock("nhi", -1, "credible public correction", "secure corroboration").get("stage"), 0))
	rows.append(_eq("a clock cannot step below zero",
		m.change_clock("nhi", -1, "nothing left to lose").get("reason"), "clock_boundary"))
	for step in ["a", "b", "c", "d"]:
		m.change_clock("local", 1, step)
	rows.append(_eq("a four-segment clock fills at four",
		m.clocks["local"]["stage"], 4))
	rows.append(_eq("further advance beyond the last segment refused",
		m.change_clock("local", 1, "e").get("reason"), "clock_boundary"))
	rows.append(_eq("clock history records the countermeasure",
		m.clocks["nhi"]["history"][1]["countermeasure"], "secure corroboration"))
	rows.append(_eq("unknown clock refused",
		m.change_clock("nope", 1, "x").get("reason"), "unknown_clock"))

	return rows
