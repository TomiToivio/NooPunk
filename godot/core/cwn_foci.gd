## Cities Without Number — the Foci engine (SRD 1.6.0–1.6.2, 2.7.1.6).
##
## Ported from the verified Python layer (`src/rules/cwn_foci.py`) so the Godot game and the Python
## tooling cannot disagree about how many picks a character has.
##
## This is the *engine*, not the catalogue prose: how many picks exist, which Foci have a second level,
## when a new pick is earned, and the gear budgets three Foci grant. The benefit text stays in the SRD
## and in the rulebook; copying it here would create a second copy to keep in sync.
extends RefCounted
class_name CwnFoci

##: SRD 2.7.1.6 — a PC adds a Focus level or a new Focus at these character levels.
const PICK_LEVELS := [2, 5, 7, 10]

##: SRD 1.6.2 — free-gear budget by character level: [vehicle, drone].
const GEAR_BUDGET := {
	1: [5000, 1000],
	2: [10000, 5000],
	3: [15000, 10000],
	4: [20000, 15000],
	5: [30000, 20000],
	6: [40000, 25000],
	7: [60000, 35000],
	8: [80000, 45000],
	9: [100000, 60000],
	10: [200000, 80000],
}

##: The three Foci that carry a gear budget, and which column they use.
const GEAR_BUDGET_FOCI := {
	"Ace Driver": "vehicle",
	"Roamer": "vehicle",
	"Drone Pilot": "drone",
}

##: Every Focus and how many levels it has. The SRD's typographic apostrophe is kept for Sniper's Eye.
const FOCUS_LEVELS := {
	"Ace Driver": 2,
	"Alert": 2,
	"All Natural": 1,
	"Armsmaster": 2,
	"Assassin": 2,
	"Authority": 2,
	"Close Combatant": 2,
	"Cyberdoc": 2,
	"Deadeye": 2,
	"Diplomat": 2,
	"Drone Pilot": 2,
	"Expert Programmer": 2,
	"Healer": 2,
	"Henchkeeper": 2,
	"Many Faces": 1,
	"Pop Idol": 2,
	"Roamer": 2,
	"Safe Haven": 2,
	"Shocking Assault": 2,
	"Sniper's Eye": 2,
	"Specialist": 2,
	"Tinker": 2,
	"Unarmed Combatant": 2,
	"Unique Gift": 1,
	"Unregistered": 1,
	"Whirlwind Assault": 2,
}


## A new character may take one Focus, plus one more with the Focused Edge.
static func new_character_picks(has_focused_edge: bool = false) -> int:
	return 2 if has_focused_edge else 1


## Focus picks earned from levelling, by the SRD's pick levels.
static func advancement_picks(character_level: int) -> Dictionary:
	if character_level < 1:
		return {"ok": false, "reason": "character level starts at 1"}
	var earned := 0
	for level in PICK_LEVELS:
		if level <= character_level:
			earned += 1
	return {"ok": true, "picks": earned}


## Creation picks plus every advancement pick earned so far.
static func total_picks(character_level: int, has_focused_edge: bool = false) -> Dictionary:
	var advanced := advancement_picks(character_level)
	if not bool(advanced["ok"]):
		return advanced
	return {"ok": true, "picks": new_character_picks(has_focused_edge) + int(advanced["picks"])}


static func max_level(focus: String) -> Dictionary:
	if not FOCUS_LEVELS.has(focus):
		return {"ok": false, "reason": "unknown Focus: %s" % focus}
	return {"ok": true, "levels": int(FOCUS_LEVELS[focus])}


## Whether spending a pick here is legal. Levels cannot be skipped, and a one-level Focus refuses a
## second pick rather than silently capping it.
static func can_take_level(focus: String, current_level: int = 0) -> Dictionary:
	if current_level < 0:
		return {"ok": false, "reason": "current level cannot be negative"}
	var cap := max_level(focus)
	if not bool(cap["ok"]):
		return cap
	return {"ok": true, "allowed": current_level < int(cap["levels"]), "max": int(cap["levels"])}


## The Focus's new level after spending a pick.
static func take_level(focus: String, current_level: int = 0) -> Dictionary:
	var legal := can_take_level(focus, current_level)
	if not bool(legal["ok"]) or not bool(legal["allowed"]):
		return {"ok": false, "reason": "%s is at level %d of %s; no further levels exist" % [
			focus, current_level, str(legal.get("max", "?"))]}
	return {"ok": true, "level": current_level + 1}


## The free-gear budget a Focus grants at a character level.
static func gear_budget(character_level: int, kind: String = "vehicle") -> Dictionary:
	if kind != "vehicle" and kind != "drone":
		return {"ok": false, "reason": "kind must be vehicle or drone"}
	if not GEAR_BUDGET.has(character_level):
		return {"ok": false, "reason": "the SRD table covers character levels 1-10"}
	var row: Array = GEAR_BUDGET[character_level]
	return {"ok": true, "budget": int(row[0] if kind == "vehicle" else row[1])}


## The budget a named Focus grants, or a refusal for a Focus that grants none.
static func budget_for_focus(focus: String, character_level: int) -> Dictionary:
	if not GEAR_BUDGET_FOCI.has(focus):
		return {"ok": false, "reason": "%s grants no gear budget" % focus}
	return gear_budget(character_level, String(GEAR_BUDGET_FOCI[focus]))
