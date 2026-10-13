# Author decision queue — what is blocking the open NoöPunk issues

**What this file is.** A consolidation, not a design. Every item is condensed from the open issue
that carries it (each row links there). Nothing here is canon, a mechanic, a name or a ruling: each
row is a **question only the author can answer**. Siblings have already written per-issue acceptance
walk-throughs — this file exists so the answers can be given in **one pass**, after which each
answered row can be verified, recorded and closed.

**Board status (2026-10-13).** Nine issues open. None is autonomously closeable: every remaining
blocker is either an author ruling (below) or a sibling's in-flight work (#325's map specification,
and the RPG boundary seam, where two fix PRs are open). Two issues (#323, #338) are open *because they were reopened
deliberately* to avoid closing on a `Closes` line while their rules remain unapproved.

## The queue

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D1 | The twelve leader seats exist as **declared blanks** (`ukweli_leaders.json`, *"TODO: requires author specification"*). Name them, authorise a proposal, or waive the criterion for the MVP. | #322 criterion 2 | *names* / *propose them* / *defer* |
| D2 | Are the M4/M5 mechanics (organisational-form transitions, rival-faction AI, win/loss) in scope for the MVP or a later issue? | #322 criteria 3, 5 | *in* / *later issue* |
| D3 | Approve rules stages B–E — bounded portfolio bonus, triggered character event, event resolution. `RULEBOOK.md` still says **NO RULES APPROVED**. | #323 | *approve* / *out of scope* |
| D4 | The eleven global parties' formal names and colloquial labels; self-name versus hostile exonym. | #328 | *ratify as drafted* / *rename* |
| D5 | MJ-12 continuity: when it starts, what it controls, why it qualifies as a Breakaway Civilization; human-led or not; internal factions; relation to disclosure, the Confederacy, Orion, the Swarm. | #328 | *decide* |
| D6 | The ASI swarm's origin/objectives/autonomy; whether any human network is voluntary or coerced. | #328 | *decide* |
| D7 | Confirm the three Ukweli party ↔ global-current affinities as **starting tendencies**, not fixed memberships. | #328 | *yes* / *no* |
| D8 | Reconcile the legacy UN party records with the established UN world government and eleven parties. | #328 | *decide* |
| D9 | #338's remaining scope — narrative encounters, campaign frame, political simulation — in or out? | #338 | *in* / *close as satisfied* |
| D10 | PSI vocabulary and limits, optional PSI TAGs, the encounter prototype. These sit inside `AGENTS.md` §4's verbatim reservation of *"psionic powers or psionic mechanics"* and `rulebook/17` §17.9. | #345 criteria 1, 2 | *approve* / *refuse* |
| D11 | Who **owns** the Archaic Revival definition — it appears in #344, #345 and #346, so it should be defined once. | #345, #346 | *pick one issue* |
| D12 | Approve the five ideological axes, the typed faction/character TAG vocabulary and the three genre pillars. | #346 | *approve* |
| D13 | Confirm **Cosmist International** (Autonomist Marxist influenced by Russian Cosmism) as the default playable faction, with the StO↔communism / StS↔capitalism reading kept explicitly fictional. | #346 | *confirm* |
| D14 | The cultural axis: is it liberal/conservative, or is a distinct authoritarian/libertarian value needed too? | #346 | *one* / *both* |

Two carry-overs from already-closed issues, recorded so they are not lost: the state's formal name
(#324 §4.1), and **ULP** versus **LFP** as the third-party name across `#issue` / `#data` / `#325` /
`#326`.

## Issues with no decision pending

- **#325** — a sibling claimed the map specification (deliverable 3) on 2026-10-13; the setting bible
  is merged. Ratification of its PROPOSAL items (the four conflicts as options, Freedom Colony's
  legal autonomy) will be a future row.
- **#282, #309** — umbrella issues: open by design, no decision needed.

## After an answer

Each answered row above becomes: a criterion check against `main` → an acceptance record in
`docs/design/ISSUE_<n>_ACCEPTANCE.md` → PR → merge → close. Rows answered *"defer"* or *"out of
scope"* close the issue just as cleanly, because the record then states the deferral rather than
pretending the item was met.

— Ai (愛)
