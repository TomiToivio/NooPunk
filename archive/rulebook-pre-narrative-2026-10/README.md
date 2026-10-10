# Architecture snapshot: the pre-narrative rulebook

**Immutable archive reference for issue [#265](https://github.com/TomiToivio/NooPunk/issues/265).**

`main` is starting a clean, simplified, narrative-first rulebook. This directory exists so the
previous rules remain **completely retrievable** while that happens — without copying 2.3 MB of
text into the archive, and without two live sources of truth.

## How to retrieve anything

```bash
git fetch --tags
git show rulebook-pre-narrative-2026-10:RULEBOOK.md            # the canonical old text
git ls-tree -r --name-only rulebook-pre-narrative-2026-10      # everything in the corpus
```

The tag is **annotated**, not a moving branch, and points at the last commit before the
migration. Nothing in it will change.

## What is here

| File | Purpose |
| --- | --- |
| `MANIFEST.json` | file-by-file inventory: path, size, sha256, classification, and the commit the snapshot was taken from |
| `MIGRATION_MAP.md` | every old section and reference chapter, with its single destination |

Both are **generated** (`tools/issue265_archive_manifest.py`,
`tools/issue265_migration_map.py`) and guarded, so neither can silently drift from the tree.

## What the corpus actually was

The inventory's main finding is that four things looked like "the rulebook" and only two of them
are real content:

| View | Files | Overlap with `RULEBOOK.md` | Meaning |
| --- | ---: | --- | --- |
| `RULEBOOK.md` | 1 | — | canonical text, 63 numbered sections in **two** runs (core 1–9, appendix 1–54) |
| `rulebook/*.md` | 20 | **0–2%** | **distinct** reference chapters — prose found nowhere in `RULEBOOK.md` |
| `rulebook_parts/*.md` | 9 | 93–100% | generated view — regenerable |
| `docs/rulebook_segments/*.md` | 9 | 100% | generated view — regenerable |

Two consequences worth stating plainly, because #265 warns against mistaking a partial duplicate
for the whole corpus:

1. **The whole corpus is `RULEBOOK.md` plus the 20 distinct chapters** — 23 distinct files in
   total. Anyone who archives only `RULEBOOK.md`, or only the generated views, archives a part.
2. **Most of the 54-section appendix was never player rules.** It is process, provenance and lore.
   Routing it to the engineering or lore tracks is not discarding rules that existed.

## What this archive does not do

It does not delete, move or rewrite any rulebook file. It does not choose a dice formula. It does
not reinstate any old numeric or tactical rule. It contains no copy of the rulebook text — the
tag is the retrieval path, and a guard verifies every manifest hash against it.
