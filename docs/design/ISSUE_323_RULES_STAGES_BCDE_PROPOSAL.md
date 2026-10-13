# Issue #323 — draft rules for stages B–E (PROPOSAL ONLY)

**Status: PROPOSAL. This approves nothing.** Every number below is a suggestion for the author to
accept, refuse or amend, and `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED** — it is
untouched by this file, and no code implements anything here. Its purpose is that each remaining
stage of #323 can be answered in one line instead of designed first.

## What is already on `main` as structure (not a rule)

| Element | Where | What it does today |
| --- | --- | --- |
| Four leaders, four offices | `strategy_game/council.py`, `data/council.json` | exactly four posts per faction, refused by name if not |
| One leader per mission, one mission per leader per turn | `structural_problems()` | refuses a leaderless mission and a second active mission for the same leader |
| Declared cost, authorisation and failure shape of a mission | `council.py` | a mission declares what it costs and who authorised it |
| Sparse relationship edges | `relationships.py` | the one stateful edge the layer reads |
| Six quantities, names only | `quantities.py` | the vocabulary a portfolio's primary is checked against |
| Bounded portfolio bonus | `council.json` | `magnitude_declared: false` with a stated reason — the *declaration* exists, the *number* does not |
| Readable assignment board | `council_view.py` | the God's-eye text view (#412, #418) |

So the structural half of **A** and **B** is landed. What follows is the rules half only.

## B — the action economy's remainder

- **B1. Refusal, not penalty.** An illegal declaration is refused before resolution, with the problem
  named; it never resolves as a weaker move. (This is what `structural_problems()` already does; the
  proposal makes it the rule rather than an implementation detail.)
- **B2. Unavailable leaders.** A leader whose status marks them unavailable (captured, ill, elsewhere)
  cannot be assigned. Their slot is lost for the turn; it is not transferred.
- **B3. Amplification, never multiplication.** A faction's members and resources may *raise the
  ceiling of one mission's effect* but never create an extra mission slot. Suggested shape: a
  resource committed to a mission may add at most one shift, declared before the roll, spent whether
  or not the roll succeeds.

## C — the bounded portfolio bonus (the gated core)

- **C1. Shape.** Each of the four portfolios has exactly one passive bonus. It is: at most **+1
  shift**; tied to **one named check family** (e.g. the office whose work is negotiation touches
  negotiate checks); visible wherever the leader is shown; and never larger than the leader's own
  skill contribution.
- **C2. Reassignment.** Moving a leader between portfolios costs **one turn** — the turn in which they
  arrive grants no bonus — is logged, and never retroactively changes a resolved turn.
- **C3. What it must never do.** Grant a free active mission; double-count a skill already applied;
  apply while its leader is unavailable; or stack with another portfolio bonus on one check. Those
  four are the failure modes the issue itself names, and each is testable.
- **C4. If refused.** The portfolio stays declarative — the *office* still decides what it decides;
  only the numeric bonus is dropped. Nothing else in the layer depends on C1's magnitude.

## D — relationships that change strategy state

- **D1. Two mission kinds, two directions.** A **trusted** edge lowers the difficulty of a *negotiate*
  mission by one step; a **strained** edge raises the difficulty of an *organise* mission by one step.
  At least two kinds of mission are therefore affected, as the criterion requires.
- **D2. Bounds.** One edge per pair, one step of effect, no cascades (a relationship never modifies
  another relationship), and no hidden modifier — an affected check states the edge that moved it.

## E — the character event deck

- **E1. Size and triggers.** Six to eight events, each keyed to a **trigger** the layer can already
  see: a leader's status change, a relationship crossing a threshold, or a mission's outcome.
- **E2. Shape of one event.** A trigger, a choice with two or three named options, and a **visible
  consequence that lands in strategy state** — a quantity, a relationship, a leader's availability —
  never dialogue alone. This is the criterion the issue states most plainly.
- **E3. Determinism.** Given the same seed and the same declaration, the same event fires with the
  same options; the event log records the trigger and the choice taken.

## F — rival AI, one paragraph

Stage F adds no new rules: NPC factions declare their turns through the same validator and the same
mission shape, so the reproducible 10–12-turn scenario exercises one engine, not two. The tests it
asks for (mission slot limits, portfolio effects, relationships, availability, event resolution) are
the same properties listed above, which is why approving B–E also settles what F must satisfy.

## The decisions this needs (one line each)

| # | Decision | Suggested default |
| --- | --- | --- |
| 1 | B3's committed-resource ceiling: one shift, declared before the roll, spent either way? | accept |
| 2 | C1's magnitude: is **+1** the ceiling for a portfolio bonus? | accept |
| 3 | C2's reassignment cost: one turn without the bonus? | accept |
| 4 | D1's two mission kinds: negotiate/difficulty-down and organise/difficulty-up? | accept |
| 5 | E1's deck size: six to eight events for the MVP? | accept |
| 6 | E2's rule that no event may end in dialogue alone? | accept |

## If approved

Implementation becomes a separate PR per stage (C, D, E in that order), each with the tests the issue
names. Nothing here is implemented now, and nothing here is canon: the offices, cities and people
this would touch are already data.
