# The AI26 adapter (#1286, work package 2)

> **Status: work package 2.** `src/social_sim/ai26.py` is the single read-only door a LaclauGPT AI26
> canonical record comes through on its way into the simulator. It validates the published contract,
> projects the coded discourse into `observed` evidence and `inferred` claims/articulations, and refuses
> anything it cannot carry with its provenance intact. It creates no actor, infers no relation and calls
> no model.

**Read with:** [boundary and contracts](BOUNDARY_AND_CONTRACTS_1286.md) · [kernel](SIMULATOR_KERNEL_1286.md) ·
[AI26 Phase 1 paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md) ·
[THEORY.md](https://github.com/TomiToivio/LaclauGPT/blob/main/THEORY.md) ·
[LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis) ·
[#1286](https://github.com/TomiToivio/NooPunk/issues/1286)

## What it does, and why each part is not optional

| step | what it enforces | why |
|---|---|---|
| **validate** | `schema_version` is exactly `1.2.0`; `source_url` is non-empty; every analysis row resolves a `provenance_id` that exists and carries a `created_at`; every `evidence_id` resolves to an `Evidence` span of *this* record's source with a `quote` or a `ref`; no id is duplicated | a record that cannot name where an interpretation came from is not evidence, it is a claim about evidence |
| **project** | `DiscourseObject` rows → `ImportedClaim`; `relations`, `antagonisms`, `equivalence_chains`, `difference_chains` → `ImportedArticulation`; canonical ids are kept as `native_id` and appear in the simulator ids (`claim:<family>:<object_id>`, `art:<family>:<relation_id>`) | a reader must be able to walk from a simulated bundle back to the record without a lookup table |
| **label** | an evidence span is `Origin.OBSERVED`; a claim or an articulation is `Origin.INFERRED`; nothing here is `SYNTHESIZED` or `SIMULATED` | the issue's four-material contract: an interpretation is not an observation, and neither is simulation output |
| **refuse** | unknown schema version, empty or absent source identity, no `analysis` section, `analysis.status: collection-only`, unresolved or foreign evidence, unresolved provenance, a rejected/superseded review, a duplicate object id, an unplaceable relation endpoint, an articulation with fewer than two endpoints, an analysis that codes nothing | a partial or coerced import is worse than none: it silently becomes synthetic material wearing an empirical label |

Material classes in the export (`AI26Import.to_dict()`):

| class | in the bundle |
|---|---|
| `observed` | `evidence[]` — the quoted or referenced spans of the source text |
| `inferred` | `claims[]`, `articulations[]`, the record's `uncertainty[]` and `abstentions[]` |
| `synthesized` | **absent**: the adapter invents nothing, not even a placeholder actor |
| `simulated` | **absent**: no rule runs here |

## The review policy, stated rather than implied

`review.status`, `reviewer`, `reviewed_at` and `flags` travel with every claim and are repeated at the
top of the bundle. Two states are **refusals**: `REJECTED` and `SUPERSEDED`, on the record and on any
individual object or relation. Everything else (`PROVISIONAL`, `ACCEPTED`, `CANONICAL`, `REVISED`) is
**carried, not enforced** — boundary §7.6 leaves "may an unreviewed statement enter a scenario" to the
researcher, and this adapter does not decide it by silently dropping records. It does say what it sees:
an `ACCEPTED` record with no reviewer or no date produces the warning *"the claim of review cannot be
checked"*, and a record with abstentions produces a warning that none of them was rescaled into a claim.

## What it deliberately does not do

* **No actors.** `analysis.actor_entity_relations`, `entities` and `entity_mentions` are read but not
  imported; a warning records that. An analysis label can denote a real person, and #1286 forbids
  instantiating an unconsenting real person as a simulated agent. Choosing synthetic stand-ins is a
  scenario decision (work package 4), and it happens where a human can see it.
* **No relation from co-occurrence.** Only statements the analysis wrote as a relation or an explicit
  equivalence/difference chain are imported. Two concepts coded in one record are not an articulation,
  and a record with claims but no stated relation imports **claims only** and says so in a warning.
  THEORY.md makes this non-negotiable: frequency and semantic similarity establish nothing by themselves.
* **No coercion of an endpoint.** A relation whose endpoint is not an imported claim (`entity-42`, an
  actor id, a typo) is an error. Coercing it to the nearest label would fabricate a relation.
* **No analysis-engine import and no mutation.** The record is validated structurally against the
  documented contract; `laclaugpt_data_analysis` is not imported, and the input mapping is never
  modified — both are asserted by tests.
* **No network, no provider, no LLM.** The module imports neither `requests` nor a model client.

## Running it

```bash
PYTHONPATH=src python -m social_sim.ai26 --canonical path/to/record.json          # bundle as JSON
PYTHONPATH=src python -m social_sim.ai26 --canonical path/to/record.json --summary # counts, for a human
```

A refusal exits `2` and prints `refused: <reason>` on stderr; a successful import prints a bundle whose
`record_id` is `ai26:<sha256 prefix of the input>` and whose `digest()` is stable across two imports of
the same record.

## Test evidence

`tests/test_social_sim_ai26_1286.py` — **41 tests**, all over synthetic fixtures built inside the file
(no corpus data, no real person):

| suite | tests | what it pins |
|---|---|---|
| `ImportTests` | 10 | a valid record imports claims, explicit articulations and evidence; `observed` evidence never becomes `inferred` and vice versa; provenance method/model/item uncertainty; review carried and dated; abstentions and uncertainty preserved; export round trip; digest and record id stability; the input mapping is not mutated; a path and a mapping agree; an `ACCEPTED` record without a reviewer is flagged |
| `RefusalTests` | 22 | version, missing version, source identity, collection-only, missing analysis, provenance id, provenance timestamp, unresolved evidence, foreign evidence, evidence without quote or ref, claim without evidence, `REJECTED` record, `SUPERSEDED` record, rejected object, duplicate object id, unplaceable relation endpoint, one-member chain, relation without evidence, unresolved provenance id, analysis that codes nothing, coerced family shape, non-JSON |
| `NoInventionTests` | 3 | co-occurrence produces no articulation; only stated relations are imported; actor naming is not imported as an actor |
| `BoundaryTests` | 3 | no RPG/provider/network import, no `Actor` type, the projected material is immutable |
| `CliTests` | 2 | the CLI prints a bundle; it refuses with exit `2` and a reason |
| `TypedMaterialTests` | 1 | the imported rows are the documented types |

## What this does not yet give the simulator

The adapter stops at a validated bundle. It does **not** build a population from it, and #1286 says it
should not: behavioural rules (work package 3), the paired contestation experiment (work package 4),
graph/metric exports (work package 5) and the end-to-end demonstration (work package 6) are where a
bundle becomes a run. The honest sequence is bundle → documented rules → experiment, so that a result
can always be traced back to which claims entered it and which assumptions acted on them.

## Scope check

No file under `src/rules/`, `rulebook/`, `docs/campaign/`, `src/world/`, `src/console/`, `src/godot/`,
`mud/` or `src/simulation/` is touched. The RPG stays frozen: this work package adds one research
module, its tests and this page.
