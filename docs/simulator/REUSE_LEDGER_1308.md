# Reuse ledger for #1308, slice 1 (SNA) — what to adapt, reference, defer or reject

> **Status: the first deliverable of #1308**, which mandates inventory before importing: *"Record
> `reuse / adapt / reference only / reject` and why; no open-ended repo-wide transplant."*
>
> **Scope of this ledger: slice 1 only** — the social graph and conventional SNA. It does not assess the
> discourse model (slice 2) or the DNA bridge (slice 3) beyond marking them deferred, and it inspects only
> the upstream files that slice 1 could plausibly need.
>
> **Position in the project, after #1310:** this simulator work is **optional infrastructure**, not the
> game. #1310 makes Romppainen's detective interactive fiction the deliverable and keeps the social
> simulation as a small, skippable support module. Nothing here may become a runtime dependency of the
> adventure, and nothing here touches `NooPunk-RPG/`.

**Licence:** `LaclauGPT-Data-Analysis` and `LaclauGPT-Data-Visualization` are both **CC0 1.0 Universal**
(public-domain dedication), verified from each repository's `LICENSE`. Code may be reused without
attribution. Provenance is still recorded here, because an unattributed copy is a maintenance hazard even
when it is legal.

## What NoöPunk already has — the reason most imports are refused

The issue's hardest rule is *"no competing simulator, duplicate tag ontology or competing canonical paper."*
NoöPunk is not empty ground:

| Existing module | What it already provides |
|---|---|
| `src/world/graphs.py` (828 l) | `PhysicalGraph`, `CyberGraph`, **`SocialGraph`** with `SocialNode`, `Relationship`, stable IDs, validation, JSON round-trip and `to_networkx()` |
| `src/world/narrative_tags.py` (412 l) | **`SocialTag`**, `GoalTag`, `ClueTag`, `PersonalityTag`, with `Polarity` and `GoalState` enums |
| `src/social_sim/kernel.py` (460 l) | `Actor`, `ActorKind`, `SocialEdge`, `CommunicationEdge`, `Event`, and — critically — **`Origin` / `Provenance`** (observed / inferred / synthetic separation) |

**Consequence:** slice 1 does **not** need a new graph type, a new node model or a new tag vocabulary. It
needs *metrics over the graph that exists* and a seeded example. Any proposal that adds a second
`SocialGraph` or a parallel tag namespace should be rejected at review.

## The ledger

`reuse` = use the existing NoöPunk module unchanged · `adapt` = port a small part with a test ·
`reference` = read for the idea, write our own · `defer` = out of slice 1 · `reject` = no.

| # | Method / need | Source path | Exact reusable portion | Verdict | Target, dependency and test implications |
|---|---|---|---|---|---|
| 1 | Conventional descriptive SNA | `LaclauGPT-Data-Analysis/src/laclaugpt_data_analysis/sna/metrics.py` (87 l) | `graph_metrics()` — degree, weighted degree, centrality; `community_assignments()` | **ADAPT** | The one genuinely worth porting: 87 lines, pure, no I/O. Land it in a NoöPunk module over `SocialGraph`, with its own `TestCase` asserting known values on a hand-checked 4-node graph. `networkx` becomes an **optional** import guarded like `graphs.py` already does — never a hard dependency of the adventure |
| 2 | Graph construction, temporal slicing | `…/sna/graph.py` (130 l) | `build_graph`, time-slice helpers | **REFERENCE** | NoöPunk already builds and validates `SocialGraph` with stable IDs. Porting this would create the second builder the issue forbids. Read it for the time-slicing idea only |
| 3 | Graph serialization | `…/sna/import_export.py` | JSON import/export | **REJECT** | NoöPunk's graphs already round-trip to JSON; a second serializer is pure duplication |
| 4 | Discourse Network Analysis models | `…/discourse_network/models.py` (181 l), `network.py` (303 l) | statement/event models, projections | **DEFER** (slice 3) | Real candidate for the DNA bridge. Not inspected further until slice 1 ships — the issue forbids inspecting ahead of need |
| 5 | SNA visualisation | `LaclauGPT-Data-Visualization/src/laclaugpt_visualization/sna.py` (384 l) | layouts, graph views | **DEFER** (last) | The issue puts Streamlit last, *after* the underlying slice warrants it, and forbids making the UI a simulator dependency |
| 6 | Canonical social graph | `NooPunk/src/world/graphs.py` | `SocialGraph`, `SocialNode`, `Relationship` | **REUSE IN PLACE** | No change needed to start. If a metric needs an accessor, add it here rather than forking |
| 7 | Social / goal tags | `NooPunk/src/world/narrative_tags.py` | `SocialTag`, `GoalTag` | **REUSE IN PLACE** | Do **not** invent a second tag namespace. New tags, if any, extend this module with the same validation |
| 8 | Provenance and confidence | `NooPunk/src/social_sim/kernel.py` | `Origin`, `Provenance` | **REUSE** | The observed / inferred / synthetic split is exactly what keeps a *synthetic* faction state from being read as empirical fact. Every edge the example creates carries one |
| 9 | Laclau vocabulary — articulation, frontier, demand, equivalence, hegemony | `LaclauGPT/paper/PHASE_1_PAPER.md`, `LaclauGPT/THEORY.md` | Concepts and their evidence limits | **REFERENCE ONLY** | No text imported, no paper edited. Slice 2 writes an **independently authored** Simulation Paper citing sections and pinned revisions. Phase 2 draft is non-canonical context |
| 10 | SNA / DNA prompt files | `LaclauGPT/PROMPT_SNA.md`, `PROMPT_DNA.md` | LLM extraction prompts | **REJECT** | There is no LLM in this simulator's loop. Importing prompts would import the pipeline behind them |
| 11 | Castells, Luhmann | Book-level theory, no repository | Network making, programming, gatekeeping, switching; communications and functional differentiation | **REFERENCE ONLY** | Interpretive assumptions **inspired by** theory, labelled as such. They are **not** SNA metrics, and no coefficient may be presented as derived from them |
| 12 | Historical tiny political simulator | issue #282 | Ideas | **REFERENCE ONLY** | Mined for ideas, explicitly not authoritative over current design |

## Dependency and licence summary

- **networkx** — optional, lazily imported, already the pattern in `src/world/graphs.py`. Metrics must
  degrade honestly when it is absent, not silently return zero.
- **No new heavy dependency** is justified by this ledger. Nothing from the research pipeline — LLM clients,
  storage, distributed execution, ingestion — is imported, and no empirical data is required to run an
  example.
- **Licence: CC0.** No attribution obligation. Provenance recorded anyway.
- **Tests:** every adapted function arrives with a `unittest.TestCase` asserting hand-checked values, per
  the repository rule that a `test_*` module-level function is not collected by CI.

## What slice 1 would then be, minimally

1. `ADAPT` #1 into one small module over the existing `SocialGraph` — a handful of transparent metrics, no
   inference.
2. A **seeded** example with two or three factions, communication and membership edges, and a few
   network-altering turns, printing its event log.
3. Tests for the metrics and for determinism (same seed, same log).
4. The Simulation Paper paragraph that says what the metrics are and, more importantly, what they are not:
   *centrality in this simulation is not political power, and the Castells/Luhmann layer is a game
   assumption, not a measurement.*

That is the whole increment. Ideology arrives in slice 2, and only after slice 1 has been merged or
rejected.
