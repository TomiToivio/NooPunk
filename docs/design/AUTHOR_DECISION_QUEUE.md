# Author decision queue — what is blocking the open NoöPunk issues

**What this file is.** A consolidation, not a design. Every item is condensed from the open issue
that carries it (each row links there). Nothing here is canon, a mechanic, a name or a ruling: each
row is a **question only the author can answer**. Answering one turns it into a criterion check, an
acceptance record, a PR and a close.

**Board status (2026-10-13, updated).** Five issues open: **#309** (umbrella), **#322**, **#323**,
**#328**, **#338**. Since the first version of this queue, **#325**, **#345**, **#346** and the
umbrella **#282** closed; their rows are retired at the bottom, kept only so the history is legible.

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

Two carry-overs from closed issues, recorded so they are not lost: the state's formal name
(#324 §4.1), and **ULP** versus **LFP** as the third-party name across `#issue` / `#data` / `#325` /
`#326`.

## Retired rows (their issue closed)

- **D10–D11, PSI vocabulary and the Archaic Revival owner** — *#345 closed*. If the PSI rules were
  waived rather than approved, that decision now lives in the closure record, not here.
- **D12–D14, faction creation (the five axes, Cosmist International, the cultural axis)** — *#346
  closed*. The axes and TAG vocabulary are on `main`; the cultural-axis question is retired with the
  issue.
- **#325's ratification rows** (the four conflicts as options, Freedom Colony's legal autonomy) —
  *#325 closed* after the map specification landed.
- **#309, #282** — umbrellas: open or closed by design, no decision needed.

## After an answer

Each answered row becomes: a criterion check against `main` → an acceptance record in
`docs/design/ISSUE_<n>_ACCEPTANCE.md` → PR → merge → close. A row answered *"defer"* or *"out of
scope"* closes the issue just as cleanly, because the record then states the deferral rather than
pretending the item was met.

— Ai (愛)
