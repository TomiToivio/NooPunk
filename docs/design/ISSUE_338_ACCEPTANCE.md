# Issue #338 — the five decisions of 2026-10-13, consolidated, with their acceptance mapping

**Status: RECORD ONLY. Documentation, no mechanics, no canon, no state.** This record gathers the
**five author decision records** that accumulated in issue
[#338](https://github.com/TomiToivio/NooPunk/issues/338)'s ~95 KB body into one place, next to the
**acceptance checkboxes each of them carries** (~29 boxes, plus the issue's sixth, binding design rule
in §6 below). A reader currently has to reconstruct the decisions from a sprawling body; the body is
also now *closed*, so a future implementer cannot reasonably be asked to mine it.

**Why this record exists when a closeout already does.** Sibling PR
[#436](https://github.com/TomiToivio/NooPunk/pull/436) landed
[`ISSUE_338_GLOBAL_HANDOFF.md`](ISSUE_338_GLOBAL_HANDOFF.md) and carried the issue's latest directions
into a six-bullet handoff plus an *unfinished work / owner* table. That record **summarizes** and
**routes**; it does not enumerate the checkboxes or state, item by item, which are met and which are
not. Its own §*Closure semantics* says plainly that closing *"does not mark its unchecked implementation
acceptance criteria as completed"* — without itemising them, that leaves a reader unable to tell a met
criterion from a gated one. **This record supplies exactly that missing half** and restates nothing the
handoff already says. It does **not** re-open or re-close the issue, and it decides nothing:

- **No mechanic, number, magnitude, threshold, cost, die, cadence, action set or victory condition** is
  defined, implied or estimated here. `strategy_game/RULEBOOK.md` records that **faction strategy and
  political simulation rules are not yet approved**, and Gates A–D
  ([`RULE_SYSTEM_RESEARCH.md`](../../strategy_game/docs/RULE_SYSTEM_RESEARCH.md)) are still open.
- **No structural fork is resolved.** The five forks — and fork 3's D1/D2/D3 in particular — live in
  [`STRUCTURAL_FORKS_AND_DECISIONS.md`](STRUCTURAL_FORKS_AND_DECISIONS.md) and are **cross-linked, never
  restated**; that document's options and its "left open here" verdicts stand unchanged.
- **No exact year is assigned.** The decision records describe the setting's opening; `AGENTS.md` §6
  makes canonical future dates **20XX**, so this record writes 20XX and treats any other figure in the
  issue body as scenario-local prose, not canon.
- **No test, guard, schema lock or CI step covers this file** — it is prose, reviewed editorially and by
  playtesting ([#271](https://github.com/TomiToivio/NooPunk/issues/271), `AGENTS.md` automated-tests
  policy). It adds no documentation gate either.

**Status vocabulary used in the tables below.** `MET` — the criterion is satisfied by an artefact
already on `main`, cited by path. `MET AS STRUCTURE` — the record/vocabulary/seam the criterion needs
exists and is checkable, while the *rule* that would make it play is unapproved. `GATED` — the criterion
cannot be satisfied without an unapproved mechanic, and the gate is named.

---

## 0. Why this is documentation, and why no sixth module was minted

The obvious way to "land" a criterion like *"one shared abstract operation/check interface supports
physical, cyber and astral actions"* is to write an `operations.py`. **That was deliberately not done**,
and the reason is the repository's own rule rather than caution for its own sake.

`AGENTS.md` §13 states it for rules — *"A **rules** difference is a defect: extract a shared
specification rather than fork the rule"* and *"Where a shared specification already exists … consume it
rather than re-declaring the same values in a second runtime"* — and
[`V1_DISCOURSE_AND_NETWORK.md`](V1_DISCOURSE_AND_NETWORK.md) §2.3 states it for vocabularies: **no third
spelling for an existing concept.** `STRUCTURAL_FORKS_AND_DECISIONS.md` §1 and §5 then document, with a
measured silent-loss path, exactly what a second spelling of one concept costs. And in fact **every
piece the criterion names already exists on `main`**; the interface is currently *implied across four
artefacts* rather than *named in one*:

| The piece of "the one interface" | Where it already is | What it does today |
| --- | --- | --- |
| the agent-led declaration (a named agent activating otherwise passive faction resources) | `strategy_game/council.py` → `MissionDeclaration` (`leader_id`, `allocated_resource_ids`, `quantity`, `refusals`, an uninterpreted `outcome`) | declares one active move; resolves nothing |
| the strategic attach point, and the single refusal | `strategy_game/turn.py` → `StrategicActionPort` (signature only) and `strategic_action()`, which raises with `PENDING_STRATEGIC_ACTION` | fixes *where* a strategic mechanic will attach, and keeps it out until Gate C closes |
| the personal-scale check, already approved | `strategy_game/turn.py` → `record_character_check()`, through `strategy_game.rpg.boundary.LeaderRpgLayer` into the **one** `tabletop.history.HistoryLog` | writes a seeded Fate check, with its dice provenance, into the one authoritative history |
| the per-domain structure that exists | cyber → `strategy_game/cyber.py` (possibility of access, #344); astral → `strategy_game/psi_operations.py` (`PsiOperationLedger`, #345); physical → **none, and none added** | cyber answers *whether access is physically possible*; astral declares and files unverified findings; physical has no subsystem because combat is reserved |

Minting `operations.py` would have produced a **second** `MissionDeclaration`-shaped record, a **second**
articulation of the same attach point `turn.StrategicActionPort` already owns, and a fifth spelling of a
concept the four above already carry — the exact defect class this repository is currently documenting
about itself. So this record **names** the interface at the four artefacts above and adds nothing.
The criterion's remaining half — the *unified resolver* itself — is a mechanic; see §7.

One more split, stated because it is this record's own choice: **the five decisions are consolidated
here as one document, not five**, because they were taken on one day, in one issue, by one author, and
they constrain each other — decision 3 sets the actor model decision 4's roadmap assumes, decision 2's
three domains are the subject of decision 1's cyber half, and decisions 4 and 5 are the same deferral
seen from the roadmap and the mission side. Five records would have to cross-reference each other four
ways to say the same thing. The **sixth**, the binding design rule, is kept as an appendix rather than
folded in, because the author labelled it a *design rule* rather than one of the five decisions.

---

## 1. Cyberspace architectural decision — rogue-AGI Blackwall containment and local-access netrunning

**Recorded in the issue body as the first 2026-10-13 decision. Detailed lore owner:
[#344](https://github.com/TomiToivio/NooPunk/issues/344).** The author's own opening line points the
detailed design there, and a later #344 clarification fixed the three-era temporal progression, so this
record does not restate the lore; it records only how the acceptance note is met. The landed artefact is
[`strategy_game/docs/CYBERSPACE_AND_CONNECTIVITY.md`](../../strategy_game/docs/CYBERSPACE_AND_CONNECTIVITY.md),
the model is [`strategy_game/data/connectivity.json`](../../strategy_game/data/connectivity.json), the
reader and check are [`strategy_game/cyber.py`](../../strategy_game/cyber.py), and the contracts are
`strategy_game/tests/test_cyber_access.py`.

| # | Criterion (author's wording, condensed) | Position | Basis on current `main` |
| --- | --- | --- | --- |
| 1.1 | Cyber operations respect physical/logical connectivity | **MET** | `cyber.resolve_access()` refuses every remote path to `local_only` and `isolated` targets **in every era**, enforced by two independent conditions; a Castellsian social/institutional edge (`social_tie`, `network_edge`, `influence_edge`, `personal_contact`) is refused **by name** with an explanatory error rather than silently treated as a route |
| 1.2 | On-prem / limited networks affect mission selection | **MET AS STRUCTURE** | the five connectivity classes (`public_gateway`, `safenet_exposed`, `private_linked`, `local_only`, `isolated`) and the seven access paths are the declared mission-selection inputs, and `connectivity.json`'s `example_mission` carries the *same* on-premises-lab mission across all three eras with a different route and cost in each. *What a route costs and how hard it is* is Gate C |
| 1.3 | Faction netrunners and their agent commanders use the unified resolver | **GATED — Gate C** | the interface exists (§0) and the single refusal exists (`turn.PENDING_STRATEGIC_ACTION`), but no resolver is implemented; a second refusal path was deliberately not added. Gate C (strategy rules) owns the mechanic |
| 1.4 | #344 owns the detailed lore and cyberspace design | **MET** | the decision says so, this record cross-links it instead of restating it, and `connectivity.json`'s `sources` names #344 for the model and #345 for the quantum-information/PSI half |

**Not absorbed.** The two illegalities the author insists on separating stay separate in code
(`ConnectivityModel.is_containment_breach()`), and the containment-breach response — a world event, a
faction asset, or both — is left to the author.

---

## 2. Rules simplification — Physical / Astral / Cyber as abstract strategic operations

**Recorded in the issue body as the second 2026-10-13 decision, with six acceptance checkboxes.** Its
own scope note supersedes older issue language requiring detailed Physical Combat, Astral Psionics or
Cyber Hacking subsystems for the strategy RPG: the three layers are now **strategic action categories and
fictional contexts**, not three mechanical engines.

| # | Criterion | Position | Basis on current `main` |
| --- | --- | --- | --- |
| 2.1 | One shared abstract operation/check interface supports physical, cyber and astral actions | **MET AS STRUCTURE** | the four artefacts of §0 together *are* the interface, and the design decision's own framing (the layers are *action categories and fictional contexts*) is what makes this satisfiable as structure. A **fifth module was refused on purpose** (§0). The mechanised resolver is GATED — Gate C, see §7 |
| 2.2 | Military squads, netrunner teams and remote viewers deployable as agent-led faction resources | **MET AS STRUCTURE** | agent-led is *enforced*, not merely stated: `council.MissionDeclaration.leader_id` and `psi_operations.PsiOperationLedger.declare()` both require a known, named agent, and `declare()` refuses an unknown asset id. Resource *effects* are Gate C |
| 2.3 | Personal physical/PSI/hacking encounters resolve through skill checks, without mandatory independent combat/hack/PSI minigames | **MET AS STRUCTURE** | the positive half is the approved Fate check: `turn.record_character_check()` resolves through `rpg/boundary.LeaderRpgLayer` and writes the result into the one history. The negative half is verifiable by absence: **no** combat, hacking or PSI resolution subsystem exists in `strategy_game/`, so none can be mandatory |
| 2.4 | Domain-specific fiction, defences and outcomes remain distinct without large rules subsystems | **MET AS STRUCTURE** | the distinctions are the author's own and are carried where they already belong — cyber's target class and its two illegalities in `connectivity.json`; astral's observation-verification ladder (`unverified`/`inconclusive`/`corroborated`/`contradicted`) in `psi_operations.PsiFinding`; physical's *injury, destruction and territory* fiction has no subsystem, which is the point. No per-domain defence model is defined |
| 2.5 | Outcomes update the same shared character, faction and global campaign state | **MET AS STRUCTURE** | there is **one** authoritative history (`tabletop/history.py`'s `HistoryLog`, issue #397) and `turn.py` is the declared connection to it; `turn.TurnOutcome` deliberately carries **no prose field**, so a narrative layer has nothing to write into. Nothing in this record adds a second state engine — and `local_slice.py` / `global_slice.py`'s parallel state engines are *existing* forks 4 and the handoff's integrate-or-retire item, not something added here |
| 2.6 | Long-term tactical-view intention preserved, explicitly deferred beyond the MVP | **MET** | `VISION.md` §3 (*one game, many zoom levels*) carries the intention, the handoff §5 carries it forward, and §4 below records the MVP/deferred separation in the author's own terms |

---

## 3. Pregenerated factions and characters, layered storylines, ideological movements instead of nation-state player factions

**Recorded in the issue body as the third 2026-10-13 decision, with eight acceptance checkboxes.** The
primary playable faction is a **transnational ideological movement**, not a sovereign state; the
comparison the author names is *Sigma Theory*'s scale with **ideological movements operating through a
global Network Society** instead of competing nation-state players.

| # | Criterion | Position | Basis on current `main` |
| --- | --- | --- | --- |
| 3.1 | Initial play uses pregenerated faction and character rosters; creation tools are not MVP blockers | **MET** | the roster is authored canon and data: `data/global_factions.json` (`"status": "author_canon"`, `source_issues: [328, 329]`), with `data/character_cards.json`, `data/founding_story.json` and `data/council.json`'s leaders/events. Creation **exists as an option** (`faction_creation.py`, `data/faction_creation.json`) and is nowhere required — which is exactly "not a blocker" |
| 3.2 | Playable factions are ideological movements with transnational networks, distinct goals and rivalries, not a set of nation-states | **MET AS DATA** | `global_factions.json` declares three `entity_kinds` — `human_ideological_formation`, `nhi_aligned_formation`, `latent_public` — and **no** nation-state kind. The *count* of the roster is fork 3's and stays open; see §7 |
| 3.3 | Characters, factions and the world each have authored, branching storyline events that interact through common state | **MET AS STRUCTURE / partly GATED** | two of the three layers are structured: character events exist (`council.CharacterEvent`, `data/council.json`'s `character_events`, projected onto the shared tabletop `Card`), and world-level seeds exist (`data/paradigm_event_seeds.json`; `data/founding_story.json` for the founder/patron edges). The **cross-layer chain** — events in one layer triggering and gating events in the others — is a mechanic and is GATED (Gates B/C). Branching *outcomes* are uninterpreted fields by design |
| 3.4 | Nation-states remain significant non-player institutions, balancing fragility, sovereignty and supranational cooperation | **MET AS DOCUMENTATION** | recorded here and in the author's decision; **no state record is minted**, because inventing state actors or their attributes is canon and is not an agent's to write. The existing `data/world/un_parties.yaml` register is a separate legacy register (fork 3) and is untouched |
| 3.5 | Model simultaneous upward transfer of authority toward the developing UN order and downward/outward fragmentation | **MET AS DOCUMENTATION** | the author's Wendt-derived paradox is recorded as the design intent; the variables the Global Politics view shows are the six non-identical quantities already named in `strategy_game/quantities.py` (§7 of [`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md)), none of which is a scalar. The *transitions* are Gate B |
| 3.6 | Scenario opening does not presume a fully consolidated UN world government or existing UNSA | **GATED — structural fork 3, D1** | **not satisfiable as a record, and deliberately not "fixed".** This decision states the opening is pre-consolidation, while an **earlier 2026-10-13 record in the same issue body** (*"CURRENT SCENARIO DIRECTION — minor faction in UN world society"*) states that a UN world government **is already in power** under a centrist hegemonic bloc. Two author records in one issue disagree, which is precisely D1 as `STRUCTURAL_FORKS_AND_DECISIONS.md` §3.1/§3.6 puts it. Resolving it here would be an agent choosing the scenario's period. It stays the author's |
| 3.7 | Keep the Sigma Theory-like worldwide strategy and paradigm-shift drama, while remaining a unified, small, open-source, tabletop-convertible RPG/strategy game | **MET AS DOCUMENTATION** | recorded here; the design comparison is [`strategy_game/docs/NOOPUNK_GLOBAL_DESIGN.md`](../../strategy_game/docs/NOOPUNK_GLOBAL_DESIGN.md) and the source ledger supplement, with the *tabletop-convertible complexity ceiling* rule in §6 below |
| 3.8 | Preserve the previous decision to **defer but plan for** a future tactical mission view; no tactical map for the first MVP | **MET** | identical to 2.6 and 4.1; the deferral is stated in the author's terms in §4 |

---

## 4. Tactical view roadmap clarification

**Recorded in the issue body as the fourth 2026-10-13 decision, with five acceptance checkboxes.** The
author's explicit scope guardrail: the roadmap must **not** be phrased as *"if ever added"*, *"unlikely"*
or *"no tactical combat layer"* without specifying **"in the MVP"** — this record keeps that wording.

| # | Criterion | Position | Basis on current `main` |
| --- | --- | --- | --- |
| 4.1 | Roadmap explicitly separates **MVP abstract encounters** from a **later tactical mission view** | **MET** | separated in the author's own terms here and in the handoff §5; the existing mission side is `council.MissionDeclaration` plus the labelled noncanonical prototype `strategy_game/global_slice.py` |
| 4.2 | Tactical **investigation/adventure** and tactical **combat** are both supported in the future design direction | **MET AS DOCUMENTATION** | recorded here as the author's direction. **Nothing is implemented**, and no terrain, movement, positioning, cover, visibility or turn-based action is defined — prototype candidates the author listed are noted as candidates, not requirements |
| 4.3 | Tactical outcomes update the same persistent global political/network and faction state as abstract encounters | **MET AS STRUCTURE** | there is one history: `turn.record_character_check()` is the only function that writes a rule outcome, and it writes into the one `HistoryLog`. A future tactical layer must therefore attach to `turn`, not to a new state; §0 names where that attach point already is |
| 4.4 | Mission contracts/state preserve sufficient information to support both abstract and future tactical resolution | **MET AS STRUCTURE** | `council.MissionDeclaration` already carries the leader, the target, the location, the committed resource ids, the authorising edge, declared refusals and an uninterpreted outcome — the author's own list (*"leader, committed resource types, target site, intent, decisions and reported consequences"*) — and `global_slice.Operation` declares `approaches` (the choice set) and a target site. Because the record is a **declaration with no mechanism in it**, both resolutions can consume it. No numeric quantity or quality *scale* is declared: quantity/quality stay names to be supplied |
| 4.5 | Older contrary statements in the issue are read as **MVP-only scope restrictions**, superseded by this clarification | **MET AS DOCUMENTATION** | recorded here. The one place this record does **not** apply that reading is 3.6's two conflicting *scenario* records, which are a fork and not a scope restriction |

---

## 5. Mission design — RPG operations first, optional miniatures tactics later

**Recorded in the issue body as the fifth 2026-10-13 decision, with six acceptance checkboxes.** Missions
are *"primarily RPG-style investigations, adventures, cyberpunk heists, diplomacy, infiltration, research,
rescue and other operations, not necessarily combat encounters"*.

| # | Criterion | Position | Basis on current `main` |
| --- | --- | --- | --- |
| 5.1 | MVP mission loop supports at least an **investigation** and a **cyberpunk heist/infiltration**, each resolvable without combat | **MET AS STRUCTURE** | `strategy_game/global_slice.py`'s `sample_world()` declares exactly those two (`investigate_crash` — investigation; `archive_heist` — the archive infiltration, resolved nonviolently through *quiet access*) beside a third site whose only force option is an abstract mission *choice*. It is labelled **noncanonical, test scaffolding, not approved rules** in its own docstring, and `strategy_game/tests/test_global_slice.py` exercises it. The **rules** of the loop are Gate C |
| 5.2 | Missions are a structured series of decisions and tabletop-convertible checks; failure introduces complications and alternative routes rather than only terminating | **MET AS STRUCTURE** | a mission is a declaration plus a choice set: `global_slice.Operation.approaches` and `council.MissionDeclaration.refusals`. The prototype's illustrative non-success branch produces an explicit *complication*, not a termination. The check itself is the approved Fate check; its difficulty is not set here |
| 5.3 | Where combat or forces matter, resolve their effect using agent skills, asset quality/quantity, choices and dice — without requiring squad-scale tactical gameplay | **GATED — Gate C** | this is the criterion that *needs a magnitude*, so it is not met and nothing here pretends otherwise: `global_slice.Resource.quantity/quality` exist as noncanonical scaffolding numbers, and `strategy_game/RULEBOOK.md` records that faction strategy rules are **not yet approved**. The interface and its single refusal exist (§0); the arithmetic does not, and no threshold, die or cost was invented to fill the gap |
| 5.4 | Keep **strategy, RPG and political simulation in one game**; no separate mandatory tactical game | **MET** | one package, one `WorldState`, one authoritative history, one political vocabulary family; the RPG half is the approved Fate layer, and no second tactical product or state engine is added. (That `local_slice.py` and `global_slice.py` hold *existing* parallel engines is forks 4 and the handoff's integrate-or-retire item — this record neither adds nor resolves one) |
| 5.5 | Keep the miniatures/XCOM-style tactical system on the **future/optional** list; explicitly exclude detailed movement, cover, per-soldier turns and tactical map engineering from the MVP | **MET** | recorded here as the author's exclusion list verbatim; nothing of it is implemented |
| 5.6 | If tactical missions are ever added, offer a coherent bridge between abstract and detailed resolution, with outcomes flowing back to the same world state | **MET AS STRUCTURE** | 4.3 and 4.4 together: a declaration record with no mechanism inside it, plus the single attach point `turn.StrategicActionPort` and the one history. That is the *bridge's* structural precondition and nothing more |

---

## 6. Appendix — the issue's sixth record: the binding tabletop-convertible design rule

Kept separate because the author labelled it a **binding design rule**, not one of the five decisions. It
carries its own six acceptance criteria, and it is quoted here in its own terms: *"If a game system cannot
be modeled using mechanics convertible to a combination of tabletop RPG, board game, card game and dice
rolls, it is too complex for NooPunk's current strategy/RPG scope."* The author's distinction is decisive
and easy to lose: this is a **tabletop-convertible complexity ceiling, not a tabletop-manufacturable
component ceiling** — dozens of decks, four or more views, large card libraries, hidden state and
automation are acceptable in a digital game; finite, intelligible player-facing actions and transparent
resolution rules are the real constraint.

| # | Criterion | Position | Basis on current `main` |
| --- | --- | --- | --- |
| 6.1 | Any new system can be described as **board state + pieces/cards + available actions + resolution rule + state transition** (with optional dice and character stats) | **MET AS DOCUMENTATION** | the rule is recorded here and in `strategy_game/docs/NOOPUNK_GLOBAL_DESIGN.md`; the existing vocabulary it is applied to is `tabletop/` (board, cards, dice, history), `quantities.py`, `council.py` and `characters.py`'s card types |
| 6.2 | A designer can explain the *player's decision and its outcome* without invoking an opaque high-fidelity simulation | **MET AS DOCUMENTATION** | recorded; the existing structure keeps the decision separable from the outcome — a declaration is a declaration (`council.MissionDeclaration`, `turn.record_declaration`) and an outcome is a rule outcome (`turn.record_character_check`) with **no prose field** on it |
| 6.3 | Persistent ideological/network dynamics are represented by understandable variables and discrete updates | **MET AS STRUCTURE** | `strategy_game/quantities.py` names the six quantities that must stay distinct (opinion/support; membership/resources; legislative seats; office; institutional access; Laclauian hegemony), following [`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §7 — and no scalar "influence" field exists anywhere in it. Centrality is *displayed, never stored* (`STRUCTURAL_FORKS_AND_DECISIONS.md` §4.2 records the one place a scalar does exist: `local_slice.Party.network`, fork 4, untouched) |
| 6.4 | Agent-led activation of passive faction resources governs major strategic operations | **MET AS STRUCTURE** | same enforcement as 2.2: a named agent is *required* by `council.MissionDeclaration` and by `psi_operations.PsiOperationLedger.declare()` |
| 6.5 | Multiple boards, many card decks and complex digital presentation are **explicitly allowed** if the underlying rules remain simple and auditable | **MET AS DOCUMENTATION** | recorded verbatim in the author's terms above; `VISION.md` §3's zoom levels and the four-view architecture are the existing framing, cross-linked rather than restated |
| 6.6 | Evaluate a small vertical slice: one political event, one agent-led mission, a faction-resource choice and an updated global network/political outcome | **MET AS STRUCTURE** | `python -m strategy_game.global_slice` runs exactly that: a discovered site, an agent activating one passive resource, a player approach choice, an outcome, and a political-consequence log line. It is an **evaluation prototype** whose own README section lists *"author approval still required"* for the skill/TAG vocabulary, dice mechanism, difficulty scales, asset economy, political transitions, combat, encounter writing and UI. It evaluates the shape; it approves nothing |

---

## 7. What is gated, and on exactly which gate

Nothing above is waived. The four gates are the ones [`RULE_SYSTEM_RESEARCH.md`](../../strategy_game/docs/RULE_SYSTEM_RESEARCH.md)
declares, and no gate has closed since:

| Criterion | Gate | What would satisfy it | Who owns the mechanic today |
| --- | --- | --- | --- |
| 1.3, 2.1 (resolver half), 5.1 (rules), 5.2 (values), 5.3 | **Gate C — strategy rules** | an approved agent-led resolution rule: what committed resource quantity and quality, an agent's check and player choices produce, and what an outcome means | the handoff routes the unified mission resolver to [#347](https://github.com/TomiToivio/NooPunk/issues/347) with scope coordination in [#309](https://github.com/TomiToivio/NooPunk/issues/309) |
| 3.3 (cross-layer chain), 3.5 (transitions) | **Gate B — political-simulation methodology** | approved causal assumptions and a play loop for the political field | [#309](https://github.com/TomiToivio/NooPunk/issues/309) |
| 2.5 (per-domain difficulty), 5.2 (difficulty) | **Gate A — leader RPG rules** | only the *personal-scale* half is approved today (the Fate slice, #389); anything beyond it is Gate A | [#347](https://github.com/TomiToivio/NooPunk/issues/347) |
| 2.5, 4.3 (integration contract proof) | **Gate D — integration contract and prototype playtest** | evidence from a playtested integrated slice | [#347](https://github.com/TomiToivio/NooPunk/issues/347) / [#309](https://github.com/TomiToivio/NooPunk/issues/309) |
| 3.6 | **not a gate — a structural fork (D1)** | the author choosing the scenario's period | author; [`STRUCTURAL_FORKS_AND_DECISIONS.md`](STRUCTURAL_FORKS_AND_DECISIONS.md) §3.6 |
| 3.2 (roster count) | **not a gate — a structural fork (D2/D3)** | the author choosing the roster's granularity and the Orion formal name | author; same record, §3.6 |

**Two more things left open, named so they are not mistaken for settled:** the *detection, defence and
counter-intrusion* model for cyber targets, and *whether Safenet reachability varies by region and by
faction* — both listed as undecided in
[`CYBERSPACE_AND_CONNECTIVITY.md`](../../strategy_game/docs/CYBERSPACE_AND_CONNECTIVITY.md) §7 and both
belonging to #344.

---

## 8. What this record does not do

- It **decides nothing**: not D1, D2 or D3; not the `politics.py`/`political.py` vocabulary; not the
  `Controller`/`MoveProposal` duplicate; not `local_slice.py`'s parallel engine; not the 4/7/11 registers.
  All five forks are cross-linked from [`STRUCTURAL_FORKS_AND_DECISIONS.md`](STRUCTURAL_FORKS_AND_DECISIONS.md)
  and left exactly as open as they were found.
- It **adds no module, field, record, third spelling, seam or state engine** (§0), and it does not edit
  `council.py`, `turn.py`, `cyber.py`, `psi_operations.py`, `quantities.py`, `global_slice.py`,
  `local_slice.py` or any data file.
- It **adds no test, guard, schema lock or CI step**, and no assertion about prose ([#271]).
- It **changes no issue state.** Issue #338 was closed by PR #436's own closing keyword on 2026-10-13;
  this record is a comment-level addition to that closed issue and neither re-opens nor re-closes it. It
  writes no closing keyword anywhere.
- It **does not touch the legacy RPG** (`AGENTS.md` §0/#306): `RULEBOOK.md`, `rulebook/` and the Godot
  scaffold are untouched, the legacy rulebook is not read as a crossover rule, and
  `strategy_game/RULEBOOK.md` still records that faction strategy and political simulation rules are
  **not approved**.
- It **carries no licence or release decision**, and it does not restate any other issue's decision.

---

*Cross-refs: [`ISSUE_338_GLOBAL_HANDOFF.md`](ISSUE_338_GLOBAL_HANDOFF.md) (the closeout handoff — summarized
here, never restated) · [`STRUCTURAL_FORKS_AND_DECISIONS.md`](STRUCTURAL_FORKS_AND_DECISIONS.md) (the five
forks, incl. D1–D3) · [`VISION.md`](VISION.md) §3 · [`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §7 · [`AGENTS.md`](../../AGENTS.md)
§0/#306, §6 (20XX), §13 · [#271](https://github.com/TomiToivio/NooPunk/issues/271) ·
[#338](https://github.com/TomiToivio/NooPunk/issues/338) ·
[#344](https://github.com/TomiToivio/NooPunk/issues/344) · [#347](https://github.com/TomiToivio/NooPunk/issues/347) ·
[#309](https://github.com/TomiToivio/NooPunk/issues/309) ·
[`strategy_game/docs/RULE_SYSTEM_RESEARCH.md`](../../strategy_game/docs/RULE_SYSTEM_RESEARCH.md) ·
[`strategy_game/docs/CYBERSPACE_AND_CONNECTIVITY.md`](../../strategy_game/docs/CYBERSPACE_AND_CONNECTIVITY.md) ·
[`strategy_game/docs/PSI_OPERATION_SEAM.md`](../../strategy_game/docs/PSI_OPERATION_SEAM.md) ·
[`strategy_game/docs/COUNCIL_LAYER.md`](../../strategy_game/docs/COUNCIL_LAYER.md)*
