## The Stress ledger screen: does the table actually see and drive the overlay (#928)?
##
## The screen is instantiated without a tree, the way the other screen suites do it: `setup()` builds the
## interface, and the handlers are the same ones the buttons call. A Control that only exists in a .tscn
## nobody loads is not a feature, so the scene file itself is loaded and instantiated here too.
extends RefCounted

const Screen := preload("res://godot/ui/stress_screen.gd")
const Stress := preload("res://mods/noopunk/stress.gd")
const SCENE := "res://scenes/stress_screen.tscn"


func _eq(name: String, actual: Variant, expected: Variant) -> Array:
	return [name, actual == expected, "got %s; expected %s" % [str(actual), str(expected)]]


func _screen(wisdom: int = 5, enabled: bool = true) -> Object:
	var screen: Object = Screen.new()
	screen.setup(wisdom, enabled)
	return screen


func _pick(button: OptionButton, id: String) -> void:
	for index in button.item_count:
		if String(button.get_item_metadata(index)) == id:
			button.select(index)
			return


func run() -> Array:
	var rows: Array = []

	# --- the scene is wired into the project --------------------------------
	rows.append(_eq("the scene file exists", ResourceLoader.exists(SCENE), true))
	var packed: PackedScene = load(SCENE)
	var instance: Node = packed.instantiate()
	rows.append(_eq("the scene instantiates with its script", instance.get_script() != null, true))
	rows.append(_eq("the scene is a Control", instance is Control, true))
	instance.free()

	# --- the screen states the meter and the ceiling ------------------------
	var screen := _screen(5, true)
	rows.append(_eq("the status line shows Stress and WIS",
		screen._status.text.contains("Stress 0 / WIS 5"), true))
	rows.append(_eq("the ceiling is editable", int(screen._wisdom.value), 5))
	rows.append(_eq("the module flag is on", screen._enabled.button_pressed, true))

	var off := _screen(10, false)
	rows.append(_eq("a disabled module says so", off._status.text.contains("module is off"), true))
	rows.append(_eq("and offers no events", off._add.disabled, true))

	# --- the trigger list separates the two systems -------------------------
	var labels: PackedStringArray = []
	for index in screen._trigger.item_count:
		labels.append(screen._trigger.get_item_text(index))
	var joined := "\n".join(labels)
	rows.append(_eq("the source's triggers are listed", joined.contains("AWN · kill_human"), true))
	rows.append(_eq("the NooPunk triggers are listed separately",
		joined.contains("NoöPunk · nhi_disclosure_confirmed"), true))

	# --- a scene, and what it costs ----------------------------------------
	_pick(screen._trigger, "kill_human")
	screen._trigger.item_selected.emit(screen._trigger.selected)
	screen._participant.button_pressed = true
	screen._on_add()
	rows.append(_eq("the cause is shown", screen._causes.text.contains("kill_human"), true))
	rows.append(_eq("the meter has not yet moved", Stress.stress(screen.tracker), 0))
	_pick(screen._modifier, "first_kill")
	screen._die.value = 4
	screen._on_add()
	rows.append(_eq("a first kill needs the rolled die", screen._causes.text.contains("+6"), true))

	screen._participant.button_pressed = false
	_pick(screen._trigger, "witness_atrocity")
	screen._trigger.item_selected.emit(screen._trigger.selected)
	screen._on_add()
	rows.append(_eq("a bystander adds no cause at all",
		Stress.latest_causes(screen.tracker).size(), 2))
	screen._participant.button_pressed = true

	screen._on_end_scene()
	rows.append(_eq("ending the scene moves the meter", Stress.stress(screen.tracker), 8))
	rows.append(_eq("a check is owed and stated", screen._status.text.contains("A check is owed"), true))
	rows.append(_eq("the save buttons become available", screen._save_fail.disabled, false))

	# --- Breakdown or Hardening --------------------------------------------
	rows.append(_eq("no Breakdown may be chosen before the check", screen._suffer.disabled, true))
	screen._on_save(false)
	rows.append(_eq("a failed check offers the Breakdowns", screen._suffer.disabled, false))
	rows.append(_eq("and the scars", screen._harden.disabled, false))
	_pick(screen._breakdown, "withdrawal")
	screen._on_suffer()
	rows.append(_eq("the active Breakdown is listed",
		screen._conditions.text.to_lower().contains("withdrawal"), true))
	rows.append(_eq("and named in the status line",
		screen._status.text.contains("Breakdown in force"), true))
	rows.append(_eq("the meter is frozen while it lasts", Stress.award(screen.tracker, "kill_human")["suppressed"], "breakdown"))

	# --- recovery, and the day limit ---------------------------------------
	_pick(screen._recovery, "major_goal")
	screen._die.value = 3
	screen._on_recover()
	rows.append(_eq("recovery brings the character back under the ceiling",
		Stress.stress(screen.tracker), 5))
	rows.append(_eq("crossing the ceiling ends the Breakdown",
		screen._conditions.text.contains("Nothing active"), true))
	_pick(screen._recovery, "safe_day")
	screen._on_recover()
	rows.append(_eq("a used recovery is barred for the rest of the day",
		_screen_recovery_disabled(screen, "safe_day"), true))
	screen._on_new_day()
	rows.append(_eq("a new day re-opens it", _screen_recovery_disabled(screen, "safe_day"), false))

	# --- Hardening, from the screen ---------------------------------------
	var harsh := _screen(5, true)
	_pick(harsh._trigger, "kill_human")
	harsh._trigger.item_selected.emit(harsh._trigger.selected)
	harsh._on_add()
	_pick(harsh._modifier, "first_kill")
	harsh._die.value = 4
	harsh._on_add()
	harsh._on_end_scene()
	harsh._on_save(false)
	_pick(harsh._scar, "nightmares")
	harsh._on_harden()
	rows.append(_eq("hardening clears the meter on screen", Stress.stress(harsh.tracker), 0))
	rows.append(_eq("the scar is listed as in force",
		harsh._conditions.text.to_lower().contains("nightmares"), true))
	rows.append(_eq("a taken scar leaves the list", _scar_index(harsh, "nightmares"), -1))

	# --- persistence ------------------------------------------------------
	screen._on_save_file()
	rows.append(_eq("the ledger is written", FileAccess.file_exists(Screen.SAVE_PATH), true))
	var before := Stress.stress(screen.tracker)
	var reopened := _screen(5, true)
	reopened._on_load_file()
	rows.append(_eq("the ledger is read back", Stress.stress(reopened.tracker), before))
	rows.append(_eq("with the same ceiling", Stress.threshold(reopened.tracker), 5))

	for freeable in [screen, off, harsh, reopened]:
		freeable.free()
	return rows


func _screen_recovery_disabled(screen: Object, id: String) -> bool:
	for index in screen._recovery.item_count:
		if String(screen._recovery.get_item_metadata(index)) == id:
			return screen._recovery.is_item_disabled(index)
	return true


func _scar_index(screen: Object, id: String) -> int:
	for index in screen._scar.item_count:
		if String(screen._scar.get_item_metadata(index)) == id:
			return index
	return -1
