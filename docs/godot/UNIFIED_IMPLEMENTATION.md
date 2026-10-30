# Unified Godot implementation: current integration contract

Audit date: 2026-10-30. This document supersedes the *recommendation only* parts of `ARCHITECTURE_CONSOLIDATION.md` for new work, without claiming that legacy scripts have already been ported.

## Current architecture and what was actually reconciled

There is **one** engine project: `/project.godot`, configured with `scenes/main.tscn` as the start scene and `GameState = res://godot/core/game_state.gd` as the only autoload. **There are multiple live gameplay implementations inside it**, not multiple Godot project files.

| Existing path | Role now | Consolidation policy |
| --- | --- | --- |
| `godot/scenes/hospital.tscn` + `godot/scenarios/lakkahaltia/` | Main hospital case | Primary case implementation, keep |
| `godot/ui/mvp_game.tscn` + `godot/core/session.gd` | Home/HQ/mission tactical MVP | Keep and extend through main menu |
| `scenes/campaign.tscn` + `src/godot/campaign_screen.gd` | Existing campaign prototype | Now exposed from main menu, preserve until parity migration |
| `scenes/lakkahaltia/ward.tscn` + `src/godot/lakkahaltia_case.gd` and `prototype.tscn` | Older scene/smoke/test variants | Compatibility fixtures, not templates for new games |
| `src/godot/cwn*/`, `src/godot/swn_psionics.gd`, `src/godot/campaign_state.gd` | Additional runtime rule/state modules | Audit and port unique behaviour into canonical ownership incrementally |
| `src/godot/core_rules.gd` | Superseded 1d10 legacy kernel | Never extend as active Without Number rules |

This change joins the existing campaign prototype to the **existing default title screen**, so users and agents can reach the three substantive modes through one launch scene. It does **not** merge incompatible case/campaign saves, delete scripts, or claim rule-engine parity.

## Required migration sequence

1. Inventory symbol-level overlaps in `godot/core/` versus `src/godot/` (CWN combat, characters, catalogue, injury/healing, hacking, SWN psionics); record unique APIs and cross-language parity fixtures. Do not presume similar file names mean identical behaviour.
2. Decide one owner *per feature*, with `godot/core/` the default destination; convert other entry points into tested adapters or remove them only after callers are migrated.
3. Migrate the campaign screen/state into `godot/` behind a versioned save migration, without combining two state instances in the same session.
4. Consolidate duplicate Lakkahaltia data and scenes only after regression tests prove the old case, campaign and MVP still function.
5. Remove legacy scaffold references and obsolete adapters in the same PR as their tested replacements. Keep Python tabletop/reference code in `src/rules/`; a Python reference is not another Godot project.

## Merge checklist

- Root main menu offers hospital, MVP and campaign paths; only one `project.godot`.
- No new divergent rules kernel or duplicated autoload.
- Run `godot --headless --path . --import`, `godot --headless --path . --script res://godot/tests/run_tests.gd`, `godot --headless --path . res://godot/tests/playthrough.tscn --quit-after 300`, and `bash tools/godot_smoke.sh` with the pinned engine; run relevant `tests/godot` suites.
- Review CI for all paths affected, including compatibility fixtures.
- Document runtime-dependent checks honestly if Godot is unavailable.

See `AGENTS.md` for binding agent coordination instructions.
