# NoöPunk simulation core (Phase B)

> **Status: implemented infrastructure. No game rules.**
>
> This is Phase B of [issue #40](https://github.com/TomiToivio/NooPunk/issues/40),
> the deterministic core described in
> [`SIMULATION_ARCHITECTURE_SPEC.md`](SIMULATION_ARCHITECTURE_SPEC.md) §4 and §12.
> It contains **no rules, mechanics, factions, institutions, or setting content**.
> Per `AGENTS.md` §1/§4 those remain author-specified, and the module boundaries
> here are arranged so that implementing them later cannot quietly invent them.

## What it is

One shared world state, derived entirely from an append-only event log. The
tabletop game, Godot and Concordia are intended to be views over this same log
(#40 §1); this directory is the part of that system which is specified enough to
build today.

```text
event log  ──reduce──▶  world state
    │                        │
    │                        └──▶ public communications ──▶ (later) LaclauGPT
    └──▶ branches (counterfactual runs sharing a prefix)
```

## Modules

| File | Owns |
|---|---|
| `events.py` | The canonical event envelope and the two rules that make the log trustworthy |
| `sqlite_store.py` | The append-only SQLite log: idempotent append, canonical ordering, export guard |
| `world_state.py` | The deterministic reducer: `state = reduce(events)` |
| `engine.py` | Turn loop, run identity, branching, and the marked fixture vocabulary |

## The two rules that matter most

Both come from the specification and are enforced in code rather than left to
callers:

1. **Ordering is `turn`, never `timestamp`.** A timestamp is recorded for the
   record but is not an ordering key. Timestamps collide, drift, and are not
   reproducible, so a reducer that ordered by them could not replay identically.
2. **`source` and `synthetic` are set by the emitting boundary, not the actor.**
   An LLM agent cannot emit an event claiming to be tabletop-sourced or
   non-synthetic. `synthetic` is never even a parameter of `Simulation.emit`.

## Properties the tests execute

`tests/test_issue40_simulation_core.py` (43 tests) demonstrates rather than asserts:

- state is exactly the reduction of the log — there is no way to write state
  directly, so log and state cannot disagree;
- replays are byte-identical, and a branch from a prefix is identical to its parent
  at that point (run identity excepted, which must differ);
- contradictory timestamps do not affect order;
- appends are idempotent, and the log is verified append-only;
- a synthetic run cannot be exported as empirical data (`list_exchanges_for_export`
  raises), which is the structural half of spec §5;
- the reducer **does not compute any derived quantity** — a test fails the build if
  words like legitimacy, cohesion, power or influence appear in reduced state;
- an unknown `action_type` is kept as history and creates no relation, so no
  canonical action vocabulary is required.

## What is deliberately absent

- **No social mechanics.** Legitimacy, cohesion, reach, institutional power and
  friends are DEFER-9; storing one of them *is* inventing a mechanic.
- **No entity-kind or relation-type enumeration.** The proposed vocabulary from #40
  is unconfirmed (DEFER-1/DEFER-2), so `kind` and `relation` are open strings.
- **No graph/assemblage layer yet.** Assemblages are DEFER-7 territory.
- **No Concordia integration.** That is Phase C and depends on DEFER-6.

## Fixture vocabulary is marked as such

`engine.fixture_id()` prefixes ids with `fixture:`, and `FIXTURE_RELATIONS` is
labelled non-canonical in code and pinned by a test. Nothing in this directory
should be read as setting material the author has specified.

## Running it

```bash
python -m unittest tests.test_issue40_simulation_core -v
```

```python
import sys; sys.path.insert(0, "src")
from simulation import Simulation, connect, append, list_events

sim = Simulation(simulation_id="demo")
sim.emit(actor="fixture:resident-a", action_type="communicate", content="hello")
state = sim.state
print(state.as_dict()["public_communications"])
```
