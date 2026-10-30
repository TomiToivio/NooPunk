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
| Hacking: Access/CPU, alert clock, wireless −2, VR −1 | hacking/hacking-mechanics, cyberspace-actions | **implemented** |
| Equipment, armour, weapons catalogue, shock/trauma, ammo/reload | gear-vehicles-cyberware/weapons, /armor | **implemented** — `data/rules/cwn_catalogue.json` (23 weapons, 8 armour) with `CwnCatalogue`: range bands, burst, ammo, trauma, shock, soak |
| Cyberware catalogue and strain costs | gear-vehicles-cyberware/cyberware/cyberware-systems | **implemented** — all 80 implants across seven tables (`data/rules/cwn_cyberware.json`, `CwnCyberware`), cost, concealment, permanent strain and injury destruction tested |
| Drones and vehicles | drones, vehicles, combat/vehicle-combat | **implemented + tested** — `godot/core/cwn_srd_vehicles.gd`: 9 drones and 10 vehicles from the SRD, drone deploy/bring-online/pack action costs, safe 1 km and 8 km max control range with automatic hijack beyond 1 km, 1 km flight ceiling, battery and charging, fitting capacity and hardpoint weapon class; vehicle AC (stationary −4, moving + driver's Drive), Armor subtracted from all damage, destruction, occupant damage with a Luck save, crash saves, and ramming (1d12/x3 vs people, no Evasion save vs vehicles). 60 assertions in `test_cwn_srd_vehicles.gd`. GM-discretion points (heavy hardpoints, which weapons can traumatise which vehicle) are returned as questions, not invented rules |
| CWN drone catalogue and mods | gear-vehicles-cyberware/drones | **implemented** — nine models, 30 fittings, eight mods in `data/rules/cwn_drones.json`, `CwnDrones` derives modified stats and costs; separate from `cwn_srd_vehicles.gd` procedures |
| Program Verbs and Subjects (24 + 12) and legality/costs | hacking/programs/program-verbs, program-subjects | **implemented** — `CwnCatalogue.can_pair`, `program_cost` |
| Air gap/range, program memory, Demons/watchdogs | hacking/cyberspace-basics, demons-watchdogs | **pending** |
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
