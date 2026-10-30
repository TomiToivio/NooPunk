> **SUPERSEDED, ARCHIVED PROTOTYPE (issue [#848](https://github.com/TomiToivio/NooPunk/issues/848)).** This is the old #827/#835 seven-attribute experiment, **not** the canonical Godot game. The sole active RPG project is the repository-root `project.godot`, startup `res://scenes/main.tscn`; its rules are vanilla CWN primary plus vanilla SWN Revised psionics. See [root START_HERE](../../START_HERE.md) and [AGENTS.md](../../AGENTS.md). Preserve this prototype for historical reference, but do not extend or use its character creation.

---

# NoöPunk — Godot game

Top-down 2D project. It opens into **character creation**: seven attributes, each rolled as 3d6 and
shown as the converted signed value from the rulebook's table. *Roll again* rerolls the set; *Continue*
enters the walking scene, where the sheet stays on screen while you move.

No skills, checks, combat, inventory, dialogue, quests, AI or simulation — by design. **No game rule
reads the attributes yet**, because no resolution mechanic has been authored.

## Run it

```bash
godot --path noopunk/game          # from the repository root
```

Or open `noopunk/game/project.godot` in the Godot 4.x editor and press F5.

## Checks

```bash
godot --headless --path noopunk/game --script res://tests/smoke.gd
godot --headless --path noopunk/game --script res://tests/character.gd
```

- `smoke.gd` — the scene loads, the player starts centred, movement changes position, the room bounds hold.
- `character.gd` — every 3d6 boundary in the rulebook's table, exactly seven attributes, the human
  −3..+3 range, reroll behaviour, and that a rolled sheet survives into the walking scene unchanged
  while the player moves.

Neither checks how anything *looks*; that is what the window is for.

## Files

| File | Purpose |
|---|---|
| `project.godot` | project config; main scene is `res://creation.tscn` |
| `creation.tscn` / `creation.gd` | the character sheet: roll seven attributes, reroll, continue |
| `main.tscn` / `main.gd` | the room: floor, player, camera, hint and the sheet read-out |
| `player.gd` | movement and bounds |
| `attributes.gd` | reads `data/attributes.json`, converts 3d6 totals to values |
| `sheet.gd` | the one autoload: holds the rolled sheet between scenes |
| `data/attributes.json` | the single machine-readable copy of the rulebook's tables |
| `tests/` | headless checks |

## Growing this project

Add to **this** project. New scenes live beside `main.tscn`; new scripts beside `player.gd`; new rule
data goes in `data/` and is quoted in `../rulebook/RULEBOOK.md` in the same change. If a change seems to
require an older Godot project or the legacy rulebook elsewhere in the repository, stop and ask instead.
