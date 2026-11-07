# Pivot 1310 — NoöPunk is a detective adventure, not a full RPG

> **Status: author decision, 2026-11-07.** Where this document and an older issue disagree, this one wins.
> It is a product-focus decision, **not** authorisation to restructure, migrate or rewrite anything.

**The game is Etsivä Harri Romppainen's detective interactive fiction.** The full tabletop/computer RPG is
**paused**, archived in place, and untouched.

The pivot exists because the set spans several genres and three ontological shocks at once, and chasing
universal mechanics produced unbounded scope and cognitive overload. **Writing and a playable investigation
come first.** Universal rules do not.

## 1. The three tracks after the pivot

| Track | New purpose | Authorship |
|---|---|---|
| **`NooPunk-Simulator/`** | The **playable detective interactive-fiction adventure** — Romppainen investigating political extremists radicalized by the three paradigm shifts. A small optional world/faction simulation may support cases, but is never the game | Agents build the adventure. **`NooPunk-Simulator/Paper/` is Tomi-only, agent READ-ONLY** |
| **`NooPunk-Story/`** | The **interactive-fiction script** — scenes, dialogue, clues, choices, branches, case arcs; may later become a science-fiction book | **`NooPunk-Story/Story/` is Tomi-authored, agent READ-ONLY.** Agents adapt from real author text; they do not fabricate manuscript prose |
| **`NooPunk-RPG/`** | **Paused archive** | **No agent modification unless Tomi explicitly reactivates it** |

## 2. The scope guard, stated as a rule

Do not edit, move, rename, delete, refactor, migrate or "tidy" anything under `NooPunk-RPG/`.

Do not revive CWN character generation, combat, psionics, equipment and economy systems, stat blocks,
levelling or universal rules **for the adventure**. Do not require CWN compatibility to build the adventure.

Do not rebuild the full RPG by the back door. **The best mechanic is the one that can be omitted without
harming the investigation.**

## 3. What the first game actually is

A small, playable detective adventure: receive a case, review a limited set of leads, visit a few Helsinki
locations, interview people, inspect objects and documents, read records, messages and competing ideological
narratives, record **clues, testimony, hypotheses, contradictions and leads** in an interactive case notebook,
choose where to go and how to act, and reach an outcome grounded in what was established — with room for
uncertainty and consequences.

**Minimal engine only:** a Story/Scene graph, an Investigation/Clue graph, simple character and social tags,
locations and case state, a small dialogue/choice interaction, save/load, and an inspectable state history.
Conventional interactive-fiction conventions, plus **GUMSHOE-like clue accessibility**: essential case progress
is never gated behind an arbitrary failed roll.

**Not in the first game:** skill trees, levels, tactical combat, a full character sheet, a universal simulation
of PSI or cyberspace.

**Optional, and only after a case is enjoyable:** a lightweight Orwell-inspired faction/surveillance overlay,
and a small DROP-inspired hacking puzzle as a skippable scene module. Neither is an MVP blocker.

## 4. Inventory of what already exists — read before writing a line

Measured on `main` at `9797a393`. **Nothing here is a mandate to reuse; it is a map so that nobody rebuilds
what is already present.**

| Artefact | Size | Verdict |
|---|---|---|
| `scripts/noopunk_case.py` | 24 l | **Runs today.** Terminal entry point: `--case`, `--opening`, `--first-day`, `--save`, `--load`, `--script`, `--seed` |
| `src/console/session.py` | 424 l | Playable case session over the canonical investigation rules, with save/load. **CWN-coupled** |
| `src/console/play.py` | 423 l | Reference console adapter (`run_command(session, line)`) |
| `src/rules/investigation.py` | 396 l | The investigative layer: **GUMSHOE's core-clue principle** on the CWN chassis. Read for the principle |
| `src/contracts/story_graph_contract.py` | 138 l | The Story Graph contract: what an adaptation may claim and what it may not. **Reusable as a contract** |
| `src/world/scenes.py` | 606 l | Scene procedures for the five live scene types. CWN-and-RPG shaped |
| `src/rules/scene_play.py` | 93 l | "Thin, **CWN-first** scene affordances". Not a starting point for a CWN-free adventure |
| `mud/nopunk_mud/solo_campaign.py` | 62 l | **Deprecated**, superseded by `nopunk_mud.campaign.engine` and `console.session`. Do not extend |
| `src/simulation/`, `src/social_sim/` | — | Optional later simulation providers. **Never a runtime dependency of the story** |
| `legacy/ubiquitous_maniacs/` | — | Older Romppainen-adjacent material (`INGRID-ROMPPAINEN.md`, day-one prototype). Historical |

### The one finding that matters for P1

**A playable terminal detective case already exists and runs** — but its spine is built *on* CWN
(`console.session` → `rules.investigation` → CWN), which this pivot forbids as a requirement.

So P1 has two honest options, and choosing between them is the author's call:

- **A. Standalone adventure core.** A small scene/case/notebook engine with no CWN import, reusing the
  *contract* (`story_graph_contract`) and the GUMSHOE *principle* by re-implementation. It obeys the pivot
  strictly, keeps the paused archive irrelevant, and duplicates a little logic.
- **B. Thin adapter over `console.session`.** Fastest to a playable Romppainen case, but the adventure would
  depend on the paused RPG's rule layer — the "back door" the issue warns about.

**Recommendation: A.** The existing spine is proof that the mechanics work; it is not the thing to build on.

## 5. What is genuinely missing

- **The Romppainen case.** No case content exists for him; `data/` carries other investigations.
- **The case notebook.** Clues, testimony, hypotheses, contradictions and leads as first-class, inspectable
  state. Today's investigation layer tracks discovered facts, not the detective's reasoning over them.
- **Story text.** `NooPunk-Story/Story/` is the source of scenes and dialogue, and it is Tomi's. Until it
  exists, development fixtures must be **clearly labelled fixtures** — never pseudo-canon.

## 6. Boundaries with the earlier directions

| Issue | Its status now |
|---|---|
| **#1295** three-track architecture | **Reinterpreted**: Story = author-written script · Simulator = the playable adventure · RPG = paused |
| **#1286**, **#1308** LaclauGPT-derived social science | **Valuable optional infrastructure**, not an obligation to build the empirical pipeline before playing |
| **#1309** Social/Ideology/Physical graphs | **Optional minimal case representations**, not an exhaustive network society. Tomi's Paper stays read-only |
| **#1301** Helsinki / Europol political-extremism investigations | **Story context.** Romppainen is now the focal detective and the adventure is the deliverable |
| **#950** MUD-first engineering priority | **Superseded as a priority.** The MUD is RPG-track and paused with it |

**Preserve existing code, documents and schemas** unless a targeted change is needed for the adventure. No
duplicate engines, and no demand that every subproject change at once.

## 7. Open questions for the author

- **A or B** in §4 — standalone adventure core, or a thin adapter over the existing session?
- Does Romppainen share the 2045 pre-Crisis Helsinki of #1301, or does his Helsinki differ?
- Which case opens the game, and is it the AGI, PSI or NHI brief from #1301 §8?
- Terminal, or an existing browser text UI? (The issue says choose **one**; do not build several.)
