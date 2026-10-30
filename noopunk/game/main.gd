extends Node2D

## The walking scene (#827) plus the character sheet read-out (#835).
##
## The sheet is shown here so the player can see that the values rolled during creation are still
## theirs while they walk around. Nothing about movement depends on the attributes yet: no check
## mechanic has been specified, so this scene displays and nothing more.

@onready var sheet_label: Label = $Sheet/Label

func _ready() -> void:
	# Autoloads are not instantiated when the project is run with `--script` (the headless checks), so
	# this looks the node up instead of assuming it exists. In the running game it always does.
	var sheet := get_node_or_null("/root/Sheet")
	if sheet != null and sheet.has_sheet():
		sheet_label.text = sheet.summary()
	else:
		sheet_label.text = "No character sheet - run creation first"
