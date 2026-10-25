# Without Number rights matrix (#569)

Audit date: 2026-10-25. This is a reuse *boundary*, not a licence grant for NoöPunk itself. No protected third-party expression has been intentionally imported as part of this work. A complete repository-wide similarity audit remains outstanding.

| Document | Evidence and terms | Permitted for this project | Excluded / not established |
| --- | --- | --- | --- |
| Cities Without Number **SRD** | CC0 dedication in the published *Systems Reference Document v1.0* introduction; source: https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/452790-sample.pdf ; mirror: https://cwn.quadrifons.com/ | Reuse the identified SRD rules and text | Deluxe/full-book text outside SRD, images, unique settings and characters |
| Worlds Without Number **SRD** | Explicit CC0 in SRD introduction: https://rpg.blulaktuko.net/wwn/srd/1-an-introduction.html ; publisher SRD: https://www.drivethrurpg.com/product/473939/Worlds-Without-Number-System-Reference-Document | Content within the SRD under CC0 | Latter Earth setting, full-book creative material, art |
| Stars Without Number **Revised** | A free edition exists, but no verified *applicable SRD text licence* established in this audit | Independently written procedural comparisons and unprotected mechanics | **No verbatim text, tables, art, setting or implied CC0 permission** pending verification |
| Ashes Without Number **Free Version** | No independently verified CC0 SRD located as of audit date | Original comparisons of high-level mechanics | **No verbatim copying or assumed CC0** from the free edition |

CC0 applies to the *specified SRD*, not to every publication bearing the game's name. Mechanics as abstract methods and independently developed original implementations are distinguishable from the source's copyrightable expression. Do not copy snippets from deluxe editions. Trademark or implied endorsement rights are not conferred by CC0.

## Import exclusion record

- **Excluded from this change:** all full-book prose, images, setting-specific factions, characters, and text from the SWN/AWN free or deluxe books.
- **Imported in this change:** no third-party content. Comparison names and links only.
- **Existing-tree audit:** the existing audit in `docs/sources/GAME_SYSTEM_RIGHTS.md` recorded no imported game-system expression; this follow-up did *not* independently prove a full-tree clean bill. Existing `legacy/` and `archive/` material is quarantined per release policy; see `tools/release_packaging_guard.py`.
- **Enforcement:** CI's existing public-release guard requires a manifest and a resolved author licence. For future Without Number imports, add exact file paths and source-document provenance to this matrix, and require human review before admitting text. A name/keyword ban is *not* an adequate copyright detector: it would falsely reject legitimate attribution and miss paraphrased copying.

Review/reopen if publishers change editions or publish an AWN/SWN SRD. No author decision on NoöPunk's publication licence is implied.
