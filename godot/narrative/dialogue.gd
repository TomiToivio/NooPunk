## Dialogue runner for the slice (#631): a tiny graph walker over `dialogue.json`.
##
## Vocabulary (all data, no code changes needed to author a new conversation):
##   node:   { speaker, text, choices?: [...], next?: node_id|null, effects?: {set_flags, add_evidence,
##             add_journal} }
##   choice: { text, next?: node_id, effects?: {...}, check?: {attribute, skill, difficulty,
##             success_node, failure_node} }
##
## A choice with a `check` resolves through GameState.resolve_check, so the dice, the modifier and the
## target come from the approved kernel and the roll is shown to the player. Effects run before the
## branch is taken, which is what lets a successful check both record evidence and change the scene.
class_name DialogueRunner
extends RefCounted

var nodes: Dictionary = {}
var state: Node
var current_id: String = ""
var last_result: Dictionary = {}

func _init(dialogue_nodes: Dictionary, game_state: Node) -> void:
	nodes = dialogue_nodes
	state = game_state

func has_node(node_id: String) -> bool:
	return nodes.has(node_id)

## Starts a conversation at the NPC's entry node and returns that node.
func start(node_id: String) -> Dictionary:
	current_id = node_id
	return current()

func current() -> Dictionary:
	if current_id == "" or not nodes.has(current_id):
		return {}
	var node: Dictionary = (nodes[current_id] as Dictionary).duplicate(true)
	node["id"] = current_id
	return node

## The node's choices, each annotated with whether its check would be attempted. Conditions live in the
## data, so a locked choice is still visible — the player sees the door, not a hidden one.
func choices() -> Array:
	var node := current()
	var out: Array = []
	for choice in node.get("choices", []):
		out.append(choice)
	return out

## Takes a choice: applies its effects, resolves its check if it has one, and moves the conversation.
## Returns the node reached (empty when the conversation ends).
func choose(index: int) -> Dictionary:
	var node := current()
	var offered: Array = node.get("choices", [])
	if index < 0 or index >= offered.size():
		push_error("DialogueRunner: no choice %d at node %s" % [index, current_id])
		return {}
	var choice: Dictionary = offered[index]
	_apply(choice.get("effects", {}))

	if choice.has("check"):
		var spec: Dictionary = choice["check"]
		var result: Dictionary = state.resolve_check(
			String(spec.get("attribute", "INT")),
			String(spec.get("skill", "")),
			int(spec.get("difficulty", 8))
		)
		last_result = result
		var branch := String(spec.get("success_node", "")) if bool(result["success"]) else String(spec.get("failure_node", ""))
		return _advance(branch)

	if choice.has("next"):
		return _advance(String(choice["next"]))

	# A choice with neither a check nor a next ends the conversation.
	current_id = ""
	return {}

func _advance(next_id: String) -> Dictionary:
	if next_id == "" or next_id == "null":
		current_id = ""
		return {}
	current_id = next_id
	# A node's own effects fire on entry. That is what lets a destination carry the consequence of the
	# choice that led to it: `doctor_record` grants the evidence, not the button that opened it.
	if nodes.has(current_id):
		_apply((nodes[current_id] as Dictionary).get("effects", {}))
	return current()

func _apply(effects: Dictionary) -> void:
	for flag in effects.get("set_flags", []):
		state.set_flag(String(flag))
	for evidence_id in effects.get("add_evidence", []):
		state.add_evidence(String(evidence_id))
	if effects.has("add_journal"):
		state.add_journal(String(effects["add_journal"]))
