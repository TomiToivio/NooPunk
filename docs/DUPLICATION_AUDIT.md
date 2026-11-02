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
| Coverage documents (`CWN_COVERAGE_MATRIX.md`, `CWN_COVERAGE_AUDIT_1068.md`, `cwn_coverage.json`) | Three overlapping audits | **`docs/rules/CWN_COVERAGE_AUDIT_1068.md` + `data/rules/cwn_coverage.json` are canonical.** My matrix was already deleted in favour of the per-rule audit; a guard now fails if two documents both claim to be canonical. |

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

## What the guard enforces

`tests/test_no_duplicate_implementations.py`:

1. At most **one** console/session implementation class (`Console` or `CaseSession`).
2. The live campaign engine exists and `solo_campaign.py`, if present, stays marked deprecated.
3. At most **one** coverage document claims to be canonical.
4. No module name appears under two code roots unless it is a documented collision.
5. Every documented collision has a written reason **and** an entry in this file.

An audit that cannot fail is not an audit. Test 4 failed on its first run with three collisions; that is the
behaviour that made it worth writing.
