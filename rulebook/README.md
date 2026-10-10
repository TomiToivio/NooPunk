> **New narrative-first rulebook (issue #265):** [NEW_EDITION.md](NEW_EDITION.md) starts with FIT / REF / INT / SOC / PSY / CYB and introduces streamlined tabletop play, Social relationships and Psyche. The previous edition is preserved completely in [the archival branch](https://github.com/TomiToivio/NooPunk/tree/archive/pre-265-full-rulebook-2026-10-10); the [migration register](../docs/rulebook_consolidation/NARRATIVE_EDITION_MIGRATION.md) tracks the transition. Existing generated parts and tests remain available until the source-of-truth switch can be made as one consistent change.

# NoöPunk rulebook: canonical editing and preservation

The **only editable rulebook** lives under `rulebook/`, with [00_INDEX.md](00_INDEX.md) as its table of contents. Never treat root `RULEBOOK.md`, `rulebook_parts/`, `rulebook/parts/` or `source_snapshots/` as an independent source of new canonical decisions without checking existing project rules and approvals. Historical duplicate sources are preserved during issue [#243](https://github.com/TomiToivio/NooPunk/issues/243).

Before editing, inspect `AGENTS.md`, related open issues/PRs and the current branch head. For every change to existing rules or lore, compare all overlapping sources via [the reconciliation ledger](../docs/rulebook_consolidation/LEDGER.md) and [inventory](../docs/rulebook_consolidation/inventory.json); update the ledger with a source-to-destination trace. Treat small examples, tables, headings, footnotes, TODOs and attribution as substantive. Never silently delete or replace a longer section with a shorter one. Exact duplicates require hash/content verification; near-duplicates require paragraph-level comparison. Keep unresolved contradictions explicitly labelled, do not resolve them by improvising new lore or mechanics. Preserve the six STATs and cross-platform parity as established by approved project decisions.

For concurrent work, announce intended files on issue #243, avoid overlapping files, push small commits, review combined diffs, and never force-push shared branches or resolve a chapter conflict with blanket 'ours' or 'theirs'. Before claiming completion, verify all section mappings, internal anchors, links, code/data consumers, tests, licensing and a human-readable diff against every baseline source. A file present in `source_snapshots/` is **preserved**, not **reconciled**. The snapshots are read-only review material and should not be edited for gameplay changes.

---

## Narrative-first edition (issue #265) — current entry point

The active rulebook now opens with **[00_START_HERE.md](00_START_HERE.md)**, the entry point for the
narrative-first edition directed by [#262](https://github.com/TomiToivio/NooPunk/issues/262). It
begins with the six approved attributes **FIT / REF / INT / SOC / PSY / CYB** and marks the
resolution formula **undecided**.

**Supersession is explicit, and nothing has been deleted.** Every legacy section and chapter has a
recorded destination in the migration map
(`archive/rulebook-pre-narrative-2026-10/MIGRATION_MAP.md`): a new chapter, a deferred advanced
supplement, lore/reference, or the historical archive. Old numerical and tactical rules are marked
**HISTORICAL** — readable, but never quietly reinstated as canon.

The complete pre-narrative corpus is preserved under
[`archive/rulebook-pre-narrative-2026-10/`](../archive/rulebook-pre-narrative-2026-10/README.md)
(manifest with hashes) and by the immutable annotated tag **`rulebook-pre-narrative-2026-10`**. That
extends [#243](https://github.com/TomiToivio/NooPunk/issues/243)'s lossless inventory and snapshot;
it does not undo it.

Rules for editing the narrative-first edition:

- The legacy chapters below remain **readable reference** until their content is carried into a new
  chapter under the migration map. Do not treat a legacy number as current canon.
- `RULEBOOK.md` is the pre-narrative canonical text. It is **preserved and archived**, and replacing
  it — together with the tests that read it — is a deliberate, reviewed change, not a bulk rewrite.
- Retain `data/rules/skills.json` unchanged pending the [#263](https://github.com/TomiToivio/NooPunk/issues/263) crosswalk.
- Regenerate and verify the archive with `python3 tools/build_rulebook_archive.py` and
  `python3 tools/build_rulebook_archive.py --check`.
