## Cities Without Number — social costs: lifestyles, wages, bribes, pharmaceuticals.
##
## Transcribed from the SRD (CC0):
##   ``gear-vehicles-cyberware/lifestyles-wages-and-bribes/{lifestyle-costs,common-wages,bribe-costs}``
##   ``gear-vehicles-cyberware/pharmaceuticals-street-drugs``
##
## The three tables are related: a bribe is priced in multiples of the target's daily wage, and a
## lifestyle is priced in monthly cash that also moves the character's maximum System Strain.
##
## Effects are recorded as mechanical hooks, not as rulebook prose.
extends RefCounted
class_name CwnSocialCosts

##: Monthly lifestyle cost and its maximum-System-Strain modifier, cheapest first.
const LIFESTYLES := [
	{"id": "squatter", "cost": 0, "strain_modifier": -2, "summary": "abandoned building"},
	{"id": "slum", "cost": 300, "strain_modifier": -1, "summary": "dirty shared apartment"},
	{"id": "middle_class", "cost": 1000, "strain_modifier": 0, "summary": "nice rental"},
	{"id": "fine", "cost": 5000, "strain_modifier": 1, "summary": "clean, secure building"},
	{"id": "luxury", "cost": 20000, "strain_modifier": 2, "summary": "luxury living"},
]

##: Average daily earnings by worker type.
const WAGES := {
	"unskilled_laborer": 10,
	"low_level_ganger": 15,
	"streetwalker": 20,
	"street_stall_merchant": 25,
	"street_tech": 50,
	"street_bodyguard": 50,
	"entry_corp_worker": 30,
	"low_level_corp_lifer": 40,
	"street_cop": 100,
	"professional_companion": 200,
	"corp_hacker": 200,
	"corp_middle_manager": 250,
	"corp_cyberdoc": 250,
	"elite_bodyguard": 500,
	"gang_boss": 750,
	"branch_office_manager": 1000,
	"high_ranking_exec": 5000,
	"oligarchic_elite": 10000,
}

##: Bribe price as a multiple of the target's daily wage. `serious` marks favors that most NPCs will
##: not do for cash alone.
const BRIBES := {
	"look_other_way_minor": {"multiple": 2, "serious": false},
	"pass_information": {"multiple": 2, "serious": false},
	"small_favor_within_authority": {"multiple": 5, "serious": false},
	"blind_eye_trouble_possible": {"multiple": 14, "serious": true},
	"blind_eye_trouble_certain": {"multiple": 60, "serious": true},
	"favor_minor_backlash": {"multiple": 30, "serious": true},
	"favor_might_be_punished": {"multiple": 90, "serious": true},
	"favor_might_get_fired": {"multiple": 180, "serious": true},
}

##: Pharmaceuticals. `min_heal` of −1 is the SRD's "None" — anyone can administer it.
const DRUGS := [
	{"id": "avalanche", "name": "Avalanche", "cost": 100, "min_heal": 0, "contact_required": false},
	{"id": "boneshaker", "name": "Boneshaker", "cost": 10, "min_heal": -1, "contact_required": false},
	{"id": "chokeout", "name": "Chokeout", "cost": 50, "min_heal": -1, "contact_required": false},
	{"id": "control_delete", "name": "Control-Delete", "cost": 25, "min_heal": -1, "contact_required": false},
	{"id": "hellbender", "name": "Hellbender", "cost": 100, "min_heal": -1, "contact_required": false},
	{"id": "lurch", "name": "Lurch", "cost": 25, "min_heal": 0, "contact_required": false},
	{"id": "madeleine", "name": "Madeleine", "cost": 100, "min_heal": -1, "contact_required": false},
	{"id": "medical_prescription", "name": "Medical Prescription", "cost": 20, "min_heal": -1, "contact_required": false},
	{"id": "olympus", "name": "Olympus", "cost": 100, "min_heal": 0, "contact_required": false},
	{"id": "panacea", "name": "Panacea", "cost": 200, "min_heal": 1, "contact_required": false},
	{"id": "pillow", "name": "Pillow", "cost": 10, "min_heal": 0, "contact_required": false},
	{"id": "psycho", "name": "Psycho", "cost": 10, "min_heal": -1, "contact_required": false},
	{"id": "reset", "name": "Reset", "cost": 1000, "min_heal": -1, "contact_required": true},
	{"id": "sand", "name": "Sand", "cost": 2, "min_heal": -1, "contact_required": false},
	{"id": "trauma_patch", "name": "Trauma Patch", "cost": 50, "min_heal": -1, "contact_required": false},
	{"id": "window", "name": "Window", "cost": 200, "min_heal": 1, "contact_required": false},
]


static func lifestyle(lifestyle_id: String) -> Dictionary:
	for row in LIFESTYLES:
		if String(row["id"]) == lifestyle_id:
			return row
	return {}


## Monthly cash for a lifestyle and the maximum-System-Strain shift it applies.
static func lifestyle_cost(lifestyle_id: String) -> Dictionary:
	var row := lifestyle(lifestyle_id)
	if row.is_empty():
		return {"ok": false, "reason": "unknown lifestyle: %s" % lifestyle_id}
	return {
		"ok": true,
		"cost_per_month": int(row["cost"]),
		"strain_modifier": int(row["strain_modifier"]),
		"summary": String(row["summary"]),
	}


## Daily earnings for a named worker type.
static func wage(worker: String) -> Dictionary:
	if not WAGES.has(worker):
		return {"ok": false, "reason": "unknown worker type: %s" % worker}
	return {"ok": true, "daily": int(WAGES[worker])}


## Price of a favor, expressed as the target's daily wage times the SRD's multiple.
static func bribe_cost(worker: String, favor: String) -> Dictionary:
	var earnings := wage(worker)
	if not bool(earnings["ok"]):
		return earnings
	if not BRIBES.has(favor):
		return {"ok": false, "reason": "unknown favor: %s" % favor}
	var row: Dictionary = BRIBES[favor]
	return {
		"ok": true,
		"cost": int(earnings["daily"]) * int(row["multiple"]),
		"multiple": int(row["multiple"]),
		"serious_risk": bool(row["serious"]),
	}


static func drug(drug_id: String) -> Dictionary:
	for row in DRUGS:
		if String(row["id"]) == drug_id:
			return row
	return {}


## Whether a character's Heal skill lets them administer the chem. `min_heal` −1 means anyone can.
static func can_administer(heal_skill: int, drug_id: String) -> Dictionary:
	var row := drug(drug_id)
	if row.is_empty():
		return {"ok": false, "reason": "unknown chem: %s" % drug_id}
	var required := int(row["min_heal"])
	if required < 0:
		return {"ok": true, "allowed": true, "required": -1}
	return {"ok": true, "allowed": heal_skill >= required, "required": required}


## A chem that would push the user past their maximum System Strain grants no benefit, though its
## harmful effects still apply. This is the SRD's rule, and it is easy to invert.
static func strain_gate(system_strain: int, max_strain: int, drug_strain: int) -> Dictionary:
	var overflow := system_strain + drug_strain > max_strain
	return {
		"ok": true,
		"benefit": not overflow,
		"harmful_effects_still_apply": overflow,
		"overflow": overflow,
	}
