# #564 acceptance record

**What closure means and does not mean.** This record maps each acceptance criterion to an artefact in the
tree and says whether it is **met** or **deferred**. One criterion is deferred on two author numbers; it is
named as deferred in the closing comment, not counted as met.

Ruling baseline: #566 (`docs/CWN_CHASSIS.md`) — layer A only, `1d10`, `FIT/REF/INT/SOC/CYB/PSY`, no classes or
levels. Provisional and reversible by one word; nothing here depends on it being permanent, because the
deferrals are numeric either way.

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | CWN/SWN comparison and design-choice matrix, referencing earlier decisions, covering every major subsystem | **met** | `docs/design/ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md` — rows 1–24 (subsystem dispositions) + rows 25–29 (AWN/WWN), an SWN-specific table, and `docs/rules/ISSUE_564_FOUR_BOOK_TABLETOP_PROCEDURES.md`. Cites #19, #22, #111, #389, #482 and the author decision queue per row. |
| 2 | One unambiguous current RPG rulebook and engine contract; legacy systems explicitly identified | **met** | `docs/CWN_CHASSIS.md` states the layering: A = the tabletop RPG, B = the crossover's Layer I (approved Fate), C = a board module. Machine contract: `data/rules/core.json` (+ `_canon_revision: issue-111-d10-independent`) and `data/rules/skills.json`. Legacy boundary: `src/rules/_retired.py`, "do not extend". |
| 3 | Six attributes and approved skills coherent; no unauthorised 2d6 / level / class migration | **met** | Ruling keeps `FIT/REF/INT/SOC/CYB/PSY` and `1d10`; `SOC` (not `CHA`) is pinned at `src/rules/core.py:8`. No class or level field exists in the sheet. The kernel's tests remain green and nothing was migrated to 2d6. |
| 4 | Character generation, core tests, investigations, cyber/BCI, PSI, combat, injuries and progression form a playable tabletop loop | **deferred in part** | Core resolution, investigation, cyber/BCI and PSI are implemented and tested (`tests/`, `strategy_game/`); combat and injuries were measured in `docs/design/ISSUE_571_COMBAT_INJURY_TRAUMA.md`. **Missing:** an authored **STAT-generation rule** (`rulebook/14_CHARACTER_GENERATION.md` defers to `RULEBOOK.md` §9.1, which contains no generation method — the only 3d6 helper is retired) and **advancement**, which queue D23 records as unapproved. Both are author numbers. |
| 5 | SWN elements individually justified and scoped; Earth-based play still works | **met** | Matrix "SWN: what actually enters": faction turn `DEFER` (strategic layer, Gate C), world/sector generation `OMIT` (would generate canon), starships `OMIT for now`, classes `OMIT`, psionics `DEFER` (wrong ontology — resolved further by `SUBSYSTEM_PSI_LEARNABLE.md`), saves/morale `MODIFY`. No Earth-based assumption was replaced. |
| 6 | At least one automated end-to-end playthrough per active scenario, deterministic seeds, no LLM | **met** | `strategy_game/tests/test_deterministic_playthroughs.py` covers six scenarios (Ubiquitous Maniacs case + legacy, The Second Shadow's investigate/confront/refer routes, and the plain RPG entry point); CI-gated; `#570` closed with the run recorded (3 tests OK), including the seed-wiring test and mid-run resume. |
| 7 | Scenario/character data migration or compatibility tested and documented | **met** | Compatibility rather than migration, which is the honest description: no data format was changed, so there is nothing to migrate. Adapters and references: `strategy_game/scenarios/ubiquitous_maniacs_cli.py`, the `ubiquitous-maniacs-legacy` route in the harness, `docs/design/RPG_CONVERSION_REFERENCE.md`, and `docs/UBIQUITOUS_MANIACS_INTEGRATION.md`. |
| 8 | Licensing and attribution audited; no protected third-party setting or full-book material copied | **met with a stated caveat** | `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`: CWN SRD CC0, WWN SRD CC0, **SWN Revised unverified**, **AWN has no SRD**. Bounded expression scan over **654 files** (excluding `legacy/`, `archive/`, and the audit documents' own subjects): WN-specific strings appear only in documents *about* the systems — no `Gyrfalcon`, no "Latter Earth" setting text (the two mentions are exclusion notes), no class/partial-class text. Caveat: this is a phrase scan, not a similarity audit, and the audit document itself says a keyword ban is an inadequate detector. |
| 9 | CI passes, canonical docs agree with behaviour, deferred questions listed | **met** | CI green on every PR in this epic (latest merges `b83fd18`, `c4be8f5`, `cdef8af`). Deferred questions live in three places: matrix §6 (the kernel question and its effect), `docs/design/AUTHOR_DECISION_QUEUE.md`, and each new subsystem specification's own "what is deliberately left open" section. |

## What is deferred, precisely

Two items, both author numbers, both already recorded elsewhere rather than invented here:

1. **STAT generation — and it is a conflict, not a gap.** The epic names "3d6 attribute generation and modifier
   range −3..+3" as the author's existing choice. **`data/rules/core.json` says the six STATs are `1..10`**, with
   `_note`: *"The six base STATs are locked by explicit author direction on issue #131 (2026-10-05) … They remain
   the universal 1..10 character attributes."* The kernel consumes a STAT **directly** (`STAT + Skill + 1d10 ≥ DV`);
   there is no modifier band anywhere in the resolution path. The 3d6 / −3..+3 model is the **retired sketch**
   recorded in `AGENTS.md` §4 (the one that also used `CHA`), not the live rule.

   So implementing the epic's sentence would not fill a gap — it would replace the #131 canon, introduce a
   modifier band the kernel does not use, and move every DV's relationship to a character's capability. That is a
   rules change, not a completion task. What is genuinely missing is narrower: **a generation method that yields
   `1..10`** (roll, array, or point-buy — the author's choice), which no document currently states.
2. **Advancement.** Queue D23 records the 25-point / Great-cap baseline without approving a distribution;
   levels are forbidden by this epic.

Neither blocks anything that was built: the kernel, the scenarios, the harness and the subsystems all work
without them. They block a *complete* tabletop loop, which is why criterion 4 is recorded as deferred rather
than met.

## What closure does not mean

- It does **not** mean the numeric subsystems are approved — they remain `DEFER` per #566.
- It does **not** mean a single unified kernel exists: layer A and layer B still resolve differently, and this
  epic settles scope, not convergence.
- It does **not** mean the licensing audit is exhaustive; see the caveat in criterion 8.
- The #566 ruling is **provisional**. Reversing it is one sentence and one follow-up issue, and nothing in this
  record depends on it being final.
