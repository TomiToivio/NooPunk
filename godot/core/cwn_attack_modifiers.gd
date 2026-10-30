## Cities Without Number — attack-roll modifiers.
##
## Transcribed from the SRD (CC0), ``rules-of-the-game/combat/attacks-in-combat``. The attack roll
## itself lives in `cwn_combat_rules.gd`; this module is where its `other_modifier` comes from.
##
## Two rows of the SRD table are not penalties but impossibilities — a two-handed gun cannot be fired
## in melee, and a target whose position is unknown cannot be shot at. Folding those into a number
## would let a caller "shoot anyway at −4", so they are reported separately and block the attack.
extends RefCounted
class_name CwnAttackModifiers

##: SRD attack-roll modifier table. Negative numbers are penalties.
const TABLE := {
	"target_prone_not_in_melee": -2,
	"target_prone_adjacent": 2,
	"beyond_normal_range": -2,
	"attacker_prone_melee": -4,
	"target_half_cover": -2,
	"target_almost_full_cover": -4,
	"thrown_while_in_melee": -4,
	"one_handed_gun_in_melee": -4,
	"target_unseen_position_known": -4,
}

##: Circumstances the SRD marks N/A: no attack is possible, so there is no modifier to apply.
const IMPOSSIBLE := {
	"two_handed_gun_in_melee": "a two-handed gun cannot be fired while in melee",
	"target_unseen_position_unknown": "the target's position is unknown, so it cannot be attacked",
}


static func is_impossible(circumstance: String) -> bool:
	return IMPOSSIBLE.has(circumstance)


## Sum the SRD modifiers for the named circumstances.
##
## Returns `{ok, modifier, blocked, unknown}`. `ok` is false when a circumstance makes the attack
## impossible, or when an id is not in the SRD table — a typo must not become a silent zero.
static func modifier(circumstances: Array) -> Dictionary:
	var total := 0
	var blocked: Array = []
	var unknown: Array = []
	for circumstance in circumstances:
		var key := String(circumstance)
		if IMPOSSIBLE.has(key):
			blocked.append(String(IMPOSSIBLE[key]))
		elif TABLE.has(key):
			total += int(TABLE[key])
		else:
			unknown.append(key)
	return {
		"ok": blocked.is_empty() and unknown.is_empty(),
		"modifier": total if blocked.is_empty() else 0,
		"blocked": blocked,
		"unknown": unknown,
	}
