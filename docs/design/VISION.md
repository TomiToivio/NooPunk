# NoöPunk long-term vision: one New Weird universe, many scales of agency

> **Status: ASPIRATIONAL NORTH STAR (issue [#309](https://github.com/TomiToivio/NooPunk/issues/309)).** This document authorizes **no new canon, rules, mechanics, gameplay actions, implementation scope, dates or production commitment**. It does not supersede [AGENTS.md](../../AGENTS.md), the relevant rulebooks, design approvals, or [the three project balances](../archive/DESIGN_PRINCIPLES.md). Each horizon must deliver a coherent experience independently. **AAA/MMO are optional distant ambitions, not requirements for H0.**
>
> **Scope:** a universe-level vision spanning the legacy NoöPunk RPG and the separate NoöPunk × LaclauGPT crossover. This is not a canonical rulebook or a strategy_game runtime specification.

## 1. Product thesis and boundaries

**One fictional universe, multiple independent ways to play it.** The ultimate aspiration combines the person-level depth and presentation ambitions of Eclipse Phase and Cyberpunk 2077; the leader and organisation play of Crusader Kings III and Dune's Architect/Agent viewpoint; the discourse- and institution-centred choices of Democracy 4 interpreted through selected Laclau/Mouffe and Castells ideas; the crisis geopolitics of Terra Invicta; the scale of Stellaris; and an EVE-like persistent human/AI-populated world with user-generated content.

**New Weird is the primary genre.** Social science fiction, science fantasy, philosophical SF, shifting dark-comic/investigative/alien moods, and cyberpunk are ingredients; cyberpunk is secondary. The story's distinguishing pressures are the interacting AGI/cyborg, NHI-disclosure and independent PSI/psychotronic paradigm shifts. Avoid fixing an unapproved chronology, inventing a scientific certainty, or reducing ontological mystery to another technology tree.

**Two games, one shared world (issue #306):**
- **Legacy RPG:** governed by [RULEBOOK.md](../../RULEBOOK.md), [rulebook/](../../rulebook/) and the existing tabletop-to-Godot/Concordia process. Its later/post-crisis default investigation scenario is described in [DEFAULT_INVESTIGATION_FANTASY.md](DEFAULT_INVESTIGATION_FANTASY.md) (**governs legacy RPG only**).
- **Crossover strategy/RPG/political simulator:** governed independently by [strategy_game/RULEBOOK.md](../../strategy_game/RULEBOOK.md) and its proposed designs, starting during **acceleration toward** the NHI Crisis while ordinary institutions still function. The legacy rules do **not** automatically carry over. Shared lore is general background unless a scenario explicitly deviates.
- **Future multiscale clients / living world:** speculative future products or modes, not authorization to merge rulebooks or modify legacy RPG files. Interoperability would need explicit mapping and approval.

**Current practical objective:** build a *fast, small, abstract, comprehensible, tabletop-convertible* political leader/faction/discourse game. A compelling game that ends at this scale is a success.

## 2. Six scales, one possible chain of consequences

| Horizon of agency | Player view | What could connect later (not mechanics) |
| --- | --- | --- |
| Person | Field agent, scientist, politician, activist, operative, NPC | Choices, identity, motives, relationships and mission consequences |
| Faction / organisation | Leader, subordinates, assets, alliances, rivals | Strategy, delegated operations, group capacity and loyalties |
| Society / discourse | Articulated demands, contested signifiers, political frontiers and communication channels | Coalitions, legitimacy, network access and competing interpretations |
| State / planet | Institutions, politics, UNSA, diplomatic crisis | Policy, consent, coordination, jurisdiction and geopolitics |
| Solar system and beyond | Posthuman and NHI diplomacy, space civilisation | Strategic expansion and inter-civilisational consequences |
| Persistent world | Human and bounded LLM players, creator communities | Multiplayer persistence, negotiated governance, modular UGC |

**Key distinction:** these are *views* into related events, not six physics engines all running at full fidelity. Model detail where a decision matters; use coarse aggregation, summaries and event boundaries elsewhere. Only design specific propagation rules following author approval.

**Illustrative, non-canonical cross-scale episode:** an investigator finds ambiguous indications of NHI influence; a faction publicises a partial report; competing movements frame it differently; media relationships affect which frames circulate; institutions face public pressure; an UNSA mission becomes relevant. The player's interface should distinguish **what happened**, **who claims what**, **what the rules actually changed**, and **what remains unknown**. This is a sample design narrative, not established lore or a specified algorithm.

## 3. Non-negotiable design qualities

**Two load-bearing principles:**
1. **Simulation first, presentation later.** A playable Python/tabletop strategy experience must not wait on a Godot front end, cinematic art, online servers, agent swarms or a galactic map.
2. **Persistent causality and legibility.** A player can inspect why a relationship, coalition, policy or event changed, including source, cause, uncertainty and rule outcome. This is the social-science game's distinctive promise.

Also preserve: deliberate scope limits, narrative/gamist/simulationist balance per [canonical principles](../archive/DESIGN_PRINCIPLES.md); eventful pace with few empty turns; many tones without a single compulsory mood; character agency inside institutions; an open and moddable *original* design; human/LLM participation subject to permission and cost budgets; and both offline/solo play and eventual community-created scenarios.

**Epistemic labels:** keep separate (a) sourced statements about historical reality, (b) public scientific consensus, (c) in-world actor/faction claims, (d) explicitly invented scenario premises, (e) simulated game outcomes and (f) unresolved mystery. The existing legacy rulebook's epistemic discipline is an inspiration for presentation, not an instruction to import its mechanics. Laclau/Mouffe and Castells illuminate possible game abstractions, not verified predictive social laws.

## 4. H0: implementation proposal for the existing crossover

**Existing reality:** [#282](https://github.com/TomiToivio/NooPunk/issues/282) has a distinct Python scaffold, not playable rules; [#295](https://github.com/TomiToivio/NooPunk/issues/295) considers leader/NPC RPG, [#296](https://github.com/TomiToivio/NooPunk/issues/296) faction-management strategy and [#297](https://github.com/TomiToivio/NooPunk/issues/297) discourse/network power. [#302](https://github.com/TomiToivio/NooPunk/issues/302) addresses society/institutions, [#303](https://github.com/TomiToivio/NooPunk/issues/303) tone, [#304](https://github.com/TomiToivio/NooPunk/issues/304) optional agents, [#305](https://github.com/TomiToivio/NooPunk/issues/305) paradigm-shift populism, [#306](https://github.com/TomiToivio/NooPunk/issues/306) separation of games. The existing [scope](../../strategy_game/docs/POLITICAL_SIMULATOR_SCOPE.md) forbids wholesale import of LaclauGPT.

### H0-A: editorial and design gates (before playable mechanics)
- Review the three existing layer proposals *separately* with author and other agents. Select only necessary leader attributes/tags, faction decisions, political representations and interactions. No new numerical ranges, costs, randomness or canonical actors assumed here.
- Write a **one-page vertical-slice proposal** specifying the player, the initial tension, the three views, one illustrative consequential decision, the ending and the estimated cognitive burden. Author approval required before mechanics.
- Specify a **paper-playable version** of proposed rules for RPG leader, faction-management and discourse/network power. Review each separately, then review cross-layer event propagation as its own fourth gate.
- Identify which facts are historical, invented, factional, mechanically simulated or uncertain. Never conflate media reach with persuasion or game scores with measured hegemony.

### H0-B: minimal runtime after those approvals
- Keep **Python standard library** as baseline; all adapters optional. The current empty scaffold and view model are a starting point, not a request to restructure them.
- Proposed components (interfaces, not committed file structure): immutable/validated command intent; authorized rules resolver; versioned world snapshot; append-only event/provenance record; projections for character card, faction board and discourse graph; save/load/replay; text/2D front end.
- Allow *one* explicit player decision to yield a clearly explained event and changes visible across the three approved projections. Seed randomness and record inputs so rules resolution can be replayed. Proposed schema fields and event semantics need design review.
- Verify with **behavioral tests for executable code only**: valid/invalid command handling, save/load, deterministic replay of approved rules, no unauthorized state mutation and consistent event-to-view projections. **Never** add tests policing design prose, lore, canon or documentation wording.
- Release a short standalone, complete and replayable scenario. Gather playtest feedback on meaningful choices, clarity, wait time and session enjoyment. No specific turn duration, player count or numeric threshold is declared here.

### H0-C: graduation criteria
1. The author has explicitly approved all mechanics and scenario canon used.
2. A fresh player can understand the three views and finish a complete session without reading the research framework.
3. Every meaningful change has an inspectable in-game explanation.
4. The game runs and saves/loads offline without an LLM, MongoDB, Mesa, Godot or a server.
5. Gameplay tests pass; editorial/gameplay review, not documentation snapshot CI, validates the prose.
6. Small scope stays small: no empty-turn slog or administrative micromanagement.

## 5. Candidate world and agent architecture (future-facing, not approved runtime)

```text
 Human command / bounded LLM proposal / authored event
                      |
            Permission + schema validation
                      |
              Approved game resolver
                      |
            Authoritative world state
                      |
              Event + provenance log
                      |
    +-----------------+-------------------+
    |                 |                   |
 Character view   Faction view      Discourse/map view
    |                 |                   |
  Missions        Organisations       Society, institutions
```

- **Boundaries:** UI, LLM and scenario content may *propose* actions; **only an approved deterministic rules resolver mutates authoritative state**. LLM-generated prose cannot directly rewrite saves, canon, economy, powers or social relations.
- **Versioned contracts from the beginning, not enterprise infrastructure:** stable identities, source type, event cause, action attribution, optional seed/rule version and snapshot compatibility *as proposed fields*, to be reviewed before implementation. Prefer simple JSON initially.
- **Delegation:** Dune-inspired Architect/Agent viewpoint is a future interface: player selects an organisational intention, eligible subordinates propose bounded plans, the resolver checks capabilities and reports consequences. No autonomous tick economy until designed.
- **Human/LLM role parity:** agent identity and permissions are explicit; agents have finite action budgets and limited context, memory/provenance and audit trails; player and rules-generated actions use the same validation contract. Optional local Ollama or other provider; no network calls in baseline.
- **Performance:** simulate only active scenes/decisions in detail; aggregate off-screen societies. Establish profiling and simulation-frequency policies *only after* playtest evidence.
- **Extensibility:** scenario data can define factions, characters, events and maps only subject to licensing, safety/moderation and canon boundaries. Treat content injection as untrusted; creator text never has rule or server authority.

## 6. Roadmap: independent, gated experiences

| Horizon | Deliverable | Gate to proceed | Explicitly not required |
| --- | --- | --- | --- |
| **H0: core prototype** | Small Python/tabletop-convertible three-layer game after approvals | Complete replayable consequential mini-scenario, comprehensible causes and fun playtest | LLM, real geopolitics, global simulation |
| **H1: indie narrative strategy RPG** | Polished 2D/text story, lifepath/character experience, faction choices, eventful NHI-crisis acceleration campaign | Finished scenario, replayability and robust saves | 3D open world, MMO |
| **H2: systemic living society** | Deeper leaders, institutions, contested politics, bounded optional AI characters, modded scenarios | Emergent stories remain legible; compute/runtime budget sustainable | Solar system, persistent servers |
| **H3: planetary / space grand strategy** | Extended Earth systems, diplomacy and selective off-world layer | Fun strategically meaningful actions without long idle periods; performance proven | Interstellar exhaustiveness |
| **H4: shared persistent worlds** | Start with cooperative/private worlds, then moderated shared worlds with human and LLM-controlled roles | Authenticated permissions, reliable persistence/rollback, anti-griefing and service economics | Mass concurrency |
| **H5: AAA / EVE-scale ambition** | Optional 3D/cinematic and massive multiplayer production | Dedicated team, funding, art/content pipeline, moderation, server operations, realistic production plan | Never blocks previous horizons |

**Promotion rule:** every horizon must work as a *standalone enjoyable game*. Do not start a later horizon merely because a library, agent or funding possibility exists. Every later-stage change requires its own approved issue, explicit resource budget, regression analysis and playtest.

### Scope kill switches
- When performance/cost becomes excessive, disable optional LLMs, reduce background simulation detail or stop expanding map scope.
- When play is slow, cut events, low-value resources or inactive turns rather than adding more automation to justify them.
- When players cannot explain why political shifts occurred, simplify rules/projections before increasing theoretical complexity.
- When multiplayer compromises fairness or governance, retain excellent solo/co-op play as the default.
- When licensing or content provenance is unclear, do not distribute borrowed expression/assets.

## 7. Comparative research and feasibility

| Inspiration | Study | Avoid |
| --- | --- | --- |
| **Dwarf Fortress** | One recorded world, historical figures, different scales of play | Requiring its vast complexity |
| **Mount & Blade** | Character-level and strategic-map consequences | Unbounded combat development |
| **Suzerain** | Political story, state tradeoffs and finite impactful decisions | Treating scripted policy drama as social science validation |
| **Democracy 4** | Readable policy-feedback interface | Assuming voter groups are static or empirical causality known |
| **Terra Invicta** | Councillors, rival geopolitical factions, NHI crisis | Slow dead-air pacing; proprietary source reliance |
| **CK3 / Dune RPG** | Relationship politics, Architect/Agent delegation | Imported copyrighted expressions/mechanics |
| **Eclipse Phase / Citizen Sleeper / Disco Elysium** | Transhuman identity, rich dilemmas, tight interface | Large inventories of unused stats, repetitive traversal |
| **Stellaris / EVE** | Scale, emergent history, persistent faction organisations | Premature world simulation, online-ops cost |
| **Cyberpunk 2077** | Far-future cinematic production aspiration | Making visual fidelity prerequisite to a fun game |

**Feasibility decision points (research, no engine selection):** evaluate Python text/2D prototypes, Godot as a later view client, and only much later full 3D tooling. Compare licensing, Python interoperability, UI authoring, save formats, performance and multiplayer operations using a small spike. Terra Invicta is **proprietary though moddable**; mods may inform experiments but must not become required source for an original standalone game. Track exact licenses for source, rules text, art and UGC. Open-source licensing for code and Creative Commons licensing for rulebook/setting are separate decisions (see [license review](../licenses/ISSUE_200_CC_RELEASE_GATE.md)).

## 8. Decision backlog and author checkpoints

- [ ] Approve a player-centred *one-page H0 slice*; choose the initial faction, situation and end condition explicitly.
- [ ] Resolve #295 leader rules, #296 faction actions and #297 discourse/network transformations independently; record alternatives and rationale.
- [ ] Agree the cross-layer command/event/provenance specification before coding a playable turn.
- [ ] Evaluate architecture via a short tabletop playtest and standard-library executable prototype.
- [ ] Define a playable pacing target from actual playtesting; do not assume an arbitrary number.
- [ ] Document what constitutes source evidence vs faction claims vs simulated outcomes.
- [ ] Decide when and whether to introduce 2D graphical UI, optional agent adapters, Mod/UGC schema and co-op.
- [ ] For future multiplayer: design ownership, delegation, rate limits, abuse controls, licensing, canonical vs community worlds and governance before any public server.
- [ ] Revisit H3–H5 only with feasibility evidence and independent author approval.

## 9. Maintenance and source-of-truth rules

- The **issue #309** records the aspiration and discussion. This document is the navigable **vision and implementation roadmap**; it is **not** a source of mechanics or canon.
- **AGENTS.md / approved rulebooks / author decisions override this roadmap**. The crossover implementation remains at `strategy_game/`; no edit here automatically permits modifications to the legacy RPG.
- Refer to the existing detailed documents instead of duplicating their rules. If context changes, update issue discussion and this roadmap together via review.
- Documentation is reviewed editorially; no snapshot, string-matching or canon-prose CI gate.
- **Near-term next action:** finish approval and a small playable design in #295–#297 under #282, not a grand rewrite.

**References:** [#309](https://github.com/TomiToivio/NooPunk/issues/309) · [#282](https://github.com/TomiToivio/NooPunk/issues/282) · [#295](https://github.com/TomiToivio/NooPunk/issues/295) · [#296](https://github.com/TomiToivio/NooPunk/issues/296) · [#297](https://github.com/TomiToivio/NooPunk/issues/297) · [#306](https://github.com/TomiToivio/NooPunk/issues/306) · [strategy scope](../../strategy_game/docs/POLITICAL_SIMULATOR_SCOPE.md).
