# `rulebook-pre-narrative-2026-10` — pre-narrative rulebook archive

This directory is the discoverable entry point to the **complete pre-narrative NoöPunk rulebook
corpus**. It documents the immutable annotated tag **`rulebook-pre-narrative-2026-10`**, which marks the pre-narrative
baseline (published before this archive, covering the full legacy corpus).

- **[MANIFEST.md](MANIFEST.md)** — every distinct legacy source with byte size and sha256, and where
  its preserved copy lives. Nothing was deleted; every file is still at its original path.
- **[MIGRATION_MAP.md](MIGRATION_MAP.md)** — section-by-section: each legacy unit's destination (new
  chapter, deferred supplement, lore/reference, or historical archive), plus anything awaiting author
  review.
- **[manifest.json](manifest.json)** — the machine-readable inventory, verified by
  `tests/test_issue265_rulebook_archive.py`.

## Retrieval

```sh
git show rulebook-pre-narrative-2026-10                 # the pre-narrative baseline
python3 tools/build_rulebook_archive.py --check   # prove the hashes still match
```

## Relationship to #243

Issue #243 made a *lossless inventory and exact snapshot* of the root `RULEBOOK.md` and
`rulebook_parts/`, and deliberately did **not** reconcile them
(`docs/rulebook_consolidation/inventory.json`, `rulebook/source_snapshots/`). This archive **extends**
that work to the rest of the corpus and adds the migration map. It does not duplicate or undo #243.

## Scope

Preservation and mapping only. It changes no rule, deletes nothing, and approves no dice formula.
