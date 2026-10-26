extends Control
# Issue #631: first playable, offline investigation; Without Number 2d6 checks.
const SAVE := "user://noopunk_case.json"
const POINTS := {"doctor": Vector2(220,170), "nurse": Vector2(530,170), "patient": Vector2(780,430), "record": Vector2(510,430), "terminal": Vector2(220,430)}
var pos := Vector2(110,170)
var clues: Array[String] = []
var outcome := ""
var rng := RandomNumberGenerator.new()
var logbox: RichTextLabel
var options: VBoxContainer
var busy := false

func _ready() -> void:
	rng.randomize()
	var panel := PanelContainer.new()
	panel.set_anchors_and_offsets_preset(Control.PRESET_RIGHT_WIDE)
	panel.offset_left = -370
	add_child(panel)
	var column := VBoxContainer.new()
	panel.add_child(column)
	var title := Label.new()
	title.text = "NOÖPUNK | LAKKAHALTIA"
	column.add_child(title)
	logbox = RichTextLabel.new()
	logbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(logbox)
	options = VBoxContainer.new()
	column.add_child(options)
	var controls := HBoxContainer.new()
	column.add_child(controls)
	for action in ["Journal", "Save", "Load"]:
		var button := Button.new()
		button.text = action
		button.pressed.connect(_command.bind(action))
		controls.add_child(button)
	_log("Inspector Romppainen enters the hospital. WASD/arrows: move; E: investigate. F5/F9: save/load.")

func _process(delta: float) -> void:
	if busy or outcome != "":
		return
	var direction := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	if Input.is_key_pressed(KEY_A):
		direction.x -= 1.0
	if Input.is_key_pressed(KEY_D):
		direction.x += 1.0
	if Input.is_key_pressed(KEY_W):
		direction.y -= 1.0
	if Input.is_key_pressed(KEY_S):
		direction.y += 1.0
	direction = direction.limit_length(1.0)
	pos += direction * delta * 175.0
	pos.x = clampf(pos.x, 60, 960)
	pos.y = clampf(pos.y, 75, 600)
	queue_redraw()

func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_E:
				if not busy:
					_interact()
			KEY_F5:
				_command("Save")
			KEY_F9:
				_command("Load")
			KEY_J:
				_command("Journal")

func _draw() -> void:
	draw_rect(Rect2(0, 0, 1010, 640), Color(0.09,0.12,0.16))
	for region in [Rect2(50,75,300,225), Rect2(365,75,300,225), Rect2(680,75,310,225), Rect2(50,310,615,300), Rect2(680,310,310,300)]:
		draw_rect(region, Color(0.19,0.23,0.26))
		draw_rect(region, Color(0.42,0.46,0.49), false, 2)
	for key in POINTS:
		var location: Vector2 = POINTS[key]
		draw_circle(location, 15, Color(0.55,0.8,0.8))
		draw_string(ThemeDB.fallback_font, location + Vector2(-28,-22), key, HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color.WHITE)
	draw_circle(pos, 13, Color(1.0,0.9,0.5))

func _interact() -> void:
	var nearest := ""
	var distance := 82.0
	for key in POINTS:
		var d: float = pos.distance_to(POINTS[key])
		if d < distance:
			nearest = key
			distance = d
	if nearest == "":
		_log("Nothing is within reach.")
		return
	match nearest:
		"doctor":
			_ask("Doctor: 'The AI issued an assessment before the examination.'", ["Record testimony", "Ask about vanished patient"], ["doctor_ai", "doctor_patient"])
		"nurse":
			_ask("Nurse: 'The camera captured a lacquered cap in an empty corridor.'", ["Take incident report", "Inspect floor plan"], ["nurse_camera", "nurse_map"])
		"patient":
			_ask("Patient: 'The walls are how it speaks.'", ["Listen carefully", "Ask about the Lakkahaltia"], ["patient_voice", "patient_lakkahaltia"])
		"record":
			_ask("A clinical file bears two different admission dates.", ["Inspect record (WIS/Notice, 8)"], ["record_check"])
		"terminal":
			_ask("The ward computer contains an offline diagnostic cache.", ["Read cache (INT/Program, 8)"], ["terminal_check"])

func _ask(message: String, labels: Array, actions: Array) -> void:
	busy = true
	_log(message)
	for old in options.get_children():
		old.queue_free()
	for i in labels.size():
		var button := Button.new()
		button.text = labels[i]
		button.pressed.connect(_act.bind(actions[i]))
		options.add_child(button)

func _act(action: String) -> void:
	busy = false
	for old in options.get_children():
		old.queue_free()
	match action:
		"record_check":
			_roll("WIS", 0, 8, "The record predates the patient's arrival.")
		"terminal_check":
			_roll("INT", 1, 8, "AI cache contains a second, unexplained assessment.")
		"end_mundane":
			outcome = "Technical or clinical explanation (provisional)"
		"end_anomalous":
			outcome = "Anomalous-phenomena explanation (provisional)"
		_:
			var notes := {"doctor_ai":"The diagnostic AI predicted an examination.", "doctor_patient":"A patient disappeared during a power failure.", "nurse_camera":"Footage contains a figure wearing a lacquered cap.", "nurse_map":"The historical floor plan shows an extra room.", "patient_voice":"The patient reports voices in the walls.", "patient_lakkahaltia":"The patient invokes the Lakkahaltia of urban folklore."}
			_note(notes.get(action, "Unresolved testimony."))
	if outcome != "":
		_log("CASE FILED: " + outcome + ". Neither interpretation proves what occurred.")
	elif clues.size() >= 3:
		_ask("The ward lights flicker. A figure appears in the glass. File a provisional report?", ["Clinical/technical", "Anomalous"], ["end_mundane", "end_anomalous"])

func _roll(attribute: String, rank: int, target: int, clue: String) -> void:
	var mod := 0 if attribute == "WIS" else 1
	var a := rng.randi_range(1,6)
	var b := rng.randi_range(1,6)
	var total := a + b + mod + rank
	_log("%s check: %d + %d + %d + %d = %d vs %d" % [attribute,a,b,mod,rank,total,target])
	if total >= target:
		_note(clue)
	else:
		_log("Inconclusive. You can re-examine the evidence.")

func _note(clue: String) -> void:
	if not clues.has(clue):
		clues.append(clue)
	_log("EVIDENCE: " + clue)

func _log(line: String) -> void:
	logbox.append_text(line + "\n\n")

func _command(action: String) -> void:
	match action:
		"Journal":
			_log("JOURNAL:\n" + "\n".join(clues))
		"Save":
			var file := FileAccess.open(SAVE, FileAccess.WRITE)
			if file != null:
				file.store_string(JSON.stringify({"version":1,"pos":[pos.x,pos.y],"clues":clues,"outcome":outcome}))
				_log("Case saved.")
		"Load":
			if not FileAccess.file_exists(SAVE):
				_log("No saved case.")
				return
			var saved = JSON.parse_string(FileAccess.get_file_as_string(SAVE))
			if not saved is Dictionary or saved.get("version") != 1:
				_log("Invalid save.")
				return
			var xy: Array = saved.get("pos", [110,170])
			pos = Vector2(float(xy[0]),float(xy[1]))
			clues.clear()
			for item in saved.get("clues", []):
				clues.append(str(item))
			outcome = str(saved.get("outcome", ""))
			_log("Case loaded.")
