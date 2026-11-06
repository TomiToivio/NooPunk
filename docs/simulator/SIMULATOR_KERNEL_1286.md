# The simulator kernel (#1286, work package 1)

> **Status: work package 1.** `src/social_sim/` is a standalone simulator: no player, no CWN, no game engine, no RPG
> import. It runs from Python over synthetic fixtures, with a step clock, seeded rules, snapshots and replay. It
> implements nothing from the AI26 adapter (work package 2) and no experiment (work package 4).

**Read with:** [boundary and contracts](BOUNDARY_AND_CONTRACTS_1286.md) · [#1286](https://github.com/TomiToivio/NooPunk/issues/1286)

## What is in the kernel

| concept | class | what the kernel enforces |
|---|---|---|
| actor | `Actor` | an id; `ActorKind.INDIVIDUAL` or `ORGANIZATION`; `affiliation` must name an **organization**; resources may not be negative; attributes are simulation variables, never RPG tags |
| social tie | `SocialEdge` | typed relation, `since_step`, provenance; both endpoints must exist |
| communication | `CommunicationEdge` | who spoke to whom, at which step, on which channel, with provenance |
| event | `Event` | step, sequence, kind, actor, target, **the rule that produced it**, the inputs it read, payload, provenance; a derived `event_id` |
| provenance | `Provenance` | an `Origin` — `observed`, `inferred`, `synthesized`, `simulated` — plus source, method, uncertainty and review status |
| run | `Simulation` | population validation, `run(steps, rule=…)`, `digest()`, `snapshot()`, `from_snapshot()` |

## Determinism, and why it is per step

Each step's pseudo-random generator is seeded from `(seed, step, rule)`. Two consequences matter:

* a run of ten steps and two runs of five produce **the same** stream, so a resumed save equals an uninterrupted one;
* the snapshot needs **no generator state**, so replay cannot drift when Python's RNG implementation changes across
  versions.

`digest()` hashes the event stream; `from_snapshot()` refuses a document whose version or digest does not match, rather
than repairing it. A tampered snapshot is a bug, not an input.

## The one transition rule, and its assumption

`noop` does nothing. `broadcast` makes **one** message per step: the speaker is chosen uniformly among actors with at
least one outgoing tie, and the listener uniformly among that speaker's targets.

That is an *assumption for the kernel to have a transition at all*, stated in the code so a reader can disagree with it.
It is not derived from Laclau and Mouffe, and it is not a claim about how discourse works. A scenario supplies its own
rule and documents it; a rule name outside the registry is refused, so a run cannot cite behaviour that does not exist.

## What the acceptance tests cover

`tests/test_social_sim_kernel_1286.py` — **25 tests**, mapped to the issue's conditions:

| condition | test |
|---|---|
| fixed seeds reproduce the stream and hash | same seed → same digest; different seed → different digest |
| resumed run equals continuous run | 10 steps vs 5 + 5 |
| snapshot round trip | restore, continue, compare digests |
| a tampered or wrong-version snapshot is refused | digest mismatch; `kernel_version: 99` |
| temporal ordering | `(step, sequence)` is sorted |
| no fabricated evidence | every event cites its rule and an input; unknown rule refused; an event claiming `observed` origin is refused |
| organization/member distinction | an affiliation must name an organization; the two actor kinds stay distinct |
| isolated actors | allowed, kept, and never chosen as speakers |
| empty input | an empty population runs and produces nothing |
| four origins kept apart | each survives a JSON round trip; a record without an origin is refused |
| modest-N benchmark | 200 actors × 100 steps under 5 s, no LLM call |
| no RPG dependency | the kernel source contains no import from `rules`, `world`, `console`, `simulation`, Evennia or Godot |

## Deliberately absent

* **The AI26 adapter** (work package 2): nothing here reads a canonical record. Mapping and rejection rules are in the
  boundary document, not in the kernel.
* **Behavioural rules beyond the baseline** (work package 3): influence, coalition and institutional response are
  assumptions that need their own rationale and parameters.
* **Experiments, exports, metrics, visualization** (work packages 4–6).
* **The integration seam** (work package 7): a simulation event and an RPG turn are still unrelated, on purpose, and the
  seam will be a documented translation rather than a shared module.

## A note on the duplication this creates

NoöPunk now holds two event models: `src/simulation/` for the RPG-adjacent world simulation, and `src/social_sim/` for
this. That is the cost of the scope rule and it is recorded in the boundary page. The kernel keeps its own event record
precisely so that research runs cannot acquire RPG semantics by accident; the seam, when it is written, is where the two
are reconciled deliberately.
