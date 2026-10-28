# Issue #728: Computer-game influence research and unified-interface design

**Status:** Research/design proposal, not approved new mechanics or implementation.  
**Scope:** The legacy NoöPunk tabletop RPG and its Godot CRPG presentation, **not** the independent `strategy_game/` crossover.  
**Rule authority:** [Without Number baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md): CWN for characters, standard STR/DEX/CON/INT/WIS/CHA, 2d6 checks, d20 attacks/saves, action economy, gear, hacking; SWN for approved PSI. Follow [AGENTS.md](../../AGENTS.md).  
**Related:** [#724 design synthesis](ISSUE_724_CRPG_DESIGN_SYNTHESIS.md), [#704 GUMSHOE investigation](ISSUE_704_GUMSHOE_INVESTIGATION.md), [#704 decision register](ISSUE_704_DECISION_REGISTER.md). This memo *extends* those proposals and does not override them.

## Research method and limits

This is a **desk review of publicly described gameplay, reference-game identity and proposed design applications**, not a claim of fresh hands-on playtesting, exhaustive feature verification, license clearance or a working Godot prototype. Linked game pages are reference starting points. Decisions below are recommendations for tabletop playtesting; a designer should verify detailed gameplay, difficulty and UX in the actual games before committing to imitation.

**Principle: one rule adjudication, multiple views.** A player selecting a node in a network diagram and a player pointing to that node on a tabletop sketch state the same intention, satisfy the same access prerequisites, take the same game action, make the same check (if required), and get the same consequences. A UI may reduce friction but may not supply game-only privileges.

## Influence matrix

**ADOPT:** use as a target experience or presentation principle. **ADAPT:** translate to existing CWN/SWN procedures. **INVESTIGATE:** benchmark/playtest before taking a decision. **AVOID:** explicitly not in the NoöPunk design. All examples below are **original proposed translations**, not descriptions of licensed mechanics or imports of third-party rules.

| Game / reference | Focus | Decision and boundary | Tabletop equivalent | Godot view | Phase / risk |
| --- | --- | --- | --- | --- | --- |
| [Shadowrun: Dragonfall](https://store.steampowered.com/app/300550/Shadowrun_Dragonfall_Directors_Cut/) | Mission briefing, party roles, turn-based position and dialogue | **ADOPT** ensemble tactical+investigative structure; **AVOID** importing Shadowrun's rules | CWN briefing, preparations, action sequence, movement and combat | Party roster, tactical grid, briefings | First slice; UI complexity, licensed world/rules |
| [Disco Elysium](https://store.steampowered.com/app/632470/Disco_Elysium_The_Final_Cut/) | Ideological dialogues, investigator interiority, consequence-rich decisions | **ADAPT** conversation framing and mutually conflicting testimony; **AVOID** new psyche stats or involuntary internal-voice checks | CWN Talk/Connect/Know checks, GM dialogue options, faction consequence log | Dialogue, journal with speaker/source, reactive choices | First slice; writing scope |
| [Citizen Sleeper](https://store.steampowered.com/app/1578650/Citizen_Sleeper/) | Limited time, relationships, visible pressure | **ADAPT** a scenario deadline using explicit GM events; **AVOID** a second dice economy | Scheduled event and resource ledger | Calendar/clock in journal | First slice; over-gamified meters |
| [DROP: System Breach](https://store.steampowered.com/app/1902300/DROP_System_Breach/) | Readable node/network cyber-intrusion aesthetic | **ADAPT** legible host graph; **AVOID** twitch/real-time hacking as a gate | Diagram of reachable devices and guarded edges | Graph UI, access highlights and log | First slice; mapping actual CWN programs |
| [Midnight Protocol](https://store.steampowered.com/app/1162700/Midnight_Protocol/) | Deliberate, command-oriented network interactions | **INVESTIGATE** concise commands as *input aliases*, not new mechanics | Player names a CWN hacking action, GM adjudicates | Select node + command/action menu | First/later; usability and rule drift |
| [Blade Runner: Enhanced Edition](https://store.steampowered.com/app/1678420/Blade_Runner_Enhanced_Edition/) | Detective atmosphere, interviews and competing leads | **ADOPT** multi-lead case structure; **AVOID** pixel hunts for required clues | GM scenes, evidence cards, interview notes | Witness dialogues, source-labelled case board | First slice; pre-scripted branching explosion |
| [Observer: System Redux](https://store.steampowered.com/app/1386900/Observer_System_Redux/) | Subjective/psychological cyberpunk horror | **ADAPT** unreliable perspective as *presentation*, not infallible psi | Describe perceptions and distinguish claims from corroboration | Distorted visuals with accessible plain-text testimony | Later; accessibility and sensitive mental-health depiction |
| [Song of Farca](https://store.steampowered.com/app/1435670/Song_of_Farca/) | Remote investigations and linking surveillance leads | **ADAPT** desk investigation and evidence provenance | Records, interview transcripts, network diagram | Multi-panel case board and remote-records view | First slice; avoid magical all-access surveillance |
| [Cyberpunk 2077](https://store.steampowered.com/app/1091500/Cyberpunk_2077/) | Social density, factional city storytelling | **INVESTIGATE** environmental/world cues; **AVOID** FPS/action pacing and AAA scope | Location briefs and NPC/faction reactions | Small dense block, dialogue hotspots | Later; unsustainable production scope |
| [Deadeye Deepfake Simulacrum](https://store.steampowered.com/app/1545990/Deadeye_Deepfake_Simulacrum/) | Low-budget cyberpunk visual punch and readable interface | **ADAPT** density and stylization; **AVOID** reflex combat as core | Distinct tokens/maps and equipment cards | Economical silhouettes, UI-first spaces | First slice; legibility at target resolution |
| [Cloudpunk](https://store.steampowered.com/app/746850/Cloudpunk/) | Voxel city silhouettes, neon atmosphere and scale illusion | **ADOPT** mood and modular environmental language; **AVOID** requiring open-world driving | Scene/location descriptions and district maps | Modular voxel-ish street/ward interior | First/later; navigation/asset costs |

## Shared domain/state contract (design proposal)

The **tabletop referee sheet** is the reference, not a separate rules translation. The eventual digital save should represent the same fields, without freezing new mechanical numbers:

- **Characters:** canonical CWN sheet (attributes, skill ranks, edges/foci, equipment and resources); specialist SWN PSI only when legitimately acquired.
- **Case facts:** stable evidence ID; observable claim/content; type (observation/testimony/inference); who/what produced it; location, timestamp, provenance and access prerequisite; whether a *core* lead or optional detail; citations to related items. The journal must distinguish player conclusions from established observations.
- **Access graph:** nodes are devices/records/people/rooms; edges are actual physical, wireless, credentialed or social routes; access state, current permissions and security descriptions. An edge never grants access because the UI draws it.
- **Pressure:** GM-authored scheduled events/deadlines, time spent on actions, named consequences. Do **not** invent a Citizen Sleeper dice pool or another currency.
- **Relations:** explicit NPC/institution attitudes, contacts, permissions and consequences in scenario notes; avoid unapproved numerical ideology meters.
- **Encounter:** existing CWN round/action/initiative, location, cover, equipment, damage and conditions; no parallel adventure-combat kernel.
- **Trace:** intention, prerequisite, governing source procedure, roll/result when applicable, state change and presented explanation, to support referee replay and Godot debugging.

Suggested interface boundary: `propose_action(state, actor, target, intent)` → list prerequisites and applicable *existing* CWN options; `resolve_with_authoritative_rules(...)` → event/result → `render_tabletop(...)` or `render_godot(...)`. These are conceptual contracts, **not approved APIs**, and no new resolution formulas are specified. Random outcomes, time costs, range, decks/programs and cyber-security capabilities must be taken from actual CWN rules rather than guessed here.

### One-to-one UI mapping

| Action intention | Tabletop procedure | Computer presentation | Must stay identical |
| --- | --- | --- | --- |
| Get an intake log | State relevant method and permission; core clue on accessible competent inspection | Inspect record → provenance card | Access, fact and follow-up leads |
| Persuade a technician to cooperate under risk | CWN Talk or context-appropriate skill check with declared stakes | Dialogue choice shows intent and relevant check | Difficulty, modifiers, possible cost/consequence |
| Examine a host | Determine physical/link reachability and permissions before CWN hacking | Highlight only actually reachable nodes | No magical remote access |
| Execute a cyber action | Choose a source-defined CWN program/action and meet its restrictions and costs | Command list + log, no timed button minigame | Same costs, checks, alarms and state |
| Investigate a suspicious discrepancy | Notice/Know/Program as appropriate; core observations not roll-gated | Case board links the facts, hypotheses separately | Observation versus speculation |
| Respond to a deadline | GM-announced scheduled pressure plus real action consequences | Visible timeline/clock | No hidden turn tax |
| Confront guards or de-escalate | CWN checks or combat actions where scene calls for them | Dialogue or tactical mode | Same stats, initiative and outcomes |

## Graph hacking: worked paper/digital parity example

**Illustrative graph, not canon and not a substitute for CWN's program and security text:**

```text
[Investigator's deck] --(local, reachable)--> [Ward terminal]
                                           |
                                     (requires access)
                                           v
                                     [Audit host] --(protected link)--> [Backup archive]
```

1. The team first obtains legitimate access to the ward terminal, or establishes another **fictionally and mechanically valid route**. On paper the GM draws the devices and marks reachable links; in Godot reachable links illuminate. A glowing node is information, not access.
2. The player requests access to the audit host. The GM/engine checks the applicable CWN hacking permissions, tool/program/deck limits, timing and opposing security. A task roll occurs **only where the source procedure calls for one**. Do not assume every edge is a generic `Program` test.
3. The host contains an **audit discrepancy** (core observation) if a valid examination route succeeds. Failure of one risky intrusion can cause source-defined alarms, resource loss, exposure or denial; it must leave a separately authored lead via the technician interview or a lawful records request. Do not grant the protected clue for free through a locked system.
4. On paper, write `audit_host: access [as established by rules]` and `E-04: event timestamp differs from maintenance log; provenance: audit export`. In Godot, the identical evidence item populates the journal and the action log records the same adjudication.
5. A link to the backup archive is a **new permission challenge**, not a free traversal. No bespoke timer, stealth meter, graph-puzzle key or hacking minigame decides success.

**Playtest checkpoint:** a paper referee and Godot facilitator take an identical starting sheet, deck, access state, chosen actions and roll sequence; their resulting evidence, costs, alarms, and access states must agree. Until current CWN cyber procedures and approved equipment are mapped, treat the above as a **workflow sketch**, not numeric rules.

## Investigation: scene graph and non-dead-end clues

Example case: *a disputed incident at a hospital*. This is a **noncanonical scenario outline**, deliberately grounded; psychiatric treatment is not evidence that a witness is inherently unreliable, nor is any alleged anomaly proven paranormal.

```text
Briefing
  ├─ Ward witness interview ──────────┐
  ├─ Accessible intake register ──────┼─ Timestamp discrepancy ──┬─ Technical review
  └─ Clinician interview ─────────────┘                          └─ Audit-host inquiry
                                                                  │
                                              Technician interview / lawful archive request
                                                                  │
                                         Report choice / referral / optional tactical intervention
```

- **Core evidence E-01:** intake register shows the original report time, once a competent investigator obtains access through normal institutional procedures. A good Notice/Know result can supply *extra* contextual detail, not determine whether the register exists.
- **Core evidence E-02:** a ward witness reports a conflicting time. It is **testimony**, not proof of cause. A Talk check under pressure can affect cooperation, consent to publicity or trust, not erase the witness's basic account where they are willing to speak.
- **Core evidence E-03:** clinician provides an independently sourced timeline. Different accounts may remain inconsistent.
- **Optional evidence E-04:** authenticated audit export shows a maintenance change. Access to restricted systems follows CWN hacking or legitimate authorization. At least one additional way to continue exists even if intrusion fails.
- **Interpretation:** investigator may conclude error, misconduct, technical sabotage or unresolved anomaly, but no UI silently declares the hypothesis true.
- **Access and privacy:** protected patient records require actual legal/ethical permission or risky consequences. Neither the tabletop GM nor Godot should reward needless disclosure of sensitive medical data.

**Shared procedure:** investigate intentions → establish credible physical/social/digital access → expose reachable core *observations* without arbitrary clue rolls → use CWN checks for uncertain consequential steps → update case/evidence ledger → offer two independent routes forward → let player interpret and intervene. This aligns with #704, and does not add a second GUMSHOE point economy.

## Integrated vertical slice, in six scenes

| Scene | Player decision | Shared rules & journal effect | Godot-only presentation |
| --- | --- | --- | --- |
| 1. Case briefing | Accept mandate and pick an approach | Record mandate, known witnesses, constraints and sources | Case overview and compact city/hospital view |
| 2. Social inquiry | Interview nurse/clinician; negotiate cooperation | CWN Talk/Connect or no roll for routine access; update testimony, relationships | Dialogue and tagged statements |
| 3. Evidence analysis | Compare timestamps and hypotheses | Notice/Know as appropriate for optional depth; all reachable core observations preserved | Source-labelled evidence board |
| 4. Network access | Choose lawful terminal access, technician help or risky intrusion | Actual CWN reachability, programs, security, resources and consequences | DROP/Midnight Protocol-inspired graph view |
| 5. Ideological/ethical choice | Respect privacy, escalate to oversight, or publish limited findings | Record chosen disclosure, changed access and named institutional reactions; no invented ideology meter | Dialogue alternatives and consequence preview |
| 6. Optional confrontation | Negotiate, withdraw, infiltrate or fight | CWN Talk/Sneak or existing combat rounds, position, injury and gear; no forced combat | Shadowrun-inspired turn-based tactical room |

The case ends with a **source-aware report**, open questions and different relationships/permissions depending on chosen actions, even if no combat occurs. A sample tabletop session should be run **before** any Godot port; existing legacy Godot systems are not claimed to implement this proposed flow.

## Visual and UX direction (small-team Godot)

Use **Cloudpunk** as an atmospheric benchmark, not a commitment to a streaming voxel metropolis. Target **one small street block, two hospital rooms, an evidence-board screen and one network graph**, with modular interiors, subdued near-contemporary props, selectively lit signage, readable silhouettes and strategic lighting. Use **Deadeye Deepfake Simulacrum** as a reference for strong indie identity, not twitch combat. Treat **Cyberpunk 2077** as a world-density and incidental-quest inspiration, not a fidelity target.

Keep UI legible at desktop and smaller screens: a clear focus state, keyboard interaction for nodes/commands, color-independent access indicators, text alternatives for sensory distortion and reduced-animation options. Detective evidence needs provenance and contradiction markers, not just glowing conspiracy strings. A network link should have a tooltip stating whether it means *known*, *reachable*, *authorized* or *blocked*.

Do not spend initial scope on open-world traversal, vehicle driving, fully voiced branching dialogue, real-time intrusion, mass NPC simulation, combat VFX or speculative psychic-vision minigames.

## Rules gaps, to be decided **before** any code

| Question | Current safe stance | Decision gate |
| --- | --- | --- |
| Are core clues a permanent NoöPunk rule? | #704 proposed referee principle, *not* imported point economy | Tabletop case playtest + author editorial approval |
| How exactly are computer network nodes represented? | Use actual CWN device reachability, hacking actions, permissions and security | Audit against CWN chapter with concrete program and deck example |
| How much elapsed time does each investigation action cost? | Use source and scenario authored timing; no new universal mechanic | Tabletop session and GM schedule |
| How are relationships/ideological consequences tracked? | Descriptive notes and access consequences, no new numerical meter | Author decision if quantitative mechanics become necessary |
| How does Godot share rules rather than approximate them? | Keep source-accurate adapter boundary and event log proposal | Separate implementation issue with code behavior tests |
| How can PSI perception be presented? | Use only properly acquired SWN techniques, and distinguish testimony | Author-approved scenario and source restrictions |

## Verification and acceptance

- [x] Reference matrix covers every game in #728 with use, tabletop equivalent, Godot view and scope/risk.
- [x] Architecture proposal separates canonical rules and case state from presentation.
- [x] Paper/digital graph-hacking parity example and CWN-first restrictions.
- [x] Investigation graph includes independent continuation routes, evidence provenance and meaningful uncertainty.
- [x] Integrated six-scene vertical slice uses shared rules throughout and keeps combat optional.
- [x] Feasible small-team visual direction and named open decisions.
- [x] No new rules, source text, runtime minigames or doc-only CI tests introduced.
- [ ] Hands-on comparison/playtesting of all commercial references: **not performed**.
- [ ] Tabletop case playtest and precise CWN hacking chapter audit: **not performed**.
- [ ] Godot prototype and parity tests: **not implemented** (requires separate authorization/issue).

### Reference links and further reading

The eleven game links appear in the matrix. Existing related research: [CRPG synthesis #724](ISSUE_724_CRPG_DESIGN_SYNTHESIS.md), [GUMSHOE #704](ISSUE_704_GUMSHOE_INVESTIGATION.md), [CWN baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md), and [Godot guidance](../GODOT.md). Original game UI, art, dialogue, code and settings remain their respective rights holders' property; this document specifies independently authored abstractions and examples, not license grants.

## Appendix — verified rule bindings (added from the parallel draft)

Two things the body above describes in prose are worth pinning to code, because a UI that drifts from
these is drifting from the rules.

**Graph hacking is a picture of state `src/rules/cwn_hacking.py` already owns.** Verified against the
module on 2026-10-29:

- `access_pool(*, intelligence_modifier, program_skill, deck_bonus)` — the pool is `INT modifier + Program
  + deck Bonus Access`, never negative, refreshed by an hour of reprogramming once a day (the caller owns
  the clock);
- `security_difficulty(...)` sets the target; `hacking_check(..., wireless=, vr_crown=)` applies flat
  penalties `WIRELESS_PENALTY = -2` and `VR_CROWN_PENALTY = -1`;
- `AlertClock` — `FAILURES_PER_ALERT = 2` failed checks raise one alert action, `ALERT_ACTIONS_TO_ALERT = 2`
  alert actions raise the network alert.

So a node diagram may show nodes, edges, security values and daemon flags; it may not invent a roll, a
timing bar or an action the module lacks. What it may add is legibility: hover reveals the check's inputs,
the clock animates as two boxes, the log shows each roll.

**Which ideas are views and which are rules.** This is the classification that decides what may be
prototyped now:

| idea | source | needs a new rule? |
|---|---|---|
| braindance reconstruction | Cyberpunk 2077 | **no** — a `Forensics` check producing a fact through the existing clue layer |
| clue-linker / KIA-style board | Blade Runner | **no** — a view over `src/rules/investigation.py` state |
| node-graph intrusion | DROP / Midnight Protocol | **no** — a view over `cwn_hacking.py` |
| real-time pressure | Blade Runner / Song of Farca | **no** — clocks already exist; real time is an affordance |
| psychological "voices" | Disco Elysium | **no** — the referee or UI voices the relevant skill; the check is unchanged |
| **Thought Cabinet / internalising ideas** | Disco Elysium | **yes** — a second progression track, and it would collide with #698 conditions |
| **dice-as-actions per cycle** | Citizen Sleeper | **yes** — a second action economy beside CWN turns; rejected as a second engine |
| ideology standing | Disco Elysium → #719 | **yes, already proposed** — Articulation / Legitimacy / Frontier must be accepted before any UI |

**Evidence labels used in §Research method.** OBSERVED = a documented feature of the shipped game;
PROPOSED = NoöPunk's adaptation; AVOID = would break the one-engine rule or the licence. No listed title
was played for this issue, so any claim about how a game *feels* is PROPOSED. The value is the mapping,
not a review score.
