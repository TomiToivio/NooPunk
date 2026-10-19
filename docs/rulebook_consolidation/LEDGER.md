# Issue #243 lossless consolidation ledger (IN PROGRESS)

Baseline: `84b0e1cb517ddf7a92ba07077ab2ebb65fba3cad` (2026-10-10). Full machine-readable inventory: [inventory.json](inventory.json).

## Verified preservation

- Root `RULEBOOK.md` and all nine `rulebook_parts/` files are copied into `rulebook/source_snapshots/` by **reusing their original Git blob SHAs**, not regenerating their text. The original paths remain intact at this stage. Exact source-to-snapshot mapping is in `inventory.json`.
- Existing `rulebook/` chapters, including all twelve `rulebook/parts/` files, retain their baseline locations and blobs. This avoids risking data loss in the first migration commit.
- This snapshot is an archival input for review, **not another editable canonical rulebook**. All new authoring goes to the reconciled chapters under `rulebook/`.

## Mandatory pending reconciliation

1. Enumerate headings and anchors recursively within every one of the 40 inventoried Markdown inputs; compare root compilation, both part directories, and canonical numbered chapters paragraph by paragraph.
2. Assign each source section a destination chapter and status: `moved`, `identical duplicate`, `overlapping retained`, `contradiction unresolved`, or `licensed content quarantined`. Preserve examples, equations, tables, TODOs and tiny lore details. A source-file copy alone does not satisfy this step.
3. Resolve headings, duplicate indexes and cross-links. Cross-check `data/rules/`, tabletop, Godot and Concordia use, and licensing/attribution. Do not invent mechanics, remove competing systems, or call unapproved mechanics canon.
4. Add reproducible checks for anchor links, section-level mapping coverage and unintended hash/content changes; run CI. Recheck against newest `main` and other agents' PRs before merge.
5. Only after human review of all 40 inputs, stop maintaining root `RULEBOOK.md` and `rulebook_parts/` as alternate active sources. Never delete raw snapshots merely because they look redundant.

## Disposition at this checkpoint

- **40/40 baseline files enumerated**, with Git blob ID and byte length; **10/10 external source blobs snapshotted**.
- **0 sections certified reconciled**; no original content deleted; all semantic conflicts remain pending.
- Pending: content review, agent instructions update (respect protected AGENTS.md decisions), links, generated output decision, tests and cleanup. This PR must not be reported as issue completion.

## Issue #497 contact-first lore extension (2026-10-16)

- **Source:** [issue #497](https://github.com/TomiToivio/NooPunk/issues/497), including its PSI-awakening extension. **Destination:** `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md` (new lore chapter; no old material removed).
- **Cross-references only:** `rulebook/7_TIMELINE.md`, `rulebook/16_CONFEDERACY_SOURCE_AND_CONTACT.md`, `rulebook/README.md`, `docs/scenarios/FIRST_CONTACT_TEN_TRADITIONS.md`.
- **Compared overlapping sources:** `rulebook/6_PSYCHIC.md` (human PSI is innate and independent of alien origin); `rulebook/15_XENOPOLITICS.md` (post-Crisis reconstruction frame retained as distinct); `docs/scenarios/PREFALL_FIRST_CONTACT.md` (older first-contact vertical slice retained unchanged); `docs/archive/DESIGN_PRINCIPLES.md` and `AGENTS.md` (mechanics and three balances unchanged).
- **Resolved by author's ruling of 2026-10-16** ("No, my issues are the new canon. Just do the issue and edit the canon! Tomi's word is always canonical!" — closing the earlier "optional 2045 scene / master 20XX non-chronology" distinction): the canonical setting year is **2045**, and issue #497's First Contact / Orion cold-war beats are **canon, not an optional scenario**. Applied to the live rulebook only: `rulebook/7_TIMELINE.md` (setting-year header, `Before 2045` headings), `rulebook/00_START_HERE.md`, `rulebook/1_NOÖPUNK.md`, `rulebook/16_CONFEDERACY_SOURCE_AND_CONTACT.md` (setting-year statements), `rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md` (canonical status, 2045 campaign present), `rulebook/README.md` (canon statement). The unordered-paradigm-shifts device survives unchanged as the account of how the setting reached 2045; the Grey diplomatic interval versus post-Crisis reconstruction **ordering** remains an open, explicitly distinguished question, and this ruling does not sequence the individual paradigm shifts by year. No archival snapshot, `RULEBOOK.md`, `rulebook_parts/`, `rulebook/parts/`, or executable code modified. Editorial review and tabletop playtesting apply, not documentation CI gates.

## Issue #517 cyberspace consolidation and narrative-first hacking (2026-10-19)

- **Source:** [issue #517](https://github.com/TomiToivio/NooPunk/issues/517), with issue #344's three dated author-canon clarifications as the connectivity model it must not contradict. **Destination:** `rulebook/22_CYBERSPACE_AFTER_THE_CRISIS.md` (new canon chapter; no old material removed), plus additive cross-references in `rulebook/5_CYBERNETIC.md`, `rulebook/10_SINGULARITY_CRISIS.md`, `rulebook/00_INDEX.md` and `rulebook/README.md`.
- **Compared overlapping sources, paragraph by paragraph:** `rulebook/5_CYBERNETIC.md` (four access modes, node card, T0–T4, Trace/ICE, software/hardware/wetware ladder — reused, not restated); `rulebook/18_CROSS_DOMAIN_STATE.md` (action clock, single-locus rule, realm gateway table — cited, not restated); `rulebook/10_SINGULARITY_CRISIS.md` §9.2.1, §9.4, §9.6, §9.15 (the three ASIs, the five Crisis explanations, the undefined thresholds); `rulebook/19_NARRATIVE_LAYER.md` (four outcome bands and the one-step bound); `rulebook/21_PSI_PARADIGM_SHIFT.md` (Noösphere vs Noöspace terminology); `RULEBOOK.md` §10.1 (difficulty band names) and §34 (Firewall retired as an in-world term); `rulebook/15_XENOPOLITICS.md` §187.7/§187.10 (post-Crisis politics; that chapter's "no economy" boundary respected); `strategy_game/docs/CYBERSPACE_AND_CONNECTIVITY.md` and `strategy_game/data/connectivity.json` (issue #344's five connectivity classes, retained by name and not forked).
- **Terminology decisions, recorded rather than improvised:** "Firewall" stays retired as an in-world name (`RULEBOOK.md` §34); **Blackwall** is the in-world shorthand and #517's "Firewall" is treated as the comparison it is. "Safenet", colloquially "Slownet", is #344's term and is kept. The new **access classes** (how the operator reaches a target) are stated as orthogonal to #344's **connectivity classes** (what the target is), with an explicit pairing table, so neither taxonomy replaces the other.
- **Refinements to existing canon, stated as refinements:** the three ASIs are distributed swarms (new §9.16); Panopticon is the only *legally* authorised ASI, UN-licensed and corporate-operated (§9.16.1); the Noösphere self-identifies as "we are the Noösphere" with its identity claim deliberately unresolved (§9.16.2); Thanatos survives inside the quarantined old Internet in addition to the wormhole escape already in §9.4.3, and is fixed as the entity *responsible* for the Crisis while §9.2.1's five *mechanisms* remain contested (§9.16.3). No existing line was deleted, reworded or renumbered.
- **Not claimed as canon:** every band-to-situation mapping, the "one C/I/N step per check" bound, the four heat states and the one-warning BCI rule are marked **TUNING PARAMETER**. No dice, difficulty value, probability or stat block was added; no new Skill, STAT or skill taxonomy was created.
- **Tests:** none added and none removed. Per `AGENTS.md` and #271 this is lore and prose; it is reviewed editorially and by tabletop playtesting, not by a CI gate. The existing suites were run unchanged after the edit (`tests` and `strategy_game/tests`).
- **Not modified:** `RULEBOOK.md`, `rulebook_parts/`, `rulebook/parts/`, `rulebook/source_snapshots/`, all `data/rules/*.json`, all executable code.
