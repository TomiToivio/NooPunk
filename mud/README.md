# NoöPunk MUD

A **second game** in the NoöPunk universe: persistent, text-only, multiplayer. Python. It shares the canon and
the CWN rules with NoöPunk Godot and nothing else — no scenes, no assets, no runtime.

Authority: [`docs/design/ADR_946_NOPUNK_MUD_BOUNDARY.md`](../docs/design/ADR_946_NOPUNK_MUD_BOUNDARY.md),
issue #946.

## Which game am I in?

| | NoöPunk Godot | NoöPunk MUD |
|---|---|---|
| Where | repository root (`project.godot`, `scenes/`, `godot/`) | `mud/` |
| Runtime | Godot 4 | Python (Evennia will host it) |
| Interface | graphical | text commands |
| Players | single player | persistent multiplayer |
| Shared | `data/rules/`, `data/world/`, canon documents | the same files, **read-only** |

Editing a `.gd` file means you are in the Godot game. Editing a `.py` file under `mud/` means you are in the
MUD. Neither may import the other; `tests/test_mud_core.py` fails if that changes.

## Run the core

The platform-neutral core runs today, without Evennia or Mesa installed:

```bash
cd mud
python -m pytest tests -q
```

## What exists

| Module | Responsibility |
|---|---|
| `nopunk_mud/rules_contract.py` | the shared CWN facts (difficulties, untrained modifier, bounds) and the `RulesEngine` protocol the host implements |
| `nopunk_mud/world_state.py` | the authoritative world: rooms, characters, resources, UNSA faction, validated events, JSON persistence and an event log |
| `nopunk_mud/llm_gateway.py` | agents return **proposals**; forbidden intents are refused; a deterministic fallback runs with no provider |
| `nopunk_mud/sim_bridge.py` | simulations emit `SimEvent`s; `reconcile()` applies them as clamped world events |

## What does not exist yet (milestones 2–7 of #946)

Evennia bootstrap, the text command set, the browser client, the Concordia-style GM and NPCs wired to a real
provider, Mesa as an actual dependency, and the multiplayer integration test. The core above is what those
will host — which is why it was built first and tested without them.
