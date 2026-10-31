# CWN compliance matrix: Godot (incumbent) versus Evennia MUD (target)

**Status: inventory, not conformance.** This file answers item 2 of #950: *"Inventory existing Godot CWN
features and Evennia baseline; publish linked-SRD compliance matrix (and explicitly mark omissions)."*

**Read the status column carefully.** `present` means a module or function exists and is tested at the
level its own suite tests it. It does **not** mean the implementation has been verified line-by-line
against the SRD. Only the rows marked `verified` have had their procedure read against the source. The
rest are `present (unverified)` — an honest label, because a file named `cwn_chases.gd` is evidence that
someone implemented chases, not evidence that they match the SRD.

Scope: `main`. Godot counts `godot/core/`; Evennia counts `mud/nopunk_mud/cwn/`, `mud/nopunk_mud/cwn_core.py`,
`mud/systems/cwn.py` and `mud/nopunk_mud/rules_contract.py`.

## 1. What the port must carry

| SRD area | Godot (`godot/core/`) | Evennia (`mud/`) | Status |
| --- | --- | --- | --- |
| Core resolution: 2d6 skill check, d20 attack/save, modifier ladder | `dice.gd`, `rules_adapter.gd`, `cwn_sheet.gd` | `cwn/__init__.py` (`skill_check`, `skill_modifier`, `attack_roll`, `saving_throw`, `save_target`, `attribute_modifier`) | **ported, verified by tests** |
| Attributes and character creation | `cwn_character.gd` | `create_character`, `Character`, `validate_sheet` | **ported, verified by tests** |
| Hit points, damage, trauma, strain | `cwn_injury.gd`, `cwn_strain.gd`, `combat.gd` | `hit_points`, `damage_roll`, `strain_maximum`, `strain_absorb` | **partially ported** — strain and damage exist; the trauma/shock table is not shown in the MUD surface |
| Combat sequence and actions | `cwn_combat_rules.gd`, `cwn_combat_actions.gd`, `cwn_attack_modifiers.gd` | — | **absent** |
| Injury and healing | `cwn_healing.gd`, `cwn_injury.gd` | — | **absent** |
| Foci and edges | `cwn_foci.gd` | — | **absent** |
| Skills catalogue | `cwn_catalogue.gd` | — | **absent** |
| Equipment, armour, weapons | `cwn_catalogue.gd`, `cwn_gear_mods.gd`, `cwn_encumbrance.gd` | — | **absent** |
| Encumbrance | `cwn_encumbrance.gd` | — | **absent** |
| Cyberware, complications, ops, demons | `cwn_cyberware*.gd`, `cwn_demons.gd` | — | **absent** |
| Alienation | `cwn_alienation.gd` | — | **absent** |
| Drugs / pharmaceuticals | `cwn_drugs.gd` | — | **absent** |
| Hacking, programs, cyberdecks | `cwn_hacking.gd`, `cwn_hacking_catalogue.gd`, `cwn_program_rules.gd`, `cwn_node_link.gd` | — | **absent** |
| Drones | `cwn_drones.gd` | — | **absent** |
| Vehicles | `cwn_vehicles.gd`, `cwn_srd_vehicles.gd` | — | **absent** |
| Chases and pursuit | `cwn_chases.gd` | — | **absent** |
| Contacts | `cwn_contacts.gd` | — | **absent** |
| Lifestyles, wages, bribes | `cwn_lifestyles.gd`, `cwn_wages.gd` | — | **absent** |
| Social costs | `cwn_social_costs.gd` | — | **absent** |
| Mission time / scenes / rounds | `cwn_mission_time.gd`, `session.gd` | — (time exists in `mud/tests/test_world_time.py` scope, not as CWN mission time) | **absent** |
| Advancement / progression | `cwn_progression.gd`, `swn_progression.gd` | — | **absent** |
| Party | `cwn_party.gd`, `party.gd` | — | **absent** |
| Psionics / psychic effort (SWN gap-fill) | `psionics.gd`, `psychic_effort.gd` | — | **absent** |
| Tags | `cwn_tags.gd`, `noopunk_tags.gd` | — | **absent** |
| Investigation adapter | `investigation_adapter.gd` | `solo_campaign.py`, `campaign/engine.py` (NoöPunk, not CWN) | **NoöPunk overlay, different layer** |

## 2. The gap in one sentence

**The MUD has the kernel and the sheet; it does not have the game.** Resolution, modifiers and character
creation are ported and tested. Combat as a sequence, injury and healing, equipment, cyberware, hacking,
drones, vehicles, chases, contacts, lifestyle and advancement — all present in Godot, all absent in
Evennia.

## 3. Explicit omissions

Recorded here so they are not discovered later as surprises:

1. **Trauma and shock.** Godot's `cwn_injury.gd` implements them; the MUD exposes `damage_roll` and
   strain but no trauma/shock procedure. A damage-only port is a different game.
2. **Combat action economy** (Main / Move / On Turn / Instant). Without it, "combat" in the MUD is an
   attack roll, not an encounter.
3. **Hacking.** The Godot side has a node-link model and a program catalogue; the MUD has nothing, so
   the #950 vertical slice cannot include its hacking beat yet.
4. **Equipment and encumbrance.** Character creation produces a sheet but the MUD has no catalogue to
   buy from and no load limits to enforce.
5. **Advancement.** No progression path in the MUD, so a campaign cannot reward anything.
6. **Verified SRD parity anywhere in the MUD.** The tests assert behaviour, not SRD text. Marking a row
   `ported` above means "a tested implementation exists", not "conforms to the SRD".

## 4. What this matrix does not claim

It is a **file-and-function inventory**. It does not assert that any Godot module is SRD-faithful, and it
does not propose an order of porting beyond the obvious dependency chain: trauma/shock and the action
economy before combat encounters, the catalogue before equipment, progression before rewards.
