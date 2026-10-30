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
walking scene behind it. **R** rolls a new agent; **WASD / arrows** move. The sheet stays as it is while
you walk, so the rolled agent is the one you are playing.

## Tests

```bash
godot --headless --path noopunk/game --script res://tests/test_agent.gd
```

Covers every band boundary (3–18), the seven attributes, the −3…+3 human range, and that a rolled sheet
is never transhuman.

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

## Growing this project

Add to **this** project. New scenes live beside `main.tscn`; new scripts beside `player.gd`. If a change
seems to require an older Godot project elsewhere in the repository, stop and ask instead.
