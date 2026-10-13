# Ukweli: the modern map specification (issue #325, deliverable 3)

**Status: PROPOSAL — specification only.** No mechanic, no numeric scale and **no geography beyond what
the scenario data already declares**. This is deliverable 3 of #325: *"concise annotated city/islands
diagram and data-driven location/network schema, respecting 6–8 playable nodes."*

It describes what `strategy_game/data/ukweli_local.json` already contains and is validated against that
file by `strategy_game/map_spec.py` — so the diagram cannot drift from the data.

---

## 1. The annotated diagram

New Ukweli on the main island, with two outlying islands. Edges are the declared route list.

```
                    ┌──────────────────────────┐
                    │  airfield_island         │   island · communications
                    │  Airfield Island         │   international airport, satellite
                    │  [pressure 1]            │   and undersea cable landing
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┴─────────────┐
                    │  port                    │   main island · shipping
                    │  Industrial Logistics    │   the working port: freight,
                    │  Port  [pressure 1]      │   labour, the shipping giant's footprint
                    └────────────┬─────────────┘
                                 │
   ┌──────────────────┐   ┌──────┴───────────────┐   ┌──────────────────┐
   │  outer_island    │───│  old_harbor          │   │  campus          │
   │  Outer Island    │   │  Old Harbor          │   │  University and  │
   │  Communities     │   │  [pressure 0]        │   │  Hospital        │
   │  island · ferry, │   │  heritage, trade     │   │  science         │
   │  tourism         │   └──────┬───────────────┘   └────────┬─────────┘
   └──────────────────┘          │                            │
                          ┌──────┴────────────────────────────┴──────┐
                          │  civic                                  │
                          │  Civic and Commercial Centre            │
                          │  [pressure 1] · government, finance     │
                          └──────┬──────────────────────────┬───────┘
                                 │                          │
                    ┌────────────┴─────────────┐   ┌────────┴─────────┐
                    │  residential             │   │  coast           │
                    │  Mixed Neighborhoods     │   │  Coastal         │
                    │  housing                 │   │  Hinterland      │
                    └──────────────────────────┘   │  agriculture     │
                                                   └──────────────────┘
```

**Reading the diagram:** `old_harbor` and `civic` are the two hubs, each with three routes. `campus`,
`outer_island`, `airfield_island` and `coast` are leaves. The graph is deliberately **sparse** — seven
routes over eight nodes — because reachability is the strategic question, not distance.

---

## 2. The location schema

Eight playable nodes, which is the top of the 6–8 budget. Fields are exactly those already in the data:

| Field | Meaning | Constraint |
| --- | --- | --- |
| `id` | stable identifier | lowercase, unique, never reused |
| `label` | display name | prose; the diagram may shorten it, the id may not change |
| `tags` | what the place *is* | open vocabulary, non-empty, no quantities |
| `island` | whether it is off the main island | boolean; must be reachable by a route |
| `pressure` | declared starting pressure | existing data, **not proposed here** |

| `id` | `island` | `tags` |
| --- | --- | --- |
| `old_harbor` | no | heritage, trade |
| `civic` | no | government, finance |
| `residential` | no | housing |
| `campus` | no | science |
| `port` | no | shipping |
| `outer_island` | **yes** | ferry, tourism |
| `airfield_island` | **yes** | communications |
| `coast` | no | agriculture |

### The route schema

A route list of unordered pairs: `[[a, b], …]`. Rules the validator enforces:

1. **6–8 nodes.** Under six cannot carry the four factions; over eight breaks the small-table promise.
2. **Both endpoints exist.** No dangling route.
3. **No self-loops, no duplicates** (a route is a set, not a direction).
4. **Connected.** Every node is reachable from every other — an unreachable node is unplayable.
5. **Every island is reachable.** An island with no route is scenery, not a location.
6. **At least two nodes** so the graph is not a single point.

---

## 3. The restricted island — a deliberate absence, and the one thing needing your word

The bible establishes that the government designated **an entire island a prohibited/protected zone**,
publicly to safeguard Ukweli's biodiversity. **No node in the scenario data is marked `restricted`**, and
#325's suggested initial state asks for *"6–8 location nodes, one marked restricted."*

I have **not** added a ninth node or a new flag, and I want to be explicit about why, because the
distinction matters:

- The playable set is already at the **top** of the budget (8). Adding the restricted island as a
  playable location would break it, not complete it.
- A *prohibited* island is by definition not somewhere a leader moves pieces on turn one. It is better
  represented as a **gate** — reachable only through an event, a discovery or a GM intervention — which
  is exactly what #303's context/agent split and the existing shock deck already support.
- The shock **"Unverified anomalous signal at coastal facility"** is the current mechanism by which the
  anomalous margin reaches play, and it does not require the island to be a node.

**So the specification states the rule rather than inventing the object:** the restricted island is
**declared in prose, out of the playable node budget, and enterable only through an event.** If you
would rather it be a marked node, that is a one-field decision and I have left it open rather than
guessing — see §5.

---

## 4. What the validator enforces

`strategy_game/map_spec.py` reads the shipped scenario data and reports, without raising:

- the node budget (6–8) and the count actually declared;
- dangling, duplicated or self-looping routes;
- connectivity, and whether every `island: true` node is reachable;
- tag presence, and that ids are unique and lowercase;
- **and it introduces no number of its own** — it checks the declared `pressure` field's shape but
  proposes no scale, per the no-quantity discipline.

---

## 5. Open questions for the author

1. **Is the restricted island a marked node, or an event-gated location?** My recommendation is the
   latter, for the reason in §3, but this is your call and I have not decided it.
2. **Should `pressure` stay on the location record at all?** It is existing declared data; #302's note
   already suggested scenario configuration rather than the engine record.
3. **Should the diagram be rendered as an image** for the eventual animated tabletop, or is a text
   diagram plus the data-driven schema sufficient for now? The digital presentation is explicitly not
   required for play.
