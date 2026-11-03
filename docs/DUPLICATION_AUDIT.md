# Duplicate-work audit

Agents work in parallel on this repository, often on the same issue, often in the same hour. This document is the
record of what that has produced, what was merged, and what is still two things pretending to be one.

**Rule:** if you build something and find a second implementation of it, the answer is never to leave both and hope.
Decide which is canonical, delete or demote the other, and add a line here.

## Resolved in this audit

| Duplicate | What happened | Resolution |
|---|---|---|
| `mud/nopunk_mud/console.py` vs `src/console/session.py` (+ `src/console/play.py`) | Two playable text front ends for the same case | **My console ceded.** `src/console/` is canonical: it has the real case graph, a walkthrough and its own tests. `console.py` and its test were deleted. |
| `BRAINSTORM_1007` pair: `DESIGN_CANON_1007.md` vs `ISSUE_1007_DESIGN_CANON.md` | Looked like two canon documents | **Both kept, cross-linked.** One preserves the author's text; the other is the decision record with `data/world/reveal_ladder.json`. Neither restates the other. |
| `solo_campaign.py` vs `campaign/engine.py` | 58-line prologue and a 464-line engine, both called "the campaign" | **Engine is canonical.** `solo_campaign.py` carries a DEPRECATED header naming the replacement; it survives only because the Evennia command set imports it. Do not add features there. |
| Coverage documents (`CWN_COVERAGE_MATRIX.md`, `CWN_COVERAGE_AUDIT_1068.md`, `CWN_COMPLIANCE_MATRIX_950.md`, `cwn_coverage.json`) | Four overlapping audits and two generators in one day | **One generator, one report: `tools/cwn_parity_audit.py` → `docs/rules/CWN_COVERAGE_1068.md`** from `data/rules/cwn_traceability.json` + `cwn_compliance_matrix.json`. Deleted the second renderer (`check_cwn_compliance.py --render`, `CWN_COMPLIANCE_MATRIX_950.md`) and the third audit (`cwn_1068_coverage.py`, `cwn_tabletop_audit_1068.json`, `CWN_COVERAGE_AUDIT_1068.md`). `docs/CWN_COVERAGE_MATRIX.md` is historical and points at the canonical report. |
| Two files named as a duplication audit (`DUPLICATION_AUDIT.md`, `DUPLICATION_AUDIT_1053.md`) | One is agent-work; the other is generated rule-level code duplication | Renamed the generated one to `docs/RULES_DUPLICATION_AUDIT_1053.md`; this file remains the work-level audit. |

## Known, not yet merged

These are recorded in `tests/test_no_duplicate_implementations.py` under `KNOWN_COLLISIONS`. They pass the guard
only because the reason is written down here.

### `cwn_core` (`src/rules/cwn_core.py` 462 lines, `mud/nopunk_mud/cwn_core.py` 254 lines)
Two CWN kernels. `src/rules` is canonical by ADR 1054; the MUD copy is imported by the parity probes in `tools/`
and by the campaign engine. **Merge plan:** point the engine and probes at `src/rules.cwn_core`, delete the MUD
copy, and let the parity probe compare the kernel against the SRD rather than against a second kernel. Deferred
because the engine's imports were not verified in this pass — and a half-migrated kernel is worse than a labelled
one.

### `social` (`src/rules/social.py` 220 lines, `mud/nopunk_mud/social.py` 189 lines)
Not duplicates: `src/rules/social.py` is the **provisional** #220 social procedures (`IS_CANONICAL = False`);
`mud/nopunk_mud/social.py` is the **#1008** rank/scoped-reputation/goals overlay. Two different rule sets with one
filename. **Merge plan:** rename the #1008 module (e.g. `faction_social.py`) when something next touches it; until
then the docstrings must keep saying which is which.

### `session` (`src/console/session.py` 371 lines, `mud/nopunk_mud/session.py` 129 lines)
Different layers, not duplicates: the portable case session vs the Evennia adapter over `CampaignEngine`.
The names are the problem, not the code.

## Documentation conflicts found while consolidating

The CWN audit pass measured the reader rulebook against the baseline: **15 chapters still teach a
superseded mechanic** (§3.2 attributes, §4.1–4.2 skills/checks, §5.5 combat, §5.8–5.9 and §51 damage and
injury, §7.4 hacking), **17** have related material only and **30** are absent. The authority block at the
top of `RULEBOOK.md` now names CWN and the Without Number baseline, so the chapters are historical — but
they are not rewritten. Do not add a second tabletop audit for this; extend the rulebook chapters or the
traceability `rulebook` column.

## What the guard enforces

`tests/test_no_duplicate_implementations.py`:

1. At most **one** console/session implementation class (`Console` or `CaseSession`).
2. The live campaign engine exists and `solo_campaign.py`, if present, stays marked deprecated.
3. At most **one** coverage document claims to be canonical.
4. No module name appears under two code roots unless it is a documented collision.
5. Every documented collision has a written reason **and** an entry in this file.

The module is written as `unittest.TestCase` so the root CI (`python -m unittest discover -s tests`)
actually executes it; a pytest-only guard would have been invisible. It now also fails when a second CWN
coverage report, a second generator, or one of the retired audit files reappears.

An audit that cannot fail is not an audit. Test 4 failed on its first run with three collisions; that is the
behaviour that made it worth writing.

## 2026-11-03 follow-up: same-night overlapping PRs

| Deliverable | Competing work | Authoritative result | Avoid repeating |
|---|---|---|---|
| Mod activation registry and validator (#1091) | #1090 (schema 2), #1094 (schema 3), #1096 (alternate schema 3) | **#1094 merged**, extending the existing `src/rules/mod_boundary.py` validator and `data/mods/registry.json`; **#1096 closed unmerged**. Compare its unique design ideas before any future incremental change, never resurrect its incompatible schema as a second contract. | A parallel mod registry, validator, or copy of the schema. |
| AWN Stress tracker (#1083) | #1088 / #1092 and duplicate branch changes noted by #1095 | **#1088 and #1092 merged**; #1095 explicitly removed its overlapping tracker changes before merging. | A second `awn_stress_tracker.py` or copied Stress numbers. |
| Portable agent interface (#1084) and WWN effects (#1085) | Earlier unchecked follow-up tickets versus #1095 | **#1095 merged** `src/console/agent.py` and level-1 effects for 13 spells in `src/rules/wwn_spell_effects.py`; 70 spells remain, and a provider-specific Concordia adapter or graphical UI is not implied complete. | Rebuild agent-action validation, seed replay, or the first 13 spell rows. |
| CWN fidelity audit (#1081) | Historical unchecked chapters 1–5 task versus #1095 | **#1095 merged** eight sourced executable assertions in `tests/test_cwn_ch1_5_fidelity_1080.py`. | Treat those eight as missing again, or pretend they verify every remaining CWN chapter requirement. |

**Operational rule for issue owners:** after every merged PR, update the parent/child issue's completed increments and remaining exact scope *before* another agent takes its unchecked boxes. Search open, merged **and closed-unmerged** PRs, inspect merged paths and code; distinguish whole-issue closure from a partial increment. #1081 is the cross-cutting evidence/integration gate; #1083 owns AWN, #1084 adapters/Tarot, #1085 WWN spells and commands, #1086 author decisions. Their overlap is intentional only when the integration gate **links** the owner, not when it starts a second implementation.
