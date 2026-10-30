## The playable scene must at least build and drive its session without a renderer (#749).
##
## Renderer-level readability needs a windowed playtest; what can be checked headlessly is that the
## scene instantiates, owns a session, and that its input handlers produce the state changes the
## acceptance criteria depend on.
extends RefCounted

const SCENE := "res://godot/ui/mvp_game.tscn"
const Adapter := preload("res://godot/core/rules_adapter.gd")
const Session := preload("res://godot/core/session.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]

func run() -> Array:
	var rows: Array = []

	var packed := load(SCENE)
	rows.append(_eq("the MVP scene loads", packed != null, true))
	if packed == null:
		return rows

	var game = packed.instantiate()
	rows.append(_eq("the MVP scene instantiates", game != null, true))
	if game == null:
		return rows

	game._ready()
	# Replace the time-seeded session with a fixed one: a scene test that depends on the clock is
	# a flaky test, and the seed is the one thing the scene lets a caller vary.
	game.session = NoopunkSession.new(RulesAdapter.new("res://data/rules/wn_core.json", 424242))
	game._update_labels()
	rows.append(_eq("the scene owns a session", game.session != null, true))
	rows.append(_eq("a new game starts at home", game.session.flow.location, "home"))

	# walking to the exit tile and interacting moves the slice to HQ
	game.player = Vector2i(11, 7)
	game._interact()
	rows.append(_eq("the home exit reaches UNSA HQ", game.session.flow.location, "hq"))

	# the HQ interaction briefs and opens the mission
	game._interact()
	rows.append(_eq("the HQ briefing opens the mission", game.session.flow.location, "mission"))
	rows.append(_eq("the briefing flag is set", game.session.flow.briefed, true))

	# the terminal interaction opens the network
	game.player = Vector2i(1, 1)
	game._interact()
	rows.append(_eq("the terminal opens the network", game.hacking_open, true))

	# hacking the manifest through the node graph satisfies the core objective
	game.session.hack_act("shipping", "query")
	var connected_manifest: Dictionary = game.session.hack_connect("manifest")
	rows.append(_eq("the manifest node is reachable from shipping", connected_manifest.get("ok", false), true))
	for _i in range(10):
		if session_alarm(game):
			break
		game.session.hack_act("manifest", "query")
		if game.session.flow.achieved("manifest"):
			break
	rows.append(_eq("querying the manifest satisfies the core objective",
		game.session.flow.achieved("manifest"), true))

	# leaving the mission resolves and debriefs
	game.player = Vector2i(11, 7)
	game._interact()   # closes the modal network view
	game._interact()   # then leaves the mission
	rows.append(_eq("the resolved mission reaches the debrief",
		game.session.flow.location, "debrief"))
	rows.append(_eq("the debrief records the approach",
		"investigative" if game.session.flow.approach == "investigative" else "other",
		"investigative"))

	# the fight toggle is refused where there is nothing to fight
	game._toggle_fight()
	rows.append(_eq("no encounter starts in the debrief", game.session.combat == null, true))

	game.free()
	return rows

func session_alarm(game) -> bool:
	return game.session.hacking != null and game.session.hacking.alarm
