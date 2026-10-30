# Godot MVP audit — what exists, what the vertical slice still needs (#749)

**Measured 2026-10-30** against `origin/main` @ `5758aeb`, Godot **4.7.2**, headless.

Work package A of #749 asks for an honest inventory before any claim of CWN coverage. This is
that inventory. It records what the repository already implements, what is absent, and what
the licence allows — it does not claim a mechanic works until a headless check exercises it.

---

## 1. How this was measured

```bash
godot --headless --path . --import                      # builds the global class cache
godot --headless --path . --script res://godot/tests/run_tests.gd
# → 138 checks, 0 failed
```

A fresh checkout **without** the import pass reports `29 checks, 2 failed`: `test_dialogue.gd`
and `test_scenario_data.gd` reference `NoopunkPsionics` by `class_name`, and the class cache
does not exist yet. That is an environment artifact, not a defect — but it is worth recording,
because a CI job that runs the suite without `--import` would look red for the wrong reason.

## 2. What already exists

| Module | Lines | What it does |
| --- | --- | --- |
| `godot/core/dice.gd` | 54 | Seeded, snapshot/restore-capable RNG (`NoopunkDice`). The determinism anchor for every roll. |
| `godot/core/rules_adapter.gd` | 161 | Reads `data/rules/wn_core.json`: attribute modifiers, difficulty values, `skill_check`, `save_target`, `attack_roll`. |
| `godot/core/game_state.gd` | 300 | Case state: scenario, evidence, journal, flags, objective, character, dialogue nodes, psionics, `save_to_file`/`load_from_file` (version 1). |
| `godot/core/investigation_adapter.gd` | 108 | Clue graph: scene gating, competency checks, passive core clues, withholding report. |
| `godot/core/psionics.gd` | 92 | Effort-shaped psionics with package/rank gating (original NoöPunk expression, not SWN's power catalogue). |
| `godot/core/psychic_effort.gd` | 79 | Effort spend/recovery arithmetic. |
| `godot/narrative/dialogue.gd` | 103 | Branching dialogue, choice effects, check branching. |
| `godot/scenes/level_builder.gd` | 394 | Tile/room/edge construction from scenario JSON; doors, walls, offsets. |
| `godot/scenes/player.gd` | 42 | Top-down grid movement for a single controllable PC. |
| `godot/scenarios/lakkahaltia/*` | — | The shipped case: dialogue, evidence, level, scenario. |
| `godot/tests/*` | — | 138 headless checks across 7 suites. |

## 3. Coverage matrix — CWN chapters against the vertical slice

`required-now` = needed for the Home → HQ → Mission slice. `later` = explicitly deferred.

| CWN area | Status in Godot | Where | Needed |
| --- | --- | --- | --- |
| Character creation, attributes, skills | **partial** — Romppainen's record not yet written; adapter resolves attributes/skills | `rules_adapter.gd`, `game_state.gd` | required-now |
| Task resolution (2d6 + skill vs difficulty) | **ported** | `rules_adapter.skill_check` | done |
| Saves | **ported** | `rules_adapter.save_target` | done |
| Attacks and armor class | **ported** (single roll) | `rules_adapter.attack_roll` | done |
| Initiative, rounds, turn order | **absent** | — | required-now |
| Grid movement, action economy | **absent** (free movement only) | `player.gd` | required-now |
| Cover, range bands | **absent** | — | required-now |
| HP, damage, Trauma/Shock, mortal injury | **absent** in Godot (Python side has it) | — | required-now (subset) |
| Gear, armor, inventory, reload | **absent** in Godot | — | required-now (subset) |
| Cyberware, System Strain | **absent** in Godot | — | later |
| Hacking: access, connectivity, programs, CPU, alarms | **absent** | — | required-now |
| NPC stat blocks, morale | **absent** | — | required-now (minimal) |
| Vehicles, chases, drones | **absent** | — | later |
| Advancement | **absent** in Godot | — | later |
| SWN psionic disciplines | **partial** — Effort-shaped packages only | `psionics.gd` | later |

Nothing above is claimed as complete on the strength of this table; each `required-now` row
gets a headless check in `godot/tests/` as it lands.

## 4. Licensing boundary (before any content is written)

- **CWN SRD** — `verified-public-domain` (CC0) in `data/sources/game_system_rights.json`.
  SRD **text and mechanics** may be used commercially with attribution; the commercial book,
  its art and its protected setting names may not.
- **SWN Revised** — `blocked-unverified`. No SRD located, so nothing may be reproduced. The
  existing psionics module is therefore an **original expression** (Effort-shaped procedure),
  not a transcription, and must stay that way.
- **Assets** — no third-party art enters the repository without a recorded licence. The MVP
  uses original or CC0 pixel art only; provenance goes in `docs/godot/ASSETS.md`.

## 5. What the vertical slice must add

Ordered by dependency, not by glamour:

1. **Combat kernel** (`godot/core/combat.gd`) — initiative order, per-turn action budget,
   grid movement, cover, attack resolution through `RulesAdapter`, HP application, enemy
   turn, encounter end conditions. Headless-testable without a renderer.
2. **Hacking kernel** (`godot/core/hacking.gd`) — node/edge network, access and connectivity
   prerequisites, program verbs, CPU costs, trace/alarm consequences. Reuses the same
   network model the tabletop layer would present.
3. **Scene flow** (`godot/core/scene_flow.gd`) — Home → HQ → Mission → Debrief with objective
   and clue state, gated transitions, and no unreachable core evidence.
4. **Save/load** covering combat, network and flow state, versioned alongside the existing
   case save.
5. **Romppainen record** — a published-creation CWN character with every undecided player
   choice marked as a choice.
6. **Scenes and UI** — pixel-art navigation, dialogue, character sheet, hacking view. This is
   the part that cannot be verified headlessly beyond scene loading; it needs a windowed
   playtest.

## 6. Honest gaps this audit adds to the issue

- The existing slice is a **case investigation**, not a tactical game: there is no turn
  system, no HP, no cover and no enemy AI anywhere in `godot/`.
- The Python rules layer (`src/rules/`) implements far more CWN than the Godot layer; the
  Godot side re-derives a subset from `wn_core.json`. Two implementations of one rule set is
  a standing drift risk that this MVP does not solve — it only avoids making it worse.
- The Godot layer has **no** representation of gear, inventory or encumbrance, so the
  "equipment" and "reload" requirements of #749 B are currently unimplemented, not partial.
