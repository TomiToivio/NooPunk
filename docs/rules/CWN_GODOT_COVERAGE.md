# CWN → Godot coverage

Source: the Cities Without Number SRD at <https://cwn.quadrifons.com/> (CC0). The single data
contract is `data/rules/wn_core.json`; `godot/core/rules_adapter.gd` exposes it to the game.
Nothing here copies rulebook prose — procedures are implemented, prose is not.

Status vocabulary: **implemented + tested**, **partial**, **pending**.

| CWN procedure | SRD section | Status in Godot |
|---|---|---|
| Attribute modifiers, 3..18 band | rules-of-the-game/character-creation | implemented — `attribute_modifier`, `roll_attributes` (3d6 down the line, seeded) |
| Skill checks (2d6 + attr + skill vs difficulty) | rules-of-the-game/skill-checks | implemented — `skill_check`, kernel difficulty ladder |
| Saving throws (d20 ≥ 16 − level − best of pair) | rules-of-the-game/saving-throws | implemented — `save_target` |
| Attacks (d20 + bonus vs AC) | rules-of-the-game/combat | implemented — `attack_roll` |
| Action economy: 1 Main, 1 Move, buy a second Move, snap −4, charge +2/−2, total defence | combat/combat-actions | implemented as data — `action_economy`, `combat_action_modifier` |
| System Strain (max = CON, cyberware permanent, forced overflow = 1 h unconscious, 1/night) | injury-healing-system-strain/system-strain | implemented — `strain_max`, `strain_absorb`, `strain_recover` |
| Major injuries (d12 clamped 1..12, row effects) | injury-healing-system-strain/major-injuries | implemented (row lookup) — `major_injury` |
| Encumbrance (stowed = STR, readied = ⌊STR/2⌋, 70 % / 50 % speed) | rules-of-the-game/encumbrance | implemented — `encumbrance`, `speed_for_load` |
| Advancement (fast/slow XP, level, attack bonus, HP, skill points, rank gates, foci levels, edges) | rules-of-the-game/character-advancement | implemented for XP/level/attack/HP/skill points/rank gates; foci and edge tables are in the kernel but **no UI** |
| Hacking: Access pool, Jack In/Move/Run, two failures = one Alert action, two actions = alert, wireless −2, VR −1 | hacking/hacking-mechanics, hacking/cyberspace-actions | **partial** — clock, Access, CPU and penalties implemented and tested; air gap/range, the Verb/Subject catalogue, demons/watchdogs and program memory are pending |
| Equipment, armour, weapons catalogue, shock/trauma, ammo/reload | rules-of-the-game/equipment, combat | **pending** — the kernel has no weapon table, so none was invented |
| Cyberware catalogue and strain costs | cyberware | **pending** — strain procedure exists; the implant list does not |
| Drones, vehicles | drones, vehicles | **pending** |
| Demons, watchdogs, network security ladder | hacking/demons-and-watchdogs | **pending** (security values are scenario data) |
| SWN Revised psionics | (SWN SRD, separate system) | **partial** — `psychic_effort.gd` plus Effort tests exist; no MVP psychic character or technique catalogue |

## Why "all rules" is not a single patch

The pending rows are catalogue content (weapons, cyberware, drones, programs) and GM procedures.
Implementing them without the source text would mean inventing numbers, which the repository's
`AGENTS.md` forbids. The next reviewable increments are:

1. Transcribe the equipment/weapon table with per-row SRD anchors, then shock/trauma and ammo.
2. Transcribe cyberware with strain costs and wire `strain_absorb` into character creation.
3. Extend the hacking kernel with air gap/range and the Verb/Subject catalogue from the SRD.
4. Drones, vehicles, demons and the security ladder as data + procedures.

## Verification

`godot --headless --path . --script res://godot/tests/run_tests.gd` → **309 checks, 0 failed**,
including `test_cwn_procedures.gd` (creation, strain, advancement, encumbrance, major injury,
action economy), the combat and hacking suites, and the Lakkahaltia regression suites.
