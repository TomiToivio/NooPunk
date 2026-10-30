## CWN catalogue (#749): transcribed tables and the procedures they drive — range bands, burst,
## ammo, trauma, shock, soak, cyberware strain and Verb/Subject legality.
extends RefCounted

const Cat := preload("res://godot/core/cwn_catalogue.gd")
const Dice := preload("res://godot/core/dice.gd")

class FixedDice:
	extends RefCounted
	var faces := {20: 15, 12: 6, 10: 6, 8: 4, 6: 3, 4: 2, 2: 1}
	func roll(sides: int) -> int:
		return int(faces.get(sides, 1))

## Reports hits and records the modifier it was asked to apply.
class FakeAdapter:
	extends RefCounted
	var hit := true
	var last_modifier := 0
	func attack_roll(_attr: int, _rank: int, _bonus: int, _ac: int, modifier: int = 0) -> Dictionary:
		last_modifier = modifier
		return {"hit": hit, "total": 15}

	func attribute_modifier(score: int) -> int:
		return 1 if score >= 14 else 0

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]

func run() -> Array:
	var rows: Array = []
	var cat := Cat.new()
	var dice := FixedDice.new()

	rows.append(_eq("weapon table is transcribed", [cat.weapons.size(), cat.armor.size(), cat.cyberware.size()], [23, 8, 17]))
	rows.append(_eq("program verbs are transcribed", cat.verbs.size(), 24))
	rows.append(_eq("program subjects are transcribed", cat.subjects.size(), 12))

	# --- range bands ----------------------------------------------------------------
	rows.append(_eq("pistol inside normal range has no penalty", cat.range_penalty("light_pistol", 8.0)["penalty"], 0))
	rows.append(_eq("pistol beyond normal range is -2", cat.range_penalty("light_pistol", 50.0)["penalty"], -2))
	rows.append(_eq("pistol beyond extreme range is illegal", cat.range_penalty("light_pistol", 81.0)["reason"], "beyond_extreme"))
	rows.append(_eq("a sword at 2 m is out of reach", cat.range_penalty("sword", 2.0)["reason"], "out_of_reach"))
	rows.append(_eq("a rifle reaches its extreme band", cat.range_penalty("rifle", 400.0)["penalty"], -2))

	# --- attack, burst, damage ------------------------------------------------------
	var fake := FakeAdapter.new()
	var shot: Dictionary = cat.attack(fake, "light_pistol", 14, 2, 13, 8.0, dice)
	rows.append(_eq("attack resolves through the kernel", shot["hit"], true))
	rows.append(_eq("pistol damage is die plus attribute modifier", int(shot["damage"]), 4))
	rows.append(_eq("only burst weapons may burst", cat.attack(fake, "rifle", 14, 2, 13, 10.0, dice, true)["reason"], "weapon_cannot_burst"))
	var burst: Dictionary = cat.attack(fake, "smg", 14, 2, 13, 10.0, dice, true)
	rows.append(_eq("burst adds +2 to hit", int(fake.last_modifier), 2))

	# --- shock on a miss ------------------------------------------------------------
	var miss := FakeAdapter.new()
	miss.hit = false
	var missed: Dictionary = cat.attack(miss, "knife", 14, 2, 15, 1.0, dice)
	rows.append(_eq("shock applies on a miss at or below its AC", int(missed.get("shock", 0)), 2))
	rows.append(_eq("shock does not apply above its AC", cat.shock_damage("knife", 16, 1), 0))
	rows.append(_eq("firearms have no shock", cat.shock_damage("light_pistol", 10, 1), 0))

	# --- soak and trauma ------------------------------------------------------------
	rows.append(_eq("armour soak reduces damage", cat.apply_soak("armored_clothing", 8), 3))
	rows.append(_eq("soak cannot go below zero", cat.apply_soak("reinforced_clothing", 2), 0))
	var trauma: Dictionary = cat.trauma("heavy_pistol", dice)
	rows.append(_eq("trauma die is rolled", trauma["roll"], 3))
	rows.append(_eq("trauma target is six by default", trauma["target"], 6))
	rows.append(_eq("a low trauma roll is not traumatic", trauma["traumatic"], false))
	rows.append(_eq("armour trauma modifier raises the target", cat.trauma("heavy_pistol", dice, "plated_longcoat")["target"], 7))
	rows.append(_eq("non-lethal weapons roll no trauma die", cat.trauma("taser_pistol", dice)["reason"], "nonlethal"))

	# --- ammo -----------------------------------------------------------------------
	var ammo: Dictionary = cat.fire({"rounds": 8}, "heavy_pistol")
	rows.append(_eq("a shot spends one round", ammo["rounds"], 7))
	rows.append(_eq("a burst spends three", cat.fire({"rounds": 20}, "smg", true)["rounds"], 17))
	rows.append(_eq("an empty weapon refuses", cat.fire({"rounds": 0}, "heavy_pistol")["reason"], "empty"))
	rows.append(_eq("reload refills the magazine", cat.reload("heavy_pistol")["rounds"], 8))
	rows.append(_eq("melee weapons do not reload", cat.reload("knife")["reason"], "not_a_firearm"))

	# --- cyberware strain -----------------------------------------------------------
	rows.append(_eq("fractional strain adds up", cat.strain_total(["deadman_circuit", "viper_sting"]), 0.75))
	var baseline: Dictionary = cat.strain_with_baseline(["cybernetic_baseline", "deadman_circuit"], 10)
	rows.append(_eq("the baseline ignores 12 - CON strain", baseline["ignored"], 2.0))
	rows.append(_eq("effective strain drops to zero", baseline["effective"], 0.0))
	rows.append(_eq("strain maximum is Constitution", baseline["maximum"], 10))

	# --- Verb/Subject legality ------------------------------------------------------
	rows.append(_eq("Blind can target a Camera", cat.can_pair("blind", "camera"), true))
	rows.append(_eq("Blind cannot target a Datafile", cat.can_pair("blind", "datafile"), false))
	rows.append(_eq("Unlock can target a Datafile", cat.can_pair("unlock", "datafile"), true))
	var program: Dictionary = cat.program_cost("unlock", "datafile")
	rows.append(_eq("Unlock costs one Access", program["access"], 1))
	rows.append(_eq("Unlock is self-terminating", program["self_terminating"], true))
	rows.append(_eq("a generic Machine subject adds +1 difficulty", cat.program_cost("blind", "machine")["difficulty_modifier"], 1))
	return rows
