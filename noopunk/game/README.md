# NoöPunk — Godot starter

Minimal top-down 2D project. One room, one placeholder player, keyboard movement, a camera and a hint
label. No stats, skills, combat, inventory, dialogue, quests, AI or simulation — by design.

## Run it

```bash
godot --path noopunk/game          # from the repository root
```

Or open `noopunk/game/project.godot` in the Godot 4.x editor and press F5. The project launches straight
into `main.tscn`.

## What you see

A UNSA agent's sheet on the left — seven attributes rolled on 3d6 and shown as signed values — and the
walking scene behind it.

| Key | Action |
|---|---|
| **R** | roll a new agent (sheet open) |
| **Enter / Space** | put the sheet away and walk |
| **Tab** | bring the sheet back |
| **WASD / arrows** | move |

The roll is kept when the sheet is put away, so the agent you walk as is the one you rolled.

## Tests

```bash
godot --headless --path noopunk/game --script res://tests/test_agent.gd
godot --headless --path noopunk/game --script res://tests/smoke.gd
```

`test_agent.gd` covers every band boundary (3–18), the seven attributes, the −3…+3 human range read from
the shared table, and that a rolled sheet is never transhuman. `smoke.gd` covers the scene, movement,
bounds and the continue/reopen behaviour.

## Files

| File | Purpose |
|---|---|
| `project.godot` | project config; main scene is `res://main.tscn` |
| `main.tscn` | the room: floor, player, camera, hint label |
| `player.gd` | movement and bounds |
| `agent.gd` | attribute generation, reading `data/attributes.json` |
| `sheet.gd` | the character sheet overlay and reroll key |
| `data/attributes.json` | **single source of truth** for the tables |
| `tests/test_agent.gd` | headless rules test |
| `tests/smoke.gd` | headless scene/movement test |

## Growing this project

Add to **this** project. New scenes live beside `main.tscn`; new scripts beside `player.gd`. If a change
seems to require an older Godot project elsewhere in the repository, stop and ask instead.
