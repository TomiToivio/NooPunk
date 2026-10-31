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

## ---- manifest-backed lookup (#908) --------------------------------------------------------------
##
## The functions above resolve by convention (`class/id.png`). The manifest is the other half: it says
## which assets exist, what they depict, and how a screen may present them. Screens ask for an **id** and
## the manifest answers; a hardcoded `res://images/...` in a scene is a second copy of this table.

const MANIFEST_PATH := "res://images/manifest.json"

var entries: Dictionary = {}
var problems: Array = []
var _cache: Dictionary = {}


static func from_manifest(path: String = MANIFEST_PATH) -> ImageLibrary:
	var library := ImageLibrary.new()
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		library.problems.append("manifest missing: %s" % path)
		return library
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not (parsed is Dictionary):
		library.problems.append("manifest is not an object: %s" % path)
		return library
	for entry in Array((parsed as Dictionary).get("assets", [])):
		if entry is Dictionary and entry.has("id"):
			library.entries[String(entry["id"])] = entry
	return library


func entry(asset_id: String) -> Dictionary:
	if entries.has(asset_id):
		return entries[asset_id]
	problems.append("unknown asset id: %s" % asset_id)
	return {}


## Load the texture for an id. Cached: a dialogue screen asks for the same portrait repeatedly.
func texture_by_id(asset_id: String) -> Texture2D:
	if _cache.has(asset_id):
		return _cache[asset_id]
	var record: Dictionary = entry(asset_id)
	if record.is_empty():
		return null
	var path := String(record.get("path", ""))
	if not (ResourceLoader.exists(path) or FileAccess.file_exists(path)):
		problems.append("file missing for %s: %s" % [asset_id, path])
		return null
	var loaded: Resource = load(path)
	if not (loaded is Texture2D):
		problems.append("%s is not a texture: %s" % [asset_id, path])
		return null
	_cache[asset_id] = loaded
	return loaded


## The stretch mode a category implies. Portraits are never cropped; a place may fill the frame.
static func stretch_mode_for(category: String) -> TextureRect.StretchMode:
	match category:
		"characters/portraits", "social_encounters":
			# Letterbox rather than crop: a face at the edge of a 3:4 portrait must not be lost to a
			# widescreen frame.
			return TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		"locations":
			return TextureRect.STRETCH_KEEP_ASPECT_COVERED
		_:
			return TextureRect.STRETCH_KEEP_ASPECT_CENTERED


## Point a TextureRect at an asset. Geometry is not decided here - see `godot/ui/image_layout.gd`.
func apply_to(rect: TextureRect, asset_id: String) -> bool:
	var record: Dictionary = entry(asset_id)
	if record.is_empty():
		return false
	var loaded := texture_by_id(asset_id)
	if loaded == null:
		return false
	rect.texture = loaded
	rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rect.stretch_mode = stretch_mode_for(String(record.get("category", "")))
	return true


func approved_count() -> int:
	var count := 0
	for asset_id in entries:
		if bool(entries[asset_id].get("approved", false)):
			count += 1
	return count
