# Godot architecture — three live entry points, one case

**Status: audit finding. Nothing here deletes, moves or rewrites code.** Deleting a working scene is the
author's call, and #631 explicitly forbids "silently destroying working systems".

Measured against `origin/main` at `5ff584b`.

## The finding

The repository has **three separate, currently-working ways to play the same Lakkahaltia hospital case**,
each wired to a different tree, and each referenced by something that would break if it were removed.
That is worse than dead code: dead code is obvious, whereas three live copies drift.

| # | Entry point | Script | Tree | Who exercises it |
| --- | --- | --- | --- | --- |
| 1 | `scenes/main.tscn` — **the project default** (`run/main_scene`) | `godot/ui/main_menu.gd` | `godot/` | Every `godot --path .` run; the title screen |
| 2 | `scenes/lakkahaltia/ward.tscn` | `scenes/lakkahaltia/ward.gd` | `scenes/` | `tools/godot_smoke.sh` — loads it headless and requires the `WARD_READY` marker |
| 3 | `scenes/lakkahaltia/prototype.tscn` | `src/godot/lakkahaltia_case.gd` | `src/godot/` | `tests/godot/test_lakkahaltia.gd` loads the packed scene |

Separately, the `godot/` tree carries its **own** complete case: `godot/scenes/hospital.tscn` +
`godot/scenes/level_builder.gd` + `godot/scenarios/lakkahaltia/`, driven by
`godot/tests/run_tests.gd`, `godot/tests/playthrough.tscn` and `godot/tests/integration_playthrough.gd`.

So the case exists **four times over**: `godot/scenes/hospital.tscn`, `ward.tscn`, `prototype.tscn`, and
the data under both `data/scenarios/lakkahaltia/` and `godot/scenarios/lakkahaltia/`.

## Which one is canonical

**`godot/`**, on the evidence:

- it owns `run/main_scene`, so it is what a player sees on `godot --path .`;
- it has the most CI coverage (three entry points in `godot.yml`: the unit suite, the headless
  playthrough, and the integration playthrough);
- it is the only tree with a separated architecture (`core/`, `narrative/`, `scenarios/`, `ui/`, `tests/`).

`ward.tscn` is a **smoke fixture** rather than a rival implementation — it exists to prove the level
builds, and `WARD_READY` is a good idea worth porting into the canonical tree if it is not already there.

`src/godot/` is the odd one out: five files, 742 lines, and it is the tree that still contains
`core_rules.gd` — **the superseded `STAT + Skill + 1d10` adapter** over `data/rules/core.json`. The
approved baseline since the 2026-10-26 ruling is the Without Number kernel, which `godot/core/` and
`src/godot/wn_rules.gd` both implement.

## Why this matters beyond tidiness

1. **Divergence is silent.** A rule or content fix landed in `godot/` will not reach `ward.tscn` or
   `prototype.tscn`, and nothing fails. Three passing suites can each be green while disagreeing.
2. **Two kernels ship at once.** `core_rules.gd` resolves on `1d10`; the ruling says `2d6`. Any scene that
   still wires the old adapter is playing a different game than the one the rules decision describes.
3. **`tests/validate_scaffold.py` pins `src/godot/core_rules.gd`** as required scaffold, so the
   superseded adapter is *enforced* by a validator. That is the one place where the repository actively
   defends the old kernel.

## Recommendation (a proposal, not an action taken)

1. **Declare `godot/` canonical** in `docs/godot/README.md`, with one sentence saying what the other two
   are for.
2. **Keep `ward.tscn` as a smoke fixture** and say so in its header — or fold its `WARD_READY` assertion
   into `godot/tests/integration_playthrough.gd` and retire the scene.
3. **Retire `src/godot/` only after porting its unique content**: `wn_rules.gd` (if `godot/core/` lacks
   the explicit-dice entry path) and anything in `case_state.gd` not already in `godot/core/game_state.gd`.
   Then remove it from `tests/validate_scaffold.py` **in the same commit**, so the validator and the tree
   cannot disagree.
4. **Do not delete `prototype.tscn` without its test.** `tests/godot/test_lakkahaltia.gd` loads it, so
   removing the scene turns a green test red — which is the correct behaviour, but it must be part of the
   same change.

## What this document does not do

- It does not move, delete or rewrite any scene, script or test.
- It does not decide the art or gameplay direction.
- It does not claim the trees are identical: they are not, and establishing exactly how they differ is the
  first step of the retirement above, not something to assume.
