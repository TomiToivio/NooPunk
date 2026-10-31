extends RefCounted
class_name ImageLibrary
## Resolves art assets for the four canonical classes (#908).
##
## The library exists so that "where does this picture live" has one answer, and so a missing asset is a
## *stated* condition rather than a blank rectangle. A scene asks for `characters/portraits/romppainen`
## and gets either a path that exists or a placeholder verdict with a reason.
##
## Two rules are enforced here rather than documented and hoped for:
##
## * **Only the four canonical classes**, because a fifth invented folder is how a project ends up with
##   art in six places and no idea which one ships.
## * **`reference/` holds no committed photography.** That folder is for consent-controlled internal
##   references; the repository is public, and a real photograph of a person is not ours to publish.

const ROOT := "res://images"

##: Canonical asset classes. Order is display order in any picker.
const CLASSES := ["characters/portraits", "social_encounters", "locations", "events"]

##: Extensions tried in order. PNG first because it carries transparency.
const EXTENSIONS := ["png", "webp", "jpg"]

##: Classes that must never contain committed photographic material.
const NON_COMMITTABLE := ["reference"]


static func is_canonical(klass: String) -> bool:
	## Named `is_canonical`, not `is_class`: `is_class` is an Object built-in and shadows badly.
	return klass in CLASSES


static func _clean_id(id: String) -> String:
	## Ids are lowercase slugs. Anything else is refused rather than silently normalised into a path that
	## might traverse out of the images tree.
	var cleaned := id.strip_edges().to_lower()
	if cleaned.is_empty():
		return ""
	for bad in ["..", "/", "\\", " "]:
		if cleaned.contains(bad):
			return ""
	return cleaned


static func path_for(klass: String, id: String) -> String:
	if not is_canonical(klass):
		return ""
	var clean := _clean_id(id)
	if clean.is_empty():
		return ""
	return "%s/%s/%s.png" % [ROOT, klass, clean]


static func resolve(klass: String, id: String) -> Dictionary:
	## `found` is true only when a file exists. When it is false the caller must decide what to show; the
	## library will not hand back a broken path and let the scene display nothing without explanation.
	if not is_canonical(klass):
		return {"found": false, "path": "", "reason": "unknown asset class: %s" % klass}
	var clean := _clean_id(id)
	if clean.is_empty():
		return {"found": false, "path": "", "reason": "invalid asset id: %s" % id}
	for ext in EXTENSIONS:
		var candidate := "%s/%s/%s.%s" % [ROOT, klass, clean, ext]
		if ResourceLoader.exists(candidate) or FileAccess.file_exists(candidate):
			return {"found": true, "path": candidate, "reason": ""}
	return {
		"found": false,
		"path": "",
		"reason": "no art for %s/%s yet — the scene must show a stated placeholder, not an empty frame"
			% [klass, clean],
	}


static func committed_photography_refused(klass: String) -> bool:
	## True when this class must reject image files outright.
	return klass in NON_COMMITTABLE


static func variant(base_id: String, variant_name: String) -> String:
	## `harbour` + `night` -> `harbour_night`. Variants are suffixes, never subdirectories, so a location
	## keeps one folder.
	var clean_base := _clean_id(base_id)
	var clean_variant := _clean_id(variant_name)
	if clean_base.is_empty() or clean_variant.is_empty():
		return ""
	return "%s_%s" % [clean_base, clean_variant]
