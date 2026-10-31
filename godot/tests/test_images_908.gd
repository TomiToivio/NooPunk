## The image pipeline: manifest, textures, and the layout rules that keep faces on screen (#908).
extends RefCounted

const Library := preload("res://godot/core/image_library.gd")
const Layout := preload("res://godot/ui/image_layout.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _close(name: String, actual: float, expected: float, tolerance: float = 0.01) -> Array:
	return [name, absf(actual - expected) <= tolerance,
		"got %.4f; expected %.4f (+/- %.4f)" % [actual, expected, tolerance]]


func run() -> Array:
	var rows: Array = []
	var library := Library.from_manifest()
	rows.append(_eq("the manifest loads", library.entries.size(), 4))
	rows.append(_eq("loading reports no problems", library.problems.size(), 0))

	var portrait := library.texture_by_id("probe_portrait")
	rows.append(_eq("a texture loads by id", portrait != null, true))
	if portrait != null:
		rows.append(_eq("the texture has the declared size", portrait.get_size(), Vector2(600, 800)))

	rows.append(_eq("an unknown id returns null", library.texture_by_id("no_such_asset"), null))
	rows.append(_eq("and says why", library.problems.size() > 0, true))

	# stretch policy comes from the asset class, not from each screen
	rows.append(_eq("portraits letterbox instead of cropping",
		Library.stretch_mode_for("characters/portraits"), TextureRect.STRETCH_KEEP_ASPECT_CENTERED))
	rows.append(_eq("locations may fill the frame",
		Library.stretch_mode_for("locations"), TextureRect.STRETCH_KEEP_ASPECT_COVERED))

	var rect := TextureRect.new()
	rect.expand_mode = TextureRect.EXPAND_KEEP_SIZE
	rows.append(_eq("apply_to succeeds", library.apply_to(rect, "probe_portrait"), true))
	rows.append(_eq("apply_to sets the stretch policy",
		rect.stretch_mode, TextureRect.STRETCH_KEEP_ASPECT_CENTERED))
	rows.append(_eq("apply_to lets the rect own its size",
		rect.expand_mode, TextureRect.EXPAND_IGNORE_SIZE))
	rows.append(_eq("apply_to refuses an unknown id", library.apply_to(rect, "nope"), false))
	rect.free()

	# ---- portrait layout ----------------------------------------------------
	var sizes: Array = [Vector2(1280, 720), Vector2(1920, 1080), Vector2(1024, 768), Vector2(800, 600)]
	for size in sizes:
		var frame: Dictionary = Layout.portrait_frame(size)
		rows.append(_eq("portrait layout has no problems at %dx%d" % [int(size.x), int(size.y)],
			frame["problems"], []))
		rows.append(_close("portrait keeps 3:4 at %dx%d" % [int(size.x), int(size.y)],
			frame["image"].size.x / frame["image"].size.y, 0.75))
		rows.append(_eq("the caption sits below the image at %dx%d" % [int(size.x), int(size.y)],
			frame["caption"].position.y >= frame["image"].position.y + frame["image"].size.y, true))

	# ---- encounter layout ---------------------------------------------------
	for size in sizes:
		var frame: Dictionary = Layout.encounter_frame(size)
		rows.append(_eq("encounter layout has no problems at %dx%d" % [int(size.x), int(size.y)],
			frame["problems"], []))
		rows.append(_eq("portrait and dialogue never overlap at %dx%d" % [int(size.x), int(size.y)],
			frame["portrait"].intersects(frame["dialogue"]), false))
		rows.append(_eq("the portrait keeps 3:4 at %dx%d" % [int(size.x), int(size.y)],
			absf(frame["portrait"].size.x / frame["portrait"].size.y - 0.75) < 0.01, true))
		rows.append(_eq("the background keeps its aspect at %dx%d" % [int(size.x), int(size.y)],
			absf(frame["background"].size.x / frame["background"].size.y - 4.0 / 3.0) < 0.01, true))

	# a safe area that never touches the viewport edge
	var safe: Rect2 = Layout.safe_rect(Vector2(1280, 720))
	rows.append(_eq("the safe area is inset from the edge",
		safe.position.x > 0.0 and safe.position.y > 0.0, true))

	# a degenerate viewport must not produce negative rects
	var tiny: Dictionary = Layout.portrait_frame(Vector2(64, 48))
	rows.append(_eq("a tiny viewport does not crash the layout", tiny.has("image"), true))
	rows.append(_eq("and its image is not inverted", tiny["image"].size.x >= 0.0, true))

	return rows
