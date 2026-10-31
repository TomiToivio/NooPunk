# CWN compliance matrix (#950)

Generated from `data/rules/cwn_compliance_matrix.json` by `tools/check_cwn_compliance.py --render`.
Do not edit by hand: edit the JSON and regenerate, or the matrix and its evidence disagree.

**Source:** https://cwn.quadrifons.com/

> The linked SRD omits some optional rules and the Antagonists/NPC sections. Coverage here describes the linked SRD; the full published rulebook is out of scope until legally available text is used.

Status is deliberately conservative: **implemented** requires an existing test; a module without a test
is **partial**. A section the linked SRD omits is **missing**, however much code mentions it.

| System | SRD | Godot | Python | MUD | Coverage | Tests | Divergence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Attributes and modifiers** | Character Creation — Attributes | `cwn_character.gd` | `wn_core.py`<br>`cwn_character.py` | `__init__.py` | `implemented` | `test_mud_cwn_parity_950.py`<br>`test_cwn_rules.gd` | — |
| **Skill checks (2d6 + rank + modifier vs band)** | Rules of the Game — Skill Checks | `rules_adapter.gd` | `wn_core.py` | `__init__.py` | `implemented` | `test_mud_cwn_parity_950.py` | — |
| **Saving throws (Physical / Evasion / Mental / Luck)** | Rules of the Game — Saving Throws | `cwn_character.gd` | `cwn_core.py` | `__init__.py` | `implemented` | `test_mud_cwn_parity_950.py` | — |
| **Hit points and advancement rolls** | Character Creation — Hit Points; Advancement | `cwn_character.gd`<br>`cwn_progression.gd` | `cwn_advancement.py` | `__init__.py` | `implemented` | `test_mud_cwn_parity_950.py` | — |
| **System Strain (capacity, lifestyle, cyberware cost)** | Equipment — System Strain; Cyberware | `cwn_cyberware_ops.gd` | `cwn_strain.py`<br>`cwn_core.py` | `__init__.py` | `implemented` | `test_mud_cwn_parity_950.py` | — |
| **Backgrounds** | Character Creation — Backgrounds | `cwn_character.gd` | `cwn_backgrounds.py` | — | `partial` | — | Data and selection exist; no MUD character-creation flow yet. |
| **Edges and Foci** | Character Creation — Edges and Foci | `cwn_character.gd` | `cwn_edges_foci.py`<br>`cwn_foci.py` | — | `partial` | — | Implemented in Python and Godot; not yet reachable from a MUD command. |
| **Combat: initiative, action economy, attacks, damage** | Combat | `combat.gd`<br>`cwn_attack_modifiers.gd` | `cwn_combat.py`<br>`cwn_combat_actions.py`<br>`cwn_core.py` | — | `partial` | `test_cwn_combat.py`<br>`test_cwn_combat_actions.py` | Resolution exists on both sides; no Evennia combat command or turn loop yet. |
| **Trauma, Shock and major injury** | Combat — Trauma and Shock | `combat.gd` | `cwn_trauma.py`<br>`cwn_major_injury.py` | — | `partial` | — | Python kernels exist and are tested; the MUD has no combat loop to call them from. |
| **Injury, stabilisation, healing** | Combat — Injury and Healing | `cwn_healing.gd` | `cwn_healing.py`<br>`cwn_injury_procedure.py` | — | `partial` | — | Not yet wired to MUD state persistence. |
| **Weapons, armour, encumbrance, gear** | Equipment | — | `cwn_equipment.py`<br>`cwn_encumbrance.py` | — | `partial` | — | Catalogues and encumbrance exist; MUD inventory is currently a simple dict. |
| **Gear modifications and crafting** | Equipment — Modifications; Crafting | `cwn_gear_mods.gd` | `cwn_gear_mods.py` | — | `partial` | — | — |
| **Lifestyles, wages and bribes** | Equipment — Cost of Living | `cwn_contacts.gd` | `cwn_core.py` | — | `partial` | — | Strain-by-lifestyle is ported to the MUD; wages and bribes are not. |
| **Vehicles and vehicle combat** | Equipment — Vehicles; Vehicle Combat | `cwn_vehicles.gd` | `cwn_vehicles.py` | — | `partial` | — | — |
| **Drones** | Equipment — Drones | `cwn_drones.gd` | `cwn_drones.py` | — | `partial` | — | — |
| **Chases and pursuit** | Rules of the Game — Chases | `cwn_chases.gd` | — | — | `partial` | — | Godot-only; no Python or MUD implementation. |
| **Cyberware installation, complications, maintenance, Alienation** | Cyberware | `cwn_cyberware_ops.gd`<br>`cwn_alienation.gd` | `cwn_core.py` | — | `partial` | — | Installation terms and Alienation tables exist; the MUD has no implant inventory yet. |
| **Hacking: decks, access, programs, subjects and verbs** | Hacking | `hacking.gd`<br>`cwn_node_link.gd` | `cwn_hacking.py`<br>`cwn_program_catalogue.py` | — | `partial` | `test_cwn_hacking_contract.py` | Playable in Godot as a node-link screen; no MUD command surface. |
| **Demons, watchdogs and countermeasures** | Hacking — Intrusion Countermeasures | `hacking.gd` | `cwn_hacking.py` | — | `partial` | — | Partial on both sides; the linked SRD's treatment is limited. |
| **Antagonists and NPC statistics** | Antagonists (not included in the linked SRD) | — | — | — | `missing` | — | The linked hosted SRD omits the Antagonists/NPC section. Not implemented and not claimed; needs legally available official text. |

## Totals

**implemented**: 5 · **missing**: 1 · **partial**: 14

## Notes

- The MUD column is empty wherever only the Godot or Python layer implements the rule; that is a
  port target, not a contradiction.
- Tabletop references point at the rulebook segment that owns the same rule, so a mechanic change
  has one place to update besides the code and this matrix.
