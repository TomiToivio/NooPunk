## The investigation console: does the table actually see and drive the GUMSHOE overlay (#932)?
##
## The screen is instantiated the way the other screen suites do it — `setup()` builds the interface and the
## handlers the buttons call are the same methods tested here. The scene file is loaded too: a Control that
## only exists in a `.tscn` nobody instantiates is not a feature.
extends RefCounted

const Screen := preload("res://godot/ui/investigation_screen.gd")
const SCENE := "res://scenes/investigation_screen.tscn"

const FULL_SHEET := {"Administer": 3, "Athletics": 3, "Connect": 3, "Drive": 3, "Exert": 3, "Fix": 3,
	"Heal": 3, "Know": 3, "Lead": 3, "Notice": 3, "Perform": 3, "Program": 3, "Punch": 3, "Shoot": 3,
	"Sneak": 3, "Stab": 3, "Survive": 3, "Talk": 3, "Trade": 3, "Work": 3}


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _screen(ranks: Dictionary = {"Notice": 0, "Know": 1}, scene: String = "entrance") -> Object:
	var screen: Object = Screen.new()
	screen.setup(ranks, scene)
	return screen


func _clue_with(screen: Object, kind: String) -> String:
	for clue in Array(screen.adapter.scene(screen.scene_id).get("clues", [])):
		if String(clue.get("kind", "")) == kind:
			return String(clue.get("id", ""))
	return ""


func run() -> Array:
	var rows: Array = []

	# --- the scene is wired into the project ---------------------------------
	rows.append(_eq("the scene file exists", ResourceLoader.exists(SCENE), true))
	var packed: PackedScene = load(SCENE)
	var instance: Node = packed.instantiate()
	rows.append(_eq("the scene instantiates with its script", instance.get_script() != null, true))
	rows.append(_eq("the scene is a Control", instance is Control, true))
	instance.free()

	# --- it reads the same case graph the adapter reads ----------------------
	var screen := _screen()
	rows.append(_eq("the case graph loads", screen.adapter.scene_ids().size() > 0, true))
	rows.append(_eq("the scene defaults to the first scene", screen.scene_id, "entrance"))
	rows.append(_eq("the overlay ships its sixteen abilities", screen.overlay.order.size(), 16))
	rows.append(_eq("a CWN rank becomes the ability's rating",
		screen.overlay.rating(screen.covering_ability("Notice")), 0))
	rows.append(_eq("the default gate is the CWN one", screen.gate, "cwn_presence"))

	# --- the guarantee: a clue is gathered without a roll and without a spend ----
	var clue_id := _clue_with(screen, "core")
	rows.append(_eq("the entrance has a core clue", clue_id.is_empty(), false))
	var gathered: Dictionary = screen.gather(clue_id)
	rows.append(_eq("a clue is gathered", bool(gathered.get("ok", false)), true))
	rows.append(_eq("gathering spends nothing", int(gathered.get("spent", -1)), 0))
	rows.append(_eq("the notebook holds the clue", screen.notebook.has(clue_id), true))
	rows.append(_eq("the gate that let it through is reported", String(gathered.get("gate", "")), "cwn_presence"))
	rows.append(_eq("gathering the same clue twice is refused",
		String(screen.gather(clue_id).get("reason", "")), "already_found"))

	# --- the open ruling is a visible switch, not a silent choice -------------
	var strict := _screen({"Notice": 0, "Know": 0})
	strict._on_gate(1)
	rows.append(_eq("the SRD gate is selected", strict.gate, "srd_rating"))
	rows.append(_eq("under the SRD gate a rank-0 mapping covers nothing",
		strict.covering_ability("Notice"), ""))
	var refused: Dictionary = strict.gather(clue_id)
	rows.append(_eq("under the SRD gate the clue is refused", bool(refused.get("ok", true)), false))
	rows.append(_eq("and the reason names the rating",
		String(refused.get("reason", "")), "rating_below_one"))
	rows.append(_eq("a refused clue does not enter the notebook", strict.notebook.has(clue_id), false))
	strict._on_gate(0)
	rows.append(_eq("under the CWN gate the same rank-0 mapping does cover it",
		strict.covering_ability("Notice").is_empty(), false))
	rows.append(_eq("and the same scene now yields the clue",
		bool(strict.gather(clue_id).get("ok", false)), true))

	# --- a competency with no mapped ability: reachable by CWN, not by the SRD -
	var survivor := _screen({"Survive": 2}, "entrance")
	var survive_clue := ""
	for clue in Array(survivor.adapter.scene("entrance").get("clues", [])):
		if String(clue.get("competency", "")) == "Survive":
			survive_clue = String(clue.get("id", ""))
	rows.append(_eq("the shipped case asks for a competency no ability maps", survive_clue.is_empty(), false))
	rows.append(_eq("no investigative ability maps Survive", survivor.covering_ability("Survive"), ""))
	var survive_gathered: Dictionary = survivor.gather(survive_clue)
	rows.append(_eq("the CWN gate still permits it", bool(survive_gathered.get("ok", false)), true))
	rows.append(_eq("and says it came through the CWN skill, not an ability",
		String(survive_gathered.get("ability", "x")), ""))
	var survive_strict := _screen({"Survive": 2}, "entrance")
	survive_strict._on_gate(1)
	rows.append(_eq("the SRD gate refuses it",
		String(survive_strict.gather(survive_clue).get("reason", "")), "rating_below_one"))

	# --- a benefit is never a clue -------------------------------------------
	var buyer := _screen({"Notice": 3}, "entrance")
	var ability := String(buyer.covering_ability("Notice"))
	var found_before: int = buyer.notebook.count()
	var bought: Dictionary = buyer.buy_benefit(ability, "a CCTV frame the team can read", 1)
	rows.append(_eq("a legal benefit is bought", bool(bought.get("ok", false)), true))
	rows.append(_eq("it costs exactly what was asked", int(bought.get("spent", 0)), 1))
	rows.append(_eq("the pool drops by the cost", int(bought.get("pool", -1)), 2))
	rows.append(_eq("the notebook is untouched by a benefit", buyer.notebook.count(), found_before))
	rows.append(_eq("and the screen measures that rather than claiming it",
		bool(bought.get("touched_notebook", true)), false))

	# --- the SRD's cost bounds and the pool's floor --------------------------
	rows.append(_eq("a benefit cannot be bought twice",
		String(buyer.buy_benefit(ability, "a CCTV frame the team can read", 1).get("reason", "")),
		"already_bought"))
	rows.append(_eq("a 3-point benefit is refused",
		String(buyer.buy_benefit(ability, "another", 3).get("reason", "")), "illegal_cost"))
	rows.append(_eq("a 0-point benefit is refused",
		String(buyer.buy_benefit(ability, "third", 0).get("reason", "")), "illegal_cost"))
	rows.append(_eq("a second benefit drains the pool", int(
		buyer.buy_benefit(ability, "a second", 2).get("pool", -1)), 0))
	rows.append(_eq("an empty pool refuses the next purchase",
		String(buyer.buy_benefit(ability, "a fourth", 1).get("reason", "")), "pool_empty"))

	# --- a new investigation restores the pools ------------------------------
	buyer.refresh_pools()
	rows.append(_eq("the pool is restored to the rating", buyer.overlay.pool(ability), 3))

	# --- the case keeps its own record ---------------------------------------
	rows.append(_eq("an unfinished case cannot be concluded", buyer.notebook.can_conclude(), false))
	rows.append(_eq("missing essential clues are named", buyer.notebook.missing_essential().is_empty(), false))

	# --- persistence lives beside the core save, not inside it ---------------
	var saved := _screen({"Notice": 1}, "entrance")
	var saved_clue := _clue_with(saved, "core")
	saved.gather(saved_clue)
	saved.save_state()
	var reloaded := _screen({"Notice": 0, "Know": 0}, "entrance")
	rows.append(_eq("the state file loads", reloaded.load_state(), true))
	rows.append(_eq("the found clue survives the round trip", reloaded.notebook.has(saved_clue), true))
	rows.append(_eq("and the rating survives with it",
		reloaded.overlay.rating(saved.covering_ability("Notice")), 1))
	DirAccess.remove_absolute(ProjectSettings.globalize_path(Screen.SAVE_PATH))

	# --- the shipped case, walked with a full CWN sheet -----------------------
	var everywhere := _screen(FULL_SHEET, "entrance")
	var refused_clues: Array = []
	for i in range(everywhere.adapter.scene_ids().size()):
		everywhere._on_scene(i)
		for clue in Array(everywhere.adapter.scene(everywhere.scene_id).get("clues", [])):
			if not bool(everywhere.permits(String(clue.get("id", ""))).get("ok", false)):
				refused_clues.append("%s/%s" % [everywhere.scene_id, clue.get("id", "")])
	rows.append(_eq("a full CWN sheet is refused no clue in the shipped case", refused_clues, []))
	rows.append(_eq("one competency has no investigative ability behind it",
		everywhere.uncovered_competencies(), ["Survive"]))

	return rows
