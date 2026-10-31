# NoöPunk MUD

A **separate, text-based, persistent multiplayer** game built on [Evennia](https://www.evennia.com/), sharing
NoöPunk canon and CWN rules with the Godot game but **no runtime**.

**Status: boundary established (#947), platform-neutral core implemented (#949), Evennia scaffold added (#948).**
The Evennia runtime and multiplayer behaviour have **not** been verified; what is tested today is the core the
server will host — precisely so that "the LLM must not decide" and "the simulation must not write" are
properties with tests rather than intentions.

## The boundary, in one table

| | NoöPunk Godot | NoöPunk MUD (this directory) |
|---|---|---|
| Runtime | Godot 4, `project.godot` at repository root | Python 3, Evennia server |
| Interface | graphical, `scenes/`, `godot/` | text commands, telnet/web client |
| Tests | `godot --headless --script res://godot/tests/run_tests.gd` | Python unittest under `mud/tests/` |
| Entry point | `project.godot` | `mud/server/` (Evennia layout) |
| Dependencies | Godot binary, no Python runtime | `mud/requirements.txt`, `mud/pyproject.toml` |

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


## What exists today

```bash
cd mud
python -m pytest tests -q        # 22 passed
```

| Module | Responsibility |
|---|---|
| `nopunk_mud/rules_contract.py` | the shared CWN facts (difficulty bands, untrained modifier, bounds) read from `data/rules/without_number.json`, a `Check` type, and a `RulesEngine` protocol the host implements |
| `nopunk_mud/world_state.py` | the authoritative world — rooms, characters, items, the **UNSA** faction — with validated events, idempotent ids, JSON persistence and an append-only log |
| `nopunk_mud/llm_gateway.py` | agents return **proposals**; `add_item`, `grant_success`, `teleport` and friends are refused by name; a deterministic fallback runs with no provider |
| `nopunk_mud/sim_bridge.py` | simulations emit `SimEvent`s carrying faction pressure only; deltas are capped at ±3 and refusals are reported, not retried |

The architecture decision behind these is
[`docs/design/ADR_946_NOPUNK_MUD_BOUNDARY.md`](../docs/design/ADR_946_NOPUNK_MUD_BOUNDARY.md).

### Two bugs the tests caught on day one

1. **Rank 0 was treated as untrained.** In Without Number `-1` is untrained and `0` is trained; the first
   version penalised every starting character by −1.
2. **`join` was missing from the event schema**, so no character could enter the world at all.

## Next steps, in order


1. Evennia project skeleton under `mud/` with its own requirements and a smoke test that the server starts
   headless — nothing about game content yet.
2. A CWN character bridge that reads `data/rules/` without copying it.
3. Concordia-style LLM agent orchestration, kept behind an interface so the MUD is playable without it.
4. Mesa-based faction/social simulation, consuming the same canon data.

The four steps above remain unstarted. The core underneath them is not: it is tested, and it is what Evennia
will host.

## Evennia scaffold (PR #948)

A first Evennia project skeleton exists under `mud/` with its own requirements and configuration, so the server
layout is decided before game content is written. **It has not been started or verified in this environment.**
Treat it as a scaffold, not as a running MUD: no multiplayer behaviour, no command set and no browser client
have been exercised.
