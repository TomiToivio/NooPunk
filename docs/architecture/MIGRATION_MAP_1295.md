# Migration map — what exists, what stays, what moves (#1295)

> **Nothing in this table has moved yet.** This is an inventory taken on 2026-11-07, so that the move can be
> staged instead of improvised. Each row is a candidate PR, not a promise.

## Why move anything at all

The pivot is about attention, not tidiness. Three tracks share one repository; when their files are
interleaved, every agent reads every rule to find the story. Separating them means a writer can open one
folder, and a simulator agent can run tests without loading a CWN character sheet.

## Inventory

| Concern | Lives today | Subproject | Move? | Risk |
| --- | --- | --- | --- | --- |
| Manuscript | (does not exist yet) | Story | n/a | the directory and `POLICY.md` are new |
| Story graph code | `src/world/graphs.py::StoryGraph`, `src/rules/graph_authoring.py` | Story/Graph | **no** — shared runtime | high: the RPG imports it |
| Story graph documents | `docs/campaign/`, `docs/scenarios/` | Story/Graph | later | medium: docs links |
| Simulator | `src/social_sim/` | Simulator | **later**, after it stabilises | medium: it is under active development |
| Simulator schema/contracts | `src/social_sim/*schema*`, `data/schema/` | Simulator + shared | no | low |
| CWN rules | `src/rules/cwn_*.py`, `mud/nopunk_mud/cwn/` | RPG | **never** | changing the path breaks the parity tool and the immutable-core lock |
| NoöPunk overlays | `src/rules/*overlay*`, `data/mods/`, `src/rules/mod_boundary.py` | RPG | later | low |
| Tabletop rules | `rulebook/`, `docs/tabletop/` | RPG | later | low |
| Campaign documents | `docs/campaign/`, `docs/scenarios/` | RPG | later | medium |
| Engines | `src/console/`, `mud/`, `godot/` | RPG adapters | no | high: they import everything |
| Portability package | `portable_noopunk/`, `src/console/` | shared | no | it is the proof of engine independence |

## Staged plan

1. **This PR.** Directories, READMEs, `Story/POLICY.md`, templates, the two schemas, the validator, the RPG
   adapter, the boundary tool, the example, the tests. No existing file moves.
2. **Manuscript first.** Tomi writes a scene in `Story/`; an agent adapts it into `Graph/`. This proves the
   workflow before any code moves, and it is the only step that produces something valuable immediately.
3. **Docs into subprojects.** Campaign and scenario documents move with redirect stubs at the old paths, one
   directory per PR.
4. **Simulator package.** `src/social_sim/` becomes `NooPunk-Simulator/` with a compatibility shim
   (`src/social_sim/__init__.py` re-exporting) so existing imports and tests keep working for one release.
5. **Overlays, not core.** `src/rules/*overlay*` and `data/mods/` move; `src/rules/cwn_*` does not. The
   immutable-core lock is the reason.
6. **Retire the shims.** One release after the move, with a note in the register.

## What must not happen

- A single commit that moves `src/rules`, `src/world` or `src/console`. They are imported by the CLI, Evennia,
   the parity tools and the portability package.
- A compatibility wrapper that silently changes semantics: a re-export is `from x import *`, not a rewrite.
- Moving the CWN core. The file paths are part of the immutable-core lock and the coverage tools.
- Filling `Story/` with placeholders to "test the migration". The manuscript is Tomi's, and the boundary
  checker will refuse it.
