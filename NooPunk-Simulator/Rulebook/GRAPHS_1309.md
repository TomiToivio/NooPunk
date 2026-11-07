# The three Simulator graph views (#1309)

> **Status: implemented and tested, small by design.** `src/social_sim/graphs.py` holds the models; the fixtures are in
> [`../Graphs/fixtures/`](../Graphs/fixtures/); the rules are summarised here and synchronized with the code.
>
> **`../Paper/` is Tomi's and read-only for agents.** This page *summarises* what the drafts say and implements only what
> they state. Where an implementation had to choose, the choice is marked **[PROPOSED]** and flagged, never written back
> into Paper.

## 1. What the three views are, and what they are not

| view | what it is | what it must never become |
|---|---|---|
| **Social** (`noopunk.simulator.social` v1) | the base: people, organizations, factions and institutions as actors, with typed ties and the author's −4…+4 value | an inference engine that creates a tie because two actors mention the same thing |
| **Ideology** (`noopunk.simulator.ideology` v1) | a **projection** over the same actor ids: coded actor–concept–position statements with their evidence | a fifth *RPG* graph family; `docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md` still lists four, and that is not changed here |
| **Physical** (`noopunk.simulator.physical` v1) | the Helsinki city graph: locations as nodes, routes as edges, three node kinds | a map of Helsinki, or an excuse to invent coordinates |

All three serialize as plain JSON with `format` and `version`, and a `World` document wraps them
(`noopunk.simulator.world` v1) so one file can be inspected, diffed and replayed.

## 2. Social: the author's semantics, enforced

From `Paper/SOCIAL_GRAPH.md`:

* a **node** is a social entity with identity and agency — a person, an organization, a faction, an institution; not a
  loose crowd. A node carries a name, a type and an id built from them (`person_mars_eldrich`).
* an **edge** is a relationship with a value from **−4** (hatred) to **+4** (friendship, love, alliance).
* a **bidirectional** edge means **both ends agree** about the relationship; a **unidirectional** edge is one actor's
  opinion, which the target may not share or may not know.

The code enforces each of those:

| rule | enforcement |
|---|---|
| value in −4…+4 | `SocialTie.__post_init__` refuses anything outside |
| mutual means mutual | a tie marked `reciprocal` **must** have an exact mirror (same value); a tie *not* marked so **must not** |
| no self-ties, no dangling ends | refused at construction |
| identity and agency | the actor kinds are closed; a "loose group" is not a node kind |
| tags travel with the record | `tags` on both nodes and ties, serialized |

**Reading helpers:** `mutual()` returns each agreed tie once, `one_sided()` returns opinions, `degree()` counts distinct
neighbours in either direction. These are descriptive SNA basics, not a claim about influence.

## 3. Ideology: a projection, with the DNA bridge

A `Stance` is one coded statement: actor, concept, position (`support`, `oppose`, `neutral`, `mixed`, `unknown`), the
**statement id** it came from, an optional evidence id, a review status and provenance. The bridge to Discourse Network
Analysis is the shared actor id: the same `person_mars_eldrich` appears in the social node and in the stance, so
projections over actor–concept–position statements are joins, not mappings.

| operation | meaning, and its limit |
|---|---|
| `table()` | actor → concept → position; a later statement for the same pair replaces the earlier |
| `agreement(a, b)` | share of **shared, coded** concepts with the same position. `unknown` is absence, not moderation, and a pair with no shared coded concept **raises** instead of scoring 0 |
| `conflicts(threshold)` | actor pairs on opposite sides of at least *n* coded concepts |

**What this never does:** it does not create a social tie, does not convert agreement into friendship or membership, and
does not claim that co-mention of a concept is an articulation. A test asserts the social tie count is unchanged after
every projection is computed.

## 4. Physical: the city graph, without invented geography

From `Paper/PHYSICAL_GRAPH.md`:

* **City Graph** — locations as nodes, traffic routes as edges. Three node kinds: **passive** (travel only), **active**
  (activities available, no sub-graph), **graph** (entering it opens another Physical Graph, i.e. a Location Graph of
  rooms and doors).
* node fields: name, id (`location_europol_field_office`), address, lat/lon.

| rule | enforcement |
|---|---|
| three node kinds only | `PLACE_KINDS` is closed |
| a `graph` node must name what it opens | `graph_ref` is required for that kind |
| coordinates are optional | `coordinates` may be `None`, and the fixture leaves all of them unset rather than inventing a position |
| routes join known places, no self-loops | refused at construction |
| one-way versus two-way | `directed` is explicit, and `reachable_from()` respects it; `traversable=False` removes an edge without deleting the place |

**Nested Location Graphs** are represented by the `graph_ref` contract only. The rooms-and-doors level is **not**
implemented — the issue lists it as optional later work, and inventing a floor plan would be pseudo-canon.

## 5. Identifiers: two conventions, no silent rewrite

Paper drafts use underscores (`person_mars_eldrich`, `location_europol_field_office`); the shared RPG contract uses
dotted ids (`social.…`, `loc.…`). Both load. `shared_id(token, kind=…)` maps one to the other and refuses a bare token it
cannot classify.

**[PROPOSED] — open decision for Tomi:** which convention is canonical. Until it is chosen, the fixtures keep the
Paper convention, the mapping is explicit, and no test asserts that one is "right".

## 6. What is implemented, and what is deliberately not

| item | state |
|---|---|
| social graph with mutual/one-sided ties, tags, serialization | **implemented**, 29 tests |
| ideology projection with the DNA bridge and honest `unknown` handling | **implemented** |
| physical city graph with three node kinds and route semantics | **implemented** (city level) |
| one world document, stable ids, headless round trip | **implemented** |
| faction mechanics, ideological transition rules | **not implemented** — the issue defers them until the social foundation is tested |
| Streamlit or any UI | **not implemented**, deliberately |
| nested Location Graphs (rooms, doors) | **not implemented**; contract only |
| migration of `src/social_sim/` into `Code/` | **not done**; the package is the documented transitional canonical home |

## 7. Verification

```
PYTHONPATH=src python -m pytest tests/test_simulator_graphs_1309.py -q      # 29 passed
```

The fixtures load together with `load_world("NooPunk-Simulator/Graphs/fixtures")`, and `World.cross_reference()` returns
the counts a demo prints: 6 actors, 3 concepts, 6 stances, 5 places, 3 routes, 0 unresolved graph references.
