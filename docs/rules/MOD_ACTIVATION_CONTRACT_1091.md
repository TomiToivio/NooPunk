# Mod activation contract (#1091)

This document describes the **single canonical registry** at `data/mods/registry.json`. Do not create a parallel mod catalogue. The implementation in `src/rules/mod_boundary.py:validate_registry` is the structural gate, and `tools/check_mod_activation.py --check` reports implementation and tabletop gaps.

A schema-3 mod records: its name and CWN safety flag; real implementation file paths; `hooks` identifying existing `path`/`symbol` entry points; `state` names; `dependencies` (currently `cwn-core` or another registered mod); an `off_switch` with `default_enabled` and `behavior`; and either a real `tabletop_procedure` file or a documented `tabletop_gap`. Missing printed procedures are **not** asserted as playable.

## Usage and scope

Run `python3 tools/check_mod_activation.py --check` and `python3 -m unittest tests.test_mod_activation_1080 tests.test_mod_activation_1091 tests.test_issue897_core_mod_boundary`. The validator reads hook source files and checks named Python or GDScript function declarations. It checks structural truth, **not** whether the game's adapters actually invoke the hook, whether the procedure is good enough to play, or whether an off-switch is wired into persistence. Those require functional tests before claiming completion.

All six registered mods are included; existing GDScript overlays are represented in their same mod entries. `vices_temptations` is not implemented and therefore deliberately has no hooks or persistent state and defaults off. Stress uses the original `data/rules/awn_stress.json` contract, never a second table of numbers. No mod changes the CWN baseline. Save data should remain intact if a mod is disabled; the off-switch means skipping optional overlay execution, not wiping historical state.

## Remaining evidence gaps

Printed tabletop procedures are still missing for all entries with an explicit `tabletop_gap`; a gap is a truthful status, not a feature. Runtime activation/deactivation and adapter save compatibility must be separately exercised. GDScript hooks and Python entry points are listed by real function names, not invented event callbacks. See issues #1081 and #1091 for evidence and follow-up.
