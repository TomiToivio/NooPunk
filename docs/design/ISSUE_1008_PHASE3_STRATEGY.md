# Phase 3 plan: faction strategy on an unmodified SWN engine (#1008)

**Status: plan. Not implemented.** The strategic layer is the last thing built, after the solo game is playable.

> **Citations.** Page references below are the ranges the author's brief supplies (#1008): *SWN Revised Deluxe*
> Factions chapter from printed p. 211, *Houses of the Landsraad* House Management from printed p. 86, CWN
> Deluxe for skills/reactions/schemes/Heat. **This repository holds no copy of those books.** Nothing here is
> quoted, and every page number is recorded as an author-supplied pointer to be verified against the licensed
> text before implementation, not as a verified citation.

## The non-negotiable boundary

**SWN Revised faction rules are the strategic core, unmodified**: Force / Cunning / Wealth, faction hit points,
FacCreds, experience and goal rewards, faction tags, assets and their movement, upkeep, the action list, faction
turn sequencing, attack and defence, and destruction. Adaptations happen **at the boundary** — which NoöPunk
entity owns which asset, where it sits, what an asset is called in 2045 — and never inside the procedure.

One faction action per faction turn stays one. A player's mission is not a faction action, and a high rank does
not buy a second one. That is the single most likely corruption of this engine, so it gets a test.

## The three clocks, kept apart

| Clock | Who acts | Governed by |
|---|---|---|
| Mission | the PC and, later, a team | CWN resolution |
| Authorization | the chain of command (Phase 1 rank) | permission, resources, Heat |
| Faction turn | the factions, including UNSA | SWN faction rules |

A mission may *feed* a faction turn — create or damage an asset, advance a goal, change a tag — but only through
an explicit bridge that spends the faction's own action budget. Missions must never mint free faction actions.

## Agent and architect views

Dune's *agent versus architect* distinction is the right **interface** idea and the wrong rules engine. Rank 0–1
sees the agent view: the case, the contacts, the orders. Rank 3–4 gains an architect view: a read-only picture of
the faction's assets, goals and standing, plus advice that the SWN engine may or may not honour. The switch is a
lens, not a new dice system — no 2d20, no Momentum, no Truths.

## Tabletop sources worth borrowing from — and what exactly to borrow

**Strategy board games**

- **Twilight Struggle** — a *tension track*. Borrow the DEFCON idea as a global Heat dial that everyone must watch:
  the cheapest way to make escalation feel costly. Do not borrow its card-driven turn structure; SWN owns turns.
- **Diplomacy** — *simultaneous hidden orders and betrayal*. Borrow for NPC factions resolving at once, which
  makes scheming legible without a GM. Do not borrow the no-dice determinism; SWN rolls.
- **COIN series (e.g. *Cuba Libre*, *Andean Abyss*)** — *asymmetric action menus*. Government and insurgency do not
  play the same game. This is the best available model for UNSA versus criminal networks versus rogue entities,
  and it maps cleanly onto "each faction has its own asset list". Do not import the full COIN board topology.
- **Pax Pamir (2nd ed.)** — *shifting loyalty to coalitions*. Loyalty as a position you can move, not a team you
  join. The right shape for NoöPunk blocs that realign around signifiers.
- **Republic of Rome** — *internal politics inside a faction*: offices, influence, prosecution. Borrow the idea
  that a faction's own members are a hazard. It is also the best warning about bookkeeping bloat.
- **A Game of Thrones (2nd ed.)** — *orders placed face-down, then revealed*. Cheap suspense per turn.
- **Root** — *asymmetry on one shared map*, and a very good lesson in how much asymmetry players can absorb
  before the rules stop fitting in their heads.
- **Oath** — *a chronicle*: the board's history is written down and changes the next regime. Borrow for campaign
  logs that make an SWN faction's rise and collapse narratively real.
- **Dune: Houses of the Landsraad** (House Management, printed p. 86 ff. per the brief) — *ventures, holdings,
  boons, status, intrigue*: the vocabulary for a noble house's economy. **Interface inspiration only**; none of
  its mechanics replace an SWN procedure.

**Card games**

- **Android: Netrunner** — *asymmetric hidden information with a shared economy of pressure*. The best model for
  UNSA investigating something that is actively hiding, without either side seeing the other's board.
- **Illuminati** — *conspiracy as card control*, plus its comedy of bureaucratic absurdity. Closest in tone to
  NoöPunk's understated humour, and a warning about how quickly a joke mechanic becomes a spreadsheet.
- **Pax Porfiriana / Pax Renaissance** — *regime change through economic and political operators* rather than
  armies. Almost exactly the 2045 problem: power bought, not conquered.
- **The Resistance / Secret Hitler** — *hidden roles and accusation*. The mechanics for infiltrators inside UNSA
  and for the PC being unsure who is compromised.
- **Condottiere / Coup** — *bluffing with limited resources* at a scale small enough to sit inside a mission.

**What not to take from any of them**: player elimination, kingmaking as a designed outcome, or a second
resolution engine. SWN rolls the strategy; CWN rolls the person; nothing here rolls a third way.

## Implementation shape

- A deterministic faction-turn state machine with seeded rolls, persisted as JSON, and **rollback plus replay
  audit**: the same seed and the same orders must reproduce the same turn, or the audit is fiction.
- A periodic turn scheduler separated from player turns, so a faction turn can resolve while the PC sleeps.
- Fixtures: a three-faction scenario on the Helsinki map, with one goal each, run for ten turns in CI.
- Turn results become concrete quests, news, rumours and stakes — a faction action that produces no readable
  consequence for the player is a number moving in the dark.
- Start with the factions the PC can actually reach. Broad simulation is vanity until the local one works.
