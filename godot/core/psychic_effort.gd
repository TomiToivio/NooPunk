## Resource-only SWN psionic Effort accounting for Godot.
## Technique effects belong in scenario data after source-specific verification.
class_name PsychicEffort
extends RefCounted

const DISCIPLINES := ["Biopsionics", "Metapsionics", "Precognition", "Telekinesis", "Telepathy", "Teleportation"]

var wisdom: int
var constitution: int
var ranks: Dictionary
var commitments: Dictionary = {}
var scene: int = 0

func _init(wis: int = 10, con: int = 10, skills: Dictionary = {}) -> void:
	wisdom = wis
	constitution = con
	ranks = skills.duplicate(true)

func capacity() -> int:
	var kernel := RulesAdapter.new()
	var highest := 0
	for name in ranks:
		if name in DISCIPLINES:
			highest = maxi(highest, int(ranks[name]))
	return maxi(1, 1 + maxi(kernel.attribute_modifier(wisdom), kernel.attribute_modifier(constitution)) + highest)

func free() -> int:
	var used := 0
	for commitment in commitments.values():
		used += int(commitment["amount"])
	return capacity() - used

func commit(key: String, discipline: String, rank: int = 0, duration: String = "scene", amount: int = 1) -> bool:
	if key.is_empty() or commitments.has(key) or not ranks.has(discipline) or not discipline in DISCIPLINES:
		return false
	if int(ranks[discipline]) < rank or rank < 0 or not duration in ["active", "scene", "day"]:
		return false
	if amount < 1 or amount > free():
		return false
	commitments[key] = {"amount": amount, "duration": duration, "discipline": discipline}
	return true

func release(key: String) -> bool:
	if not commitments.has(key) or String(commitments[key]["duration"]) != "active":
		return false
	commitments.erase(key)
	return true

func end_scene() -> void:
	scene += 1
	for key in commitments.keys():
		if String(commitments[key]["duration"]) != "day":
			commitments.erase(key)

func rest() -> void:
	commitments.clear()

func snapshot() -> Dictionary:
	return {
		"wisdom": wisdom, "constitution": constitution,
		"ranks": ranks.duplicate(true), "commitments": commitments.duplicate(true),
		"scene": scene,
	}

func restore(saved: Dictionary) -> bool:
	var candidate := PsychicEffort.new(int(saved.get("wisdom", 10)), int(saved.get("constitution", 10)), saved.get("ranks", {}))
	var kept: Dictionary = saved.get("commitments", {})
	for key in kept:
		var entry: Dictionary = kept[key]
		if not candidate.commit(String(key), String(entry.get("discipline", "")),
				0, String(entry.get("duration", "scene")), int(entry.get("amount", 0))):
			# Older snapshots may lack discipline. Do not invent a valid authorization.
			return false
	wisdom = candidate.wisdom
	constitution = candidate.constitution
	ranks = candidate.ranks
	commitments = candidate.commitments
	scene = int(saved.get("scene", 0))
	return true
