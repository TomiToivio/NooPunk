# CWN rules compliance matrix (NoöPunk MUD)

**Generated** by `python3 tools/cwn_compliance_audit.py --markdown`. Do not edit this
file by hand: edit `data/mud/cwn_compliance.json` and regenerate, so the table and the
audit can never disagree.

**Issue:** https://github.com/TomiToivio/NooPunk/issues/950 · **Rules source:** the linked SRD, <https://cwn.quadrifons.com/>
· **Full book:** Cities Without Number, Deluxe edition (user-supplied PDF) — used only to mark what the linked SRD omits; no text is reproduced

**Rows:** 46 — **30** implemented · **7** partial · **6** godot-only · **1** missing · **2** omitted-by-srd

| # | SRD section | Python target | Godot status | Coverage | Tests | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [Character Creation / Attributes](https://cwn.quadrifons.com/character-creation/attributes/) | `src/rules/cwn_character.py` | `godot/core/cwn_character.gd` | **implemented** | `test_cwn_character.py` | 3d6 in order or the fixed array; one optional 14; the two routes are exclusive. |
| 2 | [Character Creation / Skills](https://cwn.quadrifons.com/character-creation/skills/) | `src/rules/cwn_character.py` | `godot/core/cwn_character.gd` | **implemented** | `test_cwn_character.py` | The creation-time skill pool (0 then 1 then a second skill) — not the 19-skill list, which lives in data/rules/without_number.json. |
| 3 | [Character Creation / Backgrounds](https://cwn.quadrifons.com/character-creation/backgrounds/) | `src/rules/cwn_backgrounds.py` | `godot/core/cwn_character.gd` | **implemented** | `test_cwn_backgrounds.py` |  |
| 4 | [Character Creation / Contacts](https://cwn.quadrifons.com/character-creation/contacts/) | `src/rules/cwn_backgrounds.py` | `godot/core/cwn_contacts.gd` | **partial** | `test_cwn_backgrounds.py` | Contacts exist as background output; the free-contact rolls and their maintenance are GDScript only. |
| 5 | [Character Creation / Edges](https://cwn.quadrifons.com/character-creation/edges/) | `src/rules/cwn_edges_foci.py` | `godot/core/cwn_foci.gd` | **implemented** | `test_cwn_edges_foci.py` |  |
| 6 | [Character Creation / Foci](https://cwn.quadrifons.com/character-creation/foci/) | `src/rules/cwn_foci.py` | `godot/core/cwn_foci.gd` | **implemented** | `test_cwn_foci.py` |  |
| 7 | [Character Creation / Focus Gear Budget](https://cwn.quadrifons.com/character-creation/focus-gear-budget/) | — | `godot/core/cwn_foci.gd` | **godot-only** | `test_cwn_sheet.gd` | The per-focus starting gear allowance has no Python path yet; this is a first migration target. |
| 8 | [Character Creation / Final Steps](https://cwn.quadrifons.com/character-creation/final-steps/) | `src/rules/cwn_character.py` | `godot/core/cwn_character.gd` | **partial** | `test_cwn_character.py` | Attribute/skill finalisation is implemented; the shopping and contact-writing steps are scenario work, not rules. |
| 9 | [Rules / Scenes, Rounds and Mission Time](https://cwn.quadrifons.com/rules-of-the-game/scenes-rounds-mission-time/) | — | `godot/core/cwn_mission_time.gd` | **godot-only** | — | A MUD needs the same clock; port before the single-player campaign is scheduled. |
| 10 | [Rules / Saving Throws](https://cwn.quadrifons.com/rules-of-the-game/saving-throws/) | `src/rules/cwn_core.py` | `godot/core/cwn_combat_rules.gd` | **implemented** | `test_cwn_core.py` | Physical / Evasion / Mental / Luck, d20 against a target. |
| 11 | [Rules / Skill Checks](https://cwn.quadrifons.com/rules-of-the-game/skill-checks/) | `src/rules/wn_core.py` | `godot/core/cwn_combat_rules.gd` | **implemented** | `test_wn_core.py`, `test_wn_core_contract.py` | 2d6 + attribute modifier + skill; the ONE resolution the MUD calls (mud/world/cwn.py). |
| 12 | [Combat / The Combat Sequence](https://cwn.quadrifons.com/rules-of-the-game/combat/combat-sequence) | `src/rules/cwn_combat.py` | `godot/core/combat.gd` | **implemented** | `test_cwn_combat.py` |  |
| 13 | [Combat / Combat Initiative](https://cwn.quadrifons.com/rules-of-the-game/combat/combat-initiative/) | `src/rules/cwn_combat.py` | `godot/core/combat.gd` | **implemented** | `test_cwn_combat.py` |  |
| 14 | [Combat / Combat Actions](https://cwn.quadrifons.com/rules-of-the-game/combat/combat-actions/) | `src/rules/cwn_combat_actions.py` | `godot/core/cwn_combat_actions.gd` | **implemented** | `test_cwn_combat_actions.py` |  |
| 15 | [Combat / Attacks in Combat](https://cwn.quadrifons.com/rules-of-the-game/combat/attacks-in-combat/) | `src/rules/cwn_core.py` | `godot/core/cwn_combat_rules.gd` | **implemented** | `test_cwn_core.py`, `test_cwn_attack_modifiers.py` | Attack roll, hit, and the modifiers table. |
| 16 | [Combat / Damage, Trauma and Shock](https://cwn.quadrifons.com/rules-of-the-game/combat/damage-trauma-shock/) | `src/rules/cwn_trauma.py` | `godot/core/cwn_combat_rules.gd` | **implemented** | `test_cwn_trauma.py`, `test_cwn_core.py` |  |
| 17 | [Combat / Special Combat Maneuvers](https://cwn.quadrifons.com/rules-of-the-game/combat/special-combat-maneuvers/) | `src/rules/cwn_combat.py` | `godot/core/cwn_combat_actions.gd` | **partial** | `test_cwn_combat.py` | Maneuver resolution exists; the full maneuver list is data the MUD has not yet needed. |
| 18 | [Combat / Vehicle Combat](https://cwn.quadrifons.com/rules-of-the-game/combat/vehicle-combat/) | `src/rules/cwn_vehicles.py` | `godot/core/cwn_srd_vehicles.gd` | **partial** | `test_cwn_vehicles.py` | Vehicle statistics and attacks; the chase procedure is the remaining piece. |
| 19 | [Rules / Injury, Healing and System Strain](https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain) | `src/rules/cwn_injury_procedure.py` | `godot/core/cwn_injury.gd` | **implemented** | `test_cwn_injury_procedure.py` |  |
| 20 | [Injury / Mortal Injury and Stabilization](https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/mortal-injury-stabilization/) | `src/rules/cwn_major_injury.py` | `godot/core/cwn_injury.gd` | **implemented** | `test_cwn_major_injury.py` |  |
| 21 | [Injury / System Strain](https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/system-strain/) | `src/rules/cwn_strain.py` | `godot/core/cwn_strain.gd` | **implemented** | `test_cwn_strain.py` |  |
| 22 | [Injury / Natural Healing, First Aid and Poisons](https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/natural-healing-first-aid-poisons/) | `src/rules/cwn_healing.py` | `godot/core/cwn_healing.gd` | **implemented** | `test_cwn_healing.py` |  |
| 23 | [Injury / Major Injuries](https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/major-injuries/) | `src/rules/cwn_major_injury.py` | `godot/core/cwn_injury.gd` | **implemented** | `test_cwn_major_injury.py` |  |
| 24 | [Rules / Chases and Pursuit](https://cwn.quadrifons.com/rules-of-the-game/chases-and-pursuit/) | `src/rules/cwn_vehicles.py` | `godot/core/cwn_chases.gd` | **godot-only** | `test_cwn_vehicles.gd` | The Python module has chase-related vehicle data; the pursuit round structure is GDScript only. |
| 25 | [Rules / Character Advancement](https://cwn.quadrifons.com/rules-of-the-game/character-advancement/) | `src/rules/cwn_advancement.py` | `godot/core/cwn_progression.gd` | **implemented** | `test_cwn_advancement.py` |  |
| 26 | [Rules / Crafting and Modifying Gear](https://cwn.quadrifons.com/rules-of-the-game/crafting-modifying-gear/) | `src/rules/cwn_gear_mods.py` | `godot/core/cwn_gear_mods.gd` | **implemented** | `test_cwn_gear_mods.py` | Crafting, modifying, maintaining and factory mods. |
| 27 | [Rules / Encumbrance](https://cwn.quadrifons.com/rules-of-the-game/encumbrance/) | `src/rules/cwn_encumbrance.py` | `godot/core/cwn_encumbrance.gd` | **implemented** | `test_cwn_encumbrance.py` |  |
| 28 | [Gear / Mission Gear](https://cwn.quadrifons.com/gear-vehicles-cyberware/mission-gear/) | `src/rules/cwn_equipment.py` | `godot/core/cwn_catalogue.gd` | **implemented** | `test_cwn_equipment.py` |  |
| 29 | [Gear / Lifestyles, Wages and Bribes](https://cwn.quadrifons.com/gear-vehicles-cyberware/lifestyles-wages-and-bribes/) | `src/rules/cwn_core.py` | `godot/core/cwn_lifestyles.gd, godot/core/cwn_wages.gd` | **partial** | `test_cwn_lifestyles.gd`, `test_cwn_wages.gd` | Lifestyle costs are referenced in Python; the wages and bribe tables are GDScript only. Migration target. |
| 30 | [Gear / Armor](https://cwn.quadrifons.com/gear-vehicles-cyberware/armor/) | `src/rules/cwn_equipment.py` | `godot/core/cwn_catalogue.gd` | **implemented** | `test_cwn_equipment.py` | Armour types, accessories and mods; encumbrance interaction in cwn_encumbrance. |
| 31 | [Gear / Weapons](https://cwn.quadrifons.com/gear-vehicles-cyberware/weapons/) | `src/rules/cwn_equipment.py` | `godot/core/cwn_catalogue.gd` | **implemented** | `test_cwn_equipment.py` | Firearms, melee, heavy weapons, mods and damage profiles. |
| 32 | [Gear / Pharmaceuticals and Street Drugs](https://cwn.quadrifons.com/gear-vehicles-cyberware/pharmaceuticals-street-drugs/) | — | `godot/core/cwn_drugs.gd` | **godot-only** | `test_cwn_drugs.gd` | A data table plus effect procedures; the MUD needs it for any medical scene. |
| 33 | [Gear / Cyberware (installation, complications, tools, removal, concealing, maintenance)](https://cwn.quadrifons.com/gear-vehicles-cyberware/cyberware/) | `src/rules/cwn_core.py` | `godot/core/cwn_cyberware.gd, godot/core/cwn_cyberware_ops.gd` | **partial** | `test_cwn_core.py`, `test_cwn_cyberware.gd` | Installation terms, surgery and maintenance minutes are in Python; the complication table and cyberdoc tools are GDScript only. |
| 34 | [Gear / Cyberware / Skillplugs](https://cwn.quadrifons.com/gear-vehicles-cyberware/cyberware/skillplugs/) | — | — | **missing** | — | No implementation anywhere. Small and self-contained: a good first MUD-era port. |
| 35 | [Gear / Cyberware Mods and Systems](https://cwn.quadrifons.com/gear-vehicles-cyberware/cyberware/cyberware-systems/) | — | `godot/core/cwn_cyberware.gd` | **godot-only** | `test_cwn_cyberware.gd` | Body/head/skin/limb/sensory/medical/nerve systems are catalogue data plus effect procedures. |
| 36 | [Gear / Cyberware Alienation](https://cwn.quadrifons.com/gear-vehicles-cyberware/cyberware/cyberware-alienation/) | — | `godot/core/cwn_alienation.gd` | **godot-only** | `test_cwn_alienation.gd` | The clearest migration gap: a full subsystem with tests on the Godot side and nothing in Python. |
| 37 | [Gear / Cyberdecks](https://cwn.quadrifons.com/gear-vehicles-cyberware/cyberdecks/) | `src/rules/cwn_hacking.py` | `godot/core/cwn_catalogue.gd` | **implemented** | `test_cwn_hacking.py` |  |
| 38 | [Gear / Drones](https://cwn.quadrifons.com/gear-vehicles-cyberware/drones/) | `src/rules/cwn_drones.py` | `godot/core/cwn_drones.gd` | **implemented** | `test_cwn_drones.py` |  |
| 39 | [Gear / Vehicles](https://cwn.quadrifons.com/gear-vehicles-cyberware/vehicles/) | `src/rules/cwn_vehicles.py` | `godot/core/cwn_vehicles.gd` | **implemented** | `test_cwn_vehicles.py` |  |
| 40 | [Hacking / Cyberspace Basics](https://cwn.quadrifons.com/hacking/cyberspace-basics/) | `src/rules/cwn_hacking.py` | `godot/core/cwn_hacking.gd` | **implemented** | `test_cwn_hacking.py` | Access pools and security difficulty; see also D55 (the access model is an open author question). |
| 41 | [Hacking / Programs: acquiring, writing, verbs, subjects](https://cwn.quadrifons.com/hacking/programs/) | `src/rules/cwn_program_catalogue.py` | `godot/core/cwn_programs.gd, godot/core/cwn_program_rules.gd` | **implemented** | `test_cwn_program_catalogue.py` |  |
| 42 | [Hacking / Hacking Mechanics](https://cwn.quadrifons.com/hacking/hacking-mechanics/) | `src/rules/cwn_hacking.py` | `godot/core/cwn_hacking.gd` | **implemented** | `test_cwn_hacking.py` | Includes the Trace clock (AlertClock). |
| 43 | [Hacking / Cyberspace Actions](https://cwn.quadrifons.com/hacking/cyberspace-actions/) | `src/rules/cwn_hacking.py` | `godot/core/cwn_hacking.gd` | **implemented** | `test_cwn_hacking.py` |  |
| 44 | [Hacking / Demons and Watchdogs](https://cwn.quadrifons.com/hacking/demons-watchdogs/) | `src/rules/cwn_hacking.py` | `godot/core/cwn_demons.gd` | **partial** | `test_cwn_hacking.py` | Opposition is modelled; the demon catalogues are GDScript data. |
| 45 | Antagonists and NPCs | — | — | **omitted-by-srd** | — | The linked SRD states it omits this section. Coverage of the full book is therefore NOT claimed anywhere in this matrix; the Deluxe PDF is the only source and is not open content. |
| 46 | Optional rules | — | — | **omitted-by-srd** | — | Same limitation, stated by the SRD itself. Any later row claiming an optional rule must cite the full book, not the SRD. |

## What this matrix does and does not claim

* A row is **implemented** only when a Python module owns the procedure and a Python test
  exercises it. The audit fails a row that claims implemented with only a GDScript test.
* **godot-only** rows are migration targets, not coverage. They are the first work for the
  MUD-era port: `-` focus gear budget, mission time, chases, wages and bribes,
  pharmaceuticals, cyberware mods/systems, cyberware alienation.
* **omitted-by-srd** rows record the linked SRD's own stated gaps (antagonists and optional
  rules). Coverage of the full published book is **not** claimed anywhere.
* Overlays (GUMSHOE investigation, Noösphere/Psychic modules, ideology) are NoöPunk modules
  layered on this baseline and are deliberately absent from this table.

