# The AI26 research simulator (#1286, work package 1)

> **Status: work package 1, one simulator.** `src/simulation/ai26_research.py` runs a synthetic population over a fixed
> number of turns with a seed, and exports graphs, events and a replay digest. `src/simulation/provenance.py` carries the
> four origins the issue requires. No player, no CWN, no engine, no LLM call, and no RPG rule module in the import graph.

**Read with:** [boundary and contracts](BOUNDARY_AND_CONTRACTS_1286.md) · [#1286](https://github.com/TomiToivio/NooPunk/issues/1286)

## What the simulator is

A **null model**: one message per turn between two individuals, chosen by a seeded generator, over a roster of synthetic
individuals and the organizations they affiliate to. Messages are neutral synthetic tokens —
`synthetic-neutral-message-0007` — and **not** inferred discourse articulations. Nothing is persuaded, nothing is scored,
and no concept from the AI26 paper is turned into a behavioural law.

That is deliberately dull. It exists so the plumbing the issue asks for — seeded determinism, graph integrity, replay,
provenance, exports — is tested before any claim is made about behaviour.

## What is enforced

| condition | how |
|---|---|
| actors are never real people | `actor_id` must start with `synthetic:` |
| individuals and organizations stay distinct | `kind` is `individual` or `organization`; only individuals may hold an affiliation |
| no dangling edges | every edge endpoint is checked against the roster; a mismatch raises |
| no silently dropped actors | actors who never communicate appear in `summary.isolated_actors` |
| replay is exact | content-derived `event_id`s and a `replay_digest`; `verify_replay()` recomputes and compares, and a tampered event fails it |
| the export cannot pass as data | `scientific_status: hypothetical_null_model_not_empirical_finding`, and the run id is prefixed `ai26-synthetic:` |
| provenance is typed | `provenance.origin`, `.source`, `.method`, `.uncertainty` — a record, not a string |

## The four origins

`src/simulation/provenance.py` defines `Origin` — `observed`, `inferred`, `synthesized`, `simulated` — and a `Provenance`
record carrying source, method, uncertainty and the AI26 review status. It is small on purpose: it records and refuses,
and interprets nothing.

Every actor carries an origin, and **an actor may be `synthesized` or `inferred` but never `observed`**: an actor is a
stand-in, and letting the label say "observed" is how a synthetic person would end up exported as if they were in the
corpus. The export counts all four origins, so a reader sees at a glance that the roster is synthetic and the run is
simulated.

## Determinism

Seeded `random.Random(seed)`, an ordered roster, and content-derived event ids: the same roster, seed and turn count
produce byte-identical exports, and `verify_replay()` proves it after a round trip through JSON. Reversing the input
roster does not change the run — the test that catches an accidental dependence on input order.

## Tests

`tests/test_ai26_research_simulation.py` — **12 tests**: seeded runs byte-identical, roster order irrelevant, a different
seed changes the stream, negative turns refused, export/replay/provenance, tamper detection, origins distinguishable and
counted, an inferred actor allowed and an observed one refused, provenance round trip, no game or LLM runtime imports, and
the CLI.

## Consolidation note

Two kernels were written for this work package in the same hour: a standalone `src/social_sim/` package and this module
on the generic event envelope. **The standalone one was retired.** Its unique piece — the four-origin provenance
contract — was folded into `src/simulation/provenance.py` and is carried by this simulator, so there is one simulator and
one event model rather than two of each. The boundary page records the decision and its cost.

## Deliberately absent

The AI26 read-only adapter (WP2), behavioural rules beyond the null model (WP3), the contestation experiment (WP4),
metrics and visualization (WP5–6), and the RPG integration seam (WP7). None is claimed here.
