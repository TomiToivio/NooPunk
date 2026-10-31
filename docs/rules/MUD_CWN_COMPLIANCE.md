# MUD CWN compliance matrix (#950)

**Target:** Python core in `mud/nopunk_mud/cwn_core.py`, usable by Evennia commands, quests and
encounters. **Rule source:** the CWN SRD at <https://cwn.quadrifons.com/>; numbers are read from
`data/rules/without_number.json`. Coverage is claimed only where a test exercises the path.

| CWN system | SRD section | Godot status | Python target | Coverage | Test |
|---|---|---|---|---|---|
| Attributes 3–18 and −2…+2 modifiers | rules-of-the-game/character-creation | implemented | `attribute_modifier` | implemented | `test_cwn_core.py::TestAttributes` |
| 3d6 generation / published array | character-creation/attributes | implemented | `roll_attributes`, `assign_array` | implemented | same |
| Hit points (d6 + CON, max first die) | character-creation/attributes | implemented | `hit_points` | implemented | `TestDerived` |
| Saving throws (d20 ≥ 16 − level − best) | rules-of-the-game/saving-throws | implemented | `save_target` | implemented | `TestDerived` |
| Skill checks (2d6 + rank + attr vs 6/8/10/12/14) | rules-of-the-game/skill-checks | implemented | `skill_check` | implemented | `TestChecks` |
| Attacks (d20 + bonus + attr + skill vs AC) | rules-of-the-game/combat | implemented | `attack_roll` | implemented | `TestChecks` |
| Damage and attribute modifier | combat/damage | implemented | `damage` | implemented | `TestDamageAndStrain` |
| Trauma die / rating bonus damage | combat/trauma | implemented | `damage(trauma_*)` | implemented | same |
| System Strain capacity and absorption | injury-healing-system-strain/system-strain | implemented | `strain_max`, `strain_absorb` | implemented | same |
| Skills, backgrounds, contacts, edges, foci, focus gear | character-creation/* | implemented | — | **missing** | — |
| Initiative, action economy, shock, maneuvers | combat/* | implemented | — | **missing** | — |
| Injuries, stabilisation, healing | injury-healing-system-strain/* | implemented | — | **missing** | — |
| Encumbrance, weapons, armour, gear mods, crafting, wages | gear-vehicles-cyberware/* | implemented | — | **missing** | — |
| Cyberware systems, complications, maintenance, alienation | cyberware/* | implemented | — | **missing** | — |
| Hacking: cyberdecks, access, verbs/subjects, programs, demons | hacking/* | implemented | — | **missing** | — |
| Vehicles, drones, pharmaceuticals | gear-vehicles-cyberware/* | partial | — | **missing** | — |
| Advancement (XP, level, attack bonus, skill points) | character-advancement | implemented | — | **missing** | — |
| Psionics | SWN Revised (not CWN) | partial | — | out of CWN scope | — |

## Notes and boundaries

- "Godot status" is the existing GDScript kernel; the Python port must reproduce behaviour, not
  import GDScript or the Godot runtime.
- The linked hosted SRD omits Antagonists/NPCs and some optional rules. This matrix therefore covers
  the linked SRD, not the full published CWN book; omitted sections are not marked complete.
- NoöPunk overlays (Noösphere, Psyche, factions, reputation, GUMSHOE investigation) are mods on this
  core and must not change these numbers.
- The immediate solo-campaign path needs: skills/backgrounds, initiative and action economy, shock,
  injuries/healing, encumbrance, weapons/armour, and hacking. Those are the next porting slices.
