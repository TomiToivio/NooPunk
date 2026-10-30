class_name NoopunkParty
extends RefCounted

## Custom NoöPunk party layer over the Without Number rules kernel.
## Does not decide stat generation, class powers or narrative recruitment automatically.
const MAX_MEMBERS := 4
const AGENCIES := ["Suojelupoliisi", "Europol", "UNSA"]
const FORMAT_VERSION := 1

var protagonist: Dictionary = {}
var members: Array[Dictionary] = []
var selected_id: String = ""

func create_agent(id: String, agent_name: String, agency: String, sheet: Dictionary = {}) -> bool:
	if not protagonist.is_empty() or id.is_empty() or agent_name.strip_edges().is_empty() or not AGENCIES.has(agency):
		return false
	protagonist = sheet.duplicate(true)
	protagonist.merge({"id": id, "name": agent_name, "agency": agency, "role": "law_enforcer", "level": 1, "kind": "pc"}, true)
	members = [protagonist.duplicate(true)]
	selected_id = id
	return true

func join(companion: Dictionary) -> bool:
	var id := str(companion.get("id", ""))
	if protagonist.is_empty() or id.is_empty() or members.size() >= MAX_MEMBERS or has_member(id):
		return false
	if int(companion.get("level", 0)) < 1:
		return false
	var entry := companion.duplicate(true)
	entry["kind"] = "npc"
	members.append(entry)
	return true

func has_member(id: String) -> bool:
	for member in members:
		if str(member.get("id", "")) == id:
			return true
	return false

func leave(id: String) -> bool:
	if id == str(protagonist.get("id", "")):
		return false
	for i in range(members.size()):
		if str(members[i].get("id", "")) == id:
			members.remove_at(i)
			if selected_id == id:
				selected_id = str(protagonist["id"])
			return true
	return false

func select_member(id: String) -> bool:
	if not has_member(id):
		return false
	selected_id = id
	return true

func selected() -> Dictionary:
	for member in members:
		if str(member.get("id", "")) == selected_id:
			return member.duplicate(true)
	return {}

func to_dict() -> Dictionary:
	return {"version": FORMAT_VERSION, "protagonist": protagonist.duplicate(true),
		"members": members.duplicate(true), "selected_id": selected_id}

func from_dict(data: Dictionary) -> bool:
	if int(data.get("version", -1)) != FORMAT_VERSION:
		return false
	var pc: Variant = data.get("protagonist")
	var roster: Variant = data.get("members")
	var selected: String = str(data.get("selected_id", ""))
	if not pc is Dictionary or not roster is Array:
		return false
	if int(pc.get("level", 0)) != 1 or str(pc.get("kind", "")) != "pc" or not AGENCIES.has(str(pc.get("agency", ""))):
		return false
	if roster.size() < 1 or roster.size() > MAX_MEMBERS:
		return false
	var seen := {}
	var pc_count := 0
	for item in roster:
		if not item is Dictionary:
			return false
		var id := str(item.get("id", ""))
		if id.is_empty() or seen.has(id):
			return false
		seen[id] = true
		if id == str(pc.get("id", "")):
			pc_count += 1
			if item != pc:
				return false
		elif int(item.get("level", 0)) < 1 or str(item.get("kind", "")) != "npc":
			return false
	if pc_count != 1 or not seen.has(selected):
		return false
	protagonist = pc.duplicate(true)
	members.clear()
	for item in roster:
		members.append(item.duplicate(true))
	selected_id = selected
	return true
