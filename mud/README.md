# NoöPunk MUD

A **separate, text-based, persistent multiplayer** game built on [Evennia](https://www.evennia.com/), sharing
NoöPunk canon and CWN rules with the Godot game but **no runtime**.

**Status: MAIN GAME, implementation not started.** Per #950 this directory is the primary playable
implementation and the default target for coding agents; the Godot project is secondary/legacy. Nothing here
runs yet — the phase-1 build order below is the work queue, not a description of existing code.

## The boundary, in one table

| | NoöPunk MUD (this directory) — **primary** | NoöPunk Godot — **secondary/legacy** |
|---|---|---|
| Runtime | Python 3, Evennia server | Godot 4, `project.godot` at repository root |
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

## Phase 1 — offline single-player UNSA campaign (#950)

The first target is a **complete playable solo game with no multiplayer, no LLM and no external API**: create a
UNSA Academy graduate in Helsinki, take the first assignment, play several scenes, investigate, resolve
skill/combat/hacking checks, complete the quest, live with the consequences, save and resume.

Build order:

1. Evennia project skeleton under `mud/` with its own requirements and a smoke test that the server starts
   headless — nothing about game content yet.
2. CWN character bridge reading `data/rules/` without copying it.
3. Deterministic scripted GM: scenes, triggers, clue progression, adjudication, endings — all headless.
4. Investigation, travel, inventory, combat, hacking, progression, persistence.
5. GUMSHOE investigative overlay, PbtA Noösphere/Psyche/ontological shock, LaclauGPT ideology/reputation —
   modular, never replacements for the CWN baseline.

Phase 2 (multiplayer, LLM agents/GMs, Mesa population simulation) starts only after phase 1 is playable
without any of it.

None of that is started. Claiming otherwise is how a second game gets half-built in two places.
