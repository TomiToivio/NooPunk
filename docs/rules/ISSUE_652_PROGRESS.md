# Issue #652: incremental implementation status

The author goal is a full CWN chassis in the rulebook, Python and Godot,
plus SWN psychic abilities in the first scenario. **This commit is not the
full conversion.**

## Implemented in this branch
- New Python `src/rules/psionics.py` authorization wrapper, preserving
  #648's named Effort commitments, durations and validated snapshots.
- New Godot `godot/core/psionics.gd` wrapper with the same psychic-package
  authorization and scenario technique identifiers.
- Explicitly original *provisional* NoöPunk technique identifiers:
  `surface_read`, `empathic_trace`, `premonition`.
- Python regression tests for authorization, rank checks, restoration
  and Effort recovery.

## Still required before closing #652
- Build out combat, trauma, mortal injury, System Strain, first aid,
  cyberware, hacking, advancement and encounter action economy in one
  shared machine-readable contract, Python engine and Godot adapter.
- Wire the Lakkahaltia scenario to its complete canonical CWN character
  sheet, dialogue checks, hacking and psionics; add Godot playthrough tests.
- Verify every numerical rule against the authorized source material.
- Port existing #648 tests to the new classes, migrate all imports and
  remove legacy implementations **only after** consumers are migrated.
- Run Python, Godot headless unit and integration tests plus lint/type
  checks in a runner with Godot installed.

Licence note: this change contains original technique identifiers and
resource code, not excerpts of SWN Revised's protected technique prose.
