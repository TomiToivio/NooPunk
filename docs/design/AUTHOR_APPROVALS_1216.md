# Author approvals — the queue's sign-off ledger (#1216)

> **Agent-maintained index; Tomi's decisions.** This page exists so that "Tomi has reviewed the canon"
> is a recorded fact with a date rather than an assumption in a PR description. It adds no fiction, no
> canon and no rules. When a document is approved, changed or rejected, the row is updated in the same
> PR that touches the document.
>
> The documents themselves live where the [writing queue](AUTHOR_WRITING_QUEUE_1216.md) says they do;
> this ledger only records the decision.

## Status key

| Mark | Meaning |
| --- | --- |
| **AWAITING** | Written or templated, waiting for the author to read it. |
| **APPROVED** | Tomi has read it and approved it as canon or as the working version. |
| **CHANGES** | Read, with requested changes; the document is not canon until they land. |
| **BLOCKED** | Cannot be reviewed yet because a decision it depends on is open. |

## The ledger

| Document | What the author is deciding | Status | Date | Note |
| --- | --- | --- | --- | --- |
| [`docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md`](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) + [`CAMPAIGN_ROADMAP_1120.md`](../scenarios/CAMPAIGN_ROADMAP_1120.md) | The four-act shape and the episode sequence | AWAITING | — | Act III was a proposal in #1132 |
| [`docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md`](../scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md) | The first playable case, its rate of revelation, and the GM ledger in §6 | AWAITING | — | Ledger stays with the case; no separate file |
| [`docs/campaign/TONY_GERMAN_LIFEPATH.md`](../campaign/TONY_GERMAN_LIFEPATH.md) | The branchable history and what each branch grants | AWAITING | — | Template only; Tomi writes |
| [`docs/campaign/EPISODE_00_FIRST_DAY.md`](../campaign/EPISODE_00_FIRST_DAY.md) | The opening script from nightmare to Romppainen | AWAITING | — | Template only; Tomi writes |
| [`docs/campaign/PLAYER_BRIEFING.md`](../campaign/PLAYER_BRIEFING.md) | What a player is told before the first scene | AWAITING | — | Template only; the "no encyclopedia" criterion |
| [`docs/design/ROMPPAINEN_PARTY_1038.md`](ROMPPAINEN_PARTY_1038.md) | Party profiles and **D71** companion command/autonomy | BLOCKED | — | D71 must be decided before agent implementation |
| [`design/GREATER_HELSINKI_2045.md`](../../design/GREATER_HELSINKI_2045.md) | The four jurisdictions, zones and exclusion areas | AWAITING | — | Cross-reference, do not duplicate |
| [`design/GALACTIC_MACHINE_WAR.md`](../../design/GALACTIC_MACHINE_WAR.md) | The cosmology and the three prohibitions | AWAITING | — | Public / classified / disputed kept separate |
| [`docs/proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md`](../proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md) | The narrative modes and the Nordic contact model | AWAITING | — | Promotion into rulebook/history only after approval |
| [`docs/design/LITERARY_CROSS_MEDIA_1037.md`](LITERARY_CROSS_MEDIA_1037.md) + [`ISSUE_1037_DOCUMENT_REGISTER.md`](ISSUE_1037_DOCUMENT_REGISTER.md) | Tone, satire, and how prose links to scenes | AWAITING | — | Keep the document register in sync |
| [`docs/campaign/DREAMS.md`](../campaign/DREAMS.md) | Which dream material is usable, and what stays unresolved | AWAITING | — | Personal unconscious vs PSI stays open |

## How a row changes

1. The author reads the document and says what they want, in the issue or in review.
2. The same PR that acts on it updates **Status**, **Date** and **Note** here.
3. **APPROVED** means the document's own banner may say so. It does not mean agents may implement the
   mechanical work: that needs its own instruction, and CWN stays immutable either way.

## Related

- Queue: [`AUTHOR_WRITING_QUEUE_1216.md`](AUTHOR_WRITING_QUEUE_1216.md).
- Ownership: [`docs/DOCUMENT_REGISTER.md`](../DOCUMENT_REGISTER.md).
- Author workflow: [`design/README.md`](../../design/README.md).
