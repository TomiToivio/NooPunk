# CWN SRD implementation slice: Godot rules kernel

The current baseline is `rulebook/WITHOUT_NUMBER_BASELINE.md` and `data/rules/without_number.json`. `src/godot/cwn_rules.gd` provides a **new** Godot 4 GDScript rules module. It does **not** delete or reinterpret `src/godot/core_rules.gd` (the retired 1d10 runtime adapter). Do not merge the two resolution systems.

## Implemented, source-checked

- Attribute 3..18 -> standard modifier mapping; trained rank 0..4 and untrained -1; 2d6 + ability modifier + skill + circumstances + aid, meet-or-beat. Circumstances ±2; group aid maximum +1.
- Opposed checks: higher roll wins; PC wins ties.
- Physical, Evasion, Mental and Luck save targets; natural 1 always fails, natural 20 always succeeds.
- Generic d20 attack total versus armor class. Other CWN attack mechanics (e.g. special damage, trauma, shock) are not implemented.
- Hacking **eligibility precheck only**: wired connection or wireless proximity and unobstructed line of sight, free CPU and sufficient Access, wireless -2 and VR crown -1. Full Jack In, programs, Access spending, cyber targeting and alert procedures remain unimplemented. This method is not permission to bypass network access controls.

**Sources**
- https://cwn.quadrifons.com/rules-of-the-game/skill-checks/
- https://cwn.quadrifons.com/rules-of-the-game/saving-throws/
- https://cwn.quadrifons.com/hacking/hacking-mechanics/
- https://cwn.quadrifons.com/rules-of-the-game/combat/attacks-in-combat/
- https://cwn.quadrifons.com/

The community mirror warns that certain optional rules and NPC material are missing. Verify full published SRD/book before implementing omitted sections. SWN supplies PSI, AWN supplies crisis survival, WWN supplies otherworld exploration as prescribed by the NoöPunk baseline. No verbatim third-party rules prose/art was imported.

## Run tests

```bash
godot --headless --path . --editor --quit
godot --headless --path . --script tests/godot/test_cwn_rules.gd
```

These tests check executable mechanics, not rulebook prose. Next: integrate this shared kernel into the hospital case, make skill checks use a full character sheet, implement character creation and real CWN source-approved combat/hacking procedures in smaller reviewable steps.
