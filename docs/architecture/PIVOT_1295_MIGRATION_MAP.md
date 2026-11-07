# Migration map: three independent subprojects (#1295)

> **Status: audit and skeleton. Nothing has been moved.** This document inventories the repository as
> it stands, maps each area to one of the three subprojects, and lays out the staged migration. Code
> moves happen in later PRs, one area at a time, with the tree green after each.

Why not move everything now: the repository carries **1,700+ tracked files** and a CI suite of ~3,150
tests across Python, Godot, MUD and generated compliance artefacts. A wholesale move would break import
paths, generated manifests and the CWN immutability gates in a single commit that nobody could review.

---

## 1. The three subprojects

| Human-facing name | Filesystem path | Owns |
| --- | --- | --- |
| **NoöPunk Story** | `NooPunk-Story/` | the manuscript (`Story/`) and its derivative graph (`Graph/`) |
| **NoöPunk Simulator** | `NooPunk-Simulator/` | LaclauGPT-informed social simulation |
| **NoöPunk RPG** | `NooPunk-RPG/` | immutable CWN plus the NoöPunk overlay |

The issue allows the spaced names. Filesystem-safe paths are used, and this table is the mapping.

## 2. Inventory of what exists today

| Current path | Files | What it is | Target |
| --- | --- | --- | --- |
| `design/` | 28 | **Tomi's author drafts**: lifepath, campaign pivot, Greater Helsinki, Galactic Machine War, memories | `NooPunk-Story/Story/` (read-only for agents) |
| `docs/campaign/` | 6+ | campaign outline, dreams worksheet, Tony's lifepath brief, opening flow | split: prose → `Story/`; worksheet indexes → `Graph/` |
| `rulebook/`, `rulebook_parts/` | 51+ | the rulebook: procedures, timeline, character generation | prose → `Story/` (setting text); procedures → `NooPunk-RPG/` |
| `FACTIONS.md`, `GLOSSARY.md`, `START_HERE.md`, `RULEBOOK.md`, `COMPARISON.md` | 5 | top-level orientation and lore | `Story/` (lore) or root (orientation) |
| `docs/graphs/templates/`, `docs/graphs/examples/` | ~12 | SCENE/EPISODE/SERIES/SITE templates and a worked example | `NooPunk-Story/Graph/` |
| `src/world/graphs.py`, `src/world/scenes.py` | 2 core modules | the four graph families and the scene procedures | **shared contract**, later `NooPunk-RPG/` |
| `data/scenarios/lakkahaltia/case_graph.json`, `data/world/politics_1252_graph.json` | 2 | authored graph data | `NooPunk-Story/Graph/data/` once the contract is versioned |
| `src/rules/` | 193 | CWN core, SWN/AWN imports, NoöPunk overlays | `NooPunk-RPG/` (CWN **unchanged**) |
| `src/console/` | 6 | reference CLI adapter, first day, opening join | `NooPunk-RPG/` |
| `mud/`, `campaign/`, `strategy_game/`, `godot/`, `mods/`, `portable_noopunk/` | 400+ | MUD, campaign engine, strategy game, Godot client | `NooPunk-RPG/` |
| `docs/design/`, `docs/rules/` | large | design decisions and rule notes | mostly `NooPunk-RPG/`; canon prose → `Story/` |
| — | 0 | **no Simulator code exists in this repository** | `NooPunk-Simulator/` is new |
| `docs/design/ISSUE_1008_PHASE2_LACLAU.md`, `docs/research/` | ~20 | Laclau methodology notes and research | `NooPunk-Simulator/docs/` |


### Shared and infrastructure paths

| Current path | Target |
| --- | --- |
| `src/` | `NooPunk-RPG/src/` at P4; the shared contract modules move last |
| `tests/` | `NooPunk-RPG/tests/` for RPG suites; Simulator and Story Graph get their own suites from P2/P3 |
| `docs/` | split: `docs/architecture/` stays shared; rules docs → RPG; lore and prose → Story |
| `data/` | split: rules data → RPG; authored graph data → Story Graph; simulator fixtures → Simulator |
| `scripts/`, `tools/` | shared; `tools/rules_constitution_audit.py` stays the CWN gate wherever the core lives |

**The honest finding:** two of the three subprojects already exist under other names. The Simulator
does not exist here at all — the LaclauGPT pipeline lives in its own repositories, and this repository
holds only notes about it. That makes the Simulator the only genuinely new build in this pivot.

## 3. Staged plan

| Stage | Content | Tree state |
| --- | --- | --- |
| **P0 (this PR)** | three folders, READMEs, agent policy, CODEOWNERS, shared-contract note, this map | nothing moved; suite green |
| **P1** | Story boundary enforced: `Story/` holds Tomi's drafts, an index, and a guard; agents get read-only instructions | still no code moves |
| **P2** | Story → Graph workflow: template, conversion procedure, source references, validation | `Graph/` gains its first converted scene |
| **P3** | Simulator skeleton: module boundary, Phase 1 attribution, Tag/Graph adapter, independent tests | standalone, no CWN import |
| **P4** | RPG isolation: move `src/rules`, `src/world`, console, MUD, Godot behind `NooPunk-RPG/` with compatibility shims | largest and riskiest; separate PRs per area |
| **P5** | Vertical slice: author-written scene → Graph → RPG scene, with Simulator-supplied social context | integration proven end to end |

Each stage keeps the suite green and lands separately. P4 is deliberately last: it is the only stage
that can break imports.

## 4. What must not happen

- **No agent writes inside `NooPunk-Story/Story/`.** Not as a refactor, not as a "formatting pass", not
  as a side effect of generating a graph.
- **No change to CWN.** The RPG side moves; its rules do not.
- **No redesign of the LaclauGPT Phase 1 theory.** The Simulator consumes it.
- **No big-bang move.** If a stage cannot be made green, it stops there.

## 5. Ownership and enforcement

| Mechanism | What it does | Limit |
| --- | --- | --- |
| `AGENTS.md` rule | states the boundary in the file every agent reads first | a rule, not a lock |
| `.github/CODEOWNERS` | requires Tomi's review for `NooPunk-Story/Story/` | effective only if branch protection uses it |
| `tests/test_issue_1295_structure.py` | fails if the boundary text, folders or CODEOWNERS entry disappear; fails if executable content appears under `Story/` | cannot see a commit that bypasses CI |
| Git history | the manuscript's authorship stays visible per line | agents commit under Tomi's identity, so author alone is not a proof |

**Stated plainly:** with agents committing as the repository owner, no git-level check can prove who
typed a line. The enforceable promise is *review*, not authorship — CODEOWNERS plus the instruction
plus a guard that fails loudly when the boundary is edited away.

## 6. Shared contract

See [`SHARED_TAG_GRAPH_CONTRACTS_1295.md`](SHARED_TAG_GRAPH_CONTRACTS_1295.md). One format, three
consumers, and changes to it need a cross-project review — not a silent edit in whichever subproject
happened to need it first.

## 7. Success criterion, restated as a test

> Tomi can write an original branching scene; an agent converts it to Story Graph; the RPG plays it
> with Simulator-supplied social context; neither the manuscript nor CWN is touched.

P0 proves none of that. It only makes the direction unambiguous enough that the next four stages can
be reviewed on their merits.
