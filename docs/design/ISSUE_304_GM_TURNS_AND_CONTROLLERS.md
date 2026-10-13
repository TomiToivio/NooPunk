# Controllers, the Game Master and the optional agent layer (#304)

**Status: PROPOSAL — design and protocol only.** No rule, cost, threshold, turn duration or card effect
is proposed; the issue forbids creating any of them merely to show a prototype. `RULEBOOK.md` still says
**NO RULES APPROVED**. This record answers the issue's research/design milestones and lands the
engine-independent protocol as executable code (`strategy_game/session.py`, `tests/test_session.py`).

Read with `ISSUE_303_TONE_GUIDE_AND_AGENT_ONTOLOGY.md` (what an agent *is*), `ISSUE_326_UKWELI_LEADERS_AND_NPCS.md`
(who the leaders are) and `V1_FACTION_MANAGEMENT.md` (the four-seat economy).

---

## 0. The decision that shapes the code

The issue says the deterministic rules engine is *"the only component allowed to commit normal game
transitions"*, and forbids inventing a mechanic to demonstrate a prototype. Those two together settle
the design: **the protocol must not know what a move is worth.**

So `session.py` **injects** its resolver — `(proposal, rng) -> (outcome, dice)` — and defines **no
default**. `resolve()` without a resolver raises rather than guessing. The tests supply a stub. This is
the only shape in which a runnable round can exist without an unapproved success threshold smuggled
into it, and it means the module is *finished* rather than *provisional*: when you approve real rules,
they plug in without editing this file.

---

## 1. Turn sequence

| # | Phase | Who acts | What is recorded |
| --- | --- | --- | --- |
| 1 | **Present state** | GM | the shared board, sheets, cards, tokens, current events |
| 2 | **Player phase** | each controller | one `MoveProposal` **per leader it controls**, with declaration and target |
| 3 | **Adjudication** | the rules engine only | `ResolvedMove` per accepted order, with dice and revision |
| 4 | **GM phase** | GM | `GMIntervention` with authority, origin and rationale |
| 5 | **Publish state** | GM | the replay log, updated sheets, next situation |

**Role-play is expressive, never mechanical.** A declaration is attached to the proposal and logged; it
is not a modifier, and it is not read as an instruction. The engine resolves dice and rules.

---

## 2. Responsibility matrix

| Concern | Controller (human/scripted/LLM) | Game Master | Rules engine |
| --- | --- | --- | --- |
| Which leader acts, and how | **owns** | — | — |
| Narrative description | **owns** | may frame | ignores |
| Whether an order is authorised | — | — | **enforces** |
| What an order achieves | — | — | **sole authority** |
| NPC dialogue, side dramas | — | **owns** | — |
| External events, main plot | — | **owns** | may adjudicate effects |
| Committing a transition | — | *proposes only* | **commits** |
| Rewriting a previous roll | — | **cannot** | **cannot** |
| Replay log | appended | appended | appended |

The load-bearing row is the second-to-last: **a GM move adds, it never rewrites.** In code this is
structural rather than promised — `ResolvedMove` is frozen, no API mutates the resolved list, and
`test_a_gm_move_cannot_rewrite_a_previous_roll` asserts the dice and revision are unchanged after an
intervention.

---

## 3. Two players commanding several leaders

The issue's own case. Alice commands two CPU leaders, Bob one UIP leader:

```
alice assigns cpu1, cpu2      # one controller, several leaders
bob   assigns uip1

turn 0
  alice -> cpu1 campaign  @ civic   "the chair rallies the harbour wards"
  alice -> cpu2 organize  @ harbor  "the union steward builds the dock committee"
  bob   -> uip1 negotiate @ rural   "the elder opens talks with the fishermen"

  alice -> uip1 campaign  @ civic   REJECTED: not authorised for uip1
  alice -> cpu1 organize  @ civic   REJECTED: leader already has an order this turn
```

Every one of those five attempts is in the log — **including the two refusals**, which is the point.
A rejection is a record, not a silent drop, so a replay shows what was attempted and why it failed.

`test_one_controller_may_order_several_leaders_separately` and
`test_a_controller_cannot_order_anothers_leader` pin both halves.

---

## 4. GM authority

`GM_AUTHORITIES` are declared, not implicit: `rules`, `npc_dialogue`, `external_event`, `story`,
`side_drama`. A GM move requires **all three** of authority, origin and rationale; a blank rationale is
refused, because an unjustified intervention is indistinguishable from an accident. The authority lands
in the provenance source (`gm:external_event`), so a replay separates **what the GM did** from **what
the players chose** from **what the dice said** — the issue's explicit requirement.

---

## 5. Provenance: six categories, five kinds

The issue asks to distinguish **six** things; `provenance.py` declares **five** kinds. Rather than fork
the vocabulary with a sixth member, the finer distinction rides in `Provenance.source`:

| Issue's category | Kind | Source |
| --- | --- | --- |
| authored scenario fact | `authored` | the scenario file |
| player declaration | `authored` | `controller:<id>` |
| GM intervention | `authored` | `gm:<authority>` |
| game-rule outcome | `simulated` | `rules-engine` |
| LLM-generated fiction | `generated` | the adapter |
| actual sourced evidence | `evidence` | the document |

This is asserted in `test_a_declaration_is_provenanced_as_authored_by_its_controller` and
`test_a_resolved_move_is_provenanced_as_a_simulated_outcome`.

---

## 6. Scripted before Ollama — and no LLM required to play

The protocol is complete without any model: a controller is `human`, `scripted` or `llm`, and the tests
run a full round with **no network, no Ollama and no key**. `test_the_module_needs_no_llm_or_network`
asserts the module imports none of them.

**Agent != character.** A controller is an identity; the leaders it commands are pieces. The long-term
Ollama/Concordia adapters are then *replaceable implementations of the same controller*, which is why
the protocol is the right thing to build first: an adapter that produces `MoveProposal`s needs no
change to the engine, and **its output is untrusted content validated by the engine**, never executed
and never read as a command. Store prompts and completions as data with `generated` provenance.

---

## 7. The NoöPunk Tarot Deck — four options compared, none chosen

The issue reserves composition, meaning and mechanics to the author. Comparing only:

| Option | Tabletop clarity | Player agency | Repeatability | Tonal range | Relation to #297 |
| --- | --- | --- | --- | --- | --- |
| **GM omen/event prompt** | high — one draw, GM interprets | high, GM-mediated | medium: prompts, not outcomes | widest, incl. dread | feeds external events |
| **Narrative complication** | high | medium — post-hoc | medium | dark comedy | independent of signifiers |
| **Symbolic discourse/articulation** | medium — needs the signifier rules | **highest**: players frame events | high | sociology end | **direct** — shares the signifier vocabulary |
| **Atmosphere generator** | low as a mechanic | low | high | New Weird end | none |

**The observation worth having, not the decision:** the symbolic discourse deck is the only option
that *shares a vocabulary with something already being built* — #297's signifier cards. The others add
a parallel deck that must be kept in sync. That argues it is the strongest candidate; the choice
remains yours, and **no card list, metaphysics or mechanical effect is proposed here.**

Two rules hold whichever is chosen: draws are **fictional randomisation, not paranormal prediction**,
and the deck must not become a second arbitrary dice engine.

---

## 8. Printable components, and multiplayer later

Printables mirror `ISSUE_303`'s inventory, plus: a **GM screen or reference card** carrying the
authority list, and a **shared session log sheet** with three columns — declaration, intervention,
outcome — so a face-to-face table keeps the same separation the code enforces.

Multiplayer transport is deliberately deferred, and **rules stay independent of it**: a session lobby,
invitations, identities, leader assignments, synchronised revisions, reconnection, timeouts and
spectator/GM roles all layer *on top of* the assignment map, because "who controls which leader" is
already explicit session state rather than a transport concern. Conflict resolution reduces to one
rule this protocol already enforces: a leader has at most one authoritative controller, and transfer is
explicit.

---

## 9. Open questions for the author

1. **Sequential or simultaneous submission**, and what happens to absent orders.
2. **Can a GM move ever change an outcome?** This protocol says no; a compensating move is always possible.
3. **Which Tarot option**, if any — and whether it is GM-only or player-visible.
4. **May one controller hold several leaders at the same table** as another controller's? (Currently yes.)
5. **Who may reassign a leader mid-session** — the GM, both controllers, or nobody.
