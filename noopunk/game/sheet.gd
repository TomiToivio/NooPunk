extends Node

## The character sheet for the current session (#835).
##
## A tiny autoload, and deliberately the only one: the creation screen writes the rolled sheet here and
## the walking scene reads it, so the attributes survive the scene change and stay put while the player
## moves. Nothing else is stored - no skills, inventory, experience or scenario state, because none of
## those exist yet.

var rolled: Dictionary = {}
var values: Dictionary = {}

func set_roll(new_roll: Dictionary) -> void:
	rolled = new_roll.duplicate(true)
	values = NoopunkAttributes.sheet(rolled)

func has_sheet() -> bool:
	return not values.is_empty()

func summary() -> String:
	if not has_sheet():
		return "No character sheet yet"
	return NoopunkAttributes.format_sheet(values)

func clear() -> void:
	rolled = {}
	values = {}
