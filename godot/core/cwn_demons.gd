## Cities Without Number — Demons and Watchdogs (SRD §4.4).
##
## Demons are autonomous programs living on a network's server; watchdogs are human hackers holding a
## 24/7 presence. The rules that matter mechanically, and that are easy to get wrong:
##
## * A Demon's **HP** is depleted by Stun Avatar and similar effects; at zero it is **fragged** and does
##   nothing until it **reboots itself an hour** later — but it still occupies its node slot.
## * Its **skill bonus** is used for cyberspace checks *and* counts as its skill level for the damage
##   Stun or Kill Avatar does.
## * Demons **ignore network barriers** and **spend no Access** — they are assumed to have admin rights.
## * A network supports a maximum number of Demons, and a node a maximum number acting at once. Extra
##   Demons crowded into one node may only **Move Nodes** until space frees up.
## * A Demon processes a limited number of **command lines**, in priority order, skipping lines that do
##   not apply.
extends RefCounted
class_name CwnDemons

const REBOOT_MINUTES := 60

##: SRD §4.4 demon table: cost, command-line capacity, hit points, skill bonus.
const DEMONS := {
	"Tripwire": {"cost": 5000, "lines": 2, "hp": 3, "skill_bonus": 1},
	"Mastiff": {"cost": 10000, "lines": 4, "hp": 5, "skill_bonus": 2},
	"Siren": {"cost": 15000, "lines": 2, "hp": 8, "skill_bonus": 3},
	"Cataphract": {"cost": 25000, "lines": 3, "hp": 20, "skill_bonus": 3},
	"Ogre": {"cost": 50000, "lines": 4, "hp": 25, "skill_bonus": 2},
	"Headsman": {"cost": 100000, "lines": 4, "hp": 30, "skill_bonus": 3},
	"Hydra": {"cost": 200000, "lines": 7, "hp": 40, "skill_bonus": 4},
	"Nemesis": {"cost": 500000, "lines": 5, "hp": 50, "skill_bonus": 5},
}


static func demon(name: String) -> Dictionary:
	if not DEMONS.has(name):
		return {"ok": false, "reason": "unknown demon: %s" % name}
	var row: Dictionary = DEMONS[name]
	return {
		"ok": true,
		"name": name,
		"cost": int(row["cost"]),
		"lines": int(row["lines"]),
		"hp": int(row["hp"]),
		"skill_bonus": int(row["skill_bonus"]),
	}


## Demons are admin: barriers do not stop them and running a program costs no Access.
static func ignores_barriers() -> bool:
	return true


static func spends_access() -> bool:
	return false


## Whether a command list fits the Demon's line capacity. Lines are executed top to bottom, so a list
## that overflows is a programming error, not a runtime cap.
static func can_program(name: String, command_lines: int) -> Dictionary:
	var info := demon(name)
	if not bool(info["ok"]):
		return info
	return {
		"ok": true,
		"fits": command_lines <= int(info["lines"]),
		"capacity": int(info["lines"]),
		"overflow": maxi(0, command_lines - int(info["lines"])),
	}


## Damage to a Demon's code integrity. At zero it is fragged: inert for an hour, still holding its slot.
static func apply_damage(current_hp: int, damage: int) -> Dictionary:
	if damage < 0 or current_hp < 0:
		return {"ok": false, "reason": "hit points and damage cannot be negative"}
	var remaining := maxi(0, current_hp - damage)
	return {
		"ok": true,
		"hp": remaining,
		"fragged": remaining == 0,
		"reboot_minutes": REBOOT_MINUTES if remaining == 0 else 0,
		"slot_still_occupied": remaining == 0,
	}


## Damage dealt by Stun/Kill Avatar uses the Demon's skill bonus as its skill level.
static func avatar_damage_skill(name: String) -> Dictionary:
	var info := demon(name)
	if not bool(info["ok"]):
		return info
	return {"ok": true, "skill_level": int(info["skill_bonus"])}


## How many Demons may run in one node, and what happens to the extras.
static func node_capacity(max_per_node: int, present: int) -> Dictionary:
	if max_per_node < 0 or present < 0:
		return {"ok": false, "reason": "counts cannot be negative"}
	var over := maxi(0, present - max_per_node)
	return {
		"ok": true,
		"may_act": maxi(0, mini(present, max_per_node)),
		"crowded_out": over,
		"crowded_out_restricted_to_move": over > 0,
	}


## How many Demons a network's server can support at all.
static func network_capacity(max_demons: int, installed: int) -> Dictionary:
	if max_demons < 0 or installed < 0:
		return {"ok": false, "reason": "counts cannot be negative"}
	return {"ok": true, "allowed": installed <= max_demons, "free_slots": maxi(0, max_demons - installed)}


## A watchdog is a human presence, not a program: shifts are 24 hours, and it reacts with judgement a
## Demon does not have. Both facts are recorded as properties so a scenario cannot treat them alike.
static func watchdog_shift_hours() -> int:
	return 24


static func watchdog_is_intelligent() -> bool:
	return true
