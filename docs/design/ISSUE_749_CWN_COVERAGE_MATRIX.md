# Issue #749 — CWN/SWN coverage audit, reuse decision and MVP breakdown

> **Status: audit and plan. No mechanic is authored, changed or approved by this file.** It
> measures what exists on `main`, states what the Godot MVP may reuse, and splits the parent
> issue into reviewable increments. Source of truth for rules remains
> [`rulebook/WITHOUT_NUMBER_BASELINE.md`](../../rulebook/WITHOUT_NUMBER_BASELINE.md); the agent
> contract is `AGENTS.md`.

**Measured on:** `origin/main` = `1549803` (30 Oct 2026). **Engine:** Godot `4.7.2.stable`
(`ed1daf0bf`), the version pinned in `project.godot` and by CI.

**Baseline, captured before any change** (these are the numbers a later session must compare
against):

| suite | command | result |
| --- | --- | --- |
| Python, repository | `python3 -m unittest discover -s tests -p "test_*.py"` | **1452 tests, OK** |
| Godot, slice suites | `godot --headless --path . --script res://godot/tests/run_tests.gd` | **138 checks, 0 failed** |
| Godot, rules suites | `godot --headless --path . --script res://tools/run_godot_tests.gd` | **20 tests, 264 checks, 0 failures** |
| Godot, CWN kernel | `--script tests/godot/test_cwn_rules.gd` / `test_cwn_progression.gd` | PASS / PASS |

---

## 1. The measured gap this issue has to close

The rules are **not** missing. The **Godot parity** is.

| side | what exists | size |
| --- | --- | --- |
| Python, `src/rules/` | 20 `cwn_*` modules, 4 `swn_*` modules, the `wn_core` kernel, each with its own `tests/test_*.py` | ~4,900 lines of CWN/SWN law, ~600 tests |
| Godot, `src/godot/` + `godot/core/` | attribute modifier, 2d6 skill check, opposed check, four saves, d20 attack total, **hacking reachability pre-check only**, psionic Effort pool, investigation adapter, dialogue, save/load | ~1,500 lines of GDScript, 284 checks |

`src/godot/cwn_rules.gd:71` is the honest summary of the hacking gap:
`check_hacking_reach()` returns whether a jack-in is *permitted*. It does not spend Access, does not
roll against Security, does not run a Verb, and does not alert the network. Issue #749 requires the
opposite: *"hacking is navigable in a node-link screen and its actions use actual CWN hacking rules,
not only the existing eligibility precheck."*

Everything else is a smaller version of the same fact: the Python side is a rules library, the
Godot side is a vertical slice that calls four functions of it.

---

## 2. Chapter-by-chapter coverage matrix

`AS-IS (py)` = implemented in Python with source-cited procedure. `GDScript` = usable by the
engine today. **Now** = required by this MVP's first playable path; **Later** = part of the
eventual full-CWN goal but not required to reach the three locations.

| # | CWN procedure (SRD slug) | Python | Tests | GDScript today | MVP |
| --- | --- | --- | --- | --- | --- |
| 1 | Attributes, modifiers, generation (`character-creation/attributes`) | `cwn_character.py` (156) | 19 | modifier ✓ (`cwn_rules.gd:9`); generation ✗ | **Now** |
| 2 | Skills, 2d6 check, untrained −1, circumstances ±2, aid +1 | `wn_core.py` (294) | 19 + 32 contract | ✓ (`cwn_rules.gd:21`, `godot/core/rules_adapter.gd`) | **Now** |
| 3 | Saves, four kinds, nat 1/20 (`saving-throws`) | `wn_core.py` | ✓ | ✓ (`cwn_rules.gd:41,57`) | **Now** |
| 4 | Backgrounds, contacts (`character-creation/backgrounds`) | `cwn_backgrounds.py` (241) | 25 | ✗ | Now (creation) |
| 5 | Edges and Foci | `cwn_edges_foci.py` (148), `cwn_foci.py` (164) | 18 + 15 | ✗ | Later |
| 6 | Attacks vs Melee/Ranged AC (`attacks-in-combat`) | `cwn_combat.py` (80), `cwn_attack_modifiers.py` (81) | 6 + 10 | total vs AC ✓ (`cwn_rules.gd:65`); modifiers ✗ | **Now** |
| 7 | Combat action economy: Main/Move, Snap, Swarm, Charge, Total Defense | `cwn_combat_actions.py` (174) | 16 | ✗ | **Now** |
| 8 | Initiative, rounds, cover, suppression (`combat/`) | — (not a module; `cwn_combat.py` delegates AC to the caller) | — | ✗ | **Now** |
| 9 | Damage, Shock, Trauma die/rating (`damage-trauma-shock`) | `cwn_core.py` (456) | 47 | ✗ | **Now** |
| 10 | Major Injury, mortal wounds, stabilization (`major-injuries`) | `cwn_major_injury.py` (182), `cwn_injury_procedure.py` (106) | 14 + 15 | ✗ | **Now** |
| 11 | Healing, first aid, Frail, rest | `cwn_healing.py` (191) | 28 | partial (`cwn_progression.gd` natural healing) | Now |
| 12 | System Strain | `cwn_strain.py` (133) | 18 | partial (`cwn_progression.gd`) | **Now** (cyberware) |
| 13 | Encumbrance, Stowed/Readied | `cwn_encumbrance.py` (130) | 13 | ✗ | Now |
| 14 | Weapons and armour tables | `cwn_equipment.py` (155) + `data/rules/cwn_equipment.json` (35 weapons, 15 armour) | 11 | ✗ (data exists, no reader) | **Now** |
| 15 | Mods, crafting, maintenance | `cwn_gear_mods.py` (466) + `data/rules/cwn_gear_mods.json` | 35 | ✗ | Later |
| 16 | Vehicles, vehicle combat, chases | `cwn_vehicles.py` (651) + `data/rules/cwn_vehicles.json` | 41 | ✗ | Later |
| 17 | Cyberware, installation, Strain cost | `cwn_strain.py`, `cwn_equipment.json` | ✓ | ✗ | **Now** |
| 18 | Hacking: Access pool, Security 7–10/12, connection penalties, Alert clock | `cwn_hacking.py` (213) | 16 | **pre-check only** ✗ | **Now** |
| 19 | Programs / Verbs / deck CPU (catalogue content) | deliberately not shipped — the module takes a Verb modifier as an argument | — | ✗ | **Now** as scenario data |
| 20 | Drones | `cwn_drones.py` (198) | 18 | ✗ | Later |
| 21 | NPC stat lines, morale, reaction | not a module (baseline §6: "the family's stat-line convention") | — | ✗ | **Now** (one enemy) |
| 22 | Advancement: XP, skill points, HP, attack bonus | `cwn_advancement.py` (215) | 27 | partial (`cwn_progression.gd`) | Later |
| 23 | Psionics: Effort pool, techniques, package+rank gate (`SWN Psionics`) | `swn_psionics.py` (113), `psionics.py`, `swn_progression.py` (98) | 5 + 4 | ✓ pool + gate (`godot/core/psionics.gd`, `psychic_effort.gd`) | Now (rules-test fixture) |
| 24 | Starships, sector travel, faction turns (SWN) | `swn_starships.py`, `swn_sector.py`, `swn_faction_turn.py`, `swn_faction_operations.py` | 4 + 5 | ✗ | Later |
| 25 | Investigation layer (NoöPunk native, #704) | `investigation.py`, `investigation_evidence.py` | 17 + 11 + 21 | ✓ (`godot/core/investigation_adapter.gd`) | **Now** |

**What this table refuses to claim.** It is not "CWN is implemented." Rows 8, 19 and 21 have no
Python module at all — they are either delegated to the caller by design (`cwn_combat.py` says so in
its docstring) or are catalogue/table content the author has not ruled on. The GDScript column is the
MVP's real to-do list: **eleven "Now" rows have no GDScript implementation**, and rows 7, 8, 9, 10 and
18 are the ones that make the difference between "a game that shows a roll" and "a game that plays
CWN".

---

## 3. Licensing and distribution boundaries

| source | terms | what the MVP may do |
| --- | --- | --- |
| CWN SRD | **CC0** (`docs/licenses/ISSUE_569_CWN_SWN_LICENCE_AUDIT.md`) | procedures **and** text. The repo still writes its own prose and cites the slug. |
| WWN SRD | **CC0** | same; not used by this MVP. |
| SWN Revised | **no verified SRD licence** | mechanics re-expressed independently; **no** text, power names or tables. PSI is implemented as an Effort-shaped pool with NoöPunk-authored technique names (`data/rules/psionics_techniques.json`). |
| AWN | no verified CC0 located | not used by this MVP. |
| GUMSHOE SRD | CC BY 3.0, prescribed attribution sentence | method only; the sentence must appear if any of its text is reproduced (it is not). |
| art / sprites / tiles | — | original or CC0 only, with provenance per asset. **No** extracted game art from Deadeye Deepfake Simulacrum or DROP: System Breach — they are named as *aesthetic* references only. |

Consequences enforced by this MVP: no source-book prose, tables or PDF is vendored; every
`data/rules/*.json` row that comes from a source carries its slug in the file header; the game's own
credits name the Without Number family and state that NoöPunk is unofficial and unaffiliated. The
licence of the *project's own* output is still an open author decision (`LICENSE`/`NOTICE` do not
exist and agents may not create them — queue row D10).

---

## 4. Reuse decision for the Godot slice

Reuse, do not fork:

| asset | decision |
| --- | --- |
| `godot/core/rules_adapter.gd`, `src/godot/wn_rules.gd`, `cwn_rules.gd` | **extend.** One kernel; new procedures are added as functions or sibling modules that call it, never as a second resolution system. |
| `godot/core/game_state.gd` (300) | **extend** with a second scenario namespace. Keep the existing save format readable. |
| `godot/narrative/dialogue.gd` (103) | **reuse as-is** for Home and HQ conversations; the data shape already handles conditions on flags and clues. |
| `godot/scenes/level_builder.gd` (394), `godot/scenes/player.gd` (42) | **reuse** for the top-down rooms; they build from primitives, so new rooms need data, not new art. |
| `scenes/lakkahaltia/*` (ward, 572) | **do not touch.** It is #631's playable slice and its headless playthrough is a CI gate. The MVP adds a separate scenario directory. |
| `src/godot/core_rules.gd` (retired 1d10) | **leave retired.** Never call it from new code. |
| `src/rules/*.py` | **reference of record.** GDScript must not invent a number that Python does not already hold; where a table is needed at runtime it moves to `data/rules/*.json` and both sides read it (the `wn_core.json` pattern). |

**Scenario isolation:** the new content lives under `data/scenarios/romppainen/` (home, HQ, mission,
network) and `scenes/romppainen/`. Nothing under `data/scenarios/lakkahaltia/` changes.

---

## 5. Increments (each independently reviewable, in order)

| PR | scope | files | closes which acceptance criterion |
| --- | --- | --- | --- |
| **1** (this file) | audit, matrix, reuse decision, breakdown | `docs/design/ISSUE_749_CWN_COVERAGE_MATRIX.md` | work package A |
| **2** | vanilla CWN hacking as engine-side rules: Access pool, Security ladder and situation modifiers, flat connection penalties, cyberware/drone difficulty, Alert clock, and a Verb/Subject catalogue as **scenario data** | `data/rules/cwn_hacking.json`, `godot/core/cwn_hacking.gd`, `tests/godot/test_cwn_hacking.gd`, `tests/test_cwn_hacking_contract.py` | "actions use actual CWN hacking rules, not only the existing eligibility precheck" |
| **3** | combat kernel: initiative, Main/Move budget with Snap/Swarm/Charge/Total Defense, attack modifiers, cover, Shock/Trauma, Major Injury, Strain | `data/rules/cwn_combat.json`, `godot/core/cwn_combat.gd`, `godot/core/cwn_injury.gd`, `tests/godot/test_cwn_combat.gd`, `test_cwn_injury.gd` | "turn-based tactical play grounded in the published rules" |
| **4** | node-link hacking screen driving the kernel (graph layout, security state, Access spend, alert consequences, return to the physical scene) | `godot/ui/hacking_screen.gd`, `data/scenarios/romppainen/network.json` | "hacking is navigable in a node-link screen" |
| **5** | turn-based tactical encounter on the existing level builder (solo PC, enemy turn, cover, objective) | `godot/ui/tactical_screen.gd`, `data/scenarios/romppainen/mission.json` | "solo-PC tactical combat" |
| **6** | the playable spine: Home → UNSA HQ → mission → debrief, Romppainen's CWN sheet, save/load of all of it | `scenes/romppainen/*.tscn`, `src/godot/romppainen_case.gd`, `data/scenarios/romppainen/{home,hq,mission,character}.json`, `tests/godot/test_romppainen_slice.gd` | the four remaining acceptance criteria |

Rules of the sequence:

- **Python first.** A procedure enters GDScript only after it exists in `src/rules/` (or is moved to
  `data/rules/*.json`), so the two runtimes cannot disagree about a number.
- **No prose tests** (#271). Tests cover executable behaviour: seeded resolution, Access arithmetic,
  alert transitions, save round-trips, scene transitions, endings.
- **No new mechanics.** Where CWN has no equivalent, the MVP uses ordinary checks and referee
  adjudication (baseline §1) rather than inventing a subsystem.
- **Every PR re-runs the four baselines in §0** and reports the counts it saw.

---

## 6. What this document does not claim

- It does not claim CWN coverage. Eleven "Now" rows have no engine implementation; three CWN
  procedures have no Python module at all.
- It does not decide any rule. Row 19 (the Verb/Subject catalogue) is authored **scenario data**
  marked provisional, not a ruling on CWN's program list.
- It does not authorize a Godot rewrite of the Lakkahaltia slice, a second character model, or a new
  resolution system.
- It does not settle the project licence (D10) or the distribution model (D14/D16).
