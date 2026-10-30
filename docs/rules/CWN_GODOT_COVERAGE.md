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
| Attack-roll modifiers (cover −2/−4, range −2, melee −4, prone +2/−2, two N/A rows) | combat/attacks-in-combat | **implemented + tested** — `cwn_attack_modifiers.gd`; the two N/A rows block the attack instead of becoming a number, and an unknown id is refused rather than read as zero |
| Chases and pursuit (foot pace with +3 hindrance cap, vehicle pace, head-start and terrain rows) | rules-of-the-game/chases-and-pursuit | **implemented + tested** — `cwn_chases.gd`; ties escape, terrain clamped −2..+2, vehicle pursuers that miss the pace drop out |
| Scenes, rounds and mission time (6 s round, 10 min scene refresh, minute-per-action clock) | rules-of-the-game/scenes-rounds-mission-time | **implemented + tested** — `cwn_mission_time.gd`; a long action reports how many scenes it crossed |
| Cyberware installation, removal, salvage, reuse, Alienation and chrome syndromes | gear-vehicles-cyberware/cyberware/* | **implemented + tested** — `cwn_cyberware_ops.gd`: strain-tier cost/recovery/difficulty table, surgery modifiers, fail-by-one-or-two as a complication, fail-by-three as strain-max plus 1 hp, removal and salvage clocks, Alienation rounding with the Nerve +2, syndrome maxima, therapy floor and psychosis threshold |
| Crafting, modifying and maintaining gear (mod cap +3, maintenance count, workshop weeks, jury-rigged/normal/mastercrafted, factory mods) | rules-of-the-game/crafting-and-modifying-gear/* | **implemented + tested** — `cwn_gear_mods.gd` over `data/rules/cwn_gear_mods.json` (13 weapon, 11 armour, 8 drone, 7 deck mods); connection mods without a Gunlink are reported inactive, not silently applied |
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

## Vanilla CWN pass — 2026-10-30

The four procedures above were added because they existed in the Python reference or in the SRD but
had no Godot home: attack modifiers, chases, cyberware operations and mission time, plus the crafting
and gear-mod arithmetic. With them the game can resolve the SRD's procedures from data instead of from
a referee's memory.

**Verification:** `godot --headless --path . --script res://godot/tests/run_tests.gd` →
**951 checks, 0 failed** (baseline before this pass: 760).

### Still honestly pending

| Gap | What is missing |
| --- | --- |
| Cyberware catalogue breadth | strain costs are transcribed for body implants; head, limb, nerve, sensory, medical and skin tables still need extraction |
| Implant complications | the d12 table is referenced by name; roll the table from the SRD before calling installation "complete" |
| Hacking: air gap, program memory, demons/watchdogs | procedures not implemented |
| Edges and Foci | catalogue and per-level effects exist in the Python layer (`cwn_edges_foci.py`, `cwn_foci.py`) but no Godot module |
| Character creation content | backgrounds, contacts and the focus gear budget are data, not yet wired into the creation screen |
| Progression | arithmetic exists; no end-to-end advancement test |
| Desktop playtest | headless suites prove behaviour, not legibility |

Nothing in this file claims full CWN coverage. A row is "implemented" only where a test would fail
without the code.
