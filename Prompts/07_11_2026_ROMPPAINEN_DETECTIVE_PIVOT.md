# Prompt: NoöPunk becomes Etsivä Romppainen detective interactive fiction

- **Date:** 2026-11-07
- **Topic:** issue #1310
- **Source:** Tomi's own issue text in NooPunk, <https://github.com/TomiToivio/NooPunk/issues/1310>
- **Archive status:** original author prompt, retained verbatim for future reuse. It **is** a current author decision for
  the pivot it describes, but the archive itself grants no further scope and promotes no abandoned idea to canon.

## Original prompt (verbatim issue text, transport formatting normalised)

# Decision: NoöPunk becomes detective interactive fiction, NOT a full RPG

**New author direction (2026-11-07):** NoöPunk's primary playable experience is an **old-fashioned adventure / interactive-fiction detective investigation** featuring **Etsivä Harri Romppainen** in cyberpunk Helsinki. **Stop pursuing a complete tabletop/computer RPG.** The previous full-RPG ambitions were causing cognitive overload and unbounded scope growth because the setting spans multiple genres and ontological shocks. Prioritize **writing and a playable investigation** over universal mechanics.

> **Hard scope guard: do not touch `NooPunk-RPG/` for the time being.** Do not edit, move, rename, delete, refactor, migrate or "tidy" any RPG files. Do not revive CWN character generation, combat, psionics, complete equipment/economy systems, stat blocks, leveling or universal RPG rules. Preserve the RPG as an inactive historical/optional project; do not delete it. This supersedes the prior expectation of eventual full RPG integration in #1295/#1286/#1308/#1309 wherever that expectation conflicts with this pivot.

## Revised roles of the projects

| Directory / track | New purpose | Authorship and scope |
| --- | --- | --- |
| **`NooPunk-Simulator/`** | The **playable cyberpunk detective interactive-fiction adventure** about Romppainen investigating political extremists radicalized by paradigm shifts and ontological shocks. A small optional world/faction simulation may support cases without being the game itself. | Adapt and reuse existing social/ideology/physical Graph + Tag work *selectively*, not a full LaclauGPT pipeline. **`NooPunk-Simulator/Paper/` remains Tomi-only, agent READ ONLY**. |
| **`NooPunk-Story/`** | The **interactive-fiction script**: scenes, dialogue, clues, choices, branching outcomes and case arcs. May later become a conventional full-length science-fiction book. | **`NooPunk-Story/Story/` remains Tomi-authored and agent READ ONLY**. Agents may develop graph/index/adapters from actual author-written text; do not fabricate manuscript prose in Tomi's directory. |
| **`NooPunk-RPG/`** | **Paused, untouched** full-RPG archive. | **Absolutely no agent modification unless Tomi explicitly reactivates it.** Do not require CWN compatibility to build the adventure. |

This is a product-focus pivot, **not authorization to destructively restructure** existing repos or silently rewrite current Story/Simulator papers, existing theory, or canon.

## Creative and gameplay premise

**Etsivä Romppainen**, a detective investigating **political extremist movements radicalized by three mainstream paradigm shifts and ontological shocks**:

1. **AGI/ASI and human augmentation:** accelerationism, existential-risk movements, cyberpunk technology and competing political responses.
2. **Consciousness, PSI and panpsychism:** extraordinary consciousness claims, psychic phenomena, interpretations and radicalization.
3. **UFO/UAP/NHI:** disclosure, alien-contact narratives and human intermediaries/proxy organizations.

**Viewpoint:** begin as grounded **Helsinki cyberpunk noir / police investigation**, not encyclopedic global/interstellar exposition. Encounter extreme ideologies, crimes, propaganda, witnesses, ambiguous anomalies and conspiracies primarily through *human actors*. Reveal worldbuilding through investigation, not long lore dumps. Romppainen may investigate without needing to decide which cosmic explanation is true. Preserve social/political ambiguity and multiple hypotheses.

## First game = a small, playable detective adventure

**Primary gameplay loop:**
1. Receive a case / briefing and review a limited set of leads.
2. Explore a few accessible Helsinki locations, interview people and inspect relevant objects/documents.
3. Investigate records, messages, social/organizational relationships and competing ideological narratives.
4. Record **clues, testimony, hypotheses, contradictions and leads** in an interactive case notebook / Investigation Graph.
5. Choose where to go next and how to act; choices change trust, evidence access, exposure, faction responses and story state.
6. Reach a case outcome grounded in what was established, with room for uncertainty and consequences.

**Minimal engine only:** a Story/Scene Graph, an Investigation/Clue Graph, simple character/social tags, locations and case state, small dialogue/choice interaction, save/load and an inspectable state/history. Prefer conventional interactive-fiction conventions and GUMSHOE-like clue accessibility (important case progress not gated behind arbitrary failed dice rolls). **No skill trees, levels, tactical combat engine, full character sheet or universal simulation of PSI/cyberspace.** Simple scripted narrative actions and deterministic state transitions are sufficient for the first case.

Use the existing Graph/Tag contracts only where they make the adventure easier; do not rebuild the full RPG via the back door. **The best mechanic is the one that can be omitted without harming the investigation.**

## Political and hacking simulation: OPTIONAL LATER, not MVP blockers

- **Political simulation**: potentially a lightweight interface inspired by [Orwell: Ignorance is Strength](https://store.steampowered.com/app/633060/Orwell_Ignorance_is_Strength/), using a tiny faction/social/ideology graph and evidence-linked dossiers, propaganda/influence choices or surveillance dilemmas. Keep ethical and narrative consequences visible. Existing LaclauGPT/NoöPunk social-simulation research may be a **separate optional provider** of synthetic faction states, not a mandatory runtime for the story.
- **Hacking simulation**: potentially a small fictional puzzle/interface inspired by [DROP - System Breach](https://store.steampowered.com/app/1902300/DROP_System_Breach/), limited to particular investigation scenes. No elaborate general netrunning rule system.
- **No requirement** to implement either for the first playable vertical slice. Reassess only after an enjoyable detective case exists.

## Boundaries with prior work

- #1295's three-track architecture is **reinterpreted**: Story = author-written script; Simulator = playable adventure plus optional small simulation modules; RPG = paused. This issue is the **latest author decision** where older issues conflict.
- #1286 and #1308's LaclauGPT-derived social science research remains **valuable optional infrastructure**, but **not an obligation to build the whole empirical/social simulation before playing**. No full LaclauGPT import, multi-method pipeline, elaborate game mechanics or simulation-first development gate.
- #1309's Social/Ideology/Physical graphs are **optional minimal world/case representations**, not a mandate to complete an exhaustive network society and map of Helsinki before the first case. Maintain Tomi's Paper read-only rule.
- #1301's Helsinki / Europol political-extremism investigations remain useful **story context**, but Romppainen is now the focal detective and the adventure is the deliverable.
- Preserve existing code, documents and schemas unless a targeted change is needed for the adventure. Avoid duplicate engines and do not demand changes across every subproject at once.

## Step-by-step implementation plan (small PRs, one clear goal each)

- [ ] **P0. Reconcile and document pivot** in the relevant agent instructions and entry-point README files without touching `NooPunk-RPG/`, `NooPunk-Story/Story/`, or `NooPunk-Simulator/Paper/`. Explicitly warn agents not to follow stale full-RPG directions. Inventory existing reusable scene/choice/graph/code modules; do not bulk-import or rewrite.
- [ ] **P1. Minimal playable format:** choose one simple, maintainable text adventure interface (CLI or existing browser text UI), a tiny choice/scene/case-state schema and save/load, decoupled from optional simulation providers. Do not build multiple frontends initially.
- [ ] **P2. Investigation mechanics:** implement basic clues, dialogue, leads, hypotheses, case notebook, and branching consequences with no mandatory dice/skill barriers to essential evidence.
- [ ] **P3. Author-content handoff:** consume existing Tomi-written `NooPunk-Story/Story/` source and translate into inspectable Story Graph and game events without agents writing the source story. If essential script material does not exist, use clearly labeled development fixtures, not pseudo-canon; leave Tomi-authored prose to Tomi.
- [ ] **P4. One short playable Helsinki case:** start as a conventional political extremism investigation, with a few locations, suspects, interviews, evidence, decisions and at least one meaningful alternative outcome. No elaborate cosmology required.
- [ ] **P5. Test and refine:** ensure the case can be completed, no investigation softlocks, branching paths work, saved runs resume, narrative source attribution survives and no dormant full-RPG dependency is required.
- [ ] **P6. OPTIONAL after P5:** evaluate a tiny LaclauGPT-inspired faction/political-simulation overlay and/or one hacking minigame as separate, skippable investigation modules. Do not add either if it obstructs story progress.

## Acceptance criteria

- A new contributor reading the repo understands immediately: **NoöPunk's game is Romppainen's detective interactive fiction, NOT a full RPG**.
- `NooPunk-RPG/` remains untouched and there are no mandatory CWN/full-RPG rules or integration tasks.
- Tomi's `NooPunk-Story/Story/` and `NooPunk-Simulator/Paper/` are read-only for agents; the Story can be expanded by Tomi and consumed through a thin adapter.
- At least one playable end-to-end detective case can be completed with simple interactions, clues, decisions and multiple consequences.
- Optional LaclauGPT-inspired ideological/faction simulation and hacking remain clearly optional and independent.
- Work remains small, sequential, psychologically manageable and **focused on writing + playing**, not a sprawling all-genre RPG.

**Bottom line: build an engaging investigative adventure first. Keep world simulation only as deep as the immediate detective case requires.**
