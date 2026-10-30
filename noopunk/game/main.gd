extends Node2D

## The walking scene. It shows the sheet that was rolled a moment ago and nothing else about rules.

func _ready() -> void:
	var label := get_node_or_null("Hint/SheetLabel") as Label
	if label != null:
		var state: Node = load("res://character_state.gd").ensure(self)
		label.text = String(state.sheet_text()) if state != null else "No character yet."
