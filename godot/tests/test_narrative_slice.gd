## Helsinki narrative slice (#897): travel gating, discovery, clues, party cap, CWN checks and
## abstract CWN combat, save/load. No renderer needed.
extends RefCounted

const Session := preload("res://godot/narrative/helsinki_session.gd")

class FakeRules:
	extends RefCounted
	var skill_ok := true
	var hit := true
	func skill_check(_attr: int, _rank: int, _difficulty: int) -> Dictionary:
		return {"success": skill_ok}
	func attack_roll(_attr: int, _rank: int, _bonus: int, _ac: int) -> Dictionary:
		return {"hit": hit}


func _ok(name: String, condition: bool, detail := "") -> Array:
	return [name, condition, detail]


func run() -> Array:
	var rows: Array = []
	var rules := FakeRules.new()
	var s := Session.new(Session.DATA, rules)

	rows.append(_ok("starts at home", s.current == "home"))
	rows.append(_ok("home is discovered", s.is_discovered("home")))
	rows.append(_ok("HQ is known from the start", s.is_discovered("unsa_hq")))
	rows.append(_ok("the market is hidden before briefing", not s.is_discovered("market")))
	rows.append(_ok("travel to HQ works", bool(s.travel("unsa_hq").get("ok", false))))
	rows.append(_ok("PC is the first party member", s.party.size() == 1))

	s.act("briefing")
	rows.append(_ok("briefing discovers HQ", s.is_discovered("unsa_hq")))
	rows.append(_ok("briefing discovers the market", s.is_discovered("market")))
	rows.append(_ok("travel after discovery works", bool(s.travel("unsa_hq").get("ok", false))))

	rows.append(_ok("Laura joins", bool(s.recruit("laura_wendt").get("ok", false))))
	rows.append(_ok("party is two", s.party.size() == 2))
	rows.append(_ok("duplicate recruit is refused", not bool(s.recruit("laura_wendt").get("ok", true))))
	s.recruit("harri_romppainen")
	rows.append(_ok("party is three", s.party.size() == 3))
	rows.append(_ok("party cap is four", Session.PARTY_CAP == 4))

	s.travel("market")
	var witness := s.act("interview_witness")
	rows.append(_ok("a successful CWN check finds the witness clue", bool(witness.get("ok", false)) and s.is_clue("witness")))
	rows.append(_ok("the witness points to the clinic", s.is_discovered("clinic")))

	# A failed check must not invent the clue.
	s = Session.new(Session.DATA, rules)
	s.travel("unsa_hq")
	s.act("briefing")
	s.travel("market")
	rules.skill_ok = false
	s.act("interview_witness")
	rows.append(_ok("a failed check leaves the clue unfound", not s.is_clue("witness")))
	rules.skill_ok = true

	s = Session.new(Session.DATA, rules)
	s.travel("unsa_hq")
	s.act("briefing")
	s.travel("harbor")
	s.act("search_terminal")
	rows.append(_ok("the terminal yields its clue", s.is_clue("terminal")))
	rows.append(_ok("the terminal points to the warehouse", s.is_discovered("warehouse")))

	# Abstract CWN combat: three hits drop the threat, then the device can be recovered.
	s.travel("warehouse")
	var first := s.act("confront")
	rows.append(_ok("an attack roll resolves without a tactical view", first.has("check")))
	rows.append(_ok("a hit lowers the threat", s.threat_hp == 7))
	s.act("confront")
	s.act("confront")
	rows.append(_ok("three hits resolve the confrontation", bool(s.flags.get("resolved", false))))
	rows.append(_ok("the case completes on recovery", bool(s.act("recover_device").get("ok", false))))
	rows.append(_ok("case flag is set", bool(s.flags.get("case_won", false))))

	var state := s.to_dict()
	var loaded := Session.new(Session.DATA, rules)
	rows.append(_ok("save data loads", loaded.from_dict(state)))
	rows.append(_ok("loaded state keeps clues", loaded.clues.size() == s.clues.size()))
	rows.append(_ok("loaded state keeps the win", bool(loaded.flags.get("case_won", false))))
	return rows
