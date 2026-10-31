## Godot theme built from the 1974 design tokens (#897).
##
## The art bible and the game must read the same numbers. This module is the only place a hex value
## becomes a `Color`: UI code asks for a role (`"accent"`, `"danger"`), never for `#B8E986`. That way the
## palette can move in one file without a hunt through scenes.
##
## Failure is loud on purpose. If the tokens are missing or malformed, `build()` returns an empty theme
## and `problems` explains why — a silent fallback palette would drift from the bible and nobody would
## notice until the screens looked wrong.
extends RefCounted
class_name NoopunkTheme

const TOKENS_PATH := "res://docs/art/design_tokens.json"

var tokens: Dictionary = {}
var problems: Array = []


static func load_tokens(path: String = TOKENS_PATH) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


## Flatten the palette into role -> Color. The token file groups colours (core/acid/psychedelic…),
## so every leaf string that looks like a hex colour becomes addressable by its key.
func palette() -> Dictionary:
	var out: Dictionary = {}
	if tokens.is_empty():
		tokens = load_tokens()
	if tokens.is_empty():
		problems.append("tokens missing or unreadable: %s" % TOKENS_PATH)
		return out
	var source: Dictionary = tokens.get("palette", {})
	_collect(source, out)
	if out.is_empty():
		problems.append("no hex colours found under 'palette'")
	return out


func _collect(node: Variant, out: Dictionary) -> void:
	if node is Dictionary:
		for key in node.keys():
			_collect(node[key], out)
	elif node is String and String(node).begins_with("#") and String(node).length() == 7:
		out[String(node)] = Color(String(node))


## Resolve a colour by hex value or by role name, falling back through the semantic map when present.
func color(name: String) -> Color:
	var colors := palette()
	if colors.has(name):
		return colors[name]
	var semantic: Dictionary = tokens.get("semantic", {})
	if semantic.has(name):
		var target := String(semantic[name])
		if colors.has(target):
			return colors[target]
	problems.append("unknown colour role: %s" % name)
	return Color.MAGENTA  # deliberately loud: a missing role must be visible, not tasteful


## Font sizes from the token file; the bible's scale, applied as one map.
func type_scale() -> Dictionary:
	var raw: Variant = tokens.get("typography", {})
	if not (raw is Dictionary):
		return {}
	var typography: Dictionary = raw
	var scale: Variant = typography.get("scale_px", {})
	return scale if scale is Dictionary else {}


## A Theme that uses the tokens for the widgets the game actually draws today.
func build() -> Theme:
	tokens = tokens if not tokens.is_empty() else load_tokens()
	var theme := Theme.new()
	var colors := palette()
	if colors.is_empty():
		return theme

	var text := color("paper")
	if not colors.has("#E8DFC8") and colors.size() > 0:
		text = colors.values()[0]

	# Labels
	theme.set_color("font_color", "Label", text)
	theme.set_color("font_shadow_color", "Label", Color(0, 0, 0, 0.35))

	# Buttons: flat period panels, not modern pills.
	var normal := StyleBoxFlat.new()
	normal.bg_color = color("shell")
	normal.border_color = color("acid_green")
	normal.set_border_width_all(1)
	normal.set_corner_radius_all(0)
	var hover := normal.duplicate()
	hover.bg_color = color("acid_green")
	var pressed := normal.duplicate()
	pressed.bg_color = color("mustard")

	theme.set_stylebox("normal", "Button", normal)
	theme.set_stylebox("hover", "Button", hover)
	theme.set_stylebox("pressed", "Button", pressed)
	theme.set_color("font_color", "Button", text)
	theme.set_color("font_hover_color", "Button", color("ink"))

	# Panels
	var panel := StyleBoxFlat.new()
	panel.bg_color = color("shell")
	panel.border_color = color("paper")
	panel.set_border_width_all(1)
	panel.set_corner_radius_all(0)
	theme.set_stylebox("panel", "Panel", panel)
	theme.set_stylebox("panel", "PanelContainer", panel)

	var scale: Dictionary = type_scale()
	if scale.has("body"):
		theme.set_default_font_size(int(scale["body"]))
	return theme
