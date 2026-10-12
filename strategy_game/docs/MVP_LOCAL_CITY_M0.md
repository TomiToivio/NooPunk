# MVP local-city design note (M0) — issue #322

**Status: PROPOSAL, awaiting author review. Nothing here is a game rule.** This document defines no canon, implements no turn engine, adds no code, and changes no data file. It is the M0 deliverable of [#322](https://github.com/TomiToivio/NooPunk/issues/322), written to satisfy that issue's own instruction: *"Propose the minimal state schema and exact action/turn rules in this issue before building complexity."*

Mechanics are **gated**: `docs/design/VISION.md` §7 puts this at **S0-A — design gates, with any playable mechanic awaiting author approval**, and [`INTEGRATION_BOUNDARIES.md`](INTEGRATION_BOUNDARIES.md) says the faction view may show records but must not *"assign actions, resources or victories"* before rule approval. Nothing below is implemented. Documents are reviewed editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

---

## 1. Scope: one city, and only one city

**The world is global; the game board is local.** The playable arena is **one city and its environs** — districts, an industrial/logistics zone, one neighbouring town and a rural hinterland. National and global forces enter as institutions, background conditions and event effects, never as a playable map.

**Interchangeable templates, not fixed regional stereotypes.** The city is a **scenario configuration**, not a hard-coded country. No Finnish or US electoral structures, geography or institutions at the engine level.

**Out of scope — permanently, not "later":**

- advanced tactical combat, individual citizens, parcel-level geography, street navigation;
- a detailed economics model, planetary or global maps, world simulation;
- full national elections, simulated international politics;
- importing the LaclauGPT research pipeline, its data or its analyses as a runtime dependency.

**Explicitly deferred to a sibling issue** (do not duplicate):

| Concern | Owner |
| --- | --- |
| the four-leader roster, missions, portfolios, relationships | [#323](https://github.com/TomiToivio/NooPunk/issues/323), [#326](https://github.com/TomiToivio/NooPunk/issues/326) |
| the generic location schema and the first concrete configuration | [#324](https://github.com/TomiToivio/NooPunk/issues/324) deliverable C |
| global faction canon as setting data | [#328](https://github.com/TomiToivio/NooPunk/issues/328) / [#329](https://github.com/TomiToivio/NooPunk/issues/329) |
| the ideological-realignment analysis | [#327](https://github.com/TomiToivio/NooPunk/issues/327) |

This note therefore specifies only what #322 is for: **the minimal state schema, the exact action and turn rules, and the boundaries.**

---

## 2. Minimal state schema — extend `WorldState`, do not parallel it

`strategy_game` already carries the right vocabulary and **its public shape is pinned by tests and a CI smoke step**, so the MVP must **extend it, never widen or fork it**. What exists today (`strategy_game/core.py`):

```
WorldState(schema_version, leaders, factions, assets, locations, edges, events,  # + the political field)
             ^ already present: Leader, Faction, Asset, Location, NetworkEdge, Event
```

The board view is pinned at five keys and the package `__all__` at an exact set. **The MVP adds no new top-level view key.** Every MVP quantity below is either already representable or a *field on an existing record*.

**PROPOSED** — the smallest set that runs a turn, each mapped to where it already lives or what it adds:

| MVP quantity | Home | Status |
| --- | --- | --- |
| support pool per district | `Location` field (new, optional) | PROPOSED |
| institutional influence | `Location` field (new, optional) | PROPOSED |
| network connectivity | already `NetworkEdge` + `NetworkNode` | **exists** |
| security pressure | `Location` field (new, optional) | PROPOSED |
| location tag | `Location` field (new, optional) | PROPOSED |
| faction resources | `Faction` field (new, optional) | PROPOSED |
| organizational form | `Faction` tags — **not** a class or enum | PROPOSED |
| ideological claims | already `politics.py` (`Demand`, `Signifier`, `Formation`, `Frontier`) | **exists** |
| provenance of every authored value | already `provenance.py` (`ProvenanceKind`, unknown by default) | **exists** |
| characters | already `Leader`, with `attributes` and `personality_tags` as **uninterpreted data** | **exists** |

**Three schema rules, and they are the substance of this note:**

1. **Prefer the smaller nonredundant set.** The issue lists eight illustrative faction variables; this note proposes **four**. *Legitimacy* is not separate from *support* plus *institutional influence*; *network reach* is the graph, not a scalar; *radicalization* is a tag, not a meter; *tech access* is an asset or a tag.
2. **No numeric score for a political concept.** Discourse quantities stay labels and relations. A number that aggregates "hegemony" is exactly what the crossover's invariants forbid, and a derived percentage is the same defect wearing a decimal point.
3. **Absence stays absent.** A district with no recorded support value is *unknown*, not zero — `provenance.py` already treats unknown as the default, and the MVP must not silently upgrade it into evidence.

---

## 3. What each character does — deferred, with the MVP requirement stated

The issue requires **four active named characters per faction**, including the player's local leader, with NPC factions using the **same** data model and rules. **How** leaders are assigned, what portfolios they hold and how relationships work is [#323](https://github.com/TomiToivio/NooPunk/issues/323)'s design, not this one.

This note records only the constraint the turn loop must respect:

> **Every active faction move is carried out by a named leader.** Money, volunteers, contacts and equipment are **resources and capacity**, never extra independently-controlled action slots. At MVP a faction therefore has **at most four leader-led actions per turn**, reduced by injury or unavailability.

---

## 4. The turn loop — exact, and deliberately small

**PROPOSED.** Six steps, in this order:

1. **Global-to-local event.** Draw **one** event. It modifies local tensions, technologies, public meanings or institutions. One event per turn, not a deck of surprises.
2. **Situation.** Show the city overview: district influence, contested issues, faction and character status.
3. **Faction allocation.** Each faction spends scarce money, volunteers, attention, credibility, equipment and organizational capacity, and assigns its leaders to actions (≤4 per faction).
4. **Resolution.** Deterministic: seeded dice or thresholds. No LLM, no network.
5. **Consequences.** Update support, institutional influence, ties, resources and tags. Every action must **visibly change something** — the loop has no idle turns.
6. **Report.** A short consequential log: what each faction did *visibly*, and the changed balance. The report is the deliverable as much as the state is.

**The action menu is fixed and small** — six verbs, each with one resolution pattern rather than a bespoke subsystem: **campaign, organise, negotiate, investigate, communicate, develop**. Community aid, demonstrations, institutional participation, recruiting, intelligence and local tech acquisition are *outcomes framed by* these six, not additional subsystems.

**Determinism is a requirement, not a preference.** A run is reproducible from its seed, and every turn is reconstructible from a saved history. That is what makes the results log inspectable and what lets the scenario run with no model, no service and no account.

**Faction change, not classes.** Organizations move along **independent dimensions** — public legitimacy, openness/discipline, institutional vs extra-institutional tactics, coercion, spiritual authority, illegal activity — never a single `party → extremist → cult → militia → gang` track. A party may grow a mutual-aid wing, a militant split, a religious worldview or illicit financing, and a religious movement may remain peaceful and civic. In the MVP these transitions are **tags and events**.

**The comparative reference is a discipline, not a template.** The Black Panther Party and its offshoots are studied as one comparative case of community organising, mutual aid, revolutionary discourse, state pressure and internal splits — **not** to collapse distinct organisations and eras into a stereotype, and never to equate radical ideology with criminality.

**A hard boundary on content.** The game models political and social *consequences*. It must not become a manual for real-world violence, coercion or crime. Coercion and illegal activity appear as **tags with social consequences**, never as instructions.

---

## 5. Milestones, and what is gated

The issue's M0–M5, with this note's position:

| | Milestone | State |
| --- | --- | --- |
| **M0** | this design note | **this document** |
| **M1** | deterministic vertical slice: city data models, 3 factions × 4 leaders, serialization, one turn resolver, CLI | **gated** — awaits S0-A approval |
| **M2** | core politics: a few Laclaudian issues, district support, Castellsian ties, simplified institutional legitimacy, 4–6 actions, readable logs | gated |
| **M3** | global event deck, local research/adoption with costs and risks | gated |
| **M4** | organizational evolution via non-exclusive tags and event-driven shifts | gated |
| **M5** | playtest: a complete ~12-turn scenario, basic rival-faction AI, end criteria, sample transcript | gated |

**M1 is already partly satisfied and must not be duplicated.** `strategy_game` exists, runs headless with the standard library alone, and its view model already round-trips through JSON; `CI` smoke-checks it. M1's remaining work is the **turn resolver and the first scenario configuration** — not a new package.

---

## 6. Open decisions this note does not take

1. **Is the MVP's first scenario Ukweli?** [#324](https://github.com/TomiToivio/NooPunk/issues/324) proposes the Republic of Ukweli as the default *named* scenario while keeping the city generic. If yes, this schema must stay generic and Ukweli must be pure configuration. The inventory records Ukweli's outstanding naming conflicts.
2. **Three or five factions at MVP?** The issue says 3–5 initially and three if necessary to finish. This note assumes **three**, matching [#325](https://github.com/TomiToivio/NooPunk/issues/325)'s canonical three-party lineup.
3. **Do the four proposed `Location` fields belong on `Location`, or in the scenario configuration only?** Putting them on the record makes a district carry political state; keeping them in configuration keeps the engine politically empty. **Recommendation: configuration**, so the engine stays generic — but this is a structural call and it is yours.
4. **Approval of S0-A concepts**, which is what actually unblocks M1–M5.

---

## 7. Cross-links

- Overall vision and the S0–S4 plan: [`docs/design/VISION.md`](../../docs/design/VISION.md) (#309)
- Integration and authority boundaries: [`INTEGRATION_BOUNDARIES.md`](INTEGRATION_BOUNDARIES.md) (#282)
- Political layers: [`POLITICAL_SIMULATOR_SCOPE.md`](POLITICAL_SIMULATOR_SCOPE.md), [`POLITICAL_SIMULATOR_MODEL.md`](POLITICAL_SIMULATOR_MODEL.md), [`POLITICAL_SIMULATION_DESIGN.md`](POLITICAL_SIMULATION_DESIGN.md)
- Global factions as setting data: [`GLOBAL_FACTIONS.md`](GLOBAL_FACTIONS.md)
- Ukweli scenario and its canon inventory: [`../../docs/scenarios/UKWELI_LOCAL_SCENARIO.md`](../../docs/scenarios/UKWELI_LOCAL_SCENARIO.md), [`../../docs/design/ISSUE_324_UKWELI_CANON_REUSE.md`](../../docs/design/ISSUE_324_UKWELI_CANON_REUSE.md)

**This note deliberately does not:** define a rule, a number, a resolution formula or an outcome table; touch any code, test or data file; resolve §6; or claim that M1–M5 are done.
