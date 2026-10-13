# Populism as a mechanism, patronage as a relationship, realignment as something the board shows (#305)

**Status: PROPOSAL / design record. NOTHING HERE IS A RULE, A MECHANIC, A NUMBER OR CANON.**

Issue [#305](https://github.com/TomiToivio/NooPunk/issues/305); parent [#282](https://github.com/TomiToivio/NooPunk/issues/282).
`strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**, Gates A/B of
[`RULE_SYSTEM_RESEARCH.md`](../../strategy_game/docs/RULE_SYSTEM_RESEARCH.md) are still open, and this
document changes no code and no data file. It **adds no third political vocabulary**: `politics.py` and
`political.py` are **not reconciled here** ([#301](https://github.com/TomiToivio/NooPunk/issues/301)).
It does not touch the legacy rulebook, does not resolve the global roster question
([`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §6B.3), and does not re-open
[#295](https://github.com/TomiToivio/NooPunk/issues/295) / [#296](https://github.com/TomiToivio/NooPunk/issues/296)
/ [#297](https://github.com/TomiToivio/NooPunk/issues/297) / [#302](https://github.com/TomiToivio/NooPunk/issues/302)
/ [#303](https://github.com/TomiToivio/NooPunk/issues/303) / [#304](https://github.com/TomiToivio/NooPunk/issues/304),
nor [#306](https://github.com/TomiToivio/NooPunk/issues/306).

**Tests.** Per [AGENTS.md](../../AGENTS.md) and [#271](https://github.com/TomiToivio/NooPunk/issues/271),
**no test, guard, CI step or schema lock may check any of this prose.** It is reviewed editorially and
by tabletop playtesting. Nothing here is implemented, so nothing here is covered by a test — and
nothing here should be.

**What this document is, and the one thing it adds.** The issue's four comments already establish the
groundwork: the research and its evidentiary status, the Wendt/Dolan reconciliation, the eight-task
plan, the three alternate non-far-right paths, and — in the fourth comment — the argument that a
paradigm-shift movement is an *operation on the articulation graph*. The landed scenario dossier
([`strategy_game/docs/PARADIGM_REALIGNMENT_SCENARIO.md`](../../strategy_game/docs/PARADIGM_REALIGNMENT_SCENARIO.md),
PR [#380](https://github.com/TomiToivio/NooPunk/pull/380)) already carries the cast, the branching acts,
the GM hooks and the epistemic labels. This document does not restate any of that. It does one thing:
**it writes the mechanism down as structure, so that "populism", "patronage" and "realignment" are
answers to *how*, not adjectives.** Every section below is a reading of vocabulary that is *already in
the repository*, marked as proposal.

**Register guard.** NoöPunk's register is wonder, not dread. This is the single most cliche-prone
territory in the genre, and §5 says so explicitly and declines the cliche by name.

---

## 0. What this consumes, and what it owns

| Consumed as given | Its home |
| --- | --- |
| The articulation graph and its four node kinds, four relation layers and four signifier kinds | `strategy_game/politics.py`; [`POLITICAL_SIMULATOR_MODEL.md`](../../strategy_game/docs/POLITICAL_SIMULATOR_MODEL.md) |
| The setting's own dislocation → order process | `data/paradigm_shifts.yaml`, `process:` |
| The **six quantities that must stay distinct** | [`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §7; `strategy_game/quantities.py` (names only — no value, weight or range) |
| The council's four offices, the mission shape that names **one** quantity, and the rule that a mission drawing on a **patron** must name an edge that exists | [`COUNCIL_LAYER.md`](../../strategy_game/docs/COUNCIL_LAYER.md) §3; `strategy_game/council.py` |
| The one **stateful relationship edge**, its `patron_of` kind and its named state vocabulary | `strategy_game/relationships.py` |
| The founder/patron edges as structure, with the canon Eldrich tie already transcribed | `strategy_game/data/founding_story.json` |
| The canon patron case: Sir Mars Eldrich and the LFP, and the LFP's stated asymmetry | [`PEOPLES_REPUBLIC_OF_UKWELI.md`](../world/PEOPLES_REPUBLIC_OF_UKWELI.md) §6; [`IDEOLOGICAL_FORMATIONS_2026.md`](../../strategy_game/docs/IDEOLOGICAL_FORMATIONS_2026.md) §5 |
| The fictional cast, the branching acts, the GM hooks and the source caveats | `PARADIGM_REALIGNMENT_SCENARIO.md` (landed, PR #380) |

| Owned here (as proposal) | Why it was missing |
| --- | --- |
| The **movement as a graph operation** — the equivalence chain and the `FLOATING → NODAL` conversion of one signifier (§1) | The vocabulary existed; the operation had not been written down |
| The **six-quantity reading of populism**, including the counter-motion between #6 and #3/#4 (§2) | §7 kept the quantities apart; nobody had said that populism *is* their divergence |
| The **patron edge's failure modes read as realignment**, and the timing argument (§3) | `founding_story.json` names the states; the realignment consequence was not derived |
| **Realignment legibility**: what changes, and the sentence that explains it (§4) | The issue's own acceptance criterion asks for legibility, not for a swing |
| The **anti-cliche statement** (§5) | Required in writing, not implied |

---

## 1. Populism is a mechanism, not a mood

The boring reading treats populism as a weather system a polity catches. The repository already has
the vocabulary to treat it as an **operation on the articulation graph**, and the operation has a
shape — which is what makes it playable rather than atmospheric.

### 1.1 The setting's own process

`data/paradigm_shifts.yaml` states, in its own `process:` list, the sequence the setting runs:

> `dislocation` → `competing_explanations` → `competing_signifiers_and_identities` →
> `chains_of_equivalence` → `political_frontiers` → `antagonism` → `attempts_at_hegemony` →
> `temporary_institutional_order`

A paradigm-shift populist movement is **not a new step in that list.** It is what it looks like when an
actor runs the list *deliberately and fast, on one signifier*. That is the whole design claim of this
section, and it is why the movement needs no new subsystem: it is a tempo, not an institution.

### 1.2 The operation, in the graph's own vocabulary

In `politics.py` terms:

- a **`Demand`** is a claim with a claimant — a grievance, an ask, a fear;
- **`RelationLayer.ARTICULATION`** links a demand to a **`Signifier`** *by content*: this demand, read
  through this word;
- **`RelationLayer.EQUIVALENCE`** links two demands *to each other*, by shared opposition rather than
  by shared content;
- **`RelationLayer.ANTAGONISM`** runs across a **`Frontier`**, which is a **node** — the boundary is a
  single thing a player can look at;
- **`SignifierKind`** defaults to **`UNSPECIFIED`**, and `FLOATING` means its meaning is *contested
  between competing chains*.

> **The operation:** a populist movement is an **equivalence chain** plus **one signifier being
> converted from `FLOATING` to `NODAL` for that chain.**

Nothing else. The movement does not need a flag, a meter, or a type of its own. It needs one signifier,
a set of demands, and the three conditions below.

### 1.3 Three things must happen, and each one costs

**1. A `Frontier` must be declared.** Not merely a disagreement. Two factions that both say *Human
Survival* while meaning opposite things are rivals only once one of them names a "them" and a
`Frontier` node exists. The chain is held together by the *opposition*, so until a frontier is drawn,
nothing forces one reading of the signifier and it stays floating.
**Cost: the frontier is exclusionary.** The act that gives the chain its shape also defines who cannot
be inside it.
**And it is reflexive.** By the shape of the graph, a declared frontier **manufactures its opponent's
coherence for free**: everyone the boundary names now shares an opposition and can draw equivalence
edges of their own. A successful frontier builds the chain *and* the counter-chain in the same move.
That is not a balance problem to be patched. It is the phenomenon, and it is why the board after a
realignment is more interesting than the board before it.

**2. Equivalence must outrun articulation inside the chain.** The movement wins the signifier when more
of the chain's links are demands linked *to each other by shared opposition* than are demands tied to
the signifier *by specific content*. This is the mechanism behind what Laclau calls the emptiness of
the populist signifier, and it is a design lever rather than a slogan: **the movement trades
specificity for breadth, knowingly.**
**Cost: every new demand admitted narrows what the signifier is allowed to promise.**

**3. The signifier must be allowed to empty.** To hold a broad chain, the signifier has to carry less
and less particular content. `SignifierKind.EMPTY` names this, and — the point worth keeping — `EMPTY`
is **not** a synonym for *vague*. A vague slogan no one has articulated is still `UNSPECIFIED`. An
empty signifier is one that has been **filled by a chain and then asked to stand for all of it**;
*Freedom* or *Human Survival* are empty in this sense precisely because they are load-bearing.
**Cost: the "temporary institutional order" step is paid for in advance, in meaning.**

### 1.4 The price, in one sentence

**A movement buys breadth with the loss of its ability to say what it means, and the frontier it drew
to hold the chain excludes the very demands that would have made its programme concrete.**

That single sentence is *arise*, *hold* and *break* at once. The equivalence chain is a coalition that
coheres **in opposition**, and the moment it governs it must produce an articulation — because a
government has to decide something — and **any articulation excludes**, since satisfying one demand
comes at another's expense. The mechanism does not fail; it *succeeds into* its own dissolution. That
is the plot twist the issue is asking for, expressed as structure.

### 1.5 What breaks it, and what does not

- **Governing breaks it.** #3/#4 arrive, office forces a specific articulation, the chain's demands are
  ranked against each other, and the excluded ones begin to re-float the signifier.
- **A rival articulation does not break it; it *re-floats* the signifier**, and re-floating is not the
  same as defeat. A `FLOATING` signifier is contested, which means both chains are still alive.
- **Holding the nodal signifier is not power.** [`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §7 says it
  plainly — *"hegemony in meaning is not power"* — and a movement can make its signifier nodal on the
  board and lose every other quantity in the same turn. That is not a bug to be balanced away. It is
  the reason the six quantities exist as six (§2).
- **Vagueness does not do any of this work.** Per `POLITICAL_SIMULATOR_MODEL.md`, the scaffold does not
  assert that a signifier is nodal or empty: `SignifierKind` defaults to `UNSPECIFIED`, so the game
  *states* the flip rather than inferring it from a hidden number.

### 1.6 The process list, read as a graph

The setting's eight steps are not a narrative sequence here; they are eight things that happen to a
graph. The movement accelerates all of them, and every acceleration has a cost.

| `paradigm_shifts.yaml` step | What it is on the board | What the movement does to it | What it pays |
| --- | --- | --- | --- |
| **dislocation** | an existing demand stops working — the word it was read through no longer explains anything | does not create the dislocation; **waits for one** | nothing — this is the paradigm shift, not the movement |
| **competing explanations** | rival `Demand`s over one shock | picks one explanation and gives it the movement's voice | discards the others as *their* side's |
| **competing signifiers and identities** | `Signifier`s sitting `FLOATING` between chains | **selects one** and works it | abandons the others, including ones its own base holds |
| **chains of equivalence** | `EQUIVALENCE` edges between demands | draws them faster than anyone else | breadth in, specificity out (§1.3.2) |
| **political frontiers** | a `Frontier` **node** | declares one, publicly | exclusion, and a counter-chain for free (§1.3.1) |
| **antagonism** | `ANTAGONISM` edges across the frontier | welcomes it; antagonism is the glue | the ability to be the party of everyone |
| **attempts at hegemony** | the signifier's `kind` moving `FLOATING`/`UNSPECIFIED` → `NODAL` | the objective, reached by the three conditions in §1.3 | the emptying of the signifier (§1.3.3) |
| **temporary institutional order** | a `Formation`; office, seats, access | **forced on it by winning**, and it breaks the mechanism (§1.5) | the chain it rode in on |

Read down the last column and the design is legible without a single number: the movement is an actor
that spends meaning to buy speed, and then has to govern with what is left.

---

## 2. The six quantities stay six

[`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §7 — implemented as names in `strategy_game/quantities.py` —
keeps six things in six fields because they are not interchangeable. Populism is precisely the case they
were separated for.

### 2.1 The movement's divergence, in the model's own fields

| # | Quantity (§7) | Model home (as landed) | The populist reading — expressible with the model as it stands |
| --- | --- | --- | --- |
| 1 | **opinion / support** | support markers per location/jurisdiction | can reach a **ceiling and produce nothing**; between #1 and #3 sit turnout and the electoral-rule tag |
| 2 | **organisational membership / resources** | the faction's pool, tag kinds `asset` and membership | a movement's #2 can be **borrowed**: held as edges to a patron, not as its own pool (§3) |
| 3 | **legislative representation** | seat markers | the classic gap — large #1, no #3 |
| 4 | **office & government control** | office markers | a junior coalition partner holds #4 **with a shrinking #1** |
| 5 | **institutional access** | access tokens on institution-interface cards | reaching a ministry is not owning the square |
| 6 | **Laclauian discursive hegemony** | the articulation graph itself (`Signifier.kind`, `RelationLayer`) | holds the nodal signifier and loses #1–#5 |

**The movement's signature is: #6 high, #1 volatile, #3 and #4 low, #5 contested, #2 borrowed.** A
paradigm-shift movement is *natively* a large gap between meaning and office, which is exactly what §7
was written to be able to show. The issue's two sentences — "enormous opinion support and no seat", "hold
office and lose the street" — are not edge cases to handle; they are the base case.

### 2.2 The counter-motion is the plot

When #3 and #4 arrive, **#6 begins to erode** — because office forces an articulation, and an
articulation breaks an equivalence chain (§1.4). The six quantities therefore do not move together.
**They move against each other.** That counter-motion is the realignment, and it is also the reason a
single influence scalar would destroy the only thing that makes the phenomenon legible: one number would
move all six at once and there would be nothing left to explain.

### 2.3 Refused by name

- **No generic popularity number.** The model has no such field, and it must not gain one. Where a
  player wants "how popular are they", the board's answer is *which* of the six, *where*, and *at whose
  expense* — the §7 table is the answer, not a substitute for it.
- **No numeric audience-alignment scale.** `strategy_game/data/faction_creation.json` already carries
  `numeric_scale_approved: false` and states that named qualitative positions come first, with an
  ordered scale only after playtesting. Nothing in this document proposes lifting that, and the
  audience-alignment scale specifically is recorded as **PENDING** (§6.3) rather than invented.
- **No equation between exposure and support.** A patron's platform reach is **exposure**; canon says
  the same thing about the LFP in the opposite direction — its vote support sits *far below* its media
  reach. Reach, persuasion, trust and votes are four different things, and the model keeps them in
  different places.

---

## 3. The patron is a relationship with failure modes, not a stat

"Money buys influence" is the cliche, and it is the wrong model. The repository gives the right one, and
it is already structural — this section reads the realignment consequences out of a record that exists.

### 3.1 The canon case

Canon, from [`PEOPLES_REPUBLIC_OF_UKWELI.md`](../world/PEOPLES_REPUBLIC_OF_UKWELI.md) §6 (quoting):

- the LFP is "a relatively small party"; "**Nationwide support is low**; its reach depends
  disproportionately on **financing and sympathetic media** owned or influenced by its benefactor,
  **Sir "Mars" Eldrich**";
- the relationship is "**CANON — not a secret twist**": the party is formally autonomous and Eldrich's
  financial and media influence is **publicly known**;
- Eldrich is "publicly known financier of the LFP", owner/controller of the setting's world-largest
  shipping company, whose obsessions are **colonising Mars** and supporting right-wing populist
  parties — to be developed as a major NPC and organisational network, "**not an omnipotent puppet
  master**";
- the party's declared **vulnerability** in the three-faction table is "**vote support far below its
  media reach**";
- and [`IDEOLOGICAL_FORMATIONS_2026.md`](../../strategy_game/docs/IDEOLOGICAL_FORMATIONS_2026.md) §5
  states the same asymmetry: "the ULP has little genuine electoral support but very large private
  funding and media/network reach from Sir Mars Eldrich" — with the party's own libertarian wing giving
  **three answers** on whether nonhuman persons are property, customers or citizens.

Everything §3 says below is a reading of *that* case. No new patron, no new faction, no hidden twist is
invented here.

### 3.2 The shape: an edge, an agenda, and assets that are not the movement's

A patron, modelled honestly:

- is a **named character** with a card, not a field on the movement's card;
- connects to the movement by a **`relationship` edge** — canon already declares the tie
  (`sir_mars_eldrich → ulp`, kind `patron_of`, visible publicly) as a static card tag, and
  `relationships.py` builds the *stateful* edge from it rather than declaring a parallel record;
- carries his **own `goal` tags**, which are **not** the movement's goals — colonising Mars, and
  supporting right-wing populist parties, are not the LFP's doctrinaire libertarian base;
- holds the **`asset` tags** the movement depends on (the shipping company, the sympathetic media, the
  finance layer). The movement's apparent #2 is therefore **borrowed capacity**: assets that live on the
  patron's card and reach the movement along an edge.

**The one sentence that matters here: because the assets are his, the movement's resources are
BORROWED or ENTITLED, never owned.** Canon says it in the setting's own words — *"patron resources are
not automatically faction property"* (`founding_story.json`, quoting #346 step 4). A movement that reads
its own strength off its patron's card is misreading the board, and the game should make that misreading
visible rather than punish it with a die roll.

### 3.3 The failure modes — as state transitions, not as narration

`founding_story.json` names the patron edge's state vocabulary:
`aligned · divergent · conditional · withdrawing · captured · severed`. **These are the failure modes
already; this section reads what each one does to the movement's mechanism.**

1. **Dependence.** A movement whose #2 is entitled looks identical to a movement whose #2 is owned until
   the edge is stressed. `COUNCIL_LAYER.md` §3 already prices this: a mission that draws on a patron's
   asset leaves the patron edge **stressed — "a dependence debt, not a free resource"** — and
   `council.py` refuses a declaration that draws on a patron without naming an edge that exists. This is
   the same discipline the plan comment applies to support (claimed vs observed): a movement's #2 must
   be storable as **owned vs entitled**, or a severed finance edge silently reads as a membership
   collapse. *That storage question is PENDING (§6.6).*

2. **Capture.** The patron's `goal` tags pull his own `ARTICULATION` edges onto the movement's
   signifier. Capture is a **graph fact** — the patron's demands begin to outnumber the movement's on
   the shared signifier — and it is the setting's built-in contradiction rather than an authored twist:
   a movement running on *Sovereignty* or *Freedom from Machines* acquires a patron whose agenda is a
   private off-world position, commercial disclosure and alien trade concessions. **The prophet and the
   patron do not need to be lying. They need to want different things from the same word.** That is
   `divergent`, and canon already sets the Eldrich tie to it in `founding_story.json`.

3. **Agenda divergence.** Canon makes Eldrich a **node with his own contested articulation** — three
   answers on nonhuman personhood, because his party's own libertarians disagree with him. So the patron
   is not a lever the movement pulls; he is a **second articulator on the same signifier**, and the
   movement's signifier now has two chains competing for it.

4. **When the money stops.** `withdrawing → severed`. The borrowed assets revert: part of #2 leaves, and
   part of #5 leaves with them (the media edge is his). **The signifier does not leave.** Once a chain
   is nodal it no longer depends on the patron — the patron depends on the chain, because a movement
   that can deliver a bloc is worth funding. `founding_story.json`'s own note: withdrawal "removes one
   network edge (the finance and ownership layer) and reveals which quantities were rented and which
   were owned: the faction shrinks, and no save is rolled."

### 3.4 The fifth effect: patronage is the timing device

**This is the sharpest point in this document, and it is why the patron belongs in a *realignment*
design rather than in a faction-management one.**

The patron **wants the movement in office** — his concession, his shipping position and his Mars
position are safer with a friendly government. But the movement's coherence depends on **not** holding
office, because opposition is the equivalence glue (§1.3.1). The two are therefore on a clock that runs
in opposite directions:

> **Patronage is the timing device that pushes a nodal-signifier movement toward #3/#4 — which is
> exactly the move that erodes #6. It is not an upgrade to the movement; it is the pressure that
> eventually breaks its mechanism.**

Nobody has to be a villain for that to be legible. The patron is not buying a puppet; he is buying
*time* and a *policy*, and the movement is spending the only thing it actually owns, which is the word.

### 3.5 What patronage can and cannot buy — plainly

| Can buy | Cannot buy |
| --- | --- |
| **#2 capacity** — funds, premises, staff, logistics, the shipping firm's reach | **#1 consent** — exposure is not persuasion, trust or votes (Castells; canon: the LFP's vote support far below its media reach) |
| **#5 reach** — access to media and institutions, a platform edge across otherwise disconnected clusters | **#6 hegemony** — a signifier becomes nodal through a chain and a frontier, never through funding |

*Money is not consent, and a platform is not a following.* No amount of patronage moves a signifier from
`FLOATING` to `NODAL`; only the three conditions in §1.3 do. That asymmetry is the design lesson, and it
is the reason a patron edge can be a **cost** rather than a support bonus.

### 3.6 Already landed: consume, do not duplicate

Everything in §3 is a reading of structure that is on `main`:

| Structure | Where | What this document adds |
| --- | --- | --- |
| `patron_of` edge kind, sparse stateful edge, named state vocabulary, `is_severed`, `state_history` | `strategy_game/relationships.py` | the realignment reading of each state (§3.3) |
| The founder and patron edges as data, with goals the faction need not share, failure modes `["money stops", "divergence", "capture"]`, and the canon Eldrich tie | `strategy_game/data/founding_story.json` | the timing argument (§3.4) and the can-buy/cannot-buy table (§3.5) |
| "a mission that draws on a patron names an edge that exists"; the patron edge stressed as a dependence debt | `strategy_game/council.py`; `COUNCIL_LAYER.md` §3 | that this is the mechanism by which a movement's #2 is borrowed |
| The six quantities, names only | `strategy_game/quantities.py` | the populist divergence (§2) |

**No new patron record, no new tag kind, no new edge type is proposed.** If a patron edge needs a
vocabulary this package does not have, that is an author ruling, not an agent's addition.

---

## 4. Realignment the player can read

The issue's acceptance criterion asks for realignment that is *fast, surprising and traceable*. The
traceability is the design problem, so this section is about **what changes and what the player is told**.

### 4.1 What makes a population's articulation shift

Not opinion moving by itself. A **dislocation** makes an existing demand *fail* — the word it was read
through stops explaining the person's situation. What follows is not a conversion:

> **The movement does not change minds. It changes what a word means to a group that already holds the
> demand**, by drawing a new `EQUIVALENCE` edge linking that salient demand to its signifier.

This is why a paradigm shock is the ideal trigger, and it matches canon §33.2 exactly: large
populations "remain weakly ideological, confused, opportunistic, locally focused, disengaged, or
internally inconsistent", and "Many people hold hybrid or contradictory positions." A movement that
recruits by re-labelling demands needs **no new beliefs** from anyone. That is not a weakness of the
mechanism; it is how it works, and it is why the realignment can be fast without being arbitrary.

### 4.2 The board: a change of shape plus a sentence

Four things can happen, and every one of them is visible as **shape**, with a sentence that says why.
The rule for the table is simple:

> **A change is never "a number went up". It is a change of shape plus a sentence naming the actor and
> the edge.** If a player cannot say *who did it and what it connected*, the change is not legible and
> should not have happened.

| Visible event | Its shape | The sentence beside it (illustrative, in-world) |
| --- | --- | --- |
| **An edge appears** | a new `ARTICULATION` or `EQUIVALENCE` edge between two nodes | "The water-rate demand is now read through *Sovereignty* — linked by this actor, on this day, in this jurisdiction." |
| **A signifier relabels** | the signifier's `kind` changes, `UNSPECIFIED`/`FLOATING` → `NODAL` (**or back**) | "*Humanity First* stops being one policy among several and becomes the name of the group." |
| **A frontier is declared** | a `Frontier` **node** appears, with `ANTAGONISM` edges across it | "The boundary is drawn: *those who would sign the licence.* And every actor it names now has a reason to cohere." |
| **A quantity marker moves** | seat / office / access / support markers, each in its own place | "Two support markers in the port quarters; no seat has moved; the media edge is his, not theirs." |

Two properties matter:

- **Every event is dated by the turn it happened in, not by a historical date.** Canon keeps the setting
  at **20XX**; this design adds no chronology and no exact year.
- **A signifier can relabel *backwards*.** `FLOATING` is not a failure state and `NODAL` is not a
  trophy: a rival articulation re-floats the signifier, which is the board showing that the fight is
  still live.

### 4.3 A board reading — no numbers, no dates

> A dislocation lands (an ambiguous disclosure, an AGI finding). Several demands already exist across
> two jurisdictions. Actor A draws a frontier and links three of them to one signifier; its `kind` flips
> from `UNSPECIFIED` to `NODAL`, and the flip is a dated board event. Actor B's media edge — **which is
> a patron's asset, not B's organisation** — carries A's frame further than A's own organisation could
> reach. Support markers rise in two quarters, and the electoral-rule tag then sits between them and any
> seat. **And the frontier A drew has made B's chain cohere too**, because a boundary names both sides.
>
> Nothing has "swung". Every step has an author, an edge and a location — and the movement is now one
> step closer to the office that will break it (§3.4).

### 4.4 Why that is legible rather than arbitrary

The **divergence itself** is the visible signature. A generic popularity number is illegible precisely
because it moves everything at once; six quantities moving at different rates, and sometimes against
each other, is what lets a player **name the mechanism**. This is the repo's own stated standard —
`VISION.md` §4 (pillar 8, persistent causality and legibility) and §7b's definition of done, "every
meaningful change has an inspectable in-game explanation" — applied to a populist realignment.

---

## 5. The cliche, declined

**This is the most cliche-prone territory in the genre, so the cliche is declined by name.** The boring
version of this issue is a cartoon demagogue, an evil billionaire, and rain-soaked neon noir. NoöPunk's
register is the opposite: **a Noösphere being born — wonder and genuine strangeness, not dread.**

Concretely, and deliberately:

- **The populist leader is not a demagogue but a signifier mechanic.** The interesting event is that
  success at meaning is a *mechanism*, and the leader is largely incidental to it. The same operation
  would work with a different face, which is far stranger — and truer to the theory — than a Great Man.
- **The patron is not a villain but a person with a real grievance.** Canon: stargates genuinely wreck
  the economics and strategic value of his Mars position. **His complaint is not fabricated.** That is
  what makes him interesting: his solution is terrible for everyone else while his grievance is honest,
  and his party cannot even agree with him about what a nonhuman person *is*.
- **The movement's people are sincere and hybrid.** §33.2 is binding: hybrid and contradictory positions
  are normal, and large populations stay weakly ideological. Nobody in this design is a crowd of one
  mind, and the realignment recruits by re-reading demands people already hold.
- **The anti-machine pole is not one thing.** §33.3 is binding: the Butlerian Jihad "is not one
  monolithic organization", and the currents inside it include ordinary bioconservatives and religious
  traditionalists as well as militants. The setting's own fragmentation is the anti-stereotype.
- **The incumbent may be right.** The centre-left cabinet may hold legitimacy by handling the shock
  competently, and the fringe may stay peripheral. Nothing here scripts a winner, and one of the issue's
  own alternate paths ends with the fringe still outside.
- **The strangeness comes from the paradigm shifts, not from the antagonists.** The wonder in NoöPunk
  is ontological — what is a person, what is a state, what is a public — not the dread of a villain.
  The antagonists are ordinary people making ordinary mistakes about extraordinary things.

Nothing in this document requires a single scene of rain, neon, or menace.

---

## 6. Pending author rulings

Recorded as **PENDING**, with the reason and the container standing in. **A container is not a rule.**

| # | Question | Why it is not an agent's call | Container standing in |
| --- | --- | --- | --- |
| **6.1** | **Which signifiers are in the first scenario** — the issue's eight, the #327 nine, or both; and whether agents may coin new ones | Signifier-list ownership is an author decision; a rival taxonomy beside §41's four reaction families is exactly what §41 exists to prevent | `Signifier` records already exist as data; the list is not filled here |
| **6.2** | **Whether the patron sits on the council** | #346 step 4 names ally / council member / rival power centre / eventual usurper and **fixes none as the default**; `relationships.py` states outright that it "refuses to hard-code an endpoint taxonomy" for this reason | `founding_story.json` `pending_author_decisions` → `patron_seat`; the `patron_of` edge, which is agnostic about where the patron sits |
| **6.3** | **Whether any numeric scale is used at all**, including an audience-alignment scale | `faction_creation.json` carries `numeric_scale_approved: false` and §7 of the Global record refuses a scalar; the design argument (§2.2) is that a single score destroys the phenomenon rather than summarising it | Named positions only; the six quantity names in `quantities.py` |
| **6.4** | **Which module carries the mechanism** — `politics.py` or `political.py` | The fork is [#301](https://github.com/TomiToivio/NooPunk/issues/301)'s open question and must not be settled here | Both vocabularies are described, neither is extended; §1 uses `politics.py` because that is where `SignifierKind` and `Frontier` live |
| **6.5** | **Is a movement a `Formation` node with articulation edges, or a `Faction`?** | This decides whether §1's mechanism attaches to the discourse record or the faction record, and it must not re-open #296/#297 | `Formation` exists in `politics.py`; the faction record is #296's |
| **6.6** | **May #2 be stored as *owned* vs *entitled*** (borrowed assets living on a patron's card), mirroring the claimed-vs-observed discipline applied to support? | This is the one proposed addition to §7's six fields, and §7's fields are an acceptance criterion, so it needs the author's word | The patron edge is read, not re-declared; the state vocabulary already carries `withdrawing`/`severed` |
| **6.7** | **Does the game ever evaluate the `EQUIVALENCE`-vs-`ARTICULATION` condition, or does the GM declare the `FLOATING → NODAL` flip as an authored event?** | §1.3.2 describes a structural condition; whether it becomes an evaluated rule is a mechanic, and no rule is approved | `SignifierKind` is stated explicitly on the flip, not inferred from a hidden quantity |
| **6.8** | **Wendt, *The Last Humans* chapter 6** ("UAP Regimes and Terrestrial Populism") | The argument cannot be read from the chapter title, and the published text is paywalled; a *draft* exists but its numbering does not match the published edition, so it must never be cited as the published chapter | The reading gap is recorded on the issue and in `PARADIGM_REALIGNMENT_SCENARIO.md`; nothing in this document depends on the unread chapter |

---

## 7. What this document does not do

- **No code.** The issue body is explicit — *"No code or canon/rule implementation until author approval,
  per #282"* — so no module, data file or test accompanies this record, even where the structure would
  be expressible in code. The structure is written down; the author decides whether it becomes executable.
- **No test.** Per [AGENTS.md](../../AGENTS.md) and [#271](https://github.com/TomiToivio/NooPunk/issues/271),
  prose is reviewed editorially and by playtesting, never by a CI gate.
- **No rules, mechanics, numbers, thresholds, costs, dates, dice or turn cadence.**
- **No canon.** The cast, the movement and the realignment are **#305 scenario material** drawing on
  §33.2/§33.3 and on the canon Eldrich case. They add nothing to canon, and the legacy rulebook and
  `rulebook/` are untouched.
- **No resolution** of the `politics.py` / `political.py` fork, the global roster discrepancy, or the
  leadership roster — all three stay open and are named as open in §6 where this design touches them.
- **No third political vocabulary.** The mechanism is expressed in the vocabulary already on `main`.

---

**Cross-links.** [#282](https://github.com/TomiToivio/NooPunk/issues/282) the scaffold ·
[#295](https://github.com/TomiToivio/NooPunk/issues/295) leaders ·
[#296](https://github.com/TomiToivio/NooPunk/issues/296) faction management ·
[#297](https://github.com/TomiToivio/NooPunk/issues/297) discourse and network —
[`V1_DISCOURSE_AND_NETWORK.md`](V1_DISCOURSE_AND_NETWORK.md) ·
[#302](https://github.com/TomiToivio/NooPunk/issues/302) country-agnostic society ·
[#303](https://github.com/TomiToivio/NooPunk/issues/303) tone and agent ontology ·
[#304](https://github.com/TomiToivio/NooPunk/issues/304) GM turns and Tarot ·
[#305](https://github.com/TomiToivio/NooPunk/issues/305) the plot twist, and its landed scenario dossier
[`PARADIGM_REALIGNMENT_SCENARIO.md`](../../strategy_game/docs/PARADIGM_REALIGNMENT_SCENARIO.md) ·
[#323](https://github.com/TomiToivio/NooPunk/issues/323) the council layer
([`COUNCIL_LAYER.md`](../../strategy_game/docs/COUNCIL_LAYER.md)) ·
[#346](https://github.com/TomiToivio/NooPunk/issues/346) the founder and the patron
(`founding_story.json`, `relationships.py`) ·
[`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §7 and §9 · `data/paradigm_shifts.yaml`.
