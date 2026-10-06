# Issue #152 — Long-term layer: living social-science simulation (Mesa + NetworkX + LaclauGPT)

> **For Hermes:** planning only. No RULEBOOK, code, `data/`, or `requirements.txt` changes land
> until the author clears the GATES in §0. Issue #152 is an umbrella that stays open; this plan
> covers the **architecture and the Phase A prototype specification**, not a finished
> implementation. It is meant to be read beside the sibling plan
> `2026-10-06_145230-issue153-faction-strategy-layer.md` — the two long-term layers share one
> state engine and must be designed together, but land separably.

**Goal:** add an **optional** long-term social-simulation layer in which antagonistic ideological
factions struggle for hegemony — constructing, defending and transforming identities,
equivalential chains, frontiers, demands, narratives and affects — so the world keeps changing
between sessions even when the PCs are not involved.

**Architecture:** reuse the existing deterministic, event-sourced simulation core
(`src/simulation/`) rather than starting a second world. That core already enforces the two
properties this layer needs — *state is a function of the event log* and *reduction is
deterministic* (`src/simulation/world_state.py`). Mesa supplies the agent **scheduler**; NetworkX
supplies the **multiplex network**; LaclauGPT supplies the **discourse/ideology engine**; the
existing **Affect graph** (`src/simulation/affect.py`, `data/world/social_affect_schema.json`)
supplies the affect layer. The RPG stays fully playable with the whole layer switched off.

**Tech stack:** stdlib Python + `unittest` for the deterministic core (unchanged — CI installs only
`requirements.txt`); **Mesa** (new, optional extra) for the ABM scheduler; **NetworkX 3.7** (already
installed on this machine) for the graph; `data/` JSON/YAML for the shared schema; `gh` for the
PR/comment. No new engine, no parallel rule system (`AGENTS.md` §13.3, §14).

---

## 0. Decision gates (nothing lands before these)

| Gate | Decision | Owner | Options |
| --- | --- | --- | --- |
| **GATE 1** | Where the shared world-state schema lives and who owns it | author | reuse/extend `data/world/*` + `src/simulation/` (recommended) **vs** a new `data/simulation/` package **vs** a LaclauGPT-side schema with a NoöPunk adapter |
| **GATE 2** | Faction-as-agent granularity | author | **factions are Mesa agents** (recommended for Phase A) **vs** factions *emerge* from lower-level actor/organization agents |
| **GATE 3** | Mesa as a hard dependency? | author | **optional extra** (`requirements-sim.txt`, recommended — keeps CI and the stdlib-only core untouched) **vs** add to `requirements.txt` **vs** vendor a tiny scheduler and skip Mesa |
| **GATE 4** | Determinism policy for stochastic steps | author | seeded RNG, one seed per (simulation, turn), logged in the event (recommended) **vs** fully deterministic resolution **vs** allow unseeded exploration mode |
| **GATE 5** | How much of LaclauGPT is *reused* vs *re-simplified* | author | call LaclauGPT's own pipeline via adapter (recommended for analysis parity) **vs** port a small subset of the concept registry into NoöPunk **vs** LLM-prompt LaclauGPT semantics |
| **GATE 6** | Scale-aggregation policy (DEFER-5 in the archived spec) | author | meso-agents + aggregate populations (recommended) **vs** all-individual agents |

GATE 1 and GATE 6 are coupled: the aggregation policy determines whether the schema needs an
`AggregatePopulation` kind at all. Ask them together.

---

## 1. Verified current state (measured on `origin/main` @ `40e10a5`)

Everything below was read from the repo, not from memory. The `origin/main` tip is `40e10a5`
("Expand faction taxonomy and schema (#149)"); the suite is green at **801 tests OK**.

| Fact | Where it lives | Status |
| --- | --- | --- |
| Event-sourced deterministic core: `state = reduce(events)`; ordering key is `turn`, never timestamp; `source`/`synthetic` set by the emitting boundary | `src/simulation/events.py`, `world_state.py` | **Canonical, implemented.** The reducer *deliberately* stores no derived quantity (no power/legitimacy/cohesion) — storing an unspecified number *is* inventing a mechanic. |
| Engine owns turns/run identity, contains **no rules**; actor decisions are supplied by the caller | `src/simulation/engine.py` | Implemented. Fixture vocabulary (`fixture:` prefix, `FIXTURE_RELATIONS`) is explicitly **non-canonical**. |
| SQLite store for event logs | `src/simulation/sqlite_store.py` | Implemented. |
| Unified Affect graph: `AffectEdge(source,target,affect,affect_score,domain,…)`, domains `faction_us / faction_frontier / motivation / reputation / contact`, bounds **−10…+10** | `src/simulation/affect.py`, `data/world/social_affect_schema.json` (issue #107, rescaled by #144) | **Canonical, implemented.** `inherit_faction_affects()` implements the seeding rule. |
| Faction model: `Faction = US^(constitutive affects) + FRONTIER^(antagonistic affects)`; seven SNA graph layers named and numbered | `rulebook/8_FACTIONS.md` (issues #122, #144, #149) | **Canonical.** Layer 7 (Faction↔Faction) is *derived from US/FRONTIER overlap*, not stored. |
| Multi-axis ideological model: paradigm-shift positions (accelerationist / critical / doomer / …) as a **cross-product**, never one left-right axis | `data/world/ideology.json` (issue #8) | **Canonical.** Categorical, not numeric — "#8 says the model does not have to become a numeric game mechanic yet". |
| Architecture spec (three views, event format, RPG↔society bridge, DEFER register) | `docs/archive/SIMULATION_ARCHITECTURE_SPEC.md` (archived) | **Archived** — cite it, do not treat it as active canon (`AGENTS.md` §13). Contains the DEFER-1…11 register this plan inherits. |
| Faction taxonomy + schema + NHI type-vs-faction split | `data/world/faction_taxonomy.json`, `RULEBOOK.md` §43 | **Canonical** (#144). |
| Default campaign is **Helsinki-centred**, a small faction network | `RULEBOOK.md` §9.3, `FACTIONS.md` | Canonical. |
| **No mesa anywhere; NetworkX 3.7 present on this machine** | — | Measured. If Mesa is required, GATE 3 governs how it is declared. |

**Key consequence:** the simulation layer is **not** a greenfield. The event log, the reducer, the
Affect graph and the faction ontology already exist and are guarded. This layer **feeds the same
event log**; it does not build a rival state store.

---

## 2. Verified source facts this plan depends on

- **LaclauGPT** (`TomiToivio/LaclauGPT`, public) is a *discourse-analysis pipeline*, not a
  simulator. Its `THEORY.md` §14 is a machine-readable **concept registry** (`DT_ARTICULATION`,
  `DT_NODAL`, `DT_FLOATING`, `DT_EMPTY`, …) and §15 is a set of **theory invariants** that are
  normative for that repo: `INV_ANTAGONISM` (*negative sentiment cannot by itself establish an
  antagonistic frontier*), `INV_AFFECT` (*sentiment polarity cannot substitute for affective
  investment*), `INV_HEGEMONY_CORPUS` (*frequency or one document cannot establish hegemony*),
  `INV_ABSTAIN`, `INV_EVIDENCE`, `INV_DYNAMIC_LABELS`. NoöPunk's `rulebook/4_SOCIAL.md` already
  restates two of these (`Mere disagreement or dislike is not automatically an antagonistic
  frontier`; `Ambiguity alone never makes a signifier floating or empty`).
- LaclauGPT's concepts are **relational roles**, not entity classes — its §16.7 warns against
  "adding ontology or schema types merely because a theoretical term exists". This matters for
  GATE 1: `floating_signifier` etc. are **edges/roles in the graph**, not node kinds.
- Palonen's **Formula of Populism** (Us / Frontier / Affects / Abstention) is the shared schema;
  `rulebook/4_SOCIAL.md` already adopts it as a general faction model and explicitly notes it is
  **not a populism classifier**.

---

## 3. The central design crux (why GATE 1 and GATE 5 exist)

The issue asks for a *living society*. The repo's architecture forbids the obvious shortcut:
it says **do not store a derived number you have not specified** (`world_state.py` docstring), and
`AGENTS.md` §1 forbids inventing rules. So the layer cannot simply write `faction.power += 2` into
state. Two consequences shape the whole design:

1. **Derived analytics are recomputed, never stored as canon.** "Network power", "brokerage",
   "cohesion" are **views over the log + graph**, produced by the analysis step, not new canonical
   fields. This keeps the event log the single source of truth and keeps determinism.
2. **Ideological change must go through the Affect graph and the discourse roles the repo already
   defines** (US/FRONTIER, signifier roles), not through a parallel ideology store. That is the
   only way "the political field itself changes" stays auditable.

The failure mode to avoid is a **second, richer state model** that quietly becomes canon and
contradicts the tabletop rules. This plan is written to make that failure a GATE decision rather
than an accident.

---

## 4. Conflict register — findings that must be decided, not silently resolved

| # | Conflict | Why it matters | Gate |
| --- | --- | --- | --- |
| C1 | The issue says "reuse as much as practical from LaclauGPT", but LaclauGPT is an **analysis** pipeline (corpus → coded results), not a generative simulator. | Reusing it wholesale means *analysing* generated discourse; porting a subset means re-implementing theory. These are different products. | GATE 5 |
| C2 | The archived spec's **DEFER-2** (relation types) leaves `controls`, `member_of` etc. *unconfirmed*; the issue's edge list adds alliance/funding/penetration/etc. | Freezing an edge enum makes proposed vocabulary canon. | GATE 1 |
| C3 | The issue wants a multiplex network, but the existing Affect graph is a **single labelled-edge graph** with fixed domains. | Overloading Affect domains with network edges would merge two layers (the exact drift `test_issue122` guards). | GATE 1 |
| C4 | "Factions update goals, alliances, resources, reputation" implies stored per-faction scalars; the reducer forbids stored derived scalars. | Must be resolved as *derived views + event history*, or the reducer's invariant breaks. | GATE 1 / §3 |
| C5 | Mesa has no version pinned and is not in `requirements.txt`; CI installs only `requirements.txt`. | A hard Mesa import in the deterministic core would break CI. | GATE 3 |
| C6 | The default campaign is deliberately small and Helsinki-centred; the issue's Phase C is a global simulation. | Scope creep would drown the tabletop in noise — the issue itself lists this as a research question. | §8 |

---

## 5. Proposed shared-world schema (proposal, pre-GATE 1)

**Not canon until GATE 1 clears.** Two rules from §3 apply: *roles are edges, not nodes*; *derived
quantities are computed, not stored*.

| Concept (issue's list) | Proposed representation | Canon source |
| --- | --- | --- |
| `Faction` | entity in the event log; `US`/`FRONTIER` **edges** in the Affect graph | `rulebook/8_FACTIONS.md`, `data/world/faction_taxonomy.json` |
| `Actor` | entity; contacts/reputation are Affect edges | `affect.py` |
| `Organization` | entity; may be a nested faction | `data/world/organizations.yaml` |
| `Place` | entity; Helsinki-first | `GAMEPLAY_LOOP.md` |
| `Event` | the existing event envelope — **reuse, do not fork** | `src/simulation/events.py` |
| `Demand` | target **type** of an Affect edge / articulatory role | `4_SOCIAL.md` |
| `Signifier` | target type + role mark (`nodal_point / floating_signifier / empty_signifier / ordinary`) — **role, not class** | `4_SOCIAL.md`, LaclauGPT registry |
| `Affect` | existing `AffectEdge` | `affect.py` |
| `Relationship` / `NetworkEdge` | **new** — the multiplex layer (alliance, antagonism, funding, info-flow, penetration, adjacency…), kept **separate** from Affect | GATE 1 (C3) |
| `Resource` | **derived view** or event-sourced delta; no bare stored scalar (C4) | §3 |
| `Reputation` | already an Affect domain | `affect.py` |
| `Territory` | Place + optional derived control edge | GATE 1 |
| `IdeologicalFormation` | the US/FRONTIER articulation of a Faction; positions from `ideology.json` | `data/world/ideology.json` |

Deliverable if GATE 1 = "reuse": `data/world/simulation_schema.json` describing the *network* layer
and pointing at the existing artefacts, plus a `docs/design/SOCIAL_SIMULATION.md` spec — **not** a
new parallel schema.

---

## 6. Proposed work order (after gates clear)

### Phase 0 — the decision record (no code)
Write `docs/design/SOCIAL_SIMULATION.md`: the three views (Tabletop / Analysis / Simulation), the
RPG↔society bridge, the schema decision, and an explicit **DEFER register** inheriting the archived
spec's DEFER-1…11 rather than re-inventing them. Post the GATE answers as a comment on #152.

### Phase A — tiny prototype (the issue's own Phase A)
- 5–10 **Helsinki-relevant** factions, 1 city, 1 ideological issue, 3–5 ideological variables per
  faction, monthly ticks, **one-page GM output**.
- **Mesa** model loop = the issue's 9 steps, but step (1) ingests from and step (9) writes back to
  the **existing event log**.
- **NetworkX** multiplex graph with ≥3 edge types (alliance, antagonism, information flow).
- Guarded by a new `tests/test_issue152_simulation.py` in the house style (structure pins, no
  network dependency in CI — see §9).
- **Acceptance = the issue's first four AC boxes** in miniature.

### Phase B — living Helsinki campaign
Institutions + media; neighbourhood geography; network diffusion; faction splitting/coalition
formation; **persistent campaign state in SQLite**; player-action feedback via the event log.

### Phase C — NoöPunk world simulation
Transnational networks; global institutions; NHI/AI/psionic shocks; political economy; **hands the
same state to the #153 strategy layer** (§7).

### Multi-timescale clocks (design now, implement in B)
`scene` (local consequences only) → `weekly/monthly` (discourse, alliance, network, reputation) →
`seasonal/yearly` (structure, institutions, economy, rise/fall). GM command `advance-world --months 1`
returns a **campaign brief** (the issue's §5 output categories), not raw analytics.

---

## 7. Relationship to #153 (design together, land separately)

One **state engine**, two **facings**, exactly as #153 states:

| | #152 social simulation | #153 strategy layer |
| --- | --- | --- |
| who acts | autonomous factions/institutions, no player input | players deliberately, at faction-leadership scale |
| output | structural change + campaign hooks | meaningful strategic **choices** |
| shared | the event log, the Affect graph, the multiplex network, the schema, `ideology.json` | same |
| interface | emits world-delta events + GM digest | consumes them; emits strategic-decision events back |

**Design rule:** neither layer owns a private state file. The contract between them is the **event
log + the schema**. If a Phase-A prototype needs a field the strategy layer cannot read, that is a
schema bug, not a second store.

---

## 8. Scope discipline (answering the issue's own scope worry)

- **Optional and off by default.** The tabletop RPG must run with zero simulation code loaded. A
  guard asserts the core path imports no Mesa/NetworkX.
- **Helsinki-legible.** High-salience events only reach the table; everything else stays in the
  digest. The issue itself flags "keep the Helsinki campaign legible instead of … drown the RPG in
  noise" — treat that as a hard acceptance criterion, not a nice-to-have.
- **No mechanics smuggled into the RPG.** The simulation may *propose* events; it may not define
  tabletop rules. Any new tabletop rule is a separate author-gated increment.

---

## 9. Files likely to change

| File | Change | When |
| --- | --- | --- |
| `docs/design/SOCIAL_SIMULATION.md` | **new** — architecture spec, three views, DEFER register | Phase 0 |
| `data/world/simulation_schema.json` | **new** — network layer + pointers to existing artefacts | Phase 0 (if GATE 1 = reuse) |
| `src/simulation/network.py` | **new** — NetworkX multiplex layer | Phase A |
| `src/simulation/ideology_engine.py` | **new** — LaclauGPT-inspired ideological state + tick | Phase A |
| `src/simulation/mesa_model.py` | **new** — Mesa scheduler | Phase A (guarded import) |
| `src/simulation/world_state.py` | **possibly extend** the reducer with new action_types (shape only, no derived scalars) | Phase A/B |
| `requirements-sim.txt` | **new** — optional Mesa/NetworkX extra (GATE 3) | Phase A |
| `tests/test_issue152_simulation.py` | **new** — structure guard | Phase A |
| `RULEBOOK.md` / `rulebook/*.md` | **only** if the author wants a one-paragraph "living world" note in the GM section | gated |

---

## 10. Verification

- The **existing** suite (801 tests) must stay green after every phase — this layer must not move
  the core.
- New guard `tests/test_issue152_simulation.py` pins: (a) the docs/spec exists and names the three
  views; (b) the core path imports no Mesa/NetworkX; (c) the schema reuses the event envelope and
  the Affect graph rather than re-declaring them; (d) determinism (same seed → identical state).
- **Sabotage-test** each guard before claiming it works (house convention).
- If Mesa is added, confirm CI still installs only `requirements.txt` and the sim tests skip cleanly
  without Mesa (they must not fail the build).

---

## 11. Risks, tradeoffs, open questions

- **Biggest risk:** building a second state model that becomes canon by accident (§3). Mitigation:
  GATE 1 + the "no stored derived scalars" invariant + a guard.
- **Theory-fidelity risk:** simplifying LaclauGPT into "propaganda points" would violate
  `INV_ANTAGONISM`/`INV_AFFECT`. The ideological engine must keep frontier and affect as evidenced
  relations, not scores.
- **Dependency risk:** Mesa's scheduler is stochastic; determinism (GATE 4) is what makes replay and
  "what-if?" runs trustworthy.
- **Legibility risk:** the richest failure mode is a technically-correct simulation no GM can read.
  The GM digest is a first-class deliverable, not a log.
- **Open (author):** GATE 1–6. **Open (research):** the issue's own eight research questions.

## 12. Deliberately NOT in this plan

- Implementing any of Phase A–C before GATEs clear (this is planning only, per the author).
- Any tabletop **rule** — the simulation proposes, the author disposes.
- Global/planetary scope (Phase C) — the default campaign is Helsinki-centred.
- The strategy layer's own mechanics — that is the #153 plan.
- A LaclauGPT code dependency — GATE 5 decides whether NoöPunk *calls* it or *ports a subset*.
- Any change to `AGENTS.md`, the design invariants, or §33 world-canon.
