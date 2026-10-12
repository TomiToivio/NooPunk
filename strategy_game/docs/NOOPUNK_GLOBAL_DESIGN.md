# NoöPunk: Global — comparative design dossier (proposal)

**Tracking:** [#338](https://github.com/TomiToivio/NooPunk/issues/338) · **Status:** design research, **NOT approved rules/canon** · 2026-10-12

This dossier evaluates a separate **worldwide but ultra-abstract** scenario for the NoöPunk × LaclauGPT crossover. It **does not replace** the local-city proposal [#322](https://github.com/TomiToivio/NooPunk/issues/322), the crossover scaffold [#282](https://github.com/TomiToivio/NooPunk/issues/282), or the long-term [#309](https://github.com/TomiToivio/NooPunk/issues/309) vision. No new mechanics, numbers or lore here are approved. Existing `strategy_game/RULEBOOK.md` remains the authority on rules status. The legacy RPG stays separate.

## 1. Global versus local city

| Design axis | City proposal #322 | Global proposal #338 |
|---|---|---|
| Primary board | 5–8 abstract local places | Selectable **worldwide multiplex network** of consequential institutions and organizations |
| Geography | Specific city + environs | Context tags/jurisdictions on nodes, optional schematic region board |
| Core fiction | Local factions cope with external paradigm shocks | Transnational factions influence, contest and sometimes precipitate global shocks |
| Agents | Party/movement leadership and local missions | Leader + councilors with missions across network nodes |
| Politics | Local constituency, municipal institutions | Local, national and global institutional arenas, abstract elections/coalitions |
| Simulation load | Place/support dynamics and global event deck | Cross-institutional network ties, discourse propagation and system responses |
| RPG | Local meetings and crises | Diplomatic meetings, assassinations, internal disputes, investigations, ontological encounters |
| Distinctive risk | Feels parochial if global shocks have no agency | Graph sprawl, opaque causal chains, excessive upkeep |

**Shared-core option:** Both scenarios could use typed people, factions, organizations, events, demands, network edges, missions and abstract jurisdictions. The scenario determines board granularity and available content. This is a **candidate architecture**, not a requirement to merge both versions into one game.

**Provisional recommendation for comparison:** Prototype Global as a **tiny network board** rather than expanding a detailed map; preserve City as an equally valid benchmark until actual playtests show which produces more meaningful decisions per turn.

## 2. Theory → simulation mapping (conceptual, not causal laws)

| Source | Question | State / representation | Actionable player-facing consequence | Pitfall |
|---|---|---|---|---|
| **Castells** network society | Who communicates with whom, and who bridges worlds? | Typed multiplex edges among persons, institutions, organizations, media and movements; bridge and reach annotations, not automatically computed scores | Reach a broker, establish an alliance, access an institutional pathway, lose a communication channel | Centrality ≠ political legitimacy, ideology or obedience |
| **Luhmann** functionally differentiated world society | How does the same disturbance acquire distinct meanings across systems? | Named **system perspectives** on a single event; actors/organizations participate in communication, not own function systems | Science tests a claim while economy prices an opportunity, media amplifies novelty, law disputes legality, politics makes decisions, religion interprets meaning | Treating 'science' as a capturable node or collapsing all systems into one stability meter |
| **Laclau** discourse/ideology | What demands, signifiers and antagonisms become politically linked and hegemonic? | Claims, floating/empty signifiers, equivalential relations, political frontiers, competing interpretations and observable alignments | A faction can lose an office but win interpretation; an alliance can fracture when its shared signifier changes | Conflating votes, ownership, support, institutional office and hegemonic influence |

**Coupling through one state:** an event → differentiated observations → circulation across network edges → competing articulations of demands → institutions/coalitions respond → newly changed conditions inform future events. Each arrow is a **design hypothesis** requiring rules and playtesting. Do not present it as a validated prediction of society.

Additional ontologies: **living / psychic / social systems** concern different kinds of processes; **Physical / Cyber / Astral** are fictional setting dimensions and interaction contexts. Do **not** equate the two schemes. NHI and PSI are speculative **in-world** phenomena.

### Data vocabulary (suggested types, no game logic)

| Entity | Identity / minimal descriptive fields | Persistent? | Physical-card treatment |
|---|---|---|---|
| Faction | id, name, ideology/claim refs, leader refs | Yes | Faction board/tableau |
| Person / Agent | id, faction affiliation, relationships, tags | Yes | Character card |
| Organization | id, sector, jurisdiction refs, relationship refs | Yes | Organization card |
| Jurisdiction | id, political-institutional context, locale | Yes | Board node/context tag |
| NetworkEdge | source/target IDs, kind, visibility/provenance | As needed | Drawn link / relation token / dedicated link card |
| FunctionSystemPerspective | system name, communication lens | Definition | **Rule/reference overlay, not ownable asset** |
| Articulation / Demand / Signifier | IDs, meanings, linked claims/actors | May evolve | Idea/discourse card or attached marker |
| Event | trigger, source, affected actors, interpretations | Episodic | Event card with readable outcome trail |
| Action / Mission | proposed actor, target, intent | Episodic | Action card or slot, outcome undecided |
| Evidence / Knowledge | provenance, reliability unknown/contested, discovered-by | As needed | Evidence card |
| Unit / Asset | owner, kind, deployment context | As needed | Card or token; no tactical combat |

Keep cards as **UI projections of typed data**, never force every model record into an identical card schema. A political system is not an organization. Edges are not necessarily cards. Unknown or secret information has a provenance/visibility status. Do not import a legacy RPG attribute or define resolution until approved.

## 3. Political-simulator inspiration matrix

These are **features to verify against the named games during hands-on evaluation**, not claims that all titles already implement each listed feature. Recording uncertainty is important, especially for smaller browser games.

| Reference | Hypothesis to examine | Possible design takeaway | MVP cost / warning |
|---|---|---|---|
| [Fantasy Parliament: Career](https://www.fantasyparliament.co.uk/career-lander) | Leadership pressure, party discipline, policy/cabinet crises, stakeholder responses | Leader in power ≠ party control; internal revolts as RPG events | Avoid UK-only constitutional assumptions |
| [Politics Simulator](https://politics-simulator.com/) | Campaign/party resource loop, short actions, political satire | Readable short turns, limited agent attention | Verify actual mechanics before copying |
| [Fantasy President Career](https://fantasypresidentcareer.com/) | Player career, dialogue, ideological news interpretations | Narrative policy reactions through distinct observers | Avoid implicit US-presidential world model |
| [The Political Process](https://store.steampowered.com/app/1184770/The_Political_Process/) | Electoral careers, committees, elections, legislative action | Make **politics between elections** consequential | District/candidate microdata would swamp Global |
| [Geo-Political Simulator 2026 Edition](https://store.steampowered.com/app/4021780/GeoPolitical_Simulator_2026_Edition/) | Cabinet, diplomacy, economic responses, opposition, security and war | Politics → global cross-system consequences | **Negative scope benchmark:** do not reproduce nation-by-nation spreadsheets |
| [Global Election Simulator](https://globalelectionsimulator.com/) | Differing electoral systems, vote/seat scenarios | Elections as scarce institutional transition moments | Do not require an exhaustive district map |
| [Poliwave](https://www.poliwave.com/) | Scenario comparison, polling, seat projections, uncertainty | Separate support, voting, seats and government control | Do not claim scientific prediction of real elections |
| [Democracy 4](https://www.positech.co.uk/democracy4/) | Policies, public constituencies, feedback | Explorable consequences across institutions | Avoid ubiquitous numeric policy sliders |

**Crucial distinct concepts:** popular opinion ≠ membership/resources ≠ seats ≠ government office ≠ institutional access ≠ discursive hegemony. Global needs selected mechanics for **normal politics** (campaigning, coalition/legislation, internal conflicts, policy framing) as well as espionage and potential abstract armed conflict. No assumption of a universal election schedule or universal governance institution.

## 4. Strategy, role-play and hacking references

| Game | Transferable pattern | Deliberate non-goal |
|---|---|---|
| [Sigma Theory](https://store.steampowered.com/app/716640/Sigma_Theory_Global_Cold_War/) | Small covert-agent roster with global consequences; crises, science, diplomacy | Full geopolitical simulation |
| [Shadow Government Simulator](https://store.steampowered.com/app/1281190/The_Shadow_Government_Simulator/) | Discoverable networks, paths of influence and visibility | Magical guaranteed obedience through graph ownership |
| [Terra Invicta](https://store.steampowered.com/app/1176470/Terra_Invicta/) | Faction-first organization with councilor missions and paradigm crisis | Waiting-heavy pacing and planetary micromanagement |
| [Crusader Kings III](https://store.steampowered.com/app/1158310/Crusader_Kings_III/) | Leader personality/relationships, succession, betrayal | Detailed dynastic simulation |
| [Stellaris](https://store.steampowered.com/app/281990/Stellaris/) | Divergent, epic grand-strategy outcomes | Galaxy-sized production scope |
| [XCOM](https://store.steampowered.com/app/200510/XCOM_Enemy_Unknown/) | Base/strategic tension, mission stakes, research, scarce personnel | **No tactical combat** |
| [Citizen Sleeper](https://store.steampowered.com/app/1578650/Citizen_Sleeper/) & [Citizen Sleeper 2](https://store.steampowered.com/app/2442460/Citizen_Sleeper_2_Starward_Vector/) | Human-scale dice/risk pressure and vulnerability; character event decisions | Standalone exploration RPG |
| [Disco Elysium](https://store.steampowered.com/app/632470/Disco_Elysium__The_Final_Cut/) | Political role-play, dialogue, tragicomedy | Fully scripted large narrative |
| [Dune: Imperium](https://store.steampowered.com/app/1689500/Dune_Imperium/) | Worker placement, conflicting demands on agents, faction/track influence, compact deck-building | Importing copyrighted cards/rules verbatim |
| [Cultist Simulator](https://store.steampowered.com/app/718670/Cultist_Simulator/) | Tableaux, card combinations, discovery, narrative fallout | Hundreds of constantly ticking, opaque chores |
| [Drop – System Breach](https://store.steampowered.com/app/1926510/DROP__System_Breach/) & [Midnight Protocol](https://store.steampowered.com/app/1162700/Midnight_Protocol/) | Legible network-hacking visual idiom | **Hacking mechanics stay undecided** |

**Hacking options to compare, not choose:** a graph traversal puzzle; agent mission card resolution; permissions/access overlays on the same Castellsian graph. The fiction must distinguish communication/influence edges from literal technical network topology. An institution's influence relationship is not an automatically hackable IP connection.

## 5. Card/tabletop design alternatives

**All-card interface hypothesis:** enduring people and organizations use persistent cards/tableaux; event/action/idea cards can form decks; units/resources may be attached tokens; network ties appear as lines, tags or relation cards. Luhmannian function systems are reference lenses or responses, *not ownable cards*.

### A. Pure physical tabletop
- Advantage: accessible tangible action economy, accountable rolls, no software dependency.
- Risk: each cross-system effect requires lookup and updating many counters; hidden information and agent behavior require a human GM or fixed instructions.
- Must pass: full illustrative turn without spreadsheet, external calculator or hidden centrality computation.

### B. Digital-first tabletop-style (candidate)
- Advantage: retains tactile metaphors, card tableau and visible dice while deriving network relationships, dealing events, preserving secrets and presenting causal logs automatically.
- Risk: attractive card UI could disguise inscrutable invisible math; requires inspectable outcome explanations and easy controls.

### C. Physical game with optional companion
- Advantage: tangible play with less repetitive bookkeeping; possible solo/GM-assisted variant.
- Risk: app maintenance, synchronization, unclear offline rules.
- Must specify what is **playable offline**.

**Decision pending playtest**, not settled by this document.

### Candidate card lifecycle
- **Persistent:** characters, organizations, locations, enduring claims, long-term knowledge.
- **Temporary:** events, actions, missions, conditions, revelations.
- **No guaranteed shuffle:** people, permanent institutions and personal relationships remain in the shared world unless events change them.
- **No guaranteed random 'history':** deck drawing represents scenario pressures, opportunities and uncertain events, not arbitrary teleportation of governments.

### Candidate board layout
1. **World network**: 8–12 *illustrative* major jurisdiction/context clusters linked by selected cross-border organizational nodes (not a geographic country map).
2. **Faction tableau**: leader + three agents *as a feasibility starting assumption only*, not an approved hard cap, associated organizations and assets.
3. **Contested discourse area**: a few issues/signifiers and competing interpretations.
4. **Social-systems response strip**: system lenses for politics, science, law, economy, media and religion as needed.
5. **Event / mission row**: a small number of current decisions, choices and consequences.

Any count above is a **proposed testing budget**, not the game's canon or specification.

## 6. One *hypothetical* tabletop turn: AGI disclosure crisis

This is a **worked walkthrough of information flow, not game rules or a simulation run**. The outcomes are deliberately illustrative; no thresholds, statistics, dice mechanic or scoring system are defined.

**Setup:** An AGI development organization's disclosure event card connects to a scientific institution, a media organization, a regulator and a finance actor across jurisdictions. Two or three unnamed ideological factions hold distinct AGI interpretations. A leader and several agents exist as enduring character cards.

1. **Reveal:** 'Contested AGI breakthrough' event enters the event row; attach a provenance/uncertainty token. It has not yet been confirmed scientifically.
2. **Observe through Luhmann:** The science lens asks about replicability, the economy lens about transactions, law about responsibility/rights, media about relevance, politics about collectively binding regulation. These are separate descriptive *interpretations*, not five automatic numerical modifiers.
3. **Circulate via Castells:** The broadcaster and corporate ties carry messages to different organizations. An intermediary broker connects science and political institutions. The network board shows the concrete paths used.
4. **Articulate via Laclau:** One faction uses 'human survival' as an organizing signifier, another 'freedom of innovation'; claims link to different demands and potential coalitions. Do not equate the most widespread message with legitimacy or votes automatically.
5. **Assign agents:** The leader handles a diplomatic/social meeting; one agent seeks evidence; another lobbies the regulator. Use character/mission placements or cards. **Resolution is blank pending author-defined rules.**
6. **Narrative event:** A meeting erupts into a leadership dispute or bizarre NHI-related accusation. The player faces an RPG choice; consequences are described qualitatively.
7. **Institutional response:** A regulator might announce a hearing, a party might split, or the scientist might challenge the claim. Update only relationships, publicly visible commitments, and known event state relevant to the chosen *hypothetical* branch.
8. **Explain:** End-of-turn record: source event → observing systems → which network paths carried claims → faction framings → mission choices → conditional institutional outcomes. **No invented random roll or numerical bonus.**

### Illustrative upkeep audit (estimate, *not measured*)
| Component | Pure tabletop manual operations | Digital-first manual operations |
|---|---:|---:|
| Event reveal and placement | 1–2 | 1 |
| System-response reference lookups | 3–6 | 0 (displayed automatically) |
| Network path inspection | 2–5 | 1–2 |
| Agent assignments | 3–4 | 3–4 |
| Discourse/claim updates | 2–5 | 1–2 |
| Relationship/status counters | 3–8 | 0–2 |
| Logging/end-of-turn upkeep | 3–7 | 0–1 |
| **Illustrative total** | **17–34** | **6–12** |

These totals are **hypothetical estimates** for comparing procedures, not observations of tested play. Count actual touches, reference lookups, decisions, rolls and time with two human dry-runs; target no more than a handful of manual upkeep steps not directly related to interesting choices. If tables demand constant bookkeeping, eliminate trackers, combine abstractions or accept digital-only derived simulation. **Avoid a spreadsheet full of per-country × per-system statistics.**

## 7. Proposed data and UI architecture (no new mechanics)

Potential scope within `strategy_game/`: reuse the existing typed world/network/leader/political vocabulary; add **only author-approved** Global-specific view models and scenario configurations when ready. The UI can present card projections from typed entities, a world network view, an event log with provenance and character dialogue panels. A local scenario can remain a different configuration. Do not create a second runtime now.

Proposed interface-only data contracts:
- `CardView`: entity ID, display kind, title, description, icon/visibility state, links to underlying typed record.
- `GraphView`: node IDs, edge IDs, edge kind, optional jurisdiction/context, source/visibility.
- `ObservationView`: event ID, system lens, attributed observation, provenance.
- `DiscourseView`: signifier/demand IDs, articulating actors and competing interpretations.
- `TurnTraceView`: ordered *reported* state changes and their sources. No scoring/rules implied.

These are **examples for author review** and intentionally not executable API specifications.

## 8. Decision record & design gates

**Already specified:** faction-first gameplay, playable leader and delegated agents; global network abstraction; three theory inspirations; short consequential sessions; potential diplomacy/politics/espionage/warfare; role-play events; no tactical combat; hacking method open; indie/open-source/standalone crossover distinct from legacy.

**Still requires explicit author approval before implementation:**
- Turn cadence, initiative/actions and victory conditions
- Actual dice and skill checks (do **not** import legacy stats)
- Number/type of faction resources, governance and representation formulas
- How an edge modifies anything, how discourse changes, and how a system responds
- Card deck composition, card draw rules, card effects and mission outcomes
- Whether the design is fully tabletop-complete, digitally assisted or hybrid
- Combat, cyber and PSI resolution, tech/research and NHI mechanics
- Which jurisdiction/organization/faction rosters enter default scenarios

### Playtest tasks for #338
- [x] Capture side-by-side Global vs city tradeoffs (design comparison only)
- [x] Map Castells/Luhmann/Laclau to distinct tentative data and decision roles
- [x] Document one **hypothetical** cross-system crisis turn with RPG/agent/discourse components
- [x] Collect political, strategy, RPG and hacking inspiration matrix with scope cautions
- [x] Draft card taxonomy and compare physical/digital/hybrid options
- [x] Estimate bookkeeping operations with assumptions declared
- [ ] Author reviews and approves actual rules
- [ ] Prototype tiny deterministic headless Global loop **after** approval
- [ ] Verify real tabletop upkeep using recorded human playtest sessions
- [ ] Compare fun/legibility with #322 using identical evaluation criteria

**Recommendation to test, not a decision:** Start with digital-first network-board + card/tableau visualization while keeping actions and game-state entities tabletop-legible. The computer can maintain derived network/society state, but players must always see a causal explanation.

**Non-goals:** no imported LaclauGPT research stack, no full geopolitical economic database, no detailed territorial map, no tactical X-COM missions, no mandatory LLM, no automatic conversion of speculative NHI/PSI fiction into empirical claims, no unauthorized rewriting of the old game or the local-city MVP.
