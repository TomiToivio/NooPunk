# RULEBOOK.md: the constraint that shapes the split, and the one ambiguity left

Companion to [`docs/rulebook_segments/README.md`](../rulebook_segments/README.md), which owns the
segmentation itself (nine lossless segments, `manifest.json`, the seven-book destination). This file
records the two things that guide has no reason to: **why cutting `RULEBOOK.md` up does not work**,
and **a numbering collision that the seven-book migration will hit**. Read both before restructuring
anything.

## Why `RULEBOOK.md` must stay canonical and whole

The natural reading of "split the rulebook" is: move each section's body into a part and leave
`RULEBOOK.md` as an index. **That was implemented, and it failed 309 tests.** The suite reads
`RULEBOOK.md`'s *body*, not merely its headings — lore, glossary, faction and mechanics guards all
assert on text inside the file. Rewriting 309 tests to follow the bodies would have been the largest
possible risk to precisely the content this work exists to protect.

So the direction is reversed, deliberately and permanently: **`RULEBOOK.md` stays the canonical,
unedited text; the parts are generated views of it.** Any future attempt to empty the file should
expect the same 309 failures, and should not start.

The same constraint applies to *editing* it. Inserting seven lines of navigation into
`RULEBOOK.md` was enough to invalidate every offset in `docs/rulebook_segments/manifest.json` and
break `test_issue232_lossless_segments`. That manifest is frozen against the file byte-for-byte:
**any change to `RULEBOOK.md` must regenerate the segments in the same commit.**

## The numbering collision

`RULEBOOK.md` contains **two independent `## N.` runs**, separated by the marker
`# Extended canon and reference material`:

| Run | Numbers | What it is |
| --- | --- | --- |
| core | `1`–`9` | The current rulebook: Stats, Skills, the four domains, Character Generation |
| extended canon | `1`–`54` | A preserved reference ledger, including the 1816-line world-lore section |

**All nine core numbers collide with ledger numbers.** So:

- `§51` is unambiguous — there is only one.
- **`§5` is ambiguous** — core "Physical Systems" *or* ledger "Primary Eclipse Phase references".

Three guards already pin the runs separately (`test_issue101_sources_dedup` splits on the marker and
requires `1`–`9` before it and contiguous `1`–`N` after), so the duplication is deliberate and
guarded — **not drift, and not something an agent should "tidy"**. `tests/test_issue232_numbering_runs.py`
pins the collision explicitly and independently verifies that
`data/rules/rulebook_segmentation.json` disambiguates the two spaces rather than using one bare
section list.

#232's first acceptance criterion asks for "no conflicting rules definitions". Reconciling these two
runs means choosing a canonical run and renumbering the other, which breaks an unknown number of
`§N` cross-references across the repository and the lore. **That is an author decision**, so it is
reported here and left alone.

## The rulebook's shape is load-bearing

`RULEBOOK.md` is not just text; three guards constrain its structure, and all three are about
cross-references resolving:

| Guard | Constraint |
| --- | --- |
| `test_issue101_sources_dedup` | core `## 1.`–`## 9.`, then contiguous `## 1.`–`## N.` after the marker |
| `test_issues171_180_cross_references` | the `§N` *universe* is RULEBOOK.md's headings + every self-numbering `rulebook/*.md` chapter; every `§N` anywhere must resolve against it |
| same test | every self-numbering `rulebook/*.md` must be **linked from RULEBOOK.md** |

A heading deleted from `RULEBOOK.md` silently orphans references elsewhere. Note also that
`rulebook/*.md` is globbed by the second guard, which is why generated segments live in
`docs/rulebook_segments/` and not under `rulebook/`.

## Working on the subsystem issues

Maintainers of #217–#232: build on these rather than duplicating them.

| Artifact | Issue | What it decides |
| --- | --- | --- |
| `data/rules/rulebook_segmentation.json` + `tools/split_rulebook.py` | #232/#237 | the section→book map and the lossless split |
| `src/rules/issue200_resolution_lab.py` | #207 | exact odds on the raw scale |
| `data/rules/fudge_scale_migration.json` | #213 | the **author-directed** 1–10 → −3..+3 mapping. Consume it; do not re-declare it |
| `src/rules/kernel_prototype.py` | #209/#215 | candidate combination rules on the ladder |
| `src/rules/aspects_prototype.py` | #233 | aspects, narrative resource, consequences |
| `data/sources/game_system_rights.json` | #200/#231 | rights provenance for the CC release |

Rules that apply to every change here:

- **`AGENTS.md` is the canonical contract**; `tests/test_design_principles.py` fails the build if the
  documents and the design invariants disagree — including that the AGENTS.md §13.2 pole sentence
  matches the canonical document (see #200 / PR #214).
- **New numeric values are DRAFT** until the author calibrates them; say so in the docstring.
- **Deterministic and auditable.** Rolls and state transitions belong in tested code, never in an
  LLM prompt.
- **No invented lore or rules** — `AGENTS.md` §4 reserves unspecified numbers, factions and
  technologies to the author.
