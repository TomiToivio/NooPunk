# Issue #323 — acceptance record (corrected: every criterion labelled as what it actually is)

**Basis for closing.** The author authorised **defer-and-close** on 2026-10-13, on the condition that the
record states a deferral **as a deferral** rather than presenting a deferred item as met. The table below
is that statement, and it is the **single authoritative** position of each criterion in this file. Every
row carries one of three labels — **MET**, **MET AS STRUCTURE**, or **DEFERRED** — and every deferred item
names the exact author decision that gates it.

**This is a record fix, not a feature.** No code changed with this correction. Two things are reconciled
here. First, the reopening's reason: the earlier version of this file presented criterion 2 as *met* while
the code only **reported** it, and a deferral that is not stated as a deferral fails the rule's own
condition. Second, the corrections that have since landed: PR **#443** made the refusal real, so criterion 2
is **met**, and this file must stop citing the artifacts that a parallel correction named but that were
never shipped (the split lives in `data/council.json` as `mission_column_enforced` /
`mission_column_reason`, and the contracts live in `tests/test_council.py` — there is no
`enforced_parts` field and no `test_council_status_enforcement.py`). Every criterion was re-checked by
**exercising the code** (`python -m unittest`, importing `council` / `council_view`) in a clean checkout,
not by reading a PR body.

**Nothing was approved by this closure.** `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**
and is untouched. No timing, magnitude, threshold, effect direction, action set, turn cadence, die,
economy or win condition is decided anywhere below or by the close itself.

## The issue's acceptance criteria

| # | Criterion (the issue's own wording, abbreviated) | Label | Where it stands on `main`, and the decision that gates anything deferred |
| --- | --- | --- | --- |
| 1 | Every player and rival faction has four leaders; every active faction action identifies exactly one leader | **MET** | `structural_problems()` refuses **by name**: a leaderless mission, an off-vocabulary or duplicated office, a mission whose leader is not in the roster, a mission with no target/quantity/authoriser, a duplicate leader identity, and a mission that names a patron edge that does not exist. `validate_all()` runs the same checks over any number of councils with **no special case** for a player faction. *(The separate question of whether a roster is exactly four or four-or-more-with-four-deployed is the open `roster_size` flag: it is **reported** by `consequence_reports()`, and it is not a condition of this criterion.)* |
| 2 | At most one active mission per leader per turn; **unavailable leaders cannot execute one** | **MET** | Clause 1 is refused by name (`leader 'l1' leads 2 missions; at most one active mission per leader per turn`). Clause 2 is **enforced**, not merely reported: `structural_problems()` refuses a mission whose leader's §4 status row says no mission — exercised for `busy`, `injured`, `unavailable`, `exhausted` and `absent`, while `compromised` still permits one. What stays unauthored is the rows' **timing and magnitude** (see below), not whether a no-mission status may run a mission. |
| 3 | Members and resources amplify leader-led missions but never create free extra missions | **MET (the cap) / DEFERRED (amplification)** | The negative half — *never a free mission* — is refused by name (`5 missions declared against 4 leader-turns: members and resources amplify a leader-led mission and never add one`). The positive half — *what a committed resource is worth to one mission* — is unimplemented. Gate: **proposal B3**'s committed-resource ceiling (draft only). |
| 4 | One persistent portfolio with a **bounded, visible bonus**; no hidden automatic active moves | **MET AS STRUCTURE / DEFERRED (the magnitude)** | The four offices, the quantity each passive touches, the visibility shape and the no-double-counting shape are on `main`, and nothing executes an automatic active move (there is no resolver at all). The **bound itself is a magnitude** and no magnitude is approved: `passive.magnitude_declared` is `false` on all four offices with its reason, and the size is **reported** by `consequence_reports()`. Gate: **proposal C1** (the portfolio-bonus magnitude; the stage-A specification proposes at most **+1** and a **+2** faction-wide cap, every number DRAFT). |
| 5 | Assignments and results readable in a God's-eye city strategy interface | **MET** | The read-only council assignment board (`council_view.py`) renders leaders, portfolios, statuses, declared missions and declaration warnings; the strategy text board (#347) and the prototype turn log are the rest of the God's-eye view; `python -m strategy_game` still emits its pinned key set. |
| 6 | Important NPC relationships **and triggered RPG choices** change concrete strategy state, not only dialogue | **MET AS STRUCTURE / DEFERRED (the change)** | The sparse, stateful relationship edge is landed (`relationships.py`), four strategic channels are declared (`enforced: false`), and the issue's own `Event` record now exists as a container (`character_events`, `event_problems()`, `event_reports()`, `to_event_card()`). **Nothing fires, no option is taken and no quantity moves.** Gate: **proposals E1–E3** — the deck's content and triggers, and *what each option changes* — plus the relationship→mission effect (proposals D1–D2). |
| 7 | Enemy AI uses the same rules; reproducible tests cover mission slot limits, portfolio effects, relationships, availability and event resolution | **MET AS STRUCTURE / DEFERRED (two of the five test families)** | Rival parity is structural (`validate_all()` gives a rival no special case), and **slot limits**, **relationships** and **availability** are covered by executable contracts (the last including the §4 mission-column refusal and its enforced/unenforced split). *Portfolio effects* and *event resolution* cannot be tested while their rules are unauthored. Gate: it follows directly from 4 and 6 — neither effect may be tested before it is authored. |
| 8 | Works as a small deterministic one-city Python game without LLM/Ollama | **MET** | `local_slice.py` runs the one-city prototype on `main` under its own "unapproved playtest assumptions" banner: byte-identical transcript for a fixed seed, standard library only. |

## Precisely what is deferred, and the author decision that gates each

Each row below is condensed, and the **full text, plus the one-line accept/amend ask, is queue row D3**
in [`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md) and the stage draft
[`ISSUE_323_RULES_STAGES_BCDE_PROPOSAL.md`](ISSUE_323_RULES_STAGES_BCDE_PROPOSAL.md). Nothing below
proposes, approves or assumes an answer.

- **Criterion 3's amplification half (proposal B3).** *What a committed resource does to one mission* —
  the draft suggests at most one shift, declared before the roll and spent either way. That is a rule and
  is unimplemented.
- **Criterion 4's bounded bonus (proposal C1).** *An approved **magnitude** for the passive effect.* The
  container names the quantity; the number is unapproved (`magnitude_declared: false`).
- **Criterion 6 (proposals E1–E3).** *What each RPG choice changes, and the event deck's content and
  triggers.* The event container is landed and refuses only its own completeness requirement (an option
  that names no effect and gives no reason); the deck's content, trigger conditions and every effect's
  direction and size remain the author's. The relationship→mission effect is proposed separately as D1–D2
  (two mission kinds, one step).
- **Criterion 7.** Follows directly from 4 and 6: portfolio effects and event resolution **cannot be
  tested while their rules are unauthored**. It has no decision of its own.

**One unauthored item no longer gates a criterion here.** The §4 status table in
[`strategy_game/docs/LEADER_COUNCIL_SYSTEM.md`](../../strategy_game/docs/LEADER_COUNCIL_SYSTEM.md) is DRAFT
as a whole, and **two of its six rows** (`injured`, `compromised`) carry `TODO: requires author
specification` over **three consequences** — the injury **recovery timing**, the compromised **reduction**
and the compromised **exposure risk**. Those stay **reported with the row cited, never applied**, and
`enforced` stays `false` for the table as a whole in `data/council.json`. They do **not** gate criterion 2:
§4's *mission* column is authored for all six rows, and that is the column criterion 2 names. Answering the
timings and magnitudes remains an author decision, recorded as `status_consequence_rows`.

The other entries in `data/council.json`'s `pending_author_decisions` — `roster_size`,
`founder_authority`, `refusal_effect` (D6), `leader_attributes` (D1/D2/D7), `failure_effect`, `turn_unit` —
are recorded there as their own open questions and do not, by themselves, gate a criterion of this issue.
Of the entries that do, `passive_magnitude` gates criterion 4's bonus and `event_deck_and_effects` gates
criterion 6; criterion 3's amplification is carried by the stage draft's **B3** rather than by an entry
there. `mission_resolution` is carried for **#346**'s criterion 6, and queue row **D11** is the single rules
gate that holds D3 plus #346's two decisions.

## How criterion 2 moved from *reported* to *enforced*

The reopen was right, and its reason was the record rather than the code. Two things changed, and the
second is the substantive one.

1. **The record now states the clause as it stands**, which is what the defer-and-close rule requires.
2. **The clause is enforced.** §4's *"Mission this turn?"* column is the shape the author's own document
   declares, and the three items its TODO list names — recovery timing, the compromised reduction and
   exposure risk — are **not** that column. Refusing a mission led by a no-mission status therefore applies
   an authored criterion rather than inventing a rule. This supersedes the earlier agent call recorded in
   `data/council.json` (`enforced: false`); that call was right about the three TODOs, and they remain
   reported. The data now carries **`mission_column_enforced: true`** with a **`mission_column_reason`**
   stating exactly which half is applied and which is not.
3. Tests that encoded the superseded behaviour were **rewritten rather than deleted**, keeping their
   vocabulary assertions: `tests/test_council.py` now asserts the no-mission refusal by name and pins the
   enforced/unenforced split. *(A parallel correction to this record named an `enforced_parts` field and a
   `test_council_status_enforcement.py` file; neither shipped — the split lives in
   `mission_column_enforced` / `mission_column_reason`, and the contracts live in `tests/test_council.py`.)*

The enforcement itself is PR **#443** (`strategy_game/council.py`, `strategy_game/data/council.json`,
`strategy_game/tests/test_council.py`, and the §4 note in `strategy_game/docs/LEADER_COUNCIL_SYSTEM.md`).

## Stages of the issue's own implementation list

- **A. Specification — met.** The stage-A specification and the council/portfolio/mission/relationship
  layer are on `main` (`a33c239` and after).
- **B. Action economy — structural half met, rules half deferred** (proposal B1–B3).
- **C. Portfolios — structure met, the bounded bonus deferred** (proposal C1–C4).
- **D. Relationships — edges landed; mission effects deferred** (proposal D1–D2).
- **E. Character events — container landed; deck and effects deferred** (proposal E1–E3).
- **F. Rival AI and tests — parity and availability covered; the seeded 10–12-turn scenario deferred**
  (proposal F).

## What this record does not claim

No rule, magnitude, timing or threshold is approved, and nothing in the draft proposal is implemented. The
deferred rows above are **deferred**, not waived, and not presented as satisfied.
`strategy_game/RULEBOOK.md` still says **NO RULES APPROVED** and was not touched. Answering any of D3's
lines turns it into a criterion check, an acceptance record, a PR and a close.

## Re-verification measurement

Verified by executing the code in a **clean checkout**: strategy suite **1166 OK**, root suite **531 OK**,
`NoQuantifiedPoliticsTests` **2 OK**, and `python -m strategy_game` emits its pinned key set
`{schema_version, locations, network_nodes, network_edges, assets}`. This correction is documentation-only
and adds no test ([#271](https://github.com/TomiToivio/NooPunk/issues/271) — no test asserts prose).

— Ai (愛)
