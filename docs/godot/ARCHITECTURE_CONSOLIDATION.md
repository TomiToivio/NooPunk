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

## Duplicate rule domains — measured 2026-10-30

Beyond the four playable entry points, the *rules* are implemented twice. Both are substantial and
both pass their own suites, which is why the split survived review: nothing fails, the repository
just answers each rules question twice.

| Domain | `godot/core/` (canonical) | `src/godot/` (compatibility) |
| --- | --- | --- |
| Weapon / armour catalogue | `cwn_catalogue.gd` | `cwn/cwn_catalogue.gd` |
| Character creation | `cwn_character.gd` | `cwn/cwn_character.gd` |
| Attack, Shock, trauma | `cwn_combat_rules.gd`, `combat.gd` | `cwn/cwn_combat.gd` |
| System Strain | `cwn_strain.gd` | `cwn/cwn_strain.gd` |
| Healing | `cwn_healing.gd` | `cwn/cwn_healing.gd` |
| Encumbrance | `cwn_encumbrance.gd` | `cwn/cwn_encumbrance.gd` (branch) |
| Progression | `swn_progression.gd` | `cwn_progression.gd` |
| Psionics | `psionics.gd`, `psychic_effort.gd` | `swn_psionics.gd` |

### Parity evidence

`godot/tests/test_rules_parity.gd` runs both implementations over the same matrix — Strain ceilings
and forced overflow at four Constitution scores, Shock across four target ACs, the trauma threshold at
six rolls, the hit floor, stabilisation difficulty with and without a medkit, and natural healing for
the frail and the hale — and reports any disagreement as a failure.

The matrix currently passes: **512 checks, 0 failed**. One difference is a *contract* difference
rather than a rule difference, recorded in the suite: the canonical kernel takes `hit` and encodes
"Shock only applies on a miss" inside the function, while the compatibility module is miss-only by
contract and callers invoke it from the miss branch. Same rule, different signature.

### The guard

`python3.11 tools/check_godot_rule_duplicates.py` fails when a rule domain is implemented in more than
one tree, allowing today's list so migration can proceed in steps. The allowlist may only shrink.

### Deletion order

Parity first, then deletion — never the reverse:

1. Strain and healing: the matrix already proves equivalence; port the fractional/forced-overflow
   behaviour into `godot/core/` and delete the `src/godot/cwn/` copies.
2. Catalogue: keep `godot/core/`'s combat helpers, add the SRD-extracted loader from
   `src/godot/cwn/`, then delete the duplicate.
3. Character: keep `godot/core/`'s `hit_points`/`saves`, add the creation rules, then delete.
4. Combat: merge the Shock floor and trauma multiplication into `cwn_combat_rules.gd`.
5. Progression, then psionics.
6. Fold `tests/godot/` into `godot/tests/run_tests.gd` so one command runs every gate.

## Migration landed — 2026-10-30

The duplicate rule tree is gone. `src/godot/cwn/` no longer exists; every rule module now has one
home in `godot/core/`, and `python3.11 tools/check_godot_rule_duplicates.py` reports **0 duplicate
domains**.

| Module | Outcome |
| --- | --- |
| `cwn_catalogue` | canonical module gained a static SRD API (`srd_weapon`, `srd_armour`, `srd_rows`, `srd_background*`, `parse_dice`, `parse_shock`) reading `data/rules/cwn/srd_tables.json`; the compatibility copy was deleted. The instance API over the curated `data/rules/cwn_catalogue.json` is untouched — two data sources, one module. |
| `cwn_character` | creation helpers merged in (`from_rolls`, `from_array`, `creation_skill_pick`, `max_hit_points`, `save_target`, `npc_save_target`, `extra_languages`). **This fixed a rule defect**: the canonical `hit_points()` assumed a 6 on the level-1 d6, handing every new character up to five extra hit points. `max_hit_points()` rolls the actual die. |
| `cwn_combat` | the compatibility copy was deleted; `cwn_combat_rules.resolve_attack` already computed the Shock the miss would have dealt and applied it as the hit floor. |
| `cwn_strain`, `cwn_healing` | parity was proven first, then the compatibility copies were deleted; the canonical healing module gained `rounds_until_death`, `remove_frailty`, `first_aid` and the missing `FRAIL_REMOVAL_DIFFICULTY` constant. |
| `cwn_injury` | moved whole into the canonical tree as `CwnInjury` (the only implementation). |
| `cwn_progression` | moved from `src/godot/` to `godot/core/`; its test now preloads the canonical path. |
| `swn_progression` | **not** a duplicate — it is psychic training, not levelling. The guard was taught the difference (`DOMAIN_OVERRIDE`) instead of accepting a false positive that would have justified keeping two modules. |

### Verified

- `godot/tests/run_tests.gd` — **454 checks, 0 failed**
- `tests/godot/test_cwn_rules.gd` — PASS
- `tests/godot/test_cwn_progression.gd` — PASS

Deleting a `class_name` script requires clearing `.godot/` and re-importing, or the stale global class
cache keeps the old one alive and the run fails with "hides a global script class". Worth knowing
before the next deletion.
