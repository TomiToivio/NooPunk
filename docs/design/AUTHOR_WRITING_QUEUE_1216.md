# Author writing queue — consolidated audit (#1216)

> **Author-owned queue. This is a status index, not a manuscript.** Tomi owns every story, canon and
> character decision below. Agents may keep this table accurate and implement technical work only
> after explicit approval. Do not ghostwrite final fiction, invent canon, or create a duplicate when
> an existing file already owns the subject. Last audited: 2026-11-05.

## Status key

| Mark | Meaning |
| --- | --- |
| **READY** | The named file exists; Tomi can edit or approve it. |
| **TEMPLATE** | The named path exists as a human-readable worksheet: headings, prompts, tables and `[fill]` placeholders, but no drafted prose. Tomi writes the content. |
| **EMPTY** | An empty author draft exists at the named path; Tomi writes it. |
| **COVERED** | The requested material already has a canonical home under a different path; use that file, do not duplicate it. |
| **OPEN** | An author decision is still required; no agent should fill it. |

## The queue

| # | Document / decision | Source | Actual path | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Opening campaign series / episode roadmap | #1120 | `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` + `docs/scenarios/CAMPAIGN_ROADMAP_1120.md` | **READY** | The outline owns the four acts; the roadmap owns the episode sequence. Do not create a second roadmap. |
| 2 | First authored playable investigation | #1086, #1120 | `docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md` | **COVERED** | The proposed `docs/campaign/EPISODE_01_FIRST_CASE.md` would duplicate this six-scene case. Do not create it. |
| 3 | First case GM epistemic ledger | #1120 | §6 of `docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md` | **COVERED** | The proposed `docs/campaign/EPISODE_01_EPISTEMIC_LEDGER.md` would split one case's GM material. Keep the ledger with the case unless the author asks for an extract. |
| 4 | Tony German's subjective NHI Crisis memories / lifepath prose | #1123 / #1218 | `docs/campaign/TONY_GERMAN_LIFEPATH.md` | **TEMPLATE** | Author worksheet: character constants, a lifepath overview table with LP-IDs, four memory cards (A–D), a branch outcome register and continuity checks. Prompts and placeholders only; agents do not draft vignettes or choose branches. |
| 5 | Tony's opening nightmare, Sörnäinen morning, equipment ritual and Ratakatu arrival | #1123 / #1218 | `docs/campaign/EPISODE_00_FIRST_DAY.md` | **TEMPLATE** | Author-only scene worksheet: six scene rows (E00-S01…S06), a copyable scene-writing card, the nightmare card with two plausible interpretations, issued-kit prompts and playability checks. The mechanical scaffold is #1217, not the fiction. |
| 6 | Romppainen, Laura Wendt and specialist party profiles | #1086 | `docs/design/ROMPPAINEN_PARTY_1038.md` | **READY / OPEN** | Existing party document. The D71 companion command/autonomy decision is still open and must be resolved there before agent implementation. |
| 7 | Greater Helsinki setting, four jurisdictions, zones and exclusion areas | #1121 | `design/GREATER_HELSINKI_2045.md` | **READY** | Canonical narrative register; `data/world/greater_helsinki_1121.json` is the stable-ID lookup. Cross-reference `design/HELSINKI_CITY.md` and `docs/world/EUROPOL_HELSINKI_1114.md`; do not duplicate. |
| 8 | Galactic Machine War and three prohibitions | #1122 | `design/GALACTIC_MACHINE_WAR.md` | **READY** | Canonical cosmology; synchronise approved content with `rulebook/15_XENOPOLITICS.md` and `docs/world/NHI_FACTIONS_922.md` only after author approval. Keep public/classified/disputed separate. |
| 9 | Crisis survival, catastrophic normality, narrative modes and Nordic Ghost Rocket contact | #1168 | `docs/proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md` | **COVERED** | The proposed `docs/design/NORDIC_CRISIS_AND_NARRATIVE_MODES_1168.md` would duplicate the canonical memo. Use the memo; do not create the proposed path. |
| 10 | Tone / voice and cross-media scene reference conventions | #1086, #1168 | `docs/design/LITERARY_CROSS_MEDIA_1037.md` + `docs/design/ISSUE_1037_DOCUMENT_REGISTER.md` | **READY** | Existing documents. Update only after the narrative modes are approved; keep the document register in sync. |
| 11 | Dream fragments and scripted awakening ambiguity | #1168 / #1152 | `docs/campaign/DREAMS.md` | **READY** | Existing worksheet; personal unconscious vs PSI/noetic/time-space interpretations remain deliberately unresolved. |

| 12 | Player briefing — the one page read before the first scene | #1216 acceptance | `docs/campaign/PLAYER_BRIEFING.md` | **TEMPLATE** | Nine prompted sections and a list of what the briefing must not contain. This is the document that makes "playable without a universe encyclopedia" checkable. |
| 13 | Author sign-off ledger | #1216 acceptance | `docs/design/AUTHOR_APPROVALS_1216.md` | **READY** | Agent-maintained table: one row per document, status AWAITING / APPROVED / CHANGES / BLOCKED, with the date of the decision. Updates in the same PR that acts on the document. |

## Order

1. **Tony's lifepath and opening scene** — fill the two empty author drafts; decide the lifepath choices.
2. **Approve Case 01** and the rate of revelation; keep the GM ledger with the case.
3. **Expand the episode arc and party bios** only where needed to make the next case playable.
4. **Promote the setting/cosmology/memo documents** only after Tomi has reviewed them; do not overwrite conflicting historical versions silently.

## Template convention

A **TEMPLATE** row is a page Tomi can write in, not a page with placeholder prose. It contains:

- `##` section headings, one per beat or question;
- a prompt for each section — a blockquote marked *not prose*, or a labelled `[fill]` field;
- tables whose cells are `[fill]` or `[AUTHOR TO WRITE]` rather than answers;
- optionally the `<!-- Tomi writes below. -->` marker.

The guards in `tests/test_author_writing_queue_1216.py` and `tests/test_writing_templates_1216.py`
read this convention: a body line without a placeholder token, and not part of a table or a
checklist, means an agent wrote prose into an author draft.

## Rules for agents

- **Do not write final fiction.** An empty draft is a place for Tomi, not a prompt for an agent to fill.
- **Do not create a duplicate target.** If the queue names a proposed path but an existing file owns
  the subject, update this table and link the owner. The canonical examples are rows 2, 3 and 9.
- **Technical work only after approval.** A tracker item is not an implementation ticket; CWN is
  immutable, and any tabletop/Python parity work needs its own explicit instruction.
- **Keep canon decisions visible.** If a document contains both established facts and disputed or
  classified claims, label them; never promote a rumour to canon while "clarifying".
- **Record what changed.** When a file moves or is approved, update this table and the document
  register in the same PR.

## Related

- Author workflow: [`design/README.md`](../../design/README.md).
- Document ownership: [`docs/DOCUMENT_REGISTER.md`](../DOCUMENT_REGISTER.md).
- Campaign assets: [`docs/campaign/README.md`](../campaign/README.md).
- Existing case: [`docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md`](../scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md).
- Roadmap: [`docs/scenarios/CAMPAIGN_ROADMAP_1120.md`](../scenarios/CAMPAIGN_ROADMAP_1120.md).
- Author drafts: [`TONY_GERMAN_LIFEPATH.md`](../campaign/TONY_GERMAN_LIFEPATH.md), [`EPISODE_00_FIRST_DAY.md`](../campaign/EPISODE_00_FIRST_DAY.md), [`PLAYER_BRIEFING.md`](../campaign/PLAYER_BRIEFING.md).
- Sign-off record: [`AUTHOR_APPROVALS_1216.md`](AUTHOR_APPROVALS_1216.md).
