# Simulator boundary and contracts (#1286, work package 0)

> **Status: work package 0.** This page maps what the LaclauGPT AI26 material actually provides onto what a standalone
> simulator needs, records what already exists in NoöPunk, and lists the modelling choices this phase does **not**
> decide. It changes no RPG file, no rulebook, no campaign content and no canon — the scope rule in #1286 is absolute
> for this phase.

**Read with:** [AI26 Phase 1 paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md) ·
[LaclauGPT THEORY.md](https://github.com/TomiToivio/LaclauGPT/blob/main/THEORY.md) ·
[LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis) ·
[kernel implementation](SIMULATOR_KERNEL_1286.md) · [#1286](https://github.com/TomiToivio/NooPunk/issues/1286)

## 1. The authority chain, and what each link is allowed to decide

| link | decides | this issue may not |
|---|---|---|
| **AI26 paper** | the Laclau–Mouffe vocabulary, Palonen's Formula of Populism, contested signifiers, articulation, frontier, collective subject, sociotechnical imaginary, source-level uncertainty | rewrite the paper or the Phase 1 methodology |
| **THEORY.md** | the evidence contract: frequency and semantic similarity establish nothing on their own; hegemony, equivalence, antagonism, populism and empty signification need relational evidence and corpus-level verification | reinterpret it into a scoring shortcut |
| **LaclauGPT-Data-Analysis** | the technical basis: canonical record contract, evidence-linked analysis output, modular stages, provider-neutral runtime, reproducibility policy | modify the analysis engine, or treat EP24 compatibility code as design authority |
| **NoöPunk RPG** | nothing, this phase | touch, extend, "fix" or depend on it |

The simulator consumes **outputs** of the third link and implements **no** part of the first two.

## 2. What the AI26 code actually provides (inspected, not assumed)

Inspected in the local checkout of `TomiToivio/LaclauGPT-Data-Analysis` on 2026-11-07:

| contract | where | what the simulator may rely on |
|---|---|---|
| **Canonical record** | `src/laclaugpt_data_analysis/canonical.py:299` `CanonicalRecord`, `SCHEMA_VERSION = "1.2.0"` (line 27) | four sections: `raw_capture`, `intermediate`, `analysis`, `human_readable`; plus `source`, `content`, `evidence`, `provenance`, `review`, `legacy`; `source_url` is the canonical source identity and may not be empty |
| **Provenance** | `models.py:25` `Provenance` | `provenance_id`, `method`, `model`, `model_version`, `pipeline_version`, `created_at`, `metadata` |
| **Review state** | `canonical.py` `ReviewStatus` | `PROVISIONAL`, `ACCEPTED`, `REJECTED`, `REVISED`, `CANONICAL`, `SUPERSEDED` |
| **Discourse statement** | `discourse_network/models.py:65` `DiscourseStatement` | `statement_id`, `source_url`, `source_record_id`, actor/concept coding, `stance` (`support`/`oppose`/`neutral`/`mixed`/`unknown`), `agreement` plus `agreement_status` (`coded`/`ambiguous`/`not_applicable`/`abstain`), `validation_status` (`provisional`/`reviewed`/`validated`/`rejected`/`needs_review`), `EvidenceSpan` |
| **Concept types** | `discourse_network/models.py:16` `ConceptType` | `policy_claim`, `frame`, `signifier`, `imaginary`, `issue_position`, `concept`, `other` |
| **Network views** | `discourse_network/network.py` | `actor_concept_matrix`, `actor_projection`, `concept_projection`, `community_assignments`, `fragmentation_summary`, `coverage_summary` — projections over coded statements, not causal models |

Two consequences the simulator must honour:

1. **A `DiscourseStatement` is an interpretation of a text, not a behavioural parameter.** Its `validation_status` and
   `agreement_status` are part of the data, and an `abstain` or `ambiguous` statement is not a weak signal to be
   rescaled — it is a statement that does not enter a binary projection until reviewed.
2. **The projections are descriptive.** `actor_projection` and `community_assignments` say how coded claims cluster;
   none of them says an actor *will* do anything. Every transition rule in the simulator is therefore an explicit,
   separately documented assumption (§4), never a reading of a projection as a cause.

## 3. What already exists in NoöPunk, and what the simulator may reuse

| existing code | what it is | reuse decision |
|---|---|---|
| `src/simulation/events.py`, `engine.py`, `world_state.py` | #40 deterministic event envelope (turn-ordered, content-hashed ids) and a reducer, built for the RPG-adjacent world simulation | **read for patterns, not imported**: its entity/relation vocabulary and turn semantics belong to the NoöPunk fiction, and #1286 forbids RPG dependencies. The simulator keeps its own minimal event record so that a later adapter can translate between them deliberately. |
| `src/world/graphs.py` (physical/cyber/social/story) | the RPG's four graph families | **not reused.** #1286 explicitly separates simulation variables from RPG tags, and the RPG is frozen. |
| `src/simulation/clock.py`, `scheduler.py` | the campaign clock and due-event queue (#1230) | **not reused** for the same reason; the simulator's clock is integer steps, which is what reproducibility needs and what a wall clock cannot give. |
| `src/rules/**` | CWN/SWN/AWN mechanics | **out of scope, untouched.** |
| `src/social_sim/**` (this phase) | the standalone simulator kernel | **new**, with no imports from any of the above. |

**Duplication ledger.** The honest cost of the decision: NoöPunk will briefly hold two event models — the RPG-adjacent
one in `src/simulation/` and the simulator's — and two notions of a social tie. That is deliberate rather than
accidental: the alternative is a simulator that cannot run without the RPG, which is the thing #1286 forbids. The
integration seam (work package 7) is where the two meet, and it must be a documented translation, not a shared module
that drags RPG semantics into research runs.

## 4. Mapping: AI26 output → simulator input

| simulator concept | source | transformation | what must be preserved |
|---|---|---|---|
| **actor (individual)** | an `actor` naming on coded statements | the analyst's actor label becomes a synthetic actor id; **no real person is instantiated** (§6) | label, source count, the ids of the statements that name it |
| **actor (organization)** | an actor label that denotes an institution | kept as a distinct actor type, never folded into an individual | affiliation, the statements that treat it as a collective speaker |
| **discursive claim** | `DiscourseStatement` | one claim per statement, with `stance`, `agreement_status`, `validation_status`, `EvidenceSpan` | the quote, the offsets, the review state |
| **articulation between claims** | coded co-occurrence of concepts **plus** the theory's requirement for relational evidence | recorded as an *observation* with its evidence, never as an equivalence | which statements produced it, and that it is observational |
| **frontier / antagonist relation** | theory + reviewed analysis; **not** derivable from co-occurrence | only enters as researcher-supplied structure, labelled `inferred` | who supplied it and on what evidence |
| **collective subject** | proposed in analysis, contested by definition | a hypothesis with a review status, never an actor the simulator invents | the proposal's source and its contestation |
| **uncertainty** | `agreement_status`, `validation_status`, `Provenance` | carried per record; `abstain`/`ambiguous` never silently averaged | the original status string, not a number |

Anything that cannot be mapped with its provenance intact is **rejected** rather than coerced (work package 2).

## 5. The four kinds of material, kept apart

Every record in the simulator carries an origin, and the export schemas must keep them distinguishable end to end:

| origin | meaning | may it enter a metric? |
|---|---|---|
| `observed` | taken from AI26 output exactly | yes, labelled |
| `inferred` | produced by analysis or researcher judgement over observed material | yes, labelled, with its basis |
| `synthesized` | invented for a scenario — actor names, dispositions, tie weights | only inside a scenario's own outputs, never mixed into empirical comparison |
| `simulated` | produced by the simulator's rules | yes, as simulation output, never as evidence |

A round trip that loses this distinction is a bug, and the kernel tests assert it survives.

## 6. Scientific and ethical boundary

* **No predictive claims.** The simulator explores consequences of stated assumptions; it does not forecast.
* **No real, identifiable people as unconsenting simulated agents.** Analysis labels are mapped to synthetic actors;
  where a label is a real person the scenario must use a synthetic stand-in and say so.
* **Assumptions are separate from theory.** A transition rule is an assumption with a rationale and a parameter, not a
  derivation from Laclau. Sensitivity to those parameters is part of the experiment (work package 4).
* **No LLM in the loop by default.** Message generation by a model requires an explicit hypothesis, fixed prompts and
  seeds, and reviewable logs (work package 1/3); the kernel is deterministic and calls no provider.
* **Outputs are not data.** Simulation output is never written back over LaclauGPT data, and no export may be mistaken
  for an observed corpus.

## 7. Unresolved modelling choices — recorded, not decided

These are the questions this page deliberately leaves open, each with who can settle it:

1. **What makes two actors "connected"** in the synthetic population — shared coded claim, shared concept, shared
   organization, or an authored tie? (Researcher; needs the first experiment to choose.)
2. **How a claim becomes an action.** The kernel ships one documented, deliberately dull rule (§ kernel doc) and no
   theory-derived one.
3. **Whether organization actors aggregate member dispositions**, and if so by what rule. Averaging is an assumption
   with consequences, not a default.
4. **Time.** Integer steps now; whether a step means a statement, a day, or a round of interaction is a scenario
   parameter, not a kernel constant.
5. **Calibration.** Nothing is calibrated in phase 0–1. Any later calibration must name its target distribution and
   its ethical basis.
6. **Reviewer workflow.** `review_status` is carried but not enforced; whether an unreviewed statement may enter a
   scenario at all is a policy decision.
7. **Determinism limits.** Seeded and reproducible in the kernel; a future LLM rule would break exact replay, so the
   issue's "document determinism limits" clause applies from the moment one is introduced.

## 8. Scope check for this phase

* No file under `src/rules/`, `rulebook/`, `docs/campaign/`, `src/world/`, `src/console/`, `src/godot/`, `mud/` is
  modified by this work.
* No RPG vocabulary is imported into the simulator: the kernel's tests assert that its modules import nothing from
  `rules`, `world`, `console` or `simulation`.
* The old RPG issues stay closed as *not planned for this phase*; nothing here reopens them.
