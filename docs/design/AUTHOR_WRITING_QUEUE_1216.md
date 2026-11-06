# Author writing queue — consolidated audit (#1216)

> **Author-owned queue. This is a status index, not a manuscript.** Tomi owns every story, canon and
> character decision below. Agents may keep this table accurate and implement technical work only
> after explicit approval. Do not ghostwrite final fiction, invent canon, or create a duplicate when
> an existing file already owns the subject. Last audited: 2026-11-06.

## Status key

| Mark | Meaning |
| --- | --- |
| **READY** | The named file exists; Tomi can edit or approve it. |
| **TEMPLATE** | An author-owned draft with structured prompts exists; final prose is still unwritten. |
| **COVERED** | The requested material already has a canonical home under a different path; use that file, do not duplicate it. |
| **OPEN** | An author decision is still required; no agent should fill it. |

## The queue

| # | Document / decision | Source | Actual path | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Opening campaign series / episode roadmap | #1120 | `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` + `docs/scenarios/CAMPAIGN_ROADMAP_1120.md` | **READY** | The outline owns the four acts; the roadmap owns the episode sequence. Do not create a second roadmap. |
| 2 | First authored playable investigation | #1086, #1120 | `docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md` | **COVERED** | The proposed `docs/campaign/EPISODE_01_FIRST_CASE.md` would duplicate this six-scene case. Do not create it. |
| 3 | First case GM epistemic ledger | #1120 | §6 of `docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md` | **COVERED** | The proposed `docs/campaign/EPISODE_01_EPISTEMIC_LEDGER.md` would split one case's GM material. Keep the ledger with the case unless the author asks for an extract. |
| 4 | Tony German's subjective NHI Crisis memories / lifepath prose | #1123 / #1218 / #1236 | `docs/campaign/TONY_GERMAN_LIFEPATH.md` | **TEMPLATE** | Branching memory, choice, subjective-evidence and character-tag prompts added; fiction/choices remain Tomi's. See `docs/design/PROPOSAL_TONY_GERMAN_LIFEPATH_1236.md`. |
| 5 | Tony's opening nightmare, Sörnäinen morning, equipment ritual and Ratakatu arrival | #1123 / #1218 / #1217 | `docs/campaign/EPISODE_00_FIRST_DAY.md` | **TEMPLATE** | Scene cards, dream, equipment, NPC and handoff prompts added. Tomi writes dialogue; #1217 owns mechanical scaffold. |
| 6 | Romppainen, Laura Wendt and specialist party profiles | #1086 | `docs/design/ROMPPAINEN_PARTY_1038.md` | **READY / OPEN** | Existing party document; also review `docs/design/PROPOSAL_EUROPOL_NPC_DOSSIERS_1236.md` for Salla, Laura and Romppainen. The D71 companion command/autonomy decision is still open and must be resolved there before agent implementation. |
| 7 | Greater Helsinki setting, four jurisdictions, zones and exclusion areas | #1121 | `design/GREATER_HELSINKI_2045.md` | **READY** | Canonical narrative register; `data/world/greater_helsinki_1121.json` is the stable-ID lookup. Cross-reference `design/HELSINKI_CITY.md` and `docs/world/EUROPOL_HELSINKI_1114.md`; do not duplicate. |
| 8 | Galactic Machine War and three prohibitions | #1122 | `design/GALACTIC_MACHINE_WAR.md` | **READY** | Canonical cosmology; synchronise approved content with `rulebook/15_XENOPOLITICS.md` and `docs/world/NHI_FACTIONS_922.md` only after author approval. Keep public/classified/disputed separate. |
| 9 | Crisis survival, catastrophic normality, narrative modes and Nordic Ghost Rocket contact | #1168 | `docs/proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md` | **COVERED** | The proposed `docs/design/NORDIC_CRISIS_AND_NARRATIVE_MODES_1168.md` would duplicate the canonical memo. Use the memo; do not create the proposed path. |
| 10 | Tone / voice and cross-media scene reference conventions | #1086, #1168 | `docs/design/LITERARY_CROSS_MEDIA_1037.md` + `docs/design/ISSUE_1037_DOCUMENT_REGISTER.md` | **READY** | Existing documents. Update only after the narrative modes are approved; keep the document register in sync. |
| 11 | Dream fragments and scripted awakening ambiguity | #1168 / #1152 | `docs/campaign/DREAMS.md` | **READY** | Existing worksheet; personal unconscious vs PSI/noetic/time-space interpretations remain deliberately unresolved. |

## Order

1. **Tony's lifepath and opening scene** — use the two structured author templates to write original prose and decide the lifepath choices.
2. **Approve Case 01** and the rate of revelation; keep the GM ledger with the case.
3. **Expand the episode arc and party bios** only where needed to make the next case playable.
4. **Promote the setting/cosmology/memo documents** only after Tomi has reviewed them; do not overwrite conflicting historical versions silently.

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
- Author drafts: [`TONY_GERMAN_LIFEPATH.md`](../campaign/TONY_GERMAN_LIFEPATH.md), [`EPISODE_00_FIRST_DAY.md`](../campaign/EPISODE_00_FIRST_DAY.md).
- Review prompts for the other nine entries: [`AUTHOR_REVIEW_WORKSHEETS_1216.md`](AUTHOR_REVIEW_WORKSHEETS_1216.md).

## 2026-11-06 audit: coverage and template readiness

All **11 original queue items** map to existing canonical writing destinations. The proposed separate first-case, epistemic-ledger and Nordic memo files are **not missing**: they would duplicate canonical material. The two author draft files (rows 4–5) now contain human-readable scene/choice templates; the other nine have dedicated review prompts in `AUTHOR_REVIEW_WORKSHEETS_1216.md`, using links to their owning documents. **No final manuscript or author approval is implied.**

**Additional cross-document review needs (not duplicate manuscripts):** Tony/Europol continuity against outdated unnamed/female/UNSA-first framing; legal Grunt/Geek/Freak build choices; Salla/Laura/Romppainen dossiers and D71 autonomy; precise Case 01 handoff; fiction versus official/disputed/secret source tiers. Keep these as author decisions until approved.

