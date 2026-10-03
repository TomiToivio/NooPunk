# Issue #60: persistent test-session milestone

The current prototype is **NoöPunk: Eclipse Phase 2E homebrew / Concordia
RPG-Simulation**, in the alternate **20XX / pre-Fall / Earth intact** continuity.

`concordia_runtime.ep2_session.EP2Session` wraps the existing EP2 rules adapter
with SQLite character state, trusted GM-authored action offers, seeded tests and
an ordered event log. Agents choose IDs from `legal_actions(actor)` and receive
committed results through their `observe(text)` method. This duck-typed seam can
connect Concordia entities; it does not instantiate Concordia or call Ollama.

```python
from concordia_runtime.ep2_session import EP2Session
from eclipse_phase_homebrew import EP2Character, EP2PoolState

session = EP2Session("session.sqlite", seed=23)
session.add_character("player", EP2Character("noncanonical fixture", skills={"Infosec": 60}), EP2PoolState())
session.offer_action("player", "mesh_test", {"skill": "Infosec"})
event = session.resolve("player", "mesh_test")
print(event)
session.close()
```

Creation is performed once; reopening the same path restores the saved state.
Use one session writer per database. The database contains potentially sensitive
agent memories and is runtime data, not a file to commit. World metadata is a
reserved persisted dictionary; automatic world effects remain unimplemented.

Validation: `python -m unittest discover -s tests -p 'test*ep2*.py'`.
Tests exercise agent observation, resource spending, rejected actions, save/load
and equivalence of resumed and uninterrupted random sequences.

Provenance: written locally for #60 on 2026-10-03, with no imported datasets or
external code. It calls the EP-derived adapter documented in
[EP2_HOME_BREW_SOURCES.md](EP2_HOME_BREW_SOURCES.md). Treat this integrated
homebrew adapter under the same noncommercial attribution/ShareAlike boundary
as [the existing EP prototype](../licenses/ECLIPSE_PHASE_HOMEBREW.md).

Remaining: actual Concordia/Ollama orchestration, CLI scenario, private agent
memory, opposed checks, health/stress/combat, inventory, full mesh and social
world effects, and playtesting. Keep the umbrella issue open.
