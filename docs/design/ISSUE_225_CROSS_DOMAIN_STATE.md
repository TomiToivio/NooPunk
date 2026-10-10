# Issue #225 — Cross-domain actions: the state machine and the shared action economy

**Status: PROPOSAL landed as a contract, not a calibration.** `rulebook/18_CROSS_DOMAIN_STATE.md`
is now the single canonical shared-procedure section, and `src/rules/cross_domain_state.py` executes
its invariants with `IS_CANONICAL = False`. Every number in both is the author's to set; nothing
here migrates a runtime.

Cross-links: #200 (epic), #217 (resolution semantics), #222 (cyberspace procedure), #219 / #221 /
#223 / #224 (the realm chapters that consume this contract).

## Why this issue was the open dependency

Two merged passes deferred to it in writing:

| Source | What it says |
| --- | --- |
| `rulebook/5_CYBERNETIC.md` (#222) | the action-point economy is *"provisional until #217/#225 fix it"* |
| `docs/design/ISSUE_217_RESOLUTION_SEMANTICS_2026-10-10.md` (#217) | *"action points — not this issue — cross-domain, owned by #225"* |

So #225 was not a new subsystem competing with #219/#221/#223/#224; it was the contract those four
name and wait on. Writing it once is what stops four chapters from each defining their own turn.

## The design decisions this plan made, and why

### 1. Four states, and two things that are deliberately *not* states

The states are `embodied`, `cyber-immersed`, `astral-projected`, `involuntary dream/NDE`. The
discriminator is **where the consciousness acts**, not what it can do there.

The negative half matters more than the positive half: **cyberspace modes 1–3 and embodied local
PSI are not projection.** A character reading a room, or hacking from a laptop, stays embodied. If
"using a computer" counted as immersion, every investigator would be permanently body-exposed and
the body-cost would become meaningless noise. #222 states the same boundary from the other side
("only modes 3 and 4 are *intrusions*"); this section states it for the state machine.

### 2. The single-locus rule is the invariant, not a rule among rules

> One consciousness-instance has exactly one locus of control.

Everything else follows: you act in one realm per exchange, a projected body cannot act, states
replace rather than stack, and a fork is a separate instance (which is also *why* §45's continuity
question stays unresolved — this rule refuses to let copying become a free extra turn, without
settling whether a copy is the same person).

The executable form is `TRANSITIONS`: there is **no direct edge between two projected states**.
A character must return to the body before entering another projected state. That single structural
choice is what makes "one locus" checkable instead of aspirational.

### 3. One clock, 3 AP, and reactions that are never free

3 AP per actor per exchange on one shared clock, with a fixed cost table (Act / Move / Prepare /
Cover / React / Exit). Two deliberate consequences:

- **Held AP expires; a reaction borrows instead.** A reaction costs 1 AP from a held AP or from the
  *next* exchange. Making reactions free would make "react to everything" dominant; making them
  impossible would remove the tactical layer. Borrowing prices them.
- **Agents are actors, capped by permission.** A software agent, ICE, drone or AI has its own 3 AP —
  but it cannot spend AP on authority the node never granted it. That is what keeps segmentation
  meaningful (#222) when the defender is a fast machine.

### 4. Initiative: one order, refinable but not forkable

Descending REF, ties to whoever holds more AP, then the GM. This is deliberately **minimal**, because
#219 owns tactical detail. The binding part is not the ordering rule but the prohibition: a later
pass may refine the order, and may not define a second one. `AGENTS.md` §13.3 (rules parity) is the
reason.

### 5. Gateways: a precondition, not a modifier

"No realm reaches another without a declared gateway." This generalises #222's cybernetic rule
(*"device compromise is not brain compromise"*) rather than restating it as a special case. The
implementation makes that structural: `can_cross()` returns False when the gateway is absent
**regardless of any other input**, so no rating, roll or modifier can buy a crossing.

The mapping is deliberately sparse, and `NO_GATEWAY_EXISTS` names the crossings that are *known
impossible* — including **Noöspace ↔ cyberspace**, which has no general gateway. Naming the
impossibilities explicitly is what stops a later chapter inventing one by omission.

### 6. The rare cyber-PSI power: narrow, gated, counterable (AC3)

**Noetic coupling** — treating a network as a Noetic substrate — requires **all four** of: awakened
PSI + trained PSY Skill, an actual vulnerable neural gateway, psychotronic mediation, and a declared
action on the clock. Its counterplay is specific and cheap: remove the gateway (airgap, Faraday,
hardened deck, unplugged implant), dampen, sever the neural link, oppose with Psychic Defence, or let
Trace and containment do their work.

What it explicitly **cannot** do is stated as three prohibitions: it does not replace `Infosec`; it
cannot exceed its gateway; it cannot cross a realm boundary the gateway does not already span. The
issue's AC3 asks that this not become a general ability, and the prohibitions are the mechanism.

## AC mapping

| AC | Where |
| --- | --- |
| 1 — single state machine for the four states | `18_CROSS_DOMAIN_STATE.md` §*The four states*, §*The single-locus rule*; `cross_domain_state.py` `STATES` / `TRANSITIONS` |
| 2 — shared AP/initiative, transitions, reactions, body exposure, crossings, interruptions, agent economy | §*The shared action economy*, §*Physical-body exposure*, §*Effects crossing realms*, §*Interruptions and return*; `ActionEconomy`, `can_cross` |
| 3 — the cyber-PSI power has prerequisites/counterplay, not general | §*The rare power: noetic coupling* |
| 4 — executable transition invariants + simultaneous four-realm scenario | `tests/test_issue225_cross_domain_state.py`; §*Worked example: one exchange, four realms* |
| 5 — cross-links, tests, PR comment | cross-links added to `2_ATTRIBUTES.md`, `5_CYBERNETIC.md`, `6_PSYCHIC.md`; the guard; the PR |

## What was deliberately not done

- **No calibration.** AP costs, the 3-AP budget, REF ordering and forced-return difficulty are
  labelled PROVISIONAL in the chapter and non-canonical in the module. The author owns the numbers.
- **No realm-chapter content.** Combat detail (#219), hardware statistics (#221/#228), the PSI power
  list (#223) and the astral procedure (#224) are untouched — they consume this contract.
- **No new Skills, STATs or derived statistics.** The contract spends AP and uses existing Skills.
  `AGENTS.md` §1/§2 keep the rest reserved.
- **No RULEBOOK.md edit.** `rulebook/*.md` chapters are modular and separate from the canonical
  `RULEBOOK.md`; adding a chapter here does not disturb the split map or the section numbering, and
  the cross-reference guard discovers self-numbering chapters, which this chapter deliberately is
  not (no numbered headings), so no RULEBOOK link or renumbering was required.

## Verification

- Full suite green: **1228 → 1269 tests**, no pre-existing test broken.
- `tests/test_issue225_cross_domain_state.py` — 41 tests, sabotage-proven (mutate → guard fails →
  restore byte-identical).
