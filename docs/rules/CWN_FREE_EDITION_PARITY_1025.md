# CWN Free Edition parity matrix (#1025)

**Generated** by `python3 tools/render_cwn_1025_matrix.py --write` from
`data/rules/cwn_free_edition_parity_1025.json`. Do not hand-edit this file; edit the JSON and
regenerate so the audit and its evidence cannot disagree.

**Source:** CWN Free Edition 081123, 231 pages. Book page numbers are used; the PDF page is the
book page + 4 in this printing. SRD cross-check: <https://cwn.quadrifons.com/>.
The SRD omits optional sections and the Antagonists/NPC material, so the PDF governs.

**Constitution:** `docs/rules/RULES_CONSTITUTION.md` (#1006). Vanilla CWN is locked; NoöPunk,
GUMSHOE, Noösphere, faction and stress layers are separate overlays and are never counted here.

## Honest status legend

- `complete` — Python rule exists, has an executable test, and is reachable from the MUD/campaign
  where the procedure is player-facing. A module without a test is not complete.
- `partial` — some rule logic or data exists, but a printed procedure, MUD surface, persistence
  proof or book-example test is missing. The gap column names it.
- `missing` — no Python implementation of the procedure.
- `not_applicable` — setting fiction, advice or reference matter with no mechanical procedure.

Command-wired, persistent-save-safe and playtested are **not** implied by `complete` unless the
gap column says so. The baseline is deliberately conservative: no 100% claim from file existence.

**Rows:** 73 — **complete** 20 · **partial** 26 · **missing** 22 · **not_applicable** 5

| Section | Book pp. | Status | Python | MUD | Tests | Gap / evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A Slow Chrome Apocalypse | 1 | not_applicable | — | — | — | Setting fiction and tone; no procedure. |
| Attributes | 5 | complete | src/rules/wn_core.py; src/rules/cwn_character.py | mud/nopunk_mud/cwn_core.py | tests/test_cwn_character.py; tests/test_mud_cwn_parity_950.py | 3d6 in order or fixed array; one optional 14; exclusive routes. |
| Skills | 5 | complete | src/rules/cwn_character.py | mud/nopunk_mud/cwn_core.py | tests/test_cwn_character.py | Creation pool 0/1/second skill; 19-skill list in data. |
| Choosing a Background | 7 | partial | src/rules/cwn_backgrounds.py | — | tests/test_cwn_backgrounds.py | Background data and selection exist; no interactive MUD creation flow. |
| Contacts / One-Roll Contact Tables | 14 | partial | src/rules/cwn_backgrounds.py | — | tests/test_cwn_backgrounds.py | Contacts exist as background output; the d20/d100 one-roll contact tables are not ported. |
| Edges | 16 | complete | src/rules/cwn_edges_foci.py | — | tests/test_cwn_edges_foci.py | Selection and effects; MUD command surface still thin. |
| Foci | 18 | complete | src/rules/cwn_foci.py | — | tests/test_cwn_foci.py | Includes focus gear budget. |
| Hit Points, Attack Bonus, and Saves | 24 | complete | src/rules/cwn_character.py; src/rules/cwn_advancement.py | mud/nopunk_mud/cwn_core.py | tests/test_cwn_character.py; tests/test_cwn_advancement.py | — |
| Starting Gear | 25 | partial | src/rules/cwn_equipment.py | — | tests/test_cwn_equipment.py | Catalogue and packages exist; creation-time purchase/assignment is not end-to-end. |
| Final Touches | 26 | partial | src/rules/cwn_character.py | — | tests/test_cwn_character.py | Attribute/skill finalisation tested; shopping, contact writing and sheet print are scenario/UI work. |
| Scenes, Rounds, and Mission Time | 30 | complete | src/rules/cwn_mission_time.py | mud/nopunk_mud/world_state.py | tests/test_cwn_mission_time.py | Round 6 s, scene 10 min, standard action 1 min; save round-trip. |
| Saving Throws | 30 | complete | src/rules/cwn_core.py | mud/nopunk_mud/cwn_core.py | tests/test_cwn_core.py; tests/test_mud_cwn_parity_950.py | — |
| Skill Checks | 31 | complete | src/rules/wn_core.py | mud/nopunk_mud/cwn_core.py | tests/test_wn_core.py; tests/test_mud_cwn_parity_950.py | — |
| Combat / The Combat Round | 33 | partial | src/rules/cwn_combat.py; src/rules/cwn_initiative.py | mud/nopunk_mud/cwn/combat.py; mud/nopunk_mud/cwn/initiative.py | tests/test_cwn_combat.py; tests/test_cwn_initiative.py | Python kernels and MUD adapters exist; no complete turn-loop command surface/save-resume proof. |
| Combat / Actions in Combat | 34 | complete | src/rules/cwn_combat_actions.py | mud/nopunk_mud/cwn/combat.py | tests/test_cwn_combat_actions.py | — |
| Combat / Combat Maneuvers and Definitions | 36 | partial | src/rules/cwn_combat.py | — | tests/test_cwn_combat.py | Maneuver resolution exists; the full printed maneuver list and edge cases are incomplete. |
| Injury, Healing, and System Strain | 40 | complete | src/rules/cwn_injury_procedure.py; src/rules/cwn_healing.py; src/rules/cwn_strain.py | mud/nopunk_mud/cwn_core.py | tests/test_cwn_injury_procedure.py; tests/test_cwn_healing.py; tests/test_cwn_strain.py | — |
| Major Injuries and Damaging Cyberware | 41 | complete | src/rules/cwn_major_injury.py | — | tests/test_cwn_major_injury.py | — |
| Vehicle Combat | 42 | partial | src/rules/cwn_vehicles.py | — | tests/test_cwn_vehicles.py | Statistics, armour and damage; chase round procedure remains separate. |
| Chases and Pursuit | 43 | missing | — | — | — | Godot-only chase screen; no Python/Evennia procedure. Named gap. |
| Character Advancement | 44 | complete | src/rules/cwn_advancement.py | — | tests/test_cwn_advancement.py | — |
| Crafting and Modifying Gear | 46 | complete | src/rules/cwn_gear_mods.py | — | tests/test_cwn_gear_mods.py | Crafting, modifying, maintaining and factory mods. |
| Encumbrance | 48 | complete | src/rules/cwn_encumbrance.py | — | tests/test_cwn_encumbrance.py | — |
| Acquiring Gear | 49 | partial | src/rules/cwn_equipment.py | — | tests/test_cwn_equipment.py | Prices/availability data exist; acquisition rolls, legality and street contacts are not a procedure. |
| Gear, Lifestyles, and Services | 50 | partial | src/rules/cwn_core.py; src/rules/cwn_equipment.py | — | tests/test_cwn_core.py; tests/test_cwn_equipment.py | Lifestyle strain costs ported; wages, bribes and service availability are incomplete. |
| Armor | 52 | complete | src/rules/cwn_equipment.py | — | tests/test_cwn_equipment.py | — |
| Weapons | 54 | complete | src/rules/cwn_equipment.py | — | tests/test_cwn_equipment.py | — |
| Armor and Weapon Mods | 58 | complete | src/rules/cwn_gear_mods.py | — | tests/test_cwn_gear_mods.py | — |
| Pharmaceuticals and Street Drugs | 60 | missing | — | — | — | Godot data only; no Python module, effects or addiction/overdose procedure. |
| Cyberware | 62 | partial | src/rules/cwn_core.py | — | tests/test_cwn_core.py | Costs, strain and alienation tables exist; installation surgery, complications, maintenance and removal are not a procedure. |
| Cyberware Mods | 74 | missing | — | — | — | No Python implant-module catalogue or installation effects. |
| Cyberdecks | 75 | missing | — | — | — | Deck models, capacity and accessories are not modelled in Python. |
| Drones | 76 | partial | src/rules/cwn_drones.py | — | tests/test_cwn_drones.py | Catalogue/fittings; operation economy and commands absent. |
| Drone Fittings | 78 | partial | src/rules/cwn_drones.py | — | tests/test_cwn_drones.py | Fitting data exists; printed hardpoint/stack limits and operation consequences are incomplete. |
| Drone Operation | 81 | missing | — | — | — | No action/command/range procedure; Godot screen is not a parity source. |
| Vehicles | 82 | partial | src/rules/cwn_vehicles.py | — | tests/test_cwn_vehicles.py | Catalogue and fitting legality. |
| Vehicle Fittings | 84 | partial | src/rules/cwn_vehicles.py | — | tests/test_cwn_vehicles.py | Fitting legality and stacking exist; all printed fittings and their combat effects are not audited. |
| Vehicle-Mounted Weaponry | 86 | partial | src/rules/cwn_vehicles.py | — | tests/test_cwn_vehicles.py | Data and attack helpers exist; full mounted-weapon arcs, operators and ammo are incomplete. |
| Vehicle Mods | 87 | partial | src/rules/cwn_vehicles.py | — | tests/test_cwn_vehicles.py | Modification price/stacking exists; every printed mod and its edge cases are not audited. |
| Example Vehicles | 88 | partial | data/rules/cwn_vehicles.json | — | tests/test_cwn_vehicles.py | Examples exist as data; not every printed example is audited against the book. |
| Cyberspace, Nodes, and Access | 92 | partial | src/rules/cwn_hacking.py | — | tests/test_cwn_hacking.py; tests/test_cwn_hacking_contract.py | Access pools, difficulty and alert clock; node graph and movement are incomplete. |
| Hacking Mechanics | 94 | partial | src/rules/cwn_hacking.py | — | tests/test_cwn_hacking.py | Checks and alert clock; full action economy and persistence missing. |
| Programs | 96 | partial | src/rules/cwn_program_catalogue.py; data/rules/cwn_program_catalogue.json | — | tests/test_cwn_program_catalogue.py | Catalogue exists; acquisition/writing costs and execution limits incomplete. |
| Cyberspace Actions | 100 | missing | — | — | — | No Python verb/subject action loop. |
| Demons and Watchdogs | 102 | partial | src/rules/cwn_hacking.py; data/rules/cwn_hacking.json | — | tests/test_cwn_hacking.py | Data/alert hooks; no autonomous demon/watchdog turn procedure. |
| Network Servers and Architecture | 104 | missing | — | — | — | No server-architecture generator or node graph model. |
| Cyberpunk Themes | 108 | not_applicable | — | — | — | Advice and genre material. |
| Creating The World | 110 | partial | — | — | — | Only setting docs; no generic world generator. |
| Creating The City | 114 | missing | — | — | — | No city generator; Helsinki content is campaign canon, not a generic CWN procedure. |
| Building Your Districts | 121 | missing | — | — | — | No district generator/tag procedure. |
| Creating Megacorps | 126 | missing | — | — | — | No megacorp generator. |
| Creating Gangs | 128 | missing | — | — | — | No gang generator. |
| Creating NPCs | 130 | partial | src/rules/cwn_npcs.py | — | tests/test_cwn_npcs_heat.py | Reaction/morale/stat-block reading rules now exist; quick NPC generator and bestiary blocks do not. |
| Creating Schemes | 133 | missing | — | — | — | No scheme generator or clock. |
| NPC Operator Teams | 138 | missing | — | — | — | No operator-team generator. |
| NPC Scheme Results | 140 | missing | — | — | — | No result tables. |
| How To Create a Mission | 142 | missing | — | — | — | No mission generator. |
| Mission Tags | 144 | missing | — | — | — | No tag catalogue/rolls. |
| Mission Types | 158 | missing | — | — | — | No mission-type procedures. |
| Creating an Intrusion Mission | 169 | missing | — | — | — | No intrusion mission generator. |
| Playing the Mission | 172 | partial | src/rules/cwn_mission_time.py; src/rules/cwn_heat.py | mud/nopunk_mud/solo_campaign.py | tests/test_cwn_mission_time.py; tests/test_cwn_npcs_heat.py; tests/test_solo_campaign_950.py | Mission clock/Heat track exist; the full mission loop is campaign-specific. |
| Mission Rewards and Experience | 176 | partial | src/rules/cwn_advancement.py | — | tests/test_cwn_advancement.py | XP advancement exists; printed mission reward payouts are not modelled. |
| Heat | 178 | complete | src/rules/cwn_heat.py | — | tests/test_cwn_npcs_heat.py | Team-wide track and printed consequence bands; no invented accrual formula. |
| Reaction Rolls | 182 | complete | src/rules/cwn_npcs.py | — | tests/test_cwn_npcs_heat.py | 2d6 + Charisma modifier with all five printed bands. |
| Morale and Morale Checks | 183 | complete | src/rules/cwn_npcs.py | — | tests/test_cwn_npcs_heat.py | Morale 2..12; equal or higher breaks. |
| Beasts and Guard Animals | 185 | missing | — | — | — | Printed stat blocks and beast procedures not ported. |
| Corp Guards and Law Enforcement | 186 | missing | — | — | — | Printed stat blocks not ported. |
| Gangers and Criminals | 188 | missing | — | — | — | Printed stat blocks not ported. |
| Hackers and Pilots | 190 | missing | — | — | — | Printed stat blocks not ported. |
| NPC Cyber Descriptions | 194 | partial | data/rules/cwn_cyberware.json | — | tests/test_cwn_core.py | Cyber data exists; NPC cyber summaries are not a usable stat block. |
| The City (setting chapters) | 196 | not_applicable | — | — | — | Example setting, history and social advice; not generic mechanics. |
| Mixing Sine Nomine Games Together | 218 | not_applicable | — | — | — | Cross-game advice; outside vanilla CWN parity. |
| Index / Backers | 222 | not_applicable | — | — | — | Reference matter. |

## Coverage by chapter

The table above follows the Free Edition table of contents. Character creation, the core rules,
equipment basics, injuries and advancement are substantially implemented. The largest genuine
gaps are GM-facing: chases, drugs, cyberdecks/drone operation, the full hacking simulator, NPC
stat blocks, and the entire mission/scheme/city generation chapter. Those are named as missing
rather than hidden behind data files.

## Implementation backlog (dependency order)

| # | Slice | Evidence | Depends on |
| --- | --- | --- | --- |
| 1 | Parity matrix, validator and baseline audit | this PR | No dependency |
| 2 | Character creation end-to-end: contacts/one-roll tables, starting gear, final sheet, save/load | tests/test_cwn_* | 1 |
| 3 | MUD combat loop: initiative, actions, maneuvers, turn/save-resume, command wiring | cwn_combat* + cwn/* | 2 |
| 4 | Chases, vehicle combat actions, drone operation, cyberdecks | cwn_vehicles, cwn_drones | 3 |
| 5 | Pharmaceuticals, cyberware surgery/mods/maintenance/alienation, gear economy | cwn_core, cwn_gear_mods | 2 |
| 6 | Hacking simulator: node graph, cyberspace actions, programs, demons/watchdogs, servers | cwn_hacking, cwn_program_catalogue | 3 |
| 7 | NPC stat blocks/bestiary, NPC cyber summaries, reaction/morale commands | cwn_npcs | 3 |
| 8 | Mission/scheme/city/megacorp/gang generators, mission tags/types, Heat accrual | cwn_heat + new generator modules | 7 |
| 9 | Solo campaign integration and full book-example acceptance audit | mud/solo_campaign | 2-8 |

Each slice lands as its own PR linked to #1025 and updates this matrix. The issue stays open
until the final acceptance audit has no unexplained `partial`/`missing` mechanical row.
