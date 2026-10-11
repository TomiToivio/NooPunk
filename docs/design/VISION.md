# NoöPunk — long-term vision

**Status: LONG-TERM NORTH STAR. Aspirational.**

This document is a direction, not an instruction. It **authorizes no mechanics, no
canon, no numerical design and no scope**. It does not override
[`AGENTS.md`](../../AGENTS.md), and where the two ever disagree, `AGENTS.md` wins.
Nothing here is a commitment, a date, or a promise of AAA or MMO scale.

It exists for one purpose: **to keep the long horizon coherent while every actual
increment stays small.** The horizons in §7 are gates, not entitlements. Each one must
deliver a game that stands on its own; the full dream is optional and does not
retroactively justify building it now.

Sources: issue [#309](https://github.com/TomiToivio/NooPunk/issues/309) (this vision),
the crossover directive [#306](https://github.com/TomiToivio/NooPunk/issues/306), the
scaffold [#282](https://github.com/TomiToivio/NooPunk/issues/282) and its layer-design
tracks [#295](https://github.com/TomiToivio/NooPunk/issues/295) ·
[#296](https://github.com/TomiToivio/NooPunk/issues/296) ·
[#297](https://github.com/TomiToivio/NooPunk/issues/297).

**Reading test.** Having read only this file, an agent should be able to answer:
*(a) which game am I working on? (b) what may I build now? (c) what must I not do?
(d) where does the next increment go?* If it cannot, this document has failed and
should be fixed — by hand and by author review, never by a test (§10).

---

## 1. One universe, two games

There is **one fictional universe and two games** in this repository. The distinction is
binding and predates this document ([#306](https://github.com/TomiToivio/NooPunk/issues/306)):

| | Legacy NoöPunk RPG | NoöPunk × LaclauGPT crossover |
|---|---|---|
| Path | `RULEBOOK.md`, `rulebook/`, `src/`, `data/rules/` | `strategy_game/` |
| Rules | its own, unchanged | **NO RULES APPROVED** |
| Status | developed, not to be rewritten | active new game, H0 |
| Timeline | its own default campaign | **acceleration toward** the NHI Crisis |

- **Lore is shared.** Characters, institutions, NHI concepts and prior creative work
  carry over as common setting background, subject to scenario-specific deviations and
  author decisions. **Never delete or casually overwrite old lore.**
- **Rules are not shared.** Legacy attributes, skill procedures, lifepath, character
  sheets and gameplay are **not** canonical for the crossover. Cross-referencing is
  welcome; **importing a mechanic requires an explicit, author-approved conversion.**
- **The legacy RPG is never rewritten to accommodate the crossover.**

See §11 for which existing design documents govern which game — several are legacy-only
and must not be read as crossover doctrine.

## 2. The ultimate game

A New Weird roleplaying game and political simulation in which one person may play a
character, a faction leader, a shaper of public discourse, or a hand on the machinery of
planetary civilization — and in which, at the far horizon, many humans and optional
LLM-driven characters inhabit a persistent world together.

**Primary genre: New Weird.** The setting is organized around paradigm shift, ontological
mystery and institutions under stress. Social science fiction, science fantasy,
geopolitical satire, investigative mystery, philosophical science fiction, cosmic
strangeness and cyberpunk are **supporting ingredients**. Cyberpunk is *secondary* — a
texture and a politics, not the organizing principle, despite the project's name.

The core period opens with the **acceleration toward the NHI Crisis**, in which three
shifts interact: AGI acceleration and cyborgization; UFO disclosure and NHI awareness;
and psychic awakening, psionics and psychotronics. Political disruption begins **before**
full crisis. Ideologies that emerge around these shocks — including AI doomerism, NHI
infiltration paranoia and novel single-issue populisms across the spectrum — are
simulated as **contestable perspectives, never as inevitable truths**.

Tone shifts contextually: comic, bureaucratically absurd, tragic, cerebral, genuinely
alien. New Weird is the umbrella; social science fiction and dark science-fiction comedy
are deliberate modes.

## 3. Six scales of agency

One universe, many scales. The player may move between them; the simulation need not
tick every scale at the same granularity.

| Scale | Player experience |
|---|---|
| **Person** | An UNSA field agent, scientist, journalist, activist, diplomat, hacker, psychic, posthuman or faction leader — lifepath, relationships, missions, meaningful choices and consequences |
| **Organization / faction** | Lead a movement, network, intelligence cell, corporation, institute or NHI-aligned organization — leaders, assets, operations, covert and overt power, delegation, rivalry |
| **Society / discourse** | Contest hegemony through narratives, identities, alliances and communication networks — signifiers, frontiers, legitimacy, coalitions. **Abstract and gameable**, never the research stack |
| **Nation / planet** | Change states and global governance under ontological crisis — institutions, diplomacy, UNSA, crisis response, science, conflict, surveillance, trust |
| **Solar system / beyond** | Follow disclosure and accelerating technology outward — settlement, posthuman polities, asymmetric civilizations, unknown realities |
| **Persistent world** | Humans and optional LLM characters collectively produce ongoing history — persistent factions, delegated agents, asynchronous play, moderation and governance |

**Multiscale continuity.** Consequence travels upward and downward: a discovery can change
a faction's strategy; its public reading can move discourse; alignment can shift state
policy; strategy can create personal missions. Players must be able to **focus on one
scale and delegate, abstract or ignore the rest.**

*Illustrative causal chain — fiction, not a chosen mechanic:* an investigator finds
ambiguous evidence of possible NHI involvement → a faction leaks it → rival populists
frame it as liberation versus infiltration → communication networks amplify both frames →
legitimacy and coalitions shift → governments revise cooperation → new investigation and
diplomacy missions become playable. **Genuine ambiguity is preserved; nothing "must"
happen.**

## 4. Design pillars

These are written as **tests**, so a proposed feature can be rejected against them.

1. **New Weird first.** Paradigm shift and ontological mystery outrank hardware. NHI,
   PSI, AGI and psychotronics are game-world elements, **not claims about real science**.
2. **Social science as design, not as proof.** Laclau's content of struggle, Castells's
   network structure and power, and agent-based institutions give *interpretable*
   inspiration. The simulation is a **simplified game model**; no claim that theory
   mathematically determines an outcome is permitted.
3. **Character agency *and* structural forces.** Motivations and relationships coexist
   with faction strategy, ideology, networks and institutions. Neither spreadsheet
   geopolitics nor empty exploration.
4. **Something interesting at every scale, and little dead air.** Terra Invicta's breadth,
   far smaller and faster — dense decision loops, unexpected crises, real tradeoffs.
5. **Architect / Agent delegation.** Hands-on missions versus strategic orders;
   subordinates have interests and can surprise the player, while play stays legible.
6. **Human/LLM parity of *roles*, not of implementation.** A human or an AI may inhabit an
   NPC, leader, faction or diplomat — within explicit permissions, compute budgets and
   anti-abuse boundaries. LLM play is a bounded participant, never an unbounded optimizer.
7. **Simulation first, presentation later.** Headless world model and playable text/2D
   interfaces first; attractive interfaces next; cinematic 3D last, and only if resources
   exist.
8. **Persistent causality and legibility.** The game must be able to explain *why* society,
   loyalties and power changed. Deterministic rules, randomness, LLM-generated content,
   authored canon and in-world claims are **distinguishable**, always.
9. **Player and creator agency.** Scenario editing, faction and leader creation, modding
   interfaces, user campaigns, community storytelling — and, at the far horizon, shared
   world-building with moderation.
10. **Accessible scope.** Modular solo play must remain viable **even if** the MMO and AAA
    ambitions never happen. This pillar outranks the rest when they conflict.

## 5. Technical architecture (candidates, not commitments)

- **Engine-neutral, versioned** simulation and world-state API. Initial implementation
  lightweight **Python**, with explicit person / faction / discourse / world data
  contracts. Candidate libraries: dataclasses or Pydantic, NetworkX, optionally Mesa.
  **The core simulation must run with no LLM, no database service, no 3D engine and no
  network server.**
- **Independent layers:** RPG decision and resolution; character relationships and the
  organizational/agent layer; the simplified Laclau–Castells political simulation; global
  strategy; optional off-world simulation.
- **Model-assisted behaviour is a proposal layer.** Plug-in Ollama or cloud providers may
  generate dialogue, interpretation, deliberation and procedural scenarios. **LLM output
  never mutates authoritative state**; it is checked against authorized actions, canonical
  facts, rules and budgets.
- **Determinism and inspection:** recorded action/event log, seedable resolution,
  snapshots, replay tools, versioned schemas, explicit provenance. **Stochasticity lives
  in the proposal layer, not in the authoritative result.**
- **Interfaces:** CLI/text and a minimal 2D map first; a polished strategy map, character
  scenes and mission UI later; engine clients are extensible and **Godot is one candidate,
  not a locked choice**.
- **Multiplayer, far later:** authoritative server, permissions, access-controlled state,
  rate limits, persistence, rollback and conflict resolution; human/human, human/LLM and
  LLM/LLM interaction **without unlimited autonomous operation**.
- **Modding and UGC:** data-driven events and entities, a documented scenario format,
  stable extension contracts, content provenance and licensing, moderation, optional
  publishing. **Never copy proprietary code, assets or rules text** from any referenced
  commercial game.

## 6. Reference studies

Inspiration for study, never a source to port. **No proprietary rules text, assets or code
is copied or depended upon.**

- **Terra Invicta** — multi-faction geopolitical and space strategy, councilors, crisis.
  Proprietary but moddable; a *prototype mod* path may be studied, but a total conversion
  must never be presumed releasable as a standalone product.
- **Democracy 4** — policy choices, voter blocs, feedback loops.
- **Crusader Kings III** — character-focused long-horizon strategy and emergent narrative.
- **Dune: Adventures in the Imperium** — Architect/Agent framing and strategic delegation.
- **Eclipse Phase** — deep transhuman and existential science fiction for the RPG layer.
- **Cyberpunk 2077** — embodied city-scale storytelling and cinematic ambition.
- **Stellaris** — expandable civilization-scale strategy and emergent history.
- **EVE Online** — persistent player-led geopolitics, organizations, living economy.
- **Citizen Sleeper** and **Disco Elysium** — dense decisions, character voice, unusual
  institutions, minimal wasted movement.
- **NoöPunk tabletop rulebook and lore** — shared universe where relevant, but **the
  crossover is a separate scenario, game and rules implementation**, not a forced merger
  of rulebooks.

## 7. Horizons and gates

No dates. No commitments. **Every horizon must deliver a coherent game by itself**, and
each carries a **scope kill switch** — the thing that, if it is not working, gets cut
rather than rescued.

**H0 — Today: tiny, independent, actually playable.**
Three simple gameplay layers, an abstract board, a very small rule system, fast
consequential turns. This is [#282](https://github.com/TomiToivio/NooPunk/issues/282) and
its layer tracks [#295](https://github.com/TomiToivio/NooPunk/issues/295) ·
[#296](https://github.com/TomiToivio/NooPunk/issues/296) ·
[#297](https://github.com/TomiToivio/NooPunk/issues/297). Existing "no unapproved
mechanics or canon" instructions remain in force.
*Gate:* a complete, fun, explainable mini-scenario one person can finish.
*Kill switch:* any layer that cannot be explained on a table.

**H1 — Polished indie political RPG/strategy.**
Character creation and lifepath, leaders and agents, scenario authoring, dialogue and
events, an appealing 2D interface, coherent social-science-inspired rules, saves and
replay, one complete NHI-acceleration campaign.
*Gate:* repeatably enjoyable, not an impressive architecture diagram.
*Kill switch:* interface polish displacing rule coherence.

**H2 — Deep systemic living world.**
Factions evolve; characters form relationships and loyalties; policy and discourse
interact; local and global consequences become visible; optional bounded LLM character
play; robust scenario modding.
*Gate:* consequential emergent stories with understandable causes, at acceptable compute
cost and pacing.
*Kill switch:* LLM cost or latency becoming load-bearing for the experience.

**H3 — Grand-strategy expansion.**
Expanded Earth governance, UNSA diplomacy, geopolitics, space operations, posthuman
factions, further worlds and NHI contacts where appropriate.
*Gate:* strategic depth without idle-turn inflation.
*Kill switch:* any system that only produces waiting.

**H4 — Persistent multiplayer world.**
Private and co-op worlds first, then shared persistent servers with human and
LLM-controlled characters, safe creator tools and a clear governance model.
*Gate:* stable authoritative persistence, economical operation, moderation, anti-griefing,
auditability, retention.
*Kill switch:* a governance or moderation problem we cannot honestly solve.

**H5 — AAA / MMO-scale horizon.**
Cinematic 3D, detailed environments, high-fidelity missions, potentially EVE-like scale.
This is a **funding, team and technology-dependent production horizon**, not something
today's Python scaffold must already support.
*Gate:* explicit production feasibility — team, funding, content pipeline, engine, online
operations, maintenance.
*Kill switch:* everything upstream of feasibility.

### Vision-versus-commitment ledger

| Horizon | Gate | Kill switch | Owning issue |
|---|---|---|---|
| H0 | a finishable, fun mini-scenario | a layer that cannot be explained on a table | #282, #295, #296, #297 |
| H1 | repeatably enjoyable | polish over coherence | *unassigned* |
| H2 | emergent stories with clear causes | LLM cost as a dependency | *unassigned* |
| H3 | depth without dead turns | systems that only produce waiting | *unassigned* |
| H4 | stable, governable persistence | unsolvable moderation/governance | *unassigned* |
| H5 | production feasibility | everything upstream of it | *unassigned* |

**Only H0 has an owning issue, and that is deliberate.** Assigning owners to H1–H5 before
H0 ships would be the scope creep this document exists to prevent.

## 8. Non-goals for current agents

- Do **not** attempt to build an AAA RPG, a grand strategy game and an MMO simultaneously.
- Do **not** import the LaclauGPT research pipeline, claims of scientific causal certainty,
  or proprietary game content.
- Do **not** rewrite existing NoöPunk RPG rules, invent canon, select or implement new
  mechanics, or expand the scope of #282 / #295 / #296 / #297 without author approval.
- Do **not** replace local, testable rules with non-deterministic LLM-only gameplay.
- Do **not** require high-fidelity art, online infrastructure, enormous space maps or
  continuous simulation for the first playable prototype.
- Do **not** treat this document as approval for anything. It has none to give.

## 9. Open design artifacts

Each is a future piece of work, carried by a scoped issue rather than built from here.

- [ ] A **one-page playable vertical-slice pitch** — actions at person, faction and discourse scales.
- [ ] A **cross-scale world-state and event-flow architecture** — where consequence travels, and where simulation is abstracted.
- [ ] **Candidate engines, Python-to-engine bridges and licensed/modding prototypes**, findings kept non-binding.
- [ ] **Separation of human-played, LLM-played and rules-driven roles**, with the limits of delegation.
- [ ] The **horizon feature matrix** with dependencies and kill switches — extended from §7's ledger.
- [ ] **UGC governance** — moderation, canon conflicts, multiplayer trust, attribution.
- [ ] **Playtesting criteria** — engagement per minute, meaningful consequences per turn, clarity of power shifts, replayability, operational cost.
- [ ] A **discipline check**: the vision re-read against the three-layer prototype, so immediate development stays small.

## 10. How this document changes

- **Vision is not commitment.** Nothing here may be cited as approval, as a requirement, or
  as a reason to skip a gate.
- **Revisions go through an issue**, and land as a small reviewable change. An agent must
  not opportunistically extend this document while doing unrelated work.
- **Mechanics never live here.** If a proposal needs rules, statistics or numbers, it belongs
  in a scoped design issue, not in the vision.
- **This file is never guarded by tests.** Per `AGENTS.md` and
  [#271](https://github.com/TomiToivio/NooPunk/issues/271), the automated-test policy covers
  executable code only. No CI assertion, snapshot, schema lock or smoke step may check this
  document's prose, structure or wording. It is reviewed editorially and by playtesting.

## 11. Which documents govern which game

Several existing design documents belong to the **legacy RPG** and are not crossover
doctrine. Read them with the table in §1 in hand:

| Document | Governs |
|---|---|
| [`docs/design/GAMEPLAY_LOOP.md`](GAMEPLAY_LOOP.md) | legacy RPG |
| [`docs/design/DEFAULT_INVESTIGATION_FANTASY.md`](DEFAULT_INVESTIGATION_FANTASY.md) | legacy RPG — **post-Singularity** default campaign |
| [`docs/design/RULEBOOK_STRUCTURE.md`](RULEBOOK_STRUCTURE.md) | legacy RPG |
| [`docs/design/LORE_CHAPTERS_SCOPE_2026-10-07.md`](LORE_CHAPTERS_SCOPE_2026-10-07.md) | legacy RPG lore |
| [`strategy_game/docs/POLITICAL_SIMULATOR_SCOPE.md`](../../strategy_game/docs/POLITICAL_SIMULATOR_SCOPE.md) | crossover |
| [`strategy_game/docs/POLITICAL_SIMULATION_DESIGN.md`](../../strategy_game/docs/POLITICAL_SIMULATION_DESIGN.md) | crossover |
| [`strategy_game/docs/POLITICAL_SIMULATOR_MODEL.md`](../../strategy_game/docs/POLITICAL_SIMULATOR_MODEL.md) | crossover |
| [`strategy_game/docs/RULE_SYSTEM_RESEARCH.md`](../../strategy_game/docs/RULE_SYSTEM_RESEARCH.md) | crossover |
| [`strategy_game/docs/INTEGRATION_BOUNDARIES.md`](../../strategy_game/docs/INTEGRATION_BOUNDARIES.md) | crossover |
| [`strategy_game/RULEBOOK.md`](../../strategy_game/RULEBOOK.md) | crossover — **placeholder, NO RULES APPROVED** |

**The timeline warning is the one to internalize.** The legacy default campaign is set
*after* the Singularity. The crossover begins in the **acceleration toward** the NHI
Crisis, with everyday institutions and ordinary electoral politics still recognizable.
The two are not interchangeable, and this vision does not move either one.

---

*This document implements [#309](https://github.com/TomiToivio/NooPunk/issues/309). It grants
no permissions, changes no rules, and invents no canon.*
