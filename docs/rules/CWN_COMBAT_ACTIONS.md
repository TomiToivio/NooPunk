# CWN: combat actions and attack modifiers

The two halves of the combat chapter that `src/rules/cwn_combat.py` explicitly left to the caller: the
situational modifier that goes into `attack_roll(other_modifier=…)`, and the per-round action budget
that decides whether an action can be taken at all.

| subsystem | module | contract key | tests |
| --- | --- | --- | --- |
| Attack modifiers | `src/rules/cwn_attack_modifiers.py` | `combat.attack_modifiers` | `tests/test_cwn_attack_modifiers.py` |
| Action economy | `src/rules/cwn_combat_actions.py` | `combat.actions` | `tests/test_cwn_combat_actions.py` |

Sources (CWN SRD, CC0):

* <https://cwn.quadrifons.com/rules-of-the-game/combat/attacks-in-combat/>
* <https://cwn.quadrifons.com/rules-of-the-game/combat/combat-actions>

## Attack modifiers

The SRD's table is data, keyed by stable ids so a log line can name the circumstance without copying
the number: prone target (−2, or **+2** if adjacent), beyond normal range (−2), prone attacker in melee
(−4), half cover (−2), almost full cover (−4), thrown while in melee (−4), one-handed gun in melee
(−4), unseen target whose position is known (−4).

Two entries are **N/A**, not penalties: a **two-handed gun cannot be fired** while an enemy is in melee,
and a target whose position is unknown cannot be attacked. They raise `AttackImpossibleError` rather
than folding into −4, because a number would let a caller "shoot anyway" when the SRD says the attack
does not happen.

`in_melee_penalty(handedness)` encodes the same rule for ranged attacks made while engaged.

## Action economy

| SRD rule | implementation |
| --- | --- |
| One Main action per round | `TurnBudget.take_main()` |
| One Move action per round, spendable for a second by giving up the Main | `take_move()`, `convert_main_to_move()` |
| On Turn and Instant actions are not numerically capped | `ON_TURN_LIMITED = False`, `INSTANT_LIMITED = False` |
| Snap Attack: give up an **unspent** Main for an attack at −4, usable off-turn | `snap_attack_penalty(main_used=…)` |
| Swarm Attack: +2 hit / +1 damage per other assailant, cap **+6 / +3** (four attackers) | `swarm_bonus(other_assailants)` |
| Charge: Main + Move, at least 3 m, +2 to hit, −2 AC until end of round, double movement | `charge(distance, budget=…)` |
| Total Defense: give up an unspent Main for +2 AC and Shock immunity | `total_defense(main_used=…)` |
| Common actions and their costs | `COMMON_ACTIONS` |

The module enforces what the SRD fixes and refuses to invent what it leaves to the table: "as many On
Turn actions as the GM finds plausible" is not a number, so it is not enforced, and the adjudication of
simultaneous Instant actions stays with the GM.

The Swarm bonuses are returned as a pair because the SRD constrains them: the bonus damage **does not
add to Shock** and **cannot exceed the weapon's normal maximum**, while any Shock inflicted by a Swarm
Attack is always applicable. That interaction belongs to the damage step, not here.

## Composition

`cwn_combat.attack_roll(..., other_modifier=mods.attack_modifier("target_almost_full_cover"))` — a test
pins the exact case where full-cover fire turns a hit into a miss, so the two modules cannot drift into
disagreeing about what a modifier means.

## Not covered

* **Initiative and the combat sequence.** Those SRD sub-pages did not load (404 from the chapter's own
  table of contents), so turn order is not implemented and no number is invented for it.
* **Special combat maneuvers** beyond the common actions listed above, and **vehicle combat**.
* Weapons, armour and their stat lines — equipment content, not yet ported.
