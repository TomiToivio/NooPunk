## The narrative foundation: location graph, clue notebook, token-driven theme (#897 §4).
##
## These are the pieces a location-based CRPG stands on. The rules they encode are the ones the issue
## names explicitly: travel discovers nothing by itself, and an essential clue is never lost to one roll.
extends RefCounted

const Invest := preload("res://godot/narrative/investigation.gd")
const Tokens := preload("res://godot/ui/noopunk_theme.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _notebook() -> Object:
	var file := FileAccess.open("res://data/world/lakkahaltia_clues.json", FileAccess.READ)
	var data: Variant = JSON.parse_string(file.get_as_text()) if file != null else {}
	return Invest.from_data(data if data is Dictionary else {})


func run() -> Array:
	var rows: Array = []

	# ---- investigation notebook ---------------------------------------------
	var opened := {"case_opened": true, "met_informant": true, "injury_known": true}
	var book := _notebook()
	rows.append(_eq("the clue graph loads", book.clues.size(), 5))
	rows.append(_eq("an unknown clue is refused", book.gather("nope", true)["ok"], false))
	rows.append(_eq("requirements are enforced",
		book.gather("manifest_discrepancy", true, {})["reason"], "requirements_not_met"))

	var essential_miss: Dictionary = book.gather("manifest_discrepancy", false, opened)
	rows.append(_eq("an essential clue is granted on a failed roll", essential_miss["found"], true))
	rows.append(_eq("and the failure is not hidden", essential_miss["owes_complication"], true))
	rows.append(_eq("it still opens its lead", book.has("manifest_discrepancy"), true))
	rows.append(_eq("the lead is recorded", book.open_leads().has("container_yard"), true))

	var optional := _notebook()
	rows.append(_eq("a non-essential clue can be missed",
		optional.gather("official_manifest", false, opened)["found"], false))
	rows.append(_eq("a missed clue is not in the notebook", optional.has("official_manifest"), false))
	rows.append(_eq("a non-essential clue is found on success",
		optional.gather("official_manifest", true, opened)["found"], true))

	rows.append(_eq("the same clue cannot be gathered twice",
		book.gather("manifest_discrepancy", true, opened)["reason"], "already_found"))

	var case := _notebook()
	rows.append(_eq("a case is not closable with essentials missing", case.can_conclude(), false))
	rows.append(_eq("missing essentials are listed", case.missing_essential(),
		["manifest_discrepancy", "witness_account"]))
	case.gather("manifest_discrepancy", true, opened)
	case.gather("witness_account", true, opened)
	rows.append(_eq("with every essential clue the case can close", case.can_conclude(), true))
	rows.append(_eq("non-essential clues stay optional", case.has("official_manifest"), false))

	# ---- theme from tokens --------------------------------------------------
	var theme_builder := Tokens.new()
	var colors: Dictionary = theme_builder.palette()
	rows.append(_eq("tokens load", colors.size() >= 6, true))
	rows.append(_eq("tokens are colours, not prose", theme_builder.problems.is_empty(), true))
	var built: Theme = theme_builder.build()
	rows.append(_eq("a theme is produced", built != null, true))
	rows.append(_eq("labels get a token colour",
		built.has_color("font_color", "Label"), true))
	rows.append(_eq("an unknown role is loud, not silent",
		theme_builder.color("no_such_role"), Color.MAGENTA))

	return rows


