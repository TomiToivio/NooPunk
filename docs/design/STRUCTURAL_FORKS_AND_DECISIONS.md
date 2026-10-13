# Structural forks and the decisions they need (record only)

**Status: RECORD ONLY. This document resolves nothing, edits nothing, chooses nothing and adds no
test.** It makes five accumulated structural forks — four already on record, one found while writing
this — cheap for the author to decide by stating, for each: the **verified facts** with file and line,
the **interpretation** kept separate from them, **why leaving it matters** (the concrete consequence,
which open issues it complicates, and what future code inherits), and the **options with their
measured consequences**. It picks none.

**Boundaries this record holds.**

- **No file in the repository is edited**, and none of the five subjects is touched: `session.py`,
  `controllers/`, `politics.py`, `political.py`, `local_slice.py`, `global_factions.json`,
  `un_parties.yaml`. No merge, no deletion, no consolidation, no rename.
- **No mechanic, number, statistic, typology, name, date or canon is created.** The setting is
  **20XX**; no exact future date is assigned here (`AGENTS.md` §6).
- **No test, guard, schema lock or CI step covers this document** — it is prose and is reviewed
  editorially and by playtesting ([#271](https://github.com/TomiToivio/NooPunk/issues/271),
  [`AGENTS.md`](../../AGENTS.md) automated-tests policy). It adds no documentation gate either.
- **Legacy canon is untouched** ([#306](https://github.com/TomiToivio/NooPunk/issues/306),
  `AGENTS.md` §0): `RULEBOOK.md`, `rulebook/` and the legacy RPG are not read as crossover rules, and
  `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**.
- **It is not a defect report against a person.** Four of the five forks are honest artefacts of
  developing one layer at a time (`AGENTS.md` §2); what makes them worth a decision now is that each
  is *about to become load-bearing*, not that it was wrong to land.

**Method.** Every subject was read on a freshly-fetched `origin/main` at `d8763b2` (2026-10-13), and
re-verified **unchanged** at `5341b5c` and `9111ad5`: the cited source modules — `session.py`,
`controllers/`, `politics.py`, `political.py`, `local_slice.py`, `characters.py`, `relationships.py`,
`core.py`, `global_factions.json`, `un_parties.yaml` — are byte-identical across all three revisions,
so line numbers hold. Every "measured" line below is **executed output**, not a reading: the two
probe scripts are described in §7 and their output is quoted in §1.2 and §4.1, and both test suites
were run at the current base (§7 records their state, including a transient red episode `main` passed
through while this record was being written). Where a claim is inference rather than measurement, the
word **interpretation** marks it.

**Related records, not repeated here.** This document does not restate
[`ISSUE_328_ROSTER_RECONCILIATION.md`](ISSUE_328_ROSTER_RECONCILIATION.md) (the 4/7/11 measurement),
[`ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md`](ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md) (the entity-kind
analysis), [`V1_DISCOURSE_AND_NETWORK.md`](V1_DISCOURSE_AND_NETWORK.md) §2 (the two-vocabulary
comparison), or [`ISSUE_304_GM_TURNS_AND_CONTROLLERS.md`](ISSUE_304_GM_TURNS_AND_CONTROLLERS.md)
(the controller protocol). It cites them, adds what they do not measure, and puts the five decisions
side by side so they can be taken together or in any order.

**And it is not the same artefact as [`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md).** That
record (which landed while this one was being written) is a **per-issue queue of 14 author questions**
whose purpose is *"so the answers can be given in one pass"*; its rows are each anchored to the issue
they block. Its scope and this document's are complementary, measured against each other: the queue
carries **no row** for forks 1, 2 or 5 above, and none for fork 4's scalar question; its row `D8`
(*"Reconcile the legacy UN party records with the established UN world government and eleven
parties"*) touches fork 3's subject without carrying the count, the period or the granularity question
that `ISSUE_328_ROSTER_RECONCILIATION.md` §4 puts to the author. Conversely, this document does not
answer the queue's rows about the twelve leader seats, the M4/M5 mechanics, PSI vocabulary, the
Archaic Revival's owner or the five ideological axes — those are per-issue questions, not structural
forks, and they are left where they are.

---

## 0. The five forks at a glance

| # | Fork | Class | Where it lives | State of the record today |
|---|---|---|---|---|
| 1 | `Controller` and `MoveProposal` each declared **twice** with different shapes | duplicate specification in one package | `session.py` vs `controllers/` | each side has its own design record; **neither records the collision** |
| 2 | `politics.py` vs `political.py` — two political vocabularies | duplicate specification, different shapes | `strategy_game/` root | measured and **routed to the author** by `V1_DISCOURSE_AND_NETWORK.md` §2; decision open |
| 3 | 4 / 7 / 11 global-actor registers | duplicate roster, different axes | `data/world/`, `strategy_game/data/`, issue #328 | measured and routed; two later records disagree with the earliest one about how settled it is |
| 4 | `local_slice.py`'s parallel state engine, incl. `network: int` | competing state engine + scalar collapse | `strategy_game/local_slice.py` | named as *provisional playtest rules*; the scalar collapse is **not** recorded anywhere |
| 5 | **`Relationship` declared in `local_slice.py` and `characters.py`** (and again as `RelationshipEdge`) | duplicate name, different shapes | `strategy_game/` root | **not recorded anywhere** — found while writing this document |

**Why "cheap now" is a measured claim, not a slogan.** For forks 1, 2 and 5 the number of
non-test, non-`__main__` importers on `main` is **zero or one** (§1.3, §2.3, §5.3). Each decision is
therefore a change to code that nothing yet consumes. The same decisions after a rules engine binds
to one side are changes to consumed code plus to the records that depend on it.

---

## 1. Fork 1 — `Controller` and `MoveProposal` are each declared twice

### 1.1 Verified facts

| Fact | Evidence |
|---|---|
| `strategy_game/session.py` defines `class Controller` at **line 103** | `session.py:102-116` — a **frozen dataclass** with fields `id`, `kind`, `label`, and a `__post_init__` that validates `kind` against `CONTROLLER_KINDS` |
| `strategy_game/controllers/controllers.py` defines `class Controller(Protocol)` at **line 47** | `controllers.py:46-68` — a `@runtime_checkable` **Protocol** with `controller_id` (property), `controls(leader_id)`, `propose(state, *, leader_id)` |
| `strategy_game/session.py` defines `class MoveProposal` at **line 119** | `session.py:118-146` — **frozen**, fields `leader_id`, `controller_id`, `kind`, `location`, `target`, `declaration`, `turn` |
| `strategy_game/controllers/proposals.py` defines `class MoveProposal` at **line 88** | `proposals.py:87-105` — **not frozen**, fields `controller_id`, `leader_id`, `action_code`, `target_id`, `resources`, `rationale`, `provenance` |
| The two `MoveProposal`s share exactly **two** field names | measured: `shared: ['controller_id', 'leader_id']`; `session`-only `['declaration','kind','location','target','turn']`; `proposals`-only `['action_code','provenance','rationale','resources','target_id']` |
| Neither module imports the other | `session.py:50,51` imports `.local_slice` and `.provenance`; `controllers.py:35-43` imports `..capabilities`, `..core`, `..provenance`, `.proposals`. There is no import path between the two `Controller`s |
| Both definitions are **test-only** on `main` | the only importer of `strategy_game.session` is `strategy_game/tests/test_session.py:28` (the `src/concordia_runtime/session.py` hit is the legacy RPG's own module, a different file); the only importer of `strategy_game.controllers` is `strategy_game/tests/test_agent_boundary.py:35` |
| Both suites are green | `test_session.py`: **42** tests OK. `test_agent_boundary.py`: **43** tests OK |
| Neither design record names the collision | `docs/design/ISSUE_304_GM_TURNS_AND_CONTROLLERS.md` describes `session.py`; `strategy_game/docs/AGENT_BOUNDARY.md` describes `controllers/`. `AGENT_BOUNDARY.md:74` explicitly names the `politics.py`/`political.py` fork and the 4/7/11 roster as left to the author, and **does not name this one** |

### 1.2 Measured cross-type behaviour (executed, verbatim)

The two shapes do not merely differ — one direction fails loudly and the **other fails silently**.

```text
probe A: submit controllers.proposals.MoveProposal to session.SessionState
  RAISED AttributeError : 'MoveProposal' object has no attribute 'kind'

probe B: register controllers.NullAgentProvider as a session.Controller
  RAISED AttributeError : 'NullAgentProvider' object has no attribute 'id'

probe C: hand session.MoveProposal to controllers.ProposalRecorder
recorded without error; log length: 1
stored to_dict keys: ['controller_id', 'declaration', 'kind', 'leader_id', 'location', 'target', 'turn']
replayed type: strategy_game.controllers.proposals.MoveProposal
replayed action_code: ''
replayed rationale: ''
declared 'kind' survived replay: <absent>
declared 'declaration' survived replay: <absent>
JSON round-trip of a mixed log keeps the declaration: False
```

`ProposalRecorder.record()` (`proposals.py:211-214`) authorises on `controller_id`/`leader_id` only,
and both types carry those names, so it accepts the *other* `MoveProposal` and stores **its** dict
shape; `ProposalLog.replay()` (`proposals.py:168-175`) then rebuilds it as the *proposals-side* type
and silently drops `kind`, `location` and `declaration` — the free-text declaration the
`ISSUE_304_GM_TURNS_AND_CONTROLLERS.md` §1 turn sequence treats as the record of what the player
chose. The suite stays green through all of it.

### 1.3 Interpretation (offered, not asserted)

- This is the same class of defect `AGENTS.md` §13 names for rules: *"A **rules** difference is a
  defect: extract a shared specification rather than fork the rule"*, and *"Where a shared
  specification already exists … consume it rather than re-declaring the same values in a second
  runtime"* (`AGENTS.md:352-353`). Two names for one concept, in one package, with field sets that
  cannot accept each other's payloads, is a re-declaration rather than a shared specification.
- The cause is legible and not blameworthy: two units implemented the same #304 milestone in
  sequence (`CE0851D` landed `session.py`; `#385` landed `controllers/`), and the second named its
  package to *avoid* a `SessionState` collision (`AGENT_BOUNDARY.md:31-38`) without noticing the
  `Controller`/`MoveProposal` names were already taken.
- The **asymmetry is the interesting part**: `session.py` is the strict side (it validates `kind`
  against `MOVE_KINDS`), `proposals.py` is the permissive side (it is duck-typed and validates
  almost nothing). A future rules layer that reaches for the permissive side first inherits a path
  on which a declaration can lose its own content without any error.

### 1.4 Why it matters — the consequence of leaving it

- **What future code inherits.** The rules engine VISION.md §12 Step D asks for ("Headless Python
  implementation of the approved procedures") must accept *one* proposal type. Under the present
  arrangement, whichever it accepts, the other remains importable, same-named, and — per §1.2 —
  silently storable into a log that cannot replay it. `AGENTS.md` §10 ("avoid hard-coded canon",
  "make changes easy to replace") is served by deciding the shape **before** there is a consumer.
- **Which open issues it complicates.** #304 is the parent of both implementations and its remaining
  milestones (the approved action set, the resolution core, the GM menu — `proposals.py:73-84`,
  `AGENT_BOUNDARY.md:59-72`) all assume exactly one proposal record. #282's integration gate and
  VISION.md §12 Step C ("Specify the shared turn") both need a single declaration type to specify
  against.
- **Measured cost of waiting.** Today the collision is reachable only through tests. Every later
  consumer multiplies the cost of the choice, because the two designs differ in *kind*, not in
  detail: a frozen validated record with a turn (`session.py`) versus a mutable declarative record
  with provenance and no turn (`proposals.py`).

### 1.5 Options for the author — measured consequences, no choice offered

| Option | What it means mechanically | Measured consequence |
|---|---|---|
| **A. One canonical pair, the other deleted** | keep either side's design and remove the other's `Controller`/`MoveProposal` | Deleting `session.py`'s types (or the module) removes `strategy_game/tests/test_session.py`'s 42 tests at import; deleting `controllers/`'s types removes `test_agent_boundary.py`'s 43. Neither module has a runtime importer today, so **nothing else breaks**. One of two design records becomes superseded and needs its own note |
| **B. One canonical pair, the other a thin adapter** | keep both as records; make one a declared conversion of the other | Nothing breaks; the collision becomes a mapping. But the shape gap is large (§1.1: five fields unique to each side, and `turn` vs `provenance`), so the adapter must state what happens to `declaration`/`rationale` and to the missing `turn`. `test_session.py:328` pins the literal source line `"from .local_slice import MISSIONS"`, so a move of `MOVE_KINDS` away from `local_slice.py` changes that assertion too |
| **C. Keep both, declare the boundary between them** | two types stay, with an explicit statement of which layer owns which and a guard against the silent path in §1.2 | Nothing breaks and no code changes. The silent-loss path in §1.2 stays reachable and uncaught — measured today, and by construction the green suite says nothing about it |
| **D. Unify on the strict side, re-expressing the permissive fields** | one record carrying both `kind`+`turn` **and** `action_code`+`provenance` | Nothing breaks in the runtime. It changes the shape of the record the approved action set will be declared on — i.e. it pre-commits part of #304's reserved ruling (`proposals.py:75-84`) if taken before that ruling |

**Not offered as an option:** adding a third `Controller`/`MoveProposal` spelling.
`V1_DISCOURSE_AND_NETWORK.md` §2.3 states the same rule for the political vocabulary — a third
spelling for an existing concept is the drift the reconciliation exists to prevent.

### 1.6 Decision required

> **Which single `Controller` / `MoveProposal` specification is canonical for the crossover, and what
> becomes of the other — deletion, an adapter, or a declared boundary with a guard on the silent
> path?**

Anchored at #304 (protocol parent), #282 (integration), and VISION.md §12 Step C. **Left open here.**

---

## 2. Fork 2 — `politics.py` versus `political.py`

### 2.1 Verified facts

| Fact | Evidence |
|---|---|
| Two modules, one layer's vocabulary | `strategy_game/politics.py` (238 lines) and `strategy_game/political.py` (344 lines) both open with "Layer II" and both are containers-only |
| Same four-ish concepts, different shapes | `politics.py` has `SignifierKind` (`:36-52`, includes `UNSPECIFIED = "unspecified"`), `Demand` (`:95`), `Signifier` (`:126`), `Formation` (`:161`), `Frontier` (`:192`, a **node**), `RelationLayer` (`:72`); `political.py` has `SignifierRole` (`:48-56`, **no unclassified member**), `Demand` (`:106`), `Signifier` (`:133`), `Articulation` (`:164`), `Frontier` (`:191`, carries `signifier_id` + included/excluded demand lists), `PoliticalFormation` (`:259`), `CommunicativeTie` (`:224`), `PoliticalField` (`:293`) |
| Castells' power modes exist on **one** side only | `political.py:63-73` declares `PowerMode.PROGRAMMING / SWITCHING`. `politics.py:86-88` states the opposite in prose: *"Network-making, programming and switching are **not** modelled here — only the presence of a tie is recorded."* |
| **Both vocabularies are on the public package surface at once** | `strategy_game/__init__.py:13-24`: `from .core import WorldState` (and `core.py:8` imports `Demand, Formation, Frontier, Signifier` from **`.politics`**), while `__init__.py:14` does `from .political import PoliticalField, PowerMode, SignifierRole` and `__all__` exports `PoliticalField`, `SignifierRole`, `PowerMode`. Measured: `core.Demand.__module__ == 'strategy_game.politics'`, `strategy_game.PoliticalField.__module__ == 'strategy_game.political'` |
| The container is pinned **out** of `WorldState` by an executable test | `strategy_game/tests/test_political_contracts.py:285-296` — `test_the_field_is_not_nested_into_world_state` asserts `"political_field"` is not in `state.__dict__` **and** not in `state.to_dict()` |
| `politics.py` has its own numeric-field guard | `strategy_game/tests/test_political_layer.py::NoQuantifiedPoliticsTests` (40 tests in the module) covers `Demand, Signifier, Formation, Frontier` from `politics.py` |
| `political.py` has its own guard and its own import discipline | `test_political_contracts.py` (27 tests) asserts no numeric quantity and no metric-shaped key in `PoliticalField`, and asserts in a subprocess (`:270-283`) that importing `strategy_game.political` pulls in no optional adapter and no `laclaugpt` |
| `VISION.md` §12 Step B names this as a prerequisite step | `VISION.md:559` — *"Explicit mapping or consolidation decision for `politics.py` and `political.py`; stable identifiers and provenance semantics"*, exit condition *"One agreed representation for slice transitions; no silent loss of existing records"*. VISION.md:509 states the current state plainly: *"`politics.py` is integrated with `WorldState`, while `political.py` remains a separate vocabulary proposal."* |
| Two landed design records have already assumed `politics.py` | `docs/design/V1_DISCOURSE_AND_NETWORK.md` §2.2: *"This design assumes `politics.py`"* (a routed choice, not a settled one). `docs/design/NOOPUNK_GLOBAL.md` §M0.2's reuse table (`:39-51`) lists `Demand, Signifier, Formation, Frontier, RelationLayer` from `politics.py` as reusable **"Yes, as-is"** (`:44`) and does **not** list `political.py` at all |
| The comparison itself is already on record | `V1_DISCOURSE_AND_NETWORK.md` §2.1 tabulates the six differences (default role, enumerated roles, `Frontier` shape, programming/switching, `WorldState` wiring, guards) and §2.2 states the two consequences. This record verified those rows against the modules and found them accurate; it does not re-derive them |

### 2.2 Interpretation (offered, not asserted)

- The two modules are not rival implementations of one design; they are **two different questions**
  answered by two sessions: `politics.py` answers *"how is the articulation graph carried on the
  existing edge type"*, `political.py` answers *"what is the political *field* as a container"*.
  `VISION.md` §12 Step B nonetheless requires **one** agreed representation, because a rule written
  against one is not a rule against the other.
- The decision has drifted without being taken: two design records now assume `politics.py`
  (§2.1, last two rows). That is not a decision — it is a default accumulating through reuse. A
  default is the one outcome Step B's exit condition is written to prevent.
- The `SignifierKind.UNSPECIFIED` versus `SignifierRole | None` difference is load-bearing beyond
  style: `politics.py` stores the absence as a *value* (`"unspecified"`), `political.py` as `None`.
  An existing test asserts the absence is reported rather than upgraded
  (`strategy_game/tests/test_agent_ontology.py:175-178` pins a note that the fork *"stays open"* and
  is *"routed to the author"* — so the codebase already carries an executable statement that this is
  undecided).

### 2.3 Why it matters — the consequence of leaving it

- **The two consequences the earlier record measured, restated as decisions, not details:**
  1. Choosing `politics.py` **loses programming/switching entirely** — the Castells half of #297 has
     no home in `politics.py` (verified above: the vocabulary exists only at `political.py:63-73`, and
     `politics.py:86-88` states its absence). The choice therefore includes a second decision:
     **re-home or drop.**
  2. Choosing `political.py` **changes an existing executable test**: integrating `PoliticalField`
     into `WorldState` contradicts `test_political_contracts.py:295-296`, which pins that
     `political_field` is absent from `state.__dict__` and from `state.to_dict()`. The pin is correct
     behaviour — it is what stops the join happening by refactor — so the integration is a deliberate
     Gate D-style code change with its own approval, not a side effect.
- **What future code inherits.** A resolver (#297's layer), a view, or a rule written against one
  vocabulary silently does not apply to records stored in the other. Both guards (§2.1, rows 5–6)
  stay green either way, so the mismatch cannot be caught by the suite.
- **Which open issues it complicates.** The reconciliation is a named prerequisite of VISION.md §12
  Step B and §14's row B, feeding Step C (the shared turn) and Step D (the resolver). #297 owns the
  discourse/network layer whose Castells half is at stake. #282 owns the integration boundary.
  Global's actor model (`NOOPUNK_GLOBAL.md` M1) binds to whichever survives.
- **A tie-in worth seeing whole.** Step B's exit condition is *"no silent loss of existing records"*.
  Fork 1 already demonstrates a silent-loss path today (§1.2), in a different pair of modules, for the
  same structural reason: two same-named records with no declared mapping. Taking Step B is therefore
  also the occasion to state the rule that prevents Fork 1's recurrence.

### 2.4 Options for the author — measured consequences, no choice offered

| Option | What it means | Measured consequence |
|---|---|---|
| **A. Consolidate on `politics.py`** | `political.py` becomes superseded; one node/edge vocabulary | `politics.py` is already the one `core.py:8` imports and `view.py:21` reads (`RELATION_LAYERS`), so nothing in the runtime changes. **Programming/switching must be re-homed or dropped** — today it exists only at `political.py:63-73`. `strategy_game/__init__.py:14` and `__all__` (3 exported names) change; `test_political_contracts.py`'s 27 tests lose their subject and must be rewritten or removed by decision, not by refactor |
| **B. Consolidate on `political.py`** | `PoliticalField` becomes the layer's container and is joined to `WorldState` | **Two executable pins change**: `test_political_contracts.py:295-296` (the absence assertions) and `__init__.py`'s import surface. `core.py`'s four collections (`demands`, `signifiers`, `formations`, `frontiers`) and `view.py`'s political-node projection are re-pointed, and `test_political_layer.py`'s 40 tests re-point with them. `ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md` §6 cites `politics.Signifier.kind`/`RelationLayer` by name, as does `V1_DISCOURSE_AND_NETWORK.md` §2.2 — both would need a supersession note |
| **C. Keep both, declare the mapping** | the mapping Step B asks for, with one side named canonical for rules and the other for the container | Nothing breaks and no guard changes. The mapping must fix the two asymmetries explicitly (absence as `"unspecified"` vs `None`; `Frontier` as node vs as a record naming the signifier and the excluded demands), and must state which side a *rule* may be written against. It leaves two spellings live, which `V1_DISCOURSE_AND_NETWORK.md` §2.3 argues against — an argument, not a settled point |
| **D. A third, new vocabulary** | write one reconciled module | Explicitly refused by the existing record (`V1_DISCOURSE_AND_NETWORK.md` §2.3, *"No third vocabulary"*) and by the reasoning of §2.2 above; listed only so the option space is complete |

**What every option needs regardless:** the `WorldState`-wiring question is separable from the
vocabulary question. Step B names both ("stable identifiers and provenance semantics"), and
`test_political_contracts.py:285-296` shows the wiring is currently pinned **off**. Whichever
vocabulary survives, the author separately decides whether the surviving field is joined to
`WorldState` or stays id-coupled.

### 2.5 Decision required

> **Which single political vocabulary is canonical for the crossover, and — separately — is that
> field joined to `WorldState` or kept id-coupled?** If `politics.py` is canonical: **is the
> programming/switching vocabulary re-homed, or dropped?**

Anchored at VISION.md §12 Step B (§14 row B), #282, #297. **Left open here.**

---

## 3. Fork 3 — the 4 / 7 / 11 global-actor registers

### 3.1 Verified facts

| Register | Count | Artefact and status | Measured this session |
|---|---|---|---|
| **4** | 4 | [`data/world/un_parties.yaml`](../../data/world/un_parties.yaml) — Bioconservatives, Libertarian Party, United Earth Social Democratic Party, The Multitude, on an economic/social axis; the file declares `open_for_future_parties: true` and `extra_parliamentary_factions: true` (`:31-32`) | counted **4** `- name:` entries; both flags present |
| **7** | 7 | [`strategy_game/data/global_factions.json`](../../strategy_game/data/global_factions.json) — `"status": "author_canon"`, `"source_issues": [328, 329]` | counted **7** entries in `factions`: `accelerationists, cyborgists, critical, butlerian_jihad, confederacy_awakening, orion_grey_networks, normalcy_bloc` |
| **11** | 11 | issue [#328](https://github.com/TomiToivio/NooPunk/issues/328), **OPEN**, title *"Eleven global Parties: ideological hegemony, PSI/NHI paradigm shifts and the UN world government"*, body carrying an 11-row Party table | issue read via the API: state `OPEN`, `updatedAt` **2026-10-13T19:12:02Z** |

**The 7's own axis.** `global_factions.json:12-28` declares exactly three `entity_kinds`:
`human_ideological_formation`, `nhi_aligned_formation`, `latent_public`. The four entries with no
counterpart among the 7 are **MJ-12 / Continuity Directorate**, the **AIC** (rogue ASI swarm), the
**ERA** and the **HSDC** (issue #328's Parties 7, 8, 9, 10).

**The suite deliberately does not pin the count.** `strategy_game/tests/test_global_factions.py`'s
own docstring states: *"They deliberately do **not** assert which factions exist, how many there are,
or what any faction says — that is authored canon, reviewed editorially and by playtesting, not frozen
in CI."* Measured: no assertion on the length of `factions` appears in that module. So changing the
count is a **test-free** change by design ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

### 3.2 Does `ISSUE_328_ROSTER_RECONCILIATION.md` agree with `NOOPUNK_GLOBAL.md` §6B.3, or contradict it?

**It agrees on every fact and contradicts §6B.3's conclusion.** Precisely:

| Point | `NOOPUNK_GLOBAL.md` §6B.3 (`:378-392`) | `ISSUE_328_ROSTER_RECONCILIATION.md` | Verdict |
|---|---|---|---|
| The three counts are real and live on `main` | *"All three counts are real and live on `main`"* (`:388`) | reads and counts all three the same way | **AGREES** |
| The lists are different taxonomies | *"They are **different taxonomies**"* (`:390`) | §1: the **4** is *"a separate register"*, *"no conflict"* | **AGREES** |
| Which kind of mismatch (count / taxonomy / both) | *"The discrepancy **may be** a **count** mismatch, a **taxonomy** mismatch, or both — **I did not determine which**"* (`:390`) | §1: *"4-vs-11 is **not** a count mismatch — it is a different register"*; and 7-vs-11 is *"the same taxonomy at different granularity"* with *"the count difference … exactly 11 − 7 = 4"* | **CONTRADICTS** — the reconciliation determines what §6B.3 left undetermined |
| Whether the three describe the same set at all | *"Whether these three lists are meant to describe the **same** set of actors at all"* — stated as **unconfirmed** (`:390`) | the 4 is a different register; the 7 and the 11 **are** one register at two granularities | **CONTRADICTS** |
| What Global should do meanwhile | *"The count should be settled before any design binds to a number"* (`:392`) | same practical instruction, expressed as D1–D3 | **AGREES** |

**So the answer is: agrees on the evidence, supersedes on the inference.** §6B.3 is dated earlier and
its honest "I did not determine which" was correct at the time; the reconciliation is later and does
the determining. The one sentence in §6B.3 that is now **false** is the "different taxonomies"
characterisation applied to *all three*: 7 and 11 are one taxonomy, so their difference cannot be a
taxonomy difference, only a completeness difference. (§6B.3's own framing as *"a data-integrity
question, **not** a design decision"* is also superseded in practice: the reconciliation and the
Party-stratum record both show D1 changes the **setting's period**, so it is a design decision with a
data-integrity component.)

**A verified drift worth recording.** §6B.3 cites the issue as *"author-updated
**2026-10-12T15:55:15Z**"* (`:386`). The live issue's `updatedAt` is **2026-10-13T19:12:02Z** — the
issue has been updated again since that row was written. The row's *count* (11, from the title and
table) still holds; the timestamp does not. `ISSUE_328_ROSTER_RECONCILIATION.md`'s own method line
*"read on `origin/main` at `3d17524`"* is also a superseded base — `3d17524` is still an ancestor of
`origin/main` (verified) but `origin/main` has moved to `d8763b2`. Neither staleness changes a count;
both are the ordinary cost of a record that quotes a live artefact.

**Two later records, and where they stand relative to both.** On `main` now:
`ISSUE_328_GLOBAL_FACTIONS_ROSTER.md:437` asserts *"Both issues state the same seven-faction
roster"*; `ISSUE_328_ROSTER_RECONCILIATION.md` §3 logs that sentence as **now false** against #328's
eleven, and `ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md` §1-§5 restates the count conflict as *"a reading,
not a measurement"* while naming the four exceptions as **entity-kind** exceptions. Its §5 supplies
the precise formulation: **"One shared taxonomy for seven entries, plus a category difference for
four."**

### 3.3 Interpretation (offered, not asserted)

- The disagreement inside §6B.3 is not about numbers. It is about **what kind of question this is**:
  §6B.3 calls it a data-integrity question; the later records show the same evidence also decides
  whether the scenario's world government **exists at start** (D1) and whether four Parties can hold
  world-level seats at all. A count question is cheap; a period question is not.
- The "one shared taxonomy plus a category difference" formulation is the only reading that neither
  calls an `author_canon` file wrong nor pretends four Parties fit an axis that canon forbids placing
  one of them on. That is an argument for it, not a decision — three readings remain live
  (`ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md` §4: A granularity, B two strata, C competing rosters).
- The 4 should not be treated as a defect. `un_parties.yaml:31-32` declares itself non-exhaustive,
  and both later records agree the 4 is a different register. Merging it is the error to avoid.

### 3.4 Why it matters — the consequence of leaving it

- **What future code inherits.** Global's own actor model binds to a roster size and to an
  entity-kind list (`NOOPUNK_GLOBAL.md` §M0.5, §M1.1). If the design binds to "a handful of factions"
  before the count is settled, it encodes one of the three readings arbitrarily — the risk
  §6B.3 itself names at `:392`.
- **Which open issues it complicates.** [#338](https://github.com/TomiToivio/NooPunk/issues/338) is
  where §6B.3 is anchored and is **OPEN** (9 comments); its checklist is what `NOOPUNK_GLOBAL.md`
  answers. #328 is **OPEN** and
  `ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md` §9 states plainly: *"Until that is the author's, #328
  stays open."* `ISSUE_328_ROSTER_RECONCILIATION.md` §4 puts D1 (the period), D2 (granularity) and
  D3 (the Orion formal name) to the author; D1 is blocking, in its own words, because *"a Global
  design will otherwise be built on one and documented against the other."*
- **What is already stale because of it.** Measured: `global_factions.json` contains **zero**
  occurrences of `official_name`, while the two records describe *"every one of the seven
  `official_name` values is `null`"* — "absent" and "null" are different facts
  (`ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md` §8 records this correction). The file's own
  `open_questions.roster_closed_at_seven` (`:345-348`) had its **count** half superseded by #328's
  revision while its **umbrella** half stays open.

### 3.5 Options for the author — measured consequences, no choice offered

| Option | What it means | Measured consequence |
|---|---|---|
| **A. Extend 7 → 11** | the data file grows to the eleven | **Test-free by design**: `test_global_factions.py` pins no count (measured). `ISSUE_328_GLOBAL_FACTIONS_ROSTER.md:437` becomes true again; `ISSUE_328_ROSTER_RECONCILIATION.md` §3's staleness table and `ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md` §3 must be superseded by note, since both argue the four do not fit the 7's `entity_kinds` axis — the file would then need a fourth kind or `null` kinds, and canon forbids placing MJ-12 on the compass |
| **B. Two strata** | the 7 stay the paradigm stratum, the 11 the Party stratum, with 4 Parties having no paradigm entry | matches the "one taxonomy + a category difference for four" formulation. Nothing in code changes (no test pins either). The four need a **named** home for the stratum they belong to, or the world's actor set stays in issue prose only — which is where it is today |
| **C. One roster, the other superseded** | declare which of the 7-file / the 11-table is canonical | Nothing in code changes. One of two `author_canon`-adjacent records acquires a supersession note; the other becomes the single register that `un_parties.yaml` stays distinct from |
| **D. Leave it open, binding nothing** | status quo | measured cost: two design records (Global; the Party-stratum record) keep assuming a roster while stating they bind to none, and each new doc has to restate the caveat. §6B.3's own warning stays live |

### 3.6 Decision required

> **D1 — the period: does the strategy scenario start with a UN world government already established,
> or before one exists?** (The two governing artefacts say opposite things —
> `ISSUE_328_GLOBAL_FACTIONS_ROSTER.md:317-321` versus #328's revision — and whichever holds, the
> other artefact is corrected deliberately.)
>
> **D2 — the roster's granularity and kind: is `global_factions.json` extended to eleven, or do
> MJ-12, the AIC, the ERA and the HSDC belong to a differently-named stratum — and if the latter,
> what is that stratum called?**
>
> **D3 — the Orion formal name:** confirm **Greater Orion Arm Co-Prosperity Sphere** so the
> never-written `official_name` field can be created, while the other six stay pending.

Anchored at #338 (§6B.3) and #328 (the eleven, and its own open checkbox list). **Left open here.**

---

## 4. Fork 4 — `local_slice.py`'s parallel state engine, and the integer stocks

### 4.1 Verified facts

| Fact | Evidence |
|---|---|
| Four dataclasses parallel to `core.py`, in the same package | `local_slice.py:18-56` declares `Leader` (`:19`), `Party` (`:31`), `Relationship` (`:43`), `Mission` (`:51`); `core.py:12-58` declares `Leader` (`:13`), `Faction` (`:21`), `Asset` (`:29`), `Location` (`:37`), `NetworkEdge` (`:45`), `Event` (`:52`) |
| `Leader` is declared twice with disjoint fields | measured: `core.Leader` = `('identifier','name','attributes','personality_tags')`; `local_slice.Leader` = `('id','name','faction','location','portfolio','skill','status','traits')` — one shared field name, `name` |
| `local_slice.Party` declares four **integer stocks** | measured field types (`local_slice.py:31-39`): `treasury: int = 8`, `legitimacy: int = 5`, **`network: int = 2`**, `technology: int = 0` |
| `local_slice.Relationship` declares a **fifth** integer | `local_slice.py:43-47`: `a, b`, **`trust: int = 0`**, `tags` |
| Those integers are mutated by the turn loop | `local_slice.py:140-157` (passive portfolio effects: `treasury += 1`, `network = min(10, network + 1)`, `legitimacy = min(10, legitimacy + 1)`) and `:161-183` (mission costs and successes), plus `:168` (`rng.randint(1,6) + l.skill + bonus - travel - location["pressure"]`, threshold `roll >= 5` at `:169`) |
| `local_slice` is a real, consumed engine — not dead code | `Game`/`Game.from_scenario()` are imported by `strategy_game/scenario_schema.py:223-236`; `PORTFOLIOS` by `scenario_schema.py:24` and `MISSIONS` by `session.py:50`; `tabletop/bridge.py:111,213` builds a board from the slice; `render/text.py:138` adapts it to `WorldState`. Tests: `test_local_slice.py` (4), `test_scenario_schema.py` (11), `test_render_text.py` (14), `test_board_local_projection.py`, `test_session.py:26,328` |
| The two engines meet at a **lossy** seam, measured | `render/text.py:138-172` `state_from_local_slice()` copies locations, parties→`Faction`, leaders→`Leader` and routes→`NetworkEdge`, then returns a `WorldState`. Measured on the shipped `data/ukweli_local.json`: the resulting snapshot's keys are `['assets','demands','edges','events','factions','formations','frontiers','leaders','locations','schema_version','signifiers']`, and `treasury`, `legitimacy`, `network`, `technology` and `trust` are **all absent** from it (`'treasury' in blob → False`, etc.). The slice's `Party` stocks start at `8 / 5 / 2 / 0` and none of them reaches the shared core |
| The boundary is already written down as provisional | `strategy_game/docs/LOCAL_SLICE_RULES_PROVISIONAL.md`: *"These rules are **unapproved playtest assumptions** in `local_slice.py`"*. `local_slice.py:1-5` says *"All mechanics are small deterministic *playtest assumptions*, not validated social theory."* |
| The scalar collapse is **not** recorded as a defect anywhere | `grep` over `docs/design/` and `strategy_game/docs/` for a scalar/stock/collapse note about `treasury`/`legitimacy`/`network` returns nothing. The guards that exist are for the political records only (`test_political_layer.py::NoQuantifiedPoliticsTests`; `test_political_contracts.py`) |

### 4.2 Interpretation (offered, not asserted)

- Two different things live in one finding and are worth separating.
  1. **A second state engine.** `local_slice.Game` holds `locations, routes, parties, leaders,
     relations, shocks, turn, history, support` (`:59-69`) and advances them in `step()` (`:108`).
     `core.WorldState` holds a different set (`core.py:82-98`). `AGENT_BOUNDARY.md:37` names the shape
     of this risk in its own words — *"how a *competing state engine* starts"* — and avoids it for
     `controllers/` by not minting a rival `SessionState`. Here a rival state engine already exists
     and is **consumed**, with a view adapter (§4.1, row 6) bridging it lossily.
  2. **A Castellsian collapse.** `Party.network: int` makes network power a **scalar stock** owned by
     a faction. This is the specific collapse the project's records forbid in several places:
     `NOOPUNK_GLOBAL.md` §M1.0 (*Castells … "**Not a scalar 'network power' score**"*), §M1.5
     (*"derived graph quantities … **computed, never stored as a scalar political score**"*), §7
     (*"**#6** … not a scalar"*), §8.4 (*"Derived graph quantities — reach, brokerage, centrality:
     computed and shown, not held"*), and `V1_DISCOURSE_AND_NETWORK.md` §4 (*"a tie is a channel, and
     nothing else"*; centrality *"fine to display, never a modifier"*). `trust: int` on
     `local_slice.Relationship` is the same move at person scale, against
     `relationships.py`'s own *"A **named position**, never a number"* (`:125`).
- The `network // 3` mission bonus (`local_slice.py:165`) is the mechanism that makes the collapse
  observable rather than cosmetic: the scalar **modifies** an outcome, which is exactly the
  *"gate vs modify — never both"* fork `V1_DISCOURSE_AND_NETWORK.md` §4.3 leaves open. The slice has
  silently taken the "modify" side.
- This is honest for what it is. The slice's own docs call it unapproved playtest assumptions; a
  playtest assumption may be a number. What is not recorded is that it is a **number of the kind the
  design forbids**, so a reader who finds `Party.network` has no way to tell "provisional prototype"
  from "agreed design".

### 4.3 Why it matters — the consequence of leaving it

- **What future code inherits.** Every consumer of the slice inherits a state engine whose
  quantitative vocabulary is incompatible with the shared core's — measured: the seam drops all five
  integers (§4.1, row 6). A future rule that reads `Party.network` cannot be exercised through
  `WorldState`; a future rule that reads graph shape cannot see anything the slice stores.
- **Which open issues it complicates.** #322/#323/#324 own the local slice; the four-portfolio,
  one-leader-per-move council is #323's, and VISION.md §7b's hard cap is *"One resolution mechanism,
  reused everywhere — not one per pillar."* #296/#297 own the faction and network halves whose
  quantities the stocks anticipate. VISION.md §12 Step B's exit condition — *"no silent loss of
  existing records"* — is measured **not** met at this seam.
- **The precise risk of leaving it unlabelled.** The next unit that needs "how connected is this
  faction?" will find `Party.network` already there, already an int, already affecting rolls. Nothing
  in the suite objects: `test_local_slice.py` (4 tests) and `test_scenario_schema.py` (11) exercise
  behaviour, and no test asserts the absence of a network scalar. The `NoQuantifiedPoliticsTests`
  guard covers `politics.py`'s four records only — it does not reach `local_slice.py`.

### 4.4 Options for the author — measured consequences, no choice offered

| Option | What it means | Measured consequence |
|---|---|---|
| **A. Keep the slice as a declared prototype, label the stocks** | one explicit statement that `treasury`/`legitimacy`/`network`/`technology`/`trust` are provisional playtest integers owned by an unapproved slice, and that none of them is the layer's quantity | Nothing changes in code; nothing breaks. `Party.network` stops being readable as design. The slice's own docs already say "unapproved" — what is missing is the **per-field** statement, since the forbidden quantity is a specific one, not numbers in general |
| **B. Migrate the slice onto `core.py`'s containers** | `local_slice` consumes `WorldState`/`Faction`/`Leader` instead of its own dataclasses | Breaks or rewrites by construction: `data/ukweli_local.json`'s party/leader shapes feed `Party(**p)`/`Leader(**x)` (`local_slice.py:76-77`) and would need a mapping; `scenario_schema.py`, `tabletop/bridge.py`, `render/text.py` and `test_local_slice.py`'s 4 / `test_scenario_schema.py`'s 11 / `test_render_text.py`'s 14 / `test_board_local_projection.py`'s tests re-point. `test_render_text.py:82` explicitly asserts the adapter *"copies declared content only"*, so the seam's lossiness is **intended** and the migration is a deliberate reversal of it |
| **C. Replace the four integers with structural state** | network becomes graph shape (already available as `NetworkEdge`/`Location` in `core.py`), legitimacy/treasury become named positions or nothing, `trust` becomes a named position | Changes the resolver's arithmetic (`:165-169`): the `network // 3` and `trust // 2` bonuses disappear, and with them the roll modifiers, so `local_slice`'s turn output changes and its tests' expectations change with it. This is a **rules** change, so it needs the author's approval of the replacement mechanic — which does not exist (`RULEBOOK.md`: NO RULES APPROVED) |
| **D. Split the fork: keep the dataclasses, drop only the scalars** | the second engine stays for its playtest shape; the forbidden quantities go | Localised: `Party` (`:31-39`), `Relationship` (`:43-47`), and the four mutations at `:140-157`, `:161-183`, `:191`. Same arithmetic consequence as C for the modifiers, and the same approval requirement |
| **E. Leave it exactly as it is** | nothing changes | Measured cost: the next reader meets a scalar Castellsian quantity in consumed code with no label distinguishing it from design; every later record has to say "provisional" again |

### 4.5 Decision required

> **Is `local_slice.py` a parallel state engine the crossover keeps — and if so, is it labelled
> *per field* as an unapproved prototype — or is it migrated onto `core.py`? Separately: do
> `treasury`, `legitimacy`, `network` and `technology` (and `Relationship.trust`) remain integer
> stocks in a prototype, or are they replaced by structural state — which is a rules change needing
> its own approval?**

Anchored at #322/#323/#324 (the local slice), VISION.md §7b and §12 Step B. **Left open here.**

---

## 5. Fork 5 — `Relationship` is declared in two modules, and twice more under other names

**Recorded because it is the same class of defect and it was not on record. It was found while
writing this document; it is not in the four findings above, and nothing here had named it.**

### 5.1 Verified facts

| Fact | Evidence |
|---|---|
| `strategy_game/local_slice.py` declares `class Relationship` at **line 43** | fields `a`, `b`, `trust: int = 0`, `tags: list[str]` |
| `strategy_game/characters.py` declares `class Relationship` at **line 173** | a **frozen** dataclass with fields `other_id`, `kind`, `visibility: CardVisibility = PUBLIC`; `__post_init__` refuses a blank `other_id` or `kind` |
| They share **no** field name | measured: `('a','b','trust','tags')` vs `('other_id','kind','visibility')` |
| A third name for a third shape | `strategy_game/relationships.py:107-153` declares `RelationshipEdge` — a mutable, stateful tie with `identifier, holder_id, other_id, kind, role, state, state_vocabulary, state_rationale, tags, typed_tags, goals, obligation, visibility, observable, inferences, state_history, gm_notes, detail` |
| Both `Relationship` definitions are live | `characters.py` has **six** non-test importers (measured): `codex/entities.py`, `faction_cards.py`, `relationships.py`, `render/__main__.py`, `render/text.py`, `rpg/fate.py`. `relationships.py` has three (`council.py`, `founding_story.py`, `relationship_seam.py`) — so the mutable `RelationshipEdge` is reached through the same modules that own the card vocabulary. `local_slice.Relationship` is constructed from scenario JSON at `local_slice.py:78` and mutated at `:190-191`. Tests: `test_character_cards.py` (62), `test_relationships.py` (32), `test_render_text.py` (14) |
| No test or document notes the name collision | `grep` over `docs/design/` and `strategy_game/docs/` finds the `politics`/`political` fork named explicitly (`AGENT_BOUNDARY.md:74`, `V1_DISCOURSE_AND_NETWORK.md` §2) and the 4/7/11 roster named explicitly — **not** this one |
| The three shapes already disagree on the one thing the project is strict about | `relationships.py:125` states the rule: *"A **named position**, never a number."* `characters.Relationship` satisfies it (a `kind` string). `local_slice.Relationship` does not (`trust: int`, and `relationship.trust // 2` is read as a bonus at `local_slice.py:166`) |

### 5.2 Interpretation (offered, not asserted)

- Unlike forks 1, 2 and 4, this is primarily a **name** collision rather than a semantic
  contradiction: a card-facing tie and a playtest tie are plausibly different concepts. Three
  modules, three shapes, one word is nonetheless the same defect class `AGENTS.md:352-353` names, and
  it is the exact case `test_agent_ontology.py:175-178` was written to watch for — *"No third
  spelling"*.
- The substantive part is small and separable: only `local_slice.Relationship.trust` breaks the
  "named position, never a number" rule, and it is the same integer problem as Fork 4's
  `Party.network`. If Fork 4 is answered, this mostly answers with it.

### 5.3 Why it matters — the consequence of leaving it

- **What future code inherits.** A new tie-related rule or card must choose among three names; two of
  them are spelled identically, so an import decides the semantics silently. Nothing in either suite
  objects (both `test_character_cards.py`'s 62 and `test_relationships.py`'s 32 tests pass).
- **Which open issues it complicates.** #346 (faction cards and typed tags) and #389 (the RPG
  attribution/seam work) are the tracks that mint ties most often, and `relationships.py` already
  carries issue #346's typed-tag vocabulary through `characters.Tag` (`relationships.py:135-138`) —
  i.e. the two modules are **already coupled** while sharing a name with a third module's unrelated
  record.
- **Cost of deferral is bounded.** Unlike forks 1–4, no design record depends on the answer, so this
  one can be taken last without blocking anything. Saying so is the point: not every fork is urgent,
  and this record does not inflate it.

### 5.4 Options for the author — measured consequences, no choice offered

| Option | What it means | Measured consequence |
|---|---|---|
| **A. Rename the prototype's record** | `local_slice.Relationship` becomes e.g. a playtest-scoped name | Nothing breaks in behaviour. Touch points are localised: `local_slice.py:43, 78, 101, 190-191`, `data/ukweli_local.json`'s `"relationships"` key mapping (`:78`), and whichever of `test_local_slice.py`'s 4 tests reference the type. `characters.Relationship` and `relationships.RelationshipEdge` are untouched |
| **B. Rename the card-facing record** | `characters.Relationship` adopts a distinct name | Wider: `characters.py` has six non-test importers (measured, §5.1) and `test_character_cards.py`'s 62 tests exercise it; `relationships.py` already uses `other_id`/`kind` in its own shape, so a rename would also have to distinguish *it* from `RelationshipEdge` |
| **C. Declare the boundary and add nothing** | one written sentence naming which module owns which tie, plus the `trust` scalar left to Fork 4 | Nothing changes; the three shapes stay. Measured: no test covers it today, and the record is the only artefact either way |
| **D. Fold the prototype's tie into `characters.Relationship`** | one card-facing record for all ties | Breaks by construction: `characters.Relationship` is frozen with no `trust` and no `a`/`b` pair, while `local_slice` reads `r.trust` at `:101, 166, 191`; the fold therefore carries Fork 4's scalar decision with it |

### 5.5 Decision required

> **Which module owns a "relationship" record, under which name — and does the prototype's
> `trust: int` survive as a prototype number, or does it become a named position (which is the
> `relationships.py` convention and a rules change)?**

Anchored at #346, #389, and `V1_DISCOURSE_AND_NETWORK.md` §2.3's no-third-spelling rule. **Left open
here.**

---

## 6. The decisions, collected — no recommendation attached

| # | Decision | Anchored at | Blocking? (per the citing record) |
|---|---|---|---|
| 1 | Which `Controller`/`MoveProposal` spec is canonical; what becomes of the other (deletion / adapter / declared boundary + guard on the silent path) | #304; #282; VISION.md §12 Step C | **Yes for Step D** — the resolver needs one declaration type. No runtime consumer today (measured) |
| 2a | Which political vocabulary is canonical (`politics.py` / `political.py` / declared mapping) | VISION.md §12 Step B, §14 row B; #282; #297 | **Yes** — Step B is a named prerequisite of Steps C–D, and two landed design records have already assumed `politics.py` |
| 2b | If `politics.py` wins: is programming/switching re-homed or dropped? | same | **Yes** — it exists only at `political.py:63-73` |
| 2c | Is the surviving political field joined to `WorldState` or kept id-coupled? | `test_political_contracts.py:285-296` | **Yes** — currently pinned **off** by an executable test; joining is a deliberate change |
| 3-D1 | The period: UN world government already established, or not yet | `ISSUE_328_ROSTER_RECONCILIATION.md` §4 D1; #328; #306 | **Blocking**, in that record's own words — a Global design will otherwise be built on one artefact and documented against the other |
| 3-D2 | Roster granularity and kind: extend to eleven, or name a second stratum for MJ-12 / AIC / ERA / HSDC | §4 D2; `ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md` §4 | #328 stays open until it is the author's (that record's §9) |
| 3-D3 | Confirm the Orion formal name so the field can be created | §4 D3 | Not blocking; a `null`-with-a-reason waiting |
| 4a | Is `local_slice.py` a parallel engine the crossover keeps (labelled per field) or is it migrated onto `core.py`? | #322/#323/#324; VISION.md §7b, §12 Step B | It is **already consumed** (measured), so the question is about the next consumer, not the current one |
| 4b | Do `Party.treasury/legitimacy/network/technology` and `Relationship.trust` stay integer stocks, or become structural state? | `NOOPUNK_GLOBAL.md` §M1.5, §7, §8.4; `V1_DISCOURSE_AND_NETWORK.md` §4 | **Rules change** — needs its own approval; `RULEBOOK.md` says NO RULES APPROVED |
| 5 | Which module owns a "relationship" record, under which name | #346; #389 | **No** — nothing depends on it; the lowest-cost of the five |

**What this document deliberately does not do.**

- It **does not take any of the nine decisions above**, and it makes no recommendation about any of
  them. Where a reading is offered, it is labelled *interpretation* and the alternatives are left
  standing.
- It **edits no file** and touches none of the five subjects. In particular it does not rename,
  merge, split, delete or relabel any type, and it does not fill the `official_name` field or the
  roster count.
- It **adds no field, no record, no third spelling, no mechanic, no number, no name and no date**.
- It **closes no issue** and changes no issue state. Every fork above is left exactly as open as it
  was found, and this record's existence is not evidence that any of them is decided.
- It **adds no test, guard, schema lock or CI step**, and it does not restate the tests policy in a
  form that could be turned into one ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

---

## 7. Method, evidence and verification

**Base revision.** This record was written against `origin/main` = `d8763b2` and re-verified at
`9111ad5` (all `git fetch origin --prune` on 2026-10-13). The cited source modules are unchanged
across `d8763b2`, `5341b5c` and `9111ad5`, so every line number above holds at `9111ad5`. The earlier
records' own bases are older: `ISSUE_328_ROSTER_RECONCILIATION.md` was written at `3d17524`, still an
ancestor of `origin/main` (verified with `git merge-base --is-ancestor`).

**Suites at `9111ad5`, both green:**

```text
python -m unittest discover -s strategy_game/tests -p "test_*.py"
Ran 1059 tests in 2.478s
OK

python -m unittest discover -s tests -p "test_*.py"
Ran 509 tests in 17.944s
OK
```

**A transient red episode, recorded because this document's base moved through it.** At `5341b5c`
(between the two revisions above) the same command reported `Ran 1057 tests — FAILED (failures=3)`:
`test_council.PortfolioTests::test_the_worked_turn_pursues_four_of_six_and_names_the_two_it_leaves`,
and `test_rpg_boundary.LayerIndependenceTests::test_no_module_imports_a_strategy_engine` plus
`::test_the_only_shared_vocabulary_is_the_declared_type` (the last two on
`strategy_game/rpg/boundary.py` importing `core`). The root suite was green throughout (509 OK). A
sibling session's PR fixed it and `origin/main` at `9111ad5` is green; **none of the five subjects of
this document was involved, and this document changed no file that failed**. It is recorded here only
so that the counts above are auditable against the revision that produced them.

Per-module counts quoted in the text (measured at `9111ad5`): `test_session` 42,
`test_agent_boundary` 43, `test_political_contracts` 27, `test_political_layer` 40,
`test_local_slice` 4, `test_render_text` 14, `test_character_cards` 62, `test_relationships` 32,
`test_scenario_schema` 11.

**Probes.** The §1.2 and §4.1 outputs were produced by two read-only scripts that import the
packages and print. They write nothing, mutate no repository file, and are not part of this
repository — they exist to make the statements checkable, and any reader can reproduce them with
`python -c` against the same revision:

- Probe 1: field-set diffs for the two `Controller`/`MoveProposal` pairs; the three cross-type
  attempts (A, B, C); `core.Leader` vs `local_slice.Leader` field sets; the `Party` and
  `Relationship` integer field types; the `state_from_local_slice()` loss test; the
  `strategy_game.__all__` / module-origin check.
- Probe 2: records a `session.MoveProposal` into `controllers.ProposalRecorder`, then reads back
  `to_dict()`, `replay()` and a `ProposalLog` JSON round-trip to show which declared content
  survives.

**Counts of the registers** were produced by parsing the artefacts
(`len(global_factions.json["factions"]) == 7`; four `- name:` entries in `un_parties.yaml`), not by
reading a document that states them.

**The one thing that is *not* measured here.** How many other rosters, vocabularies or parallel state
engines exist beyond the five above. `NOOPUNK_GLOBAL.md` §6B.3 says of its own sweep *"I swept only
these three records, so there may be further rosters elsewhere"* (`:390`), and that caveat still
holds.

**No test covers this document.** It is Markdown; the two suites above are unchanged by it and would
report identical counts whether it exists or not ([#271](https://github.com/TomiToivio/NooPunk/issues/271),
`AGENTS.md` automated-tests policy). It is reviewed editorially and by playtesting.

---

*Cross-refs: [`AGENTS.md`](../../AGENTS.md) §0/#306 (two games; legacy canon untouched), §2 (one layer
at a time), §6 (20XX), §13 (a rules difference is a defect; consume a shared specification) ·
[#271](https://github.com/TomiToivio/NooPunk/issues/271) (no tests over prose) ·
[VISION.md](VISION.md) §12 Step B, §14 row B, §7b ·
[`ISSUE_328_ROSTER_RECONCILIATION.md`](ISSUE_328_ROSTER_RECONCILIATION.md) ·
[`ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md`](ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md) ·
[`V1_DISCOURSE_AND_NETWORK.md`](V1_DISCOURSE_AND_NETWORK.md) ·
[`ISSUE_304_GM_TURNS_AND_CONTROLLERS.md`](ISSUE_304_GM_TURNS_AND_CONTROLLERS.md) ·
[`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §6B.3, §7, §8.4, M1 ·
[`../../strategy_game/docs/AGENT_BOUNDARY.md`](../../strategy_game/docs/AGENT_BOUNDARY.md) ·
[`../../strategy_game/docs/LOCAL_SLICE_RULES_PROVISIONAL.md`](../../strategy_game/docs/LOCAL_SLICE_RULES_PROVISIONAL.md)*
