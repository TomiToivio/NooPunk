extends RefCounted

## #913: two selectable nodes at start, everything else locked, and a grounded Helsinki.
const Map := preload("res://godot/core/city_map.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [got, want]]

func run() -> Array:
	var rows: Array = []

	var ids: Array = Map.selectable_ids()
	ids.sort()
	var expected: Array = ["home_helsinginkatu", "unsa_hq_ratakatu"]
	expected.sort()
	var starts: Array = Map.start_nodes()
	starts.sort()

	rows.append(_eq("exactly two selectable nodes", Map.selectable().size(), 2))
	rows.append(_eq("selectable ids", ids, expected))
	rows.append(_eq("start nodes match", starts, expected))

	var home: Dictionary = Map.node("home_helsinginkatu")
	var hq: Dictionary = Map.node("unsa_hq_ratakatu")
	var home_name := String(home.get("name", ""))
	var hq_name := String(hq.get("name", ""))
	var home_district := String(home.get("district", ""))
	var hq_summary := String(hq.get("summary", ""))

	rows.append(["home is on Helsinginkatu", home_name.contains("Helsinginkatu"), home_name])
	rows.append(["HQ is on Ratakatu", hq_name.contains("Ratakatu"), hq_name])
	rows.append(["home is in Sornainen/Kallio", home_district.contains("Kallio"), home_district])
	rows.append(["HQ is the former Suojelupoliisi building", hq_summary.contains("Suojelupoliisi"), hq_summary])

	rows.append(_eq("travelling home is allowed", Map.travel("home_helsinginkatu")["ok"], true))
	rows.append(_eq("travelling to HQ is allowed", Map.travel("unsa_hq_ratakatu")["ok"], true))

	var locked: Dictionary = Map.travel("market_square")
	var locked_reason := String(locked.get("reason", ""))
	rows.append(_eq("a locked node is refused", locked["ok"], false))
	rows.append(["the refusal says why", locked_reason.contains("not yet discovered"), locked_reason])
	rows.append(_eq("an unknown node is refused", Map.travel("atlantis")["ok"], false))

	var total_nodes := Map.nodes().size()
	var selectable_count := Map.selectable().size()
	var counts := "%d nodes, %d selectable" % [total_nodes, selectable_count]
	rows.append(["there are locked nodes to find later", total_nodes > selectable_count, counts])

	rows.append(_eq("no forbidden terms in node text", Map.forbidden_terms_in_text(), []))

	var district_count := Map.districts().size()
	rows.append(["the map spans more than one district", district_count >= 2, str(district_count)])

	return rows
