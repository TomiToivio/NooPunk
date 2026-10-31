## Image preview: portrait and social-encounter layouts in the real renderer (#908).
##
## Two modes, one screen. The geometry comes from `image_layout.gd`; the pixels are drawn here from the
## design-token palette, because **no artwork is approved yet** and a screen that needs a committed image to
## open would be a screen nobody can look at.
##
## When the first approved portrait lands, replace `_procedural_texture()` with the manifest id and
## `ImageLibrary.resolve()` — the layout does not care where the pixels came from.
##
## Built in `setup()`/`_ensure_build()`, not `_ready()`: a `--script` runner adds nodes before the main loop
## starts, so `_ready` never fires and a test would measure an empty control.
extends Control

const Layout := preload("res://godot/ui/image_layout.gd")

## Palette, mirrored from docs/art/design_tokens.json. Kept as constants here rather than loaded, because
## this screen must open on a fresh clone with no assets at all.
const INK := Color(0.10, 0.086, 0.07)
const OCHRE := Color(0.77, 0.54, 0.23)
const RUST := Color(0.61, 0.29, 0.17)
const BONE := Color(0.91, 0.86, 0.77)

var mode: String = "portrait"
var problems: Array = []

var _built := false
var _image: TextureRect
var _background: TextureRect
var _caption: Label
var _dialogue: Label
var _mode_button: Button


func setup(start_mode: String = "portrait") -> void:
	mode = start_mode
	_ensure_build()
	_relayout()


func _ready() -> void:
	_ensure_build()
	_relayout()


func _ensure_build() -> void:
	if _built:
		return
	_built = true
	set_anchors_preset(Control.PRESET_FULL_RECT)

	var background := ColorRect.new()
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	background.color = INK
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	_background = TextureRect.new()
	_background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_background.visible = false
	_background.texture = _procedural_texture(800, 600, OCHRE)
	add_child(_background)

	_image = TextureRect.new()
	_image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_image.texture = _procedural_texture(600, 800, RUST)
	add_child(_image)

	_caption = Label.new()
	_caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(_caption)

	_dialogue = Label.new()
	_dialogue.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_dialogue.visible = false
	add_child(_dialogue)

	_mode_button = Button.new()
	_mode_button.text = "Encounter layout"
	_mode_button.pressed.connect(_toggle_mode)
	add_child(_mode_button)


## A flat two-tone field with a border, so letterboxing and aspect choices are visible without art.
static func _procedural_texture(width: int, height: int, field: Color) -> Texture2D:
	var image := Image.create_empty(width, height, false, Image.FORMAT_RGBA8)
	image.fill(field)
	for x in width:
		image.set_pixel(x, 0, BONE)
		image.set_pixel(x, height - 1, BONE)
	for y in height:
		image.set_pixel(0, y, BONE)
		image.set_pixel(width - 1, y, BONE)
	return ImageTexture.create_from_image(image)


func _toggle_mode() -> void:
	mode = "encounter" if mode == "portrait" else "portrait"
	_relayout()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_M:
		_toggle_mode()


func _relayout() -> void:
	if not _built:
		return
	problems.clear()
	var viewport := get_viewport_rect().size
	_mode_button.position = Vector2(12, viewport.y - 40)

	if mode == "portrait":
		var frame: Dictionary = Layout.portrait_frame(viewport)
		problems.append_array(frame["problems"])
		_background.visible = false
		_place(_image, frame["image"])
		_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		_caption.position = frame["caption"].position
		_caption.size = frame["caption"].size
		_caption.text = "Harri Romppainen — portrait frame (3:4, aspect kept, nothing cropped)"
		_dialogue.visible = false
		_mode_button.text = "Encounter layout"
	else:
		var frame: Dictionary = Layout.encounter_frame(viewport)
		problems.append_array(frame["problems"])
		_background.visible = true
		_place(_background, frame["background"])
		_place(_image, frame["portrait"])
		_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		_caption.position = Vector2(frame["portrait"].position.x,
			frame["portrait"].position.y + frame["portrait"].size.y + 6.0)
		_caption.size = Vector2(frame["portrait"].size.x, 24)
		_caption.text = "Harri Romppainen"
		_dialogue.visible = true
		_dialogue.position = frame["dialogue"].position
		_dialogue.size = frame["dialogue"].size
		_dialogue.text = "«You're the new one. Sit down — the file is thicker than it looks.»"
		_mode_button.text = "Portrait layout"


func _place(rect: TextureRect, frame: Rect2) -> void:
	rect.position = frame.position
	rect.size = frame.size
