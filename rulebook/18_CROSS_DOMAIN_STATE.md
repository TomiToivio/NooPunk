# Cross-domain state and the shared action economy

> **Status: NOÖPUNK NATIVE — issue #225.** This is the **single canonical shared-procedure
> section** for realm-spanning play. The realm chapters consume it and must not restate it:
> physical combat is #219, cybernetic hardware is #221/#228, the PSI power list is #223, and the
> astral procedure is #224. Every number here is **PROVISIONAL pending author calibration**; the
> author owns the final values.

NoöPunk has four realms — **Physical, Social, Cybernetic and Psychic** — and a scene can occupy
several at once. Without one contract, each chapter would invent its own turn, its own action
budget and its own initiative order, and a scene where one character dives, another projects and a
third is in a firefight would have no shared clock. This section is that one contract.

Its immediate debt: the cyberspace procedure was written with the action economy **provisional
until #217/#225** (`5_CYBERNETIC.md`), and the resolution pass recorded action points as
*"cross-domain, owned by #225"* (`docs/design/ISSUE_217_RESOLUTION_SEMANTICS_2026-10-10.md`). This
section closes that debt rather than adding a third deferral.

## The four states

A character's **consciousness** is in exactly one of four states. The state says *where the
character acts*, not *what they can do there*.

| State | Where the consciousness acts | Body | Entered by | Ended by |
| --- | --- | --- | --- | --- |
| **Embodied** | Spacetime — Physical, Social and local Psychic action | the character controls it | default | — |
| **Cyber-immersed** | Cyberspace, as a full-sensorium dive (mode 4) | present, and **not** controlled | a full-sensorium dive rig | voluntary exit, emergency disconnect, or forced return |
| **Astral-projected** | Noöspace | present, and **not** controlled | the Noöspace technique (#224) | voluntary return, snap-back, or severance |
| **Involuntary dream / NDE** | a dream or a Noöspace episode | present, and **not** controlled | sleep, trauma, or near-death | waking, or forced return |

Two things that are **not** full projection, and must not be treated as states:

- **Cyberspace modes 1–3** (global WWW, embodied local AR/WLAN, node/edge graph hacking). The
  character stays **embodied**; a screen, deck or goggles is an *interface*, not a locus. Only
  mode 4 moves the locus (`5_CYBERNETIC.md`).
- **Embodied local PSI.** A psychic reading a room is embodied. Projection is a different act with
  a different price (#224).

**State, not skill, decides reach.** A character cannot leave the embodied state by rolling well,
and cannot be *kept* in a projected state by an opponent's good roll — transitions are decisions
and effects, never check outcomes alone.

## The single-locus rule

> **One consciousness-instance has exactly one locus of control.**

This is the invariant the whole section exists to protect. Four consequences:

1. **You act in exactly one realm per exchange.** A cyber-immersed character does not also take a
   Physical action this exchange, however many AP they hold.
2. **A non-embodied body cannot act.** It cannot move, attack, or defend actively. It is a body,
   not an agent, until the state ends.
3. **You cannot be in two states at once.** Entering a state from another is a transition, not an
   addition; the old state ends.
4. **A fork or copy is a separate instance**, not a second locus for the same one. Continuity and
   copying remain deliberately unresolved (`RULEBOOK.md` §45) — this rule does not settle them, it
   only refuses to let them become a free extra turn.

An effect that would give one instance two loci simultaneously is **not supported**. There is no
"split attention" action in the core procedure.

## The shared action economy

**PROVISIONAL.** Every actor spends from **one clock**.

- **3 action points (AP) per actor per exchange.** There is no separate hacking turn, PSI turn or
  astral turn; a dive, a projection and a firefight all consume the same budget on the same clock.
- **Agents are actors.** A software agent, a piece of ICE, a drone, an AI or an NPC has its own
  3 AP and its own position in the order. An AI may act faster in the fiction, but it is **capped
  by its permissions** — it cannot spend AP on authority the system never granted it
  (`5_CYBERNETIC.md`).

| Action | AP | Notes |
| --- | ---: | --- |
| **Act** — do the thing the current state and privilege actually permit | 1 | A failed relevant check still spends the AP |
| **Move** — change position, node or band | 1 | Embodied movement; in cyberspace, traversal to an adjacent node |
| **Prepare** — Map, aim, study, attune, ready a device | 1 | The set-up action that makes a later Act better |
| **Cover** — erase traces, take cover, break a lock-on, ground | 1 | Defensive or hygiene action |
| **React** — act out of turn in response to someone else | 1 | See *Reactions* — never free |
| **Exit** — leave a projected state (emergency disconnect, return) | 1 | Always available; always costs something |

**Holding AP.** Unspent AP does **not** carry over between exchanges. An AP may be *held* during
the exchange for a reaction, and expires with the exchange.

**Initiative.** Within one exchange, actors act in order of **descending REF**. Ties are broken by
the actor holding more AP, then by the GM. This is the **shared contract only** — a later physical
or cybernetic pass may refine the ordering, but it may not fork it: every realm uses this one order.

**Reactions.** A reaction costs **1 AP**, paid from an AP held this exchange or **borrowed from the
next**. A reaction is therefore never free, and a character who reacts repeatedly starts the next
exchange in debt. This is what stops "react to everything" from being the dominant tactic.

## Physical-body exposure

While cyber-immersed, astral-projected or in an involuntary dream / NDE:

- **The body is present, locatable and vulnerable.** It is where the character physically is.
- **It cannot be actively controlled by the projected consciousness.** No Move, no attack, no
  active defence. Passive cover applies; deliberate defence does not.
- **Others can defend it.** A bodyguard, a locked room, restraints, a medical bay or a team that
  knows what is happening are all real answers, and the correct ones.
- **Harm to the body is a forced-return trigger** (see *Interruptions*).
- **Protection is fictional and situational, not a stat block** (PROVISIONAL): physical protection
  (a locked, watched location; restraints that stop the body walking off), a cybernetic break — a
  medical neural bridge that can sever the link — or a noetic anchor or ward (#224). No protection
  is free; each is a commitment someone made in advance.

> **The deepest access costs the body.** That price is the point of the design, not a footnote —
> the same rule governs the cybernetic dive and the astral projection.

## Effects crossing realms: gateways

> **No realm reaches another without a declared gateway.**

Most cross-realm effects people assume are actually impossible. The general rule:

| From → To | The gateway that must exist | Without it |
| --- | --- | --- |
| Cyberspace → mind (wetware) | an actual vulnerable connected neural path | unreachable, whatever the attacker rolls |
| Physical → cyberspace | physical access to the device or its network | no entry |
| Mind → cyberspace | the narrow noetic coupling below | no effect |
| Noöspace → body | a noetic anchor or resonance (#224) | no effect |
| Noöspace → cyberspace | **no general gateway exists** | no effect |

**"Device compromise is not brain compromise"** (`5_CYBERNETIC.md`) is the cybernetic case of this
one general rule, not a special exception. A gateway is a **precondition**, not a modifier: it
cannot be bought with a good roll, and its absence cannot be overcome by a better one.

## Interruptions and return

Returning is **always possible and never free**.

- **Harm to the body** triggers a **forced-return test** (PROVISIONAL: PSY-based, difficulty set by
  the severity of the harm). Failure means the state holds and the character remains exposed.
- **Trace fills** → the node's `containment` fires (`5_CYBERNETIC.md`) and the session may be
  crashed rather than closed.
- **Severance** — a hostile astral effect cutting the projection — costs trauma and disorientation,
  not just time (#224).
- **Return costs, by state** (PROVISIONAL): a cybernetic exit forfeits uncommitted work; a *crashed*
  session may stun; an astral snap-back disorients; waking from an involuntary state is not chosen
  at all.
- **A body left unprotected is the price of every state but Embodied.**

## The rare power: noetic coupling (cyber-PSI)

NoöPunk has one unusual cross-domain capability, and it is deliberately **not a general ability**.

**Noetic coupling** is the rare ability to treat a network as a Noetic substrate — to perceive a
graph as a pattern of meaning, or to extend a psychic defence across a segment.

**Prerequisites — all of them, every time:**

1. **Awakened PSI** and the relevant PSY Skill (trained-only; no untrained coupling).
2. **An actual vulnerable neural gateway** — a real neural path into the network. A hardened deck,
   an external device or a character with no BCI **cannot** couple, at any rating.
3. **A psychotronic coupling or attunement.** The capability is mediated by technology
   (`6_PSYCHIC.md`), not by willpower alone.
4. **A declared action.** Coupling is an act on the shared clock, costing AP like anything else.

**Counterplay — specific and available:**

- **Remove the gateway.** An airgap, a Faraday cage, a hardened deck or an unplugged implant ends
  coupling outright. This is the primary answer and it is cheap.
- **Psychotronic dampening / grounding** suppresses the coupling for its duration.
- **Sever the neural link** (a medical bridge, an emergency break) ends it and costs the coupler.
- **Psychic Defence** opposes it where it acts on a mind through the network.
- **Trace and containment** still apply (`5_CYBERNETIC.md`); coupling does not hide a session.

**What it explicitly cannot do:** it does not replace **Infosec** or any hacking Skill; it cannot
exceed the gateway it runs through; it cannot cross a realm boundary the gateway does not already
span; and it cannot reach a mind the network does not physically reach. The author owns any
widening of this capability; nothing here should be read as a general "psionic hacking" license.

## Worked example: one exchange, four realms

**PROVISIONAL numbers.** A team is in a clinic. **A** is cyber-immersed at a records segment;
**B** is astral-projected, seeking a witness's memory; **C** is embodied, talking to a receptionist
while a guard watches; **D** is an embodied software agent defending the segment (a **sentry**,
`5_CYBERNETIC.md`).

Initiative by REF: **A (REF 8) → C (REF 7) → D (REF 6) → B (REF 5)**. All four spend from one
clock, 3 AP each.

| Actor | AP | Action | Resolution | Realm |
| --- | ---: | --- | --- | --- |
| **A** | 1 | Escalate to T1 | `CYB 6 + Program 3 + 1d10(6) = 15` vs hardening 13+2 | Cyberspace |
| **A** | 1 | Act — pull one record | loud: Trace 1 | Cyberspace |
| **A** | 1 | Hold (kept for a reaction) | — | — |
| **C** | 1 | Prepare — read the receptionist | `SOC 5 + Kinesics 3 + 1d10(7) = 15` vs 13 | Social |
| **C** | 1 | Act — `Talk` for a visitor log | `SOC 5 + Talk 4 + 1d10(4) = 13` vs 13 | Social |
| **C** | 1 | Move — step out of the guard's eyeline | — | Physical |
| **D** (sentry) | 1 | Act — raise Trace | Trace 2 | Cyberspace |
| **D** | 1 | Act — alert the human operator | containment is now *committed* | Cyberspace |
| **D** | 1 | Hold | — | — |
| **B** | 1 | Act — reach for the memory | `PSY 6 + Noöspace 4 + 1d10(5) = 15` vs 15 | Noöspace |
| **B** | 1 | Hold | — | — |
| **B** | 1 | **React** — the body is shaken; forced-return test | `PSY 6 + Psychic Defence 3 + 1d10(6) = 15` vs 15 — holds | Noöspace |

Three things the example is meant to show:

1. **One clock.** The dive, the conversation, the sentry and the projection all spend from the same
   three-AP budget in the same order.
2. **The single-locus rule is visible.** A cannot also shoot, and B acts in Noöspace while B's body
   is in the room and does nothing.
3. **No gateway, no crossing.** D cannot reach A's mind — the dive rig is hardened, so the wetware
   rung is unreachable however well D rolls. B cannot reach the clinic's network, because no
   general Noöspace→cyberspace gateway exists. The guard on those two lines is the point of the
   section.

## What this section deliberately does not do

- **No combat detail** — damage, wounds, armor, cover values and tactical positioning are #219.
- **No hardware statistics** — COMPUTE/INTERFACE/NETWORK ratings are #221/#228.
- **No PSI power list** — powers and permissions are #223.
- **No astral procedure** — projection, navigation and encounter rules are #224.
- **No new Skills, STATs or derived statistics.** The contract spends AP and uses existing Skills.
- **No fork of initiative.** A later pass may refine the ordering; it may not define a second one.

Nothing here calibrates the author's numbers. The AP cost, the 3-AP budget, the REF ordering, the
forced-return difficulty and every DRAFT value above are **proposals for playtest**.
