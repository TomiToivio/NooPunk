## CWN SRD §3.2.2 Common Wages. Exact daily earnings from the published SRD.
## Source: https://cwn.quadrifons.com/gear-vehicles-cyberware/lifestyles-wages-and-bribes/common-wages/
extends RefCounted
class_name CwnWages

const DAILY := {
	"unskilled_street_laborer": 10,
	"low_level_ganger_or_street_thug": 15,
	"common_streetwalker": 20,
	"petty_street_stall_merchant": 25,
	"capable_street_tech_or_cyberdoc": 50,
	"competent_street_bodyguard": 50,
	"entry_level_corp_worker": 30,
	"low_level_corp_lifer": 40,
	"street_cop_or_skilled_corp_worker": 100,
	"professional_companion": 200,
	"corp_employed_hacker": 200,
	"corp_middle_manager": 250,
	"corp_sponsored_cyberdoc": 250,
	"elite_or_well_known_bodyguard": 500,
	"successful_gang_boss": 750,
	"corp_branch_office_manager": 1000,
	"high_ranking_corp_exec": 5000,
	"oligarchic_elite_of_a_city": 10000,
}

static func daily_earnings(worker: String) -> Dictionary:
	if not DAILY.has(worker):
		return {"ok": false, "reason": "unknown worker", "worker": worker}
	return {"ok": true, "daily_earnings": int(DAILY[worker])}

static func hire_cost(worker: String, days: int) -> Dictionary:
	if days < 0:
		return {"ok": false, "reason": "days cannot be negative"}
	var result := daily_earnings(worker)
	if not result["ok"]:
		return result
	return {"ok": true, "cost": result["daily_earnings"] * days}
