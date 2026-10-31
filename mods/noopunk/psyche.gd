## Noösphere exposure and Psyche — a NoöPunk overlay (#897).
##
## This module is the worked example of the rule in `docs/design/FOUNDATIONAL_LOCK_897.md`: an overlay
## reads and returns state, and never computes core CWN resolution. It does not roll dice, does not touch
## attributes, skills, saves or hit points, and does not import from `godot/core/`.
##
## Framing, because it is easy to get wrong: exposure to the noösphere is **not** mental illness. It is a
## narrative condition with consequences — awe, obsession, dissociation, conviction, dread — and the system
## tracks pressure and consequence rather than diagnosing anyone. Nothing here pathologises a character
## or makes a claim about real psychiatry.
extends RefCounted
class_name NoopunkPsyche

##: Exposure pressure. Resets only through recovery; it is a narrative meter, not a health bar.
const MAX_EXPOSURE := 10

##: What an exposure tier means at the table. Codes, not prose: the narrative layer owns the words.
const CONSEQUENCES := {
	0: "calm",
	1: "attunement",
	2: "intrusion",
	3: "dissociation",
	4: "overwhelm",
}

##: Active PSI is an OPEN DESIGN QUESTION in #897. Until playtesting decides, the default answer is
##: "undecided", and callers must not treat it as granted.
const ACTIVE_PSI_DEFAULT := "undecided"


## Apply exposure. `resilience` dampens the gain; it never turns exposure negative.
static func expose(exposure: int, amount: int, resilience: int = 0) -> Dictionary:
	if exposure < 0 or amount < 0:
		return {"ok": false, "reason": "exposure and amount cannot be negative"}
	var gain := maxi(0, amount - maxi(0, resilience))
	var next := mini(MAX_EXPOSURE, exposure + gain)
	return {
		"ok": true,
		"exposure": next,
		"gained": next - exposure,
		"tier": tier(next),
		"consequence": CONSEQUENCES[tier(next)],
		# A consequence is narrative; it is not damage and does not reduce hit points.
		"narrative_event": next > exposure,
	}


## Recovery lowers exposure. It cannot go below zero, and it does not erase what already happened —
## the narrative layer keeps the history.
static func recover(exposure: int, amount: int = 1) -> Dictionary:
	if exposure < 0 or amount < 0:
		return {"ok": false, "reason": "exposure and amount cannot be negative"}
	var next := maxi(0, exposure - amount)
	return {"ok": true, "exposure": next, "recovered": exposure - next, "tier": tier(next),
		"consequence": CONSEQUENCES[tier(next)]}


## Tier 0–4 from exposure 0–10.
static func tier(exposure: int) -> int:
	if exposure <= 0:
		return 0
	if exposure <= 3:
		return 1
	if exposure <= 6:
		return 2
	if exposure <= 8:
		return 3
	return 4


## At overwhelm the character is not "broken": they are in a scene the table must address. The overlay
## reports that a narrative beat is owed rather than imposing a mechanical penalty.
static func owes_narrative_beat(exposure: int) -> bool:
	return tier(exposure) >= 4


## Whether the character may attempt active PSI. Until #897's open question is resolved by playtesting,
## this returns the undecided marker rather than a permission.
static func active_psi_status(campaign_flag: String = "") -> Dictionary:
	if campaign_flag.is_empty():
		return {"ok": true, "status": ACTIVE_PSI_DEFAULT,
			"note": "open design question: passive/minor PSI for the PC, stronger active PSI with NPCs"}
	if campaign_flag != "allowed" and campaign_flag != "denied":
		return {"ok": false, "reason": "campaign flag must be allowed or denied"}
	return {"ok": true, "status": campaign_flag, "note": ""}
