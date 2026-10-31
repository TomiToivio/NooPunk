## The layout maths that keeps faces on screen (#908).
##
## Geometry only: no manifest, no files, no artwork. That is deliberate — the rules that decide whether a
## portrait is cropped must be testable on a machine that has never been sent a single image.
extends RefCounted

const Layout := preload("res://godot/ui/image_layout.gd")


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _close(name: String, actual: float, expected: float, tolerance: float = 0.01) -> Array:
	return [name, absf(actual - expected) <= tolerance,
		"got %.4f; expected %.4f (+/- %.4f)" % [actual, expected, tolerance]]


func run() -> Array:
	var rows: Array = []
	# the classic resolutions plus one awkward one
	var sizes: Array = [Vector2(1280, 720), Vector2(1920, 1080), Vector2(1024, 768), Vector2(800, 600)]

	for size in sizes:
		var tag := "%dx%d" % [int(size.x), int(size.y)]

		# ---- portrait page ------------------------------------------------
		var portrait: Dictionary = Layout.portrait_frame(size)
		rows.append(_eq("portrait layout has no problems at " + tag, portrait["problems"], []))
		rows.append(_close("portrait keeps 3:4 at " + tag,
			portrait["image"].size.x / portrait["image"].size.y, 0.75))
		rows.append(_eq("the caption sits below the image at " + tag,
			portrait["caption"].position.y >= portrait["image"].position.y + portrait["image"].size.y,
			true))
		rows.append(_eq("the image stays inside the safe area at " + tag,
			portrait["safe"].encloses(portrait["image"]), true))

		# a 2:3 portrait must letterbox differently, not crop
		var tall: Dictionary = Layout.portrait_frame(size, 2.0 / 3.0)
		rows.append(_close("2:3 portraits keep their aspect at " + tag,
			tall["image"].size.x / tall["image"].size.y, 2.0 / 3.0))

		# ---- social encounter ---------------------------------------------
		var encounter: Dictionary = Layout.encounter_frame(size)
		rows.append(_eq("encounter layout has no problems at " + tag, encounter["problems"], []))
		rows.append(_eq("portrait and dialogue never overlap at " + tag,
			encounter["portrait"].intersects(encounter["dialogue"]), false))
		rows.append(_eq("the portrait keeps 3:4 at " + tag,
			absf(encounter["portrait"].size.x / encounter["portrait"].size.y - 0.75) < 0.01, true))
		rows.append(_eq("the background keeps 4:3 at " + tag,
			absf(encounter["background"].size.x / encounter["background"].size.y - 4.0 / 3.0) < 0.01,
			true))
		rows.append(_eq("the dialogue panel has room for text at " + tag,
			encounter["dialogue"].size.x > size.x * 0.25, true))
		rows.append(_eq("everything stays inside the safe area at " + tag,
			encounter["safe"].encloses(encounter["portrait"])
				and encounter["safe"].encloses(encounter["dialogue"]), true))

	# ---- safe area ------------------------------------------------------
	var safe: Rect2 = Layout.safe_rect(Vector2(1280, 720))
	rows.append(_eq("the safe area is inset from every edge",
		safe.position.x > 0.0 and safe.position.y > 0.0
			and safe.end.x < 1280.0 and safe.end.y < 720.0, true))
	rows.append(_eq("the safe area is symmetric about the centre",
		absf(safe.position.x - (1280.0 - safe.end.x)) < 0.01, true))

	# ---- degenerate inputs ----------------------------------------------
	var tiny: Dictionary = Layout.portrait_frame(Vector2(64, 48))
	rows.append(_eq("a tiny viewport does not crash the layout", tiny.has("image"), true))
	rows.append(_eq("and its image is not inverted", tiny["image"].size.x >= 0.0, true))

	var nonsense: Rect2 = Layout.fit(0.0, Rect2(0, 0, 100, 100))
	rows.append(_eq("a zero aspect returns an empty rect rather than dividing by zero",
		nonsense, Rect2()))

	return rows
