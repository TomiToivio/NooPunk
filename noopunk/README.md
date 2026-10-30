> ## ARCHIVED — SUPERSEDED BY #848
>
> This directory came from the blank-rulebook restart (#827) and its custom seven-attribute sheet
> (#835). **Issue #848 restored vanilla CWN/SWN and the root `project.godot` as canonical.** Nothing here
> is authoritative; it is kept as reference until the author reauthorises or a migration removes it.
>
> Canonical: rulebook `rulebook/00_INDEX.md`, Godot `project.godot`, startup scene `res://scenes/main.tscn`.

# NoöPunk — canonical restart (issue #827)

**This directory is the canonical NoöPunk project from now on.** Everything here is new and intentionally
minimal. The legacy material elsewhere in the repository (the old `rulebook/`, the earlier Godot projects
under `godot/` and `src/godot/`, the Python kernels under `src/rules/`) is **frozen reference**: not
deleted, not extended, not the target of new work.

## The two canonical paths

| What | Path |
|---|---|
| Tabletop rulebook | [`rulebook/RULEBOOK.md`](rulebook/RULEBOOK.md) |
| Godot top-down RPG | [`game/`](game/) — open `game/project.godot` |

Every subsequent issue targets **these** paths. If a future task seems to belong to an older directory,
that is a signal to stop and ask, not to quietly resume work there.

## How we work

Tomi supplies the rules, scenario concepts, interactions and guidelines **one piece at a time**. Each
piece is implemented in both the rulebook and the game, in one pass, and nothing broader is invented
along the way. See [`../docs/design/TOMI_DRAFT_WORKFLOW.md`](../docs/design/TOMI_DRAFT_WORKFLOW.md).

## Status

- Rulebook: **blank draft** — structure only, no rules.
- Game: **starter** — one room, one placeholder player, keyboard movement, camera, nothing else.
