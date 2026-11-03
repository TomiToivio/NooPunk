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
| `docs/rules/CWN_PARITY_MATRIX.md` vs `docs/rules/CWN_COVERAGE_1068.md` | **Same 66-section dataset rendered twice by one tool** | **Merged.** The report is canonical and now carries the full table as an appendix; the matrix is a generated pointer. `tools/cwn_parity_audit.py` emits one document plus the stub, and `--check` fails if either drifts. |
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

## The guard was inert, and that is the finding of this pass

`tests/test_no_duplicate_implementations.py` was written as **five bare `def test_*()` functions**. The root suite
runs `python -m unittest discover -s tests -p "test_*.py"`, which collects `unittest.TestCase` subclasses only:

```
python -m unittest discover -s tests -p 'test_no_duplicate_implementations.py'
Ran 0 tests in 0.000s          <- what CI saw
python -m pytest tests/test_no_duplicate_implementations.py
5 passed                      <- what the author saw
```

So the mechanism meant to stop duplicate work had never executed in CI. It was green by absence. Both test
classes are now `unittest.TestCase`, and the same command collects **5 tests**.

**Rule for every agent:** a test written as a bare function in `tests/` does not exist. It will pass locally
under `pytest` and be invisible to CI forever.

## What the guard enforces

`tests/test_no_duplicate_implementations.py`:

1. At most **one** console/session implementation class (`Console` or `CaseSession`).
2. The live campaign engine exists and `solo_campaign.py`, if present, stays marked deprecated.
3. No module name appears under two code roots unless it is a documented collision.
4. Every documented collision has a written reason **and** an entry in this file.
5. At most **one** document per family (`*COVERAGE*`, `*DUPLICATION_AUDIT*`) claims to be canonical. A demoted
   document must say "pointer" in its opening lines, or it counts as still claiming the role.

An audit that cannot fail is not an audit. Test 3 failed on its first run with three collisions; that is the
behaviour that made it worth writing.

A family is a **question**, not a word in a filename. `*PARITY*` was tried and rejected as a family because
`CWN_SRD_PARITY_AUDIT_858.md` (Godot SRD evidence for #858) and `PORTABLE_RULES_PARITY.md` (portable rulebook ↔
Python contract for #1053) both say "parity" and answer different questions. Matching on the word reproduced
the exact false positive this file exists to prevent.

## Coverage documents: which one answers which question

Several agents have now measured "how complete is CWN", each with a different denominator. They are not
interchangeable, and the confusion has already produced a sixth.

| Document | Question it answers | Denominator | Generator |
|---|---|---|---|
| `docs/rules/CWN_COVERAGE_1068.md` | Are the SRD's navigation sections implemented in Python, with tests? | 66 SRD sections | `tools/cwn_parity_audit.py` |
| `docs/rules/CWN_COVERAGE_AUDIT_1068.md` | Which rules are curated against the tabletop audit, with named procedures? | curated rows | `tools/cwn_1068_coverage.py` |
| `docs/rules/CWN_FE_PARITY_MATRIX.md` | Which pages of the Free Edition PDF are covered? | 98 TOC sections | `tools/cwn_fe_parity.py` |
| `docs/rules/CWN_DELUXE_COVERAGE_1068.md` | What is covered against Deluxe? | 265 printed pages | hand-written |
| `docs/rules/CWN_GODOT_COVERAGE.md` | What does the legacy Godot edition implement? | Godot scripts | hand-written |

**Merged in this pass:** `docs/rules/CWN_PARITY_MATRIX.md` was a second rendering of the *same* 66-section
dataset, emitted by the same tool as `CWN_COVERAGE_1068.md`. It is now a generated pointer, and the full section
table lives in that report's appendix. One tool emitting two documents is the purest form of this bug: the
duplicate is produced by the build, so no reviewer ever chose it.

**Note for the next agent:** `AGENTS.md` lists `CWN_COVERAGE_AUDIT_1068.md` + `data/rules/cwn_coverage.json` as
"the coverage truth", while its §1068 section and `START_HERE.md` name `CWN_COVERAGE_1068.md`. Both files are
real and answer different questions (see the table); the wording is what is ambiguous. Do not resolve that by
deleting either one — resolve it by saying which question you are asking.

**Not merged, and why:** the remaining four documents use different denominators on purpose. Collapsing them
would replace one honest "partial" with one dishonest "complete". If you need a new number here, extend one of
these rows rather than writing a seventh document.
