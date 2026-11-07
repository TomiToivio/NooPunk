# NoöPunk RPG

The game track: **Cities Without Number as an immutable core**, plus a NoöPunk overlay that adds tags,
graphs and scenes without touching the core.

## The boundary

- `src/rules/` carries CWN, imported SWN/AWN material and NoöPunk overlays. **CWN is not modified,
  rebalanced, forked or replaced here.** The rule is enforced by `tools/rules_constitution_audit.py`
  and the immutable-core gates in CI.
- NoöPunk gameplay lives in the overlay: social / goal / clue / personality tags, the four graph
  families, the six scene types.
- The RPG **consumes** Story Graph content and Simulator social state through adapters. It is not the
  source of truth for either.

## Status

P0 skeleton. Today the RPG code is still at the repository root (`src/`, `mud/`, `campaign/`,
`strategy_game/`, `godot/`, `mods/`, `portable_noopunk/`). Stage P4 moves it here, one area per PR,
with compatibility shims. **Nothing has been moved yet; every existing path still works.**
