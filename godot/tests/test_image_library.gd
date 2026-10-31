extends RefCounted

## #908: one place for art, four classes, and a stated placeholder instead of an empty frame.
const Library := preload("res://godot/core/image_library.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	rows.append(_eq("four canonical classes", Library.CLASSES.size(), 4))
	rows.append(_eq("portraits is canonical", Library.is_canonical("characters/portraits"), true))
	rows.append(_eq("an invented folder is not", Library.is_canonical("misc"), false))

	rows.append(_eq("portrait path",
		Library.path_for("characters/portraits", "romppainen"),
		"res://images/characters/portraits/romppainen.png"))
	rows.append(_eq("location path",
		Library.path_for("locations", "harbour"),
		"res://images/locations/harbour.png"))

	# ids are slugs; traversal and spaces are refused rather than normalised into a path
	rows.append(_eq("path traversal refused", Library.path_for("locations", "../secret"), ""))
	rows.append(_eq("spaces refused", Library.path_for("locations", "har bour"), ""))
	rows.append(_eq("empty id refused", Library.path_for("locations", "   "), ""))

	# a missing asset is a stated condition, never a silently broken path
	var missing := Library.resolve("events", "first_contact")
	rows.append(_eq("missing asset is not found", missing["found"], false))
	rows.append(["missing asset explains itself",
		String(missing["reason"]).contains("placeholder"), String(missing["reason"])])
	rows.append(_eq("missing asset hands back no path", missing["path"], ""))

	rows.append(_eq("unknown class cannot resolve", Library.resolve("nowhere", "x")["found"], false))

	# reference material is internal only
	rows.append(_eq("reference is non-committable", Library.committed_photography_refused("reference"), true))
	rows.append(_eq("portraits are committable", Library.committed_photography_refused("characters/portraits"), false))

	# variants are suffixes, not subdirectories
	rows.append(_eq("day/night variant id", Library.variant("harbour", "night"), "harbour_night"))
	rows.append(_eq("variant refuses an empty name", Library.variant("harbour", ""), ""))

	return rows
