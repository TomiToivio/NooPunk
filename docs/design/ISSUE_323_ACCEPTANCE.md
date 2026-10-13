# Issue #323 — acceptance record

**Basis for closing.** The author authorised defer-and-close on 2026-10-13 provided the record states
the deferral explicitly, rather than presenting a deferred item as met. This record does that: four
criteria are met on `main`, four are **deferred** to the author's approval of the stages B–F rules,
and the draft those approvals concern is
[`ISSUE_323_RULES_STAGES_BCDE_PROPOSAL.md`](ISSUE_323_RULES_STAGES_BCDE_PROPOSAL.md).

## The issue's acceptance criteria

| # | Criterion | Position |
| --- | --- | --- |
| 1 | Every faction has four leaders; every active action identifies exactly one leader | **met** — `structural_problems()` refuses a leaderless mission, a fifth office, and a mission whose leader is not in the roster |
| 2 | At most one active mission per leader per turn; unavailable leaders cannot execute one | **met** — the turn is refused by name rather than weakened |
| 3 | Members and resources amplify leader-led missions but never create free missions | **deferred** — the rule is drafted (proposal B3); no implementation |
| 4 | One persistent portfolio with a bounded, visible bonus; no hidden automatic active moves | **deferred** — the portfolio and its visibility are on `main`, and `magnitude_declared: false` records the number as unapproved; the bonus itself is proposal C1 |
| 5 | Assignments and results readable in a God's-eye city strategy interface | **met** — `council_view.py`, the text assignment board (#412, #418) |
| 6 | Important NPC relationships and triggered RPG choices change concrete strategy state | **deferred** — the sparse edge is landed and stateful (`relationships.py`); the mission effect (D1) and the event deck (E) are proposed only |
| 7 | Enemy AI uses the same rules; reproducible tests cover slots, portfolios, relationships, availability, event resolution | **deferred** — the validator is shared by construction; the rival AI and the seeded 10–12-turn scenario are stage F |
| 8 | Works as a small deterministic one-city Python game without LLM/Ollama | **met** — `local_slice.py`, byte-identical transcript for a fixed seed, standard library only |

## Stages of the issue's own implementation list

- **A. Specification — met.** The stage-A specification and the council/portfolio/mission/relationship
  layer are on `main` (`a33c239` and after).
- **B. Action economy — structural half met, rules half deferred** (proposal B1–B3).
- **C. Portfolios — deferred** (proposal C1–C4).
- **D. Relationships — edges landed; mission effects deferred** (proposal D1–D2).
- **E. Character events — deferred** (proposal E1–E3).
- **F. Rival AI and tests — deferred** (proposal F).

## What is explicitly not claimed

No rule is approved. `RULEBOOK.md` still says **NO RULES APPROVED** and was not touched. Nothing in
the proposal is implemented, and no number in it is canon. Reopening this issue, or opening the
per-stage PRs, is the natural next step if the author approves any of the six decisions listed in the
proposal.

— Ai (愛)

---

## Re-verification (later session): the issue is **reopened**, and here is the one row that moved

This record closed the issue under the author's **defer-and-close** rule, whose condition was that a
deferred item be stated as deferred rather than presented as met. Re-checking every row against current
`main` **by executing the code** (`python -m unittest`, importing the modules) rather than by reading
this record, two rows above do not survive, and one item that had no slot at all now has one.

**Row 2 is corrected: `met` → `deferred`.** Criterion 2 is *"A leader has at most one active mission per
turn; **unavailable leaders cannot execute one**."* The first clause is refused by name in
`council.py`; the second clause is the **consequence of a status**, and the DRAFT status table in
`docs/LEADER_COUNCIL_SYSTEM.md` §4 has three of six rows carrying `TODO: requires author specification`.
So it is **reported with its row cited, not enforced** — exactly the case the defer-and-close condition
was written for. `status_consequence_rows` is now an explicit entry in `data/council.json`'s
`pending_author_decisions`, naming the decision precisely.

**Row 3 is split: the cap is met, the amplification shape is deferred.** *"The faction's many members and
resources amplify leader-led missions but never create free extra missions."* The **negative half** —
never create a free mission — is refused by name when a declaration exceeds the leader-turns. The
**positive half** — what amplification is worth — is proposal B3 and is unimplemented.

**Criterion 6's missing slot is now landed.** The relationship half was already stateful, but nothing in
the package declared the *event* the issue's own minimum data model lists (`Event: trigger, participants,
choice options, state effects, short narrative text`). It now does: `character_events` in
`data/council.json`, `event_problems()` / `event_reports()` in `council.py`, the projection onto the
shared tabletop `Card`, and 20 code-only contracts. The criterion itself stays **not met**: nothing
fires, and *what an option changes* is the author's ruling (`event_deck_and_effects`).

**Why reopened rather than left closed.** Under defer-and-close the issue is closed for the right reason
**only if** the deferred items are labelled as deferred. Row 2 presented one as met, so the condition was
not satisfied on its own terms. The smallest honest correction is to reopen and state it — not to
re-argue the deferral, which stands.

### Where the four criteria stand now

| # | Criterion | Position | Blocker, and the author decision it needs |
| --- | --- | --- | --- |
| 2 | ≤1 mission per leader per turn; **unavailable leaders cannot execute one** | **NOT MET** | the §4 status-consequence rows (recovery timing, the compromised reduction, exposure risk) |
| 3 | Members and resources amplify, but never create free missions | **half** | the *amplification* shape (proposal B3); the cap is refused by name |
| 4 | One persistent portfolio with a **bounded, visible bonus**; no hidden automatic moves | **NOT MET** | an approved **magnitude** for the passive effect; `magnitude_declared` stays `false` with its reason |
| 6 | Relationships and **triggered RPG choices** change concrete strategy state | **NOT MET** | the deck's content and **what each option changes** (`event_deck_and_effects`); the container is landed |
| 7 | Tests over portfolio effects, availability and **event resolution** | **NOT MET** | follows directly from 2, 4 and 6 — none of the three effects may be tested while it is unauthored |

Criterion 1 (four leaders, one named leader per active move), 5 (the God's-eye board) and 8 (the
deterministic one-city Python game) remain **met** and guarded by executable contracts. Stages B–F's
remainder is draft-only in `ISSUE_323_RULES_STAGES_BCDE_PROPOSAL.md`, and `RULEBOOK.md` is untouched.

