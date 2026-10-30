class_name CwnParty
extends RefCounted

## The active party: one player character plus up to three companions, 1..4 members (#806).
##
## The design change this encodes: **the player is not Romppainen.** The PC is a level-1 field agent
## of Suojelupoliisi, Europol or UNSA, created by the player; Romppainen is an experienced NPC who
## joins *some* missions as a controllable companion. So the party size is not a constant — solo,
## a pair, a trio and a full squad all have to work — and the PC must survive every composition
## change with identity, progression and inventory intact.
##
## Two rules that are easy to get wrong and are enforced here rather than documented:
##
## - **The PC cannot leave the party.** A companion joins and leaves; the protagonist is the thing
##   the save is about. Removing the PC is a bug, not a design choice.
## - **Exactly one member is controlled at a time**, and control may pass to a companion without
##   changing who the PC is. "Controllable" is a permission on the member, not a promotion.
const VERSION := 1
const MIN_MEMBERS := 1
const MAX_MEMBERS := 4
const AGENCIES := ["Suojelupoliisi", "Europol", "UNSA"]

var members: Array = []
var controlled_id: String = ""

func size() -> int:
	return members.size()

func is_empty() -> bool:
	return members.is_empty()

func has(id: String) -> bool:
	return not find(id).is_empty()

func find(id: String) -> Dictionary:
	for member in members:
		if str(member.get("id", "")) == id:
			return member
	return {}

## The persistent player character. There is exactly one, always.
func player_character() -> Dictionary:
	for member in members:
		if bool(member.get("is_pc", false)):
			return member
	return {}

func companions() -> Array:
	var out: Array = []
	for member in members:
		if not bool(member.get("is_pc", false)):
			out.append(member)
	return out

## Add a member, refusing anything that would break the 1..4 constraint or duplicate an id.
func add_member(spec: Dictionary) -> Dictionary:
	var id := str(spec.get("id", "")).strip_edges()
	if id.is_empty():
		return {"ok": false, "reason": "member_needs_an_id"}
	if has(id):
		return {"ok": false, "reason": "member_already_in_party", "id": id}
	if members.size() >= MAX_MEMBERS:
		return {"ok": false, "reason": "party_is_full", "max": MAX_MEMBERS}
	var level := int(spec.get("level", 1))
	if level < 1:
		return {"ok": false, "reason": "level_must_be_at_least_1"}
	var is_pc := bool(spec.get("is_pc", false))
	if is_pc and not player_character().is_empty():
		return {"ok": false, "reason": "party_already_has_a_player_character"}
	var member := spec.duplicate(true)
	member["id"] = id
	member["level"] = level
	member["is_pc"] = is_pc
	member["controllable"] = bool(spec.get("controllable", true))
	if not member.has("inventory"):
		member["inventory"] = []
	members.append(member)
	if controlled_id.is_empty() or is_pc:
		controlled_id = id
	return {"ok": true, "id": id, "size": members.size()}

## A companion leaves. The player character may not.
func remove_member(id: String) -> Dictionary:
	if not has(id):
		return {"ok": false, "reason": "not_in_party", "id": id}
	if bool(find(id).get("is_pc", false)):
		return {"ok": false, "reason": "the_player_character_cannot_leave_the_party"}
	if members.size() <= MIN_MEMBERS:
		return {"ok": false, "reason": "party_would_be_empty"}
	for index in members.size():
		if str(members[index]["id"]) == id:
			members.remove_at(index)
			break
	if controlled_id == id:
		var pc := player_character()
		controlled_id = str(pc.get("id", "")) if not pc.is_empty() else str(members[0]["id"])
	return {"ok": true, "size": members.size(), "controlled_id": controlled_id}

## Control switches to another member. Companions may be controlled; the PC is not demoted by it.
func set_controlled(id: String) -> Dictionary:
	if not has(id):
		return {"ok": false, "reason": "not_in_party", "id": id}
	if not bool(find(id).get("controllable", true)):
		return {"ok": false, "reason": "member_is_not_controllable", "id": id}
	controlled_id = id
	return {"ok": true, "controlled_id": id}

func controlled() -> Dictionary:
	return find(controlled_id)

func to_dict() -> Dictionary:
	return {
		"version": VERSION,
		"members": members.duplicate(true),
		"controlled_id": controlled_id,
	}

## Load, validating before mutating: a party with no PC, two PCs, or an out-of-range size is a
## corrupt save, and applying half of it would be worse than refusing it.
func from_dict(data: Dictionary) -> bool:
	if int(data.get("version", -1)) != VERSION:
		return false
	if typeof(data.get("members", null)) != TYPE_ARRAY:
		return false
	var incoming: Array = data["members"]
	if incoming.size() < MIN_MEMBERS or incoming.size() > MAX_MEMBERS:
		return false
	var seen := {}
	var pc_count := 0
	for entry in incoming:
		if typeof(entry) != TYPE_DICTIONARY:
			return false
		var id := str(entry.get("id", ""))
		if id.is_empty() or seen.has(id):
			return false
		seen[id] = true
		if bool(entry.get("is_pc", false)):
			pc_count += 1
		if int(entry.get("level", 0)) < 1:
			return false
	if pc_count != 1:
		return false
	var control := str(data.get("controlled_id", ""))
	if control.is_empty() or not seen.has(control):
		control = str(incoming[0].get("id", ""))
	for entry in incoming:
		if bool(entry.get("is_pc", false)):
			control = str(entry["id"]) if control.is_empty() else control
	members = incoming.duplicate(true)
	controlled_id = control if seen.has(control) else str(incoming[0]["id"])
	return true
