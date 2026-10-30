# START HERE — the NoöPunk restart (issue #827)

The tabletop rulebook and the Godot game are being restarted **together**, from the smallest
foundation that can be played. Everything that came before stays in the repository, untouched, as
legacy material — it is not the current game, and new work must not drift back into it.

## The two canonical artifacts

| Artifact | Canonical path | Status |
| --- | --- | --- |
| Tabletop rulebook | [`noopunk/rulebook/RULEBOOK.md`](noopunk/rulebook/RULEBOOK.md) | **blank by design** |
| Godot game | [`noopunk/game/`](noopunk/game/) (`noopunk/game/project.godot`) | one room, one player, movement |
| Rules of the process | this file + issue **#827** | meta-issue, stays open |

**Legacy, frozen — do not add to it:** the root `RULEBOOK.md`, `rulebook/`, the root
`project.godot`, `godot/`, `src/godot/`, `src/rules/`, `data/rules/`, `strategy_game/`. They keep
working and keep their history. They are not where the new NoöPunk is being designed.

## Run the game

```sh
godot --path noopunk/game
```

Controls: **WASD** or **arrow keys** to move. **Esc** quits. The window opens directly into the
playable room.

Headless sanity check (the one CI can run):

```sh
godot --headless --path noopunk/game --script res://tests/smoke.gd
```

```
PASS: noopunk starter — scene loads, player is centred and movable, bounds hold
```

## How the next piece of work arrives

Tomi supplies **one** rule, interaction or scenario fragment. Then:

1. It is written into `noopunk/rulebook/RULEBOOK.md`, in its section.
2. The same decision is implemented in `noopunk/game/` so it can be played.
3. Both are checked together — the rulebook says what the game does; the game does what the
   rulebook says.
4. Only the child issue closes. **#827 stays open.**

A child issue must name **both** artifacts it changes. If a proposed change touches only one side,
the issue says why: a presentation-only change is legitimate; a rule that exists only in code is not.

## What does not exist yet, on purpose

No attributes, no skills, no dice, no combat, no injury, no inventory, no dialogue system, no NPCs,
no quests, no factions, no psionics, no hacking, no economy, no LLM integration. Each arrives when
the author writes it, not before. **An empty section in the rulebook is the current design state.**
