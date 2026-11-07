# Prompt: Strategic reset: build the LaclauGPT social-science simulator first

- **Date:** 2026-11-07
- **Topic:** issue #1286
- **Source:** Tomi's own issue text in NooPunk, <https://github.com/TomiToivio/NooPunk/issues/1286>
- **Archive status:** original author prompt, retained verbatim for future reuse. It is **not** an approved canon or
  implementation specification by itself, and archiving it does not authorize work on a frozen subproject.

## Original prompt (verbatim issue text, transport formatting normalised)

# NoöPunk Social Science Simulator: independent subproject within the three-track architecture

> **Updated direction (2026-11-07; supersedes the RPG freeze in the earlier version of this issue).** NoöPunk has three **parallel, independently developable subprojects: Story, Simulator, and RPG**, as defined by [#1295](https://github.com/TomiToivio/NooPunk/issues/1295). **The RPG is NOT frozen as a subproject. Only the Cities Without Number (CWN) core rules are immutable.** Agents may develop any of the three tracks within its boundaries, without implementing matching changes in the other two at the same time. Integrate and test compatibility periodically, especially Simulator ↔ RPG. This issue remains the **Simulator work tracker**, not the sole active NoöPunk tracker.

## Three subprojects and their relationships

| Subproject | Independent purpose | Shared system and integration |
| --- | --- | --- |
| **NoöPunk Story** | Tomi writes the original branching screenplay/choices/script, potentially developed into the **NoöPunk science-fiction book**. | Story uses a compatible **Story Graph**. The agent-derived Story Graph supplies the RPG's narrative scenes, choices, prerequisites and consequences. |
| **NoöPunk Simulator** | A standalone **LaclauGPT-based Social Science Simulator**, also the **gamified simulation subproject of [LaclauGPT](https://github.com/TomiToivio/LaclauGPT)**. | Uses shared compatible **Tag/Graph contracts** for agents, discourse, ideology, organizations/factions and relations; supplies the NoöPunk RPG's **ideology and faction simulation**. |
| **NoöPunk RPG** | A playable **Cities Without Number** game with a modular, Narrativist-inspired **NoöPunk Mod**, built using compatible Graphs and Tags. | **CWN core rules are immutable.** The mod overlays CWN rather than modifying it; RPG consumes the Story Graph and Simulator state using explicit adapters. |

**Direction of authority:** Tomi's Story → agent-maintained Story Graph → RPG narrative; LaclauGPT scientific input → Simulator Tag/Graph state → RPG ideology/factions. The RPG is a consumer, not the authoritative editor of Story or Simulator. All three may use the **same interoperable Graph/Tag vocabulary and versioned contracts** without being one tightly coupled runtime.

**Separate development is the default.** A Story PR need not modify Simulator or RPG; a Simulator PR need not modify Story or RPG; an RPG PR need not modify Story or Simulator. Make an adapter change only when needed and review changes to shared contracts across all affected tracks. **Occasionally run cross-project compatibility/integration tests**; do not require simultaneous feature parity or three-track updates per PR.

## Hard guardrails for agents

1. **Immutable CWN core:** Never rewrite, rebalance, fork, replace or redesign Cities Without Number core mechanics. Changes for NoöPunk belong in a separate, CWN-compatible **NoöPunk Mod** based on our Narrativist-inspired Tag/Graph system. Preserve existing SWN/AWN integrations unless a separately scoped issue calls for changes; no rules churn.
2. **Story authorship:** Per #1295, `NooPunk-Story/Story/` contains **Tomi-only writing, agent READ ONLY**. Do not write, rewrite, format, rename, move, delete or generate manuscript/script/novel text in that directory. Agents may develop `NooPunk-Story/Graph/` as a derivative, using source references and review notes instead of fabricating canon. The eventual novel is optional, not a requirement to implement the graph or RPG.
3. **Simulator scientific independence:** Simulator runs independently of a CWN sheet, campaign, player, Evennia or Story runtime. Keep its research contracts and assumptions explicit. It may power **gamified simulations**, but game abstractions must not become empirical findings or rewrite LaclauGPT Phase 1 methodology.
4. **Shared Graph/Tag interoperability:** Define minimal stable node/edge types, tag namespace/meaning, IDs, data formats, temporal semantics, provenance, schema versions, adapters and validation tests. Share **contracts**, not forced coupling. Story Graph, Simulator Graph and RPG mod can have track-specific extensions while remaining compatible. Never silently change another subproject's semantic meaning.
5. **No blanket RPG freeze and no sole-tracker rule:** RPG agents may implement separately authorized RPG tasks/mod features, preserving CWN core. Story Graph agents and Simulator agents may work in parallel. Do not close or forbid other Story/RPG issues merely because #1286 exists.
6. **Work within the track:** In a Simulator-only PR, prefer Simulator files and contracts; touching RPG code should be an explicitly scoped separate PR, not an automatic consequence. Conversely, no mandatory Simulator changes with each RPG feature. Preserve existing code/history during staged migration under #1295.

## Canonical scientific sources and boundaries

1. **[LaclauGPT AI26 Phase 1 paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md)** remains the starting point for Simulator methodology. Preserve its theoretical commitments regarding discourse, contested signifiers, articulations, frontiers, political subjects and uncertainty. **Do not alter the scientific paper or Phase 1 theory/methodology through this issue.** Paper phases are not software work packages.
2. **[LaclauGPT THEORY.md](https://github.com/TomiToivio/LaclauGPT/blob/main/THEORY.md)** supplies the evidence/interpretation boundary: co-occurrence, frequency and semantic similarity do not by themselves establish hegemony, equivalence, antagonism or populism.
3. **[LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis)** is the analysis and canonical-record technical basis; use a read-only, version-aware and reviewable adapter rather than altering the analysis pipeline. Collection → Analysis → Visualization remains the research pipeline.
4. **[#1295](https://github.com/TomiToivio/NooPunk/issues/1295)** owns the three-subproject structural reorganization, shared Graph/Tag contracts and author-only Story guardrail; **#1286 owns Simulator scientific implementation**. Avoid duplicate or competing simulators; follow the current canonical implementation ledger.

**Scientific boundary:** AI26 discourse-analysis codes are interpretations of evidence, not behavior parameters or verified causal laws. Specify and test synthetic initial conditions, transition assumptions, calibration and sensitivity separately. Retain provenance and uncertainty; distinguish **observed, inferred, synthesized and simulated**. Do not represent fabricated messages or simulations as empirical AI26 data, claim predictive validity without evidence, or instantiate identifiable real persons as unconsenting simulated agents. Human review must remain possible.

## Simulator architecture and minimal scope

Implement a standalone, reproducible, inspectable computational social-science simulator of agents, organizations/factions, ideology, communications and social structures, with **compatible Tags and Graphs**. The common contract should allow RPG adapters to subscribe to or query Simulator state without giving CWN control over simulation rules.

- **Actor/organization graph:** synthetic individuals, organizations and factions, membership/affiliation, resources, dispositions, roles and changes. Simulator tags are typed social-science variables, compatible with shared Tag schema but **not automatically CWN character mechanics**.
- **Social and communication graphs:** directed, typed, time-indexed nodes/edges with stable IDs, organization/individual separation, traceable sources, uncertainty and replay.
- **Discourse/ideology graph:** explicitly evidenced AI26 claims and articulations, demands/signifiers, frontiers, contested relations and projects. Avoid inferring articulation from mere co-occurrence.
- **Event/dynamics system:** communicate/respond, affiliate/disaffiliate, support/contest, link/separate demands, resources/attention and institutional reactions; trace each event to an actor, time, rule and input. Start with documented seeded baseline rules, then justified behavioral hypotheses. LLM components are optional and require clear hypotheses, reproducibility and logs.
- **Outputs:** state snapshots, event trace, Graph/Tag exports, metrics, run manifests, visualization contracts and provenance. A future RPG adapter may expose faction/ideology state and process RPG interventions through an explicit contract, **without merging the RPG rule engine into Simulator**.

## Simulator work packages (independent of Story/RPG development)

Prior work already delivered WP0–WP2 on `main` (see `docs/simulator/` and linked PRs); a parallel synthetic contestation experiment also exists. **Reverify current implementations before marking further items complete or retiring duplicates.** Checkboxes below track end-to-end acceptance, not simply whether any code with that name exists.

- [x] **WP0. Audit and contracts (initial):** AI26 paper/THEORY.md → Data-Analysis canonical schema → Simulator input mapping, uncertainty/ethics boundary and duplication ledger (`docs/simulator/BOUNDARY_AND_CONTRACTS_1286.md`).
- [x] **WP1. Baseline kernel (initial):** seeded deterministic synthetic actors/organizations, communication/social edges, events, replay/snapshots and provenance (`src/social_sim/kernel.py`; canonical per `docs/DUPLICATION_AUDIT.md`).
- [x] **WP2. AI26 read-only adapter (initial):** canonical record validation and provenance/evidence-linked claims/articulations (`src/social_sim/ai26.py`; `docs/simulator/AI26_ADAPTER_1286.md`).
- [ ] **WP3. Explicit behavioral assumptions:** documented and configurable communication/influence, coalition, ideology and institutional/faction rules. Separate assumptions from LaclauGPT observations; include sensitivity and parameter justification.
- [ ] **WP4. Reproducible experiments:** assess existing `src/simulation/ai26_experiment.py` work against the **canonical Simulator**; implement or migrate a paired contestation scenario with control/intervention, multiple seeds, sensitivity and failure/abstention paths without establishing a second engine.
- [ ] **WP5. Exports and evaluation:** typed, versioned Tag/Graph exports, metrics, source/event provenance, run manifest, validation and justified empirical comparisons.
- [ ] **WP6. End-to-end demo:** runnable synthetic social/ideology/faction simulation with Graph/Tag visualization and clear observed/inferred/synthesized/simulated distinctions, useful independently and later for gamified LaclauGPT experimentation.
- [ ] **WP7. RPG interoperability:** define and verify a **versioned, optional Simulator ↔ RPG ideology/faction adapter**, initially via contract/fixture tests. **Integration can now be implemented when independently scoped; it is no longer forbidden.** Never change immutable CWN mechanics as part of that integration.
- [ ] **Shared schema compatibility (#1295):** coordinate with Story Graph and RPG Mod agents on common Tag/Graph IDs, schema versioning, import/export and compatibility tests; this does not require simultaneous feature implementation.

## Acceptance and anti-scope-creep checks

- Simulator can run seeded synthetic fixtures from Python, with no CWN, Story runtime, playable campaign or per-agent LLM API requirement.
- Same inputs/seed/config produce reproducible event traces and snapshot/export hashes, or documented limits when using external LLMs.
- Schemas preserve provenance, uncertainty and the four material origins through round trips.
- Test graph integrity, ordering, affiliation, isolation, empty/uncertain inputs, conflicting discourse articulations, no fabricated evidence and a modest-N runtime/memory baseline.
- Scientific outputs distinguish observed source evidence from inferred interpretation and synthesized/simulated activity. The original AI26 methodological contract is untouched.
- Shared Tag/Graph contract tests detect breaking names/IDs/edge semantics/schema changes; **periodically test Simulator ↔ RPG compatibility** (and Story Graph → RPG when appropriate).
- **CWN core is unchanged**, while NoöPunk Mod remains a separate, compatible overlay. A Simulator-only PR does not need RPG changes or Story changes to pass.
- Agents never write Tomi's manuscript in `NooPunk-Story/Story/`. Story-derived graphs are reviewable derivatives, not substitute prose or invented canon.
- The aim is an inspectable scientific simulator that can also support gamified simulation and the RPG's ideological/faction world. Do not expand the MVP into an exhaustive world simulator.

## Agent coordination and issue hygiene

**Authority:** #1295 defines how Story, Simulator and RPG coexist; this issue coordinates Simulator scientific work and its contracts. The three tracks **progress asynchronously**. Keep PRs small and track-specific; identify exact tests and compatibility impact. Periodically perform integration rather than requiring it for every individual change.

**Suggested division:** Tomi writes the Story (potentially a book); Story Graph agents adapt only the author-written source; Simulator agents develop LaclauGPT-informed ideology/faction processes; RPG agents maintain CWN-compatible gameplay and NoöPunk Mod. Each may proceed independently. When an integration milestone arrives, validate Story Graph → RPG and Simulator ↔ RPG using fixtures, adapters and shared schema tests. **No new change should reopen the endless CWN-core rules redesign cycle.**

**Important:** this update rescinds all earlier language in #1286 saying "RPG frozen," "RPG work forbidden," "Simulator FIRST and everything else later," "sole active tracker," "no RPG files under any circumstances," or "WP7 document only." Historical comments may retain those earlier instructions, but **the current issue body and #1295 supersede them**.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

## Implementation slice claimed: research adapter/kernel on existing simulation event-log core

Audit (2026-11-07):
- **Canonical existing implementation:** `src/simulation/events.py` (`Event.create`, deterministic IDs and strict `synthetic`), `src/simulation/world_state.py` (`reduce_events`, `replay_digest`), `src/simulation/engine.py` (turn/event log and branching). Reuse these, **do not create another event store/reducer/game loop**.
- **Existing RPG-adjacent material to NOT edit:** `src/world/graphs.py`, `strategy_game/`, `src/rules/`, `mud/`, `rulebook/` and game/setting docs. `strategy_game/docs/POLITICAL_SIMULATOR_SCOPE.md` represents an earlier game proposal, NOT the new AI26 research simulation.
- **Scientific references inspected:** LaclauGPT `paper/PHASE_1_PAPER.md` + `THEORY.md`, and `LaclauGPT-Data-Analysis` README and current canonical-analysis package location.
- **Existing PR ownership:** no open simulator PR found at start of this slice.
- **Missing research-specific work:** deterministic synthetic actor/organization roster; a simple documented exploratory communication process; typed social/communication graph snapshots; standalone CLI export/tests; boundary mapping.
- **Files planned for PR:** `src/simulation/ai26_research.py`, `tests/test_ai26_research_simulation.py`, `docs/research/AI26_SIMULATOR.md`. No RPG paths. No LaclauGPT code or paper changes.
- **Out of scope:** empirical AI26 schema adapter (requires separate schema validation and human review), any claim of causal realism/predictive validity, RPG integration.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

Claiming the complementary canonical input adapter and paired experiment slice. The kernel/CLI files claimed above belong to that implementation. I will use separate research-only paths, validate against Data Analysis CanonicalRecord 1.2.0, and keep source evidence outside synthetic actor state.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

## #1286 implementation progress (PR #1287)

Implemented a first **research-only** increment on branch `feat/1286-ai26-research-simulator`: reusable canonical event-log–based synthetic population, communication and affiliation events, deterministic replay, time-stamped social/communication graph projections, standalone CLI/JSON and regression tests. Scientific boundaries and AI26 source-to-simulator mapping are documented in `docs/research/AI26_SIMULATOR.md`.

**Scope audit:** PR changes exactly three files: `src/simulation/ai26_research.py`, `tests/test_ai26_research_simulation.py`, `docs/research/AI26_SIMULATOR.md`. No RPG rules, CWN, campaigns, game/strategy code, agents, or lore touched. Existing `Event` and `reduce_events` reused; no parallel event engine.

**Verification:** CWN immutable-core structural gate passed. General Python CI was still running when checked. PR is mergeable, but it remains open pending test verification.

**Not complete:** no live read-only AI26 canonical-data adapter or validated human-review mapping; no scientifically justified behavioral transition model, experiment sensitivity study or empirical calibration. Existing issue #1286 remains open. Explicitly do not interpret synthetic random encounters as hegemony, populism or observed ideology.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

Canonical #1286 work is now merged on main; no fourth simulator was added.

**Merged increments**

- #1287 (`d4f5abd2`) — `src/simulation/ai26_research.py`: synthetic random-encounter null model, deterministic event log/replay, `docs/research/AI26_SIMULATOR.md`.
- #1288 (`20ac9dce`) — `src/simulation/ai26_input.py` + `ai26_experiment.py`: read-only reviewed AI26 canonical relations, evidence/provenance checks, paired contestation experiments, `docs/research/AI26_CONTESTATION.md`.
- #1289 (`d33f02b0`) — `src/social_sim/kernel.py`: the canonical WP0/WP1 kernel (actors/organizations, social/communication edges, four material origins, rule-traceable events, seeded replay); `docs/simulator/BOUNDARY_AND_CONTRACTS_1286.md` and `SIMULATOR_KERNEL_1286.md`.

**Verification:** 27 tests across kernel, AI26 research and contestation pass (one skip); the #897 AGENTS lock guards pass after the new top-level directive.

My overlapping `src/social_science` PR #1290 was closed unmerged: it duplicated the kernel, and its adapter was less strict than the merged `ai26_input.read_relations` (which requires a dated human approval and evidence). No RPG, CWN/SWN/AWN, campaign or game-adapter file was changed.

**Still open for #1286:** calibration/sensitivity study, empirical comparison where justified, notebook/visualization demonstration, and the future optional CWN seam. The issue remains open.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

## Work package 2 delivered — the read-only AI26 adapter (PR #1292, merged `ee5d5f7`)

Continuing the sequence after WP0 contracts + WP1 kernel (`src/social_sim/kernel.py`). This increment is one module and its evidence; no RPG file, rulebook, campaign, CWN mechanic, game adapter or canon is touched.

**What landed.** `src/social_sim/ai26.py` is the single door a LaclauGPT AI26 canonical record comes through into the simulator:

- **validates** the published contract structurally — `schema_version` exactly `1.2.0`, non-empty `source_url`, every analysis row resolving a `provenance_id` that exists and carries `created_at`, every `evidence_id` resolving to an `Evidence` span of *this* record's source with a quote or a ref, no ambiguous ids;
- **projects** coded `DiscourseObject` rows into `ImportedClaim` (`claim:<family>:<object_id>`) and only the **explicit** `relations`, `antagonisms`, `equivalence_chains`, `difference_chains` into `ImportedArticulation` (`art:<family>:<id>`), keeping the canonical id as `native_id`;
- **labels material**: evidence spans `observed`, claims and articulations `inferred`; nothing here is `synthesized` or `simulated`;
- **refuses** (22 tested refusal cases) an unknown schema version, an empty source identity, a collection-only analysis, a missing analysis section, unresolved or foreign evidence, unresolved provenance, a `REJECTED`/`SUPERSEDED` review on the record or on a row, a duplicate object id, an unplaceable relation endpoint, a one-member chain, an analysis that codes nothing, a coerced family shape and non-JSON;
- **carries, does not enforce** `PROVISIONAL`/`ACCEPTED`/`CANONICAL`/`REVISED` review state, consistent with WP0 §7.6, and warns when an `ACCEPTED` record has no reviewer or date;
- **invents nothing**: no actor (an analysis label may denote a real person — synthetic stand-ins are a scenario decision), no relation from co-occurrence, no analysis-engine import, no mutation of the input, no network or model call. Each of those is a test, not a promise.
- CLI: `PYTHONPATH=src python -m social_sim.ai26 --canonical record.json [--summary]` — prints the bundle, or exits `2` with `refused: <reason>`.

**Boundary documents:** `docs/simulator/AI26_ADAPTER_1286.md` (mapping, refusal table, review policy, what a bundle still does not give the simulator), plus a pointer from the kernel page and a register row.

**Verification.** `python -m unittest discover -s tests -p "test_*.py"` → **3329 tests, OK (skipped=4)**, re-run on post-merge `origin/main` `ee5d5f7`. `tests/test_social_sim_ai26_1286.py` is 41 unittest tests over in-file synthetic fixtures (no corpus data read or written). `ruff check` clean on every changed Python file. CI on the PR: `test`, `cwn-structure`, CodeQL and both Analyze jobs green.

**Also repaired a red `main`.** `tests/test_ai26_research_simulation.py` (from #1287) was written as bare pytest-style functions with `import pytest` and a cwd-relative `sys.path.insert`: `unittest discover` collected nothing from it, and CI — which installs only `requirements.txt`, no pytest — could not import the module, so `test_test_isolation` was failing on `main` at `d33f02b`. Rewritten as a `unittest.TestCase` suite with the assertions unchanged; 9 tests now actually run.

**PR #1290 closed as superseded.** It added `src/social_science/`, a *third* event model beside `src/simulation/` and `src/social_sim/`, against an issue that says to avoid another competing world engine; its head branch was already gone from the remote and it was `CONFLICTING`. Its commit stays reachable at `refs/pull/1290/head` (`491b25e`) and its `metrics.py` / `export.py` / `benchmark.py` are the reference shape for WP5. If a separate `social_science` package *was* the intended architecture, that is an author call — reopen it and I will rebase instead of porting.

**Still open on this tracker:** WP3 (documented behavioural assumptions beyond the `broadcast` baseline), WP4 (paired contestation experiment with multiple seeds and sensitivity), WP5 (graph/event exports, metric definitions, run manifest), WP6 (end-to-end demonstration noting observed vs simulated vs inferred), WP7 (passive integration seam document only). The adapter stops at a validated bundle by design: it creates no population, and #1286 says it should not.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

## Status check: WP0–WP2 are on `main`, and there are **two** simulator stacks

I built WP0 + WP1 as a standalone package (`simulator/`), then found the work already merged and **discarded mine unpublished**. Rather than add a third, here is what is actually on `main` and the one conflict that needs your decision.

### Verified state — `ee5d5f78`, green

`python -m unittest discover -s tests` → **3329 tests OK** (4 skipped); `rules_constitution_audit`, `check_engine_boundary`, `cwn_parity_audit` all `--check` green. **No file under `src/rules`, `rulebook`, `src/world`, `src/console`, `mud` or `docs/campaign` was modified** — the freeze holds.

| WP | Evidence on `main` |
|---|---|
| 0 | `docs/simulator/BOUNDARY_AND_CONTRACTS_1286.md` (126 l) |
| 1 | `src/social_sim/kernel.py` (460 l) + `docs/simulator/SIMULATOR_KERNEL_1286.md`; 25 tests |
| 2 | `src/social_sim/ai26.py` (733 l) + `docs/simulator/AI26_ADAPTER_1286.md` (97 l) |
| 4 (partial) | `src/simulation/ai26_experiment.py` — "paired synthetic contestation experiment" |
| 5, 7 | **not verified present** — exports/metric definitions and the documented CWN seam |

### The conflict worth your ruling

There are **two unlinked implementations**, each with its own tests:

| Stack | What it is | Its own boundary claim |
|---|---|---|
| `src/social_sim/` | the documented WP1/WP2 simulator (`kernel.py`, `ai26.py`) | `BOUNDARY_AND_CONTRACTS_1286.md` §3 says it **deliberately does not import** `src/simulation/` |
| `src/simulation/ai26_input.py`, `ai26_research.py`, `ai26_experiment.py` | a second simulator built **on** `src/simulation/{events,engine,world_state,sqlite_store}.py` | none; it reuses the RPG-adjacent core |

The WP0 boundary document is explicit that the `src/simulation/` event/engine vocabulary is **RPG-adjacent and must not be built upon** for #1286 — *"read for patterns, not imported: its entity/relation vocabulary and turn semantics belong to the NoöPunk fiction"*. The second stack does exactly what that document forbids, and neither stack references the other.

So the questions are yours:

1. **Which stack is canonical?** If `src/social_sim/` is, the `src/simulation/ai26_*` modules are a boundary violation and should be archived with a superseded banner — their tests currently make the suite look broader than the approved design.
2. **Or is the `src/simulation/` route the intended one**, and the WP0 document over-strict? Then `src/social_sim/` is the orphan and its 25 + 8 tests should be retired rather than maintained twice.

I have **not** chosen, deleted or merged either: both are other agents' merged work, and picking one is a design decision, not housekeeping.

### One defect already fixed on `main`

`tests/test_ai26_research_simulation.py` had eight module-level `pytest` functions — never collected by `unittest discover` — and `import pytest` is not in `requirements.txt`, so CI could not import the module. Another PR converted it to `TestCase` while my fix was open; I closed mine as superseded. It now contributes **8 real tests**.

### What I did not do

I did not write a fourth simulator, did not tick any box in the issue, and did not touch the RPG. WP3 (behavioural rules), WP5 (metrics/exports) and WP7 (the documented CWN seam) still need a single owner before more parallel work lands.

---

## Follow-up in the same thread (2026-11-06)

The author added or revised the direction in the thread. Kept separately so the original is not overwritten.

**Work packages 0 and 1 are in; work package 2 landed from a parallel branch; no RPG file was touched.** `main` green at **3,329 tests** (2 skipped).

## WP0 — the boundary and the contracts

[`docs/simulator/BOUNDARY_AND_CONTRACTS_1286.md`](https://github.com/TomiToivio/NooPunk/blob/main/docs/simulator/BOUNDARY_AND_CONTRACTS_1286.md). It records the authority chain (paper → THEORY.md → Data-Analysis → *nothing* from the RPG) and what the AI26 code actually provides, **read from the local checkout rather than assumed**:

- `CanonicalRecord` (schema 1.2.0) with `raw_capture` / `intermediate` / `analysis` / `human_readable`, and `source_url` as the non-empty source identity;
- `Provenance` (method, model, pipeline version, created_at) and the six `ReviewStatus` values;
- `DiscourseStatement` with `stance`, `agreement` + `agreement_status` (`coded`/`ambiguous`/`abstain`), `validation_status`, `EvidenceSpan`; `ConceptType`; and the descriptive `actor_projection` / `concept_projection` / `community_assignments`.

Two consequences it states: an abstention is **not** a weak signal to be rescaled, and the projections are descriptive, so no transition rule may be read off them. It also maps each simulator concept to its source, keeps `observed` / `inferred` / `synthesized` / `simulated` apart, states the ethics (no real people as unconsenting agents, no predictive claims, LLM only under an explicit hypothesis), and lists seven modelling choices **left open** with who can settle each.

## WP1 — the simulator, and the duplication it created

Two slices landed within the hour: `src/social_sim/` (standalone kernel, four-origin provenance, snapshot/replay, plus the WP2 adapter with 41 tests) and `src/simulation/ai26_research.py` (a null-model demo on the #40 event envelope). That is two simulators for one issue, so `docs/DUPLICATION_AUDIT.md` now names **`src/social_sim/` as canonical** — WP2 needs per-record origins and an adapter that can refuse an import, and it is built on that kernel — and [`docs/research/AI26_SIMULATOR.md`](https://github.com/TomiToivio/NooPunk/blob/main/docs/research/AI26_SIMULATOR.md) carries a **Superseded** banner.

I did not delete the older module: it is yours and freshly merged, and it is still green. The banner says it is not the path to extend, and the ledger says to delete it once the canonical path covers the null-model demo. **Say the word and I will delete it in one PR.**

## Also repaired in passing

`main` was red twice for reasons unrelated to the simulator: two guards pinned the #897 wording after your 2026-11-07 directive replaced the top of `AGENTS.md`, and the new AI26 test module imported `pytest` in an environment whose CI runs only `unittest`. Both fixed with their intent preserved.

## What is deliberately not done

WP3 (behavioural assumptions), WP4 (the contestation experiment), WP5–6 (metrics, exports, visualization) and WP7 (the integration seam). The kernel ships a **null model** on purpose — neutral synthetic tokens, no persuasion, no scoring — so that seeded determinism, graph integrity, replay and provenance are proven before any claim about behaviour. No concept from the paper has been turned into a transition rule.

The one question I would put to you before WP3: **should organization actors aggregate their members' dispositions, and by what rule?** Averaging is an assumption with consequences, and the boundary page lists it as open rather than choosing.
