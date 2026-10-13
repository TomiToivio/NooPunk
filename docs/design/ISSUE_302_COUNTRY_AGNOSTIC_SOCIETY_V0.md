# Country-agnostic society V0 (#302): systems, organizations, networks and discourse

**Status: PROPOSAL — design only, no mechanics.** This document answers design tasks 1–6 of
[#302](https://github.com/TomiToivio/NooPunk/issues/302). **Task 7 (any Python implementation) stays
blocked** on author approval, per this issue's own instruction: *"Discussion/research first; do not
implement unapproved mechanics."* No rule, number, threshold, subsystem count or faction position is
approved here. `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**. This is one new file; no
existing document, schema or module is edited, and it defines nothing the scaffold must obey.

The three lenses stay **separate registers**, not one blended formula: Luhmann supplies functional
differentiation, Castells the communication topology, Laclau the articulation of meaning. Where they
tension, this document says so instead of synthesising them.

---

## 0. What this consumes (and must not duplicate)

The scaffold already contains more of this model than the issue's framing assumes. Everything below is
read from `main`, and the design reuses it rather than declaring a parallel vocabulary.

| Concept | Existing home | Verdict |
| --- | --- | --- |
| Political actor | `strategy_game/core.py` → `Faction` | reuse |
| Individual | `strategy_game/core.py` → `Leader` | reuse |
| Institution / holding | `strategy_game/core.py` → `Asset` | reuse (partial — see §2) |
| Place | `strategy_game/core.py` → `Location` | reuse |
| Any tie, including political ones | `strategy_game/core.py` → `NetworkEdge(source, target, layer)` | reuse |
| A record of something that happened, with its origin | `strategy_game/core.py` → `Event(identifier, description, provenance)` | reuse |
| Origin / reality status | `strategy_game/provenance.py` → `Provenance`, `ProvenanceKind` | reuse |
| Discourse records | `strategy_game/politics.py` → `Demand`, `Signifier`, `Formation`, `Frontier` | reuse |
| Signifier role | `strategy_game/politics.py` → `SignifierKind` (`unspecified`/`nodal`/`floating`/`empty`) | reuse |
| Relation labels | `strategy_game/politics.py` → `RelationLayer` (`articulation`/`equivalence`/`antagonism`/`communication`) | reuse |
| Political node typing | `strategy_game/politics.py` → `PoliticalNodeKind` | reuse |
| Layer boundaries | `strategy_game/ports.py` → `LeaderRPG`, `FactionStrategy`, `PoliticalSimulation`, `AgentProvider`, `AgentRunner`, `MapProvider` | reuse (signatures only) |
| Serializable state | `strategy_game/core.py` → `WorldState` | reuse |

The standing prohibition holds: this is **not** LaclauGPT integration, and the Phase 1 analytical
taxonomy must not be turned into causal transition formulas
(`strategy_game/docs/INTEGRATION_BOUNDARIES.md`).

---

## 1. The one-page tabletop-first model (task 1)

Six terms. Each is classified by what it *is*, because the issue asks that analytical category, authored
scenario input and game rule never be confused:

| Term | What it is | Class |
| --- | --- | --- |
| **System** | A functionally differentiated mode of communication (politics, law, economy, science, mass media). A way of *reading* an event. **Not an agent, not a player, not a node with preferences.** | analytical category |
| **Organization** | A declared institution that participates in one or more systems (a ministry, a court, a laboratory, a broadcaster). | authored scenario input |
| **Faction** | A declared political actor with claims and a leader. | authored scenario input, stored as the existing `Faction` |
| **Audience** | Declared receivers that a communication reaches, or fails to reach. | authored scenario input |
| **Event / communication** | A declared record, plus the ties that carried it. | authored scenario input, stored as the existing `Event` + `NetworkEdge` |
| **Structural coupling** | The recorded fact that one system *responded to* another system's output. | game rule — **proposed, unapproved** |

**The load-bearing rule:** a system never acts. "Science responds" is shorthand for *an organization
that participates in scientific communication produced an output under that system's code*. This is what
keeps the model honest and keeps the issue's non-goal — a sprawling agent simulation — out.

The **country is a scenario boundary**, not a model of a nation: it is the label on a bounded local
observation of world society. Which subsystems exist, and how many, remain author-approved choices
(§9), and religious communication may be scenario-specific rather than always present.

---

## 2. Reuse map and the three real gaps (task 2)

`strategy_game/core.py` already declares the node and edge universe; `politics.py` already declares the
discourse records. The societal layer therefore **adds no node class and no edge collection**. Three
concepts the issue names have **no home today**, and these are genuine gaps rather than oversights to
paper over:

1. **`Organization` — missing.** `WorldState` holds `leaders`, `factions`, `assets`, `locations`,
   `edges`, `events`, `demands`, `signifiers`, `formations`, `frontiers`. There is no organization. The
   nearest existing records are `Asset` (a holding with an owner) and `Location` (a place). A ministry
   is neither: it is an institution that *participates in several systems* and need not be owned by a
   faction. §6 proposes the smallest record that closes this.
2. **`Audience` — missing.** Receivers are currently only implicit as `NetworkEdge.target` nodes and as
   `Location`s. §6 proposes an optional record; the fallback is to keep using edge targets.
3. **Structural coupling — missing.** `RelationLayer` offers `articulation`, `equivalence`,
   `antagonism` and one Castells tie, `communication` — all *discourse/network* labels. None of them
   says "one system responded to another's output", which is #302's central concept. Adding a fifth
   `RelationLayer` would be wrong: coupling is not an edge between two actors, it is a relation between
   two *registers*. §6 proposes it as its own record instead.

**Diagram — systems as registers, organizations as nodes, one multiplex graph:**

```
   REGISTERS (analytical, not agents)          ONE DECLARED GRAPH (core.WorldState.edges)
   ┌────────┬────────┬─────────┬──────────┐    ┌──────────────────────────────────────────┐
   │politics│  law   │ science │  media   │    │  Organization ──communication── Audience  │
   │economy │  ...   │         │          │    │        │                                  │
   └───┬────┴───┬────┴────┬────┴────┬─────┘    │  Faction ──articulation── Signifier       │
       │        │         │         │          │        │                                  │
       └────────┴────┬────┴─────────┘          │  Demand ──equivalence──▶ Demand            │
                     │                        │     │                                     │
             Event + Provenance ──────────────▶│  Frontier ──antagonism──▶ Formation       │
        (authored / evidence / claim,          │        (layer label on NetworkEdge)        │
         never silently upgraded)              └──────────────────────────────────────────┘
                     │
        ┌────────────▼─────────────┐
        │  Coupling (proposed):     │  one register responded to another register's output
        │  source_system →          │  RECORDED, not scored: no strength, no causation
        │  target_system, event_id  │
        └───────────────────────────┘
```

**Adapters** (`ports.py`) sit beside these registers, unchanged: each is
`describe(state: WorldState) -> object`, signature only. `MapProvider` explicitly must not infer
borders, travel, control or ownership.

---

## 3. One multiplex graph (task 2, "avoid duplicate classes")

`core.py` states the rule this design inherits:

> *Political relations are ordinary `NetworkEdge` entries in `edges` carrying a `RelationLayer` label —
> there is deliberately no second edge collection, so the whole political field stays one multiplex
> graph.*

The societal layer adds **no second edge collection either**. Communication reach, articulation,
equivalence and antagonism are all `layer` labels on the same `edges` list. This is what lets the
acceptance criterion — *"which connections carried its communications"* — be answered by reading one
list, and it is why an `Organization` record (§6) must be a *node*, not a parallel graph.

---

## 4. Single event walkthrough (task 3)

One incoming event, the issue's own example: a disputed announcement of anomalous results (fictional; in
Noöpunk register this could be a *PSI research announcement* or an *NHI disclosure claim*).

**The record.** `Event(identifier, description, provenance)`. The `provenance` field is what keeps the
issue's reality-status rule: the announcement enters as `reported_claim` or `authored`, **never**
`evidence`, and an in-game announcement is not a statement about actual science. Provenance is a
separate field precisely so description and origin never blur.

**The same event, read five ways — divergent responses, not one score:**

| Register | Reads the event as | Produces (authored output) |
| --- | --- | --- |
| Science | a claim requiring method and replication | a review announcement, a refusal to comment |
| Law | a question of jurisdiction and permission | a hearing, a licensing decision |
| Mass media | a story with reach and an audience | coverage, or silence |
| Economy | a risk and an investment signal | insurance, funding, or divestment |
| Politics | a demand to be articulated | a claim, a coalition, a frontier |

**How communications travel.** Reach is mediated by edges, not by truth: an organization *receives* the
event only if a `communication` tie carries it. A truthful claim with no edges reaches nobody; a false
one with a broadcaster's edges reaches everybody. The model records reach as edges; it does **not**
derive legitimacy or hegemony from it.

**How factions frame it.** A `Demand` is linked to a `Signifier` by an `articulation` edge; two demands
may be linked by `equivalence` rather than by shared content; a `Frontier` carries `antagonism`. Mere
disagreement is not antagonism, and no universal hegemony score exists.

**Where player choices enter.** Not in the registers — a leader spends a move on an *organization*
(#295/#296's four-leader economy), and a faction attempts an *articulation* (#297's discourse layer).
The societal layer is context: it decides what the move is *read as*, not what it costs.

**Trace.** Every output carries its origin. Consequences are labelled authored / game-generated, and
never presented as empirical findings — which is acceptance criterion (4).

### Acceptance-criteria self-check

| Criterion | Where it is answered |
| --- | --- |
| (1) why the same event matters differently to science, law, media, economy, politics | the five-register table above |
| (2) which connections carried its communications | the single `edges` list, `layer == "communication"` (§3) |
| (3) how factions politically framed it | `Demand` / `Signifier` / `articulation` / `frontier` (§4) |
| (4) which consequences are authored rather than empirical | `Event.provenance` + labelled outputs (§4) |

---

## 5. Two possible abstractions, and the smaller one (task 4)

| | **(A) Systems as passive filters / lenses** | **(B) Systems with limited approved state** |
| --- | --- | --- |
| Stored state per system | none | a little, approved per system |
| Rendering one event | one event, several readings | reads *and* transitions between readings |
| Legibility | high — a system is a way to read | lower — needs a per-system state table |
| Agency | player agency stays entirely in #295/#296/#297 | same, but with extra levers |
| Replayability | the *inputs* vary, the lens is constant | state can diverge and compound |
| Theoretical honesty | high — no system "wants" anything | risks implying systemic drives |
| New rules required | none | yes, and each needs approval |

**Recommendation: (A).** It is the smaller option, it introduces no unapproved mechanic, and it keeps
the issue's own boundary — Luhmannian systems *"do not replace any of those three playable layers; they
provide their shared societal context."* (B) becomes interesting only after a specific transition rule
has been authorised, and (A) is its prerequisite rather than its rival.

---

## 6. Minimal structured records — proposal only (task 5)

Three additive records, each the smallest thing that closes a gap from §2. **None is a mechanic**: no
strength, cost, duration, threshold or causal weight appears in any of them.

```
Organization                       # closes gap 1: institutions as nodes
  id, label, participates_in[]     #   system names it communicates under — a list, not a score
  location_id?, provenance

Coupling                           # closes gap 3: cross-system response, recorded
  id, source_system, target_system, event_id, provenance
                                   # "one register responded to another's output".
                                   # No strength. No direction of causation beyond the recording.

Audience                           # closes gap 2, OPTIONAL — edge targets may suffice
  id, label, provenance
```

**Interfaces to the three playable layers** (all additive, no layer is replaced):

| From | To | Shape |
| --- | --- | --- |
| #295 leader outcome | societal read | an organisation-level output with provenance; never a system action |
| #296 faction action | societal read | a declared move; the register supplies how it *reads*, not what it *costs* |
| #297 discourse/network result | societal read | `Demand`/`Signifier`/`Frontier` records the societal layer can cite |

The existing ports already carry this: `LeaderRPG`, `FactionStrategy` and `PoliticalSimulation` each
`describe(state)`. The societal layer needs **no fourth port** — it is a reading of the same
`WorldState`, which is also why the issue insists this is not a new engine.

---

## 7. Nation-agnostic configuration (task 6)

The country is a boundary, so swapping it must change **labels only**:

```
scenario:
  country_label: "<any name>"          # the only thing that changes
  organizations:  [{id, label, participates_in[]}, ...]
  audiences:      [{id, label}, ...]
  seeds:          [event_id, ...]
  subsystems:     [politics, law, economy, science, mass_media]   # author-approved set
```

Swap `country_label` and the organization labels and reproduce the same walkthrough unchanged: the
registers, the edge semantics, the discourse records and the provenance rules all stay identical. No
mechanics move. A scenario that needs a *different* rule is a different scenario, not a different
country — which is the whole point of country-agnosticism.

---

## 8. Non-goals and safeguards

- **Not LaclauGPT integration.** No corpus analysis, DNA extraction, RAG, Mongo/Redis, LLM
  requirement, imported empirical coefficients or purported social prediction.
- No detailed national map, historical policy simulation, elections, GDP, population ABM, or automatic
  invented canon.
- No unconstrained LLM agents. Any future optional agent may propose narrative, never silently mutate
  authoritative state (`INTEGRATION_BOUNDARIES.md`).
- **Provenance throughout:** historical evidence, authored alternate-history fiction, AI-generated
  drafts and simulated outcomes stay distinct, and an absence of provenance stays visibly unknown
  rather than being upgraded into evidence.
- The existing NoöPunk RPG is untouched, and the three-issue approval sequence is preserved.
- No test freezes this text: `INTEGRATION_BOUNDARIES.md` forbids testing lore/rulebook wording.

---

## 9. Open questions for the author (the approval gates)

1. **Which subsystems, and how many?** §1 illustrates politics, law, economy, science, mass media.
   Religious communication is deliberately scenario-specific. This is your choice, not mine.
2. **(A) or (B)** from §5? I recommend (A) and would not build (B) first.
3. **Are `Organization` / `Coupling` / `Audience` wanted at all**, and if so as records in the
   scaffold, or as scenario data outside it?
4. **Do the three collaboration checkpoints** in `INTEGRATION_BOUNDARIES.md` — (A) leader roleplay
   semantics, (B) political-simulation causal assumptions, (C) faction-management resolution — need to
   settle before even the record shapes are fixed?

Nothing above is ratified. On approval of a subset, task 7's implementation would be
standard-library-only, offline, with round-trip serialization tests — and no lore tests.

---

**Related:** parent [#282](https://github.com/TomiToivio/NooPunk/issues/282); leader RPG
[#295](https://github.com/TomiToivio/NooPunk/issues/295); faction management
[#296](https://github.com/TomiToivio/NooPunk/issues/296); discourse/network power
[#297](https://github.com/TomiToivio/NooPunk/issues/297); agent ontology and genre
[#303](https://github.com/TomiToivio/NooPunk/issues/303); optional agents and GM
[#304](https://github.com/TomiToivio/NooPunk/issues/304).
