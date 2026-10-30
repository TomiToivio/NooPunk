# Issue #848 — one shared CWN/SWN baseline and one Godot RPG

**Status:** coordination record. #848 stays open until alignment is verified; this document pins the
baseline and retires the competing directions.

## Decision

- **Rules:** plain vanilla **Cities Without Number** primary, plain vanilla **Stars Without Number
  Revised** where CWN has no procedure (its psionics). No seven-attribute conversion, no custom
  difficulty ladder, no reskin of published mechanics.
- **Game:** one 2D top-down Godot RPG in the repository-root project, turn-based tactical play,
  source-faithful hacking and PSI.
- **One baseline:** every agent works from the commit below and the paths in this document.

## Audited baseline

| Item | Value |
|---|---|
| Baseline commit | **`36092a5`** (`main`, audited 2026-10-30) |
| Tabletop authority | CWN SRD <https://cwn.quadrifons.com/> primary; SWN Revised SRD for psionics |
| Rules record in-repo | `docs/rules/` (coverage + procedure notes), `data/rules/` (machine-readable) |
| Canonical Godot project | **`project.godot`** (repository root) |
| Canonical startup scene | **`scenes/main.tscn`** → `godot/ui/main_menu.gd` |
| Canonical rules kernel | **`godot/core/`** (issue #791; `src/godot/` is legacy) |
| Canonical Godot tests | **`godot/tests/run_tests.gd`** (the suite CI runs) |
| Legacy test root | `tests/godot/` — no new tests, files move out as touched |

### Verified at the baseline

```sh
godot --headless --path . --import                       # rc 0
godot --headless --path . --script res://godot/tests/run_tests.gd
# 760 checks, 0 failed
```

The root project's own tests pass and the project imports cleanly at `36092a5`. A top-down gameplay
scene is **not** on `main` yet (see "Known gap"); the menu, ward/campaign routes and the CWN kernels
are.

## Subsystem authority

Do not blend books inside one procedure. CWN governs unless the row says otherwise; where SWN is
named, use the SWN Revised procedure whole.

| Subsystem | Authority |
|---|---|
| Attributes (STR/DEX/CON/INT/WIS/CHA), 3–18 and modifiers | CWN |
| Character creation, classes, foci, backgrounds, skills | CWN |
| Skill checks (2d6 + attribute + skill vs difficulty) | CWN |
| Saving throws (d20 ≥ 16 − level − best of pair) | CWN |
| Combat: attacks, AC, shock, trauma, action economy, major injuries, strain | CWN |
| Equipment, armour, weapons, cyberware, drones, vehicles | CWN |
| Hacking: Access/CPU, verbs, subjects, programs, demons | CWN |
| Progression: XP, levels, attack bonus, HP, skill points | CWN |
| Psionics: Psychic class, disciplines, Effort, techniques | **SWN Revised** |

A character is built entirely under one book's creation rules; a CWN character does not acquire SWN
psychic disciplines, and an SWN psychic uses SWN skills and combat, not a hybrid.

## Superseded directions

| Direction | Where it lives | Disposition |
|---|---|---|
| Blank-rulebook restart (#827) | `noopunk/rulebook/RULEBOOK.md` | **Archived, read-only.** Kept for history; no new work |
| Seven-attribute sheet (#835: Fitness…Empathy) | `noopunk/game/`, `noopunk/game/data/attributes.json` | **Archived.** Not the attribute system; do not extend |
| Agent guidance naming `noopunk/` canonical | `AGENTS.md` §"NEW AUTHORITATIVE RESTART", `START_HERE.md`, `noopunk/README.md` | **Superseded by this document / #848**; agent-facing files now say so |
| Seven typed attribute tags (#821) | `docs/rules/ISSUE_821_TAG_MIGRATION.md`, `rulebook/` | Reference only until Tomi reauthorizes |
| `restart/` tree (removed in #834) | git history | Left in history; not restored |

Nothing is deleted by this migration: the archive keeps its files, branches and history. No
force-reset, no erased work.

## Migration actions

1. `AGENTS.md` carries a **CURRENT DIRECTIVE** at the top: #848, baseline SHA, canonical paths,
   vanilla CWN/SWN, and the supersession list.
2. The stale `noopunk/`-canonical section in `AGENTS.md` is replaced with an archive pointer.
3. Root `START_HERE.md` describes the canonical project and how to run/test it.
4. `noopunk/README.md` and `noopunk/START_HERE.md` carry an archive banner pointing at the root.
5. Open PRs from the blank restart were **none** at audit time; no PR was merged into the archive.

## Known gap (next child issue, not silently claimed)

`main` has no top-down gameplay scene: `scenes/main.tscn` is the menu, the Romppainen MVP route
(`godot/ui/mvp_game.tscn`) is a Control-based flow, and `godot/scenes/hospital.tscn` is a `Node3D`
level. The #782 slice contributed the CWN kernel, catalogues and procedures, not a surviving 2D
top-down scene. The next implementation child issue is therefore:

> **Build the top-down vertical slice in the root project**: a `Node2D` scene reachable from
> `scenes/main.tscn`, with tile movement, turn order, one CWN attack resolution and one skill check
> against the existing `godot/core/` kernels — tested headlessly, plus a screenshot check.

This document does not claim that slice exists.

## Coverage backlog

From `docs/rules/CWN_GODOT_COVERAGE.md` (statuses as of the baseline):

- Cyberware: head, limb, nerve, sensory, medical and skin tables (body implants are in).
- Drones and vehicles (catalogue + chase/craft procedures in `CWN_VEHICLES_CHASES_CRAFT.md`).
- Hacking: air gap/range, program memory, demons and watchdogs.
- SWN Revised psionics: technique catalogue and a legal Psychic creation path (Effort kernel exists).
- Foci and Edge tables: data exists, no UI.
- Top-down scene and turn-based tactical loop (see "Known gap").

## Handoff block (required in related PRs)

```
Baseline commit SHA: 36092a5
Canonical rulebook:  CWN SRD (primary) + SWN Revised SRD (psionics); repo record docs/rules/, data/rules/
Canonical Godot project: project.godot (repository root)
Canonical startup scene: scenes/main.tscn
Rules authority: vanilla CWN primary + vanilla SWN Revised (psionics only)
Superseded instructions/branches: #827 blank restart, #835 seven attributes, noopunk/ tree; no open PRs at audit
Verified behaviors / test commands:
  godot --headless --path . --import
  godot --headless --path . --script res://godot/tests/run_tests.gd   # 760 checks, 0 failed
```
