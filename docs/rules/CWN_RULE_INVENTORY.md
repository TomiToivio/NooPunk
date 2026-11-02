# CWN rule inventory — every Deluxe chapter and section

Source: *Cities Without Number, Deluxe Edition (lightweight PDF, 081123)*, printed pages as they appear in the book (PDF page = printed + 3). Generated from `data/rules/cwn_rule_inventory.json` by `tools/cwn_rule_inventory_audit.py --markdown`; do not edit this table by hand.

**65 rows** — 38 implemented, 9 partial, 6 missing, 12 not_applicable

| printed p. | section | status | python | tests | evidence |
| --- | --- | --- | --- | --- | --- |
| 9 | Character Creation — Attributes | implemented | `src/rules/cwn_character.py` | `tests/test_cwn_character.py` | attribute array, modifiers, substitution |
| 9 | Character Creation — Skills | implemented | `src/rules/cwn_character.py` | `tests/test_cwn_character.py` | skill pools, caps at creation |
| 11 | Character Creation — Choosing a Background | implemented | `src/rules/cwn_backgrounds.py` | `tests/test_cwn_backgrounds.py` | background skill packages |
| 18 | Character Creation — Contacts | partial | `src/rules/cwn_backgrounds.py`<br>`src/rules/social.py` | `tests/test_cwn_backgrounds.py` | contacts are granted by backgrounds and tracked in social.py; the contact network/reaction procedure has no dedicated test yet |
| 20 | Character Creation — Edges | implemented | `src/rules/cwn_edges_foci.py` | `tests/test_cwn_edges_foci.py` | edges incl. Spellcaster/Summoner gating |
| 22 | Character Creation — Foci | implemented | `src/rules/cwn_foci.py`<br>`src/rules/cwn_edges_foci.py` | `tests/test_cwn_foci.py` | focus levels 1-2 |
| 28 | Character Creation — Hit Points, Attack Bonus, and Saves | implemented | `src/rules/cwn_character.py` | `tests/test_cwn_character.py` | HP, attack bonus, saves table |
| 29 | Character Creation — Starting Gear | implemented | `src/rules/cwn_equipment.py` | `tests/test_cwn_equipment.py` | packages and purchasing |
| 30 | Character Creation — Final Touches | implemented | `src/rules/cwn_character.py`<br>`src/rules/cwn_advancement.py` | `tests/test_cwn_advancement.py` | final derived values |
| 34 | The Rules of the Game — Scenes, Rounds, and Mission Time | implemented | `src/rules/cwn_mission_time.py` | `tests/test_cwn_mission_time.py` | scene/round/mission clock |
| 34 | The Rules of the Game — Saving Throws | implemented | `src/rules/cwn_core.py` | `tests/test_cwn_core.py` | four saves, target numbers |
| 35 | The Rules of the Game — Skill Checks | implemented | `src/rules/cwn_core.py` | `tests/test_cwn_core.py` | 2d6 + attribute + skill vs difficulty band |
| 36 | The Rules of the Game — Combat | implemented | `src/rules/cwn_combat.py`<br>`src/rules/cwn_combat_actions.py`<br>`src/rules/cwn_initiative.py`<br>`src/rules/cwn_attack_modifiers.py` | `tests/test_cwn_combat.py`<br>`tests/test_cwn_combat_actions.py` | attacks, actions, initiative, modifiers, shock/trauma |
| 44 | The Rules of the Game — Injury, Healing, and System Strain | implemented | `src/rules/cwn_healing.py`<br>`src/rules/cwn_strain.py`<br>`src/rules/cwn_major_injury.py`<br>`src/rules/cwn_injury_procedure.py`<br>`src/rules/cwn_trauma.py` | `tests/test_cwn_healing.py`<br>`tests/test_cwn_strain.py` | mortal wounds, stabilisation, healing, strain |
| 46 | The Rules of the Game — Vehicle Combat | implemented | `src/rules/cwn_vehicles.py` | `tests/test_cwn_vehicles.py` | vehicle movement and damage |
| 47 | The Rules of the Game — Chases and Pursuit | implemented | `src/rules/cwn_vehicles.py` | `tests/test_cwn_vehicles.py` | pursuit procedure lives beside vehicle combat in cwn_vehicles |
| 48 | The Rules of the Game — Character Advancement | implemented | `src/rules/cwn_advancement.py` | `tests/test_cwn_advancement.py` | XP, levels, skill points |
| 50 | The Rules of the Game — Crafting and Modifying Gear | implemented | `src/rules/cwn_gear_mods.py` | `tests/test_cwn_gear_mods.py` | mods, build/repair costs |
| 52 | The Tools of the Trade — Encumbrance | implemented | `src/rules/cwn_encumbrance.py` | `tests/test_cwn_encumbrance.py` | readied/stowed limits |
| 53 | The Tools of the Trade — Acquiring Gear | implemented | `src/rules/cwn_equipment.py` | `tests/test_cwn_equipment.py` | prices and legality |
| 54 | The Tools of the Trade — Gear, Lifestyles, and Services | implemented | `src/rules/cwn_equipment.py` | `tests/test_cwn_equipment.py` | lifestyles, wages, bribes |
| 56 | The Tools of the Trade — Armor | implemented | `src/rules/cwn_equipment.py` | `tests/test_cwn_equipment.py` | armour classes and accessories |
| 58 | The Tools of the Trade — Weapons | implemented | `src/rules/cwn_equipment.py`<br>`src/rules/cwn_combat.py` | `tests/test_cwn_equipment.py` | weapons, shock, burst, firearms |
| 64 | The Tools of the Trade — Pharmaceuticals and Street Drugs | partial | `data/rules/cwn_catalogue.json`<br>`src/rules/cwn_equipment.py` | `tests/test_cwn_equipment.py` | drug catalogue is data; addiction/recovery procedure not modelled |
| 66 | The Tools of the Trade — Cyberware | implemented | `src/rules/cwn_cyberware.py`<br>`data/rules/cwn_cyberware.json` | `tests/test_cwn_cyberware.py` | systems, strain, installation, removal |
| 79 | The Tools of the Trade — Cyberdecks | implemented | `src/rules/cwn_hacking.py`<br>`data/rules/cwn_hacking.json` | `tests/test_cwn_hacking.py` | deck models and costs |
| 80 | The Tools of the Trade — Drones | implemented | `src/rules/cwn_drones.py`<br>`data/rules/cwn_drones.json` | `tests/test_cwn_drones.py` | drone chassis and control |
| 86 | The Tools of the Trade — Vehicles | implemented | `src/rules/cwn_vehicles.py`<br>`data/rules/cwn_vehicles.json` | `tests/test_cwn_vehicles.py` | vehicle catalogue |
| 96 | Hacking — Cyberspace, Nodes, and Access | implemented | `src/rules/cwn_hacking.py` | `tests/test_cwn_hacking.py` | nodes, access levels |
| 98 | Hacking — Hacking Mechanics | implemented | `src/rules/cwn_hacking.py` | `tests/test_cwn_hacking.py` | verb rolls, alert, tracing |
| 100 | Hacking — Programs | implemented | `src/rules/cwn_program_catalogue.py`<br>`data/rules/cwn_program_catalogue.json` | `tests/test_cwn_program_catalogue.py` | program verbs and costs |
| 106 | Hacking — Demons and Watchdogs | implemented | `src/rules/cwn_hacking.py` | `tests/test_cwn_hacking.py` | demon/watchdog opposition |
| 108 | Hacking — Network Servers and Architecture | implemented | `src/rules/cwn_hacking.py` | `tests/test_cwn_hacking.py` | server architecture |
| 112 | Creating Your Dystopia — Cyberpunk Themes | not_applicable | — | — | GM advice, no mechanic |
| 114 | Creating Your Dystopia — Creating The World | not_applicable | — | — | world-building procedure, no mechanic |
| 118 | Creating Your Dystopia — Creating The City | not_applicable | — | — | city-building procedure |
| 125 | Creating Your Dystopia — Building Your Districts | not_applicable | — | — | district generator is content |
| 130 | Creating Your Dystopia — Creating Megacorps | partial | `src/rules/swn_faction_engine.py` | `tests/test_swn_faction_engine.py` | corp-scale organisations are optional SWN factions, not a CWN rule |
| 132 | Creating Your Dystopia — Creating Gangs | not_applicable | — | — | generator tables are content |
| 134 | Creating Your Dystopia — Creating NPCs | implemented | `src/rules/cwn_npcs.py` | `tests/test_cwn_npcs_heat.py` | NPC statblocks and reaction |
| 137 | Creating and Running Missions — Creating Schemes | not_applicable | — | — | GM procedure |
| 146 | Creating and Running Missions — How To Create a Mission | not_applicable | — | — | GM procedure |
| 148 | Creating and Running Missions — Mission Tags | partial | `data/scenarios` | — | scenario data, no rule engine |
| 162 | Creating and Running Missions — Mission Types | not_applicable | — | — | GM procedure |
| 173 | Creating and Running Missions — Creating an Intrusion Mission | not_applicable | — | — | GM procedure over the hacking rules |
| 176 | Creating and Running Missions — Playing the Mission | not_applicable | — | — | GM procedure |
| 180 | Creating and Running Missions — Mission Rewards and Experience | implemented | `src/rules/cwn_advancement.py` | `tests/test_cwn_advancement.py` | mission XP awards |
| 182 | Creating and Running Missions — Heat | implemented | `src/rules/cwn_heat.py` | `tests/test_cwn_npcs_heat.py` | heat accumulation and police response |
| 186 | Faces On the Street — Reaction Rolls and Morale | implemented | `src/rules/cwn_npcs.py` | `tests/test_cwn_npcs_heat.py` | reaction rolls, morale |
| 189 | Faces On the Street — Beasts and Guard Animals | implemented | `src/rules/cwn_npcs.py`<br>`data/rules/cwn_catalogue.json` | `tests/test_cwn_npcs_heat.py` | animal statlines |
| 190 | Faces On the Street — Corp Guards and Law Enforcement | partial | `data/rules/cwn_catalogue.json` | `tests/test_cwn_equipment.py` | statlines live in the gear catalogue; no dedicated statblock test |
| 192 | Faces On the Street — Gangers and Criminals | partial | `data/rules/cwn_catalogue.json` | `tests/test_cwn_equipment.py` | statlines live in the gear catalogue; no dedicated statblock test |
| 194 | Faces On the Street — Hackers and Pilots | partial | `data/rules/cwn_catalogue.json` | `tests/test_cwn_equipment.py` | statlines live in the gear catalogue; no dedicated statblock test |
| 200 | The City — The City | not_applicable | — | — | setting material |
| 222 | Mixing Sine Nomine Games Together — Mixing Sine Nomine Games Together | not_applicable | — | — | conversion guidance |
| 227 | Supplemental Material — Cyber Product Line Quirks | missing | — | — | no module: quirks are content, but the rule that a quirk changes a system's behaviour is unimplemented |
| 228 | Supplemental Material — Variant Humanity | missing | — | — | no module |
| 230 | Supplemental Material — Cyber Alienation | implemented | `src/rules/cwn_alienation.py` | `tests/test_cwn_alienation.py` | verified against printed pp. 226-231 in this pass |
| 232 | Supplemental Material — Cheap Cyber | missing | — | — | no module; price/maintenance tables are content, the maintenance rule is not modelled |
| 234 | Supplemental Material — Magic in the City | partial | `src/rules/cwn_magic.py` | `tests/test_cwn_magic.py` | the magic *economy* is implemented; campaign frame is prose |
| 235 | Supplemental Material — Mages and Spellcasting | implemented | `src/rules/cwn_magic.py` | `tests/test_cwn_magic.py` | verified against printed pp. 231-233 in this pass |
| 240 | Supplemental Material — Summoners and Spirit Calling | partial | `src/rules/cwn_magic.py` | `tests/test_cwn_magic.py` | Summoner Effort and binding accounting only; spirit statistics are content |
| 247 | Supplemental Material — Magic-User Foci | missing | — | — | no module |
| 248 | Supplemental Material — The Graced | missing | — | — | no module |
| 250 | Supplemental Material — Magic Items | missing | — | — | no module |
