# NoöPunk × LaclauGPT crossover — V1/2: faction management (design record)

**Status: PROPOSAL / design record. NOTHING HERE IS A RULE, A MECHANIC, A NUMBER OR CANON.**
Issue [#296](https://github.com/TomiToivio/NooPunk/issues/296); parent
[#282](https://github.com/TomiToivio/NooPunk/issues/282); depends on V1/1 leaders
([#295](https://github.com/TomiToivio/NooPunk/issues/295)); matched half is V1/3
([#297](https://github.com/TomiToivio/NooPunk/issues/297), record:
[`V1_DISCOURSE_AND_NETWORK.md`](V1_DISCOURSE_AND_NETWORK.md));
[`strategy_game/RULEBOOK.md`](../../strategy_game/RULEBOOK.md) still says **NO RULES APPROVED**.
Gate C in [`RULE_SYSTEM_RESEARCH.md`](../../strategy_game/docs/RULE_SYSTEM_RESEARCH.md) is open.

This file is the **consolidated record** for the faction-management half. It does **not** restate
the seven design comments already on the issue — it takes the parts they converged on as *proposals*,
names the one open fork in each area, and adds the deliverable the thread was missing: a **computed**
bookkeeping budget (§4) that decides the design, rather than an estimate that assumes it. Where this
file and a comment disagree, this file is the later reading; where this file and the author disagree,
**the author wins and this file is stale.**

Read alongside: [`VISION.md`](../VISION.md) §3 (zoom levels), §7b (the MVP and the "one loop" cap),
[`NOOPUNK_GLOBAL.md`](../NOOPUNK_GLOBAL.md) §7 (the six quantities) and §9 (the counted turn),
[`LEADER_COUNCIL_SYSTEM.md`](../../strategy_game/docs/LEADER_COUNCIL_SYSTEM.md) §1 (one named leader
per move), and [`POLITICAL_SIMULATOR_SCOPE.md`](../../strategy_game/docs/POLITICAL_SIMULATOR_SCOPE.md).

---

## 0. What this half is, in one paragraph

A tiny, fast, faction-scale board game, **not** grand strategy: a few factions, each an object with a
leader, one objective, a very small set of faction tracks, a handful of numberless asset cards and
allies/rivals; an abstract board of *positions and institutions*, never a hex map; one event per round
and a small fixed operation menu whose actions are **exclusive** (one leader, one verb, one target
slot, one stake). It is the *Organization/faction* and *Society/district* row of `VISION.md` §3's table
seen close — the same `WorldState` the God's-eye map reads, projected, never a second engine.

**The one subtraction, kept.** Dune's House sheet is a menu of many resource-ish traits; this layer
takes **three**. Three is the smallest set in which a faction must make a *trade* (capable and
illegitimate, legitimate and brittle, or united and broke). No economy: nothing has a price, spending is
track movement, and an asset is used or lost, never bought.

---

## 1. The faction card — three tracks, and the §7 mapping that must hold

`NOOPUNK_GLOBAL.md` §7 fixes **six quantities that must stay distinct** and forbids one generic
"influence" scalar. A three-track faction card is exactly where that collapse happens quietly, so the
tracks are chosen to be **representations of named quantities**, not new meters:

| Track (names as proposed by the thread) | Represents | §7 quantity | Not |
| --- | --- | --- | --- |
| **Capacity** | members, volunteers, funds, equipment, reachable means | **#2** organizational membership / resources | a currency ledger |
| **Standing** | how legitimate and credible the faction looks to others — its ability to reach and be heard by an institution interface | **#5** institutional access | **not** ownership, **not** popularity, **not** hegemony |
| **Cohesion** | whether the faction holds together internally | **representation only — see below** | morale points |

**The track-name finding, recorded.** One proposal on the thread named the tracks *Influence /
Capacity / Cohesion*. **"Influence" cannot be a faction track name.** §7 says it in its own words — a
single influence scalar "would collapse exactly the distinctions the theory and the acceptance criteria
require". A track literally called *Influence* either **is** that collapse or is a misnamed #5; a reader
cannot tell which. The names that survive the mapping are **Capacity / Standing / Cohesion**, and
Proposal A's warning should be **printed on the card**, not only in a rulebook: *Standing is institutional
standing, not a scientific Laclau hegemony index.*

**Cohesion is the honest problem with every three-track proposal.** Cohesion is **not one of §7's six
quantities**, and §9.3 allows "exactly six quantity conventions + at most a few status tokens — no
seventh meter". So Cohesion is legitimately either (a) a **status token/tag** (legal) or (b) a **seventh
metre**, which requires the author to say so explicitly. **This record assumes (a) — a token — and routes
the choice to the author (§8).** It does not invent a seventh metre.

**Every number on the card is a draft proposal.** Track ranges (0–5, 0–6, 0–3 across the thread's
proposals), starting values, and the operation difficulties (7/9/11) are **the thread's proposals for the
author to select among** — not values this record introduces. This record adds no number of its own.

**Assets are numberless cards.** One generic shape: `id`, a `label`, one **kind tag**
(`institution` / `operative` / `channel` / `research` / `holding`), **no numeric statistics** — permission
plus a tag, spendable/exposable. `core.Asset` today carries only `identifier, label, location_id,
owner_faction_id`; the `kind` tag is an **additive field proposal** (see §7).

**Positions are abstract, not geographic.** A few abstract positions (e.g. Capital / Port / Media Hub /
Institution). **No hex map, no adjacency, no movement, no territory control** — binding per the issue and
per #302/#303.

---

## 2. One resolution mechanism — §7b's hard cap, and not a style choice

`VISION.md` §7b: *"One resolution mechanism, reused everywhere — not one per pillar."* This half may
therefore **not** pick its own die. As it stands, the pair carries several candidate mechanisms across
both threads (a `2d6 + attribute vs 7/9/11` check; a `2d6 + Reach vs 9/11` check; a die-free graph-distance
chain; a fully deterministic card-driven variant). **Choosing one mechanism for both halves is a Gate A/C
author decision.** This record does not select one.

What the repo already provides, so the choice is cheap either way:

- `strategy_game/tabletop/dice.py` supplies **notation, an injectable seeded RNG, a per-die breakdown and
  a `RollLog` that stores faces** so `replay()` reconstructs results without touching the RNG — and
  deliberately **no resolution** (no difficulty, no target number, no opposed check). "We have dice" is
  true; "we have a check" is not.
- The die-free candidate needs **no new primitive**: `Board.neighbors`, an edge list and hop counting are
  standard library, so it is reproducible with no randomness in the campaign chain at all.

The interface between the halves is a **typed outcome record**, not a call into the other half's rules
(§5). The resolver is the sole writer of resolved state (`VISION.md` §13).

---

## 3. The counted turn — the computed bookkeeping budget

**This is the deliverable this thread was missing, and it is the finding.** §9 of
`NOOPUNK_GLOBAL.md` sets a *counted* physical budget: **≤ ~40 discrete bookkeeping updates**, **~4–6
rolls**, **~12–20 lookups per turn**. Three proposals on the thread say "no bookkeeping phase"; none
counts against that budget. Below it is counted, and the design is read off the count.

### 3.1 The measurement model (PROPOSED measurement assumptions, to falsify by playtest)

Per **round**, physical paper, **f** factions each taking **k** actions, with the V1/3 discourse campaign
**integrated as one of the faction's k actions and sharing its roll** (the reason is §4):

| Stage | Physical operations | Counts as |
| --- | --- | --- |
| Event | 1 card drawn + 1 read + ~2 effect applications | 4 **updates** + 1 **lookup** |
| Per faction — declare k actions | k action cards placed + k leaders marked busy | 2k **updates** |
| Per faction — resolve | k track/asset writes + k asset flips (the campaign's alignment-marker write, when integrated, is folded into this) | 2k **updates** |
| Per faction — resolve (read) | modifier card + threshold table, per action | 2k **lookups** |
| Per faction — end of round | 1 asset restored + 1 status cleared | 2 **updates** |
| Per faction — resolve (roll) | one roll per action | k **rolls** |
| Per faction — static read | status/asset check at end of round + the six-quantity read | 2 **lookups** |
| Six-quantity pass | only the quantities this round touched | 1 **update** |

Which gives, in closed form:

```
rolls   = f·k                          (+ f  when the campaign is a separate resolution step)
lookups = 2·f·k + 2·f + 1
updates = 4·f·k + 2·f + 5
```

### 3.2 The counts — re-derived, not copied

| Configuration | updates | rolls | lookups | Against §9's budget (≤40 / 4–6 / 12–20) |
| --- | ---: | ---: | ---: | --- |
| 3 factions × **3** actions | **47** | **9** | **25** | **over on three bands at once** (updates, rolls, lookups) |
| 3 factions × **2** actions (campaign **integrated**) | **35** | **6** | **19** | **inside every band** |
| 3 factions × 2 actions, campaign as a **separate** step | 35 | **9** | 19 | **over on rolls** |
| 2 factions × 2 actions | 25 | 4 | 13 | inside every band |
| 3 factions × 1 action | 23 | 3 | 13 | inside; 3 rolls sits *under* the 4–6 band (fewer rolls is not a problem) |

Every figure above follows from the three formulas; none is carried over unverified. Spot-checking:
`3×2 integrated` → rolls `3·2=6`; lookups `2·6+2·3+1=19`; updates `4·6+2·3+5=35`. `3×3` → rolls `9`;
lookups `2·9+2·3+1=25`; updates `4·9+2·3+5=47`.

### 3.3 The three findings, stated rather than smoothed over

1. **Three actions per faction does not fit.** At 3 factions it lands at **47 updates / 9 rolls / 25
   lookups** — over the physical cap on **three of the five bands simultaneously**. **Two actions per
   faction fits**, with ~5 updates of headroom. (So the thread's "3 actions" and "2–3 actions" proposals
   are, at three factions, on the wrong side of §9's own line.)
2. **Splitting the campaign into its own resolution step breaks the roll budget.** It takes the roll
   count from **6 to 9** — over §9's 4–6 — for **no gain in decision quality.** Even granting the
   generous assumption that a separate campaign step adds *no* updates (it should add some), it is
   **still over on rolls**, so the conclusion does not depend on that assumption. *This is the
   bookkeeping argument for **one shared resolver across both halves**, and it is why §7b's "one
   resolution mechanism, reused everywhere" is not merely aesthetic: **one shared resolver is both the
   §7b "one loop" requirement and the bookkeeping answer.***
3. **Leader count is a hidden cost.** At the repo's proposed **four leaders per faction**, twelve leader
   cards exist and each needs a status check every round even when only six act. Four leaders is a
   *roster* choice ([#323](https://github.com/TomiToivio/NooPunk/issues/323)'s business, and the
   4/7/11 roster discrepancy is deliberately **not** resolved here), not a bookkeeping optimisation; this
   record counts it, it does not change it.

**Session length.** At §9's **≤8 min/turn** physical target, **3 rounds = ≤24 min** (inside the issue's
**20–30 min** acceptance); **4 rounds = ≤32 min** (outside it). So a **three-round envelope** is what the
acceptance criterion actually supports — a prediction to falsify by playtesting, not a chosen rule.

### 3.4 Where this design must not quietly assume a computer

The honest limit, stated because it is the easiest thing here to fake:

- **Derived graph quantities cannot be hand-counted.** `NOOPUNK_GLOBAL.md` §8.4 is explicit: reach,
  brokerage and centrality are *computed and shown, not held*. On paper, **counting hops along a ~10-edge
  list is one hand action** — hand-doable. **Betweenness or brokerage across 3 factions + 3 institutions +
  2 audiences is NOT.** Therefore, in the **physical** game, **brokerage must be an authored tag on an
  organization card** ("this one is the broker"), **or the layer must declare itself display-only.** It must
  **never** be presented as a number a player reads off a graph by hand.
- **The paper version is primary.** `AGENTS.md` §3/§14 and #303's physical-tabletop criterion both require
  the mechanic to be expressible with cards, tokens and one die decision *before* it is code.
- **Digital is a port** and may do more (automated expiry, computed reach, the log). What it may **not** do
  is *become the definition* of a paper mechanic no one can execute.

---

## 4. One loop, not two halves — the typed interface

`VISION.md` §7b: the pillars must **feed each other in one loop**; three disconnected mini-games sharing a
menu is a failed MVP. The circuit a player can see:

```
leader choice (#295 leader card, one named leader per move)
  → faction operation (this half: one verb, one slot, one stake — its roll IS the campaign roll)
    → emitted as a typed outcome record (actor, target, band, delta, provenance=SIMULATED)
      → the discourse half reads it as a campaign (#297: channel tie → reach → reception → alignment)
        → a §7 quantity moves (support marker / access token / articulation edge / new frontier node)
          → that movement is the next round's event or the next leader dilemma
```

**The two halves exchange a typed record, not each other's rules.** That is what lets the faction rules
(Gate C) and the political assumptions (Gate B) be approved *separately* while still forming one loop, and
it keeps the resolver the sole writer of resolved state. Both halves must be **simulated**, not one
simulated and one narrated — §7b's test (*removing any pillar obviously breaks the game*) is the check.

**Exclusivity is the whole tension, and it needs no anti-idle patch.** One leader, one verb, one target
slot, one stake per action, with the action count smaller than the number of things worth doing. That
delivers "you cannot do everything", player-vs-player consequence without combat/territory/trade, and the
"no idle turns" guarantee **structurally** — a faction that declines to act loses slots visibly. The
thread's anti-idle *rules* (a forced free Organise; "no round ends with an unchanged `board_view`") work,
but they patch a design that can idle; exclusivity plus a fixed small action count means there is nothing
to patch. If the author keeps one idea from this half, this is it.

---

## 5. The six quantities, kept distinct — what is simulation and what is representation

The acceptance criterion, and the discipline that stops the collapse. On the card/board:

| Thing on the card/board | Classification | §7 quantity | Why |
| --- | --- | --- | --- |
| **Support markers** per area/constituency | **simulation** | **#1** opinion/support | moves only when a named rule resolved |
| **Capacity** (faction pool/tableau) | **simulation** | **#2** membership/resources | §7: **amplifies** a leader-led action, **never** buys an extra action |
| **Office markers / seat markers** | **simulation, only if an election or office window fires** | **#3** seats, **#4** office | board slots, **not** faction-card tracks; two distinct quantities |
| **Access tokens** on institution-interface cards | **simulation** | **#5** institutional access | ability to *reach and be heard by*, **not** ownership |
| **Standing** track | **simulation** (a representation of #5) | **#5** | not popularity, not hegemony — printed on the card |
| **The articulation graph** (signifier → demands, where the frontier runs) | **simulation**, and the **only** one with **no number in it at all** | **#6** Laclauian hegemony | its home is the political layer itself (§3/§7 of #297's record) |
| **Objective line, ally/rival labels, asset tags, leader trait tags** | **representation** | — | authored labels a player reads; assert nothing about the world, carry no number |
| **Cohesion** (if kept) | **representation only** | — | a status **token**, unless the author rules a seventh metre |

**Nothing on the card is a seventh quantity, and nothing collapses two of the six into one.** Anything the
card shows that is not in this mapping must be **labelled representation on the card itself** — a labelling
discipline a player can check, not a rule.

---

## 6. Reconciliation with what is already on `main`

- **`core.py` is the container; do not extend `local_slice.py`.** `local_slice.py` carries parallel
  `Leader`/`Party`/`Relationship`/`Mission`/`Game` dataclasses, separate from `core.py` — a second state
  engine. Everything this half proposes uses `core.Faction`, `core.Asset`, `core.Location`,
  `core.NetworkEdge`, `core.Event` and their proposed *additive fields*.
- **⚠ Latent defect — do not inherit it.** `local_slice.Party` declares `treasury: int`, `legitimacy: int`
  and **`network: int`**. The first two are at least recognisable as #2 and #5. **`network: int` is network
  power stored as a scalar stock** — the exact shape [#297](https://github.com/TomiToivio/NooPunk/issues/297)
  forbids, because Castellsian power is *shape*, not an amount. It is inside an unapproved prototype, not
  canon, and **this record does not touch the file** — but **if the V1 design copies that field name, the
  collapse happens by inheritance.** Recorded as the author's call.
- **`core.Asset` has no `kind` tag today.** The `institution / operative / channel / research / holding`
  tag is an additive-field proposal needing approval — flagged, not assumed.
- **A numeric resource already exists elsewhere.** `test_global_slice.py` asserts
  `world.resources[0].quantity == 2`, i.e. a numeric resource exists in the *global* slice prototype. So
  "no numbers in the faction layer" is true of `Faction`/`Asset` and **false of the tree as a whole** —
  worth knowing before the vocabulary is frozen.
- **#302 / #303 are unapproved and assumed as card types.** #302 proposes `Organization` and `Audience` as
  new records and systems as *passive lenses*; #303 requires population groups, areas and organizations
  never to be merged or double-counted. This half's board keeps "area card" and "constituency card"
  **separate** rather than inventing a generic "population unit".

---

## 7. Pending author choices — routed, not decided

1. **Track names and count** — Capacity/Standing/Cohesion (proposed; the only names that survive the §7
   mapping) and **two or three**? Two is leaner; three gives Cohesion a currency for the anti-idle story.
2. **Is Cohesion a status token or a seventh metre?** §9.3 permits the first and requires the author's
   explicit word for the second. (This record assumes a token.)
3. **Which single resolution mechanism both halves share** (§2), and whether `tabletop/dice.py`'s substrate
   is used for it or the die-free graph comparison replaces dice entirely.
4. **Does the #297 campaign count as one of a faction's two actions, or is it a separate step?** The
   bookkeeping answer is **integrate** (rolls 6 vs 9) — this is the pair's single most consequential shared
   decision.
5. **Action count** — 2 (fits, §3.3) or 3 (over budget at three factions)?
6. **Does the V1 include an election/office window at all** (#3/#4)? If not, two of the six quantities are
   dormant in V1 — worth saying out loud rather than discovering at playtest.
7. **One concealed thing per faction, or fully open information?** (`tabletop/cards.py` already carries
   `CardVisibility`; the "intrigue" transfer shrinks to one hidden thing per faction.)
8. **Three rounds or four?** The 20–30 min acceptance supports three at ≤8 min/turn.
9. **Does the physical game ever need brokerage as a computed number, or is it always an authored tag?**
   (§3.4 — on paper it must be a tag or display-only.)
10. **Win / end condition** — deliberately not proposed here, consistent with the thread.
11. **The `local_slice.py` `network: int` field** — the author's call (§6).

---

## 8. Why no code landed with this record

`strategy_game/RULEBOOK.md` says **NO RULES APPROVED**; Gate C is open; the issue's own work list says
**"Confirm chosen rules before coding."** Every number above is a proposal. Landing a `faction.py` resolver
now would implement unapproved mechanics, which `AGENTS.md` §0/§1/§2/§14 forbid. The implementation shape
remains a proposal (faction container, the six operations, one resolver, outcome→delta mapping, the event
table, the turn sequencer — reusing `core.py`, emitting `Provenance = SIMULATED`), to be built **after** the
author selects the rules. This record lands the **design and its counted budget**, which is what the design
gate asks for, and nothing executable.

---

*Cross-refs: #282 (parent), #295 (leader contract this half consumes), #297 (matched half),
#302 (organizations/audiences as records), #303 (agent ecology and the physical-tabletop criterion),
#323 (leader council / roster), #347 (`tabletop/` — the rule-free substrate). Everything here is a
proposal; nothing is approved and no rule, number or canon is created.*
