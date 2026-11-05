# Author writing queue — consolidated tracker (#1216)

> **Author-owned queue. This is a status index, not a manuscript.** Tomi owns every story, canon and
> character decision below. Agents may keep this table accurate, create empty author drafts where a
> target does not exist, and implement technical work only after explicit approval. Do not ghostwrite
> final fiction, invent canon, or create a duplicate when an existing file already owns the subject.

## Status key

| Mark | Meaning |
| --- | --- |
| **READY** | The named file exists; Tomi can edit or approve it. |
| **EMPTY** | An empty author draft exists at the named path; Tomi writes it. |
| **COVERED** | The requested material already has a canonical home under a different path; use that file, do not duplicate it. |
| **OPEN** | An author decision is still required; no agent should fill it. |

## The queue

| # | Document / decision | Source | Target path | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Opening campaign series / episode roadmap | #1120 | `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` | **READY** | Existing four-act outline. The episode-level sequence is **COVERED** by `docs/scenarios/CAMPAIGN_ROADMAP_1120.md`; do not create a second roadmap. |
| 2 | First authored playable investigation | #1086, #1120 | `docs/campaign/EPISODE_01_FIRST_CASE.md` (proposed) | **COVERED** | Canonical manuscript is `docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md` (six scenes, CWN checks, clue table). Do **not** create `EPISODE_01_FIRST_CASE.md`; it would duplicate the case. |
| 3 | First case GM epistemic ledger | #1120 | `docs/campaign/EPISODE_01_EPISTEMIC_LEDGER.md` (proposed) | **COVERED** | The ledger is §6 of `CASE_01_THE_TUESDAY_COMPLAINT.md`. A separate file would split one case's GM material; keep it in the case unless the author asks for an extract. |
| 4 | Tony German's subjective NHI Crisis memories / lifepath prose | #1123 | `docs/campaign/TONY_GERMAN_LIFEPATH.md` | **EMPTY** | Empty author draft created; only a title and banner. Tomi writes the memories and choices. |
| 5 | Tony's opening nightmare, Sörnäinen morning, equipment ritual and Ratakatu arrival | #1123 | `docs/campaign/EPISODE_00_FIRST_DAY.md` | **EMPTY** | Empty author draft created; scripted fiction belongs to Tomi. Coordinate with the separate character-generation issue. |
| 6 | Romppainen, Laura Wendt and specialist party profiles | #1086 | `docs/design/ROMPPAINEN_PARTY_1038.md` | **READY / OPEN** | Existing party document. The D71 companion command/autonomy decision is still open and must be resolved there before agent implementation. |
| 7 | Greater Helsinki setting, four jurisdictions, zones and exclusion areas | #1121 | `design/GREATER_HELSINKI_2045.md` | **READY** | Canonical narrative register; `data/world/greater_helsinki_1121.json` is the stable-ID lookup. Cross-reference `design/HELSINKI_CITY.md` and `docs/world/EUROPOL_HELSINKI_1114.md`; do not duplicate. |
| 8 | Galactic Machine War and three prohibitions | #1122 | `design/GALACTIC_MACHINE_WAR.md` | **READY** | Canonical cosmology; synchronise approved content with `rulebook/15_XENOPOLITICS.md` and `docs/world/NHI_FACTIONS_922.md` only after author approval. Keep public/classified/disputed separate. |
| 9 | Crisis survival, catastrophic normality, narrative modes and Nordic Ghost Rocket contact | #1168 | `docs/design/NORDIC_CRISIS_AND_NARRATIVE_MODES_1168.md` (proposed) | **COVERED** | Existing canonical memo: `docs/proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md`. Use it; do not create the proposed duplicate. |
| 10 | Tone / voice and cross-media scene reference conventions | #1086, #1168 | `docs/design/LITERARY_CROSS_MEDIA_1037.md` + `docs/design/ISSUE_1037_DOCUMENT_REGISTER.md` | **READY** | Existing documents. Update only after the narrative modes are approved; keep the document register in sync. |
| 11 | Dream fragments and scripted awakening ambiguity | #1168 / #1152 | `docs/campaign/DREAMS.md` | **READY** | Existing worksheet; personal unconscious vs PSI/noetic/time-space interpretations remain deliberately unresolved. |

## Order

1. **Tony's lifepath and opening scene** — fill the two empty drafts; decide the lifepath choices.
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
