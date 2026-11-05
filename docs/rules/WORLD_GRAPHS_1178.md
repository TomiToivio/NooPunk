# World graphs: Physical, Cyber, Social and Story (#1178)

**Status: first playable graph slice implemented; issue #1178 remains open for later work.**
The Astral Graph is deliberately **not** implemented. Physical and Astral nodes are
**locations**; characters are occupants, not spatial nodes.

## Corrected semantics

| Graph | Nodes | Edges | What moves / acts |
|---|---|---|---|
| **Physical** | Places: world, city, district, location, room | Routes, doors, paths | A PC/NPC occupies one location and traverses one valid edge. Co-location enables ordinary CWN interaction. |
| **Cyber** | Devices: camera, turret, controller, host, service | Network links | A hacker **avatar** occupies a device and moves along network links. The operator's body stays in its Physical node. The device can also act as a machine. |
| **Social** | Characters and factions | Directed relationships, score −4…+4 | No spatial movement. A relationship is not a route. |
| **Story** | Series → Episodes → Scenes | Sequence, prerequisite and transition links | Scenes reference Physical/Cyber/Social records and goals; a scene is not a location. |
| **Astral** | *Deferred* | *Deferred* | Added only when scripted Astral Projection scenes need navigation. |

The implementation is `src/world/graphs.py`; tests are `tests/test_world_graphs_1178.py`.
Nothing in the module rolls dice, spends Effort, changes HP or replaces CWN movement,
exploration, combat or Hacking. `WorldGraphs` only validates cross-references and serializes
the four families.

## Author-facing shape

The canonical interchange shape is plain YAML/JSON. A loader can pass the parsed mapping to
`WorldGraphs.from_dict()`; no NetworkX import is required to author or validate it.

```yaml
format: noopunk.world.graphs
version: 1
physical:
  graph_type: physical
  nodes:
    - {id: loc.home, label: Kurvi home, kind: room}
    - {id: loc.office, label: Europol office, kind: room}
  edges:
    - {source: loc.home, target: loc.office, directed: false, kind: door}
  occupants:
    pc.rookie: loc.home
cyber:
  graph_type: cyber
  nodes:
    - id: cyber.camera
      label: Corridor camera
      device_type: camera
      physical_location: loc.office
      actions: [observe, record]
  edges: []
  avatars: {}
social:
  graph_type: social
  nodes:
    - {id: pc.rookie, label: Rookie, kind: character}
    - {id: npc.falk, label: Laura Falk, kind: character}
  edges:
    - {source: pc.rookie, target: npc.falk, score: 2, kind: colleague}
story:
  graph_type: story
  nodes:
    - {id: series.first, label: First series, kind: series}
    - {id: episode.one, label: First case, kind: episode, parent_id: series.first}
    - id: scene.briefing
      label: Briefing
      kind: scene
      parent_id: episode.one
      scene_types: [social]
      prerequisites: [flag.case_open]
  edges:
    - {source: series.first, target: episode.one}
    - {source: episode.one, target: scene.briefing}
```

## API

```python
from src.world.graphs import WorldGraphs

graphs = WorldGraphs.from_dict(payload)
graphs.physical.enter("pc.rookie", "loc.home")
graphs.physical.move("pc.rookie", "loc.office")       # one valid edge
graphs.physical.co_located("pc.rookie", "npc.falk")  # same node?

graphs.cyber.enter("pc.rookie", "cyber.camera")
graphs.cyber.move_avatar("pc.rookie", "cyber.server")  # body does not move
graphs.cyber.actions_at("pc.rookie")                   # declared device actions

graphs.social.score("pc.rookie", "npc.falk")           # None when no edge, not 0
graphs.story.advance("scene.briefing", "scene.raid", flags={"flag.warrant"})
```

`from_dict()` validates: unique non-empty IDs, non-dangling endpoints, no self-loop routes,
parents exist, social scores in −4…+4, story hierarchy (Series → Episode → Scene), and Cyber
device `physical_location` references a real Physical node in `WorldGraphs`.

## Invariants

1. **One actor, one position per graph.** A Cyber avatar does not move the Physical body.
2. **No teleport.** Movement requires one valid edge; no implicit map-wide travel.
3. **Co-location is a fact, not a roll.** Two actors can interact at the same Physical node;
   CWN resolves what they do.
4. **Social links are not routes.** They survive Physical travel and never place a character.
5. **Scene entry is gated, not railroaded.** A transition needs its condition; a scene with
   prerequisites cannot be entered until they are recorded. Mandatory truths are not hidden
   behind one optional check.
6. **Astral is absent, not silently approximated.** `WorldGraphs.to_dict()` has no `astral`
   key; the Astral schema is added with the scripted projection work.

## Not implemented in this slice

- Astral graph and projection navigation (deferred by #1178).
- NetworkX **projection is available** via `WorldGraphs.to_networkx()` (optional import; the
  authored dicts remain the source). A Markdown-frontmatter loader and a full scene runtime
  are not implemented yet.
- Psychic Training, Hybrid/Mutant, Mentalist/Spellcaster/Summoner Edges and the PC
  Telepathy/Telekinesis restriction. Those are separate later tasks in #1178.
- Tabletop rulebook wording; no CWN/SWN/WWN/AWN rule is changed.

## Acceptance tests

`python3.11 -m unittest tests.test_world_graphs_1178` covers the issue's listed cases:
two actors meet only when co-located; movement follows one edge; a camera is a Cyber node
with a Physical location; an avatar moves without moving the body; Social ties survive
Physical travel; a scene transition depends on a flag; the bundle round-trips; no Astral key
exists.

## Loading the canonical Helsinki places

`src/world/helsinki.py` adapts the existing `data/world/helsinki_locations.json` into a `PhysicalGraph`: the six
places keep their canonical ids, each gets its district as a `parent_id`, and `start_location()` returns the
opening node instead of a hard-coded string.

The location file has **no routes** — travel was an action of the old map panel — so routes come from the caller:

```python
from src.world.helsinki import load_helsinki_physical, start_location

graph = load_helsinki_physical(routes=[(start_location(), "kurvi")])
graph.enter("rookie", start_location())
graph.move("rookie", "kurvi")
```

Route endpoints are validated against the loaded places, so a typo in a route fails at load rather than at play.
Tests: `tests/test_helsinki_graph_adapter_1178.py`.

**Import trap:** this repository also has `mud/world`, importable as `world` when MUD tests put `mud/` on
`sys.path`. Import the graph as `src.world.graphs` (as the acceptance tests do) or as `world.graphs` only from a
module that is itself inside `src/world`. A bare `import world.graphs` from an unrelated test can resolve to the
MUD package depending on collection order — that failure is order-dependent and looks like a flaky import.
