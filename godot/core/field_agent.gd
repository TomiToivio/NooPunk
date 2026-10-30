## The player character (#809): a level-1 field agent created on top of the Without Number kernel.
##
## NoöPunk keeps CWN/SWN as its mechanical floor and customizes on top of it. This factory produces a
## sheet **shaped exactly like `godot/scenarios/mvp_romppainen/character.json`**, so the same session,
## combat, hacking and scene code consumes a created agent without knowing that Romppainen used to be
## the avatar. The customization itself — backgrounds, edges, foci, NoöPunk skills — is authored in
## the tabletop layer first and only then wired here.
##
## The agencies are the three the campaign premise names: Suojelupoliisi (domestic), Europol
## (European) and UNSA (the setting's international body).
##
## **Hit points follow the tabletop rule: 1d6 + the CON modifier at level 1.** `godot/core`
## `hit_points(level, con, rolls)` and `src/godot` `max_hit_points(roll, con_mod, htk)` still disagree
## about the base, which is recorded as blocked on #791/#809; this factory computes the level-1 total
## itself rather than import either convention into new content.
extends RefCounted
class_name NoopunkFieldAgent

const Character := preload("res://godot/core/cwn_character.gd")
const Party := preload("res://godot/core/party.gd")

const AGENCIES := ["Suojelupoliisi", "Europol", "UNSA"]
const STARTING_LEVEL := 1
## A law enforcer starts with these trained at rank 0 unless the build says otherwise.
const DEFAULT_SKILLS := {"Investigate": 0, "Notice": 0, "Shoot": 0}
const SIDEARM := {
	"name": "sidearm", "weapon_kind": "ranged", "attribute": "DEX", "combat_rank": 0,
	"attack_bonus": 1, "damage": [1, 6, 0], "trauma_rating": 1, "trauma_target": 6,
	"shock_value": 0, "shock_ac": -1, "ammo": 8, "ammo_max": 8, "lethal": true,
}

## Returns {"ok": true, "sheet": {...}} or {"ok": false, "reason": ...}.
## Either the eighteen dice or an array assignment is required — never both, never neither.
static func create(member_name: String, agency: String, rolls: Array = [],
		assignment: Dictionary = {}, skills: Dictionary = {}, hp_roll: int = 0) -> Dictionary:
	if not (agency in AGENCIES):
		return {"ok": false, "reason": "unknown_agency"}
	if member_name.strip_edges().is_empty():
		return {"ok": false, "reason": "the_agent_needs_a_name"}
	var scores: Dictionary = {}
	if assignment.is_empty():
		if rolls.size() != 18:
			return {"ok": false, "reason": "six_sets_of_three_d6"}
		var rolled: Dictionary = Character.roll_attributes(rolls)
		if not bool(rolled.get("ok", false)):
			return {"ok": false, "reason": String(rolled.get("reason", "invalid_attributes"))}
		scores = rolled["scores"]
	else:
		var assigned: Dictionary = Character.assign_array(assignment)
		if not bool(assigned.get("ok", false)):
			return {"ok": false, "reason": String(assigned.get("reason", "invalid_assignment"))}
		scores = assigned["scores"]
	if hp_roll != 0 and (hp_roll < 1 or hp_roll > 6):
		return {"ok": false, "reason": "hit_points_are_rolled_on_1d6"}
	var die := hp_roll if hp_roll != 0 else randi_range(1, 6)
	var constitution := int(scores.get("CON", 10))
	var con_modifier: int = Character.effective_modifier(constitution)
	var hit_points := maxi(1, die + con_modifier)
	var trained := DEFAULT_SKILLS.duplicate()
	trained.merge(skills, true)
	return {
		"ok": true,
		"sheet": {
			"id": "pc", "name": member_name.strip_edges(), "agency": agency,
			"kind": "pc", "role": "law_enforcer", "level": STARTING_LEVEL,
			"attributes": scores,
			"modifiers": {
				"STR": Character.effective_modifier(int(scores.get("STR", 10))),
				"DEX": Character.effective_modifier(int(scores.get("DEX", 10))),
				"CON": con_modifier,
				"INT": Character.effective_modifier(int(scores.get("INT", 10))),
				"WIS": Character.effective_modifier(int(scores.get("WIS", 10))),
				"CHA": Character.effective_modifier(int(scores.get("CHA", 10))),
			},
			"hp_max": hit_points, "hp_roll": die,
			"ac": 10 + Character.effective_modifier(int(scores.get("DEX", 10))),
			"ac_melee": 10 + Character.effective_modifier(int(scores.get("DEX", 10))),
			"ac_ranged": 10 + Character.effective_modifier(int(scores.get("DEX", 10))),
			"attack": SIDEARM.duplicate(true),
			"skills": trained,
			"saves": Character.saves(STARTING_LEVEL, scores),
			"strain": {"max": constitution, "used": 0},
			"psionics": {"disciplines": {}, "packages": []},
			"choices": [], "gear": [SIDEARM["name"]], "inventory": {},
			"source": "NoöPunk character creation (level-1 law enforcer) over CWN attributes, saves, skills and gear; customized backgrounds and edges are added by the tabletop layer.",
		},
	}
