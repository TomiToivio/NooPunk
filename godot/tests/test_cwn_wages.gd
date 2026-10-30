## Regression fixtures for all eighteen published CWN SRD §3.2.2 daily wages.
extends RefCounted
const W := preload("res://godot/core/cwn_wages.gd")
const EXPECTED := {
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
func run() -> Array:
	var rows: Array = []
	rows.append(["complete SRD wage table has 18 entries", W.DAILY.size() == 18, "expected 18"])
	for worker in EXPECTED:
		var actual := W.daily_earnings(worker)
		rows.append(["SRD daily wage: " + worker, actual.get("daily_earnings", -1) == EXPECTED[worker], str(actual)])
	rows.append(["unknown worker rejected", not W.daily_earnings("dragon")["ok"], "unknown must not silently price at zero"])
	rows.append(["three-day hire cost", W.hire_cost("competent_street_bodyguard", 3).get("cost", -1) == 150, "3 x 50"])
	rows.append(["negative hire duration rejected", not W.hire_cost("competent_street_bodyguard", -1)["ok"], "negative"])
	return rows
