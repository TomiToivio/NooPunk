## Image library: manifest-backed textures for screens (#908).
##
## Screens ask for an **id**, never a path. The manifest owns where the file is, how it should be stretched
## and what it is for. A screen that hardcodes `res://images/...` is a second copy of the manifest.
##
## Missing art is loud: `texture()` returns null and records a problem naming the id and the path. A silent
## blank texture looks like a design choice, and nobody investigates a design choice.
extends RefCounted
class_name NoopunkImageLibrary

const MANIFEST_PATH := "res://images/manifest.json"

var entries: Dictionary = {}
var problems: Array = []
var _cache: Dictionary = {}


static func load_library(path: String = MANIFEST_PATH) -> NoopunkImageLibrary:
	var library := NoopunkImageLibrary.new()
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


## Load the texture for an id. Cached, because a dialogue screen asks for the same portrait repeatedly.
func texture(asset_id: String) -> Texture2D:
	if _cache.has(asset_id):
		return _cache[asset_id]
	var record: Dictionary = entry(asset_id)
	if record.is_empty():
		return null
	var path := String(record.get("path", ""))
	if not ResourceLoader.exists(path):
		problems.append("file missing for %s: %s" % [asset_id, path])
		return null
	var loaded: Resource = load(path)
	if not (loaded is Texture2D):
		problems.append("%s is not a texture: %s" % [asset_id, path])
		return null
	_cache[asset_id] = loaded
	return loaded


## The stretch mode the manifest category implies. Portraits are never cropped; locations may fill.
static func stretch_mode_for(category: String) -> TextureRect.StretchMode:
	match category:
		"characters/portraits", "social_encounters":
			# Letterbox rather than crop: a face at the edge of a 3:4 portrait must not be lost to a
			# widescreen frame.
			return TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		"locations":
			# A place has no face at a fixed coordinate; filling the frame is the right trade.
			return TextureRect.STRETCH_KEEP_ASPECT_COVERED
		_:
			return TextureRect.STRETCH_KEEP_ASPECT_CENTERED


## Point a TextureRect at an asset. Geometry is not decided here — see `image_layout.gd`.
func apply_to(rect: TextureRect, asset_id: String) -> bool:
	var record: Dictionary = entry(asset_id)
	if record.is_empty():
		return false
	var loaded := texture(asset_id)
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
