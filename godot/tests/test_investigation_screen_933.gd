## Investigation screen: the clue arrives, the pool pays for advantages (#933).
extends RefCounted

const Gumshoe := preload("res://mods/noopunk/gumshoe_investigation.gd")
const Screen := preload("res://godot/ui/investigation_screen.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _scene() -> Dictionary:
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/world/investigation_scene_intake.json"))
	return parsed if parsed is Dictionary else {}


func run() -> Array:
	var rows: Array = []

	# ---- ratings come from the CWN sheet, not a second economy ---------------
	var sheet := {"skills": {"Administer": 0, "Talk": 2, "Notice": -1}}
	var ratings: Dictionary = Gumshoe.ratings_from_sheet(sheet)
	rows.append(_eq("a trained skill at rank 0 becomes rating 1", ratings["bureaucracy"], 1))
	rows.append(_eq("rank 2 becomes rating 3", ratings["reassurance"], 3))
	rows.append(_eq("an untrained skill becomes rating 0", ratings["evidence_collection"], 0))
	rows.append(_eq("an absent skill is untrained, not an error", ratings["research"], 0))
	rows.append(_eq("every converted ability gets a rating", ratings.size(), 16))

	var built := Gumshoe.from_sheet(sheet)
	rows.append(_eq("the overlay builds from a sheet", built.rating("bureaucracy"), 1))
	rows.append(_eq("and the pool starts at the rating", built.pool("bureaucracy"), 1))

	# ---- the screen ----------------------------------------------------------
	var screen: Object = Screen.new()
	screen.setup(sheet, _scene())
	rows.append(_eq("the screen names the scene", screen._title.text, "UNSA intake records"))
	# One trained CWN skill covers several investigative angles (Administer -> bureaucracy, law,
	# textual analysis), so the menu lists every ability the sheet already pays for — not a second economy.
	var offered := 0
	for ability_id in screen.gumshoe.order:
		if screen.gumshoe.rating(ability_id) >= 1:
			offered += 1
	rows.append(_eq("the menu offers exactly the abilities the sheet pays for",
		screen._abilities.get_child_count(), offered))
	rows.append(_eq("and the untrained skill's ability is not on it",
		screen.gumshoe.rating("evidence_collection"), 0))

	# gather the core clue: no roll, no spend
	screen._gather("bureaucracy")
	rows.append(_eq("the core clue is found", screen.found.has("intake_discrepancy"), true))
	rows.append(_eq("gathering costs no pool", screen.gumshoe.pool("bureaucracy"), 1))
	rows.append(_eq("and the log says what was learned",
		screen._log.text.contains("referral date"), true))
	rows.append(_eq("the clue is not found twice", screen.found.size(), 1))

	# an ability with nothing in this scene says so
	screen._gather("reassurance")
	rows.append(_eq("a second ability finds its own clue", screen.found.has("clerk_note"), true))

	# ---- benefits spend, and only spend -------------------------------------
	var poor := Gumshoe.from_sheet({"skills": {"Administer": 0}})
	rows.append(_eq("a 1-point benefit is affordable with pool 1", poor.pool("bureaucracy"), 1))
	var bought: Dictionary = poor.buy_benefit("bureaucracy", "metadata_copy", 1)
	rows.append(_eq("the benefit is bought", bought["ok"], true))
	rows.append(_eq("the pool drops", poor.pool("bureaucracy"), 0))
	rows.append(_eq("and the clue still gathers with an empty pool",
		poor.gather("bureaucracy", {"id": "intake_discrepancy", "core": true})["found"], true))

	# the screen disables an unaffordable benefit instead of failing on click
	var screen2: Object = Screen.new()
	screen2.setup({"skills": {"Administer": 0, "Talk": 0}}, _scene())
	var disabled := 0
	for child in screen2._benefits.get_children():
		if child is Button and bool(child.disabled):
			disabled += 1
	rows.append(_eq("a 2-point benefit is disabled when the pool cannot pay", disabled >= 1, true))

	# ---- refresh -------------------------------------------------------------
	var refreshed: Dictionary = screen.gumshoe.refresh()
	rows.append(_eq("a new investigation restores pools", refreshed["bureaucracy"], 1))
	rows.append(_eq("and clears the benefits", screen.gumshoe.benefits.size(), 0))
	screen.free()
	screen2.free()

	# ---- the fixture is data, and it is coherent ----------------------------
	var scene := _scene()
	var abilities: Array = []
	for clue in Array(scene.get("clues", [])):
		abilities.append(String(clue.get("ability", "")))
	rows.append(_eq("the fixture has a core clue", Array(scene.get("clues", [])).size(), 2))
	var known := 0
	for ability_id in abilities:
		if built.abilities.has(ability_id):
			known += 1
	rows.append(_eq("every clue names a converted ability", known, abilities.size()))

	return rows
