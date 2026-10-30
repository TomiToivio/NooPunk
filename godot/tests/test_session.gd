## End-to-end session checks for #749: the whole slice, twice, with two different solutions.
##
## The point of these checks is the acceptance criterion that the mission is completable *without*
## a fight, and that a save taken mid-mission restores the same state.
extends RefCounted

const Adapter := preload("res://godot/core/rules_adapter.gd")
const Session := preload("res://godot/core/session.gd")

const SAVE_PATH := "user://test_mvp_session.json"

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]

func _session(seed_value: int) -> NoopunkSession:
	return Session.new(Adapter.new("res://data/rules/wn_core.json", seed_value))

func run() -> Array:
	var rows: Array = []

	# --- content loads ---------------------------------------------------------------
	var s := _session(101)
	rows.append(_eq("the character record loads", s.character.get("id", ""), "romppainen"))
	rows.append(_eq("undecided player choices are marked, not invented",
		(s.character.get("choices", []) as Array).size() > 0, true))
	rows.append(_eq("the mission loads", s.mission.get("id", ""), "kallas_warehouse"))
	rows.append(_eq("the session starts at home", s.flow.location, "home"))

	# --- investigative path, no combat -----------------------------------------------
	rows.append(_eq("travel to HQ", s.travel("hq")["ok"], true))
	s.brief()
	rows.append(_eq("travel to the mission after briefing", s.travel("mission")["ok"], true))
	rows.append(_eq("the network opens on arrival", s.hacking != null, true))

	s.hack_connect("shipping")
	for _i in range(6):
		if s.hacking.alarm:
			break
		if not s.hacking.done("shipping", "query") and s.hacking.can_act("shipping", "query"):
			s.hack_act("shipping", "query")
			continue
		if not s.hacking.is_node_connected("manifest"):
			if s.hack_connect("manifest").get("reason", "") != "":
				break
			continue
		if s.hacking.can_act("manifest", "query"):
			s.hack_act("manifest", "query")
			if s.flow.achieved("manifest"):
				break
		else:
			break
	rows.append(_eq("the manifest can be reached through the network", s.flow.achieved("manifest"), true))
	rows.append(_eq("no encounter was needed", s.combat == null, true))
	rows.append(_eq("the investigative resolution is accepted", s.resolve("investigative", "success")["ok"], true))
	rows.append(_eq("the mission records its approach", s.flow.ending()["approach"], "investigative"))
	rows.append(_eq("the debrief is reachable", s.travel("debrief")["ok"], true))

	# --- save and restore --------------------------------------------------------------
	var write_err := s.save_to(SAVE_PATH)
	rows.append(_eq("the session saves", write_err, OK))
	var restored := _session(101)
	var read_err := restored.load_from(SAVE_PATH)
	rows.append(_eq("the session loads", read_err, OK))
	rows.append(_eq("the restored session is at the debrief", restored.flow.location, "debrief"))
	rows.append(_eq("the restored session keeps the resolution", restored.flow.resolved, true))
	rows.append(_eq("the restored session keeps the manifest objective",
		restored.flow.achieved("manifest"), true))
	rows.append(_eq("the restored session keeps the network state",
		restored.hacking != null and restored.hacking.connected.has("shipping"), true))

	# --- tactical path: the same mission, a fight ---------------------------------------
	var t := _session(202)
	t.travel("hq")
	t.brief()
	t.travel("mission")
	rows.append(_eq("the optional encounter starts", t.start_encounter(), true))
	var guard_present := t.combat.actors.has("guard")
	rows.append(_eq("the enemy from the mission data is in the fight", guard_present, true))

	var guard := 0
	var player_turn := false
	while not t.encounter_over() and guard < 200:
		guard += 1
		if t.combat.current_id() == "romppainen":
			var shot := t.combat_attack("romppainen", "guard")
			if not bool(shot.get("hit", false)):
				t.combat_end_turn()
			player_turn = true
		else:
			t.combat_attack(t.combat.current_id(), "romppainen")
			t.combat_end_turn()
	rows.append(_eq("the encounter reaches an end state", t.encounter_over(), true))
	rows.append(_eq("the player character acted", player_turn, true))
	rows.append(_eq("the tactical resolution is accepted", t.resolve("tactical", "success")["ok"], true))
	rows.append(_eq("the tactical approach is recorded", t.flow.ending()["approach"], "tactical"))

	# --- flow still refuses the impossible ---------------------------------------------
	var f := _session(303)
	rows.append(_eq("the mission still cannot be skipped from home",
		f.travel("mission")["reason"], "mission_is_briefed_at_hq"))

	return rows
