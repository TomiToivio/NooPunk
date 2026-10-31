# Core vs mod matrix (#897)

The Milestone 1 deliverable of [#897](FOUNDATIONAL_LOCK_897.md): a record of **which published
mechanics are implemented verbatim, which are adapted, and which are NoöPunk optional modules** — so that
no future agent silently substitutes a novel resolution system for the baseline.

Rules for reading this file:

- **Verbatim** means the procedure follows the published text; the SRD page is named in
  `docs/rules/CWN_GODOT_COVERAGE.md`.
- **Adapted** means the published *mechanic* is preserved but something around it changed — presentation,
  data shape, or an interface concession. Every adaptation is justified in its own row.
- **Mod** means NoöPunk material layered on top. A mod may read core state and may not compute core
  resolution.
- A blank cell is not permission to improvise. If a procedure is not listed, it is **not implemented**;
  add a row before adding code.

## A. Core CWN — implemented verbatim

34 modules in `godot/core/cwn_*.gd`, exercised by the headless suite
(`godot --headless --path . --script res://godot/tests/run_tests.gd`).

| Subsystem | Governing source | Module(s) |
| --- | --- | --- |
| Attributes and the 3–18 band | CWN, rules-of-the-game | `rules_adapter.gd`, `cwn_character.gd` |
| Skill checks (2d6 + attribute + skill), difficulty ladder | CWN, skill-checks | `rules_adapter.gd` |
| Saving throws (d20, 16 − level − best of pair) | CWN, saving-throws | `rules_adapter.gd`, `cwn_character.gd` |
| Attacks (d20 + bonus vs AC) and the attack-modifier table | CWN, combat / attacks-in-combat | `cwn_attack_modifiers.gd`, `cwn_combat_rules.gd` |
| Combat actions and the action economy | CWN, combat-actions | `cwn_combat_actions.gd` |
| Damage, trauma and shock | CWN, damage-trauma-shock | `cwn_combat_rules.gd`, `cwn_injury.gd` |
| System Strain | CWN, system-strain | `cwn_strain.gd` |
| Major injuries and healing | CWN, major-injuries / natural-healing | `cwn_injury.gd`, `cwn_healing.gd` |
| Encumbrance | CWN, encumbrance | `cwn_encumbrance.gd` |
| Chases and pursuit | CWN, chases-and-pursuit | `cwn_chases.gd` |
| Scenes, rounds and mission time | CWN, scenes-rounds-mission-time | `cwn_mission_time.gd` |
| Advancement (XP, level, attack, HP, skill points, rank gates) | CWN, character-advancement | `cwn_progression.gd` |
| Edges and foci | CWN, character-creation/edges, /foci | `cwn_foci.gd` |
| Contacts | CWN, character-creation/contacts | `cwn_contacts.gd` |
| Equipment, armour and weapons catalogue | CWN, gear-vehicles-cyberware | `cwn_catalogue.gd`, `cwn_gear_mods.gd` |
| Lifestyles, wages, bribes | CWN, lifestyles-wages-and-bribes | `cwn_lifestyles.gd`, `cwn_wages.gd` |
| Pharmaceuticals and street drugs | CWN, pharmaceuticals-street-drugs | `cwn_drugs.gd` |
| Cyberware: installation, removal, alienation, complications | CWN, cyberware/* | `cwn_cyberware.gd`, `cwn_cyberware_ops.gd`, `cwn_cyberware_complications.gd`, `cwn_alienation.gd` |
| Hacking: Access/CPU, Alert clock, programs, verbs, demons | CWN, hacking/* | `cwn_hacking.gd`, `cwn_hacking_catalogue.gd`, `cwn_programs.gd`, `cwn_program_rules.gd`, `cwn_demons.gd`, `cwn_node_link.gd` |
| Drones and vehicles | CWN, drones / vehicles / vehicle-combat | `cwn_drones.gd`, `cwn_vehicles.gd`, `cwn_srd_vehicles.gd` |
| Party handling | CWN (GM-facing) | `cwn_party.gd` |
| Tag vocabulary used by the core | CWN-derived | `cwn_tags.gd`, `cwn_social_costs.gd` |

## B. Core CWN — adapted

| Subsystem | What changed | Why | Where |
| --- | --- | --- | --- |
| Character creation input | choices are data (`choices: [...]`) rather than a guided wizard | keeps the sheet reproducible and testable before a UI exists; a wizard is a UI layer, not a rule | `data/`, character sheets |
| Vehicle/drone catalogue access | SRD tables read through a generated data contract instead of transcribed constants | removes hand-transcription as a failure mode; `tools/cwn_srd_extract.py` regenerates it | `data/rules/cwn/srd_tables.json` |
| Weapon/armour row naming | accessor resolves the name column per sub-table | the SRD names rows differently per table (`Firearm`, `Civilian Armor`, `Melee Weapon`); a fixed column silently matched nothing | `godot/core/cwn_catalogue.gd` |

No adaptation in this section changes a die roll, a target number or a resource cost. If one ever does, it
belongs in section D as a mod, not here.

## C. Gap-fills — SWN / WWN

| Gap | Source | Scope | Status |
| --- | --- | --- | --- |
| Psionics (Psychic class, disciplines, Effort, techniques) | **SWN Revised** | whole subsystem, not blended with CWN skills or combat | **partial** — the Effort resource layer exists and is tested; the class, discipline gates and technique catalogue are not complete |
| Space travel, starships, factions | SWN Revised | not yet needed by a Helsinki campaign | **not implemented** |
| WWN material | WWN | none borrowed | **none** — each future borrowing needs its own row here naming the gap CWN leaves |

CWN remains primary wherever the two overlap. A procedure that exists in CWN is never sourced from SWN.

## D. NoöPunk optional modules

**None of these are implemented.** They are design-stage overlays with no code, listed so they are not
mistaken for core rules, and so nothing invents them accidentally.

| Module | Purpose | Core interaction | Status |
| --- | --- | --- | --- |
| Noösphere / ontological shock / Psyche | exposure, perception, instability, resilience, awakening, recovery | reads core state; adds narrative consequences, not real-world psychiatric claims | design only |
| Ideology and factions | Laclau-inspired identification, shifting alliances, antagonisms, faction standing | reads social state; must not predetermine the player's ideology | design only |
| Relationships, reputation, contacts | NPC trust, obligations, social capital, institutional standing | reads `cwn_contacts.gd`; adds standing, does not replace reaction rolls | design only |
| Investigative mode | clue discovery and synthesis, contradictions, lead progression | borrows GUMSHOE's *never block an essential clue behind one failed roll* as an **optional** module; CWN checks remain the resolution | design only |
| Active vs passive PSI | **open design question** | tentative: PC gets passive/minor PSI, stronger active PSI mostly NPC | **not canonised — do not build on it** |

The rule for every row: **core CWN rulebooks must remain intelligible, and the core suites must pass,
with all mods disabled.**

## E. Backlog

Not implemented, in rough order of what the vertical slice needs:

1. SWN psionics completion (class, disciplines, techniques, advancement gates).
2. Noösphere/Psyche module with its own tests.
3. Ideology, faction and reputation module.
4. Investigative mode with the no-blocked-clue guarantee.
5. Location map and action menus (Milestone 3) — no core change expected.
6. Non-tactical combat resolution over `cwn_combat_rules.gd` (Milestone 3).
7. Hacking graph mode over `cwn_hacking.gd` (Milestone 4).

## F. Adding a row

1. Name the published procedure and its source page, or say plainly that it is a NoöPunk invention.
2. If it is a mod, place it in section D and state which core state it reads.
3. Add or extend a test in the same PR; a rule without a test is a claim.
4. Run the core suites with mods disabled before claiming parity.
