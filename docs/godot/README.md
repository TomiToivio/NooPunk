# The Godot 4 slice — *Etsivä Romppainen ja Lakkahaltian Salaisuus* (#631)

A ten-minute playable case: one hospital, three conversations, six pieces of evidence, one sealed file,
and two endings that are both defensible and neither of which says what the phenomenon was.

**Status:** first vertical slice. It runs, it is tested headlessly, and it is deliberately small. Rules,
combat, hacking, PSI, BCI and factions are seams, not features.

## Engine and platform

| | |
| --- | --- |
| Engine | **Godot 4.7.2-stable** (pinned in `project.godot` and in the CI workflow) |
| Tested on | Linux x86_64 (this repository's CI), headless and windowed |
| Renderer | `gl_compatibility` (the project's existing setting, kept) |
| Language | GDScript only. No addons, no RPG in a Box, no export step |
| Network | none. The game never contacts an LLM or a service; it runs entirely offline |

## Run it

```bash
# from a clean checkout, with Godot 4.7.2 on PATH (binary name may be `godot` or Godot_v4.7.2-stable_linux.x86_64)
godot --path . --import          # first run only: builds .godot/ (git-ignored)
godot --path .                   # launches scenes/main.tscn, the title screen
```

Press **Begin the case**. You spawn in the hospital lobby.

| control | action |
| --- | --- |
| `W` `A` `S` `D` | walk |
| mouse | look |
| `E` | talk to an NPC / inspect a prop |
| `J` | hide or show the evidence-and-journal panel |
| `F5` | save the case (`user://save_lakkahaltia.json`) |
| `F6` | close the case — offers the endings the evidence supports |
| `Esc` | release the mouse |

A full run: inspect the reception terminal and the records cabinet, talk to Nurse Aho and to Patient
Korhonen (consent first, then the account, then the place), then `F6`. Talking to Dr. Laine first is the
intended opening; the cabinet stays locked until either the roster or his hint is in hand.

## Test it

```bash
# unit suites: rules adapter, game state, dialogue, scenario-data integrity
godot --headless --path . --script res://godot/tests/run_tests.gd

# playthrough of the assembled level: builds, walks, talks, closes the case
godot --headless --path . res://godot/tests/playthrough.tscn
```

Observed with Godot 4.7.2 on Linux: **68 unit checks, 0 failed** and **15 playthrough checks, 0 failed**.
CI (`.github/workflows/godot.yml`) runs both on every change under `godot/`.

The playthrough runs as a scene, not through `--script`, on purpose: a `--script` main loop is not a
normal game start and does not register the project's autoloads, so a playthrough there would be testing
a different program.

## How it is put together

```
project.godot                     engine settings, input map, the one autoload
scenes/main.tscn                  the pre-existing title scaffold; godot/ui/main_menu.gd adds the entry points
godot/
  core/dice.gd                    seeded RandomNumberGenerator wrapper: every roll is replayable
  core/rules_adapter.gd           the ONLY place a mechanic is read: reads data/rules/wn_core.json
  core/game_state.gd              autoload GameState: character, evidence, journal, flags, endings, save/load
  narrative/dialogue.gd           dialogue-graph runner: effects, checks, branches
  scenes/hospital.tscn            the level: one Node3D, everything else is built from data
  scenes/level_builder.gd         builds rooms, props, NPCs, player and HUD from level_hospital.json
  scenes/player.gd                walk, look, gravity
  ui/hud.gd                       objective, evidence, journal, the roll readout, the ending panel
  scenarios/lakkahaltia/*.json    scenario, dialogue, evidence, level layout — all authorable data
  tests/                          unit suites + the headless playthrough
```

**Data, not code, is where the case lives.** A new conversation, a new clue or a new room is a JSON edit:
`scenario.json` (sheet, objectives, endings), `dialogue.json` (nodes, choices, effects, checks),
`evidence.json` (provenance, what it substantiates, what it falsely suggests), `level_hospital.json`
(rooms, props, NPCs, spawn). `godot/tests/test_scenario_data.gd` fails the build if a node reference, an
evidence id, an NPC entry point or an ending gate no longer resolves — a data contract, not a prose gate.

**One state, one save.** `GameState` is an autoload because two scenes disagreeing about what happened is
the classic save-file bug. The save is versioned (`SAVE_VERSION`), carries the RNG seed, and refuses a
save from another case or a future version instead of half-applying it.

## Rules: an adapter, and the one open question it refuses to hide

`godot/core/rules_adapter.gd` reads `data/rules/wn_core.json` — the repository's approved Without Number
baseline (`docs/rules/WN_BASE_SYSTEM.md`, `src/rules/wn_core.py`) — and implements nothing of its own:

* attributes are the six canon ones on 3–18, modifiers from the kernel's band table;
* a skill check is `2d6 + attribute modifier + skill level + situational + aid` against 6/8/10/12/14;
* saves are `d20 >= 16 − level − the higher of the pair`;
* untrained is passed explicitly as `-1` (the kernel's `untrained_modifier`), never guessed.

**The open question is #564's die pool.** Its history contains a 3d6 core-check proposal that the author
has not adopted or rejected, and the issue for this slice forbids silently substituting one for the
other. So the adapter takes an optional `approved_die_pool` and *reports* what it used
(`2d6 (kernel)` or `3d6 (approved override)`); the check result carries the label, the UI shows it, and
`test_rules_adapter.gd` pins both paths. A future ruling changes one argument, not the code.

**What this slice deliberately does not implement:** combat, hacking, BCI, PSI procedures, factions,
advancement. They are later milestones (below), and each would have to come through the same adapter.

## Save format

`user://save_lakkahaltia.json` — `save_version`, `scenario_id`, `run_seed`, `character`, `evidence`,
`journal`, `flags`, `current_objective`, `ending`. JSON on purpose: a save is inspectable, and a reviewer
can read a bug report without a binary tool.

## Known limitations

* **Placeholder art.** Rooms, props and people are primitives with flat colours. No third-party asset is
  committed; see [`ASSET_MANIFEST.md`](ASSET_MANIFEST.md).
* **Movement is flat.** No stairs, no crouch, no jump; the level is one storey by design.
* **Three NPCs, one case.** The ward *hub* — recurring cast, procedure, department politics — is designed
  (`docs/design/ISSUE_626_NORTHERN_NOOSPHERE.md` §5) but not built.
* **The place itself is off-screen.** Act 4's forest station is written, not modelled; the slice ends at
  the case's filing decision.
* **No combat.** If it is ever needed here, it comes from the rules kernel, not from a scene script.
* **One language.** English UI text; the case's Finnish names and place-names are kept as names.
* **Accessibility:** no remapping UI, no subtitles for a non-existent voice track, mouse-look only.

## Asset policy

Nothing third-party ships in this slice. The intended CC0 sources for the next milestone, the licence
checklist, and the rule that purchased packs never enter the public repository are in
[`ASSET_MANIFEST.md`](ASSET_MANIFEST.md).

## Next milestones

1. **Richer detective RPG** — the ward hub with recurring NPCs, more cases, cybernetics and hacking
   through the adapter, PSI as a procedure rather than a flag.
2. **Tactical missions** — an X-COM-shaped layer, kept behind the same rules kernel.
3. **Grand strategy** — the faction layer (`strategy_game/`) and this RPG sharing one world, not one code
   base.

## Where this sits in the repository

The two-games rule (`AGENTS.md` §0) still holds: `strategy_game/` is the crossover game, and this is the
legacy RPG's Godot front end — `rulebook/`, `RULEBOOK.md` and the tabletop material remain canonical, the
Godot code is a port, and no rule is invented here. The author's 2026-10-26 direction (#631) is what
authorises building the front end now rather than after the tabletop rulebook is finished; the adapter is
how that stays honest.
