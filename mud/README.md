# NoöPunk MUD

A **separate, text-based, persistent multiplayer** game built on [Evennia](https://www.evennia.com/), sharing
NoöPunk canon and CWN rules with the Godot game but **no runtime**.

**Status: first implementation scaffold added in PR #948.** Evennia runtime and multiplayer behaviour have not yet been verified; see the implementation notes below.

## The boundary, in one table

| | NoöPunk Godot | NoöPunk MUD (this directory) |
|---|---|---|
| Runtime | Godot 4, `project.godot` at repository root | Python 3, Evennia server |
| Interface | graphical, `scenes/`, `godot/` | text commands, telnet/web client |
| Tests | `godot --headless --script res://godot/tests/run_tests.gd` | Python unittest under `mud/tests/` |
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

## Remaining steps, in order

1. Run and smoke-test the Evennia server in a Python environment; correct any Evennia version-specific integration issues.
2. Expand CWN conformance using shared `data/rules/` without forking rules.
3. Implement a real, optional LLM provider behind the validated intent boundary.
4. Persist/reconcile Mesa social simulation through authoritative game-world handlers.
5. Add multiplayer end-to-end coverage and server-restart persistence tests.

## Implementation scaffold and commands

## Quick start

Requires Python 3.12+ and a compatible Evennia release.

```sh
cd mud
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
evennia migrate
evennia start
```

Use Evennia's browser client at http://localhost:4001 or a telnet client at localhost:4000. Create two separate accounts to test concurrent presence. **Not validated on a running Evennia server in this PR.** Evennia owns durable character/room state; the game setup hook seeds three connected Helsinki rooms once.

Commands: `look`, `say`, `north` / `south` / exits, `sheet`, `check <skill>=<difficulty>`, `supplies`, `scavenge`, `unsa`, `faction`, `talk <npc>`. Standard Evennia multiplayer communication and connection commands remain available.

## Architecture contract

- `server/`, `commands/`, `typeclasses/`, `world/`: **Evennia only**; persists authoritative rooms, characters and faction inventory.
- `systems/cwn.py`: a **small verified CWN skill-check slice** (2d6 + skill + attribute modifier against difficulty), not a complete CWN implementation. CWN's remaining character creation, combat, hacking, equipment and progression are future work.
- `systems/agents.py`: bounded, provider-neutral Concordia-*style* narration and validated intents; no dependence on Concordia internals and no LLM controlling player characters.
- `systems/simulation.py`: optional Mesa resource agents, emitting proposals only. World mutations must be applied separately by validated Evennia code.
- `world/seed.py`: starter Helsinki, UNSA safehouse and NPC. The Noösphere / ideology system is deferred as an optional overlay.

**Authority:** Never treat LLM prose or Mesa events as CWN rolls or inventory mutations. Players choose actions. The MUD and Godot share **specification and canon**, not runtime classes. MUD agents must read `mud/AGENTS.md` before changing code.

## Current scope

This PR provides an isolated playable-text vertical-slice scaffold and unit-tested pure mechanics/contracts. Survival, GM, NPC and Mesa integration are intentionally minimal, not a claim of full #946 acceptance. The first faction is UNSA; rogue factions and player-founded organizations come later.
