## Layout geometry for portraits and social encounters (#908).
##
## Pure functions of (viewport size, art aspect). No nodes, no theme, no drawing — so the rules can be
## asserted headlessly instead of judged by eye on one monitor at one resolution.
##
## The rules:
## * everything sits inside a safe area, so UI never runs into a bezel or a TV's overscan;
## * an image keeps its aspect ratio — **a face is never cropped to make a frame prettier**;
## * a caption sits below its portrait and does not overlap it;
## * in an encounter the portrait and the dialogue panel do not overlap, at any aspect we support.
extends RefCounted
class_name NoopunkImageLayout

##: Fraction of the smaller viewport dimension kept clear on every edge.
const SAFE_MARGIN := 0.05
##: Caption strip height as a fraction of viewport height.
const CAPTION_HEIGHT := 0.09
##: Gap between panels, as a fraction of viewport width.
const GAP := 0.03
##: Portrait width in an encounter, as a fraction of the safe area width.
const ENCOUNTER_PORTRAIT_WIDTH := 0.34


static func safe_rect(viewport: Vector2) -> Rect2:
	var margin: float = minf(viewport.x, viewport.y) * SAFE_MARGIN
	return Rect2(Vector2(margin, margin), viewport - Vector2(margin, margin) * 2.0)


## Largest rect of `aspect` (width / height) that fits inside `into`, centred.
static func fit(aspect: float, into: Rect2) -> Rect2:
	if aspect <= 0.0 or into.size.x <= 0.0 or into.size.y <= 0.0:
		return Rect2()
	var width := into.size.x
	var height := width / aspect
	if height > into.size.y:
		height = into.size.y
		width = height * aspect
	var origin := into.position + (into.size - Vector2(width, height)) * 0.5
	return Rect2(origin, Vector2(width, height))


## Portrait page: image above, caption below. Both inside the safe area.
static func portrait_frame(viewport: Vector2, aspect: float = 3.0 / 4.0) -> Dictionary:
	var safe := safe_rect(viewport)
	var caption_h := viewport.y * CAPTION_HEIGHT
	var image_area := Rect2(safe.position,
		Vector2(safe.size.x, maxf(safe.size.y - caption_h - viewport.y * GAP, 1.0)))
	var image := fit(aspect, image_area)
	var caption := Rect2(
		Vector2(safe.position.x, image.position.y + image.size.y + viewport.y * GAP),
		Vector2(safe.size.x, caption_h))
	return {"image": image, "caption": caption, "safe": safe, "problems": _check(viewport, image, caption, aspect)}


## Social encounter: background fills the safe area, portrait inset on the left, dialogue on the right.
static func encounter_frame(viewport: Vector2, background_aspect: float = 4.0 / 3.0,
		portrait_aspect: float = 3.0 / 4.0) -> Dictionary:
	var safe := safe_rect(viewport)
	var background := fit(background_aspect, safe)
	var portrait_width := safe.size.x * ENCOUNTER_PORTRAIT_WIDTH
	var portrait_height := minf(portrait_width / portrait_aspect, safe.size.y * 0.62)
	portrait_width = portrait_height * portrait_aspect
	var portrait := Rect2(
		Vector2(safe.position.x, safe.position.y + safe.size.y - portrait_height),
		Vector2(portrait_width, portrait_height))
	var dialogue := Rect2(
		Vector2(portrait.position.x + portrait.size.x + viewport.x * GAP,
			safe.position.y + safe.size.y * 0.38),
		Vector2(
			safe.position.x + safe.size.x - (portrait.position.x + portrait.size.x + viewport.x * GAP),
			safe.size.y * 0.58))
	var problems := _check(viewport, portrait, dialogue, portrait_aspect)
	if portrait.intersects(dialogue):
		problems.append("portrait overlaps the dialogue panel")
	if dialogue.size.x <= 0.0:
		problems.append("no room for dialogue beside the portrait")
	return {"background": background, "portrait": portrait, "dialogue": dialogue,
		"safe": safe, "problems": problems}


static func _check(viewport: Vector2, image: Rect2, other: Rect2, aspect: float) -> Array:
	var problems: Array = []
	var safe := safe_rect(viewport)
	if not safe.encloses(image):
		problems.append("image leaves the safe area")
	if not safe.encloses(other):
		problems.append("text panel leaves the safe area")
	if image.size.y > 0.0:
		var actual: float = image.size.x / image.size.y
		if absf(actual - aspect) > 0.01:
			problems.append("aspect changed: %.3f vs %.3f" % [actual, aspect])
	if image.intersects(other):
		problems.append("image overlaps its text panel")
	return problems
