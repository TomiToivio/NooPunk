# Pivot: NoöPunk: Etsivä Romppainen ja Uusi Paradigma (#1310; revised by #1322)

> **Status: original author decision 2026-11-07; updated project title and framing 2026-11-08 by #1322.** NoöPunk's playable product is an **old-fashioned detective
> interactive-fiction adventure** in cyberpunk Helsinki, with **Etsivä Harri Romppainen** as the detective. The
> full tabletop/computer RPG is **paused and preserved**, not deleted and not to be developed.

The full RPG remains paused. This page documents the original implementation pivot and is subordinate to the current [README](../../README.md) and [#1322](https://github.com/TomiToivio/NooPunk/issues/1322) for public title, motivation and pre-crisis scenario. The author-only manuscript is not yet an approved playable episode.\n\nThis page is the reconciliation P0 of [#1310](https://github.com/TomiToivio/NooPunk/issues/1310). It says what each track
is now for, what an agent may touch, and — because the repository already contains a playable case — **what is reuse and
what is not**.

---

## 1. The three tracks, as they now stand

| track | purpose now | who writes it | what an agent may do |
|---|---|---|---|
| **`NooPunk-Simulator/`** | the **playable detective adventure**, plus an *optional* small world/faction simulation supporting cases | code: agents; `Paper/`: **Tomi only** | build and test the adventure; treat `Paper/` as read-only, as `NooPunk-Simulator/AGENTS.md` already requires |
| **`NooPunk-Story/`** | the **interactive-fiction script**: scenes, dialogue, clues, choices, branches, case arcs; later possibly a novel | **Tomi only** in `Story/` | derive graph/index/adapters **from** the manuscript; never write prose into `Story/` |
| **`NooPunk-RPG/`** | a **paused full-RPG archive** | — | **nothing.** Do not edit, move, rename, refactor, migrate or "tidy" it; do not revive CWN character generation, combat, psionics, economy, stat blocks or leveling |

**Superseded expectations.** [#1295](../architecture/PIVOT_1295_MIGRATION_MAP.md)'s three-track architecture is
*reinterpreted*, not abolished: Story is the author's script, Simulator is the playable adventure, RPG is paused.
#1286 and #1308's LaclauGPT research stays valuable **optional** infrastructure rather than a prerequisite gate;
#1309's graphs become optional case representations; #1301's Helsinki and Europol material stays useful **story
context** with Romppainen as the focal detective.

**What this does *not* license:** destructive restructuring of directories, rewriting theory papers, or "finishing" the
RPG by another name. The guard is symmetrical: no RPG development, and no adventure feature that quietly requires one.

---

## 2. What already exists, and what it is worth

An inventory, because the pivot's risk is rebuilding what is already here. Sizes are lines on `main` at the time of
writing; the verdict is a recommendation, not a promise.

### 2.1 Reusable as-is for the adventure

| module | what it does | verdict |
|---|---|---|
| `scripts/noopunk_case.py` + `src/console/play.py` (423) | **a working text adventure**: `look`, `go`, `clues`, `take`, scripted beats for tests | **the P1/P2 substrate.** It already runs: `python scripts/noopunk_case.py --script beats.txt` prints scenes, leads and clues. Do not write a second console |
| `src/console/session.py` (`CaseSession`, `load_session`) | case state, save/resume | reuse; extend only if the adventure needs a state the session cannot hold |
| `src/rules/investigation.py` (396) | **GUMSHOE's core-clue principle**: clues, `Investigator`, `load_case_graph`; essential clues are not behind rolls | reuse. This is the mechanic #1310 asks for and it exists |
| `data/scenarios/lakkahaltia/*.json` | a complete case graph, dialogue, chassis drill | **reuse as the worked example** and as the test fixture; whether it is *Romppainen's* first case is an author decision |
| `src/world/graphs.py` (story/social/physical/cyber graphs) | typed graph records with validation | reuse **selectively** — a case needs scenes and leads, not four graph families |
| `docs/graphs/templates/` | Series / Episode / Scene / Domain templates | reuse as the authoring format |
| `docs/scenarios/CASE_BRIEFS_1301.md`, `CASE_01_THE_TUESDAY_COMPLAINT.md` | three shift-based briefs plus one complete case with a GM ledger | **story context**: candidates for the first Romppainen case, but the detective is Romppainen, not Tony |

### 2.2 Optional, and only after a case is fun

| module | what it does | verdict |
|---|---|---|
| `src/social_sim/kernel.py` + `ai26.py` (WP1/WP2, #1286) | deterministic synthetic population, read-only AI26 adapter | **optional provider** of faction state. Never a runtime dependency of the story |
| `src/campaign/{clock,story,daily,tasks}.py` | clock, story arcs, daily loop, tasks (#1230) | optional case pacing; do **not** make the player keep a timetable to investigate |
| `src/world/networks.py`, `data/world/networks.json` | connectivity classes and the authorisation ladder | optional for a hacking scene that #1310 calls *later* |
| `docs/lore/eu_technology_bureaucracy.md`, `docs/world/PLATO_EISS_EURONET_1200.md` | institutions, hardware, authorisation | **background for writing**, not systems to implement |

### 2.3 Frozen: read, do not extend

| path | why |
|---|---|
| `src/rules/cwn_*.py`, `src/rules/*.py`, `rulebook/`, `RULEBOOK.md` | the CWN chassis and the RPG's rules. Paused |
| `mud/`, `src/godot/`, `godot/`, `mods/`, `strategy_game/`, `portable_noopunk/`, `noopunk/` | RPG front ends and adapters. Paused |
| `src/console/first_day.py`, `src/console/opening.py` | Tony German's first day and opening flow. Superseded as *the* opening; keep as history |
| `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md`, `design/characters/*` | Tony's campaign and lifepath drafts. Story context, not the deliverable |
| `NooPunk-RPG/**` | **untouchable** by this issue's hard guard |

**The duplication rule still applies.** Two text adventures, two clue models or two case-state schemas would be a
regression, not progress.

---

## 3. What the pivot actually adds

The adventure's *engine* largely exists; what it lacks is **Romppainen as the detective**, an **author-supplied script**
to play, and an **entry point a newcomer understands**.

| step | state after this P0 | next action |
|---|---|---|
| **P0 reconcile and document** | **this page**, the root directive, and the two subproject READMEs | done here |
| **P1 minimal playable format** | already satisfied in kind: one CLI, scripted and interactive, save/load | verify it against Romppainen's case rather than Tony's; no new frontend |
| **P2 investigation mechanics** | already satisfied in kind: clues, leads, notebook, no dice gate on essentials | add the *hypotheses and contradictions* notebook the pivot names, if the script needs it |
| **P3 author-content handoff** | not started | a thin adapter that reads Tomi's `NooPunk-Story/Story/` script into scene/choice records; fixtures labelled as fixtures until the prose exists |
| **P4 one short playable case** | the Lakkahaltia case exists; whether it is the pivot's case is Tomi's call | either retarget it to Romppainen or build the first Romppainen case from a brief |
| **P5 test and refine** | the console case has tests; softlock and branch coverage need a case-specific check | after P4 |
| **P6 optional politics/hacking** | not started, and deliberately last | only if it does not obstruct the story |

---

## 4. Boundaries an agent must not cross, stated once

1. **`NooPunk-RPG/` is not edited** in any way, for any reason, unless Tomi reactivates it explicitly.
2. **`NooPunk-Story/Story/` and `NooPunk-Simulator/Paper/` are read-only.** Agents may read them and derive graphs; they
   may not write prose, restructure them, or "improve" them.
3. **No CWN compatibility requirement.** Building the adventure does not require character generation, combat, psionics,
   equipment economy or levels.
4. **No second engine.** Extend `src/console/` and `src/rules/investigation.py`; do not create a parallel adventure
   runtime, a second clue model or a second save format.
5. **No pseudo-canon.** If the script for a scene does not exist, use a clearly labelled development fixture, or leave
   the scene out.

---

## 5. Open decisions for Tomi

1. **Is the Lakkahaltia case retargeted to Romppainen** (renaming and rewriting its fiction), or kept as a separate
   training case while a new Romppainen case becomes the first?
2. **Does the adventure use the four graph families at all**, or only scenes, leads and clues? The pivot says graphs are
   optional; the existing code offers them.
3. **What the first case is about** among the three paradigm shifts — and whether it names a real movement or invents
   one.
4. **How much of the notebook is player-facing**: a flat clue list (as today) or hypotheses, contradictions and a
   conclusion the player commits to?
5. **Whether the novel and the interactive fiction share one manuscript** or drift into two, and which is canonical if
   they differ.

---

## 6. Verification of this page's claims

* The text adventure runs today: `PYTHONPATH=src python scripts/noopunk_case.py --script beats.txt` prints scenes,
  leads and clues for `data/scenarios/lakkahaltia/case_graph.json`.
* The clue model is `src/rules/investigation.py`; the console is `src/console/play.py`; the save format is
  `src/console/session.py`.
* Nothing in this document requires a file under `NooPunk-RPG/`, `NooPunk-Story/Story/` or `NooPunk-Simulator/Paper/` to
  change.
