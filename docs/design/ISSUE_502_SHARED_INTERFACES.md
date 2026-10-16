# Issue #502 — the minimal shared interface: `WorldState`, `Faction`, `Leader`, `Agent`, `Case`, `MissionOutcome`

**Status: SPECIFICATION FOR REVIEW.** The author owns acceptance. This record decides nothing by
itself; it is the author-specified interface *written down*, with an audit of what already exists in
the repository and what is new.

**What this file is.** Issue [#502](https://github.com/TomiToivio/NooPunk/issues/502) asks for one
thing from engineering first: *"Define a minimal shared `WorldState`, `Faction`, `Leader`, `Agent`,
`Case`, `MissionOutcome` interface."* This record supplies it — six records, what each is for, its
minimal fields, its versioning and extension points, and **which parts exist in code on
`origin/main` today and which are new**. Its purpose is #502's first architecture rule: **one world
model, three views** — characters and actions (RPG), organization and missions (X-COM scale),
factions / institutions / networks (Terra Invicta scale) — instead of three parallel models that
must later be reconciled. The roadmap that carries the rule is
[`VISION.md`](VISION.md) §17; this file is the specification it links to.

**What this file is not.**

- It is **not an approval.** It selects no mechanic, number, magnitude, cost, probability, cadence,
  threshold, action set, skill roster, faction taxonomy, mission list, case content or canonical
  fact. Where a mechanic would be needed, the field is **named, marked, and left empty** with
  *awaiting author decision* — the placeholder behaviour `AGENTS.md` §1 requires.
- It is **not a schema lock, and not a test contract.** No code changes in the PR that lands this
  file. Nothing here may be asserted by an automated test or CI gate: per the repository's
  automated-tests policy, tests cover **executable code only**, and canon, lore, scenario prose and
  design documents are reviewed editorially and through tabletop playtesting. If a future
  implementation adds these records, the tests are written against the **implementation's
  behaviour**, never against this document's wording.
- It is **not a second RPG engine**, and not a rewrite of the rules. The existing homes keep their
  work: #482's two-layer mechanics ([`rpg/`](../strategy_game/rpg/),
  [`strategy_game/RULEBOOK.md`](../strategy_game/RULEBOOK.md)), #389's approved RPG foundation, and
  #461's five-seat structure. #502's rule 6 is binding here: **reuse and track dependencies instead
  of creating competing engines.**
- It does **not** unify the two `WorldState` classes in this repository. #502's "one world model"
  governs the **crossover game** (`strategy_game/`). The legacy engine's `WorldState`
  (`src/simulation/world_state.py`, the event-reduction state of one LaclauGPT-informed simulation
  run) belongs to the **legacy** RPG engine and stays where it is — `AGENTS.md` §0's two-games rule.
- It contains **no code**. The interface is described as fields and contracts; writing Python is a
  separate, scoped piece of work.

---

## 1. The audit: what exists today, and what is new

Measured by reading `origin/main` at the time of writing, not from memory.

| Record | In code today? | Where it lives today | Fields as they exist today |
|---|---|---|---|
| `WorldState` | **Yes** (and again, separately, on the legacy side) | `strategy_game/core.py` — `class WorldState`; the legacy engine has its own, unrelated `class WorldState` in `src/simulation/world_state.py` | `schema_version` (default `"scaffold-1"`), `leaders`, `factions`, `assets`, `locations`, `edges`, `events`, plus the Layer II political collections `demands`, `signifiers`, `formations`, `frontiers`; explicit `to_dict`, `to_json`, `from_json` |
| `Faction` | **Yes** | `strategy_game/core.py` — `class Faction`; the authored roster record is `GlobalFaction` in `strategy_game/factions.py`, and `faction_cards.py` / `faction_creation.py` carry `FactionCard` and `FactionDraft` | `identifier`, `name`, `leader_id`, `asset_ids` |
| `Leader` | **Yes — twice, on two different layers** | `strategy_game/core.py` — `class Leader`; `strategy_game/local_slice.py` — a second, provisional `class Leader`; `council.py` carries `CouncilLeader` and `leaders.py` carries `Person` + `LeaderRoster` | `core`: `identifier`, `name`, `attributes`, `personality_tags`. `local_slice`: `id`, `name`, `faction`, `location`, `portfolio`, `skill`, `status`, `traits` |
| `Agent` | **Yes — once, and not on `WorldState`** | `strategy_game/global_slice.py` — `class Agent` (the #338 experimental slice); the roster **structure** is `rpg/roster.py` — `Seat`, `SeatKind.LEADER` / `SeatKind.AGENT`, `AgentSeat`, one leader + four agents, one action per character per turn | `id`, `name`, `skills` |
| `Case` | **No — new** | nothing in the repository defines a `Case` record | the nearest existing vocabulary is `MissionDeclaration` (`council.py`, which states *"a declaration is not an outcome: nothing here resolves or writes one"*), `Mission` (`local_slice.py`), and the proposed mission kinds in `strategy_game/data/strategic_skills.json` (`status: PROPOSAL`) |
| `MissionOutcome` | **No — new** | nothing in the repository defines a `MissionOutcome` record | the nearest existing vocabulary is `TurnOutcome` (`turn.py`), `Resolution` + `Outcome` (`rpg/fate.py`), `ResolvedMove` (`session.py`), `EventEffect` (`council.py`), and the deliberately *uninterpreted* `MissionDeclaration.outcome` string field |

Three consequences, and all three shape §3:

1. **`WorldState`, `Faction`, `Leader` and `Agent` already exist.** The specification therefore
   **adopts and extends** the existing records. A second `Faction` beside `core.Faction`, or a
   second leader record beside `core.Leader`, is exactly the competing engine #502's rule 6
   forbids. Where a provisional duplicate exists (`local_slice.Leader`, `global_slice.Agent`), this
   record names it as a **slice**, not as a rival definition.
2. **`Case` and `MissionOutcome` are the only genuinely new records.** Their absence is the reason
   the RPG layer cannot today report a durable result: `LeaderRpgLayer.describe` in
   `rpg/boundary.py` joins nothing to `WorldState` *on purpose* (the join is the unapproved Gate D
   decision), and `MissionDeclaration.outcome` is documented as staying empty. These two names are
   what #502 supplies to fill that gap.
3. **The existing `WorldState` is load-bearing.** It is referenced under `strategy_game/` in 43
   files — 29 Python, 12 Markdown, plus the package entry points — and the character, faction,
   political and tabletop work all read or write it. The interface starts there, from
   `docs/design/VISION.md` §12's own baseline (`core.py`, `ports.py`, `provenance.py`, `view.py`),
   and extends serialization only as needed (VISION §13).

---

## 2. The five rules these interfaces follow

1. **Minimal, not complete.** Only the fields the first playable investigation must read or write.
   A field that is not needed yet is an **empty extension point**, not a filled one (`AGENTS.md`
   §1 and §10).
2. **One record, three views.** Records are written by the resolver and read by projections. A view
   does not recalculate or award a consequence (VISION §13).
3. **References, not ownership.** Records name each other by stable identifier and never embed one
   another. That keeps snapshots diffable, save files small, and the three views independently
   projectable.
4. **Provenance stays separate from description.** Anything that records *what happened* carries a
   `Provenance` (`provenance.py`, `ProvenanceKind`), so authored, evidenced, generated and simulated
   material never read alike — the rule #282 already implements for `Event`.
5. **No numbers in this specification.** Where a mechanic would need a magnitude, the field is
   named, its type is left open, and it is marked **awaiting author decision**. Naming a field is
   not approving its mechanic.

---

## 3. The six interfaces

### 3.1 `WorldState` — the one durable snapshot

**Purpose.** The single versioned snapshot of one campaign's world, from which all three views
project: the character/action view (RPG), the organization/mission view (X-COM scale), and the
faction/institution/network view (Terra Invicta scale). A save file *is* a serialized `WorldState`.

**Exists today** — `strategy_game/core.py` (`class WorldState`). It already carries a
`schema_version` string, the collections `leaders`, `factions`, `assets`, `locations`, `edges`,
`events`, and the Layer II political vocabulary `demands`, `signifiers`, `formations`, `frontiers`;
`from_json` reads each collection with `.get(..., [])`, so a snapshot written before a collection
existed still loads.

**Minimal fields.**

| Field | Status | Note |
|---|---|---|
| `schema_version: str` | exists | The snapshot's own version. See §4. |
| `player_leader_id: str \| None` | **new** | The structural expression of #502's premise: **the player character is the faction leader from day one.** Set from the first turn, and it must resolve to a `Leader` that is also some `Faction.leader_id` (§3.2). |
| `leaders: list[Leader]` | exists | §3.3 |
| `factions: list[Faction]` | exists | §3.2 |
| `agents: list[Agent]` | **new collection** | §3.4. The `Agent` record exists in code, but `core.WorldState` does not carry it today. One home for agents — not a second roster beside `rpg/roster.py`'s seats. |
| `cases: list[Case]` | **new collection** | §3.5 |
| `mission_outcomes: list[MissionOutcome]` | **new collection** | §3.6. Append-only, like `events`. |
| `events: list[Event]` | exists | The recorded history of what happened, each with provenance. Unchanged. |
| `assets`, `locations`, `edges` | exist | Unchanged. Political relations remain ordinary `NetworkEdge` entries carrying a relation-layer label, so the political field stays one multiplex graph. |
| `demands`, `signifiers`, `formations`, `frontiers` | exist | Unchanged (Layer II vocabulary; no rules attached). |

**Extension points.** Every new collection defaults to **empty**, so a campaign with no cases and no
outcomes is still a valid `WorldState`. A later phase adds its own collection or its own optional
field rather than widening one of these six records. One caution worth stating, because it is
already true in the code: `strategy_game/view.py`'s view has a **pinned key set** asserted by
`strategy_game/tests/test_agent_boundary.py` (`schema_version`, `locations`, `network_nodes`,
`network_edges`, `assets`). Adding a field to `WorldState` must **not** silently appear in that
projection; widening a view is its own deliberate decision.

**Versioning.** `schema_version` is the snapshot's shape version, distinct from the rules version it
was played under. Growth is **additive** (§4).

### 3.2 `Faction` — the organized actor the player leads

**Purpose.** One faction: the player's own — the one the player character **leads** — or a rival. It
is the record the RPG's decisions land on and the record the organizational board and the political
field later read.

**Exists today** — `strategy_game/core.py` (`class Faction`: `identifier`, `name`, `leader_id`,
`asset_ids`). The authored, read-only roster record is `GlobalFaction` in `factions.py`
(`identifier`, `label`, `kind`, `subtitle`, `axis_defaults`, `stances`, `signifiers`, `sources`,
`provenance`, `detail`). The two should share identifiers: the authored roster and the running
snapshot must name the same factions.

**Minimal fields.** #502 states the minimal faction state Phase 1 needs under the hood explicitly:
*"leader, members, objectives, relationships, intelligence, resources, reputation"*. The record
below is that list, mapped onto what the code already has.

| Field | Status | Note |
|---|---|---|
| `identifier: str` | exists | Stable id; shared with the authored roster. |
| `name: str` | exists | Display label. |
| `leader_id: str \| None` | exists | **This is where #502's premise lands structurally.** For the faction the player leads, `leader_id` is never empty, and it must equal `WorldState.player_leader_id`. For a rival faction in Phase 1 it may be empty or name an authored leader. |
| `member_ids: list[str]` | **new** | The faction's "members" — its **agents** (§3.4) and any other named people. `core.Faction` carries assets today, not people. |
| `objective_ids: list[str]` | **new** | "Objectives", by reference. #502 specifies no objective record, so the ids are the extension point and the record behind them is undecided — **awaiting author decision**. |
| `relationship_ids: list[str]` | **new, as references only** | "Relationships". The relationship records themselves already exist in one shared collection (`strategy_game/relationships.py`: `RelationshipEdge`, `RelationshipSet`; and the read-only roster edges in `leaders.py`). **Recommendation, not a decision:** keep relationships in that one shared collection and let a faction name them, rather than growing a second, per-faction relationship store. |
| `intelligence`, `resources`, `reputation` | **new; named, unquantified** | #502 lists all three as Phase 1 faction state. **Whether each is a number, an open vocabulary, or a collection is an author decision**, and this specification deliberately fixes none of them. The interface's only requirement is that a `MissionOutcome` can durably point at whatever they become. |

**Extension points.** A `detail: dict[str, Any]` field retained verbatim, following
`GlobalFaction`'s existing pattern, so authored faction material the typed fields do not cover is
never dropped. A `provenance: Provenance` field, following `Event`'s and `GlobalFaction`'s existing
pattern, so an authored faction is never confused with a generated one.

**Versioning.** Additive (§4).

### 3.3 `Leader` — the player character and every other named leader

**Purpose.** The named person who leads a faction. #502's premise makes this record the player
character: **the faction leader from day one**, who can act in RPG scenes and direct the faction's
agents.

**Exists today, twice, on two layers.**

- `strategy_game/core.py` — `class Leader`: `identifier`, `name`, `attributes`, `personality_tags`.
  This is the identity-and-link record the snapshot carries.
- `strategy_game/local_slice.py` — a provisional `class Leader`: `id`, `name`, `faction`,
  `location`, `portfolio`, `skill`, `status`, `traits`. This belongs to the #322/#323/#324 playtest
  slice, and its numbers are slice scaffolding, not approved rules.
- Elsewhere: `council.py` carries `CouncilLeader` (id, name, portfolio, status, location, detail),
  `leaders.py` carries `Person` + `LeaderRoster` + the twelve-seat roster for the Ukweli material,
  and the **approved Fate character sheet** lives in the RPG layer — `rpg/fate.py`'s `Character`,
  reached from outside through `rpg/boundary.py`'s `sheet()`.

**Minimal fields.** The design intent is that the snapshot's `Leader` is the **identity and link
record**, and the **sheet stays where it is** — in the RPG layer, behind the existing boundary — so
the approved #482 sheet is not duplicated into the strategy model.

| Field | Status | Note |
|---|---|---|
| `identifier: str` | exists | Stable id, shared with `Faction.leader_id` and with the RPG layer's character id. |
| `name: str` | exists | Display label. |
| `faction_id: str \| None` | **new on `core.Leader`** | Which faction this person leads or belongs to. The provisional `local_slice.Leader` already has the equivalent (`faction`). |
| `attributes: dict[str, Any]` | exists | Kept, and kept **empty by default**: the approved six individual skills and their allocation belong to the RPG layer's sheet, not here. |
| `personality_tags: list[str]` | exists | Kept as the existing free-tag field. |
| `sheet_ref` (or the sheet read through the boundary) | **new, by reference** | How the strategy model reaches the character sheet. The **existing** `rpg/boundary.py` — `LeaderRpgLayer.sheet(character_id)` — is the intended path; this specification does not authorise the join it currently refuses to perform. |

**Contract.** The record must not restate the character sheet. `rpg/boundary.py` deliberately joins
nothing to `WorldState` today, and defining *that join* is the "wire RPG decisions into durable
faction/world-state updates" task of #502 — a code change, made under the rules that govern it, not
by this document.

**Extension points.** `detail: dict[str, Any]` retained-verbatim, following `GlobalFaction`.

**Versioning.** Additive (§4).

### 3.4 `Agent` — a party member the faction has recruited or assigned

**Purpose.** A member of the party who is not the leader. #502 states it plainly: *"Other party
members are the faction's agents. The leader can participate in RPG scenes and direct agents"*, and
the party is *"a set of recruited or assigned agents"* with *"character sheets, relationships,
skills/TAGs, and distinct capabilities"*. An agent can be **directed by the leader** and can also
**act within a scene**.

**Exists today.**

- `strategy_game/global_slice.py` — `class Agent`: `id`, `name`, `skills` (frozen dataclass, the
  #338 experimental slice; its numbers are slice scaffolding).
- `strategy_game/rpg/roster.py` — the **structure**: five seats, `SeatKind.LEADER` and
  `SeatKind.AGENT`, `AgentSeat.LEADER` / `AGENT_1`…`AGENT_4`, one action per character per turn.
  #482/#461 state this structure and it is implemented; `rpg/roster.py` also states that a different
  leader/agent count is an author decision.

**Minimal fields.**

| Field | Status | Note |
|---|---|---|
| `identifier: str` | exists (`global_slice.Agent.id`) | Stable id; shared with `Faction.member_ids` and with the RPG layer's character id. |
| `name: str` | exists | Display label. |
| `faction_id: str \| None` | **new** | Which faction holds this agent. |
| `seat_id: str \| None` | **new, optional** | The seat this agent occupies, when it occupies one — the link to `rpg/roster.py`'s five-seat structure (`leader`, `agent_1`…`agent_4`). Optional so an agent without a seat is representable without inventing a sixth seat. |
| `sheet_ref` (or the sheet read through the boundary) | **new, by reference** | As with `Leader`: the sheet is the RPG layer's, reached through the existing boundary. |
| `status: str` | **new, open vocabulary — awaiting author decision** | Which states an agent can be in (available, on a case, unavailable, otherwise) is a mechanic this specification does not define. The field exists so a case can mark an agent as committed without a second flag elsewhere. |

**Contract.** An `Agent` is never a second copy of a `Leader`'s sheet, and never a `Faction`. The
leader is *not* an agent record with a flag: the leader is a `Leader` (§3.3) whose identity
`WorldState.player_leader_id` names.

**Extension points.** `detail: dict[str, Any]` retained-verbatim.

**Versioning.** Additive (§4).

### 3.5 `Case` — one investigation

**Purpose.** The RPG-scale unit of work: one investigation the faction pursues. In **Phase 1** a
case is played through scenes with the leader and the agents; in **Phase 2** cases *"become missions
on an organizational board"*, which is why the case is the container and the mission is one attempt
at it — a case can outlive a single mission. It is also the natural home of a `Location`
(`core.Location`, existing) and of the "case file" the provenance kind `EVIDENCE` already refers to
in `Event`.

**New.** No `Case` record exists in the repository.

**Minimal fields.**

| Field | Status | Note |
|---|---|---|
| `identifier: str` | **new** | Stable id. |
| `label: str` | **new** | Short display title. |
| `summary: str` | **new**, default empty | Author- or scenario-supplied text. A *field* for the briefing is interface; the briefing's content is scenario authoring, and no content is supplied here. |
| `status: str` | **new, open vocabulary — awaiting author decision** | Which states a case moves through (e.g. open / active / closed) is a mechanic, and it is the author's to rule on. The interface requires only that the field exists and is an open vocabulary rather than an enum invented here. |
| `location_id: str \| None` | **new** | Reference to an existing `core.Location`. |
| `lead_agent_id: str \| None`, `assigned_agent_ids: list[str]` | **new** | Who is on the case. This is #502's "party of agents" made concrete: the leader may lead a case directly, or an agent may. |
| `provenance: Provenance` | **new on this record** | Following `Event`. An authored case and a seeded one must not read alike. |

**Contract.** A `Case` has **no** progress track, difficulty, clock or score. All of those are
unapproved mechanics. The case's *result* is not a field on the case either — it is a
`MissionOutcome` (§3.6), which is exactly what `MissionDeclaration`'s comment means by *"a
declaration is not an outcome"*.

**Extension points.** `detail: dict[str, Any]` retained-verbatim, following `GlobalFaction`'s
pattern. A future Phase 2 may add `mission_ids` or `clock_ids`; neither is defined here.

**Versioning.** Additive (§4).

### 3.6 `MissionOutcome` — the durable result of one played mission

**Purpose.** The record that carries a **play decision into faction and world state** — #502:
*"Outcomes update the same world state that later strategy layers will use"*, and the engineering
task *"Wire RPG decisions into durable faction/world-state updates"*. It is the answer to the gap
`council.py` documents today: `MissionDeclaration` holds an `outcome: str` field that is explicitly
*"Uninterpreted. Nothing in this package produces an outcome, so it stays empty."*

**New.** No `MissionOutcome` record exists in the repository.

**Minimal fields.**

| Field | Status | Note |
|---|---|---|
| `identifier: str` | **new** | Stable id. |
| `case_id: str \| None` | **new** | The `Case` this result belongs to (§3.5). A case may have several outcomes over its life. |
| `declaration_id: str \| None` | **new** | The `MissionDeclaration` (`council.py`, existing) that was played, if one was declared. This is how *"a declaration is not an outcome"* stays true while the outcome still names what was attempted. |
| `actor_ids: list[str]` | **new** | Who acted — the leader and/or the agents (`Leader.identifier`, `Agent.identifier`). |
| `outcome: str` | **new, open vocabulary — awaiting author decision** | **No success/failure scale, no degree, no margin is defined here.** The RPG layer's existing `Outcome` enum (`rpg/fate.py`) resolves a *check*; a mission outcome is a different, larger thing and its vocabulary is the author's ruling. |
| `event_ids: list[str]` | **new** | The `Event` records (existing, with provenance) that the resolver wrote for this outcome. This is the append-only history a view projects and a replay re-reads. |
| `effects` | **new, deliberately empty — the extension point** | **What a mission may change** — an objective, an intelligence item, a resource, a reputation, a relationship — is precisely the mechanic this specification must not invent. When the author rules on it, the shape to reuse is **`council.py`'s existing `EventEffect`** (`target_kind`, `target`, …, documented as *"What one event option touches. The target is named; how far it moves is not approved."*), rather than a second effect vocabulary. Default empty. |
| `provenance: Provenance` | **new** | The outcome is a *resolved* record; `Provenance` keeps a resolved result distinguishable from an authored or simulated one. |

**Contract (the authority rule).** `MissionOutcome` is written by the **resolver only**. VISION §13's
controller table is explicit: *"Resolver — Apply approved rules and recorded randomness — Sole
writer of resolved gameplay state"*, and *"Views show its consequences; they do not independently
recalculate or award them."* Nothing in a controller, a view or a prompt writes this record.

**Extension points.** `effects` (above) is the named empty extension point; `detail: dict[str, Any]`
retained-verbatim follows `GlobalFaction`'s pattern.

**Versioning.** Additive; append-only in practice (§4).

---

## 4. Versioning, saves and extension points

**Two versions per snapshot, plus the recorded randomness.** A save file must carry:

1. **`WorldState.schema_version`** — the shape of the snapshot itself (`"scaffold-1"` today).
2. **the rules version** the campaign was played under — the rulebook and rule-data version, so a
   later reader can tell which rules produced a record.
3. **the recorded inputs and random outcomes**, not a seed alone. VISION §13 and §15 already state
   why: a seed cannot reproduce changed code or a changed model response, so a replay record
   identifies the initial snapshot, the rule and schema versions, the accepted inputs, the recorded
   randomness and the resulting events — and a replay must not call a model again.

**Additive growth is the rule.**

- A **new collection** defaults to empty and is read with `.get(name, [])`, so an older snapshot
  loads (`core.WorldState.from_json` already does this for every collection).
- A **new field** takes a default, so an older snapshot loads without it.
- A **rename, a retype or a semantic change** of an existing field is a **new `schema_version` plus a
  documented migration step**; it is never a silent reinterpretation of an existing key.
- A **view's key set is separate from the snapshot.** The pinned projection in `strategy_game/view.py`
  (asserted by `strategy_game/tests/test_agent_boundary.py`) must not widen by accident when a record
  gains a field.

**Extension points must be empty and named.** Per `AGENTS.md` §1 and §10, an undefined area is
represented by an **empty, named** extension point rather than a filled one: `effects` in
`MissionOutcome`, `detail` on each record, and the unquantified `intelligence` / `resources` /
`reputation` of `Faction`. Nothing here is a placeholder that may be "helpfully" completed.

**Provenance never collapses.** Authored, evidenced and simulated material stay distinguishable
(`provenance.py`). An `Event` with no provenance reads as unknown rather than as fact, and the same
default applies to the three new records.

**No automated gate on any of this.** This document, and the canon it describes, are reviewed
editorially and by playtesting. No unittest, snapshot, schema lock, `tools/` check, action or hook
may assert this file's wording or its field list.

---

## 5. What stays open — author decisions this specification deliberately does not make

Named so that a later implementer does not mistake an empty field for a settled one.

- **`Case.status` and `MissionOutcome.outcome` vocabularies.** Which states, and which results, exist.
- **Whether `intelligence`, `resources` and `reputation` are numbers, vocabularies or collections**,
  and what a faction's "objectives" are as records (`objective_ids`' targets).
- **What a mission may change** — the contents of `MissionOutcome.effects`, which is #502's
  *"durable faction and world-state updates"* and the substance of the whole wiring task.
- **Whether relationships are per-faction or one shared collection.** The recommendation in §3.2 is
  to keep one shared store; the decision is not made here.
- **The strategic agent skill roster and its mission kinds** — #482's open row, `status: PROPOSAL` in
  `strategy_game/data/strategic_skills.json` (see `docs/design/AUTHOR_DECISION_QUEUE.md`).
- **Mission difficulty, cost, cadence and effects** — the same queue's separate rows.
- **Whether `global_slice.Agent` and `local_slice.Leader` are superseded** by the records here, kept
  as slices, or kept as alternate views. This specification adopts their *names*, not their numbers,
  and does not delete them.
- **The record names themselves**, if the author prefers different ones.
- **Acceptance of this specification**, by an author ruling.

---

## 6. What this enables, in #502's own task order

Recorded so the sequence is legible; **none of it is authorised by this file**, and items 3–6 are
implementation work under their own scoped issues and rules.

1. **Audit** the existing character, faction, rules and mission code and issues (#482, #338) — §1
   above.
2. **Define** the minimal shared interface — this file, §3.
3. **Implement** a thin playable X-Files investigation with a **faction-leader** PC and a party of
   agents: a Phase 1 vertical slice on the existing `rpg/` work, with a `WorldState` that carries the
   three new collections of §3.1. Subject to `AGENTS.md` §2 (one layer at a time) and VISION §12.
4. **Wire** RPG decisions into durable faction and world-state updates: the join `rpg/boundary.py`
   currently and deliberately refuses to perform.
5. **Phase 2** mission board — only after the vertical slice of 3 and 4 works.
6. **Phase 3** abstract political simulation — only after small-scale strategy has a fun loop.

---

*This record implements nothing, approves nothing and invents no canon. It records the interface
#502 specifies, on the evidence of what already exists in `strategy_game/`, and leaves every
mechanic it touches to the author. Refs #502, #482, #338, #389, #461.*
