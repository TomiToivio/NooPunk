# NoöPunk — Godot starter

Minimal top-down 2D project. One room, one placeholder player, keyboard movement, a camera and a hint
label. No stats, skills, combat, inventory, dialogue, quests, AI or simulation — by design.

## Run it

```bash
godot --path noopunk/game          # from the repository root
```

Or open `noopunk/game/project.godot` in the Godot 4.x editor and press F5. The project launches straight
into `main.tscn`.

## Files

| File | Purpose |
|---|---|
| `project.godot` | project config; main scene is `res://main.tscn` |
| `main.tscn` | the room: floor, player, camera, hint label |
| `player.gd` | movement and bounds — the only script |

## Growing this project

Add to **this** project. New scenes live beside `main.tscn`; new scripts beside `player.gd`. If a change
seems to require an older Godot project elsewhere in the repository, stop and ask instead.
