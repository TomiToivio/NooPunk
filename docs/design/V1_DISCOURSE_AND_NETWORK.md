# NoöPunk × LaclauGPT crossover — V1/3: discourse and network power (design record)

**Status: PROPOSAL / design record. NOTHING HERE IS A RULE, A MECHANIC, A NUMBER OR CANON.**
Issue [#297](https://github.com/TomiToivio/NooPunk/issues/297); parent
[#282](https://github.com/TomiToivio/NooPunk/issues/282); reads V1/1 leaders
([#295](https://github.com/TomiToivio/NooPunk/issues/295)); matched half is V1/2
([#296](https://github.com/TomiToivio/NooPunk/issues/296), record:
[`V1_FACTION_MANAGEMENT.md`](V1_FACTION_MANAGEMENT.md)).
`politics.py` and `political.py` are **not reconciled here**, no third vocabulary is added, and
[`strategy_game/RULEBOOK.md`](../../strategy_game/RULEBOOK.md) still says **NO RULES APPROVED**. Gate B
in [`RULE_SYSTEM_RESEARCH.md`](../../strategy_game/docs/RULE_SYSTEM_RESEARCH.md) is open.

This file is the **consolidated record** for the discourse/network half. It does **not** restate the seven
comments already on the issue; it takes the three things they agree on as *proposals*, then adds the
grounding in the code actually on `main`, because this layer's hardest constraints are **executable** (they
are asserted by tests, not prose). Where this file and the author disagree, **the author wins.**

**No LaclauGPT runtime dependency.** The theory is vocabulary and a legibility discipline, never a
validated transition law. One sentence for the layer's docstring: *the theory tells us which distinctions
matter and what would be dishonest to claim; it does not tell us what happens next.*

Read alongside: [`NOOPUNK_GLOBAL.md`](../NOOPUNK_GLOBAL.md) §7 (the six quantities) and §8.4 (derived
quantities computed and shown, not held), [`POLITICAL_SIMULATOR_MODEL.md`](../../strategy_game/docs/POLITICAL_SIMULATOR_MODEL.md),
[`POLITICAL_SIMULATOR_SCOPE.md`](../../strategy_game/docs/POLITICAL_SIMULATOR_SCOPE.md), and
[`INTEGRATION_BOUNDARIES.md`](../../strategy_game/docs/INTEGRATION_BOUNDARIES.md).

---

## 0. The three agreements, taken as proposals

The thread already agrees on three things, and this record does not re-argue them:

- **No single hegemony number.** Every proposal refuses one, and so does the issue body ("no universal
  single 'hegemony number' necessary").
- **Reception must not be a roll.** *Articulation is not persuasion* — a die makes "they didn't want it"
  indistinguishable from "the dice said no".
- **Only a declared frontier permits opposition.** Mere disagreement is not antagonism; making that a
  *precondition* is the clearest case of the theory improving play rather than decorating it.

What follows is the discipline that keeps all three honest as code.

---

## 1. The no-number discipline — a rule may be numeric while its result is structural

The issue says a rule may be numeric while its **result** is structural, and that giving hegemony a number
**imports support or access into it**. That is not a preference here; it is asserted:

```python
# strategy_game/tests/test_political_layer.py :: NoQuantifiedPoliticsTests
RECORDS = (Demand, Signifier, Formation, Frontier)
METRIC_TOKENS = ("score", "strength", "influence", "threshold",
                 "weight", "probability", "rating")
# 1. no field of those four records may have type int or float
# 2. no field NAME of those four records may contain a metric token
```

Read as a **design constraint**, the guard says three specific things:

1. **A numeric channel reach cannot live on a discourse record.** Not `Signifier.reach`, not
   `Frontier.strength` — and not a field merely *named* `influence_strength` or `reach_weight`, because the
   guard checks **names as well as types** (`influence` is itself one of the tokens).
2. **Therefore numbers live in exactly three places, all visible:**
   (a) **inside a rule's comparison**, computed at resolution and **stored nowhere** — §8.4's *"computed and
   shown, not held"*;
   (b) **in authored scenario or asset data**, e.g. a channel's reach as a scenario value;
   (c) **in the rule's own constants** (a threshold), which need Gate B like everything else.
   The guard's own comment anticipates the change and asks for it to be made **deliberately**: *"A future
   rule may legitimately need a number. If that day comes the guard should be changed deliberately, with the
   rule and its approval, rather than the quantity slipping in unnoticed."*
3. **The recorded result must be structural.** Concretely, the effects this layer would record are:
   **an audience alignment marker flips** between three values; **a `Signifier.kind` relabels**
   (`unspecified → nodal`); **an edge appears** (an `articulation` placed, an `equivalence` drawn); **a
   frontier node is declared**. Nothing in the effect list is "a number went up".

### 1.1 What "hegemony" gets, if not a number

It gets **a shape and a sentence** — the direct answer to `POLITICAL_SIMULATOR_MODEL.md`'s own open
question 5 ("what makes a hegemonic shift legible to a player without pretending political change is a
measured score"):

> A hegemonic shift is legible as **a change of shape plus a sentence**: *this signifier now carries that
> chain; the frontier now runs here; the commitment of that audience moved one step.* If the player cannot
> point at the edge, the relabelled kind, or the moved marker, no hegemonic shift happened — and if you want
> to show that a faction's position weakened, you show that **its signifier lost demands** rather than that a
> **meter fell**.

The load-bearing §7 sentence is: *"A faction can hold the #6 nodal signifier and lose everything else —
hegemony in meaning is not power."*

### 1.2 The one sibling move this record argues against

Proposal A on the thread proposes audience alignment on a bounded **−2…+2** scale. That is the one design
move to argue against, and not because it is "more nuance": §7 gives **opinion/support (#1)** its own
quantity and its own home — **per-jurisdiction support markers**, locally scoped. A numeric per-faction
alignment inside the discourse layer is therefore **a second home for #1** — the collapse the six quantities
exist to prevent, wearing a finer grain. The **3-value marker** is not a simplification of the same thing; it
is a *different* thing — a reading of **commitment to an articulation**, not a measurement of how many people
agree. If a finer grain is wanted, it should be asked of **#1's home**, not added to **#6's**.

---

## 2. The articulation graph carries no quantities — and the two-vocabulary fork

### 2.1 The fork, measured from `main`

`VISION.md` §12 Step B: one decision, *"one agreed representation, no silent loss of existing records."*
This record does **not** make that decision. It reads both modules and states the concrete consequences of
each choice. These are not stylistic differences; each one changes what a rule can be written against:

| | `politics.py` | `political.py` |
| --- | --- | --- |
| Signifier's unclassified default | `SignifierKind.UNSPECIFIED`, literal value **`"unspecified"`**, the enum default | `Signifier.role: SignifierRole \| None = None` — **`None`**, no enum member |
| Enumerated roles | `unspecified / nodal / floating / empty` | `nodal / floating / empty` (**no** unclassified member — absence is `None`) |
| `Frontier` shape | a **node**: `identifier, label, provenance`. No signifier ref, no demand lists | `identifier, signifier_id, included_demand_ids[], excluded_demand_ids[]` — names **the signifier and the excluded demands** |
| Castells programming / switching | **absent by statement.** `RelationLayer.COMMUNICATION`'s docstring: *"Network-making, programming and switching are not modelled here — only the presence of a tie is recorded."* | **present**: `PowerMode.PROGRAMMING / SWITCHING` on `CommunicativeTie` |
| Wired into `WorldState` | **yes** — `core.py` imports `Demand, Formation, Frontier, Signifier` from `.politics` and carries them as four collections | **no** — `test_political_contracts.py` asserts `"political_field"` is **not** in `state.__dict__` and **not** in `state.to_dict()` |
| Numeric-field guard | `test_political_layer.py::NoQuantifiedPoliticsTests` covers `Demand, Signifier, Formation, Frontier` from this module | `test_political_contracts.py` asserts no numeric quantity and no metric-shaped key anywhere in `PoliticalField` |

**Two consequences on the record, because they are decisions disguised as details:**

- **Choosing `politics.py` loses programming/switching entirely.** The Castells half of #297 — "programming
  and switching as positions a faction holds, not as amounts of power it has" — has **no home** in
  `politics.py`. It exists only on `political.CommunicativeTie.mode`. So Step B is not cosmetic:
  **choosing `politics.py` means the Castells power-mode vocabulary must be re-homed or dropped**, and
  dropping it removes the only mechanism the layer has for *"this faction sets what the network carries"* as
  distinct from *"this faction is well connected"*.
- **Choosing `political.py` changes an existing executable test.** Its integration is pinned as *not done*
  by `test_political_contracts.py::IsolationContractTests::test_the_field_is_not_nested_into_world_state`,
  which asserts `political_field` is absent from `WorldState`. Joining it is Gate D; the pin is correct
  behaviour (it stops the join happening by refactor). Whichever way Step B goes, one of the two modules'
  guards changes, and that is a **code change needing approval** — not something a design record may slip
  through.

### 2.2 Which vocabulary this record assumes — and why, routed to the author

**This design assumes `politics.py`, in two parts:** (i) the four node records and `RelationLayer` labels on
existing `NetworkEdge` entries — because that is the shape `core.WorldState` already carries and
`view.board_view` already projects (political nodes appear as typed nodes alongside factions, political
relations as labelled edges in the **same** graph); and (ii) the frontier **as a node**, which
`POLITICAL_SIMULATOR_MODEL.md` records as a **legibility choice rather than a theoretical requirement**, with
the edge-vs-node question left in the author's hands. For the frontier's *content* — the excluded demands —
`political.py`'s field is the richer one, which is another reason the reconciliation is worth doing rather
than picking.

**This is a routed choice, not a settled one:**
**`politics.py` → programming/switching must be re-homed or dropped. `political.py` → an executable test
that pins "not wired in" changes (Gate D).** The author decides; this record only measures the cost.

### 2.3 Do not invent a third spelling

Proposals on the thread write the unclassified role as **"unrecorded"** (`role ∈ {unrecorded, nodal,
floating, empty}`). **That string is in neither module.** `politics.py` says `"unspecified"`;
`political.py` uses `None`. Adopting "unrecorded" as a *fourth enum value* creates a third spelling for the
same absence — the exact drift Step B exists to prevent. This record uses **`unspecified`** when it means
`politics.py`'s member and **absent** when it means "no value recorded", and introduces no synonym for
either. If "unrecorded" is preferred as a player-facing label, it should be a **label on the card**, defined
once as the rendering of `unspecified`, not a new enum value. **No third vocabulary.**

---

## 3. The one rule chain — reach → reception → opposition → limits, as a structural result

This is the mechanism the issue asks for: four steps, and the only randomness is an *optional* seeded event
deck (`random.Random(seed)`). The chain's **result is structural** (§1.3): a marker flips, a kind relabels,
an edge appears, a frontier is declared.

```
A faction plays ONE campaign: (signifier, audience) via a channel it holds a tie to.

1. REACH      reach the audience?          <-- the open fork (see §3.1)
2. RECEPTION  (no roll — a deterministic condition on an existing claim)
              Does the audience already hold a claim on some issue the signifier carries,
              with a stance MATCHING this campaign?
                yes -> ALIGNMENT marker moves ONE step in the campaign's direction
                no  -> no alignment change; the campaign MAY still re-role the signifier
                       (unspecified -> nodal) -- you won the WORD, not the audience
3. OPPOSITION only a rival holding BOTH (a) a tie to the SAME audience and (b) a DECLARED
              FRONTIER against that signifier may counter in the same round.
              One counter cancels one alignment step.
4. LIMITS     1 campaign per faction per round; a channel carries 1 campaign per round;
              alignment clamps at its ends.
```

- **Why step 2 has no roll.** *Articulation is not persuasion:* reaching an audience is not moving it.
  Making reception a deterministic condition on an existing claim keeps that distinction and makes the
  outcome explainable — *"it failed because no one there already wanted it"* is a sentence a player can act
  on.
- **Why step 3 requires a *declared* frontier.** *"Mere disagreement or dislike is not automatically an
  antagonistic frontier"* is a rule of the theory, and it becomes a rule of the game: **you cannot oppose a
  campaign unless you have declared what you are against.** This is what stops the layer collapsing into
  "everyone fights everyone".

### 3.1 The open fork at step 1 — reach as a die, or reach as a graph fact

The thread splits here, and this record does **not** resolve it:

- **Die-based:** `2d6 + Reach(channel)` vs a fixed near/far threshold; ties by higher Reach, then lower
  faction id.
- **Die-free:** `Reach[channel] >= hops(F, A)` over the communication graph (BFS), reception as the claim
  condition above, so `"position, not rhetoric"` is answerable *structurally* ("too many hops"), the whole
  chain is seed-reproducible with **no dice at all**, and no new primitive is needed — `Board.neighbors`, an
  edge list and hop counting are standard library. The die-free chain also lowers the roll count (§5), which
  is a genuine argument in its favour.

**This is a Gate A/C author decision**, and it is entangled with the shared-resolver decision (§5) — the two
halves cannot pick different mechanisms (`VISION.md` §7b).

### 3.2 Transparent explanatory output (required by the issue)

Every campaign emits a **trace record** — the only "AI-free explanation" the layer needs:

```
campaign c-4  f-coop → s-homes → a-port (channel: newsletter, Reach 1, +1 position)
  reach      ...                                RECEIVED
  reception  a-port holds (i-1, support); s-homes carries (i-1, support)   MATCH
  opposition none — no declared frontier on s-homes
  effect     (a-port, i-1): uncommitted → committed
```

A player can always answer *why*, and a reader can tell this is a **game result**, because the trace is
stored with `Provenance.SIMULATED` and never with `EVIDENCE`.

---

## 4. Network power as shape — a tie is a channel, and nothing else

`core.NetworkEdge` is `(source, target, layer)` — **no weight, no strength, no capacity**.
`RelationLayer.COMMUNICATION`'s docstring says only the *presence* of a tie is recorded, and
`political.CommunicativeTie`'s says *"the scaffold stores the relation and never derives reach or influence
from it."* Those two sentences are the layer's constitution. Four invariants any tiny implementation keeps:

1. **A tie is a channel, not a vote.** A connection permits reaching; it never means anyone agrees. Reach is
   a **precondition** that gates whether a campaign can address an audience. The player who fails gets *"it
   did not travel"*, not *"they disagreed"*. `VISION.md` S0-A states the boundary exactly: *"never conflate
   media reach with persuasion, or a game score with measured hegemony."*
2. **A tie is not a belief.** An edge asserts nothing about what either end thinks; an audience's stance
   lives in its own claims, as separate records. If edges and claims are allowed to imply each other, the
   graph becomes a mind-reading device and the trace stops being honest.
3. **A tie is not a resource — the defect a tiny implementation is most likely to ship.** If holding a
   channel both enables targeting **and** adds a bonus to reception, then reach and resonance have been
   welded together and the network layer has become a resource. **Either the channel gates the attempt (a
   structural reach fact) or it modifies the outcome (a resource) — never both.** The gating version keeps
   the layer honest, because *"your message did not travel"* and *"your message travelled and did not land"*
   are the two different facts this whole layer exists to distinguish.
4. **Centrality is not causation; brokerage is a precondition, not a multiplier.** A centrality figure is
   descriptive, boundary-dependent and non-unique — fine to **display**, never a modifier (§8.4:
   computed-and-shown, not held). A broker's honest power is that it *shortens or permits the path*: with the
   broker you can be heard at all; without it you cannot. A broker that also adds dice makes the biggest graph
   the biggest dice pool — the network layer quietly becoming the resource layer again. The same goes for a
   **structural hole**: the honest game fact is that the path is long or absent (a hop count or an unreachable
   audience), **not** a bonus for sitting beside the gap.

**One author question the repo has already written down:** `NetworkEdge` is undirected in practice, while
articulation is asymmetric between signifier and demand (`POLITICAL_SIMULATOR_MODEL.md` open question 2). If
a campaign traverses edges as channels, direction can matter (a broadcaster that cannot be answered is a
different fact from a two-way tie), and the current edge type does not say.

---

## 5. One loop, one resolver — this half cannot pick its own mechanism either

`VISION.md` §7b's hard cap — *"One resolution mechanism, reused everywhere — not one per pillar"* — is the
**same finding** V1/2's counted budget reaches from the other side:

- The pair currently carries several candidate mechanisms across both threads. **If one half owns one and the
  other owns a different one, the pair has become the "three disconnected mini-games sharing a menu" §7b
  calls a failed MVP** — because the player would learn two resolution languages to play one loop.
- **The counted turn** (V1/2 §3, re-derived there from the measurement model): a three-faction round with
  **two** actions per faction and the campaign **integrated as one of them, sharing its roll** lands at
  **~35 updates, 6 rolls, ~19 lookups — inside every band** of `NOOPUNK_GLOBAL.md` §9. Making the campaign a
  **separate** resolution step takes the same round to **9 rolls — over §9's 4–6** — for no gain in decision
  quality. So *"integrate the campaign into the faction action"* keeps the pair inside the physical budget.
  If the die-free chain is chosen instead, the roll count drops further and the headroom grows.
- **Therefore one shared resolver is both the §7b "one loop" requirement and the bookkeeping answer.** It is
  the same conclusion from both halves, which is why it is the pair's most important joint decision.
- **The interface is a typed record, not a call.** V1/2 emits an operation outcome (actor, target, band, delta,
  `provenance=SIMULATED`); this half reads it as a campaign and returns a trace. That lets the faction rules
  (Gate C) and the political assumptions (Gate B) be approved *separately* while forming one loop, and keeps
  the resolver the sole writer of resolved state (`VISION.md` §13).

---

## 6. Simulation vs representation, and the six quantities kept distinct

| Thing in this layer | Classification | §7 quantity | Note |
| --- | --- | --- | --- |
| **The articulation graph** (which demand hangs on which signifier, where the frontier runs) | **simulation**, and the **only** one with **no number at all** | **#6** Laclauian hegemony | its home *is* the graph; this is the layer's core |
| **Alignment marker** `(audience, issue) → {opposed, uncommitted, committed}` | **simulation** (a 3-value reading of *commitment to an articulation*) | **#6**, **not #1** | **not** opinion/support — see §1.2 |
| **Audience claims** (the audience's own stance records) | **simulation** | — | a claim, not a population's opinion |
| **Communicative tie / channel** | **simulation** — *presence only* | — | reach as **shape**, never an amount (§4) |
| **Reach** (a channel's strength, if used as a rule constant) | **authored scenario value / rule constant**, never stored on a discourse record | — | §1.2 |
| **Institution access tokens** | **representation of #5** in V1/2's half | **#5** | **not** this layer's business; reaching a broadcaster ≠ owning the media system |
| **Support markers** per jurisdiction | **simulation**, but #1's home is elsewhere | **#1** | this layer makes **no statement** about how many people agree |
| **Issue cards, signifier labels, `unspecified/nodal/floating/empty`** | **representation** (descriptive labels) | — | the engine never infers a role |
| **Provenance class (fictional / simulated / sourced)** | **representation with a rule** | — | load-bearing: game output `SIMULATED`, history `EVIDENCE`, invented scenario `AUTHORED`, never conflated |

**Nothing here collapses #1, #2, #5 and #6 into one number.** Built on, not just stated — three rules the
implementation is held to:

1. **An `antagonism` edge is not a vote against, and a `communication` edge is not agreement.** Neither moves
   any marker by itself; otherwise "who talks to whom" silently becomes "who supports whom".
2. **No quantity in this layer may be *derived from* another layer's quantity.** Access (#5) does not become
   resonance; support (#1) does not become commitment; membership (#2) does not become reach. §7's explicit
   non-identities are the test cases, and each is a bug the layer should be **unable to express**.
3. **A faction may be strong in this layer and lose everywhere else**, and the game must show that state
   without it reading as an anomaly. If the design ever makes discourse power *convertible* into influence,
   it has broken §7 in one move.

**Where a number is tempting and should still be refused:** a per-faction "discourse power" figure for
comparison or matchmaking. That is a hegemony scalar with a different label; it would import support or
access into #6 and make the three quantities unseparatable in play.

---

## 7. Pending author choices — routed, not decided

1. **Which of the two vocabularies, and does programming/switching survive the choice?** (§2 — the decisive
   practical difference: `politics.py` drops it; `political.py` changes the "not wired in" test.) **Not
   decided here; no third vocabulary added.**
2. **Deterministic reach (a graph fact) vs a reach roll?** (§3.1 — entangled with the shared mechanism.)
3. **Does a channel gate the attempt, or modify the outcome — never both?** (§4.3. If the answer is "modify",
   the network layer *is* a resource and the reach/resonance distinction is gone.)
4. **Is the alignment marker state at all, or a view-time projection from claims?** A projection dissolves a
   record question entirely — worth considering before inventing a record.
5. **One shared mechanism across both halves — and if it is the die-free chain, is the layer then entirely
   without randomness?** (§5.)
6. **Does the campaign count as one of a faction's two actions (integrated), or a separate step?** (§5 —
   rolls 6 vs 9; this is the pair's single most consequential shared decision.)
7. **Is direction meaningful on a channel?** (`POLITICAL_SIMULATOR_MODEL.md` open question 2, unresolved.)
8. **Does `unspecified` ever relabel in play, and does the relabel cost the acting faction anything?** (A
   relabel is one structural write; the *cost* question is balance, not load.)
9. **Alignment scale — the proposed 3 values, or finer?** If finer, it belongs to **#1's** home, not #6's
   (§1.2).
10. **Where do `Audience` and `Organization` records live?** `core.py` has neither; #302 §6 proposes them as
    additive records. This design uses audiences as **authored scenario entities** and takes no position on
    the records. **Unapproved; inherited, not decided.**
11. **Win / end condition** — none proposed, consistent with #296.

---

## 8. Why no code landed with this record

`strategy_game/RULEBOOK.md` says **NO RULES APPROVED**; Gate B is open; the issue's own work list says
**"Confirm rule choices before coding."** Every mechanism above is a proposal, and the two-vocabulary fork is
an **unmade** decision (§2). Landing a `discourse.py` resolver now would implement unapproved mechanics and
would either pick a vocabulary silently or add a third — both explicitly forbidden. The implementation shape
remains a proposal (the campaign rule, the reception condition, the opposition check, the trace record —
reusing whichever vocabulary Step B selects, emitting `Provenance = SIMULATED`, standard-library playable,
NetworkX optional), to be built **after** the author selects the rules and reconciliation. This record lands
the **design and its executable constraints**, and nothing executable.

---

*Cross-refs: #282 (parent), #295 (leader contract), #296 (matched half and the shared resolver),
#302 (organizations, audiences, systems as passive lenses), #303 (constituencies/areas/organizations kept
distinct), #347 (`tabletop/` — the rule-free substrate both halves draw on). Everything here is a proposal;
nothing is approved and no rule, number or canon is created.*
