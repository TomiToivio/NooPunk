# Two Stress engines on `main` — reconciliation record (#928)

> **Status: reconciliation record, no code change.** Issue
> [#928](https://github.com/TomiToivio/NooPunk/issues/928) was implemented **twice**, within minutes, by
> two sessions: PR [#930](https://github.com/TomiToivio/NooPunk/pull/930) (overlay) merged first, PR
> [#929](https://github.com/TomiToivio/NooPunk/pull/929) (core) merged second. Both are on `main` as of
> `1010ab8`. This file records exactly what the two do differently, why the duplication is architecturally
> blocked from being resolved by either session alone, and what the options cost. The ruling is row
> **D58** in [`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md).

## What landed

| | `godot/core/awn_stress.gd` (#929) | `mods/noopunk/stress.gd` (#930) |
| --- | --- | --- |
| Layer | **core**, `class_name AwnStress`, wired into the `GameState` autoload | **overlay** in `mods/noopunk/` |
| Size | 186 lines | 787 lines + a 538-line contract |
| Values | `const TRIGGERS` / `const NOOPUNK_TRIGGERS` in the script | `data/rules/awn_stress.json`, read at runtime |
| Tests | `godot/tests/test_awn_stress_928.gd`, 18 checks | `test_noopunk_stress.gd` + `test_noopunk_stress_screen.gd`, 148 checks |
| UI | none — its own docs list "a visible HUD/GM scene end panel" as a gap | `scenes/stress_screen.tscn` + `godot/ui/stress_screen.gd`, reachable from `scenes/main.tscn` |
| Persistence | `snapshot()` / `restore()` into the `GameState` save | its own versioned file, `user://awn_stress_state.json`, beside the core save |
| Live-game path | **yes** — `GameState.queue_stress_event()` / `resolve_scene_stress()` | no; the table drives it through the screen |
| Docs | `docs/AWN_STRESS_928.md` | `docs/design/AWN_STRESS_MODULE_928.md` |

Both agree on the spine: the ceiling is WIS and is **exceeded**; the first check is −2 and each further
one while still over is another −2; a successful check removes no Stress; a Breakdown suppresses further
Stress and ends at or below WIS; Hardening clears Stress to zero, resists one further point per scene,
grants one irreversible scar, and stacks.

## Where they differ

| Subject | Core `AwnStress` | Overlay `stress.gd` | Note |
| --- | --- | --- | --- |
| Who resolves the save | takes the `d20` and compares `roll + penalty >= target`, computing the CWN target itself from the character sheet | takes a boolean, reports the penalty, lets the caller use the core | the overlay respects `tests/test_foundational_lock_897.py`; the core module is allowed to, because it is core |
| Participation | not modelled — a GM queues what they queue | `participated: false` yields no Stress | #928 asks for the distinction explicitly |
| First kill | `extra` integer supplied by the caller | the caller's `1d6` result, keyed to the modifier | equivalent in play |
| Ranged values ("1 to 3") | `custom_points` | contract `stress_range`, clamped | equivalent in play |
| NoöPunk triggers | 5 ids, incl. **`ontological_shock`**, values 1–2 | 7 ids, **no** ontology-shock entry, values 1–3 with rationales | **the one substantive rule difference** — see below |
| Addiction | flag + list; the daily/monthly/weekly lifecycle is listed as a gap | full submodule: doses, missed day, 1d4 removal, monthly save, weekly recovery | |
| Scar effects | `effects(level)` returns a 13-key dictionary for the UI/adapters | contract `effects` per scar; `Dependent`, `Bloodthirsty` and `Penitent` exceptions applied **in resolution**, not only reported | |
| Breakdown effects | `combat_restricted` etc. reported | reported; HP/penalty data in the contract | neither applies them to a sheet — correctly, that is the table's act |
| Recovery | `restful_day`, `indulgence` (which itself consumes System Strain), `talk` (no once-per-day limit), `goal` | all four, with the once-per-day limits and the System Strain cost returned for the core to apply | |
| Persistence | inside the `GameState` schema | separate file with `version` + migration | the core schema is the core's; the overlay's is the overlay's |

**The substantive rule difference is ontology shock.** #928 says *"Keep ontology-shock/PSI mechanics
distinct from generic Stress. Define integration points, do not create a second incompatible
mental-health system."* The overlay obeys that and routes ontology shock to the Psyche overlay
(`mods/noopunk/psyche.gd`, #689); the core module scores it as Stress (+2). Both cannot be true. This is
the one place where a table could see a different number depending on which entry point it used, so it
needs a ruling, not a preference.

## Why neither session could resolve it alone

- **The overlay may not import the core.** `tests/test_foundational_lock_897.py` forbids
  `mods/**` from loading anything under `godot/core/`. So an overlay **cannot** delegate to
  `AwnStress`; if the rule lives in core, the overlay duplicate can only be deleted, not rewired.
- **The core may not import the mods.** The same lock forbids `godot/core/**.gd` from referencing
  `mods/`, so `GameState` cannot be re-wired to the overlay either. Moving the engine into `mods/`
  would silently remove the live-game API #929 added.
- **The duplicate guard cannot see it.** `tools/check_godot_rule_duplicates.py` compares domains as
  `<system>:<rule>` over `godot/core`, `src/godot/cwn` and `src/godot`; `mods/` is not a scanned tree, and
  `awn:stress` ≠ `noopunk:stress` even if it were. CI is therefore green with two engines present.

## Verified state of `main` at `1010ab8`

| Check | Result |
| --- | --- |
| `godot --headless --path . --import` then `--script res://godot/tests/run_tests.gd` | **1822 checks, 0 failed** (1768 before the import — see the trap below) |
| `python3 -m unittest discover -s tests` | **1652 tests, OK** |
| `python3 tools/release_packaging_guard.py` | PASS, 0 errors |

**Trap worth knowing.** `godot/core/game_state.gd` (the autoload) now names the global class
`AwnStress`. With a stale `.godot/global_script_class_cache.cfg` every run fails with *"Could not find
type AwnStress"* → the autoload does not instantiate → 36 checks silently do not run and the suite
reports **1768 checks, 0 failed**. Always `--import` before a headless suite, or read the check count
rather than the pass line.

## Options

**A — the core owns the rule; the overlay retires (recommended).**
`godot/core/awn_stress.gd` stays the engine and starts reading `data/rules/awn_stress.json` instead of
`const`s; the overlay's unique content moves into core with it: participation, the addiction lifecycle,
the three scar exceptions, the seven labelled NoöPunk triggers and the 148 checks. `mods/noopunk/stress.gd`
is deleted; the screen moves to `godot/ui/stress_screen.gd` calling the core engine (UI may call core);
`data/mods/registry.json` keeps the row only if a mod still exists.
*Why this is the house pattern:* AWN is a **published subsystem being imported**, like `cwn_*`/`swn_*`,
and NoöPunk code already lives in core (`godot/core/noopunk_tags.gd`, `noopunk_crisis_contact.gd`). #848
explicitly admits "selective WWN/AWN material" and names only the *homebrew* set — social relationships,
LaclauGPT factions, noösphere/Psyche, narrative procedures — as `mods/` material. Stress is not in that
list.
*Cost:* one sitting of file moves and a re-run; the overlay's tests move with it.

**B — the overlay owns the rule; the core module retires.**
Blocked unless `GameState` loses the Stress API, because core may not import `mods/`. It would also
retire the only live-game path. Not viable without re-opening the #897 lock.

**C — both stay, with a written non-divergence rule.**
Cheapest today and the worst to maintain: two arithmetics, two save formats, one rule that already
differs (ontology shock). This is exactly the drift `docs/godot/UNIFIED_IMPLEMENTATION.md` exists to
stop.

## Smallest useful answer to D58

* **"core owns it, overlay retires"** → an agent executes option A as one PR that ends with a single
  engine, one contract and one suite; or
* **"both stay"** → the ontology-shock difference must be resolved one way (the author says which), and
  the contract becomes the single source of the values, read by both; or
* **"overlay only"** → `GameState` loses the API and `mods/` is confirmed as the home of imported
  subsystems, which contradicts the placement of `cwn_*`/`swn_*` and would need the lock amended.

Nothing in this file deletes or changes either implementation.
