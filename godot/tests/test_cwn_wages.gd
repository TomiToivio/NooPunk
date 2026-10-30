extends RefCounted

## #873: common wages, SRD 3.2.2.
const Wages := preload("res://godot/core/cwn_wages.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	rows.append(_eq("eighteen published roles", Wages.all().size(), 18))
	rows.append(_eq("unskilled laborer is 10 a day", Wages.daily("unskilled_laborer"), 10))
	rows.append(_eq("street cop is 100", Wages.daily("street_cop"), 100))
	rows.append(_eq("corp hacker is 200", Wages.daily("corp_hacker"), 200))
	rows.append(_eq("gang boss is 750", Wages.daily("gang_boss"), 750))
	rows.append(_eq("oligarch is 10000", Wages.daily("oligarch"), 10000))
	rows.append(_eq("entry corp worker is 30, not a typo for 300", Wages.daily("entry_corp_worker"), 30))

	# two roles share a price, and that is the SRD's own overlap, not a data error
	rows.append(_eq("street tech is 50", Wages.daily("street_tech"), 50))
	rows.append(_eq("street bodyguard is also 50", Wages.daily("street_bodyguard"), 50))

	# durations are computed, never stored twice
	rows.append(_eq("three days of a laborer", Wages.for_days("unskilled_laborer", 3), 30))
	rows.append(_eq("one day is the daily rate", Wages.for_days("oligarch", 1), 10000))
	rows.append(_eq("zero days costs nothing", Wages.for_days("street_cop", 0), 0))

	# refusals rather than plausible defaults
	rows.append(_eq("an unknown role earns nothing and warns", Wages.daily("not_a_role"), 0))
	rows.append(_eq("an unknown role's entry is empty", Wages.entry("not_a_role"), {}))
	rows.append(_eq("names resolve for prose lookups",
		Wages.by_name("Successful gang boss").get("id"), "gang_boss"))

	# bribes multiply the daily wage; the multiplier is the SRD's, passed in
	rows.append(_eq("a x2 bribe for a street cop", Wages.bribe("street_cop", 2), 200))
	rows.append(_eq("a x5 bribe for a middle manager", Wages.bribe("corp_middle_manager", 5), 1250))

	# every role must carry a positive wage
	for row in Wages.all():
		var ok: bool = int(row.get("daily", 0)) > 0
		rows.append(["%s has a positive wage" % row.get("id"), ok, str(row.get("daily"))])

	return rows
