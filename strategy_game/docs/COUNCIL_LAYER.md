# The council layer: portfolios, missions, scarcity and relationship channels (issue #323)

**PROPOSAL. Approves nothing.** `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**, and this
document implements no rule. It is the *structural* layer beneath the written specification in
[`LEADER_COUNCIL_SYSTEM.md`](LEADER_COUNCIL_SYSTEM.md) (stage A of this issue): that document says what
the council *should* do — **every number in it is DRAFT** — and this layer turns the parts the issue
itself states as acceptance criteria into executable checks, while leaving every unauthored effect
explicitly recorded as open.

| Artifact | Role |
| --- | --- |
| `strategy_game/data/council.json` | the four offices, the mission shape and its declared costs, the status table, the four strategic channels, the open questions |
| `strategy_game/council.py` | the two validators (requirements refused; unauthored effects reported) and the structural readings |
| `strategy_game/tests/test_council.py` | 49 executable contracts (issue #271: code only) |
| `strategy_game/quantities.py` | the six quantities of `docs/design/NOOPUNK_GLOBAL.md` §7, in one place |
| `strategy_game/relationships.py` | the one sparse, stateful relationship edge, read by the mission layer |

**Consumed, not restated:** `core.py` already declares `Leader` and `Faction`; the stage-A specification
owns the prose and the DRAFT numbers; `LEADER_MICRO_RULES_PROPOSAL.md`'s Reason/Nerve/Rapport card is
**UNAPPROVED** and nothing here assumes any attribute set — **D1, D2 and D6 are open and D7 refuses
importing the six legacy STATs**. The four offices keep the specification's DRAFT names
(`politics_diplomacy`, `organisation_networks`, `operations_resources`, `research_intelligence`).

**Cross-link:** `docs/design/V1_FACTION_MANAGEMENT.md` (§#296) states *why no code landed with that
record* and maps the faction card onto §7's six quantities — a different layer from this one, and its
*"one resolution mechanism"* cap is not touched here: this layer resolves nothing at all. Its
*"leader count is a hidden cost"* finding is a bookkeeping argument about the same four-slot roster, not a
second definition of the council.

## 1. Two validators, and why the difference is the whole discipline

Issue #323 states some things as requirements and other things as proposals. The code keeps them apart:

- **`structural_problems()` — refused by name.** The issue's own acceptance criteria: a mission names
  exactly one leader; one leader leads at most one move a turn; a faction declares no more moves than it
  has leader-turns; a move names *which* of the six quantities it tries to move and a valid target and an
  authoriser; the four posts are distinct and each office is held by one leader; a mission that draws on a
  patron names an edge that exists.
- **`consequence_reports()` — reported with its source, never refused.** Everything whose *effect* is
  unauthored: the DRAFT status table's no-mission rows, a portfolio's passive magnitude, the effect of a
  council refusal, the price of a declared resource, a roster that is not four. Refusing on one of these
  would be implementing an unapproved rule.

Nothing resolves. No mission is rolled, no outcome written, no quantity moved, no turn advanced; there is
no economy, no die, no action set and no win condition. `MissionDeclaration.outcome` exists as an
uninterpreted field that no code in this package writes, and a declared outcome is *reported* as out of
scope.

## 2. What each office decides, and why four of them disagree

Map each office to **which of the six quantities** it serves. A portfolio is not only a passive: it is a
**standing interest** in one quantity, which is exactly what makes its holder disagree with the other
three.

| Office | Serves, of the six | Its holder's standing position | What it argues for |
| --- | --- | --- | --- |
| **Politics & Diplomacy** | seats, office, access | convert support into institutions | compromise, coalition, court the incumbent, bank a seat now |
| **Organisation & Networks** | opinion/support, membership, reach | grow the base and the network | mass mobilisation, expand, refuse elite deals that hollow the movement |
| **Operations & Resources** | membership/resources, resilience, covert capacity | secure means and options | acquire, keep capability, take the ruthless option, protect the patron's money |
| **Research & Intelligence** | access *via* intelligence, articulation | know and frame | investigate, verify, publish — or publish first and apologise later |

Research and evidence are deliberately **not** one of the six: evidence is not a track, it is what a
claim is grounded in.

**Disagreement is structural, not scripted.** §7 of the global design record says the six quantities are
non-identical *by rule*, and the four-move cap says a faction cannot pursue all of its priorities in a
turn. The council is therefore a **scarcity mechanism**, and
`unpursued_quantities()` always leaves something out — four moves against six names. That reading is set
membership over names: no weight, no score and no priority ordering is computed anywhere. A council whose
members always agree would be a council whose four offices serve one quantity, which is what
`shared_interest_report()` reports as a defect.

The argument is **personal as well as structural**: two holders who disagree on strategy *and* share a
sparse `rival` tie produce a leak or a quiet sabotage; two who disagree but are `mentor`/`friend` produce
a compromise. It is resolved by the office's interest and the relationship record — not by a die roll, so
no new subsystem is needed to make the council non-decorative.

## 3. What a mission is, costs, and who authorises it

One declared attempt to move **one named quantity** for one named target, in one place, led by exactly one
named leader. The declaration states which quantity it moves — that field is what stops it being a generic
success roll: *"win the ward"* (seats) and *"win the crowd"* (opinion) are different missions, not one
mission with different modifiers.

- **Authorisation.** The faction leader assigns, so `authorised_by` must name someone. Whether the council
  may authorise without the principal, or refuse the principal's order, is **not decided**; an authoriser
  who is not the principal is reported.
- **Costs, all named and unpriced.** (a) one of the four leader-turns — the opportunity cost is measured
  in *quantities not pursued*; (b) the declared resources and assets; (c) the risk the leader ends the turn
  in a named status; (d) if it draws on a **patron's** asset, the patron edge is stressed — a dependence
  debt, not a free resource, per #346 step 4.
- **Failure is not nothing.** The declared shape: the attempted quantity does **not** move, and a
  *different* quantity moves the wrong way. Which quantity moves wrong, and by how much, is a rule and is
  recorded as `declared: false`.
- **Refusal is a described slot.** A portfolio holder may contest a mission that cuts against their
  office's quantity; whether that refusal is a status or an authored choice is decision **D6** of the
  micro-rules proposal, unauthored.

## 4. How a personal tie produces a strategic consequence

The relationship record is not a narrative side-layer; it is a channel and a gate on the same six
quantities. Four channels are declared in the data, every one of them with `enforced: false`:

1. **Gates legality and cost** — a `mentor` or `indebted` tie to a target reaches this channel; a
   `suspicious` tie reaches it from the other side.
2. **Carries quantities** — a personal edge to another faction's leader *is* the conduit for access,
   articulation and coalition (Castells). The RPG layer is the graph on which four of the six quantities
   move.
3. **Decides trade-off or split** — the officers' opinions decide whether §2's structural disagreement is
   productive or destructive.
4. **Written back as state** — at step 7 of the turn order relationships update *alongside* the quantities,
   and the next turn's mission legality reads them. One loop, not three mini-games.

Two separations the code keeps honest: a tie is read **by the mission's own leader** to the target, and an
**absent** tie is reported as *unmodelled* rather than as zero — the record is sparse, so nothing may be
read from the absence. And no channel grants anything: `channels_for()` returns declarations, and
`strategic_consequences()` returns a reading with `enforced: false`.

## 5. Rival parity

`validate_all()` runs the same validators over any number of councils. A rival faction cannot hold a fifth
office, bank an unused mission, gain a free action from its members or resources, or escape the cap: there
is no special case anywhere in the module for a player faction.

## 6. What the author still has to decide

- **Roster size.** Issue #323 says a faction has four leaders; issue #346 says the four-slot limit counts
  characters *assigned to field actions*, not all managers. Compatible on the four-move cap, different on
  the roster. Flagged on both issues; **not** resolved here.
- **Is the founder one of the four leaders, or a fifth authority over them?**
- **The effect of a council refusal** (D6).
- **A portfolio's passive magnitude.** The specification proposes *at most +1* and a *+2* faction-wide cap
  and marks every number DRAFT, so `magnitude_declared` is `false` with a reason.
- **The leader card.** Reason/Nerve/Rapport, one capability plus tags, or something else — D1/D2 open, D7
  refuses the six legacy STATs. No attribute is named anywhere in this layer.
- **Which quantity a failed mission moves the wrong way.**
- **The turn unit** — weeks or months. Nothing here reads a clock; a turn is an argument, not a duration.

Every one of these is recorded in `data/council.json`'s `pending_author_decisions` with the reason it is
open and the container standing in for it, and a contract asserts that no such entry is missing its
reason. **A container is not a rule.**

**Not the same question:** `council_size` is *one faction's* leader roster. It is deliberately not the open
data-integrity question of which canonical faction records are canonical
(`docs/design/NOOPUNK_GLOBAL.md` §6A), which stays unresolved and is not touched here.

## 7. The seam to the RPG layer (issue #389)

The relationship record above is *read*, never *applied*: `strategic_consequences()` returns a reading
with `enforced: false`. Issue #389 has since approved the **RPG layer's** rules basis (Fate Core), while
the **strategy** and **political-simulation** layers remain unapproved. Those two facts are what
`strategy_game/relationship_seam.py` exists to keep apart.

The seam is **signature-only**, in the spirit of `ports.py`:

- `RPGRelationshipSource` is a `typing.Protocol` — the one way the strategic layer may *read* the
  personal state the RPG layer owns (`relationship_states`, `declared_edge_ids`). It resolves nothing
  and transitions nothing.
- `NullRelationshipSource` is the default: it declares nothing, and its emptiness is **UNMODELLED,
  never zero** — the same discipline as §4's absent-tie rule.
- `strategic_consequence_view()` **reuses** `CouncilModel.strategic_consequences()` rather than
  re-implementing it, and attaches `applied: false` and the owner of the mechanics. It imports nothing
  from `strategy_game/rpg/`, and a contract asserts that in a subprocess.

So the seam is the structure that makes the author's remaining decision *expressible*: once there is a
ruling about what a tie changes, it has a declared slot to land in. Until then it lands nowhere, and
the triggered-RPG-choice half of acceptance criterion 6 stays open with it.
