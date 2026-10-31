## Image preview: portrait and social-encounter layouts in the real renderer (#908).
##
## Two modes, one screen. The geometry comes from `image_layout.gd` and the textures from
## `image_library.gd`; this node only applies the rects. Toggle with the button or the `M` key.
##
## Built in `setup()`/`_ensure_build()`, not `_ready()`: a `--script` runner adds nodes before the main loop
## starts, so `_ready` never fires and a test would measure an empty control.
extends Control

const Library := preload("res://godot/core/image_library.gd")
const Layout := preload("res://godot/ui/image_layout.gd")

var library: Object = null
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
	library = Library.from_manifest()
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
	if library == null:
		library = Library.from_manifest()

	var background := ColorRect.new()
	background.set_anchors_preset(Control.PRESET_FULL_RECT)
	background.color = Color(0.10, 0.086, 0.07)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	_background = TextureRect.new()
	_background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_background.visible = false
	add_child(_background)

	_image = TextureRect.new()
	_image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
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
		_apply(_image, "probe_portrait", frame["image"])
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
		_background.position = frame["background"].position
		_background.size = frame["background"].size
		_background.texture = library.texture_by_id("probe_encounter")
		_apply(_image, "probe_portrait", frame["portrait"])
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


func _apply(rect: TextureRect, asset_id: String, frame: Rect2) -> void:
	if not library.apply_to(rect, asset_id):
		problems.append_array(library.problems)
	rect.position = frame.position
	rect.size = frame.size
