## The investigation console: where an investigator's abilities meet a scene's clues (#932).
##
## Three modules already exist and this screen adds no fourth rule. It is the place they meet a human:
##
## * `mods/noopunk/gumshoe_investigation.gd` — the GUMSHOE SRD procedure: abilities, ratings, pools, benefits.
## * `godot/core/investigation_adapter.gd` — the *only* place Godot reads a clue rule (#718): what a sheet may
##   discover in a scene, competence by presence.
## * `godot/narrative/investigation.gd` — the notebook: what was found, what it opens, what it contradicts.
##
## Four boundaries are visible in the interface on purpose:
##
## * **The split of authority is stated, not blurred.** The *adapter* decides whether an investigator may
##   find a clue — competence is the presence of a CWN rank, and rank 0 is trained. The *overlay* decides
##   what points can buy. Where the two disagree about the rating gate the ruling is open (D61), so the gate
##   is a visible control and every gather says which gate let it through.
## * **Gathering never rolls and never spends.** A competent investigator gets the clue; the screen records,
##   it does not resolve.
## * **A benefit is never a clue.** Benefit buttons spend pool points and log. They cannot touch the
##   notebook, so buying one cannot be what solves the case.
## * **The screen never edits the CWN sheet.** Skill ranks are copied in; the core save schema is untouched
##   and this screen's state lives at `user://gumshoe_investigation_state.json`.
extends Control

const Gumshoe := preload("res://mods/noopunk/gumshoe_investigation.gd")
const Adapter := preload("res://godot/core/investigation_adapter.gd")
const Notebook := preload("res://godot/narrative/investigation.gd")

const SAVE_PATH := "user://gumshoe_investigation_state.json"
const GATE_CWN := "cwn_presence"
const GATE_SRD := "srd_rating"

var overlay: Object
var adapter: Object
var notebook: Object
var sheet: Dictionary = {}
var scene_id: String = ""
var gate: String = GATE_CWN
var log_lines: Array = []

var _built := false
var _status: Label
var _scene: OptionButton
var _gate: OptionButton
var _clues: VBoxContainer
var _abilities: VBoxContainer
var _case: Label
var _log: Label
var _benefit_name: LineEdit


func _ready() -> void:
	if not _built:
		if overlay == null:
			setup({"Know": 0, "Notice": 0})
		else:
			_build()


## Open the console for one character and one scene. `sheet` is a CWN skill dict copied from the sheet,
## e.g. `{"Notice": 2, "Know": 1, "Program": 0}` — rank 0 is a trained rank in CWN, and the default gate says so.
func setup(sheet_ranks: Dictionary = {"Know": 0, "Notice": 0},
		scene: String = "", case_path: String = "") -> void:
	sheet = sheet_ranks.duplicate(true)
	adapter = Adapter.new() if case_path.is_empty() else Adapter.new(case_path)
	overlay = Gumshoe.shipped(_ratings_from_sheet(sheet))
	notebook = _notebook_from_graph(adapter.case_graph)
	scene_id = scene if not scene.is_empty() else _first_scene()
	_build()


# ---- the CWN <-> SRD bridge -------------------------------------------------------------


## An investigative rating is the CWN rank of the skill it maps to. A character built purely on CWN
## therefore has ratings without a second character build; whether rank 0 *gathers* is the gate's question.
func _ratings_from_sheet(ranks: Dictionary) -> Dictionary:
	var template: Object = overlay if overlay != null else Gumshoe.shipped()
	var ratings: Dictionary = {}
	for ability_id in template.order:
		ratings[ability_id] = int(ranks.get(String(template.cwn_skill_for(ability_id)), 0))
	return ratings


## Seed the notebook from the same case graph the adapter reads: a `core` clue is essential, and its
## `leads_to` are the locations it opens. The notebook is the record of the case, not a second rule engine.
func _notebook_from_graph(graph: Dictionary) -> Object:
	var rows: Array = []
	for scene in Array(graph.get("scenes", [])):
		for clue in Array(scene.get("clues", [])):
			rows.append({
				"id": String(clue.get("id", "")),
				"essential": String(clue.get("kind", "optional")) == "core",
				"requires": [],
				"opens": Array(clue.get("leads_to", [])),
				"contradicts": [],
			})
	return Notebook.from_data({"clues": rows})


# ---- the two actions the rules allow -----------------------------------------------------


## Whether this investigator may find this clue in this scene — and by which gate.
##
## Permission is the adapter's rule (a CWN rank is present, rank 0 included). The overlay is consulted
## afterwards: where an ability maps to the clue's competency its own `gather()` verdict is honoured, and
## under the SRD gate a competency with no mapped ability at rating 1 or more is refused outright.
func permits(clue_id: String) -> Dictionary:
	var clue := _clue(clue_id)
	if clue.is_empty():
		return {"ok": false, "reason": "unknown_clue", "scene": scene_id}
	var competency := String(clue.get("competency", ""))
	if not bool(adapter.is_competent(sheet, competency)):
		return {"ok": false, "reason": "no_competence", "competency": competency}
	var ability := covering_ability(competency)
	if gate == GATE_SRD and ability.is_empty():
		return {"ok": false, "reason": "rating_below_one", "competency": competency}
	return {"ok": true, "reason": "", "competency": competency, "ability": ability}


## Gather a clue from the current scene. No roll, no spend: this screen never resolves anything.
func gather(clue_id: String) -> Dictionary:
	var verdict := permits(clue_id)
	if not bool(verdict.get("ok", false)):
		return verdict
	var clue := _clue(clue_id)
	var ability := String(verdict.get("ability", ""))
	if not ability.is_empty() and int(overlay.rating(ability)) >= 1:
		# Where the overlay's own rating gate is satisfied, its verdict is the one that counts. Where the CWN
		# gate allowed a rank-0 investigator, the overlay has no opinion to give and must not veto.
		var from_overlay: Dictionary = overlay.gather(ability, {"id": clue_id,
			"core": String(clue.get("kind", "")) == "core"})
		if not bool(from_overlay.get("ok", false)):
			return from_overlay
	var recorded: Dictionary = notebook.gather(clue_id, true, {})
	if not bool(recorded.get("ok", false)):
		return recorded
	return {
		"ok": true,
		"found": true,
		"clue": clue_id,
		"ability": ability,
		"cwn_skill": String(clue.get("competency", "")),
		"core": String(clue.get("kind", "")) == "core",
		"gate": gate,
		"spent": 0,
	}


## Buy a special benefit with pool points. The only place points leave a pool, and it never yields a clue.
func buy_benefit(ability_id: String, benefit_id: String, cost: int = 1) -> Dictionary:
	var before: int = notebook.count()
	var result: Dictionary = overlay.buy_benefit(ability_id, benefit_id, cost)
	# A benefit that reached the notebook would be a second way to solve a case. There is not one, and the
	# flag is measured rather than asserted.
	result["touched_notebook"] = notebook.count() != before
	return result


## A new investigation restores every pool to its rating; nothing else refreshes between cases.
func refresh_pools() -> Dictionary:
	return overlay.refresh()


## The overlay ability whose CWN mapping is this competency, if any. Under the SRD gate the ability must
## also carry a rating of at least 1; under the CWN gate the adapter has already spoken for the sheet.
func covering_ability(competency: String) -> String:
	for ability_id in overlay.order:
		if String(overlay.cwn_skill_for(ability_id)) != competency:
			continue
		if gate == GATE_SRD and int(overlay.rating(ability_id)) < 1:
			continue
		return String(ability_id)
	return ""


## Competencies the shipped case asks for that no investigative ability covers. Not a warning to bury: it is
## shown in the interface, because under the SRD gate those clues are out of reach.
func uncovered_competencies() -> Array:
	var uncovered: Array = []
	for scene in Array(adapter.case_graph.get("scenes", [])):
		for clue in Array(scene.get("clues", [])):
			var competency := String(clue.get("competency", ""))
			if covering_ability(competency).is_empty() and not uncovered.has(competency):
				uncovered.append(competency)
	uncovered.sort()
	return uncovered


func _clue(clue_id: String) -> Dictionary:
	for clue in Array(adapter.scene(scene_id).get("clues", [])):
		if String(clue.get("id", "")) == clue_id:
			return clue
	return {}


func _first_scene() -> String:
	var ids: Array = adapter.scene_ids()
	return String(ids[0]) if not ids.is_empty() else ""


# ---- persistence: beside the core save, never inside it ---------------------------------


func save_state() -> void:
	var payload := {
		"scene": scene_id,
		"gate": gate,
		"sheet": sheet,
		"overlay": overlay.to_dict(),
		"found": notebook.found,
		"leads": notebook.leads,
		"contradictions": notebook.contradictions,
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		return
	file.store_string(JSON.stringify(payload, "\t"))


func load_state() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		return false
	var data: Dictionary = parsed
	sheet = Dictionary(data.get("sheet", sheet))
	gate = String(data.get("gate", GATE_CWN))
	scene_id = String(data.get("scene", scene_id))
	overlay = Gumshoe.shipped(_ratings_from_sheet(sheet))
	overlay.from_dict(Dictionary(data.get("overlay", {})))
	notebook.found = Array(data.get("found", []))
	notebook.leads = Array(data.get("leads", []))
	notebook.contradictions = Array(data.get("contradictions", []))
	return true


# ---- the interface -----------------------------------------------------------------------


func _build() -> void:
	_built = true
	var scroll := ScrollContainer.new()
	scroll.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(scroll)
	var page := VBoxContainer.new()
	page.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	page.add_theme_constant_override("separation", 8)
	scroll.add_child(page)

	var title := _label(page, "Investigation — GUMSHOE SRD procedure over CWN (optional)")
	title.add_theme_font_size_override("font_size", 20)
	_status = _label(page, "")
	_status.add_theme_font_size_override("font_size", 16)

	var top := HBoxContainer.new()
	page.add_child(top)
	top.add_child(_label_raw("Scene  "))
	_scene = OptionButton.new()
	_scene.custom_minimum_size = Vector2(220, 0)
	for id in adapter.scene_ids():
		_scene.add_item(String(id))
		_scene.set_item_metadata(_scene.item_count - 1, String(id))
	_select(_scene, scene_id)
	_scene.item_selected.connect(_on_scene)
	top.add_child(_scene)

	top.add_child(_label_raw("    Competence gate  "))
	_gate = OptionButton.new()
	_gate.add_item("CWN — rank 0 is trained")
	_gate.set_item_metadata(0, GATE_CWN)
	_gate.add_item("SRD — rating at least 1")
	_gate.set_item_metadata(1, GATE_SRD)
	_gate.select(0 if gate == GATE_CWN else 1)
	_gate.item_selected.connect(_on_gate)
	top.add_child(_gate)

	var new_case := Button.new()
	new_case.text = "New investigation (restore pools)"
	new_case.pressed.connect(_on_refresh)
	top.add_child(new_case)
	var save := Button.new()
	save.text = "Save"
	save.pressed.connect(_on_save)
	top.add_child(save)

	_label_raw_section(page, "Clues in this scene — a competent investigator gets these without a roll")
	_clues = VBoxContainer.new()
	page.add_child(_clues)

	_label_raw_section(page, "Abilities — ratings and pools, with the CWN skill each one maps to")
	_abilities = VBoxContainer.new()
	page.add_child(_abilities)

	_label_raw_section(page, "A special benefit (1–2 pool points; an advantage, never a clue)")
	var benefit_row := HBoxContainer.new()
	page.add_child(benefit_row)
	_benefit_name = LineEdit.new()
	_benefit_name.placeholder_text = "what the points buy, in the referee's words"
	_benefit_name.custom_minimum_size = Vector2(340, 0)
	benefit_row.add_child(_benefit_name)

	_label_raw_section(page, "The case so far")
	_case = _label(page, "")
	_log = _label(page, "")
	_log.modulate = Color(0.78, 0.82, 0.9)

	_refresh()


func _refresh() -> void:
	_status.text = "Scene: %s · %d clue(s) found · %d lead(s)" % [
		scene_id, notebook.count(), notebook.open_leads().size()]
	_fill_clues()
	_fill_abilities()
	_fill_case()


func _fill_clues() -> void:
	_clear(_clues)
	for clue in Array(adapter.scene(scene_id).get("clues", [])):
		var clue_id := String(clue.get("id", ""))
		var row := HBoxContainer.new()
		_clues.add_child(row)
		var found: bool = notebook.has(clue_id)
		var marker := "✓" if found else "·"
		var kind := String(clue.get("kind", "optional"))
		var verdict: Dictionary = {"ok": true, "reason": ""} if found else permits(clue_id)
		var note := "" if bool(verdict.get("ok", false)) else "  (%s)" % String(verdict.get("reason", ""))
		var label := _label(row, "%s %s [%s] — %s%s" % [
			marker, clue_id, kind, String(clue.get("competency", "")), note])
		label.custom_minimum_size = Vector2(520, 0)
		if not found:
			var button := Button.new()
			button.text = "Gather"
			button.disabled = not bool(verdict.get("ok", false))
			button.pressed.connect(_on_gather.bind(clue_id))
			row.add_child(button)


func _fill_abilities() -> void:
	_clear(_abilities)
	for ability_id in overlay.order:
		var row := HBoxContainer.new()
		_abilities.add_child(row)
		var skill := String(overlay.cwn_skill_for(ability_id))
		var text := "%s · %s · rating %d · pool %d" % [
			String(ability_id), skill, overlay.rating(ability_id), overlay.pool(ability_id)]
		var label := _label(row, text)
		label.custom_minimum_size = Vector2(420, 0)
		for cost in [1, 2]:
			var button := Button.new()
			button.text = "buy %d" % cost
			button.disabled = overlay.pool(ability_id) < cost
			button.pressed.connect(_on_buy.bind(ability_id, cost))
			row.add_child(button)


func _fill_case() -> void:
	var lines: Array = []
	lines.append("Found %d of %d clues; %s." % [
		notebook.count(), notebook.clues.size(),
		"every essential clue is in hand" if notebook.can_conclude() else "essential clues are missing"])
	var missing: Array = notebook.missing_essential()
	if not missing.is_empty():
		lines.append("Missing essential: %s" % ", ".join(missing))
	var leads: Array = notebook.open_leads()
	if not leads.is_empty():
		lines.append("Leads opened: %s" % ", ".join(leads))
	var contradicted: Array = notebook.contradicted()
	if not contradicted.is_empty():
		lines.append("Contradicted: %s" % ", ".join(contradicted))
	var uncovered: Array = uncovered_competencies()
	if not uncovered.is_empty():
		lines.append("No investigative ability covers %s — under the SRD gate those clues are out of reach." %
			", ".join(uncovered))
	_case.text = "\n".join(lines)


func _note(result: Dictionary) -> void:
	var line := String(result.get("reason", ""))
	if bool(result.get("ok", false)):
		if result.has("clue"):
			line = "gathered %s via %s (%s gate)" % [
				String(result.get("clue", "")), String(result.get("ability", "")),
				String(result.get("gate", ""))]
		elif result.has("benefit"):
			line = "bought %s for %d point(s); pool now %d — no clue was gained" % [
				String(result.get("benefit", "")), int(result.get("spent", 0)),
				int(result.get("pool", 0))]
	if line.is_empty():
		line = "no change"
	log_lines.append(line)
	while log_lines.size() > 12:
		log_lines.pop_front()
	_log.text = "\n".join(log_lines)
	_refresh()


# ---- handlers (the buttons call exactly these) -------------------------------------------


func _on_gather(clue_id: String) -> void:
	_note(gather(clue_id))


func _on_buy(ability_id: String, cost: int) -> void:
	var benefit := _benefit_name.text.strip_edges()
	if benefit.is_empty():
		benefit = "benefit"
	_note(buy_benefit(ability_id, benefit, cost))


func _on_refresh() -> void:
	refresh_pools()
	_note({"ok": true, "reason": "a new investigation restores every pool to its rating"})


func _on_save() -> void:
	save_state()
	_note({"ok": true, "reason": "saved to %s" % SAVE_PATH})


func _on_scene(index: int) -> void:
	scene_id = String(_scene.get_item_metadata(index))
	_refresh()


func _on_gate(index: int) -> void:
	gate = String(_gate.get_item_metadata(index))
	_note({"ok": true, "reason": "competence gate is now %s" % gate})


func _select(button: OptionButton, id: String) -> void:
	for index in button.item_count:
		if String(button.get_item_metadata(index)) == id:
			button.select(index)
			return


func _clear(box: Node) -> void:
	for child in box.get_children():
		box.remove_child(child)
		child.free()


func _label(parent: Node, text: String) -> Label:
	var label := _label_raw(text)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	parent.add_child(label)
	return label


func _label_raw(text: String) -> Label:
	var label := Label.new()
	label.text = text
	return label


func _label_raw_section(parent: Node, text: String) -> void:
	var label := _label_raw(text)
	label.modulate = Color(0.75, 0.8, 0.9)
	parent.add_child(label)
