# NoöPunk: Global — an ultra-abstract worldwide strategy RPG (design alternative)

> **DESIGN ALTERNATIVE / PROPOSAL — noncanonical, approves no mechanics, does not replace the local-city MVP ([#322](https://github.com/TomiToivio/NooPunk/issues/322)) or the shared vision ([#309](https://github.com/TomiToivio/NooPunk/issues/309)).**
>
> This document answers the checklist of issue [#338](https://github.com/TomiToivio/NooPunk/issues/338). It is an **exploration**, written to be reviewed and, if the author wishes, rejected. It **grants no rules, invents no canon, changes no code or data file, and edits none of the documents it cross-links to**. `strategy_game/RULEBOOK.md` still says *NO RULES APPROVED*, and this document does not change that. Every number, name and procedure below is **illustrative and unapproved** unless it is explicitly marked as an existing, verified component of the repository.

**Reading order.** M0 (comparison), M1 (theory-to-data), M2 (a worked tabletop turn), M3/M4 (two prototypes, described not built), M5 (what evidence would decide). Then the second half: the seven political simulators, the two tabletop models, the card taxonomy, a mock-up turn, the bookkeeping audit, and the three tabletop approaches with **one** recommendation. Sources and their verification status are in the companion ledger [`NOOPUNK_GLOBAL_SOURCE_LEDGER.md`](NOOPUNK_GLOBAL_SOURCE_LEDGER.md); the honesty of that ledger is part of the deliverable, because the issue itself warns *"verify mechanics before adopting"* and *"assuming inaccessible/unverified details."*

**Placeholder discipline.** All actor, faction, jurisdiction and institution labels used in examples are **abstract placeholders** ("Faction Alpha", "the player's leader", "a ministry"). No named character, institution, party or date is created here, and none may be read as canon. The single incident walked through in M2 and in the mock-up is the **issue's own illustrative example** — "a corporate AGI disclosure" ([#338](https://github.com/TomiToivio/NooPunk/issues/338), *Illustrative integrated turn*), not new lore.

---

## 0. Status, boundaries, and what this document is not

| | |
|---|---|
| **Game** | The NoöPunk × LaclauGPT crossover (`strategy_game/`), per [AGENTS.md](../../AGENTS.md) §0 and [#306](https://github.com/TomiToivio/NooPunk/issues/306) |
| **Relationship to #322** | A **competing scenario/design variant**, not an expansion of the local-city MVP. Both options stay on the table (M0). |
| **Relationship to #309 / VISION.md** | Consistent with the one-game, God's-eye identity; proposes a *different first slice* (whole-Earth abstraction) from the *local* first slice #322 proposes. It does not override either. |
| **Relationship to #282** | The same scaffold and the same approval gates. Nothing here is implemented, and no runtime behavior changes. |
| **Tests** | Per [AGENTS.md](../../AGENTS.md) and [#271](https://github.com/TomiToivio/NooPunk/issues/271), **no test, guard, CI step or schema lock** may check any of this prose. It is reviewed editorially and by playtesting only. |
| **Lore** | Shared lore carries over; **legacy rules do not** ([AGENTS.md](../../AGENTS.md) §0). Nothing here rewrites the legacy RPG or the existing scenario canon. |

**What this document is not.** It is not a ruleset, not a roadmap, not a promise that Global will be built, and not an argument that Global beats the local city. It is the evidence-shaped case for keeping Global alive as an option, and the specific things that would have to be measured before either option is chosen.

---

## M0 — Comparative design document: #322 local city vs Global ultra-abstract Earth

Both are the *same game seen at different zooms* — but they imply different **first slices**, different **content budgets** and different **failure modes**. Neither is the winner. This section sets them side by side so the author can choose on evidence ([#338](https://github.com/TomiToivio/NooPunk/issues/338) M0).

### M0.1 The two proposals in one line each

- **#322 local-city MVP.** One generically-located small city and its environs; 5–8 abstract districts; 3–5 factions of four named leaders; the wider world arrives as an **external event feed**, not as a board. Full design note: [`strategy_game/docs/MVP_LOCAL_CITY_M0.md`](../../strategy_game/docs/MVP_LOCAL_CITY_M0.md).
- **Global ultra-abstract Earth.** The whole planet represented *as society, not terrain*: a compact multiplex network of organizations, named people, jurisdictions-as-context and function-system interfaces; a leader with a small agent roster acting through discourse, networks, institutions and covert operations. A handful of transnational factions, not 175 country models. Pitch: [#338](https://github.com/TomiToivio/NooPunk/issues/338).

### M0.2 Shared components — what could actually be reused

The scaffold already carries more of Global than a fresh start would. Reuse means **consume the existing container/vocabulary**, not fork it ([`strategy_game/docs/INTEGRATION_BOUNDARIES.md`](../../strategy_game/docs/INTEGRATION_BOUNDARIES.md)):

| Existing artefact | Home | Reusable for Global? | Note |
|---|---|---|---|
| `WorldState` + `Leader`, `Faction`, `Asset`, `Location`, `NetworkEdge`, `Event` | [`../strategy_game/core.py`](../../strategy_game/core.py) | **Yes, as-is** | `Location` is already a *point* (lat/long), so it scales from a city district to a global node without a schema change. `NetworkEdge.layer` already makes the graph multiplex. |
| `Demand`, `Signifier`, `Formation`, `Frontier`, `RelationLayer` | [`../strategy_game/politics.py`](../../strategy_game/politics.py) | **Yes, as-is** | The political field is already **one labelled multiplex graph**; articulation/equivalence/antagonism/communication are edge labels. Laclau's content, Castells' ties and the game board share one structure. |
| `Provenance` / `ProvenanceKind` (unknown-by-default) | [`../strategy_game/provenance.py`](../../strategy_game/provenance.py) | **Yes, as-is** | The evidence/claim/rumour discipline Global needs is already here. A faction's PSI/NHI posture is a *claim it holds*, not a fact the game asserts. |
| `board_view` / `political_view` | [`../strategy_game/view.py`](../../strategy_game/view.py) | **Yes** | Already emits `network_nodes` (factions + political nodes) and `network_edges`. Global's compact map is this view plus filters. |
| Capability-gated optional adapters | [`../strategy_game/capabilities.py`](../../strategy_game/capabilities.py), [`../strategy_game/ports.py`](../../strategy_game/ports.py) | **Yes** | NetworkX/Mesa/Ollama stay optional; the core runs on the standard library. |
| Seeded, per-leader, one-mission turn resolver | [`../strategy_game/local_slice.py`](../../strategy_game/local_slice.py) | **Pattern yes, rules no** | The *shape* (validate all orders → seeded resolution → log) transfers; the city mission list and district schema do not. |
| Four-portfolio, one-leader-per-move council | [`strategy_game/docs/LEADER_COUNCIL_SYSTEM.md`](../../strategy_game/docs/LEADER_COUNCIL_SYSTEM.md) | **Yes (stage-A proposal)** | Global needs the same rule: *every active move is carried by one named leader.*

**What does not transfer:** the city's 5–8 district schema, location pressure, adjacency travel, and the six-verb city mission menu. A global board keeps the *interfaces* and replaces the *content*.

### M0.3 Unique trade-offs

| Dimension | #322 local city | Global ultra-abstract Earth |
|---|---|---|
| **Abstraction unit** | a district (place) | a node (an organisation, person, jurisdiction-context or institution interface) |
| **Board size** | 5–8 places, fixed | a compact graph — a *handful* of clusters, not a map |
| **Scope honesty** | small, finishable | risks infinite content; must be aggressively abstracted |
| **Grounding** | the player can *picture* the city; ordinary life is legible | the player sees *structure*; the world is legible only through framing |
| **Content authoring** | hand-author one city (cheap, bounded) | author factions/signifiers/events that must read as *global* (expensive, open-ended) |
| **Emergence** | local consequences, tight feedback | transnational consequences, loose feedback, harder to attribute |
| **Failure mode** | feels *too small*; the world is furniture | feels *like a spreadsheet*; the world is noise |
| **Compute** | tiny | small *if* abstraction is respected; large if centralities are computed every turn |
| **Replayability** | depends on faction/leader variety in one city | higher if signifiers/coalitions are genuinely contested |
| **Authoring the "wider world"** | arrives as an event feed (cheap) | *is* the board (the expensive half) |

### M0.4 Narrative benefits of each

- **Local city.** The player can hold the whole board in their head. An AGI disclosure is *a thing that happened to their city* — a plant closes, a school debates it, a colleague quits. Character stakes are immediate and legible. The Black-Panther-family comparative case in [#322](https://github.com/TomiToivio/NooPunk/issues/322) — community organising, mutual aid, state pressure, splits — only reads at this scale.
- **Global.** The player can play *the thing NoöPunk is actually about*: the fight over what AGI/NHI/PSI **mean** at planetary scale, and the fact that different function systems observe the *same* shock differently. The issue's own pitch — "a faction may gain legitimacy while losing an intelligence asset" — is a global-board sentence. Disclosure cascades, coalition hegemonies and "who defines the crisis" are native to this board.

### M0.5 Minimum set of simulation entities each needs

**Local city (from #322 M0), minimum:** 1 configurable city; 5–8 `Location`s each with a small political state or a scenario-config; 3 factions × 4 named `Leader`s; ~a dozen `NetworkEdge`s (communication + political layers); an external **event feed**; the four political collections; one seeded resolver. **No** jurisdiction layer, **no** function-system layer beyond event *effects*.

**Global, minimum:** a small set of **jurisdiction/context nodes** (not 175 — a *handful*, treated as tags/institutional contexts); **3–7 transnational factions**; a **leader + small agent roster** per faction (same four-slot council as [#323](https://github.com/TomiToivio/NooPunk/issues/323)); a compact set of **organizations** and **institution interfaces**; a **small subset of function systems** (e.g. science, economy, law, mass media, politics) as *rules/contexts*, not as ownable cards; a set of **signifiers/demands/formations/frontiers**; a multiplex `NetworkEdge` field; and a versioned **event** stream. The difference from local is only that the *node set* is now the world — but it must be a **handful**, per M1 and the bookkeeping audit.

### M0.6 Explicit non-goals

**Non-goals of #322 (already stated there):** tactical combat; individual citizens; parcel-level geography; detailed economics; planetary/global map; world simulation; full national elections; simulated international politics; the LaclauGPT research pipeline as a runtime dependency.

**Non-goals of Global (proposed here):**

- **No detailed planet.** No 175-country sim, no province grid, no granular economy, no population micro-model. Global scope is achieved by **higher abstraction**, never by generating a detailed Earth.
- **No function system as a controllable "Science"/"Politics" resource.** A faction may capture a ministry or influence a broadcaster; it does not own a social system (see M1).
- **No separate tactical combat game**, no space layer at MVP, no mandatory LLM, no account/server.
- **No "increase influence" as the core verb** (see §7).
- **No canon.** No named new factions, characters or institutions.

### M0.7 Keeping both alive

The two options are **not** mutually exclusive at the level of the shared core: both consume `core.py`/`politics.py`; both need the same four-leader council; both need a seeded resolver and a provenance discipline. What differs is **which board is built first**. The recommendation is therefore not "pick one" but "**decide on evidence (M5)** which first slice is the smaller honest game," because choosing Global first and discovering it is unbookkept is the specific risk [#338](https://github.com/TomiToivio/NooPunk/issues/338) itself names.

---

## M1 — Theory-to-data design (proposal, noncanonical)

**Everything in this section is a PROPOSAL and noncanonical.** It defines typed entities *as data*, with clean distinctions, observables and the *causality each is allowed to carry* — deliberately not more. It follows the repository's existing choice that the political field is **one labelled multiplex graph** ([`../strategy_game/politics.py`](../../strategy_game/politics.py)). No numbers, thresholds or transitions are fixed.

### M1.0 How the three theories map — and what they do **not** license

| Theory | Supplies to the model | What it must **not** be turned into |
|---|---|---|
| **Castells** | **Network structure and power**: reach, brokers/switchers, centrality, counterpower — as *observable graph shape*. | Not a scalar "network power" score; not "more edges = more power" without conditions. |
| **Luhmann** | **Differentiated function-system observation**: each system reads the *same* event by its own logic; systems couple but stay autonomous. | **A function system is NOT an ownable institution.** A faction may *capture* a ministry or *influence* a broadcaster; it does not "own politics" or "conquer science." Function systems are **rules/contexts and event-response layers**, not collectible cards. |
| **Laclau** | **Contestation of meaning**: demands, articulation, equivalential chains, antagonistic frontiers, nodal/floating/empty signifiers, hegemonic formations. | **Discourse influence is NOT ownership, popularity or institutional control.** Gaining a signifier is not "winning"; hegemony is a *structure of meaning*, not a score. |

The **bridge** the issue asks for: an event alters communication and interpretation across function systems; actors transmit and frame it through networks; factions contest articulation and legitimacy; the resulting support, coalitions and institutional decisions feed back into the world. The graph is the single substrate; the theories are the *lenses* on it. **No claim that theory predicts an outcome is permitted** ([#306](https://github.com/TomiToivio/NooPunk/issues/306), [`VISION.md`](VISION.md) §4).

### M1.1 The eight proposed typed entities

Each row gives: **distinction** from its nearest neighbours, **observables** (what a view may show), and **causality it is allowed to carry** (what it may *cause*, once rules exist). All are noncanonical.

---

**1. `faction`** — a transnational **political project** with a leader, agents, resources and an ideological articulation.

- *Distinction.* From `organization` (§3): a faction is a *political project* that can capture, ally with or oppose organizations; an organization is an *operating body* (party, cell, company, institute, NGO, broadcaster) with assets and a home context. A faction may own or ally with several organizations; an organization may be non-political. From `leader/agent`: the faction persists when individuals change.
- *Observables.* name; compass position (economic/social); **orthogonal paradigm stance** to AGI/PSI/NHI/Confederacy plus sovereignty/agency/consent — explicitly **not** deducible from compass; declared demands/signifiers; membership/resources pool; the set of organizations it aligns with. (The roster's own design already separates compass from paradigm stance — [`GLOBAL_FACTIONS.md`](../../strategy_game/docs/GLOBAL_FACTIONS.md) §3.)
- *Causality allowed.* May recruit, campaign, lobby, legislate, negotiate, infiltrate, research, contest meaning, and (later) coerce — each *through named leaders*. May **capture** an institution interface but may not convert a function system into property.

---

**2. `leader` / `agent`** — a **named person** who carries authority, and subordinate named operatives.

- *Distinction.* From `faction`: a person is mortal and can defect, be injured, be compromised or die; the faction's interests outlive them. From `organization`: a person *holds office within* a body; the body is not the person. `leader` is the person with special authority; `agent` uses the *same* character foundation with a mission slot ([#338](https://github.com/TomiToivio/NooPunk/issues/338); [`LEADER_COUNCIL_SYSTEM.md`](../../strategy_game/docs/LEADER_COUNCIL_SYSTEM.md)).
- *Observables.* attributes/traits as **uninterpreted data** (already `Leader.attributes`/`personality_tags`); portfolio; status (`ready`/`busy`/`injured`/`unavailable`/`compromised`/`exhausted`/`absent` — the council proposal's shape); location node; sparse pairwise `opinion`/`trust` relationships; faction-facing `loyalty` kept **separate** from person-facing affection.
- *Causality allowed.* **Every active move is carried by one named person** (the council's central rule). People generate mission outcomes, relationship events and RPG encounters; they do not by themselves change the meaning of a signifier.

---

**3. `organization`** — an **operating body** with assets, a home context and a place in the network.

- *Distinction.* From `faction`: an organization is a *body*, not a *project* — it may be independent, a target, an ally or a shell. From `jurisdiction`: an organization *operates within and across* jurisdictions; a jurisdiction is an *institutional/legal context*. From `asset`: an organization owns or controls assets; an asset is a possession/unit.
- *Observables.* kind (party / movement / company / NGO / intelligence cell / broadcaster / research institute / NHI-aligned network — the issue's own list); home jurisdiction(s); the faction(s) it aligns with; its `asset`s; its ties (multiplex edges).
- *Causality allowed.* May hold assets, host leaders, be recruited/captured/allied with, and carry communication. It does **not** own a function system; a broadcaster influenced by a faction is still a mass-media system's operation, observed by mass media's logic.

---

**4. `jurisdiction`** — an **institutional/legal context and tag**, not the main board.

- *Distinction.* From `location` (the base point): a jurisdiction is a *legal/institutional envelope* over one or more nodes; it is the thing that has "an election," "a regulation" and "a threshold." From `organization`: a jurisdiction is a *context*, not an actor; states act through their governments, which are office-holders and organizations. From `function-system response`: a jurisdiction is a *unit of law/politics*, not an observation.
- *Observables.* a name/tag; the institutions it hosts (as **interfaces**, §6); its electoral rule as a **tag** (e.g. "PR," "first-past-the-post") — an abstraction, never a full constituency database; the offices it contains.
- *Causality allowed.* May enact **policy** (which then triggers differential system responses) and hold **elections** (infrequent, consequential). Jurisdictions are **contexts for** the graph, per the issue: "Geographic states/regions are tags, jurisdictions and institutional contexts, not the main board."

---

**5. `multiplex network edge`** — a **typed relation** between nodes.

- *Distinction.* This is the *only* relation type; there is deliberately **no second edge collection** ([`politics.py`](../../strategy_game/politics.py)). Its `layer` distinguishes: communication (Castells), articulation (demand→signifier), equivalence (demand↔demand by shared opposition), antagonism (across a frontier) — and, proposed by extension, trust/alliance, finance/ownership, intelligence access and coercion. Direction is a property, not a new type.
- *Observables.* source, target, `layer`, direction; **derived** graph quantities (reach, brokerage, centrality, counterpower) — computed, never stored as a scalar political score.
- *Causality allowed.* Ties **transmit** influence, framing, resources and intelligence **along** them (with conditions); the *shape* (broker who links otherwise-separate clusters; isolated counterpower) matters. A tie is **not** itself a vote, a seat, a belief or a resource — it is a channel.

---

**6. `function-system response`** — a **rule/context layer** that observes an event by its own logic.

- *Distinction.* From `event`: the response is the *interpretation-and-effect* an autonomous system produces, not the incident. From `organization`/`institution`: **a function system is not an ownable institution** — it has no owner and no card; it is a *context* that reads events. From `discourse articulation`: the response is a system's *operational* reading (verification, liability, commercial potential, newsworthiness), not a contested public meaning.
- *Observables.* which system responded (a small subset: e.g. science, economy, law, mass media, politics, optionally religion/education/health/art); the *kind* of response, expressed as a **qualitative, system-specific effect** on the event's observables (not a universal "+5 stability").
- *Causality allowed.* Each system may **couple** to others via structural couplings the author defines, but **no two systems may be collapsed into one effect**. The same policy or discovery produces **different** responses in different systems — the issue forbids "no universal +5 stability effect."

---

**7. `discourse articulation`** — the **linking of a demand to a signifier**, and the wider chain/frontier/formation structure.

- *Distinction.* From `opinion/support`: articulation is *meaning*, not counted support. From `legislative representation`/`office`/`institutional access`: articulation is *not* institutional control and *not* popularity. From `function-system response`: articulation is a *contested public meaning*, not an operational reading.
- *Observables.* demands (claim + claimant); signifiers with a declared **kind** (`nodal`/`floating`/`empty`/`unspecified`, unknown by default); the articulation/equivalence/antagonism edges; formations; frontiers. All already in `politics.py`.
- *Causality allowed.* A signifier may *unify* a chain of demands (nodal), be *fought over* (floating), or *stand for the chain while emptying its content* (empty). **Discourse influence is not ownership, not popularity, and not institutional control.** A faction can hold the nodal signifier and still lose the election; it can win the election and still lose the frontier.

---

**8. `event`** — a **recorded incident** with an origin, kept separate from interpretation.

- *Distinction.* From `function-system response`: the event is the *incident*; the responses are readings of it. From `discourse articulation`: the event is *what happened*, not *what it means*. From `provenance`: the origin label travels with the event so source-supported material is never conflated with authored/generated/simulated discourse (already enforced — `Event.provenance` defaults to `UNKNOWN`).
- *Observables.* identifier, description, `provenance` (evidence / authored / simulated / unknown), participants, and (proposed, unapproved) trigger/effects.
- *Causality allowed.* An event may **propagate** into several systems, ties and articulations; it must **not** carry a single global effect. A simulated event must never be silently promoted to evidence.

### M1.2 One structure, many lenses

The eight entities are **not eight subsystems**. They are node kinds and edge layers on one multiplex graph plus two non-graph contexts (jurisdictions; function systems). This is the same discipline [`politics.py`](../../strategy_game/politics.py) already encodes: *"the political field is one labelled multiplex graph."* Global adds **people-as-nodes with mission slots** and **functional response layers**, without adding a second graph or a per-concept subsystem.

---

## M2 — Tabletop/paper turn example: one AGI-disclosure incident

**Illustrative only.** The incident is the issue's own: *a corporate AGI disclosure occurs across several jurisdictions*. Actor labels are placeholders: the **player faction** is "Faction Alpha"; rival factions are "Beta" and "Gamma". No named person or institution is created.

**Setup (start of turn).** Three factions each have four leaders (one is the player's). A small node set: a few jurisdictions-as-context, several organizations (a company, a broadcaster, a regulator-ish ministry interface, a research institute, a religious/PSI network), and one contested signifier: **"{the disclosure}"**, currently `floating`.

### The turn, step by step

1. **Event.** The disclosure event is drawn `provenance = SIMULATED`. It is *one* event, not a deck of surprises.
2. **System observations (Luhmann).** The same event is read differently and **independently**:
   - **science** — "is this verifiable?" (an evidence-status question);
   - **economy** — commercial potential and liability exposure;
   - **law** — rights, liability, regulatory competence;
   - **mass media** — newsworthiness and controversy amplification;
   - **politics** — regulation, oversight, electoral salience.
   No universal effect. Science's reading does **not** set law's.
3. **Network transmission (Castells).** The broadcaster organization and the company's ties carry the event outward. A **broker** organization (a body with ties to two otherwise-separate clusters) determines whether the framing reaches the PSI network at all. Reach is *graph shape*, not a scalar.
4. **Articulation (Laclau).** Alpha, Beta and Gamma attach rival demands to the floating signifier — e.g. *liberation*, *exploitation*, *existential danger*, *NHI infiltration*. Each articulation is an edge to the signifier; equivalences form between compatible demands; an **antagonistic frontier** may be drawn. Beta reaches the signifier first and makes it **nodal** *for its chain* — but **nodal for Beta's chain ≠ Beta owns "the meaning" and ≠ Beta is popular**.
5. **Agent missions.** Each faction assigns up to four leaders (one mission each): e.g. Alpha *investigates* (is it real?), *negotiates* with a jurisdiction interface, *organises* the PSI network, *communicates* a counter-frame. Missions resolve on a **seeded** check (leader attributes + relationship + tie conditions + jurisdiction context). Movement is minimal (own node or an adjacent one).
6. **Aftermath / feedback.** Say Alpha's *investigation* succeeds (it gains an evidence token: the event's status moves toward `EVIDENCE`) but its *communication* fails. Beta made the signifier nodal and gains **discourse influence** — **not** an election win, **not** institutional control, **not** popularity. Gamma's coercion-tagged move triggers exposure risk. Alpha's leader may end the turn `compromised`. The log must state, per change: *who did it, where, on what seed, why.*

### Where the meaningful decisions actually are

- **Framing:** which demand to articulate to the signifier — and whether to contest Beta's nodal claim or build an equivalence chain with it.
- **Brokerage:** whether to spend an agent to reach the PSI network through the broker, or to *become* the bridge (risky — being a broker attracts both sides).
- **Evidence vs meaning:** whether to invest in *verification* (a science/law reading) or in *framing* (a mass-media/articulation play) — two different currencies.
- **Institutional:** whether to lobby a jurisdiction interface now, or wait for the (infrequent) election/policy window.
- **Personal:** which leader is exposed to the risky mission, given relationships, loyalty and the risk of `compromised`.

### Where explainability breaks down — honestly

1. **Attribution of discourse change.** When the signifier becomes nodal, *why* — a single decisive articulation? A broker's transmission? Cumulative mass-media repetition? Without an approved rule, the log can show the *edge* but not the *weight*. **This is unresolved.**
2. **Cross-system coupling.** If law's response depends on science's evidence status, a chain of system effects across three turns is hard to narrate. Coupling rules are the least legible part and the most likely to hide.
3. **Centrality ≠ cause.** Castells gives structure; the game can display a broker's centrality, but "centrality changed the outcome" is a *claim*, not a mechanism, unless a rule says so.
4. **Hegemony as a structure, not a score.** A player will *want* a "how hegemonic am I?" number. There is none, and inventing one is exactly what the crossover invariants forbid. The honest answer: read the graph.
5. **Hidden vs open state.** Some readings (a rival's true intent; whether the disclosure is genuine) must be hidden; hidden state is where opacity creeps in. Mitigation: the *event history* always records what was *observable*, and hidden state resolves to an explicit revealed event, never to a silent mutation.

---

## M3 — Deterministic headless prototype (proposal; describe, do not implement)

**DESCRIBE ONLY.** No new rules, no code, until author approval (per [#282](https://github.com/TomiToivio/NooPunk/issues/282) and [`INTEGRATION_BOUNDARIES.md`](../../strategy_game/docs/INTEGRATION_BOUNDARIES.md)).

- **Shape.** A `python -m strategy_game.global_slice --turns N --seed S` headless run, **reusing** `core.py`, `politics.py`, `provenance.py`, `view.py`, `capabilities.py` and the `local_slice.py` *pattern* (validate-all → seeded resolve → append to history). Standard library only; no LLM, database or server.
- **Tiny test graph.** A *handful* of jurisdiction/context nodes, ~5–7 organizations, one contested signifier, a few demands, 2–3 rival factions, one broker position. Small enough to draw on one sheet (see §10).
- **2–3 rival factions**, each with a leader + a *small* agent roster reusing the four-slot council constraint; rivals obey the **same** slot limit and the same seeded resolver.
- **A few function-system responses** (e.g. 3 of {science, economy, law, media, politics}) implemented as **rules/contexts**, each producing a *system-specific* qualitative effect — never one universal effect.
- **A few ideological claims** (demand→signifier articulations) with kind labels; articulation/equivalence/antagonism edges on the existing `NetworkEdge`.
- **Serializable turn logs.** Each turn appends a JSON record: event + provenance, per-leader missions and rolls, per-system responses, articulations changed, edges added/removed, and the six quantities touched (see §7) — **each as a distinct field**. `WorldState.to_json()` already round-trips; extend only as an approved rules layer requires.
- **Determinism.** Reproducible from `(seed, turn)`, exactly as `local_slice.py` does. Replay must not re-call any model.
- **What it would prove (and not).** It would prove the *mechanics are bookkeepable and explainable*; it would **not** prove Global is fun or better than #322 — that is M5.

---

## M4 — UI and narrative prototype (proposal; describe, do not implement)

- **Compact global network visualisation.** Not a map of borders: clusters of organizations/people, jurisdiction nodes as context, edges coloured by `layer` (communication / articulation / equivalence / antagonism / …), the frontier drawn as a boundary. Reuses `board_view`'s `network_nodes`/`network_edges`.
- **Layers and filters.** Toggle layers (communication vs political relations vs ownership); highlight brokers/switchers; highlight the nodal signifier; filter by faction alignment. Filters are *views*, never state changes ([`INTEGRATION_BOUNDARIES.md`](../../strategy_game/docs/INTEGRATION_BOUNDARIES.md)).
- **Dossiers.** Character dossiers (attributes/traits/relationships/status), organization cards, signifier panels (with declared kind, unknown-by-default), jurisdiction panels (offices + electoral-rule tag).
- **Decisions.** The same God's-eye screen presents mission assignment, articulation choices, policy/election windows and system responses — **no mode switch** ([`VISION.md`](VISION.md) §2–3).
- **Textual RPG encounters.** A compact dialogue/skill-check panel for personal events (assassination attempt, interrogation, uncanny revelation, an ethical dilemma), resolved with the approved check, embedded in the strategy UI.

### M4.1 The graph-hacking model is explicitly UNDECIDED

Per [#338](https://github.com/TomiToivio/NooPunk/issues/338) ("do not decide the hacking model yet") and [AGENTS.md](../../AGENTS.md) §4 (hacking **deferred**), **no hacking model is chosen.** The alternatives, with trade-offs:

| Alternative | What it is | Strengths | Drawbacks |
|---|---|---|---|
| **Graph-node puzzles** | the player resolves a network map (Drop / Midnight Protocol style) to breach a node | evocative; strongly Castellsian; visible network | becomes a disconnected minigame; UI-heavy; hard to keep "in the same state"; risks a skill the rest of the game lacks |
| **Mission/resource abstraction** | hacking is an agent mission kind resolved on the seeded check, costing assets/intel | fits the one-resolver rule; explainable; cheap to author; shares state | loses the "feel" of cyberspace; might read as a generic mission |
| **Network-access mechanics** | access is a *property* of edges/nodes (a control token on a tie/chokepoint); hacking is seizing/maintaining a network path | ties directly to the Castellsian board; affects the same organizations/ties; no separate minigame | needs careful rules to avoid "control = win"; centrality bookkeeping |

The issue's constraint applies to all three: hacking must affect the **same** shared organizations/networks, not become a disconnected minigame. **No decision is made here.**

---

## M5 — Feasibility decision framework (what evidence would settle it)

**This document does not have the evidence.** It has reasoning and a reading of the repository. To decide whether Global beats #322's local-city complexity, the project needs *measurements*, collected the way [`VISION.md`](VISION.md) §15 already proposes (no arbitrary numeric targets set in advance).

| Question | Evidence to collect | If Global fails | If Global wins |
|---|---|---|---|
| **Fun** | per-minute engagement; decision density; "want to keep playing" in playtest | keep #322 as the first slice | Global may be the better first slice |
| **Clarity** | can a stranger *explain why power shifted* from the log, without a map? | Global's abstraction is noise | abstraction is legible |
| **Compute** | turn latency; centralities recomputed per turn; memory | Global needs optimisations #322 does not | Global runs as cheaply |
| **Authoring burden** | hours to author one global event/faction/signifier vs one city district; content lifespan | Global's content is too open-ended for a small team | authoring scales |
| **Replayability** | distinct endings/strategies within approved content; replay variance | #322's tighter board replays better | contested signifiers create variance |
| **Bookkeeping (see §9)** | per-turn state updates, card movements, tracks, rolls, lookups — *counted* | Global is unplayable as a tabletop game | Global is bookkeepable |

**The decisive test design.** Build *both* first slices to a **tabletop-playtestable** state (paper or a thin headless resolver) using the *same* shared core, play each with the author, and compare on the metrics above. The evidence that settles the question is **a played comparison**, not an argument. Until then, **both options stay alive** (M0.7).

---

# Second half — democratic politics, tabletop, cards and bookkeeping

## 6. Comparison matrix of the seven political simulators

Scope of the check: I retrieved each product's **own** pages and, where possible, third-party reviews. The **reliability column states honestly what could be verified** — the issue's own instruction is *"verify mechanics before adopting; avoid assuming inaccessible/unverified details."* Raw evidence is in [`NOOPUNK_GLOBAL_SOURCE_LEDGER.md`](NOOPUNK_GLOBAL_SOURCE_LEDGER.md). No mechanic below is adopted; the matrix only records lessons and boundaries.

Columns, as the issue requires: **politics between elections · representation · internal party governance · policies · stakeholder/system responses · costs/economy · evidence reliability.**

| Simulator | Politics *between* elections | Representation | Internal party governance | Policies | Stakeholder / system responses | Costs / economy | **Evidence reliability** |
|---|---|---|---|---|---|---|---|
| **Fantasy Parliament / PM Career** ([career-lander](https://www.fantasyparliament.co.uk/career-lander)) | **Central.** "Weekly decisions & crises"; survive the long game; internal discipline problems; media traps; policy crises; "news cycle filler weeks." | MP Mode: real seats; whips name your lobby; Aye/No/free vote, one-/three-line; Speaker's eye; a real bill each month. | **Central.** "Party factions can remove you"; leadership contests (letters/hustings/ballots); cabinet & shadow-cabinet performance scores; "lose the party, lose your job." | Flagship policy to reset the agenda; a monthly bill through the House; editable decision responses; an AI "policy tester." | Voter personas + stakeholder approval (papers, unions, business lobbies, party factions); AI-scored speeches/stunts; a front page about what you did. | Party HQ: membership fee & roll, donors book (take or return), marginal research, activist teams; backlash when overreaching. Subscription model on the sibling product. | **PARTIALLY VERIFIED.** Own feature pages retrieved; the product sits behind login/account; deeper numbers unverified. Some **naming ambiguity** with a same-domain MP-drafting product (BBC). |
| **Politics Simulator** ([politics-simulator.com](https://politics-simulator.com/)) | Claimed: a career "from activist to head of state." | Claimed (unspecified). | Claimed (unspecified). | Claimed (unspecified). | Claimed "authentic" reactions; marketing copy only. | "Resources" mentioned, unexplained. | **NOT VERIFIED.** Only the marketing landing page is reachable without an account; **no mechanics are documented** on it. The name also collides with an unrelated itch.io card game. Treat as unverified. |
| **Fantasy President Career** ([fantasypresidentcareer.com](https://fantasypresidentcareer.com/)) | Career Mode (1990–2025) month-by-month, US-scoped; a legislative desk calendar of bills; the presidency takes over the same career. | US offices only: governor, state legislator, Congress, senator, president (jurisdiction-specific). | Limited on the page — not a prominent feature. | "Your own bill to carry"; a player-submitted "Policy Guesser." | A monthly "character sheet" pacing how much you can do; Wikipedia page generation as flavour; events & reactions. | Subscription (£5.99/mo; £59.99/yr); 48-month terms. | **PARTIALLY VERIFIED.** Own site retrieved with moderate detail; some modes explicitly "an untested reskin" of another mode; deeper numbers unverified. |
| **The Political Process** ([Steam 1184770](https://store.steampowered.com/app/1184770/)) | Turn-based; **primary and general elections simulated for every one of 600+ procedural politicians**; you watch colleagues' races. | Run for office from the ground up; write legislation in the body you hold. | Party control of the executive; colleagues run and defect; party organization via policy/budget. | Write legislation; balance budgets; 100+ policy-driven metrics. | 100+ metrics change over time from policies you and colleagues create. | Budget balancing is a core loop. | **WELL VERIFIED (scope).** Steam description + third-party review. Early Access; **no win conditions**; **no tutorial**; diplomacy/international relations are *planned, not present*. |
| **Geo-Political Simulator 2026 Edition** ([Steam 4021780](https://store.steampowered.com/app/4021780/)) | **Central.** Regime censures: motion against head of state, constructive no-confidence, dissolution, confidence vote, Art. 49.3; play as head of state **or opposition**. | Parliaments reproduced; electoral-threshold legislation; G20 "worldwide laws." | Party AI forms/dissolves coalitions, changes leaders, creates new parties; "party strategies with regime censures." | Nationwide laws; budgets; lobbying; media intervention. | 600+ data elements per 175 countries, real-time; popularity; AI/robotics employment impact. | Detailed economic/financial/company accounting. | **MIXED.** Feature/scopes **well documented** (Steam + reviews); but the *reliability of the simulation* is **disputed** — ~48% mixed user reviews, crashes, opaque UI, "mechanics feel random." Feature list verified; model trustworthiness **not** endorsed. |
| **Global Election Simulator** ([globalelectionsimulator.com](https://globalelectionsimulator.com/)) | **Effectively none.** It is an election-night explainer/simulator, per country. | Strong: vote-to-seat conversion following each country's **real** electoral law. | No. | No (you move party/candidate support, not policy). | Live count by batch/seat; interactive maps; begins from the real latest result. | No. | **WELL VERIFIED (scope).** Own site describes mechanics clearly. It is an *educational electoral explainer*, not a career/party simulation. |
| **Poliwave** ([poliwave.com](https://www.poliwave.com/), [/game](https://www.poliwave.com/game)) | Minimal: forecasting + a campaign minigame ("**Landslide**: take a party through a full campaign"). | Strong: seat projections, scenario editing, district drawer, map maker. | No. | No. | Swing model, Monte Carlo seat ranges, poll averages; distinguishes projection/uncertainty. | No (Pro subscription for advanced features). | **WELL VERIFIED (scope).** Own site + game page. It is an *election-forecasting platform* with a campaign game, not a between-elections political sim. |

### 6.1 What Global should take, and what it must avoid (from the matrix)

- **Take:** between-election decision pressure (Fantasy Parliament / GPS 2026); regime-level institutional moves *as rules over the same graph* (GPS 2026 censures, abstracted); legislation as a *policy object that triggers differential system responses* (The Political Process's metric feedback, but **not** 100+ metrics); the clean distinction between **support, votes, seats and uncertainty** (Poliwave / GES); the "real electoral law as a tag" idea (GES) **without** the full constituency database.
- **Avoid:** UK- or US-specific institutions as universal rules (Fantasy Parliament / Fantasy President Career); simulating every district, law and demographic (The Political Process); vast country-by-country indicators and granular economic accounting (GPS 2026); a complete real-world constituency database (GES/Poliwave); treating a forecasting tool or election explainer as a *politics* game.
- **The matrix's design implication, verbatim from the issue:** *"Ordinary politics must be playable and rewarding, not just an 'increase influence' button."* See §7 and §11.

---

## 6A. The two core-insight sources: Sigma Theory and The Shadow Government Simulator

**Added 2026-10-13 — design alternative / proposal, noncanonical, approves no mechanics.** Issue [#338](https://github.com/TomiToivio/NooPunk/issues/338) names these two games as its **core insight** and lists them as primary Strategy inspirations: *"Study the strategic abstraction of **Sigma Theory** and **The Shadow Government Simulator**: a compact graph and small roster of key people can convey planetary-scale competition."* The earlier version of this document omitted both. This subsection closes that gap: it states what each game actually does **from its own sources**, what it does and does not prove about the issue's core claim, the one mechanical lesson Global should take, and what Global must **not** copy. Raw evidence and per-source reliability are in the companion ledger [`NOOPUNK_GLOBAL_SOURCE_LEDGER.md`](NOOPUNK_GLOBAL_SOURCE_LEDGER.md). Nothing here is adopted; no mechanic, number or canon is approved.

**The claim under test.** *"A compact graph and small roster of key people can convey planetary-scale competition."* It has two halves — a **compact graph** and a **small roster of key people** — and it is a claim about the *feasibility of abstraction*, not about any particular model. Each game below is judged against both halves, and against what Global specifically proposes (M1: a multiplex graph of organizations, people, jurisdictions-as-context and function-system couplings, with contested meaning).

### 6A.1 Sigma Theory: Global Cold War — what it does, and what it proves

**What it actually does (verified from its own Steam listing, app 716640).** A turn-based espionage strategy game. A paradigm-shifting discovery — the "Sigma Theory" — *"can only be harnessed by a handful of scientists"*; the player is *"placed at the head of your country's Sigma division"*, racing *"before anyone else"*. Mechanics stated on the page:

- **A small named roster is the engine.** *"Recruit a team of **four special agents from 50 unique unlockable characters**"*, each with *"their own story, motivations and traits"*; archetypes include investigator, soldier, hacker, seducer.
- **A managed relationship roster of non-agent actors.** *"Develop and manage your relations with **over 100 NPCs**: lobbies, armed groups, politicians…"* through *"flattery, threats or blackmail"*; *"they may turn on you."*
- **Missions, not a world model.** Agents are sent *"around the world to gather scientists, discover compromising documents on local politicians, and more"*; you *"seduce, manipulate and bribe"* targets.
- **Counter-espionage, interrogation and prisoner exchange.** Rivals *"will also use their agents to infiltrate your country"*; you *"track, capture and interrogate them … then exchange them for ransom."*
- **A keep-or-share decision on research.** *"Will you keep these discoveries for yourself or share them with the world?"*
- **No simulated planet.** There is no model of national economies, territories or populations; the "world" is the player's nation, the rival nations, mission geography, and the NPC relationship roster.

**Does it prove the core claim?** **Yes for the stronger half — "a small roster of key people" — and partially for "a compact graph".** Sigma Theory is the **strongest existing evidence in this document's source set** for the claim: planet-scale rivalry (every superpower competing for a singularity-class discovery) is carried by four named operatives plus a managed relationship roster of 100+ individuals, with **no country simulated as a territory or an economy**. If the claim's strong form is "people and relationships can carry a planetary premise", Sigma Theory demonstrates it at commercial scale (Mostly Positive, 77% of 893 reviews).

What it **does not** carry, stated precisely:

- Its "graph" is a **roster of individuals with relations**, closer to a hub-and-spoke (your agency ↔ rival agencies ↔ per-node contacts) than to the **multiplex graph of organizations, jurisdictions and function-system couplings** Global proposes (M1). It therefore says nothing about whether *that* graph can carry the load.
- It does **not** avoid countries. The player *is* a nation's Sigma division and rival *nations* act against them; additional playable **nations ship as DLC** ("Additional Nation": Nigeria, Brazil). The accurate statement is that Sigma Theory does not simulate countries *in detail* — not that it has no countries at all. A sibling report that Sigma Theory simulates *no country* is **not confirmed as written** and is corrected here.
- It does not model contested **meaning** (Laclau) or autonomous **function systems** (Luhmann) at all.

**The lesson Global should take.** A handful of named operatives, each a person with traits and motivations, plus a **relationship roster you actively manage**, is enough to make global rivalry legible and playable; missions are the engine, and relationships are a resource that can be lost. This is direct support for the council's "every move is carried by one named person" rule and for treating the relationship roster (M1/M2) as first-class.

**What Global must NOT copy.** The **nation-as-playable-side** identity and real-world nation framing — Global makes jurisdictions **tags/contexts**, not sides (M1.4). The **separate tactical minigames** (field-operation pursuits, exfiltration phases, drone positioning): Global must not fragment into a disconnected minigame (M4.1). **Assassination/kidnapping** as a central verb — Global's core is the contestation of meaning, not covert violence. The **DLC-nation content model**.

### 6A.2 The Shadow Government Simulator — what it does, and what it proves

**What it actually does (verified from its own Steam listing, app 1281190).** A turn-based strategy game in which you *"lead a secret society towards world domination"* by *"investigat[ing] the influential and convert[ing] them … via bribery, seduction and intimidation"*. Mechanics stated on the page:

- **The board** ***is*** **a discovered network of people.** *"When you enter a new nation, you'll be alone with just a headquarters at your disposal and minimal information. Slowly … uncover[] who are the influential and how much power they truly wield … their traits and personalities."*
- **Connections are the mechanism.** *"You'll discover **who they are connected to**, and thus person by person, you shall take over the whole elite."*
- **Connectivity is power *and* exposure.** *"Having a strong interconnected network is the key to success, but **the bigger you get the more visible you are** and this could lead to your demise. Manage your network, **cut and create connections**."*
- **The world outside the graph is abstract.** Regions have *"procedurally generated networks"*; *"the world's countries will unite against you"*; *"nations you take over become yours to command"* — *"Be it a person or a country, they shall all become like pawns."*
- **A secret-society frame.** You unlock factions *"such as the Masons and the Templars"*, with bribery/seduction/intimidation as the conversion loop.

**Does it prove the core claim?** **Yes for the "compact graph" half — the strongest available evidence for it.** The Shadow Government Simulator's actual game board *is* a graph of influential people and their connections, uncovered under fog of war, and that graph is asserted to be sufficient to drive a global-domination premise. It also demonstrates **graph-shape-as-mechanic** directly: connectivity is simultaneously success and visibility, and the player is told to *cut and create connections* — exactly the reach/brokerage/exposure tension Global's Castells layer wants (M1.5, §7).

What it **does not** carry:

- The graph is a graph of **people (elites) only** — not the multiplex of **organizations, jurisdictions-as-context and function systems** Global proposes; there is no Luhmannian function-system layer and no contest of meaning.
- The world outside the graph is a **conquest target** ("nations … become pawns"), a domination fantasy, not a struggle over what a shock *means* (Laclau) — a different genre from NoöPunk.
- Its **procedural network generation** trades authored political meaning for variety; Global cannot use generated networks as a substitute for content that must *read as global* (M0.3, §9).
- It shows one shadow organization versus rival organizations and "the world's nations", not many co-equal transnational **political projects** contesting articulation.

**The lesson Global should take.** **Fog-of-war network discovery** — the player does not read the graph, they *uncover* it — is a concrete mechanic that lets a small graph carry a global premise, and it fits Global's provenance / `UNKNOWN`-by-default discipline (M1.8) exactly. The companion lesson is the **connectivity ⇄ visibility trade-off**: growing the network raises both power and exposure, which is the honest shape of the broker risk in M2.

**What Global must NOT copy.** The **secret-society / Illuminati** framing (Masons, Templars) and **bribery–seduction–intimidation as the conversion loop** — Global's core is contestation of meaning, not conversion by coercion. **Procedurally generated networks** as a stand-in for authored meaning. The **"nations become pawns"** conquest model. A **people-only graph**: Global is multiplex (M1.2).

### 6A.3 Verdict on the core claim (evidence, not approval)

- The two games are the **strongest evidence in this document's source set** that a global-scale game need not simulate a planet: **Sigma Theory carries the "small roster of key people" half** (four named operatives plus a managed 100+ relationship roster, no territory/economy model), and **The Shadow Government Simulator carries the "compact graph" half** (a fog-of-war network of influential people whose connections drive world domination, with a real connectivity/exposure tension).
- **Neither** demonstrates the *specific* thing Global proposes. Neither models **Luhmannian function systems**; neither has a **contested-meaning** layer; both reduce the world outside their graph to **discrete nations / targets / pawns**. The pair therefore proves the claim's **general form** (abstraction can carry scale) and does **not** validate Global's particular multiplex model (M1).
- The honest conclusion, in the document's existing framing: these two sources are strong evidence that the **risk named in M0.3 and M5 is survivable** — a global board can stay compact — and they are **not** evidence that any specific mechanic here is correct. No mechanic is adopted.

---

## 6B. Carry-over notes and one open finding (no design decisions)

**Added 2026-10-13. Noncanonical. Approves no mechanics and no canon; resolves nothing.** These are carry-over *questions* the issue implies but this document does not decide.

### 6B.1 The Luhmannian layer is already canon (§36) — a carry-over question, not a new build

`RULEBOOK.md` **§36 ("The four NoöPunk systems") is already canon**: §36.1 gives Luhmann's baseline, §36.2 **"The four layers"** names them **Physical / Psychic / Social / Cybernetic**, and **§36.7 is literally "Structural coupling between the layers"** — with the coupling-interface table (Physical ↔ Psychic, Psychic ↔ Social, Social ↔ Cybernetic, Cybernetic ↔ Physical, Psychic ↔ Cybernetic, Psychic ↔ Psychic, and all four) and the rule *"Coupling is not collapse."* Under [AGENTS.md](../../AGENTS.md) §0, **legacy rules do not carry over** to the crossover without an explicit, approved conversion decision, while **lore and known canon do**. The Luhmannian layer is therefore a **carry-over question for the crossover, not a new build**: the crossover does not have to invent it — it has to *decide, explicitly, whether and how to import it*.

**A naming divergence to flag, not to silently resolve.** Issue [#338](https://github.com/TomiToivio/NooPunk/issues/338) writes the cross-cutting layers as **"Physical/Cyber/Astral"** (e.g. *"Physical/Cyber/Astral activities modify shared state"*; *"policy debates on astral jurisdiction"*; *"Physical/Cyber/Astral dimensions as cross-cutting NoöPunk setting layers"*), whereas canon §36.2 names them **Physical / Psychic / Social / Cybernetic**. The issue's **"Astral"** is not a canon layer name, and **"Cyber"** is not canon's **"Cybernetic"**; canon's word for the consciousness domain is **"Psychic"**. The issue itself calls these *"cross-cutting setting layers rather than identical taxonomies"*, so the divergence may be deliberate vocabulary — but it is a **divergence**, and this document **flags it rather than picking one**. Whoever scopes the crossover must settle "Astral" vs "Psychic" explicitly.

### 6B.2 The paper-playable tabletop version is an existing gate deliverable (VISION.md S0-A)

[`VISION.md`](VISION.md) **§S0-A already requires** that, *"before any playable mechanics"*, the leader, faction and discourse rules get a **"paper-playable version … reviewed separately, with cross-layer event propagation as its own fourth gate."** The tabletop work in §§9–11 of this document therefore sits **under an existing gate deliverable**, not a new direction: a paper-playable variant is something the vision already demands, so Global's tabletop option is a candidate *answer* to that requirement, not a new requirement. Nothing here changes the gate; the gate already exists.

### 6B.3 OPEN FINDING — three unreconciled global rosters (data-integrity question, not a design decision)

**This is recorded as an unresolved data-integrity question. This document does not choose the correct number and does not resolve it.** The repository currently holds **three different global-actor rosters**, and Global will depend on that roster:

| Where | Count | What it actually is (verified this session) |
|---|---|---|
| [`data/world/un_parties.yaml`](../../data/world/un_parties.yaml) | **4** | Four UN parliamentary parties on an economic/social axis (Bioconservatives; Libertarian Party; United Earth Social Democratic Party; The Multitude). The file itself declares `open_for_future_parties: true` and `extra_parliamentary_factions: true`, i.e. explicitly **non-exhaustive**. |
| The crossover's global-factions record: [`strategy_game/data/global_factions.json`](../../strategy_game/data/global_factions.json) | **7** | `status: "author_canon"`, `source_issues: [328, 329]`; contains exactly **seven** factions (Accelerationists; Cyborgists; Critical; Doomers / Butlerian Jihad; Confederacy Awakening; Orion / Grey networks; Normalcy Bloc), and its own note says *"The seven global paradigm factions as authored in issues #328 and #329."* |
| Issue [#328](https://github.com/TomiToivio/NooPunk/issues/328) (OPEN, author-updated **2026-10-12T15:55:15Z**) | **11** | The issue is titled *"Eleven global Parties …"* and its body carries an **11-row** official roster table of global Parties under a UN world government (three of them NHI-led). |

**What I could verify.** The **4** (read `un_parties.yaml`) and the **7** (read `global_factions.json` and counted its `factions` array) are confirmed. Issue #328's **11** is confirmed from the issue's own title and roster table. All three counts are real and live on `main`.

**What I could NOT confirm.** Whether these three lists are meant to describe the **same** set of actors at all. They are **different taxonomies**: `un_parties.yaml` is a UN-parliamentary axis list; #328 is "eleven global Parties under a UN world government" (including NHI-led Parties); `global_factions.json` reconciles #328/#329 into "seven global *paradigm* factions". The discrepancy may be a **count** mismatch, a **taxonomy** mismatch, or both — I did not determine which, and I swept only these three records, so there may be further rosters elsewhere.

**Why record it here.** Global's actor model (M0.5, M1.1) binds to a roster. Binding a design to "a handful of factions" before the **4 / 7 / 11** question is settled risks encoding an arbitrary number. **The count should be settled before any design binds to a number** — but that settlement is the author's, and it is a data-integrity question about which records are canonical, **not a design decision** this document is entitled to make.

---

## 7. The six quantities that must stay distinct

The issue's acceptance criterion. These are **six different things**, kept in **six different fields**, with **six different component conventions** (§8). **None is interchangeable.**

| # | Quantity | What it is | What it is **not** | Component convention (§8) | Home in the model |
|---|---|---|---|---|---|
| 1 | **Opinion / support** | how a *constituency/population* currently feels | not membership; not seats; not hegemony | per-jurisdiction **support markers** (localized) | `Location`/jurisdiction field; `local_slice.support[loc][faction]` pattern |
| 2 | **Organizational membership / resources** | members, volunteers, funds, equipment, capacity | does **not** buy extra actions — it *amplifies* a leader-led mission | faction **pool/tableau** | `Faction` fields (proposed) |
| 3 | **Legislative representation** | seats held in a body | not opinion; not office | **seat markers** per chamber/jurisdiction | jurisdiction/chamber structure (proposed) |
| 4 | **Office & government control** | who holds which executive/office | not seats; not access | **office markers** on board slots | office/jurisdiction structure (proposed) |
| 5 | **Institutional access** | a faction's ability to *reach and be heard by* a function-system **interface** (a ministry, regulator or broadcaster) | not ownership of the system; not seats; not hegemony | **access tokens** attached to institution-interface cards | institution interfaces (proposed) |
| 6 | **Laclauian discursive hegemony** | which articulation is **nodal** / where the frontier runs | **not** a scalar; not ownership; not popularity; not control | the **articulation graph** itself | `politics.py` (`Signifier.kind`, `RelationLayer`) |

**Explicit non-identities** (the failure the issue warns against):

- A faction can hold **#1 support** and still lose **#3 seats** (turnout, electoral rule).
- A faction can win **#3 seats** and not hold **#4 office** (coalition arithmetic).
- A faction can have huge **#2 membership** and no **#5 access**.
- A faction can hold the **#6 nodal signifier** and lose everything else — **hegemony in meaning is not power**.
- **#5 access ≠ #6 hegemony.** Reaching a broadcaster is not owning the media system and not defining common sense.

**Why no "increase influence" button.** The core loop must let the player *choose which of the six to pursue*, and each must move for a *visible, different reason*: organising moves #1/#2; a legislative vote moves #3; a coalition moves #4; a negotiation/lobby move opens #5; a framing/articulation play moves #6. A single "influence" scalar would collapse exactly the distinctions the theory and the acceptance criteria require.

---

## 8. Card taxonomy and component inventory

**Core modelling rule (from the issue):** a card is an **ergonomic representation and interaction object**, **not** necessarily a single flat entity type, and **not** necessarily a literal card in memory. **Typed domain models stay separate from the card UI.** Different underlying models keep a person, an organization, a function system, a communication relation, a semantic articulation, a temporary effect and an action distinct. **Function systems are better modelled as rules/contexts than as ownable "Politics"/"Science" cards.**

### 8.1 Persistent vs temporary

| Class | Examples | Lifetime | Owned by |
|---|---|---|---|
| **Persistent — named people** | faction leader; agents | whole campaign (until death/defection) | the faction |
| **Persistent — bodies** | organization/party/company/institute tableau cards | campaign | the body (may be aligned to a faction) |
| **Persistent — context** | jurisdiction/context cards; institution-**interface** cards | campaign | the world (never "owned") |
| **Persistent — meaning** | idea/signifier cards; demand cards | campaign | **contested** — a card's *alignment* is an edge, not ownership |
| **Persistent — possession** | assets/units (as **tokens** attached to their owner card, not separate decks) | until lost | the owning card |
| **Temporary — events** | crisis/event cards (from a versioned deck) | one turn | the world |
| **Temporary — actions** | mission/action cards (hand) | a turn or a round | the faction |
| **Temporary — effects** | status tokens (e.g. `compromised`), modifiers | auto-expiring | attached to a card |

### 8.2 How network edges are represented

Edges are **not** entities with their own deck. Three representation options (choose per surface, not globally):

1. **Drawn links** on a board/map between placed cards (default for the global network view).
2. **Relation cards** laid between two cards when the tie needs a token (a control/access token for §4 access mechanics).
3. **Tags/overlays** on a node card for minor or transient ties.

All three map to **one** underlying `NetworkEdge` with a `layer`. **Never** a second edge collection.

### 8.3 Event/action lifecycle

`deck (versioned) → drawn event → system observation (rules, not a card) → declared actions → seeded resolution → tokens attached / edges changed / six quantities updated → temporary effects expire at end of turn → effects recorded in the log.`

### 8.4 Deliberately **NOT** cards

- **Function systems** — rules/contexts and response layers; a faction may capture a ministry *interface*, never "Politics."
- **Derived graph quantities** — reach, brokerage, centrality: computed and shown, not held.
- **Hidden/deep model variables** — stay in digital mode; only their *revealed* consequences become cards/events.
- **The six quantities as such** — they are tracks/markers/relations, not cards.

### 8.5 Ownership and shuffling

- **Named leaders and enduring organizations stay on the table/tableau — they are never shuffled each turn** (the issue's own test).
- **Deck-building represents organizational capabilities and accumulated knowledge** (skills, research, doctrine, contacts), **not** a random pool of political actors.
- **Units/assets are tokens attached to their owning card.**
- **Ideology/signifier cards are contested, not owned.** Ownership of a *frame* is meaningless; alignment is an edge.
- **Jurisdiction/institution interfaces are owned by the world** and targeted, not collected.

---

## 9. Manual bookkeeping audit

**Bookkeeping risk is a PRIMARY constraint** — the issue says so explicitly. This section **counts** the required operations per turn for a *small* Global turn, for the physical and the digital variants, and proposes a **measurable budget**. The numbers are **illustrative estimates to be measured in playtest**, not approved rules.

### 9.1 The counted turn (a deliberately minimal Global turn)

| Stage | Physical operations | Digital operations |
|---|---|---|
| Draw/resolve 1 event card | 1 draw + 1 read + (provenance check) | 1 automated |
| System observations (3 systems) | 3 lookups + 3 apply + 3 mark | automated, 3 lines in log |
| Portfolio passives (4 per faction) | 4 read + 4 apply | automated |
| Agent assignment (4 leaders × 1 mission) | place 4 mission cards + move ≤4 tokens | 4 clicks |
| Resolution checks | 4 rolls + 4 modifier lookups + 4 threshold compares + 4 applies | 4 automated |
| Relationship/character event (≤1) | 1 draw + 1 choice + 1 apply | automated prompt |
| Articulation changes (2 edges) | move/place ≤2 relation cards | 2 clicks |
| Six-quantity update | ~6–10 marker moves across tracks/pools/seat/office/access/relation | automated |
| Temporary-effect expiry & cleanup | ~3 removals + return tokens | automated |
| Log write | 1 short hand entry (or none) | 1 automated |

### 9.2 Counts per turn

| Metric | Physical (minimal subset) | Digital-first |
|---|---|---|
| **State updates (discrete)** | ~**35–55** | ~**0 manual** (logged) |
| **Card movements** | ~**10–14** | ~**6 clicks** |
| **Tracks touched** | **6** (one per quantity) + status tokens | same, on screen |
| **Dice rolls** | ~**4–6** | ~**4–6** (seeded, shown) |
| **Lookup steps** | ~**12–20** (system responses, modifiers, thresholds) | ~**0–3** |
| **Hand/tableau size** | leaders 4 + agents ≤4 + org cards 4–7 + signifier/demand ≤6 | same, filtered |

### 9.3 Proposed budget (measurable, to set **before** implementing)

- **Table time per turn:** target **≤ 8 minutes** for the physical subset; **≤ 3 minutes** digital.
- **Discrete bookkeeping actions per turn:** hard cap **~40** physical (the "minimal subset" above lands just under it).
- **Tracks:** exactly **six** quantity conventions + at most a few status tokens — no seventh meter.
- **Automated expiry:** every temporary effect has a printed end-of-turn condition; the digital variant enforces it.
- **The failure signal:** if a turn needs a **spreadsheet** or a second page of tracks, the design has exceeded the budget and must cut a system, not add a UI.

**Consequence stated plainly:** the *full* theory (all function systems × all factions × all jurisdictions, updated independently) is **not** bookkeepable physically. Global is only viable as a tabletop game **if** the active node/agent/event set stays tiny and derived quantities stay digital-only (design alternative 2, §11).

---

## 10. Mock-up of one tabletop-compatible Global turn

**Illustrative, not approved rules.** Same incident as M2. Placeholder labels only: **Faction Alpha** (player), **Beta**, **Gamma**. The board is a few clusters on one sheet.

**Board snapshot (start of turn):** jurisdiction/context node *J1, J2, J3*; organizations *company, broadcaster, institute, PSI-network, ministry-interface*; signifier **S ("{disclosure}")** currently `floating`; edges: communication ties across the clusters, a broker org bridging two clusters.

| Step | Tabletop action | Underlying model | Six quantities touched |
|---|---|---|---|
| 1. **Event** | draw *disclosure* from the event deck (`provenance=SIMULATED`) | `Event` | — |
| 2. **System responses** | read the three response cards (science/economy/media); apply each *system-specific* effect | function-system **contexts** (rules) | — (feeds 1 & 6 later) |
| 3. **Network influence** | send Alpha's *organise* agent along a communication edge through the broker to the PSI network | `NetworkEdge(communication)` | #2 (capacity), enables #1 |
| 4. **Portfolios & checks** | resolve Alpha's 4 missions on 1d6+skill+bonus−context | seeded resolver | #1, #2, #5 |
| 5. **Ideological framing** | attach Alpha's demand *"verification and rights"* to **S**; place the articulation edge; Beta contests by attaching *"liberation"* | articulation edge; `Signifier.kind` | #6 (structure, **not** a score) |
| 6. **Election/policy window** | if due: a jurisdiction **policy** vote (Alpha lobbies the ministry interface) → enacts a tag; **no** universal stability effect | jurisdiction + policy object | #3 or #4 or #5 (whichever the rule says) |
| 7. **System response cascade** | law reads the enacted policy differently from economy | coupled contexts | — |
| 8. **Character RPG event (≤1)** | Alpha's *investigate* leader is offered a choice: publish the evidence (risk exposure) or hold it (gain `trust` with a contact); resolve the skill check | `Leader` + `Relationship` | #5, status token |
| 9. **Update & cleanup** | move markers on the six tracks; expire temporary effects; return tokens | six distinct fields | all six, separately |
| 10. **Log** | one line: who did what, where, seed, consequence | `Event`/history | — |

**What this mock-up demonstrates:** every step touches a **different** quantity; there is **no** generic "increase influence" step; and the *system responses* (steps 2 and 7) are **rules**, not cards anyone can own.

---

## 11. The three tabletop approaches — comparison and **ONE** recommendation

| | **1. Strict tabletop-complete core** | **2. Tabletop-like digital first** | **3. Hybrid companion** |
|---|---|---|---|
| **What it is** | every essential state variable is a card/token/short track; a full turn runs on paper + dice, no algorithm | a board/card interface; the computer transparently holds centralities, coupled system effects, hidden info, rival AI and event scheduling | physical board/cards + an optional lightweight app for bookkeeping, event generation and network visualisation |
| **Bookkeeping** | highest manual load; only viable for a *tiny* active set (§9) | load is automated; board stays legible | load is split; the app removes the worst parts |
| **Pros** | forces rules to be *explicable*; true tabletop; great design discipline | achievable by a small Python team; matches the released artefact; scales depth under the hood; deterministic and testable | keeps the tabletop feel; salvages physical play; incremental |
| **Cons** | likely **exceeds the bookkeeping budget** if theory is kept full; content must be brutally cut | not "tabletop-complete"; a physical port will be a *simplified variant*, not numerically identical | needs *both* a print production and an app; "one source of truth" is harder; two maintenance surfaces |
| **Playable without electronics?** | **Yes — by definition** | **No (fully)**; a printed simplified subset only | **Partially** — the documented core is playable by hand; the app is optional |

### Recommendation: **Approach 2 — tabletop-like digital first.**

**Justification.**
1. **It is the artefact the project actually ships.** NoöPunk is an **open-source indie digital game** that must build and run from source, offline, with no account ([`VISION.md`](VISION.md) §7a). Approach 2 is that game; approaches 1 and 3 are *design constraints* it can still honour.
2. **It is the only approach that survives the PRIMARY bookkeeping constraint (§9).** The full Castells/Luhmann/Laclau model — differential system responses, coupled effects and derived centralities — cannot be updated by hand without a spreadsheet, which the issue rules out. The **computer must carry the derived and hidden quantities**; the player keeps the *legible* ones (the six quantity conventions).
3. **It preserves the design discipline of Approach 1** by requiring that the *player-facing* state stay within the §9 budget, and it preserves the physical option of Approach 3 by publishing the same rules as a **simplified paper variant** where they fit.

**What remains playable without electronics, per approach:**
- **Approach 1:** everything essential — that is its point.
- **Approach 2:** a *simplified variant* only — the printed core (event + a reduced action set + the six markers) is playable; derived centralities, hidden info and rival AI are **not**.
- **Approach 3:** the documented core is playable by hand; the app (bookkeeping, event generation, network view) is **optional**. The app must state exactly which turn operations become unavailable if switched off.

This recommendation is a **proposal**, not an approved choice, and does not by itself decide the M3/M4 designs.

---

## 12. Non-goals and guardrails for any Global implementation

- **No canon, no mechanics** until author approval ([#282](https://github.com/TomiToivio/NooPunk/issues/282)).
- **No tests/CI over this prose** ([AGENTS.md](../../AGENTS.md), [#271](https://github.com/TomiToivio/NooPunk/issues/271)).
- **No modification** of `RULEBOOK.md`, `rulebook/`, `src/`, `data/rules/`, the loader/scaffold, or the existing #309/#322/#282 documents.
- **No rewriting legacy lore.**
- **No mandatory LLM / database / server / account.**
- **No function system as ownable property; no scalar "hegemony"; no universal system effect; no "increase influence" button.**

---

## 13. Cross-links

- Long-term vision: [`VISION.md`](VISION.md) ([#309](https://github.com/TomiToivio/NooPunk/issues/309))
- Local-city MVP design note: [`../../strategy_game/docs/MVP_LOCAL_CITY_M0.md`](../../strategy_game/docs/MVP_LOCAL_CITY_M0.md) ([#322](https://github.com/TomiToivio/NooPunk/issues/322))
- Scaffold and approval boundaries: [`../../strategy_game/docs/INTEGRATION_BOUNDARIES.md`](../../strategy_game/docs/INTEGRATION_BOUNDARIES.md) ([#282](https://github.com/TomiToivio/NooPunk/issues/282))
- Four-leader council / missions / relationships: [`../../strategy_game/docs/LEADER_COUNCIL_SYSTEM.md`](../../strategy_game/docs/LEADER_COUNCIL_SYSTEM.md) ([#323](https://github.com/TomiToivio/NooPunk/issues/323))
- Global faction roster (author taxonomy): [`../../strategy_game/docs/GLOBAL_FACTIONS.md`](../../strategy_game/docs/GLOBAL_FACTIONS.md) ([#328](https://github.com/TomiToivio/NooPunk/issues/328)/[#329](https://github.com/TomiToivio/NooPunk/issues/329))
- Core containers: [`../../strategy_game/core.py`](../../strategy_game/core.py); political vocabulary: [`../../strategy_game/politics.py`](../../strategy_game/politics.py); provenance: [`../../strategy_game/provenance.py`](../../strategy_game/provenance.py); views: [`../../strategy_game/view.py`](../../strategy_game/view.py)
- Source verification ledger (companion): [`NOOPUNK_GLOBAL_SOURCE_LEDGER.md`](NOOPUNK_GLOBAL_SOURCE_LEDGER.md)
- The two core-insight sources (Sigma Theory; The Shadow Government Simulator) and the carry-over / open-finding notes: **§6A** and **§6B** above

## 14. Deliberately not done here

- No rules, numbers, thresholds or transitions are fixed; every figure is illustrative and unapproved.
- No implementation, no code change, no new test, no CI step.
- No hacking model chosen (M4.1).
- No winner declared between #322 and Global (M0.7); the decision is deferred to playtest evidence (M5).
- No canon, no named new character/institution/date/faction.
- The seven-simulator mechanics I could not reach are recorded as **unverified**, not guessed (§6; ledger).
