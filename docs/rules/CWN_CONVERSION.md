# CWN conversion: what is ported, and what is not

**Status: implementation record.** The decision is the author's
([`rulebook/WITHOUT_NUMBER_BASELINE.md`](../../rulebook/WITHOUT_NUMBER_BASELINE.md), 2026-10-26): *"use
CWN/SWN/AWN/WWN system for everything … we will modify later."* This page records how far the code has
actually got, so that "converted" is a claim someone can check instead of a description.

The machine-readable contract is [`data/rules/wn_core.json`](../../data/rules/wn_core.json). The Python
kernel is [`src/rules/wn_core.py`](../../src/rules/wn_core.py); the Godot runtime reads the same file
through [`godot/core/rules_adapter.gd`](../../godot/core/rules_adapter.gd). Psionics has its own pair:
`data/rules/psionics_techniques.json` with `src/rules/psionics.py` and `godot/core/psionics.gd`.

## 1. Source hierarchy

| Source | Role | What NoöPunk takes |
| --- | --- | --- |
| **Cities Without Number** (2023) | primary chassis | attributes, skills, checks, saves, combat, damage/Shock/Trauma, injury, System Strain, cyberware, hacking, encumbrance, advancement, NPC stat lines |
| **Stars Without Number Revised** (2017) | co-primary | the *shape* of psionics: a committed pool, core capability before techniques, one technique per skill level; space and faction turns when those modules are in play |
| **Worlds Without Number** (2021) | situational | the Effort pool pattern (CC0), exploration and project procedures |
| **Ashes Without Number** (2025) | situational | crisis-zone survival, supplies, hazards, settlements |

CWN settles overlapping general rules. A specialist source governs its own procedure and nothing else.
No second armour, injury, advancement or action-economy system is added.

## 2. Ported, with where to look

| Subsystem | Contract key | Python | Godot | Tests |
| --- | --- | --- | --- | --- |
| Attributes and modifier bands | `stats` | `attribute_modifier()` | `attribute_modifier()` | `test_wn_core_contract.py`, `test_cwn_procedures.gd` |
| Skill list and untrained states | `skills` | `SKILLS`, `PSIONIC_SKILLS`, `UNSKILLED_PENALTY`, `UNSKILLED_ATTACK_PENALTY` | read from the contract | `test_cwn_procedures.py` |
| Skill checks, opposed checks, aid | `skill_check`, `modifiers` | `skill_check()`, `opposed_check()` | `skill_check()` | `test_wn_core_contract.py` |
| Saves | `saves` | `save_target()`, `roll_save()` | `save_target()` | `test_wn_core_contract.py` |
| Attack rolls | `combat.attack` | `attack_roll()` | `attack_roll()` | `test_cwn_procedures.py`, `test_cwn_procedures.gd` |
| Damage, Shock, Trauma, Damage Soak | `combat.damage`, `.shock`, `.trauma` | `resolve_attack()`, `DamageSoak()` | `resolve_damage()` | both |
| Mortal injury, stabilization, Frailty | `combat.mortal_injury` | `MortalWound`, `stabilize_difficulty()` | `stabilize_difficulty()`, `mortal_rounds()` | both |
| Major Injuries | `combat.major_injury` | `major_injury()`, `MAJOR_INJURIES` | via the contract table | `test_cwn_procedures.py` |
| Action economy and movement | `combat.actions`, `combat.initiative` | constants + movement | constants | contract test |
| System Strain | `strain` | `SystemStrain` | `strain_*()` helpers | both |
| First aid, natural healing, Frailty removal | `healing` | `first_aid_healing()`, `natural_healing()`, `frail_field_removal_difficulty()` | `first_aid_healing()`, `natural_healing()` | both |
| Cyberware installation, maintenance, alienation | `cyberware` | `cyberware_installation()`, `installation_outcome()`, `cyberware_maintenance_cost()`, `alienation_exceeded()` | *(tabletop-facing; not needed by the slice)* | `test_cwn_procedures.py` |
| Hacking: Access, security, connection, cyberware/drone difficulty, alerts | `hacking` | `access_pool()`, `hacking_difficulty()`, `hacking_check()`, `cyber_hack_difficulty()`, `AlertCounter` | the same four functions | both |
| Encumbrance | `encumbrance` | `stowed_capacity()`, `readied_capacity()`, `overload_stage()`, `movement_for_stage()` | *(tabletop-facing)* | `test_cwn_procedures.py` |
| Advancement: XP, skill points, attack bonus, HP | `advancement` | `level_for_xp()`, `skill_point_cost()`, `minimum_level_for_skill()`, `attack_bonus()`, `hit_points_gain()` | `level_for_xp()`, `attack_bonus()`, `skill_point_cost()`, `minimum_level_for_skill()` | both |
| NPC stat-line convention | `npc` | documented; level data carries the stat lines | level data + `attack_roll()` | `test_scenario_data.gd` |
| Psionics: Effort, commitment, torching, training gate | `psionics` | `psionics.py` | `psionics.gd` | both |
| Psionic technique catalogue | `data/rules/psionics_techniques.json` | `load_catalogue()` | `technique()`, `core_for()` | both |

Two corrections are worth naming because they were found by reading the source rather than by
preferring a number:

1. **Saving throws** are `16 − level − the higher of the pair`, not a flat 15. At level 1 that is 15,
   which is why the advancement chapter's "first level characters have 15" is consistent with the
   formula and not a second rule.
2. **Shock is not clamped to the situational bound.** A wireless link (−2) plus a VR crown (−1) is −3
   on the check; folding those into "circumstances" would silently swallow the third point. The kernel
   therefore carries flat modifiers in `Check.misc`, separate from `situational`.

## 3. Not ported, and why

| Gap | Why it is still open | Next step |
| --- | --- | --- |
| Equipment catalogue as data (weapons, armour, gear, drugs, drones, vehicles) | It is content, not procedure. Prices, encumbrance and stat lines are the author's to fix, and a wrong catalogue is worse than none. | One data file per family (`data/rules/cwn_weapons.json`, …) behind the existing `equipment_catalog_index.py` |
| Edges and Foci | Their *text and benefits* are authored content. The mechanics (skill points, HP, attack bonus) are ported. | Author the list; the kernel already models their effects as inputs |
| Drones and vehicle combat | Needs the equipment catalogue first; vehicle combat also needs its own reading. | After the catalogue |
| Faction turns (SWN) | A whole subsystem the current scenarios do not need. | When a scenario uses factions |
| AWN survival (supplies, exposure, hazards, enclaves) | No scenario is set in a crisis zone yet. | When the first crisis-zone scenario is written |
| WWN projects and exploration | Same: no scenario uses them yet. | When a scenario uses an expedition clock |
| Magic options (WWN) | Canon treats magic as setting PSI/psychotronics, not as a spell list. | Deliberately deferred; not an omission |

## 4. The first scenario

`godot/scenarios/lakkahaltia/` is the playable slice, and it now resolves against the CWN contract rather
than scenario-local numbers:

- **the sheet** is a CWN operator stat line: level 3, six attributes, CWN skills (`Know`, `Notice`,
  `Talk`, `Administer`, `Heal`, `Program`) plus `Telepathy`, hit points, attack bonus, both Armour
  Classes with Damage Soak, four saves, System Strain with permanent cyberware strain, two weapons, and
  a psionics block;
- **the dialogue checks** use canonical skills and attributes only (`INT/Know`, `CHA/Talk`, `WIS/Notice`,
  `INT/Administer`, `INT/Program`, `WIS/Telepathy`);
- **hacking** is a real path: `INT/Program` against a branch-office network (difficulty 9) reads the
  ward's access log;
- **psionics** is a real path: the patient scene offers `Surface Read` (Telepathy core). The training
  gate runs *before* the dice — an untaught character takes the failure branch and spends nothing, and a
  taught one records the reading as an *impression*, never as a finding;
- **the NPCs** carry CWN stat lines (hit dice, attack bonus, both ACs, hit points, Trauma Target,
  weapon), which `RulesAdapter.attack_roll()` + `resolve_damage()` resolve directly.

The data test `godot/tests/test_scenario_data.gd` enforces the contract: every check uses a canonical
attribute and skill, the sheet can actually make every check it is offered, every NPC has a complete
stat line, and the sheet's Effort maximum equals the adopted formula. That test exists because a renamed
skill silently resolves as *untrained* — the character rolls −1 and nobody learns why.

## 5. Licence boundary

| Source | Terms | What was done |
| --- | --- | --- |
| CWN SRD | CC0 dedication | Mechanics implemented; prose written fresh, no SRD sentence copied |
| WWN SRD | CC0 dedication | The Effort pool pattern adopted |
| SWN Revised | **no verified SRD licence** | Mechanics re-expressed independently; **no text, power name or table reproduced**. The technique catalogue is original NoöPunk content, marked `provisional` |
| AWN | **no verified CC0 located** | Design reference only; nothing imported |

The rights matrix is [`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`](../licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md).
Psionic technique names and effect text were authored for this repository; where a technique's *numbers*
resemble another game's, that is unprotected mechanics, not copied expression.

## 6. Verification

```bash
python3 -m pytest tests/test_cwn_procedures.py tests/test_swn_psionics.py tests/test_wn_core_contract.py
godot --headless --path . --import
godot --headless --path . --script res://godot/tests/run_tests.gd
godot --headless --path . res://godot/tests/playthrough.tscn --quit-after 300
godot --headless --path . --script res://godot/tests/integration_playthrough.gd
```

— Ai (愛)
