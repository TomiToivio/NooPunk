extends Node

## The rolled sheet, kept for the session so it survives a scene change (#835 requirement 3).
##
## Deliberately tiny: seven converted values and nothing else. Skills, equipment, experience and
## history are undecided, so the sheet does not pretend to have them.

var rolls: Array = []


func store(new_rolls: Array) -> void:
	rolls = new_rolls.duplicate(true)


func is_complete() -> bool:
	return rolls.size() == NoopunkAttributes.names().size()


func sheet_text() -> String:
	if rolls.is_empty():
		return "No character yet."
	return "\n".join(NoopunkAttributes.sheet_lines(rolls))


func clear() -> void:
	rolls = []


## The autoload is registered in a normal game run, but not in a bare `--script` test run, where Godot
## starts a SceneTree without autoloads. This returns the registered node, or installs one under the
## same name, so scene scripts and tests share a single source of truth either way.
static func ensure(context: Object) -> Node:
	var tree: SceneTree = context as SceneTree
	if tree == null and context is Node and (context as Node).is_inside_tree():
		tree = (context as Node).get_tree()
	if tree == null:
		return null
	var existing := tree.root.get_node_or_null("CharacterState")
	if existing != null:
		return existing
	var created = (load("res://character_state.gd") as GDScript).new()
	created.name = "CharacterState"
	tree.root.add_child(created)
	return created
