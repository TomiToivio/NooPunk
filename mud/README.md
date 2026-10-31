# NoöPunk MUD

A **separate, text-based, persistent multiplayer** game built on [Evennia](https://www.evennia.com/), sharing
NoöPunk canon and CWN rules with the Godot game but **no runtime**.

**Status: boundary established, implementation not started.** Nothing here runs yet. This file exists so
that the boundary is decided before the first line of MUD code, which is what #946 asks for.

## The boundary, in one table

| | NoöPunk Godot | NoöPunk MUD (this directory) |
|---|---|---|
| Runtime | Godot 4, `project.godot` at repository root | Python 3, Evennia server |
| Interface | graphical, `scenes/`, `godot/` | text commands, telnet/web client |
| Tests | `godot --headless --script res://godot/tests/run_tests.gd` | pytest under `mud/tests/` |
| Entry point | `project.godot` | `mud/server/` (Evennia layout) |
| Dependencies | Godot binary, no Python runtime | `mud/requirements.txt` |

## What is shared

Canon, scenario data, CWN mechanics **as specifications**, and platform-neutral schemas. Shared inputs are
read, not forked: if a rule changes, it changes once and both games follow.

## What is never shared

Runtime assumptions, UI code, scene files, and release automation. A MUD change must not be able to alter
Godot behaviour, and a Godot change must not be able to alter the MUD's.

## Rules of engagement for agents

1. **Identify the target game before editing.** MUD work stays under `mud/`; Godot work stays under
   `godot/`, `scenes/` and the root `project.godot`.
2. **No cross-imports.** `mud/` must not reference `res://`, `.gd`, `.tscn`; Godot code must not import
   `mud.*`. `tests/test_mud_godot_boundary.py` enforces this.
3. **CWN is not forked.** Noösphere, ideology, social ties and ontological shock are modules layered on the
   CWN baseline, never edits to it.

## Next steps, in order

1. Evennia project skeleton under `mud/` with its own requirements and a smoke test that the server starts
   headless — nothing about game content yet.
2. A CWN character bridge that reads `data/rules/` without copying it.
3. Concordia-style LLM agent orchestration, kept behind an interface so the MUD is playable without it.
4. Mesa-based faction/social simulation, consuming the same canon data.

None of that is started. Claiming otherwise is how a second game gets half-built in two places.
