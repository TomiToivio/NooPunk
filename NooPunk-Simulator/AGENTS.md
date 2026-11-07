# AUTHOR-ONLY PAPER: NON-NEGOTIABLE READ-ONLY RULE (#1309)

**`NooPunk-Simulator/Paper/` belongs exclusively to Tomi. ALL AI agents MUST treat it as READ ONLY.** Agents may read and cite Tomi's serious Social Science, fictional world and Game Design drafts, but **must never add, create, edit, rewrite, format, rename, move, delete, sync, replace, or generate files anywhere under `NooPunk-Simulator/Paper/`**. This includes README files, accidental lint/format fixes, scripts, automations, PR merges and refactors. No autonomous write is authorized. Only Tomi directly authors these drafts.

- **Agents write derived interpretations, design notes and human-readable simulation rules in `NooPunk-Simulator/Rulebook/`**, not in Paper.
- Implement the Rulebook in **`NooPunk-Simulator/Code/`**, reusing the existing canonical `src/social_sim/` implementation until migration is explicitly planned/tested. **`NooPunk-Simulator/Graphs/`** is the home for the three Simulator graph definitions and fixtures.
- The three Simulator graph views are **Social, Ideology and Physical**. Ideology is a Simulator discourse projection, not automatically a new family in the existing shared RPG graph contract. Follow [#1309](https://github.com/TomiToivio/NooPunk/issues/1309), [#1308](https://github.com/TomiToivio/NooPunk/issues/1308), and [shared contract](../docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md).
- When Tomi's Paper disagrees with agent-written Rulebook/code, record the discrepancy and ask Tomi to resolve authorship decisions; **never modify Paper to reconcile them**. No bulk LaclauGPT imports or duplicate simulator kernels.

---

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
