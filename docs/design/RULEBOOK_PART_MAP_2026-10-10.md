# Rulebook part map (issue #232)

**Status: PROPOSED, non-destructive.** This is the **executable form** of the seven-book
architecture already recorded in [`docs/rulebook_segments/README.md`](../rulebook_segments/README.md).
It decides no canon and moves no text: `RULEBOOK.md` remains the single canonical source.

## Why this document exists

The architecture README states the destination — *seven readable books* — and its own integrity
checklist carries the open item:

> `[ ]` Move *approved canonical text* to the seven future book sections, preserve every passage
> (or explicitly archive obsolete historical notes), citations and existing link targets.

That step needs an answer the README does not give: **which section of the 320 KB rulebook
belongs to which book.** Without it the migration is guesswork, and the failure mode is a
section that belongs to no book and is silently left behind — the one outcome the issue forbids
(*"do not lose anything"*).

So this document does one thing: it assigns **every one of the 64 sections** to a book, in
machine-readable form, and a guard re-derives the section list from `RULEBOOK.md` to prove
nothing went homeless. It complements, and does not replace, two pieces of work already merged:

| Guarantee | Held by |
| --- | --- |
| no **byte** lost (staging snapshots) | `docs/rulebook_segments/manifest.json` + `tests/test_issue232_lossless_segments.py` |
| no **section** homeless (ownership map) | `docs/rulebook_map.json` + `tests/test_rulebook_split_map.py` |

## What the document actually is (measured, not assumed)

| | |
| --- | --- |
| `RULEBOOK.md` | **320,640 characters** |
| Top-level `##` sections | **64** — 10 in the core half, 54 in the ledger half |
| Marked split | `# Extended canon and reference material` at offset **37,416** |

The rulebook is already **two documents in one file**: a ~37 KB **core game-book** (§1–§9) and a
~283 KB **ledger** (§1–§54). The asymmetry is the single most important fact for the migration,
because the core half is already a complete, playable book and the ledger is where nearly all
the material lives.

## The measurement that justifies the two provisional parts

Assigning all 64 sections gives:

| Part | Sections | Characters | Share |
| --- | ---: | ---: | ---: |
| NoöPunk Lore | 9 | 143,299 | **45.0%** |
| Reference & Provenance *(provisional)* | 19 | 65,129 | **20.5%** |
| Psychic Systems | 8 | 35,959 | 11.3% |
| Character Generation | 3 | 22,337 | 7.0% |
| Basic Rules | 7 | 18,784 | 5.9% |
| Social Systems | 5 | 14,380 | 4.5% |
| Cybernetic Systems | 5 | 8,411 | 2.6% |
| Physical Systems | 6 | 7,929 | 2.5% |
| GM Toolkit *(provisional)* | 2 | 1,908 | 0.6% |
| **Total** | **64** | **318,136** | |

**The rulebook is a lore document with a rules appendix, not a rules document with lore.** Lore
plus reference apparatus is **65.5%** of the text; every domain system Tomi named as a book sits
between 0.6% and 11.3%. That is not a criticism of the document — it is exactly why #219–#228
exist as work packages, and it is the argument for the split: a reader looking for the combat
rules currently crosses a 143 KB lore span to find seven pages.

### The seven books are adopted unchanged

1. **Basic Rules** · 2. **Character Generation** · 3. **Physical Systems** ·
4. **Cybernetic Systems** · 5. **Psychic Systems** · 6. **Social Systems** · 7. **NoöPunk Lore**

Both of these match the README's seven exactly, in its order, with its names.

### Two provisional parts, and why they are provisional

The README anticipates the first — a GM toolkit *"can be a subsection/book later if it becomes
sufficiently large"* — and its segment table already routes material to a "GM Reference". It
leaves the second open by folding *"references and credits"* into Lore (book 7 lists
*"theory, citations, glossary and detailed catalogs"*).

Both are carried here as **provisional**, flagged in the JSON:

- **GM Toolkit** — narrative layer, escape hatches, missions, encounters, generators (#229,
  #230). Small today (0.6%) precisely because it is the least-written part; naming it now is
  what makes #230's work visible instead of scattering it through Basic and Social.
- **Reference & Provenance** — licensing, source hierarchy, provenance labels, the change
  procedure and ledger, glossary, sources, adapter contract, field catalogs (#231, #232). At
  **20.5%** it is larger than Psychic and Character Generation combined, and it is where the CC
  release is actually decided. Folding it into Lore would put the licensing boundary inside the
  fiction, which is the conflation #231 exists to prevent.

**Both are the author's call.** If they are folded away, the map changes in one place and the
guard follows; nothing else depends on the count being nine.

## Boundary calls worth stating

A reviewer will disagree with at least one of these, so they are recorded rather than buried:

- `core:2 History: The Singularity Is Past` → **Lore**, though it sits in the core half. It is
  setting, not mechanics, and it is the reader's first contact with the world.
- `ledger:12/13/14` → **Physical** (harm, combat, embodiment), joined by `ledger:32`.
  `ledger:52` (equipment list) → **Cybernetic**, because equipment in this setting *is*
  augmentation and software.
- `ledger:40` (reverse-engineering, contact map) → **Psychic**: the contact map is a PSI/NHI
  apparatus, not faction politics. But `ledger:42` → **Lore** and `ledger:43` → **Social**: the
  faction *history* is lore, the faction *mechanics* are social.
- `ledger:22–31` (Concordia actions, persistence, adapter contract, rule-change procedure,
  change ledger, healthy-rulebook definition, governing principle, test-session subset) →
  **Reference** (the subset → **GM Toolkit**): they are contracts *about* the document, and none
  of them is played.
- `core:Contents` → **Reference**: navigation for the whole is not a part of any one.

## Migration protocol

Nothing here is executed. This is the checklist a later, author-approved migration follows,
derived from what currently depends on the document's shape:

1. **Guards that pin the two-document shape.** `RULEBOOK.md` is asserted to be a core book
   numbered `1..8` plus a ledger numbered contiguously, split by the marker. A file move must
   migrate those assertions in the same change, never delete them.
2. **Citation resolution.** `tests/test_theory_sections_survive.py` resolves every `§x.y`
   written *inside* `RULEBOOK.md` against headings *in* `RULEBOOK.md`; modular chapters are
   cited **by link, never by their own §-numbers**. That rule exists because this trap has bitten
   before. A per-book split must keep in-file citations in-file, or convert them in one pass.
3. **The change ledger** (`## 27. Change ledger`) legitimately quotes superseded text, so
   absence guards must stay ledger-aware across a move or they will red on the history itself.
4. **`data/rules/core.json` and the runtimes consume values, not prose** — the split must not
   change any value they read.
5. **Do not renumber.** Book-local numbering would break every existing `§` citation in the
   repository and in closed issues. The README's own note applies: prefer a small root index
   *only after* migrations preserve old anchors, links and all tests.

## What this does not do

- It does not move, cut, reorder or rewrite a single character of `RULEBOOK.md`.
- It does not select a licence and does not touch the release gate (#231).
- It does not authorise rule content. The four domain books are 2.5–11.3% written, and filling
  them is #219–#228's work on the author's approval, not this document's.
- It does not supersede the segmentation snapshots; they remain the byte-lossless staging area.
