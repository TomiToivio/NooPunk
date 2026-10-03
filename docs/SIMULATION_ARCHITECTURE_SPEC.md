# NoöPunk Simulation Architecture Specification

> **Status: Phase A specification (issue #40). Documentation only.**
>
> This document defines **interfaces, boundaries, and open questions**. It defines
> **no** rules, mechanics, lore, factions, statistics, or simulation semantics.
>
> It is deliberately not an implementation. Per [`../AGENTS.md`](../AGENTS.md) §2,
> NoöPunk advances one layer at a time, and §4 leaves social mechanics, factions,
> detailed simulation mechanics, professions, economy and most world systems
> explicitly **unresolved**. A document that invented the neighbourhood-crisis
> mechanics in order to look complete would be violating §1, not satisfying #40.
>
> Where a decision is required, this document records it in the
> [DEFER register](#11-defer-register) instead of choosing it.
>
> Issue #40's Phase A items are answered as: **1** [state model](#2-canonical-state-model),
> **2** [event format](#3-event-format), **3** [simulation vs empirical separation](#5-simulation-vs-empirical-separation),
> **4–6** [mapping](#9-mapping-rulebook-laclaugpt-and-pcm-into-state) (with the
> unresolved parts deferred), **7** [tabletop macro mechanics](#10-tabletop-macro-mechanics-minimum),
> **8** [Concordia API review](#7-concordia-integration-boundary-and-api-review).

## 1. Scope and the three views

Issue #40 defines NoöPunk as one evolving world with three views:

| View | Who acts | What may write to shared state |
|---|---|---|
| **Tabletop RPG** | humans at a table | events, via the same log as every other view |
| **Godot** | humans, via the UI | events, via the shared API |
| **Concordia** | LLM agents + institutions | events, via the GM/resolver seam |

The binding architectural rule, restated from the issue so it cannot drift:

> **One shared world state + one event log, with multiple interfaces.**

An interface may *read* state freely. An interface must not hold canonical state of
its own, and must not write state except by emitting an event that a reducer has
accepted. This is the single rule that makes the three views the same world rather
than three products.

Canonical order from [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) and
`AGENTS.md` §3/§11/§14 still governs *development order*:
**tabletop rules first → digital specification → Godot → Concordia.** Nothing here
authorises implementing a runtime ahead of its tabletop rule.

## 2. Canonical state model

### 2.1 Status of this vocabulary

Issue #40 proposes a list of entity kinds and relation types. **That list is a
proposal in an issue, not an author decision.** This section therefore records it
as a *candidate vocabulary* to be confirmed or replaced by the author, and the
schema is defined by what it must support rather than by a frozen enumeration.

Two consequences, both deliberate:

- **No enumeration is declared canonical here.** Writing a `kind` enum into a
  shared schema is exactly the "invent canon by implementing it" failure that
  `AGENTS.md` §1 forbids.
- **The schema must accept an open kind/relation vocabulary.** An open string with
  a documented registry is reversible; a closed enum is not (see `AGENTS.md` §10,
  "prefer reversible architecture").

### 2.2 What the state model must support

Issue #40 requires the model to be graph-friendly, technology-neutral, and usable
without a graph database initially. The following are requirements on the schema,
not content in it:

1. **Entity records.** Every entity has a stable id, a kind, a label, and a
   country/platform/time context where applicable.
2. **Typed relations between entities.** Directed, and carrying the same
   provenance discipline as the entities they connect.
3. **Provenance on everything.** Which event produced this entity or relation,
   and therefore which view and which actor.
4. **Open vocabularies.** `kind` and `relation` are strings validated against a
   registry, so new kinds are additive and no kind becomes canon by appearing in
   code.
5. **No mechanics.** The state model stores *what happened and who relates to whom*.
   It does not store derived statistics, power, legitimacy, cohesion, or any other
   quantity until the author specifies what those mean. Storing an unspecified
   number is inventing a mechanic.

### 2.3 Candidate vocabulary (awaiting author confirmation)

Recorded from the issue verbatim in intent, so the author can accept or rewrite it
in one place. **Unconfirmed:**

- **Entity kinds (candidate):** persons/characters; LLM or synthetic agents;
  groups; factions; organizations; corporations; states; institutions; media;
  platforms; technologies; places; resources; communications; events;
  concepts/signifiers; demands/claims; political formations; governance
  proposals/decisions.
- **Relation types (candidate):** `communicates_with`, `member_of`, `controls`,
  `funds`, `trusts`, `opposes`, `allies_with`, `influences`, `articulates`,
  `represents`, `regulates`, `owns`, `depends_on`, `observes`, `responds_to`.

The relation list in particular must not be frozen before
[§9.3](#93-pcm-concepts) and [§8.2](#82-which-theory-accounts-for-what) are
resolved: several of these relations are *theory-laden* (`articulates`,
`influences`, `trusts`) and carry commitments that `AGENTS.md` §13 requires to be
cited in the theoretical-source register before they become canonical mechanics.

### 2.4 Recommended storage shape (proposal, not requirement)

The issue suggests SQLite + NetworkX + JSON/JSONL, with optional later
MongoDB/RDF adapters. This is recorded as a **proposal**. No storage decision is
binding in Phase A. The only binding property is that state must be derivable from
the event log ([§4](#4-event-sourcing-as-the-spine)), so no store may be the sole
home of a canonical fact.

One thing the issue states directly and this document treats as binding: **every
simulation run must have a unique `simulation_id`**
([§3](#3-event-format), [§5](#5-simulation-vs-empirical-separation)).

## 3. Event format

Every state change is an event. The envelope below is the **minimum** set of
fields the architecture requires; the issue's own example is the starting point.

Required fields, with the reason each exists:

| Field | Why it is required |
|---|---|
| `simulation_id` | isolates one run; makes replay and branching addressable |
| `event_id` | stable identity so replay is idempotent and de-duplication is possible |
| `turn` | ordering within a run; the issue's own turn loop depends on it |
| `timestamp` | wall-clock record; **not** a substitute for `turn` ordering |
| `actor` | who acted (entity id, including synthetic agents) |
| `action_type` | what kind of act; open vocabulary, registry-validated |
| `target` | who/what it was directed at, where applicable |
| `content` | the substance — utterance, statement, decision |
| `location` | place context, where applicable |
| `visibility` | public/private; the LaclauGPT layer consumes *public* communications |
| `source` | which view emitted it: `tabletop` / `concordia` / `godot` / `system` |
| `synthetic` | explicit synthetic marker (see [§5](#5-simulation-vs-empirical-separation)) |

Two schema rules matter more than the field list:

1. **Ordering is `turn`, never `timestamp`.** Timestamps collide, drift, and are
   not reproducible. Any reducer ordering by timestamp is a correctness bug.
2. **`source` and `synthetic` are set by the emitting boundary, not by the actor.**
   An LLM agent must not be able to emit an event claiming to be tabletop-sourced
   or non-synthetic. The envelope's provenance fields are written by the runtime
   seam ([§7.4](#74-the-mandatory-resolver-seam)), so "this is synthetic" is
   structurally true rather than self-reported.

An event is **immutable once logged**. Corrections are new events.

## 4. Event sourcing as the spine

The issue's rule — *do not let Concordia, Godot, or an LLM directly mutate
arbitrary state* — is the central architectural constraint. Its consequences:

- **State is a function of the event log.** `state = reduce(events)`. Anything not
  derivable this way is not canonical.
- **Reducers are deterministic.** Same events in, same state out. This is what makes
  the issue's reproducibility, replay, save/load, branching and auditability
  requirements achievable at all.
- **Branching is a log operation**, not a state copy: a branch is a new
  `simulation_id` that shares a prefix of events and diverges at a turn.
- **The log is the research artifact.** The issue notes LaclauGPT analysis should
  operate on the event/communication stream — so the log, not a dashboard, is the
  interface to the social-science layer.

Consequence for the LLM (binding, and the reason for the Concordia finding in
[§7.2](#72-finding-concordias-world-state-components-are-llm-generated)):
**an LLM proposes; the reducer decides.** Model output may become an event only
after a deterministic resolver has accepted it.

## 5. Simulation vs empirical separation

The issue requires synthetic simulation data to be **impossible to confuse** with
empirical LaclauGPT research data. "Impossible" is a strong claim and needs more
than a convention. The specification's position:

1. Every event carries `synthetic` and `simulation_id`. There is no default;
   the field is required and set at the emitting boundary.
2. **Exported artifacts carry the marker in their identity**, not only in a column
   — a filename or dataset id that cannot be mistaken for an empirical export.
3. The LaclauGPT adapter ([§9.2](#92-laclauGPT-concepts)) is an *export path with a
   marker*, never a shared store. Synthetic and empirical data must not land in the
   same collection, table, or directory.
4. Anything derived from simulated communications inherits the marker transitively.

The concrete enforcement mechanism (schema constraint, separate database, or
export-naming rule) is **deferred** — the requirement is stated, the mechanism is
the author's call. See [DEFER-4](#11-defer-register).

## 6. The RPG ↔ society bridge

Issue #40 §8 is the project's central mechanic: character-scale action must change
society, and society must change what a character can do. Architecturally this is
**not** a new subsystem — it is a property that falls out of the event spine:

- The character action is an event with `source=tabletop`.
- The LaclauGPT/PCM/assemblage adapters are **reducers and observers over the same
  log**, so a character's public communication is visible to the discourse layer
  without any character-specific plumbing.
- The changed state is what the next scene reads.

Two honest limitations, stated rather than papered over:

1. **The bridge's *content* is unspecified.** The issue's examples (leaking
   corporate data, saving a neighbourhood, killing a faction leader, uploading an
   autonomous LLM) are illustrations, not rules. *What* a leaked dataset does to a
   faction is a social mechanic, and social mechanics are in `AGENTS.md` §4's
   unresolved list. This document defines the pipe; it does not define what flows
   through it.
2. **"The organisation does not simply disappear"** (the issue's succession
   example) is a substantial institutional mechanic and is **deferred**, not
   designed here.

So the bridge specification is: *any macro effect reachable from a character action
must be reachable as a sequence of logged events and reducer steps, with no
character-specific back channel.* That is checkable in Phase B. The rules that
determine the effects are Phase A's deferred content.

## 7. Concordia integration boundary and API review

### 7.1 Role

Concordia executes NoöPunk rules; it does not replace them. It supplies agent
infrastructure (entities, components, Game Masters, engines) and LLM-driven
intention/utterance/roleplay. Canonical rules, state, and numeric resolution stay
in NoöPunk.

### 7.2 Finding: Concordia's world-state components are LLM-generated

**This was established by reading the pinned revision, not from memory.**
`requirements-concordia.txt` pins
`git+https://github.com/google-deepmind/concordia.git@405584db8e09e001da6deb147a6389f7a7f44e28`.
At that revision, `concordia/components/game_master/world_state.py`:

- class `WorldState`, `post_act(event)`: calls
  `prompt.open_question('... what state variables are important ... Respond with a
  comma-separated list of variable names ... in the format "name|value" ...')` and
  writes the parsed result into `self._state`.
- class `GenerativeClock`, `post_act(event)`: **time itself is model-generated** by
  `self._time = prompt.open_question('... what is the new time? ...')`.

This conflicts with three explicit #40 requirements:

| #40 requirement | Why LLM-generated state breaks it |
|---|---|
| "Rules code resolves rules" | the model, not the rules, is writing the canonical state |
| reproducible runs / replay / branching | a sampled world state is not reproducible |
| `AGENTS.md` §12 | prompts must not silently become canon |

**Architectural decision recorded:** NoöPunk owns its world state and its clock.
Concordia's `WorldState`/`GenerativeClock` components are **not** the canonical
store, and must not be used as one. They may, if the author later wants, provide a
*narrative* state for agent flavour — but a narrative state is not canonical state
and must not be readable as it.

This is the single most consequential finding of the Phase A review: without it,
the simulator's world state is "whatever the LLM narrated", which the issue
explicitly forbids.

### 7.3 The deterministic seam Concordia already provides

Usefully, Concordia's entity component protocol has a **`post_act` hook that is
called on a GM resolution**, and its `ActionSpec.output_type` includes
`OutputType.RESOLVE` alongside the choice/next-acting/terminate types
(`concordia/typing/entity.py`). That is the correct integration seam:

- the LLM proposes the *action* (`FREE`/`CHOICE` free text);
- the GM's resolution step is where **NoöPunk's deterministic resolver** runs and
  produces the canonical `RESOLVE` outcome;
- the outcome becomes an event; the reducer applies it.

The engine variants available at the pinned revision (`sequential`,
`simultaneous`, `asynchronous` under `concordia/environment/engines/`) determine
turn ordering, and `Sequential` reads an action spec from the GM string
(`engine_lib.action_spec_parser`). Which engine NoöPunk uses is **deferred** — it
depends on whether a turn resolves players simultaneously, which is itself a
tabletop rule not yet specified ([DEFER-6](#11-defer-register)).

### 7.4 The mandatory resolver seam

Binding interface rule, stated so Phase C cannot skip it:

> No LLM output may enter the event log except through the deterministic resolver.
> Where a canonical rule exists, the resolver must reach the rule through the
> shared rules layer — not through a re-implementation inside Concordia
> (`AGENTS.md` §13: a rules difference between runtimes is a defect). Where no rule
> exists, the resolver must return an *explicit unresolved outcome*, not an
> improvised one.

The last clause is the important one: it converts "the rule isn't written yet" from
a silent invention into a visible gap.

## 8. Assemblage and communication layers (interfaces only)

The issue asks for a Deleuzian/DeLandian assemblage layer and a Luhmannian
communication layer, and explicitly asks that the theory division of labour be
**investigated and documented** rather than collapsed.

### 8.1 What this document does and does not do

It records the **distinction** the issue requires and the **interface seam** each
layer needs. It does **not** define assemblage formation rules, territorialisation
semantics, or communication-system emergence criteria — those are mechanics, and
per `AGENTS.md` §13 they must be cited in
[`THEORETICAL_SOURCES.md`](THEORETICAL_SOURCES.md) before becoming canonical.

The issue's own guardrail is adopted verbatim as a design constraint:
**an assemblage is not the same thing as a network community.** SNA-style graph
properties are *one* measurable aspect, not a definition.

### 8.2 Which theory accounts for what

The issue lists Deleuze/DeLanda, Luhmann, Laclau, Castells, Leifeld/DNA, SNA and
PCM and warns against collapsing them. The mapping below is a **proposal for the
author to confirm**, phrased so each theory owns a distinct question:

| Theory | Owns the question | Not responsible for |
|---|---|---|
| Deleuze / DeLanda | what heterogeneous components are bound together, and how stable that binding is | counting edges; political outcomes |
| Luhmann | how communication recursively reproduces itself into a system | the content/meaning of what is communicated |
| Laclau | how demands articulate into equivalential chains and antagonisms | network structure; governance rules |
| Castells | communication networks and network power | the normative evaluation of that power |
| Leifeld / DNA | the actor↔concept bridge (coded statements) | whether the stance is *true* |
| SNA | measurable structure of whatever graph exists | what the structure *means* |
| PCM | governance mechanics for heterogeneous human/AI collectives | declaring an outcome correct |

Confirming or correcting this table is an **author decision** ([DEFER-7](#11-defer-register)).
It is deliberately phrased as "owns the question", which is falsifiable, rather
than as a vocabulary mapping, which would smuggle in semantics.

## 9. Mapping RULEBOOK, LaclauGPT and PCM into state

The issue's Phase A items 4–6 ask for these mappings. The honest result of reading
the current sources is that **most of the mapping cannot be written yet**, and the
reason is structural, not laziness.

### 9.1 RULEBOOK mechanics → canonical state

**What exists and maps cleanly:** attributes (six, author-specified), 3d6
ordinary-human attribute generation, the 2d6 skill-check engine, difficulty ladder,
the skill list and the level-0..4 scale (`RULEBOOK.md`; note
`data/rules/core.json` still holds the **superseded 3d6-era** values and is not
canonical — see `AGENTS.md` §13/§15 and RULEBOOK §17.1).

**What cannot map:** social mechanics, factions, institutions, economy,
advancement, combat resolution, and detailed simulation mechanics are all in
`AGENTS.md` §4's unresolved list. There is therefore **no tabletop macro mechanic to
map** for the society-scale state that #40 §8 and §9 require.

**Recorded consequence:** the RPG→society bridge ([§6](#6-the-rpg--society-bridge))
has a defined pipe and no defined contents, and the missing contents are a
**tabletop-first** gap: per `AGENTS.md` §14 the correct action is to specify the
tabletop macro rules first, not to invent them in the simulation.

### 9.2 LaclauGPT concepts

The issue lists actors, concepts, signifiers, demands/claims, equivalential
relations, antagonisms, nodal points, floating/empty signifiers, discourse
formations, actor-concept networks, communication networks, institutional/platform
context and temporal change.

Mapping these into shared state is **mostly blocked**, and the block is a *source*
question: LaclauGPT's canonical vocabulary lives in the LaclauGPT repository, not
here. NoöPunk must not re-define Laclau's terms locally to make state shapes
convenient — that would create the competing source of truth that
`AGENTS.md` §13 and the single-source-of-truth test in `test_design_principles.py`
exist to prevent.

**So the Phase A output for this item is an interface requirement, not a mapping:**
the adapter must consume LaclauGPT's vocabulary as an external contract, and the
author must state which of those terms are shared canonical concepts versus
LaclauGPT-local analysis labels. **Deferred** ([DEFER-8](#11-defer-register)).

Also deferred, and deliberately: the issue's "do not require every mechanism to be
LLM inferred" is adopted as a constraint, but *which* mechanisms become explicit
graph mechanics is a design decision.

### 9.3 PCM concepts

Same structure, same block. The issue lists governance proposals, commons,
rights, membership, representation, delegation, federation, conflict resolution,
human/AI participation, collective ownership, legitimacy, exit/voice/fork and
distributed coordination.

NoöPunk must consume PCM's vocabulary as an external contract, and the issue's
constraint that **PCM outcomes are not automatically correct** — the simulator is a
laboratory — is adopted as binding. The mapping itself is **deferred**
([DEFER-8](#11-defer-register)), for the same single-source reason.

## 10. Tabletop macro mechanics (minimum)

Issue #40 §9 requires the tabletop version to stay playable without a computer and
asks for "a compressed human-resolvable form of macro simulation". It proposes
Faction/Assemblage sheets with relationship map, key signifiers, resources,
legitimacy, cohesion, reach, institutional power, network position, demands,
antagonisms, and clocks/tracks.

**This is the item where the temptation to invent is strongest and the prohibition
is clearest.** Naming a sheet field is naming a mechanic:
"legitimacy", "cohesion", "reach" and "institutional power" are quantities whose
meaning, scale, and interaction are exactly the social mechanics that `AGENTS.md`
§4 reserves to the author, and that §15 requires be **left unresolved rather than
filled with another system's defaults**.

Therefore Phase A records:

- the **requirement** (tabletop play must not depend on software, and every
  society-scale effect the digital simulation produces must have a human-resolvable
  tabletop form);
- the **candidate field list from the issue**, explicitly unconfirmed;
- **no field is defined, scaled, or given a resolution procedure.**

That preserves the author's ability to specify the macro system without
retrofitting it past a speculative implementation. See
[DEFER-9](#11-defer-register).

## 11. DEFER register

Every decision this specification refuses to make, with the reason and the owner.
This is the document's most important section: it is the difference between a
specification and an invention.

| ID | Deferred decision | Why it must not be an agent's call | Owner |
|---|---|---|---|
| DEFER-1 | Canonical entity-kind enumeration | declaring an enum makes proposed vocabulary into canon (`AGENTS.md` §1) | author |
| DEFER-2 | Canonical relation-type enumeration | several relations are theory-laden and need source-registry entries (§13) | author |
| DEFER-3 | Storage backend (SQLite / Mongo / RDF) | reversible architecture is preferred until the state shape is stable (§10) | author |
| DEFER-4 | Synthetic/empirical enforcement mechanism | requirement is clear; mechanism affects research workflow | author |
| DEFER-5 | Simulation scale-aggregation rules | "do not simulate every individual" needs an aggregation policy | author |
| DEFER-6 | Concordia engine choice + turn resolution order | depends on the tabletop turn rule, which is unspecified (`AGENTS.md` §14) | author |
| DEFER-7 | Theory division of labour (§8.2 table) | collapsing or assigning theories is a methodology decision | author |
| DEFER-8 | LaclauGPT / PCM shared-vocabulary boundary | the terms are canonically defined in *other* repositories | author |
| DEFER-9 | Tabletop macro-mechanic field set and resolution | social mechanics are in `AGENTS.md` §4's unresolved list | author |
| DEFER-10 | Which mechanisms are explicit graph mechanics vs LLM-inferred | the issue sets the preference; the division is a design choice | author |
| DEFER-11 | Success criteria/metrics for "macro effect is observable" | metric design is research methodology | author |

An agent encountering one of these must return an unresolved outcome, not a
plausible default ([§7.4](#74-the-mandatory-resolver-seam)).

## 12. What Phase A leaves for later phases

Stated so the boundary is auditable rather than implied:

- **Phase B** (deterministic core: SQLite + event log, reducer, replay/branch,
  tests) — **implemented**: `src/simulation/` (`events.py`, `sqlite_store.py`,
  `world_state.py`, `engine.py`), 43 behaviour tests in
  `tests/test_issue40_simulation_core.py`. It uses a clearly non-canonical
  `fixture:` vocabulary, which is exactly the route this section predicted, so
  DEFER-1/2/3 need not be answered first. What Phase B deliberately does **not**
  contain: any social mechanic, and the graph/assemblage layer (`src/simulation/`
  has no graph module yet — assemblages are DEFER-7 territory).
- **Phase C** (Concordia prototype) depends on DEFER-6 and on a specified tabletop
  turn rule.
- **Phase D** (LaclauGPT + PCM adapters) depends on DEFER-8.
- **Phase E** (RPG integration) depends on DEFER-9 — it cannot integrate a macro
  system that does not exist.
- **Phase F** (Godot) is unaffected structurally: it is a client over the same
  event API.

The dependency chain is the honest answer to "why is Phase A only a document":
**the project's own invariant is tabletop-first**, and the tabletop macro layer is
specified by the author, not derivable by an agent.

## 13. Relationship to existing documents

This document deliberately does not restate them:

- [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) — the three balances; binding.
- [`THREE_LAYERS.md`](THREE_LAYERS.md) — material/ontological/social setting layers.
- [`CONCORDIA_ARCHITECTURE.md`](CONCORDIA_ARCHITECTURE.md) — the infrastructure-only
  Concordia runtime and its port debt.
- [`THEORETICAL_SOURCES.md`](THEORETICAL_SOURCES.md) — where each theory's claim and
  NoöPunk's interpretation are kept separable.
- [`PROJECT_CONVERGENCE.md`](PROJECT_CONVERGENCE.md) — the conceptual LaclauGPT/PCM
  synthesis.
- [`../AGENTS.md`](../AGENTS.md) — the binding agent rules this document obeys.
