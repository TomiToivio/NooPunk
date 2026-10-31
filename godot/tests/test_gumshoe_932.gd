## GUMSHOE investigation on top of CWN: clues never gated by dice, pools for benefits only (#932).
extends RefCounted

const Gumshoe := preload("res://mods/noopunk/gumshoe_investigation.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func run() -> Array:
	var rows: Array = []

	# ---- the ability list ----------------------------------------------------
	var sheet := {"research": 3, "evidence_collection": 2, "interrogation": 1,
		"forensic_pathology": 1, "streetwise": 2, "law": 1}
	var gumshoe := Gumshoe.shipped(sheet)
	rows.append(_eq("the converted ability list loads", gumshoe.order.size(), 16))
	rows.append(_eq("a rating is taken from the sheet", gumshoe.rating("research"), 3))
	rows.append(_eq("the pool starts at the rating", gumshoe.pool("research"), 3))
	rows.append(_eq("an unbought ability exists with rating zero", gumshoe.rating("cryptography"), 0))

	# every ability names a CWN skill, so the overlay cannot demand a second skill list
	var missing: Array = []
	for ability_id in gumshoe.order:
		if gumshoe.cwn_skill_for(ability_id).is_empty():
			missing.append(ability_id)
	rows.append(_eq("every investigative ability maps to a CWN skill", missing, []))

	# ---- clues never depend on a die roll ------------------------------------
	var core: Dictionary = gumshoe.gather("research", {"id": "manifest_discrepancy", "core": true})
	rows.append(_eq("a core clue is found", core["found"], true))
	rows.append(_eq("and costs nothing", core["spent"], 0))
	rows.append(_eq("with the pool untouched", gumshoe.pool("research"), 3))

	var empty_pool := Gumshoe.shipped({"research": 1})
	empty_pool.buy_benefit("research", "extra_file", 1)
	rows.append(_eq("the pool really is empty", empty_pool.pool("research"), 0))
	rows.append(_eq("an empty pool still gathers a clue",
		empty_pool.gather("research", {"id": "anything"})["found"], true))

	var without := gumshoe.can_gather("cryptography")
	rows.append(_eq("an unbought ability cannot gather", without["ok"], false))
	rows.append(_eq("and the refusal names the CWN skill that could",
		without["cwn_skill"], "Program"))
	rows.append(_eq("an unknown ability is refused",
		gumshoe.gather("astrology", {})["reason"], "unknown_ability"))

	# ---- special benefits ---------------------------------------------------
	var bought: Dictionary = gumshoe.buy_benefit("research", "archive_photo", 1)
	rows.append(_eq("a benefit can be bought", bought["ok"], true))
	rows.append(_eq("the pool drops by the cost", bought["pool"], 2))
	rows.append(_eq("the same benefit is not sold twice",
		gumshoe.buy_benefit("research", "archive_photo", 1)["reason"], "already_bought"))
	rows.append(_eq("a benefit cannot cost zero",
		gumshoe.buy_benefit("research", "free_lunch", 0)["reason"], "illegal_cost"))
	rows.append(_eq("a benefit cannot cost three",
		gumshoe.buy_benefit("research", "extravagant", 3)["reason"], "illegal_cost"))
	rows.append(_eq("a two-point benefit is legal",
		Gumshoe.cost_is_legal(2), true))

	var poor := Gumshoe.shipped({"research": 1})
	poor.buy_benefit("research", "one", 1)
	rows.append(_eq("a benefit cannot overdraw the pool",
		poor.buy_benefit("research", "two", 1)["reason"], "pool_empty"))

	# ---- buying a benefit is never what solves the case ----------------------
	rows.append(_eq("a benefit is not a clue", bought.has("clue"), false))
	rows.append(_eq("a clue gather does not create a benefit",
		core.has("benefit"), false))

	# ---- refresh -------------------------------------------------------------
	var restored: Dictionary = gumshoe.refresh()
	rows.append(_eq("a new investigation restores the pool", restored["research"], 3))
	rows.append(_eq("and forgets the benefits", gumshoe.benefits.size(), 0))
	rows.append(_eq("after refresh the pool is full again", gumshoe.pool("research"), 3))

	# ---- no second resolution engine ----------------------------------------
	var delegated: Dictionary = Gumshoe.delegate_to_cwn(true, 0)
	rows.append(_eq("general tests stay in CWN", delegated["engine"], "cwn"))
	rows.append(_eq("the CWN result is passed through", delegated["success"], true))
	rows.append(_eq("a spend is reported without re-rolling", delegated["spent"], 0))
	rows.append(_eq("a negative spend is refused",
		Gumshoe.delegate_to_cwn(true, -1)["reason"], "negative_spend"))

	# ---- persistence ---------------------------------------------------------
	var saving := Gumshoe.shipped({"research": 3, "law": 2})
	saving.buy_benefit("research", "archive_photo", 2)
	var state: Dictionary = saving.to_dict()
	var loaded := Gumshoe.shipped({"research": 3, "law": 2})
	loaded.from_dict(state)
	rows.append(_eq("pools survive a save", loaded.pool("research"), 1))
	rows.append(_eq("benefits survive a save", loaded.benefits.has("archive_photo"), true))
	rows.append(_eq("a restored pool cannot exceed its rating", loaded.pool("law"), 2))

	var corrupt := Gumshoe.shipped({"research": 2})
	corrupt.from_dict({"pools": {"research": 99}, "benefits": []})
	rows.append(_eq("an impossible saved pool is clamped", corrupt.pool("research"), 2))

	return rows
