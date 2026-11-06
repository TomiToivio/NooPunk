# LaclauGPT social-science simulator — contracts, boundary and MVP (#1286)

> **Status: active standalone simulator MVP. No NoöPunk RPG work.** This document implements the
> audit/contracts and the first runnable kernel for #1286. It is not a new game rulebook, not the CWN
> RPG, and not a claim that Laclau and Mouffe's concepts are causal laws.
>
> **Authority:** [LaclauGPT AI26 paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md),
> [THEORY.md](https://github.com/TomiToivio/LaclauGPT/blob/main/THEORY.md), and the
> [LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis) canonical record /
> evidence contracts. The paper and methodology are not modified here.
>
> **Freeze:** no RPG, CWN/SWN/AWN/WWN, campaign, tag-as-RPG-rule, story-engine or game-adapter file is
> changed by this work. The preserved RPG is a future optional interface, not part of this delivery.

## 1. Audit: what exists, and what this adds

| Existing thing | What it is | Use in #1286 |
| --- | --- | --- |
| `src/simulation/` (#40) | NoöPunk's deterministic **game/world** event log, reducer, SQLite replay and branch support | Inspected for conventions; **not imported**. It models game events and world state, not AI26 discourse inputs or synthetic actor behavior. |
| `src/rules/`, CWN/SWN/AWN, `mud/`, `godot/`, `strategy_game/`, campaign/tag files | The preserved RPG and its adapters | **Out of scope. Not imported. No changes.** |
| `LaclauGPT-Data-Analysis` canonical record | Pydantic-backed `CanonicalRecord` with `source_url`, raw/source/content, evidence, `analysis`, `review`, provenance | Read-only schema source for the adapter. The package is not copied or modified. |
| `data/scenarios/lakkahaltia/` | RPG case data | Out of scope; not read. |
| AI26 exports | JSON-compatible canonical records with analysis objects | The simulator's only empirical input path, and only when provenance/uncertainty are explicit. |

**Duplication ledger:** there is no existing AI26 social-science simulator. The closest existing
engine (`src/simulation`) is a game-event log and explicitly has no social/behavioral rules. This
package is therefore a new concern, not a second implementation of it. It does not import
`src.simulation`, because reusing a game-event envelope with different semantics would blur observed
and simulated material and force RPG-shaped changes. A future consolidation can wrap one, but only
after the contracts stay separate.

**Unresolved modelling choices recorded rather than decided:** which AI26 discourse fields are
comparable across codebooks, how to calibrate initial dispositions, whether organizations should have
their own message-selection rules, and how to evaluate simulated against empirical distributions
without over-claiming. These are in §8.

## 2. Boundary: observed, inferred, synthesized, simulated

Every record carries a `Provenance` with exactly one material class:

| Class | Meaning | Example |
| --- | --- | --- |
| `observed` | Source material captured from a platform | A post's text and URL |
| `inferred` | An AI26 interpretation of source material | A signifier, formation, equivalence chain |
| `synthesized` | A fixture or researcher-authored initial condition | A synthetic actor's starting disposition |
| `simulated` | Produced by this package during a run | A communication event, affiliation, institutional response |

Rules:

1. An AI26 claim is **inferred**, never observed. The export's `source_url` is retained in its
   `source_id`, and its review status/flags survive.
2. A synthetic actor's disposition is a **simulation variable**, not an empirical measurement and not
   an RPG tag.
3. No export may turn a simulated event into observed data. The run manifest says synthetic.
4. An incomplete or collection-only record is rejected rather than filled with guesses.

## 3. AI26 adapter contract

`src/social_science/adapter.py` consumes a JSON-compatible canonical record.

**Required:** `source_url` (non-empty canonical identity), `schema_version`, and an `analysis` object.
A record with no analysis is collection-only and is refused.

**Claims:** from `analysis.signifiers`, `nodal_points`, `formations`, `discourses`, `imaginaries`,
`us`, `them`, `frontier`, `themes`. A string is a label-only claim; an object may supply
`label`/`text`/`name`, `kind`, and `confidence`/`uncertainty` in `[0, 1]`. ID = stable slug of category
and label. Duplicate labels in one category are one claim.

**Articulations:** only explicit `equivalence_chains` / `difference_chains` (and explicit
`relations` of those types) become `Articulation` records. **Raw co-occurrence is not a relation.**
Unknown endpoints are skipped with a warning, not invented.

**Preserved:** `review.status`, `review.flags`, `analysis.uncertainty`, `analysis.abstentions`, and
warnings. `apply_to(simulation)` only adds missing claims/articulations; it does not mutate the export.

**Not represented:** raw text, embeddings, model runs, codebook internals and platform metadata. The
simulator does not need them and must not pretend they are behavioral variables.

## 4. Kernel contract

`src/social_science/engine.py`:

| Piece | Behaviour |
| --- | --- |
| `Actor` | `individual` or `organization`; id, label, affiliation, roles, resources, attention, disposition, active; provenance |
| `Claim` | demand/signifier/project; id, label, kind, owner, provenance, uncertainty |
| `Articulation` | explicit equivalence/difference between two claims |
| `SocialEdge` | typed, time-indexed source→target relation |
| `CommunicationEdge` | public/private communication, time-indexed |
| `SimEvent` | append-only event with actor, target, payload, rule and provenance |
| `SocialScienceSimulation` | seeded turn loop, event log, snapshot/restore, digest |

**Determinism:** `random.Random(config.seed)`; actors, claims and targets are processed in sorted
order; event ids are sequential per turn; snapshot includes RNG state; `digest()` hashes the snapshot
without RNG state. External LLMs are not called. If an LLM is added later, its prompts/seeds/logs must
be explicit and determinism limits documented.

## 5. Behavioral assumptions (the whole MVP)

These are **assumptions**, not findings. `DEFAULT_RULES` is exported with every run.

| Rule | Assumption | Parameter |
| --- | --- | --- |
| Communication | An active actor with an outgoing tie may send one claim per turn | `communication_probability` |
| Abstention | No target, failed draw, or abstention draw → `abstain`, never a fabricated message | `abstention_probability` |
| Influence | Receiver's disposition moves toward the claim by the sender's stance sign | `influence_rate` |
| Attention | Receiver attention rises after communication and decays each turn | `attention_decay` |
| Coalition | Crossing the disposition threshold records one simulated coalition edge | `coalition_threshold` |
| Contest | Opposite-sign positions beyond threshold record a contest event | `coalition_threshold` |
| Institution | An organization with attention above threshold records one response per turn | `institutional_threshold` |

No rule uses “hegemony”, “populism” or “empty signifier” as a numeric score. Those remain analytical
interpretations requiring relational evidence.

## 6. Run, experiment and export

```bash
PYTHONPATH=src python3.11 -m social_science --seed 7 --turns 8
PYTHONPATH=src python3.11 -m social_science --seed 7 --turns 8 --intervention --out /tmp/run.json
```

The synthetic fixture has six residents, two civic organizations and three claims. `--intervention`
raises one organization's attention and adds one bridge tie. It is a **control/intervention fixture**,
not a policy recommendation.

`export_run()` / `write_run()` produce:

- run manifest: seed, turns, config, rule text, digest, provenance note;
- actors, claims, articulations, social edges, communication edges;
- every event with its rule and provenance;
- exploratory metrics (graph density/components/degree, event counts, disposition summaries).

Metrics are descriptions of the synthetic run. They are not predictive validity, hegemony scores or
empirical findings.

**Baseline benchmark** (local, Python 3.11, 200 synthetic actors in a ring, 3 claims, 10 turns):
**0.29 s**, **3,017 KiB peak traced allocation**, **4,365 events**. This is a scaling sanity check,
not a performance guarantee; run `benchmark()` on the target host for a comparable number.

## 7. Tests and anti-scope checks

`tests/test_social_science_1286.py` covers:

- same seed → same events and digest; different seed → different run;
- snapshot/restore and continued replay;
- unique event ids and monotonic time;
- edges reference known actors; articulations reference known claims;
- actor/organization distinction; isolated actor abstains; empty claims abstain;
- adapter accepts synthetic canonical fixtures, rejects collection-only/missing-identity records,
  keeps uncertainty/review, does not invent co-occurrence relations, and is idempotent;
- exports label synthesized/simulated material and the manifest says synthetic;
- CLI runs with no RPG, Evennia or LLM;
- metrics are explicitly exploratory.

**Scope test (manual/PR review):** the diff must touch only `src/social_science/`,
`docs/simulation/`, `docs/DOCUMENT_REGISTER.md` and its tests. Any RPG path is a failed PR.

## 8. Unresolved modelling choices

1. Which AI26 fields are comparable across codebooks, and which need a codebook-specific adapter.
2. How initial dispositions are calibrated, and whether calibration is even possible without
   over-fitting to one corpus.
3. Whether organizations select messages differently from individuals, and whether that is one rule
   or several documented rules.
4. How to compare simulated distributions to empirical ones ethically and statistically, and when
   that comparison would be misleading.
5. How to represent contradictory articulations without collapsing them into one graph.
6. Whether a later CWN adapter needs only passive event subscription or also command injection.

## 9. Future CWN seam — document only, not implemented

A later optional adapter could subscribe to simulator events and present them to a GM/player, while
CWN independently resolves any RPG action. This document does **not** implement that adapter, does not
import RPG code, and does not change a rule. The simulator's events are already a neutral, versioned
trace; the seam should be a one-way reader first, then a reviewed command interface.

## 10. Related

- [#1286](https://github.com/TomiToivio/NooPunk/issues/1286) — this tracker.
- [LaclauGPT AI26 paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md)
- [THEORY.md](https://github.com/TomiToivio/LaclauGPT/blob/main/THEORY.md)
- [LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis)
- `src/simulation/` — the earlier game-event core, **not imported** and not changed.
