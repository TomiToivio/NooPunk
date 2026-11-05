# The four graph families (#1178)

**Status:** implemented for **physical**, **cyber**, **social** and **story**; the **astral** graph is deliberately
absent. Code: `src/noopunk_graphs/` (`model.py`), tests: `tests/test_graph_families_1178.py`.

The one rule that shapes everything: **a character is never a node.** Characters *occupy* places and move along
edges; the only family whose nodes are people is the social graph, and there a character is a node and the edges are
relationships, not routes.

| family | nodes are | edges are | a character is | movement |
|---|---|---|---|---|
| **Physical** | places: world → city → district → location → room | routes, doors, passages | an **occupant** of one place | along an edge, never across the map |
| **Cyber** | devices, services, networks — a device is *also* a place an avatar enters | network links | occupant of a cyber node (the **avatar**) | along a link; the body stays where it is |
| **Social** | characters and factions | relationships, **−4…+4** | **the node** | none — a social link is not a route |
| **Story** | series, episodes, scenes | entry / sequence / alternative transitions, each gated by a flag | not present | none — scenes are not places |
| **Astral** | *deferred* | — | — | — |

## Why the astral graph is not here

Astral Projection is a **scripted event** in this design (spontaneous OOBE, NDE, or a Monroe-style technology
scene), not a freely activated power, and a navigable astral graph is only useful when such a scene needs to be
walked. Until then an astral scene is a story scene with tags and a description. Constructing the astral family
raises `GraphError` with that reason, so nobody adds it by accident and calls it approved.

## What the code enforces

1. **Family kinds.** A physical node may be a place; a social node may be a character or faction; an "agent" or
   "character" kind in any place family is refused.
2. **Occupancy is separate from nodes.** `World.place(actor, node)` refuses a social node (characters *are* those
   nodes), refuses a story node (a scene is not a place), and refuses an id that is already a node — a location
   cannot walk into a room.
3. **Movement needs an edge.** `World.move` refuses a hop with no edge, honours `directed`, and refuses social
   movement outright.
4. **Two occupancies per character, never one.** Cyber movement is keyed `(actor, family)`, so a hacker's avatar
   crossing a network leaves the officer's body exactly where it was.
5. **Co-location is the interaction condition.** `co_located(a, b)` is true only when both occupy the same place in
   the same family.
6. **Cyber devices reference the physical graph.** `location_ref` points at a physical node; pointing at another
   cyber node is refused, because the device *is* the cyber node and *sits in* a physical one.
7. **Social edges are signed and bounded.** `relationship` is required and must be −4…+4; a `travel_cost` on a
   social edge is refused.
8. **Story transitions name their flag.** Every non-entry transition requires `when`; `available_scenes(episode,
   flags)` returns only what the flags permit; `verify_required_scenes(episode)` refuses an episode whose required
   scene is missing or is not a scene.
9. **Ids are unique and references resolve.** Duplicate node or edge ids and dangling endpoints are refused at
   construction, not at play time.

## Using it

```python
from noopunk_graphs import World, Graph, Node, Edge, Family, physical_from_helsinki

world = World([physical_from_helsinki("data/world/helsinki_locations.json",
                                      routes=[("home_helsinginkatu", "kurvi")])])
world.place("rookie", "home_helsinginkatu")
world.move("rookie", "kurvi")
world.occupants("kurvi")            # ("rookie",)
```

`World.to_dict()` / `World.from_dict()` round-trip the whole thing through JSON, including occupancy, so a save file
can reproduce who was standing where.

## What is not in this slice

* **No new dependency.** The graph is an adjacency map; a NetworkX projection can be added later by whoever needs
  one. Nothing in play depends on a third-party library.
* **No authored YAML/Markdown loader.** The authoring formats in
  [`docs/design/DRAFT_GRAPH_SCENES_1164.md`](../design/DRAFT_GRAPH_SCENES_1164.md) remain proposals; this slice takes
  JSON (and the existing Helsinki data) and leaves the format decision to the author.
* **No astral navigation, no cross-layer effects, no tactical grid.** Those are separate approvals.
* **No PSI or Edge rules.** The SWN/Psychic Training/Hybrid decisions in #1178 §1–§4 are tracked separately.

## Running it

```sh
python3 -m unittest tests.test_graph_families_1178 -v
# or, as CI collects it:
python3 -m unittest discover -s tests -p 'test_*.py'
```
