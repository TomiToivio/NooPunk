> **Superseded (2026-11-07):** the canonical simulator is now `src/social_sim/` — the kernel in
> [`../simulator/SIMULATOR_KERNEL_1286.md`](../simulator/SIMULATOR_KERNEL_1286.md) and the read-only AI26 adapter in
> [`../simulator/AI26_ADAPTER_1286.md`](../simulator/AI26_ADAPTER_1286.md). This page and `src/simulation/ai26_research.py`
> describe the earlier null-model slice built on the shared event envelope; it still runs and is still tested, but it is
> **not** the simulator to extend, and the two must not both acquire features. Delete this module once the canonical
> path covers its demo, so that NoöPunk holds one simulator rather than two.

# AI26 research simulator: first implementation slice (#1286)

**Status:** synthetic null-model prototype. Not an RPG. Not empirical AI26 research results. Not a validated model of persuasion, populism, hegemony or social change.

## Scientific authority and boundaries

- [LaclauGPT AI26 scientific paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md) and [THEORY.md](https://github.com/TomiToivio/LaclauGPT/blob/main/THEORY.md) govern discourse-theoretical interpretation.
- [LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis) is the **canonical AI26 analysis implementation**, not a simulation engine. It produces preliminary, evidence-linked interpretations subject to human verification.
- The simulator must not claim that the AI26 theory establishes behavioral transition laws. Nothing about the model's random communication events implies that a nodal point, empty/floating signifier, antagonism, equivalence, ideological formation or hegemony has been empirically detected.
- **No real-person simulation:** synthetic actor IDs and fictional organization placeholders only. The output marks all records `provenance=simulated`.
- **RPG freeze:** no CWN/SWN/AWN or other RPG system is called or changed. This is a research kernel demonstration only.

## Duplication audit and implementation choice

The NoöPunk repository **already contains** `src/simulation/events.py`, `engine.py`, `world_state.py`, `sqlite_store.py`. It has deterministic event IDs, append-only log representation, replay and relational-state reduction. **Do not reimplement them.** `src/world/graphs.py` and `strategy_game/` contain RPG-oriented graph and political game systems. They are frozen, not repurposed.

This slice adds only `src/simulation/ai26_research.py`, a research-specific experiment *built on* `Event.create`, `next_occurrence`, `reduce_events` and `replay_digest`. It derives two graph projections from the existing event stream instead of creating a second authoritative graph store.

## Current synthetic data contract

| Field | Definition | Research limitation |
| --- | --- | --- |
| `ResearchActor.actor_id` | Stable `synthetic:` identifier | No mapping to real people |
| `kind` | `individual` or `organization` | Synthetic type, not automatic political subject |
| `affiliation` | Optional person → organization declaration | Relationship chosen by fixture author |
| `Event(action_type='relate')` | Declared membership edge | No inference from language |
| `Event(action_type='communicate')` | Directed synthetic encounter with neutral token | No persuasion or semantic interpretation |
| `turn` and `timestamp` | Discrete, seeded deterministic time | Artificial calendar; not source observation |
| `graphs.social_edges` | Directed membership edges | No social power metric |
| `graphs.communication_edges` | Directed, time-stamped communications | Network topology ≠ ideological formation |
| `replay_digest` | Derived from existing canonical reducer | Verifies reconstruction, not scientific validity |

## Run it (standard library only)

From a checkout with Python 3.11+, in the root directory:

```bash
PYTHONPATH=src python -m simulation.ai26_research \
  --population 100 --turns 250 --seed 42 \
  --output /tmp/ai26-synthetic-demo.json
python -m pytest -q tests/test_ai26_research_simulation.py
```

The JSON contains configuration, all replayable events, typed/temporal social and communication graph edge lists, actors including isolates, and summary counts. Repeating an identical run with identical input yields identical bytes. Its messages are explicitly labeled *synthetic-neutral-message*; they are not research observations.

## Empirical input boundary: proposed, NOT implemented here

The next incremental task is to inspect the **current** LaclauGPT-Data-Analysis AI26 canonical record objects, analysis output fields, source citations, review status and schema evolution. Map only validated source-evidence-backed fields into a **separate immutable observed/inferred input type**, never straight into synthetic `Event` fields.

Required before any AI26 ingestion:
1. Validate the actual versioned AI26 canonical schema rather than importing EP24 compatibility columns.
2. Preserve record/document IDs, provenance, source spans, coding versions, confidence/abstentions and human-review flags.
3. Distinguish `observed` / `model_inferred_unverified` / `human_reviewed` / `synthetic_assumption` / `simulated`.
4. Reject unverified inference as behavioral ground truth; require explicit researcher-approved mapping to scenario assumptions.
5. Maintain a read-only adapter; never write into source LaclauGPT collections.

## Research roadmap (not implemented by this slice)

- Hypothesis-driven transition mechanisms for agents, organizations, communication diffusion and coalition change with explicit sensitivity parameters and null baselines.
- Carefully named discourse event types with evidence status and source attribution, strictly separate from ordinary message co-occurrence.
- Replicate simulations across seeds, compare with null controls, and report negative/uncertain results. No automated hegemony score.
- Export visualization-compatible networks and manifests plus benchmarking.
- A passive future boundary for the frozen CWN RPG, **only after explicit user reauthorization**.

## Tests and future agents

`tests/test_ai26_research_simulation.py` covers determinism, seed divergence, provenance, actor-organization integrity, graph endpoints, isolated actors, replay and tamper detection. Do not alter RPG code or `AGENTS.md` RPG freeze while expanding the simulator. PR #1286 work must stay independent of the operational LaclauGPT demo.
