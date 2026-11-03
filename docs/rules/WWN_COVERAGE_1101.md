# Worlds Without Number — coverage register (#1101)

**94 rows** across the free SRD, the free-book-only material and Deluxe. Source: the [WWN SRD](https://wwn.quadrifons.com/) (CC0; system text only).

This is an **audit**, not a claim that NoöPunk runs Worlds Without Number. The tabletop rulebook remains CWN; WWN rows are the code-level supplement the issue asks for. A row is `verified reuse` only where the procedure is the shared Without Number chassis and a CWN test exercises it.

Citations are **section anchors**, not page numbers: the CC0 SRD is unpaginated and the free-book PDF was unavailable (HTTP 403), so no page is invented. Deluxe rows carry the issue's printed page because those are the only pages we can state without the text.

## What the audit found

| Status | Rows | Meaning |
| --- | ---: | --- |
| implemented | 11 | WWN-specific module, procedure and test exist. |
| verified reuse | 11 | The procedure is the shared Without Number/CWN chassis and is tested there. |
| partial | 13 | Some code or catalogue exists; the named procedure is incomplete. |
| missing | 42 | No implementation. |
| blocked | 9 | Source text unavailable/lawful text not on this host; must not be synthesised. |
| n/a | 8 | Chapter index or setting-only material with no procedure. |

- **22 of 94** rows are implemented or verified reuse; the rest are named gaps, not silently missing.
- **9 blocked** rows are Deluxe or free-book-only procedures whose lawful text is not on this host. They are not synthesised.
- Of the 85 free-SRD rows, **22 are implemented or reused**, so the SRD is not the bottleneck; the unimplemented systems are (classes, factions, equipment, bestiary, travel).

## Register

| § | Procedure | Status | Code | Tests | Tabletop | Note |
| --- | --- | --- | --- | --- | --- | --- |
| | **Character Creation** | | | | | |
| 1.0.0 | Character Creation | n/a | — | — | reference_only | Chapter index; counted in its sections, not as a procedure. |
| 1.1.0 | Attributes | verified reuse | `wn_core.py` (attribute_modifier, skill_check, opposed_check) | `test_wn_core_contract.py` | cwn_delegated | Same six attributes and modifier curve; CWN/Without Number chassis. |
| 1.2.0 | Skills | partial | `wn_core.py` (attribute_modifier, skill_check, opposed_check) | `test_wn_core_contract.py` | cwn_delegated | The 2d6 check is shared; the WWN skill list is not mapped onto CWN skills. |
| 1.3.0 | Backgrounds | missing | — | — | reference_only | No WWN backgrounds; CWN backgrounds govern character creation. |
| 1.4.0 | Classes | partial | — | — | reference_only | Class framework absent; only the High Mage has a class table. |
| 1.5.0 | Class List | n/a | — | — | reference_only | Chapter index; counted in its sections, not as a procedure. |
| 1.5.1 | The Adventurer | partial | `wwn_high_mage.py` (HighMage, ARTS, HIGH_MAGE_TABLE…) | `test_wwn_high_mage.py` | reference_only | Partial-caster table exists; no Adventurer combination engine. |
| 1.5.2 | The Accursed | missing | — | — | reference_only | Not implemented. |
| 1.5.3 | The Bard | missing | — | — | reference_only | Not implemented. |
| 1.5.4 | The Beastmaster | missing | — | — | reference_only | Not implemented. |
| 1.5.5 | The Blood Priest | missing | — | — | reference_only | Not implemented. |
| 1.5.6 | The Duelist | missing | — | — | reference_only | Not implemented. |
| 1.5.7 | The Elementalist | partial | `wwn_spells.py` (SPELLS, learning_days, free_spells_per_level…) | `test_wwn_spells.py` | reference_only | 15 spells catalogued; class Arts and progression absent. |
| 1.5.8 | The Expert | missing | — | — | reference_only | Not implemented. |
| 1.5.9 | The Healer | missing | — | — | reference_only | Not implemented. |
| 1.5.10 | The High Mage | implemented | `wwn_high_mage.py` (HighMage, ARTS, HIGH_MAGE_TABLE…) | `test_wwn_high_mage.py` | reference_only | Full and partial Arts/Spells tables, Effort, preparation, casting. |
| 1.5.11 | The Invoker | missing | — | — | reference_only | Not implemented. |
| 1.5.12 | The Mage | missing | — | — | reference_only | Not implemented. |
| 1.5.13 | The Mageslayer | missing | — | — | reference_only | Not implemented. |
| 1.5.14 | The Necromancer | partial | `wwn_spells.py` (SPELLS, learning_days, free_spells_per_level…) | `test_wwn_spells.py` | reference_only | 16 spells catalogued; class Arts and progression absent. |
| 1.5.15 | The Skinshifter | missing | — | — | reference_only | Not implemented. |
| 1.5.16 | The Thought Noble | missing | — | — | reference_only | Not implemented. |
| 1.5.17 | The Vowed | missing | — | — | reference_only | Not implemented. |
| 1.5.18 | The Warrior | missing | — | — | reference_only | Not implemented. |
| 1.5.19 | The Wise | missing | — | — | reference_only | Not implemented. |
| 1.6.0 | Foci | missing | — | — | reference_only | Not implemented. |
| 1.7.0 | Final Character Creation Steps | partial | — | — | reference_only | CWN final steps available; WWN packages/Foci absent. |
| | **Rules of the Game** | | | | | |
| 2.0.0 | The Rules of the Game | n/a | — | — | reference_only | Chapter index; counted in its sections, not as a procedure. |
| 2.1.0 | Scenes, Rounds, and Mission Time | verified reuse | `cwn_mission_time.py` (MissionClock, Tick) | `test_cwn_mission_time.py` | cwn_delegated | Shared Without Number chassis; no WWN-specific code. |
| 2.2.0 | Saving Throws | verified reuse | `cwn_core.py` (save_target, saving_throw, shock_applies) | `test_cwn_core.py` | cwn_delegated | Shared Without Number chassis; no WWN-specific code. |
| 2.3.0 | Skill Checks | verified reuse | `wn_core.py` (attribute_modifier, skill_check, opposed_check) | `test_wn_core_contract.py` | cwn_delegated | Shared Without Number chassis; no WWN-specific code. |
| 2.4.0 | Combat | verified reuse | `cwn_core.py` (save_target, saving_throw, shock_applies) | `test_cwn_core.py` | cwn_delegated | CWN combat is the chassis; ignore CWN Trauma when running WWN. |
| 2.5.0 | Injury, Healing, and System Strain | verified reuse | `cwn_healing.py` (natural_healing, stabilized, Patient)<br>`cwn_strain.py` (SystemStrain) | `test_cwn_healing.py`<br>`test_cwn_strain.py` | cwn_delegated | Shared Without Number chassis; no WWN-specific code. |
| 2.6.0 | Chases and Pursuit | verified reuse | `cwn_vehicles.py` (resolve_chase, ChaseOutcome) | `test_cwn_vehicles.py` | cwn_delegated | Shared Without Number chassis; no WWN-specific code. |
| 2.7.0 | Character Advancement | partial | `cwn_advancement.py` (level_for_xp, attack_bonus) | `test_cwn_advancement.py` | reference_only | CWN XP/level tables only; WWN class advancement tables absent. |
| 2.8.0 | Crafting and Modifying Gear | verified reuse | `cwn_gear_mods.py` (load_mods, weapon_mod) | `test_cwn_gear_mods.py` | cwn_delegated | Shared Without Number chassis; no WWN-specific code. |
| 2.9.0 | Encumbrance | verified reuse | `cwn_encumbrance.py` (stowed_capacity, readied_capacity, tier_for) | `test_cwn_encumbrance.py` | cwn_delegated | Shared Without Number chassis; no WWN-specific code. |
| 2.10.0 | Falling and Other Hazards | missing | — | — | reference_only | Falling/hazard procedure not ported. |
| 2.11.0 | Overland Travel | missing | — | — | reference_only | Overland travel not ported. |
| 2.12.0 | Wilderness Exploration and Expeditions | missing | — | — | reference_only | Wilderness expeditions not ported. |
| 2.13.0 | Dungeon Exploration | missing | — | — | reference_only | Dungeon exploration not ported. |
| | **Equipment** | | | | | |
| 3.0.0 | Equipment, Armor, and Weapons | n/a | — | — | reference_only | Chapter index; counted in its sections, not as a procedure. |
| 3.1.0 | Money and Currency | missing | — | — | reference_only | CWN currency/economy governs. |
| 3.2.0 | Adventuring Gear | missing | — | — | reference_only | No WWN gear catalogue. |
| 3.3.0 | Hirelings and Services | missing | — | — | reference_only | No WWN hireling procedure. |
| 3.4.0 | Armor | missing | — | — | reference_only | CWN armour list governs; WWN list absent. |
| 3.5.0 | Weapons | missing | — | — | reference_only | CWN weapons list governs; WWN list absent. |
| | **Magic** | | | | | |
| 4.0.0 | Magic and Spellcasting | n/a | — | — | reference_only | Chapter index; counted in its sections, not as a procedure. |
| 4.1.0 | Spells and Arts | implemented | `wwn_spells.py` (SPELLS, learning_days, free_spells_per_level…)<br>`wwn_high_mage.py` (HighMage, ARTS, HIGH_MAGE_TABLE…) | `test_wwn_spells.py`<br>`test_wwn_high_mage.py` | reference_only | 83 spells (52/15/16) and the High Mage Arts. |
| 4.2.0 | Preparing and Casting Spells | implemented | `wwn_high_mage.py` (HighMage, ARTS, HIGH_MAGE_TABLE…) | `test_wwn_high_mage.py` | reference_only |  |
| 4.3.0 | Dual Partial Spellcasters | partial | `wwn_high_mage.py` (HighMage, ARTS, HIGH_MAGE_TABLE…) | `test_wwn_high_mage.py` | reference_only | Partial High Mage table only; dual pools/combination absent. |
| 4.4.0 | High Magic Spells by Level | implemented | `wwn_spells.py` (SPELLS, learning_days, free_spells_per_level…) | `test_wwn_spells.py` | reference_only |  |
| 4.4.1 | High Magic Spells by Name | implemented | `wwn_spells.py` (SPELLS, learning_days, free_spells_per_level…) | `test_wwn_spells.py` | reference_only |  |
| 4.5.0 | Elementalist Spells | partial | `wwn_spells.py` (SPELLS, learning_days, free_spells_per_level…) | `test_wwn_spells.py` | reference_only | Catalogue only; effects 0/15 transcribed. |
| 4.6.0 | Necromancer Spells | partial | `wwn_spells.py` (SPELLS, learning_days, free_spells_per_level…) | `test_wwn_spells.py` | reference_only | Catalogue only; effects 0/16 transcribed. |
| 4.7.0 | Developing New Spells | missing | — | — | reference_only | Not implemented. |
| 4.8.0 | Building Magical Workings | partial | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only | Only the permanent-working Renown multiplier; no working procedure. |
| 4.9.0 | Magic Items and Enchanted Treasures | missing | — | — | reference_only | Not implemented. |
| 4.10.0 | Creating Magic Items | missing | — | — | reference_only | Not implemented. |
| | **Monsters and Foes** | | | | | |
| 5.0.0 | Monsters and Foes | n/a | — | — | reference_only | Chapter index; counted in its sections, not as a procedure. |
| 5.1.0 | Monster and NPC Statistics | missing | — | — | reference_only | No WWN stat-block model/bestiary. |
| 5.2.0 | Reaction Rolls and Parleying | verified reuse | `cwn_npcs.py` (reaction_roll, morale_check) | `test_cwn_npcs_heat.py` | cwn_delegated | 2d6 reaction bands shared with CWN; parleying prose not ported. |
| 5.3.0 | Morale Checks and Fleeing | verified reuse | `cwn_npcs.py` (reaction_roll, morale_check) | `test_cwn_npcs_heat.py` | cwn_delegated | 2d6 morale check shared with CWN; fleeing prose not ported. |
| 5.4.0 | Instinct Checks | missing | — | — | reference_only | Not implemented. |
| | **Factions** | | | | | |
| 6.0.0 | Factions | n/a | — | — | reference_only | Chapter index; counted in its sections, not as a procedure. |
| 6.1.0 | Faction Statistics | missing | — | — | reference_only | WWN faction engine absent; SWN engine is a different system. |
| 6.2.0 | The Faction Turn | missing | — | — | reference_only | WWN faction engine absent. |
| 6.3.0 | Asset Locations and Movement | missing | — | — | reference_only | WWN faction engine absent. |
| 6.4.0 | Attribute Checks | missing | — | — | reference_only | WWN faction engine absent. |
| 6.5.0 | Faction Tags | missing | — | — | reference_only | WWN faction engine absent. |
| 6.6.0 | Faction Turn Actions | missing | — | — | reference_only | WWN faction engine absent. |
| 6.7.0 | Creating Factions | missing | — | — | reference_only | WWN faction engine absent. |
| 6.8.0 | Cunning Assets | missing | — | — | reference_only | WWN faction engine absent. |
| 6.9.0 | Force Assets | missing | — | — | reference_only | WWN faction engine absent. |
| 6.10.0 | Wealth Assets | missing | — | — | reference_only | WWN faction engine absent. |
| | **Major Projects** | | | | | |
| 7.0.0 | Major Projects | n/a | — | — | reference_only | Chapter index; counted in its sections, not as a procedure. |
| 7.1.0 | Renown | implemented | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only |  |
| 7.2.0 | Determining the Project Difficulty | implemented | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only |  |
| 7.3.0 | Determining the Project Scope | implemented | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only |  |
| 7.4.0 | Determining the Opposition | implemented | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only |  |
| 7.5.0 | Decreasing Difficulty | implemented | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only |  |
| 7.6.0 | Achieving the Goal | implemented | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only |  |
| 7.7.0 | Magical Projects | partial | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only |  |
| 7.8.0 | Major Projects and Existing Factions | partial | `wwn_projects.py` (project_difficulty, renown_after_adventures, ProjectState…) | `test_awn_wwn_campaign_procedures.py` | reference_only |  |
| 7.9.0 | Player Run Factions and Major Projects | missing | — | — | reference_only | Not implemented. |
| | **Deluxe** | | | | | |
| G.0.0 | The Legates p.322 | blocked | — | — | blocked | Legate class framework, Words, and dominion play. Deluxe PDF not on this host; not synthesised. |
| H.0.0 | Iterums and the Gyre p.344 | blocked | — | — | blocked | Iterum creation, paths, and the Gyre. Deluxe PDF not on this host; not synthesised. |
| I.0.0 | The Latter Earth p.356 | blocked | — | — | blocked | Setting material; CC0 does not cover protected setting text. Deluxe PDF not on this host; not synthesised. |
| J.0.0 | Ruins and Relics p.358 | blocked | — | — | blocked | Deluxe ruin/relic procedures. Deluxe PDF not on this host; not synthesised. |
| K.0.0 | The Sciences of the Latter Earth p.370 | blocked | — | — | blocked | Deluxe science/technology rules. Deluxe PDF not on this host; not synthesised. |
| | **World and Campaign** | | | | | |
| D.1.0 | Worldbuilding p.94 | blocked | — | — | blocked | World creation and history tools. Not in the CC0 SRD; the free-book mirror returns HTTP 403; not synthesised. |
| D.2.0 | Sandbox Play p.160 | blocked | — | — | blocked | Sandbox/campaign fronts. Not in the CC0 SRD; the free-book mirror returns HTTP 403; not synthesised. |
| D.3.0 | Sites and Ruins p.210 | blocked | — | — | blocked | Location/ruin generators. Not in the CC0 SRD; the free-book mirror returns HTTP 403; not synthesised. |
| D.4.0 | NPC and Faction Tools p.250 | blocked | — | — | blocked | Supporting-cast and faction tools. Not in the CC0 SRD; the free-book mirror returns HTTP 403; not synthesised. |

## Cross-game compatibility

The issue asks for a CWN↔WWN↔SWN↔AWN matrix. This is the part that can be stated without inventing conversions; each row names what exists and what does not.

| Area | Status | Code | Note |
| --- | --- | --- | --- |
| Characteristics, saves, skill checks | verified reuse | `wn_core.py`, `cwn_core.py` | Same 2d6/d20 chassis. |
| Classes and advancement | partial | `wwn_high_mage.py` | High Mage only; 15 classes absent and 3 partial. CWN classes remain the tabletop default. |
| Magic and spellcasting | partial | `wwn_spells.py`, `wwn_high_mage.py` | Catalogue + High Mage; other traditions effects absent. |
| Equipment and economy | missing | — | CWN catalogue governs; no WWN conversion. |
| Creatures and NPCs | partial | `cwn_npcs.py` | Reaction/morale only; no bestiary. |
| Factions | missing | `swn_faction_engine.py` | SWN faction engine exists but is a different system; not reused. |
| Major projects | implemented | `wwn_projects.py` | Renown/difficulty/scope/opposition/advancement; magical workings partial. |
| Travel, wilderness, dungeon, hazards | missing | — | AWN survival exists but WWN procedures are not mapped. |

## Blocked sources

- **Deluxe (G–K)**: *The Legates*, Iterums/Gyre, the Latter Earth, Ruins and Relics, Sciences of the Latter Earth. The Deluxe PDF is not on this host; the CC0 SRD does not cover it. Nine rows are blocked, not guessed.
- **Free-book-only world/campaign tools (pp. 94–279)**: not in the CC0 SRD; the free-book mirror cited by #1101 returned HTTP 403 on 2026-11-03. Four rows are blocked.
- Rights: `data/sources/game_system_rights.json#worlds-without-number-srd` records `verified-public-domain` for the **SRD**, not the commercial book or its protected setting. Do not copy setting text from either edition.

## Next queue (Phase 2, by dependency)

1. **Classes**: 15 of 19 absent, 3 partial (Adventurer, Elementalist, Necromancer); start with Warrior/Expert/Mage and the Adventurer combination engine, then Foci. High Mage is the only implemented class.
2. **Factions**: the WWN faction turn is wholly absent. The SWN engine is a different system — reuse its dice/state utilities only after a named parity check.
3. **Equipment and bestiary**: no WWN catalogues; the CWN lists govern the tabletop, so this is a conversion decision, not a transcription sprint.
4. **Travel/wilderness/dungeon/hazards**: unported; AWN survival exists but is not WWN.
5. **Spell effects**: 13 of 83 transcribed (#1085); do not duplicate its queue.
6. **Deluxe G–K**: blocked until a lawful copy exists.

## Verification

```bash
python3.11 tools/wwn_coverage_audit_1101.py --check
```

The check verifies every claimed module/procedure via AST, every test path, the implemented/test link, and that this report is byte-identical to a fresh render.

Generated by `tools/wwn_coverage_audit_1101.py` from `data/rules/wwn_traceability.json`; do not edit by hand.
