extends RefCounted
const Intelligence := preload("res://godot/narrative/faction_intelligence.gd")

func _eq(label: String, got: Variant, expected: Variant) -> Array:
	return [label, got == expected, "got %s expected %s" % [got, expected]]

func run() -> Array:
	var rows: Array = []
	var intel := Intelligence.new()
	rows.append(_eq("human group registered", intel.register_faction({"id": "helsinki_clinic", "faction_type": "civil_society_knowledge", "name": "Clinic"}), true))
	rows.append(_eq("NHI bloc registered separately", intel.register_faction({"id": "orion", "faction_type": "nhi"}), true))
	rows.append(_eq("duplicate faction refused", intel.register_faction({"id": "helsinki_clinic", "faction_type": "corporate"}), false))
	rows.append(_eq("unverified Orion link recorded", intel.record_assertion({"id": "a1", "subject": "helsinki_clinic", "claim": "investor met an Orion broker", "source": "anonymous interview", "relation": "claimed_proxy", "evidence_status": "rumor"}), true))
	rows.append(_eq("unsupported faction refused", intel.record_assertion({"id": "a2", "subject": "unknown", "claim": "bad", "source": "witness", "evidence_status": "rumor"}), false))
	rows.append(_eq("rumor visible to investigator", intel.evidence_for("helsinki_clinic").size(), 1))
	rows.append(_eq("rumor is not verified", intel.evidence_for("helsinki_clinic", false).size(), 0))
	rows.append(_eq("cannot upgrade without evidence source", intel.update_status("a1", "verified", ""), false))
	rows.append(_eq("status can be evidence-backed", intel.update_status("a1", "verified", "contract + corroborated interview"), true))
	rows.append(_eq("verified evidence becomes visible", intel.evidence_for("helsinki_clinic", false).size(), 1))
	rows.append(_eq("provenance preserved", intel.assertions["a1"]["history"].size(), 1))
	rows.append(_eq("reputation changes", intel.adjust_reputation("helsinki_clinic", 13), true))
	rows.append(_eq("reputation clamped", intel.reputations["helsinki_clinic"], 10))
	var snapshot := intel.to_dict()
	var restored := Intelligence.new()
	rows.append(_eq("save restored", restored.from_dict(snapshot), true))
	rows.append(_eq("roundtrip deep equality", restored.to_dict(), snapshot))
	rows.append(_eq("invalid save refused", restored.from_dict({"version": 1, "factions": {}, "assertions": {"fake": {"subject": "missing"}}, "reputations": {}}), false))
	rows.append(_eq("bad save does not overwrite state", restored.to_dict(), snapshot))
	return rows
