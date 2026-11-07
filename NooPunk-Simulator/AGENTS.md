# Agent rules for NoöPunk Simulator

The root [`AGENTS.md`](../AGENTS.md) applies; this file is the local contract for simulator work.

## One simulator, and it already exists

`src/social_sim/` is canonical (#1294): `kernel.py` (WP1) and `ai26.py` (WP2), with
`docs/simulator/` and 66 tests. Do **not** add a second event store, reducer, game loop or "engine"
package, and do not rebuild the AI26 adapter. `src/simulation/ai26_*.py` is an earlier slice kept for
reference, not a place to extend. Code moves into this directory at stage P3/P4 behind a compatibility
package, not before.

## What the simulator may depend on

The kernel and the adapter import the standard library and each other — no `rules`, no `world`, no
`console`, no `simulation`, no Evennia, no Godot, no provider client.
`tests/test_social_sim_kernel_1286.py` fails if that changes. Reuse the shared tag/graph vocabulary by
adapter ([contract](../docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md)); never import RPG semantics
into a research run.

## Scientific discipline

* **Four material classes stay apart** — `observed`, `inferred`, `synthesized`, `simulated`. Evidence spans
  from a canonical record are `observed`; analysis objects and relations are `inferred`; scenario
  inventions are `synthesized`; rule output is `simulated`. A round trip that loses the distinction is a bug.
* **No relation from co-occurrence.** Frequency and semantic similarity establish nothing on their own
  (`THEORY.md`); only explicitly stated relations and equivalence/difference chains enter a simulation.
* **No real person as an unconsenting agent.** Analysis labels may denote real people; synthetic
  stand-ins are a scenario decision, and the adapter creates no actor.
* **Rules are assumptions.** Every transition rule is documented, parameterised, seeded and traceable to
  the inputs it read. No LLM in the loop by default; an LLM rule needs a hypothesis, fixed prompts, seeds
  and reviewable logs.
* **Output is not data.** Never write simulation output over LaclauGPT data, and never present it as
  observation.

## Methodological attribution

The Phase 1 paper and `THEORY.md` are authoritative for the discourse analysis and are not modified here.
Phase 1 does not supply a simulation engine, and nothing in this directory may claim it does.

## Tests

`unittest`, never bare pytest-style functions: CI runs `python -m unittest discover -s tests` and installs
no pytest. Synthetic fixtures only; no corpus data and no real person in a test.
