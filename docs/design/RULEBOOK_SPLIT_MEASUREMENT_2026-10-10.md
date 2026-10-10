# Rulebook split: measurement, the defect it exposed, and migration notes (issue #232)

**Status: companion notes. The canonical artefacts are `data/rules/rulebook_segmentation.json`
(the section→part map), `rulebook_parts/` (the generated parts) and `tools/split_rulebook.py`.**
This document carries no second map and decides no canon. `RULEBOOK.md` stays canonical.

## 1. A duplicate that was retired, not kept

`docs/rulebook_map.json` (a second total section→part map, with a second guard) existed briefly
in this repository. It was written **two minutes after** the eight-part map landed in #234, and
the two disagreed on granularity — nine parts against eight — which means every future section
addition would have had to be entered twice, in two files that nothing kept in sync.

Two sources of truth for one fact is the defect, so the duplicate was **removed** and its unique
value folded into this document: the per-part measurement, the migration protocol, and the
record of the defect below. The eight-part scheme is now the single vocabulary.

## 2. The measurement

Every section of `RULEBOOK.md` (320,640 characters, 64 top-level sections), assigned:

| Part | Sections | Characters | Share |
| --- | ---: | ---: | ---: |
| `07_lore_and_world` | 14 | 188,341 | **58.7%** |
| `06_social_systems` | 8 | 32,781 | 10.2% |
| `00_meta_and_provenance` | 16 | 26,684 | 8.3% |
| `02_character_generation` | 3 | 22,337 | 7.0% |
| `01_basic_rules` | 8 | 19,482 | 6.1% |
| `05_psychic_systems` | 5 | 16,450 | 5.1% |
| `04_cybernetic_systems` | 5 | 8,411 | 2.6% |
| `03_physical_systems` | 5 | 6,154 | 1.9% |
| **Total** | **64** | **320,640** | 100% |

**The rulebook is a lore document with a rules appendix, not the reverse.** Lore is 58.7% of it;
the four domain systems together are **14.7%**, and combat — the thing a reader is most likely to
open the book for — is **1.9%**. That is not a criticism of the document: it is the measurement
that justifies issues #219–#228 as work packages, and it is the argument for the split, because
those pages are currently reachable only by crossing a 188 KB lore span.

## 3. The defect this work found and fixed

The first generated parts **contradicted their own map**, and every existing test passed.

`tools/split_rulebook.py` classified each segment as `preamble` (before the core/ledger marker),
`marker`, or `ledger`, and then assigned **every** preamble segment to `00_meta_and_provenance`
without consulting the map. The map, meanwhile, declared the core half explicitly — `core: ["3",
"4"]` for Basic Rules, `core: ["5"]` for Physical, and so on.

The result: **the entire playable core game-book — Stats, Skills, the four system chapters,
character generation, and the history that opens the book — was filed under a part whose stated
purpose is *"Not player-facing rules"***, while `01_basic_rules` contained only ledger sections
and `02_character_generation` contained no character generation. A reader following the split
would have found the rules exactly where the index said they were not.

Nothing caught it, because both of the guard's properties were satisfied:

- **totality** — every section was assigned to *some* part;
- **losslessness** — the bytes were all preserved, in order.

Filing everything into one part satisfies both. The properties that were missing are the ones
that matter to a reader: *which* part, and *does each part contain what it declares*.

### The fix

`assign()` now resolves a core-half section against the map's `core` list — the two numbering
spaces restart at 1, so a section's key depends on which side of the marker it sits. Only the
title heading, the unnumbered table of contents, the marker and structural H1s stay with the
meta part. `01_basic_rules` now contains `## 3. Stats` and `## 4. Skills`; the four system
chapters sit in their own books; the map's `core` lists are live data instead of decoration.

### The guard

`tests/test_rulebook_segmentation.py` gained `ThePartsContainWhatTheMapDeclaresTests`, which
asserts the declaration against the artefacts: every part delivers **exactly** the sections the
map assigns it, the core numbering space gets the same totality check the ledger already had,
and the written `01_basic_rules.md` really contains Stats and Skills. Sabotage-verified: reverting
the assignment fix fails it, as do dropping a declared core section, letting meta claim one it
does not deliver, removing a heading from a generated part, and dropping a declared ledger
section.

## 4. Migration protocol

Not executed here. This is the checklist a later, author-approved migration follows, derived from
what currently depends on the document's shape:

1. **Guards that pin the two-document shape.** `RULEBOOK.md` is asserted to be a core book
   numbered `1..8` plus a ledger numbered contiguously, split by the marker. A file move must
   migrate those assertions in the same change, never delete them.
2. **Citation resolution.** `tests/test_theory_sections_survive.py` resolves every `§x.y` written
   *inside* `RULEBOOK.md` against headings *in* `RULEBOOK.md`; modular chapters are cited **by
   link, never by their own §-numbers**. A per-book split must keep in-file citations in-file, or
   convert them in one pass.
3. **The change ledger** (`## 27. Change ledger`) legitimately quotes superseded text, so absence
   guards must stay ledger-aware across a move or they will red on the history itself.
4. **`data/rules/core.json` and the runtimes consume values, not prose** — the split must not
   change any value they read.
5. **Do not renumber.** Book-local numbering would break every existing `§` citation in the
   repository and in closed issues.

## 5. What this does not do

- It does not move, cut, reorder or rewrite a single character of `RULEBOOK.md`.
- It does not select a licence and does not touch the release gate (#231).
- It does not authorise rule content: the four domain books are 1.9%–5.1% written, and filling
  them is #219–#228's work on the author's approval.
- It does not supersede either the staging snapshots (`docs/rulebook_segments/`) or the
  navigable parts (`rulebook_parts/`); those are the two losslessness guarantees, byte-level and
  section-level respectively.
