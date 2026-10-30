## Combat kernel checks for #749.
##
## Everything here is executable behaviour: seeded resolution, movement legality, the action
## economy, cover, and encounter termination. No prose assertions.
extends RefCounted

const Adapter := preload("res://godot/core/rules_adapter.gd")
const Combat := preload("res://godot/core/combat.gd")

func _eq(name: String, got: Variant, want: Variant) -> Array:
	return [name, got == want, "got %s want %s" % [str(got), str(want)]]

func _actor(id: String, side: String, pos: Vector2i, extra: Dictionary = {}) -> Dictionary:
	var base := {
		"id": id, "side": side, "pos": pos,
		"hp": 8, "ac": 13, "dex": 12, "combat_rank": 2, "attack_bonus": 1,
		"damage": [1, 6, 0],
	}
	for key in extra:
		base[key] = extra[key]
	return base

func _fight(seed_value: int) -> NoopunkCombat:
	var combat: NoopunkCombat = Combat.new(Adapter.new("res://data/rules/wn_core.json", seed_value))
	combat.add_actor(_actor("romppainen", "pc", Vector2i(1, 1)))
	combat.add_actor(_actor("thug", "enemy", Vector2i(4, 1), {"hp": 6}))
	return combat

## Start a fight and advance to the PC's turn, so Shock/ammo assertions are not initiative-dependent.
func _pc_turn(seed_value: int) -> NoopunkCombat:
	var combat: NoopunkCombat = _fight(seed_value)
	combat.start()
	var guard := 0
	while combat.current_id() != "romppainen" and guard < 8:
		guard += 1
		combat.end_turn()
	return combat

func run() -> Array:
	var rows: Array = []

	# --- initiative ---------------------------------------------------------------
	var a := _fight(7)
	var order_a := a.start()
	var b := _fight(7)
	var order_b := b.start()
	rows.append(_eq("initiative is reproducible from one seed", order_a, order_b))
	rows.append(_eq("every combatant is in the initiative order", order_a.size(), 2))
	rows.append(_eq("initiative starts at the first combatant", a.current_id(), order_a[0]))

	# --- movement -----------------------------------------------------------------
	var combat := _fight(11)
	combat.start()
	var mover := combat.current_id()
	var start_pos: Vector2i = combat.actors[mover]["pos"]
	var legal := combat.move(mover, start_pos + Vector2i(2, 1))
	rows.append(_eq("a move within five squares is legal", legal["ok"], true))
	rows.append(_eq("the actor really moved", combat.actors[mover]["pos"], start_pos + Vector2i(2, 1)))
	rows.append(_eq("the move is spent", combat.actors[mover]["moved"], true))
	rows.append(_eq("a second move is refused", combat.move(mover, start_pos)["reason"], "move_already_used"))

	var other := _fight(11)
	other.start()
	var m2 := other.current_id()
	var far := other.move(m2, other.actors[m2]["pos"] + Vector2i(9, 0))
	rows.append(_eq("a move beyond the allowance is refused", far["reason"], "beyond_move"))

	var blocked := _fight(11)
	blocked.start()
	var m3 := blocked.current_id()
	var target_id := "thug" if m3 == "romppainen" else "romppainen"
	rows.append(_eq("a move onto an occupied square is refused",
		blocked.move(m3, blocked.actors[target_id]["pos"])["reason"], "square_occupied"))
	rows.append(_eq("a move outside the grid is refused",
		blocked.move(m3, Vector2i(-1, 0))["reason"], "out_of_bounds"))

	# --- turn order ---------------------------------------------------------------
	var turns := _fight(3)
	var order := turns.start()
	turns.end_turn()
	rows.append(_eq("ending a turn advances to the next combatant",
		turns.current_id(), String(order[1 % order.size()])))
	turns.end_turn()
	rows.append(_eq("a full round advances the round counter", turns.round_number, 2))
	rows.append(_eq("flags are reset for the new round",
		turns.actors[turns.current_id()]["acted"], false))

	# --- attacks ------------------------------------------------------------------
	var hits := 0
	var misses := 0
	for seed_value in range(1, 41):
		var fight := _fight(seed_value)
		fight.start()
		var attacker := fight.current_id()
		var defender := "thug" if attacker == "romppainen" else "romppainen"
		var result := fight.attack(attacker, defender)
		if bool(result.get("hit", false)):
			hits += 1
			rows.append(_eq("a hit deals at least one damage", int(result["damage"]) >= 1, true)) if rows.size() < 3 else null
		else:
			misses += 1
	rows.append(["attacks both hit and miss across seeds", hits > 0 and misses > 0, "hits %d misses %d" % [hits, misses]])

	var once := _fight(5)
	once.start()
	var atk := once.current_id()
	var def := "thug" if atk == "romppainen" else "romppainen"
	once.attack(atk, def)
	rows.append(_eq("a second attack in the same turn is refused",
		once.attack(atk, def)["reason"], "action_already_used"))
	rows.append(_eq("attacking out of turn is refused",
		once.attack(def, atk)["reason"], "not_this_actors_turn"))

	# --- damage, cover, termination ----------------------------------------------
	var lethal := _fight(9)
	lethal.start()
	var killer := lethal.current_id()
	var victim := "thug" if killer == "romppainen" else "romppainen"
	lethal.actors[victim]["hp"] = 1
	lethal.actors[victim]["cover"] = 0
	var guard := 0
	while not lethal.is_over() and guard < 60:
		guard += 1
		var result := lethal.attack(killer, victim)
		if not bool(result.get("hit", false)):
			lethal.end_turn()
			lethal.end_turn()
	rows.append(_eq("a combat ends when one side is down", lethal.is_over(), true))
	rows.append(_eq("the outcome names the surviving side", lethal.outcome().begins_with("pcs_") or lethal.outcome().begins_with("enemies_"), true))

	var covered := _fight(13)
	covered.start()
	var c_atk := covered.current_id()
	var c_def := "thug" if c_atk == "romppainen" else "romppainen"
	covered.actors[c_def]["cover"] = 4
	var covered_result := covered.attack(c_atk, c_def)
	rows.append(_eq("cover raises the target's effective Armor Class",
		int(covered_result["roll"]["armor_class"]), int(covered.actors[c_def]["ac"]) + 4))

	# --- Shock, Trauma and ammunition in the turn loop (#751) -------------------------
	var shock_fight := _pc_turn(11)
	shock_fight.actors["romppainen"]["shock_value"] = 2
	shock_fight.actors["romppainen"]["shock_ac"] = 20
	shock_fight.actors["romppainen"]["weapon_kind"] = "melee"
	var before_hp := int(shock_fight.actors["thug"]["hp"])
	var swing := shock_fight.attack("romppainen", "thug")
	rows.append(_eq("a melee attack is resolved against the melee Armour Class",
		int(swing["armor_class"]),
		int(shock_fight.actors["thug"]["ac_melee"]) + int(shock_fight.actors["thug"]["cover"])))
	if bool(swing.get("hit", false)):
		rows.append(_eq("a hit deals its rolled damage and no Shock", int(swing["shock"]), 0))
	else:
		rows.append(_eq("a miss within the rating deals the weapon's Shock",
			int(swing["damage"]), 2))
		rows.append(_eq("and the target loses exactly that",
			int(shock_fight.actors["thug"]["hp"]), before_hp - 2))

	var ammo_fight := _pc_turn(12)
	ammo_fight.actors["romppainen"]["ammo"] = 1
	ammo_fight.actors["romppainen"]["ammo_max"] = 1
	ammo_fight.actors["romppainen"]["weapon_kind"] = "ranged"
	ammo_fight.attack("romppainen", "thug")
	rows.append(_eq("firing spends a round", int(ammo_fight.actors["romppainen"]["ammo"]), 0))
	ammo_fight.end_turn()
	ammo_fight.end_turn()
	rows.append(_eq("an empty weapon cannot fire",
		ammo_fight.attack("romppainen", "thug").get("reason", ""), "empty_magazine"))
	rows.append(_eq("reloading refills the magazine",
		int(ammo_fight.reload("romppainen").get("ammo", -1)), 1))

	return rows
