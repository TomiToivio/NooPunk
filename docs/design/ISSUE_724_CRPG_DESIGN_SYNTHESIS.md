# Issue #724: Computer RPG design synthesis

**Status:** Design recommendation, not approved mechanics or a runtime implementation.  
**Scope:** NoöPunk computer RPG and its tabletop-first source, **not** the independent `strategy_game/` crossover.  
**Authority:** Follow `AGENTS.md`'s 2026-10-26 override and `rulebook/WITHOUT_NUMBER_BASELINE.md`. CWN is primary; SWN supplies psionics and other compatible extensions. Existing Godot code is preserved until a separately approved port.

## Design position

**Tactical depth from Shadowrun: Dragonfall; investigation, psychology and political dialogue from Disco Elysium; consequential action budgets and visible pressures from Citizen Sleeper.** These are *experiential references*, not three rules engines to splice together.

The aim is a rules-literate investigative CRPG: preparation, equipment, teamwork and spatial position matter when tactics are warranted, but most encounters can also progress through discovery, social action, negotiation or retreat. No scene should become a combat arena merely because an engine can render one.

## The gameplay loop

1. **Receive a case:** an institutional briefing, affected people and an unresolved question. Record evidence provenance and alternative interpretations, not an automatically true conspiracy.
2. **Investigate:** visit locations, inspect records and talk to witnesses. Core leads remain discoverable through appropriate fictional access; checks determine speed, expense, exposure, additional detail or complications.
3. **Interpret and choose:** competing social, ideological and psychological frames influence contacts and institutional reactions. Avoid forcing a single correct interpretation of ambiguous NHI/PSI events.
4. **Prepare and intervene:** allocate resources, choose allies and a method: interview, infiltration, diplomacy, technical analysis or tactical operation.
5. **Resolve consequences:** update one case ledger containing clues, NPC relationships, time pressure and outcome flags; show what changed and why. Feed results into the next briefing.

Tactical scenes are **conditional**, not mandatory. A failed combat can lead to escape, capture, injury or loss of trust rather than a universal mission restart. Preserve the consequences of avoiding combat as deliberately as those of winning it.

## Mechanics-to-inspiration decision matrix

**Categories:** ADOPT = design pattern to prioritize; ADAPT = translate into the existing rules; INVESTIGATE = prototype/review separately; AVOID = reject as direct import. These are *proposals*, not licensing claims.

| Source | Decision | Proposed use | Tabletop / digital | First slice or later | Type |
| --- | --- | --- | --- | --- | --- |
| CWN | **ADOPT** | Primary attributes, skills, checks, progression, equipment and tactical resolution as defined by the current Without Number baseline; no replacement dice engine | Same source procedure / Godot representation | First | Core |
| SWN | **ADAPT** | Approved PSI and compatible science-fiction options via tabletop rules, not invented Godot-only mechanics | Shared rules / UI reveals options | First only where needed | Core |
| Shadowrun: Dragonfall | **ADOPT** | Mission briefing, companion roles, spatial cover, positioning, tactical approaches, dialogue-linked outcomes; not its proprietary rules | Mission procedure / tactical scene & party UI | First: optional small encounter | Play structure |
| Disco Elysium | **ADAPT** | Inspectable conversation checks, conflicting perspectives, thought-provoking ideological choices; psychological voices remain characterization, not new stats | Roleplay prompts / reactive dialogue and journal | First: one consequential dialogue | Narrative presentation |
| Citizen Sleeper | **ADAPT** | Limited choices under visible time pressure; one readable case clock rather than an economy of overlapping gauges | GM clock / journal pressure indicator | First: one clock | Interface + procedure |
| GUMSHOE | **ADAPT** | A reachable core clue is not gated behind a random success; roll for risky follow-up, costs, hidden detail or consequences, using baseline checks | GM clue principle / evidence journal | First | Investigation procedure |
| Fate | **INVESTIGATE** | Situational descriptors and character-complication prompts without importing 4dF, Fate points or a second resolution engine | GM framing / contextual dialogue prompts | Later | Narrative technique |
| PbtA | **INVESTIGATE** | Fictional triggers and meaningful complications on failure without importing playbooks or a 2d6 move engine | GM advice / result messaging | Later | Narrative technique |
| Eclipse Phase / Transhumanity's Fate | **INVESTIGATE** | Transhuman and philosophical texture; assess separately for compatibility and license | Lore comparison / characterization | Later | Reference |
| Parallel dice engines, combat-only quests, encyclopedic skill proliferation | **AVOID** | No double-resolution rules, artificial combat bottlenecks, or duplicate character sheets | Both | Always | Guardrail |

The previous `docs/design/ISSUE_516_REFERENCE_MATRIX.md` concerns a **different, earlier crossover-context decision process**. Its Fate-centric implementation descriptions do not displace the current RPG Without Number baseline.

## Explicit answers to design questions

- **When tactics?** Only when positioning, equipment, exposure, teamwork or environmental constraints make distinct tactical choices meaningful. Otherwise resolve through ordinary investigation or social procedures.
- **What stays visible?** Character abilities, equipment permissions, known risks, clue provenance, companions' involvement and clocks. Hide neither the existence of meaningful rules nor essential evidence behind UI flourish.
- **How are clues handled?** Each scene defines at least one obtainable lead and at least one independent route forward. Successful checks may grant interpretation or leverage; failed checks still permit continuation with consequences.
- **Ideology?** Different factions can describe the same evidence differently; player choices alter relationships and access. No hidden universal morality meter or automatic endorsement of a theory.
- **PSI, cybernetics and NHI?** Apply current approved tabletop mechanics only. Ambiguous phenomena may be presented as competing witness accounts; never fabricate a new powers system via the CRPG specification.
- **Shared model?** One serializable case state holds evidence IDs, sources, trust/reputation changes, clock status, resources and outcome flags. Godot presents state rather than defining a conflicting tabletop rule.
- **Narrativist overlay?** Small, contextual and removable. Use it to enrich interpretation and consequence, never to dissolve builds, probability or tactical planning.

## Proposed vertical slice: the disputed hospital case

**Illustrative pitch, not canonical scenario content:** An investigative team is sent to a contemporary hospital after contradictory testimony about an unusual event. A clinician calls it a clinical incident, an activist calls it institutional mistreatment and a witness suspects an anomalous cause.

1. **Briefing and evidence:** case journal shows three statements with distinct provenance; an intake record is an always-reachable core clue.
2. **Dialogue:** interview the clinician and a witness. A baseline skill check can win additional disclosure, but cannot erase the essential case lead. Offer an ideological/ethical choice about whether to report, protect or publicly challenge the institution.
3. **Clock:** one visible external pressure, such as scheduled transfer of a witness. Investigative detours advance it according to a tabletop-reviewed procedure; no numbers are declared by this memo.
4. **Optional tactical branch:** a restricted records area can be approached through authorization, negotiation or risky physical entry. Only if confrontation arises, present a small turn-based tactical scene that uses the same character sheet and baseline rules.
5. **Consequence ledger:** record discovered facts, unresolved interpretations, NPC relations, clock outcome and the chosen intervention. Show an epilogue with at least two meaningfully distinct outcomes.

### Acceptance criteria for a later implementation issue

- Player can complete the case **without** tactical combat, with no dead-end caused by a failed clue roll.
- Tactical branch is optional but mechanically meaningful; builds and positioning can change its outcome.
- At least one dialogue choice changes an NPC relationship or institutional access.
- One clock communicates pressure and affects events; it does not silently invalidate the primary lead.
- Save/reload restores one coherent state and the case journal does not present speculative interpretation as confirmed evidence.
- A documented mapping shows every roll and character field derives from the current tabletop baseline.
- Evaluate executable behavior with tests **only when code is actually implemented**. This memo adds no prose/CI tests.

## Follow-up decision gates

1. Approve/adjust the loop and matrix through editorial review and a tabletop micro-playtest.
2. Write the hospital-case procedure with existing approved tabletop stats and checks; resolve any undefined detail there first.
3. Convert the approved procedure to an engine-independent case-state specification.
4. Open a **separate implementation issue** for Godot scene, UI and executable tests. This research issue does not authorize or claim a functioning vertical slice.

References: [#724](https://github.com/TomiToivio/NooPunk/issues/724), [#704](https://github.com/TomiToivio/NooPunk/issues/704), `AGENTS.md`, `rulebook/WITHOUT_NUMBER_BASELINE.md`, `docs/design/ISSUE_516_REFERENCE_MATRIX.md`, `docs/design/VISION.md`.
