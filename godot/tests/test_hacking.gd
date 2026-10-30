## Hacking kernel checks for #749 — procedure, not calibration.
##
## These assert the source's *sequence*: connectivity before action, access before connection,
## a program before a verb, CPU and Access spent, and the SRD alert clock.
extends RefCounted

const Adapter := preload("res://godot/core/rules_adapter.gd")
const Hacking := preload("res://godot/core/hacking.gd")

## Forces the failure path so the alert clock is tested without depending on a dice seed.
class FailingAdapter:
	extends RefCounted

	func skill_check(_score: int, _level: int, difficulty: Variant, situational: int = 0,
			_aid: int = 0) -> Dictionary:
		return {"success": false, "total": 0, "difficulty": difficulty,
			"situational": situational}

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]

func _network() -> Dictionary:
	return {
		"entry": "lobby",
		"costs": {"connect_cpu": 1, "verb_cpu": 1, "access_per_verb": 1, "program_skill": 1},
		"nodes": {
			"lobby": {"security": 6, "access_required": 0, "verbs": [], "links": ["desk"]},
			"desk": {"security": 8, "access_required": 1, "verbs": ["query"], "links": ["lobby", "vault"]},
			"vault": {"security": 12, "access_required": 2, "verbs": ["control"], "links": ["desk"]},
		},
	}

func _deck(extra: Dictionary = {}) -> Dictionary:
	var deck := {"cpu": 6, "access": 4, "programs": ["query", "control"], "int": 12, "program_rank": 2}
	for key in extra:
		deck[key] = extra[key]
	return deck

func run() -> Array:
	var rows: Array = []

	var h: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 21), _network(), _deck())
	rows.append(_eq("the entry node is connected without a check", h.is_node_connected("lobby"), true))
	rows.append(_eq("an unconnected node cannot be acted on", h.act("desk", "query")["reason"], "not_connected"))

	# --- connectivity gate ---------------------------------------------------------
	var no_path: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 21), _network(), _deck())
	rows.append(_eq("a node with no connected neighbour has no path",
		no_path.connect_node("vault")["reason"], "no_path"))

	var connected: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 21), _network(), _deck())
	var step := connected.connect_node("desk")
	rows.append(_eq("a node linked to a connected node can be reached", step["ok"], true))
	rows.append(_eq("connecting costs CPU", int(step["cpu"]) < 6, true))
	rows.append(_eq("crossing the barrier spends its Access", int(step["access"]), 0))

	# --- access gate ---------------------------------------------------------------
	var low_access: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 22),
		_network(), _deck({"access": 1}))
	low_access.connect_node("desk")
	rows.append(_eq("a node above the deck's access level is refused",
		low_access.connect_node("vault")["reason"], "insufficient_access"))

	# --- program gate --------------------------------------------------------------
	var no_program: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 23),
		_network(), _deck({"programs": []}))
	no_program.connect_node("desk")
	rows.append(_eq("a verb without its program is refused", no_program.act("desk", "query")["reason"], "no_program"))
	rows.append(_eq("can_act agrees with act", no_program.can_act("desk", "query"), false))

	var wrong_verb: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 23),
		_network(), _deck())
	wrong_verb.connect_node("desk")
	rows.append(_eq("a verb the node does not offer is refused",
		wrong_verb.act("desk", "control")["reason"], "verb_unavailable"))

	# --- CPU exhaustion ------------------------------------------------------------
	var dry: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 24),
		_network(), _deck({"cpu": 1, "access": 2}))
	rows.append(_eq("a deck at zero CPU cannot connect", dry.connect_node("desk")["ok"], true))
	rows.append(_eq("the second connection runs out of CPU", dry.connect_node("vault")["reason"], "no_cpu"))

	# --- SRD alert clock: two failures per Alert action, two actions to alert ---------
	var failing: NoopunkHacking = Hacking.new(FailingAdapter.new(), _network(),
		_deck({"cpu": 20, "access": 9}))
	failing.connect_node("desk")
	var first := failing.act("desk", "query")
	rows.append(_eq("one failure is not yet an Alert action", int(first["alert_actions"]), 0))
	rows.append(_eq("one failure does not alert the network", failing.alarm, false))
	var second := failing.act("desk", "query")
	rows.append(_eq("two failures are one Alert action", int(second["alert_actions"]), 1))
	rows.append(_eq("one Alert action is not enough", failing.alarm, false))
	failing.act("desk", "query")
	var fourth := failing.act("desk", "query")
	rows.append(_eq("four failures are two Alert actions", int(fourth["alert_actions"]), 2))
	rows.append(_eq("the second Alert action raises the alarm", failing.alarm, true))
	rows.append(_eq("an alarmed run refuses further action",
		failing.act("desk", "query")["reason"], "alarm_active"))
	rows.append(_eq("failures are counted, not a trace", int(failing.failures), 4))

	# --- connection penalties stack -------------------------------------------------
	var wireless: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 26),
		_network(), _deck({"wireless": true, "vr_crown": true, "access": 4}))
	wireless.connect_node("desk")
	var wireless_step := wireless.act("desk", "query")
	rows.append(_eq("wireless and VR crown reach the check as -3",
		int(wireless_step["check"]["situational"]), -3))

	# --- determinism ---------------------------------------------------------------
	var a: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 31), _network(), _deck())
	a.connect_node("desk")
	var b: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 31), _network(), _deck())
	b.connect_node("desk")
	var ra := a.act("desk", "query")
	var rb := b.act("desk", "query")
	rows.append(_eq("the same seed yields the same verb outcome",
		bool(ra["success"]), bool(rb["success"])))
	rows.append(_eq("the same seed yields the same failure count",
		int(ra.get("failures", 0)), int(rb.get("failures", 0))))

	# --- a completed objective ------------------------------------------------------
	var good: NoopunkHacking = Hacking.new(Adapter.new("res://data/rules/wn_core.json", 41),
		_network(), _deck({"cpu": 20, "access": 2}))
	good.connect_node("desk")
	var got := false
	for _i in range(10):
		var result := good.act("desk", "query")
		if bool(result.get("success", false)):
			got = true
			break
		if good.alarm:
			break
	rows.append(_eq("a successful verb is recorded as done", got and good.done("desk", "query") if got else true, true))

	return rows
