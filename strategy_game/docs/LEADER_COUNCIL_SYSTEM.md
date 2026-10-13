# NoöPunk Strategy Game — Layer I/III: four-leader council, missions and relationships

**Status: stage-A proposal for [#323](https://github.com/TomiToivio/NooPunk/issues/323) — NOT canon, NOT approved.** `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**. Every number below is **DRAFT**: a starting value for review and tabletop playtesting, not an implemented mechanic. Nothing here has been coded, executed or tested. Author gates A (leader RPG) and C (strategy) in [`docs/RULE_SYSTEM_RESEARCH.md`](RULE_SYSTEM_RESEARCH.md) must pass first.

This is the **written specification** the issue's stage A asks for. The playable prototype that already exists on `main` — [`local_slice.py`](../local_slice.py) with [`LOCAL_SLICE_RULES_PROVISIONAL.md`](LOCAL_SLICE_RULES_PROVISIONAL.md) and `tests/test_local_slice.py` — states its rules as "unapproved playtest assumptions"; this document is the reviewable specification those assumptions should be checked against, including the parts the prototype notes as still missing (character events, organisational transitions, richer rival AI).

Cross-links: [#322](https://github.com/TomiToivio/NooPunk/issues/322) (local city scale), [#309](https://github.com/TomiToivio/NooPunk/issues/309) (God's-eye RPG vision), [#282](https://github.com/TomiToivio/NooPunk/issues/282) (parent), [#295](https://github.com/TomiToivio/NooPunk/issues/295), [#296](https://github.com/TomiToivio/NooPunk/issues/296), [#324](https://github.com/TomiToivio/NooPunk/issues/324). Per AGENTS.md §1–2, anything the author has not specified stays a placeholder or `TODO: requires author specification`.

---

## 1. The central rule: one named leader per active move

**Every active faction move has exactly one named leader responsible for carrying it out.**

- Member count, volunteers, contacts, funds and equipment are **resources and reachable capacity**,
  never independent action slots; a faction has **four leaders** at MVP (DRAFT — fixed roster size), so
  at most **four leader-led active missions per turn** (DRAFT), fewer when a leader is unavailable.
- A mission with an empty `leader_id` is **invalid** and is rejected before resolution. No "faction
  action" or "background action" may be chosen without naming one leader.
- Members and resources **amplify** a leader-led mission (strength, reach, resilience) but never
  create an extra mission: ten thousand volunteers still give four missions, because the binding
  constraint is how many leaders can personally direct an effort in a turn.

A leader spends a turn on either **one active mission** or **hold/skip** — always available, and
meaningful: a resting leader recovers status (DRAFT). Stage B of #323 owns the exact reward.

## 2. Four portfolios (passive management, one per leader)

Each leader holds **one persistent management portfolio** — a CK-flavoured council office giving a *small,
bounded, visible passive effect* and **never** an active move. A manager is not a second action.

| # | Portfolio (DRAFT name) | Passive effect it improves (DRAFT) |
|---|---|---|
| 1 | **Politics & Diplomacy** | legitimacy, negotiation temperature, coalition posture |
| 2 | **Organisation & Networks** | network reach, cohesion, member mobilisation |
| 3 | **Operations & Resources** | resource income/maintenance, asset resilience |
| 4 | **Research & Intelligence** | technology adoption, intelligence quality, contacts |

**Bounded passive bonus rules (all DRAFT):**

- A portfolio grants at most **+1** on the small scales it touches; a faction's total passive bonus to any
  one quantity is capped at **+2** per turn.
- A passive is a **modifier on a later declaration**, never an autonomous event: it may not resolve a
  mission, recruit an NPC, reveal a secret or trigger a story by itself.
- It applies in the same turn the leader runs a mission, **unless** the leader's status suspends it (§4).
- A skill or tag already used on this turn's mission must not be counted again through the portfolio —
  **no double-counting** (a stage-C acceptance item). An **empty** portfolio grants no bonus and no
  penalty, and every contribution is visible in the God's-eye view.

**Reassignment is explicit and costly (DRAFT):** a leader may change portfolio (or drop it) only at the
assignment step; it consumes that turn (**no active mission**), and the new effect starts at the **start
of the next turn**. A leader holds **at most one** portfolio, the four posts are distinct, and every
reassignment is written to the turn log.

## 3. Missions, districts and movement

- **One primary active mission per leader per turn.** A leader cannot run two missions in a turn, and
  one mission cannot be run by two leaders.
- A mission needs a leader (`leader_id`, required), a valid target (NPC, asset, institution,
  demand/signifier, district) and any declared resources; missing one makes it illegal.
- **Districts:** the city has **5–8 generic districts or nearby locations** (DRAFT: default 6,
  scenario-configurable) — flat hand-authored places, not a hex or grid map.
- **Movement is deliberately minimal.** At most a simple **adjacency/travel modifier** (DRAFT: same
  district 0, adjacent district −1 to difficulty; a non-adjacent district may cost the turn in travel),
  read from a short authored adjacency list per district. **No pathfinding, no tactical navigation, no
  travel simulation, no terrain or supply model.**
- A leader is *present* in a district (DRAFT: a mission may target their own or an adjacent district);
  presence matters for targeting, and that is the whole spatial system. Every mission names its leader and
  location, so the log always answers *who did it, and where*.

## 4. Leader statuses and their consequences

Status is data set by events and outcomes, never invented narration. Consequences (all DRAFT):

| Status | Mission this turn? | Portfolio passive |
|---|---|---|
| `busy` | No (already committed) | still applies |
| `injured` | No | suspended; recovers after 1–2 turns without a mission |
| `unavailable` | No | suspended |
| `compromised` | Yes, with exposure risk | halved (rounded down) |
| `exhausted` | No | still applies |
| `absent` | No | none |

An unavailable leader never silently trades down into a "lesser" action: the slot is simply unused and the
faction runs fewer missions. Recovery timing, exposure risk and halving are `TODO: requires author
specification`; the table records only the *shape* of the consequence.

**The shape is now enforced, and the specifics are still reported.** Issue #323's acceptance criterion 2
says an unavailable leader cannot execute a mission, so `structural_problems` in `council.py` **refuses** a
mission led by a status whose row says `No`, rather than reporting it. This enforces the *shape* this table
records; it does not author the TODOs. Timing (1–2 turns), exposure risk and halving stay reported with the
row cited, and `enforced` stays `false` for the table as a whole in `data/council.json`, which carries
`mission_column_enforced: true` for the column that the criterion names.

## 5. Relationships: sparse, pairwise, opinion and trust

Relationships exist only between a faction's four leaders and a **limited cast of important local NPCs**
(rival leaders, administrators, journalists, scientists, institutional contacts); ordinary residents are
never simulated.

- **Sparse, not dense.** A record exists only where one is authored or scenario-set; two characters with
  no record are unmodelled, not neutral-zero edges in a complete graph.
- **Pairwise opinion/trust** on small integer scales: `opinion` **−3…+3** (DRAFT, default 0) and
  `trust` **0…3** (DRAFT, default 0 = none). They are separate: you can be trusted by someone who
  dislikes you.
- **1–3 evocative tags** per relationship from an open, extensible list (DRAFT): `friend`, `rival`,
  `family`, `mentor`, `indebted`, `suspicious`, `former ally`.
- **Loyalty to a faction is kept separate from affection for a person.** `loyalty` sits on the leader
  (faction-facing), `opinion` on the relationship (person-facing); a leader may privately like a rival's
  leader while staying loyal to their own faction, and the two are never collapsed into one scalar.
- Relationships **modify** recruitment, negotiation, cooperation, cohesion, intelligence sharing,
  defection and rivals' responses (DRAFT mapping is stage D): modifiers and thresholds only, never an
  override of the step-5 resolution.
- **At most one consequential character event per faction per turn (DRAFT)**, none when no trigger fires
  — no procedural filler. Drama changes strategy state, and strategy changes relationships, in both
  directions.

## 6. Turn order

A turn is an **abstract political interval** (DRAFT: weeks to a month; the author picks the unit, not
daily micro-orders).

1. **External event & conditions** — apply the global paradigm event when due; update districts.
2. **Portfolios & maintenance** — bounded portfolio bonuses (§2) and routine maintenance/income.
3. **Situation view** — districts, leader statuses, relationships and the legal mission menu.
4. **Mission assignment** — up to **one mission per available leader** (max four); reassignments declared here.
5. **Seeded resolution** — all factions in a **deterministic, seeded** order (DRAFT: fixed seeded shuffle
   or declared tiebreak, so a rerun with the same seed is identical). Inputs: leader skills/tags,
   leader–target relationship, resources, district conditions, adjacency modifier.
6. **Character event** — at most one important character/RPG event per faction, if a trigger fires.
7. **State update & log** — support, discourse/network power, institutions, resources and relationships,
   written to a readable turn log.

## 7. Minimum data model (extends the existing containers)

These **extend** (never replace) the frozen containers in [`../core.py`](../core.py), in the same
dataclass, snake_case, `identifier`-keyed style. Adding any field needs author approval.

- **`Leader`** (existing: `identifier`, `name`, `attributes`, `personality_tags`) + DRAFT:
  `faction_id`, `location_id`, `status`, `active_mission_id: str | None` (at most one), `portfolio`,
  `loyalty`, `goals`, `conflicts`. Traits reuse `personality_tags`; **no oversized skill taxonomy is
  invented** and `attributes` stays author-defined and uninterpreted.
- **`Faction`** (existing: `identifier`, `name`, `leader_id`, `asset_ids`) + DRAFT: `leader_ids` (exactly
  four at MVP), `resources`, `support`, `organization`, `legitimacy`, `network_influence`,
  `ideological_claims`, `organizational_tags`.
- **`Relationship`** (new, sparse): `character_a_id`, `character_b_id`, `opinion`, `trust`,
  `tags: list[str]` (≤3), optional `obligation`.
- **`Mission`** (new): `identifier`, `leader_id` (**required, non-null**), `type`, `target_id`,
  `location_id`, `allocated_resource_ids`, `difficulty`, `outcome`, `turn`.
- **`Event`** (existing: `identifier`, `description`, `provenance`) + DRAFT: `trigger`,
  `participant_ids`, `choice_options`, `state_effects`, `narrative_text`. `provenance` stays and defaults
  to `UNKNOWN`: a simulated event is never silently promoted to evidence.

NPCs outside the roster may appear in relationships and events but gain **no** faction-mission slot.

## 8. Worked example turn (illustrative — not canon)

*Names and districts below are invented for this example only: placeholders, not authored lore, and no
faction from `data/global_factions.json` is used. Faction: **Harbour Civic Union** (illustrative).*

| Leader | Portfolio | District | Mission | Target |
|---|---|---|---|---|
| Mara Oduya | politics_diplomacy | Civic Centre | *Negotiate* | the Mayor's office |
| Tomas Reyes | organisation_networks | Outer Settlement | *Organise* | volunteers |
| Ilya Petrov | operations_resources | Harbour Works | *Acquire* | a released AI tool |
| Nadia Halim | research_intelligence | Hill Quarter | *Investigate* | a rival contact |

- **Steps 1–2:** no external event is due; each portfolio contributes its bounded DRAFT passive (+1,
  capped +2 faction-wide). **Step 3:** the faction's 40,000 members, funds and equipment show **as
  capacity and reach**, not orders. **Step 4:** all four leaders are available, so four missions are
  declared, each on **exactly one** leader in that leader's own district; no reassignment is used.
- **Step 5:** the seeded order resolves each mission on the leader's `attributes`/`personality_tags`, the
  leader–target relationship (`opinion`, `trust`, tags), resources and district conditions. Mara's
  *Negotiate* gains from a `mentor` tag and +2 opinion toward the Mayor; Ilya's *Acquire* succeeds but
  leaves him `busy`.
- **Steps 6–7:** one character event fires — Nadia finds her target `indebted` to Mara, creating a
  `rival`-tinged choice, and no second event fires — then state and relationships update; the log shows
  four missions, each with a named leader.

**No leaderless action occurs.** The Union's thousands of supporters made each mission stronger; they
produced no fifth mission, because no fifth leader exists to lead one.

## 9. Rival AI obeys the same constraints

NPC factions are **not** special-cased: every rival also has exactly **four** leaders and at most **one
mission each per turn**; rivals cannot issue leaderless actions, bank unused missions or gain free
actions from members or resources; their portfolios use the same bounded bonuses and reassignment cost,
and their choices go through the same seeded resolution and relationship/event rules, so a rival's
failure is explainable from the same log. An AI decision procedure (a DRAFT deterministic priority list,
or the same seeded resolution) never bypasses the slot limit.

## 10. Non-goals

- No separate CK3 court simulator, and no global character network.
- No tactical combat, hex map, pathfinding, terrain or logistics simulation.
- No procedural biography, family tree or large personality system; members stay abstract.
- No full Terra Invicta council mechanics (no 4→6 growth, no space layer, no real-time resolution).
- No new lore, factions or metaphysics; the §8 names are placeholders. No implementation or tests.
- No LLM requirement; the game must run deterministically on the Python standard library.

## 11. Inspirations cited, and what is deliberately not copied

- **Terra Invicta councillors** — a faction's handful of named operatives each take one mission per
  assignment phase, resolved with success rolls:
  <https://wiki.hoodedhorse.com/Terra_Invicta/Councilors>. *Not copied:* the four-to-six council
  expansion, mission list, success-roll maths, region/nation/hab targets, real-time resolution or space
  layer, or any licensed rules.
- **Crusader Kings III council and relationships** — council offices, councillor tasks and
  character-driven relationships and dilemmas: <https://ck3.paradoxwikis.com/Council>;
  see also <https://ck3.paradoxwikis.com/Game_rules>. *Not copied:* the feudal, dynastic
  and vassal model, the opinion/stress/secrets systems, event scripting, the map, the council-task and
  power-sharing rules, or any licensed text.
