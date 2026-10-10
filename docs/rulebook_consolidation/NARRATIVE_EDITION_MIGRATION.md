# Narrative edition migration register (#265)

**Preservation checkpoint:** [archive/pre-265-full-rulebook-2026-10-10](https://github.com/TomiToivio/NooPunk/tree/archive/pre-265-full-rulebook-2026-10-10). This branch is the **complete Git tree** captured before #265 edits: original files, histories and accompanying data. Do not delete or force-push this reference. Historical content is valued, and the new edition will reuse it selectively.

**New introductory rulebook:** [rulebook/NEW_EDITION.md](../../rulebook/NEW_EDITION.md). Draft canonical candidate, pending synchronization with older rulebook infrastructure and review. The legacy split/segment tooling and tests continue to describe the archival edition until migrated.

| Historical location / assets | Destination / disposition |
|---|---|
| Root `RULEBOOK.md` and generated `rulebook/parts/` / `rulebook/00_INDEX.md` | Archived intact in checkpoint; new readable introduction in `rulebook/NEW_EDITION.md`. Generation/guard migration remains to do. |
| `rulebook_parts/`, `docs/rulebook_segments/`, `source_snapshots/` where present | Preserve in historical branch and assess unique content before consolidating under active rulebook. |
| `data/rules/skills.json` and existing skills crosswalk | Retain source and catalogue; audit/translate to narrative-edition examples under #263, no silent pruning. |
| Character creation, academy and lifepath material (#144, #158, #218) | Reuse for chapter on UNSA Academy characters; numeric choices unresolved. |
| Social / affect and narrative resources (#220, #229) | Reuse for relationships, NPC autonomy and Psyche; new narrative-layer modeling pending. |
| Investigation templates and scenarios (#141, #226, #230) | Reuse case structure; update opening premise only after reconciliation. |
| Cyber, PSI, Astral and cross-domain content (#221–#225) | Reuse lore and bounded access concepts; reconcile three-reality vocabulary and edition procedures. |
| Tactical conflict, detailed gear and old numeric systems | Preserve in archive and mark as possible later-edition research; not active first-edition requirements. |
| Tests, scripts, Godot, Concordia and data models | Preserve; adjust deliberately after chosen gameplay procedures are approved. |

## Safe next edits

1. Compare existing source files and #243 consolidation ledger for one-to-one coverage; append any previously unlisted artifacts.
2. Review this draft with #262–264 guidance. Do not copy proprietary game text or mechanics wholesale.
3. Choose original outcome-resolution and progression procedures via author review.
4. Migrate active root `RULEBOOK.md`, index, generated parts, parsers and CI **together**, without leaving incompatible active claims. Until then the new edition is an explicitly designated **draft**.
5. Playtest an UNSA investigation in which PC/party relationships and Psyche produce persistent consequences, then implement auditable state across tabletop/Godot/Concordia.

**No deletion or automatic rewriting is implied.**