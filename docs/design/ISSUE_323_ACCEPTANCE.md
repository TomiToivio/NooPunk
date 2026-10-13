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
