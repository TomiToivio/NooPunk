# NoöPunk restart — Godot starter

A top-down 2D game with one room, one player and movement. That is the whole feature list, on
purpose: the next rule Tomi writes gets implemented here, on top of this, instead of inside a system
designed in advance.

## Run

```sh
godot --path noopunk2
```

The project opens directly into the playable room. Requires Godot 4.x (developed against 4.7).

## Controls

| Key | Action |
| --- | --- |
| WASD or arrow keys | move |
| Esc | quit |

## Sanity check

```sh
godot --headless --path noopunk2 --script res://tests/smoke.gd
```

Checks that the scene loads, the player starts centred, movement changes position, the room bounds
hold on both axes, and the camera and hint exist. It cannot check that anything *looks* right — that
is what the window is for.

## Layout

```
noopunk2/
├── project.godot          # this project (separate from the legacy root project)
├── scenes/main.tscn       # the room, the player, the camera, the hint
├── scripts/player.gd      # movement and bounds
└── tests/smoke.gd         # headless check
```

## Deliberately absent

No stats, skills, dice, combat, inventory, dialogue, NPCs, quests or simulation. Adding one before its
rule exists in `rulebook/RULEBOOK.md` would recreate exactly the problem the restart is fixing.

## Manual verification

1. The window shows a dark room with a lighter inner rectangle.
2. A gold rectangle (the player) sits in the middle.
3. WASD and the arrow keys move it; diagonal movement is not faster.
4. It stops at the room edges instead of leaving them.
5. The hint label reads "WASD / arrow keys to move".
