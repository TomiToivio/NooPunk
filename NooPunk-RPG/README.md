# NoöPunk RPG — the mechanics track

> **The CWN core is immutable.** This subproject consumes a story graph and a social-world state; it does not
> own either, and it does not own the rules it runs on.

## What is here now, and where it will move

This directory is a **pointer** until the staged migration in
[`docs/architecture/MIGRATION_MAP_1295.md`](../../docs/architecture/MIGRATION_MAP_1295.md) reaches the RPG. Nothing
has been moved, because moving a rules tree in one commit is how a project loses a week.

| Concern | Lives today | Destination |
| --- | --- | --- |
| Cities Without Number rules | `src/rules/cwn_*.py`, `mud/nopunk_mud/cwn/` | unchanged; **never** edited for a NoöPunk feature |
| NoöPunk overlays (tags, graphs, mods) | `src/rules/*overlay*`, `src/world/graphs.py`, `data/mods/` | `NooPunk-RPG/` |
| Tabletop text | `rulebook/`, `docs/tabletop/` | `NooPunk-RPG/` |
| Campaign and scenarios | `docs/campaign/`, `docs/scenarios/` | `NooPunk-RPG/` |
| Engines (CLI, Evennia, Godot) | `src/console/`, `mud/`, `godot/` | adapters, unchanged |

## The boundary, stated once

- **CWN is not forked, rebalanced or rewritten.** A NoöPunk feature that needs a new CWN number is a NoöPunk
  overlay with its own justification, or it does not ship.
- **The RPG does not author the story.** Scenes come from the graph; if a scene is missing, the graph is
  incomplete, not the RPG.
- **The RPG does not simulate society.** Social state arrives from the Simulator through the shared tag/graph
  contract.

## Adapters

`src/contracts/story_graph_contract.py` validates a story-graph document; the RPG-side consumer is
`src/contracts/rpg_scene_adapter.py`, which turns a validated scene into the shape the existing
`src.world.graphs.StoryNode`/`StoryGraph` already uses. Both are covered by contract tests.
