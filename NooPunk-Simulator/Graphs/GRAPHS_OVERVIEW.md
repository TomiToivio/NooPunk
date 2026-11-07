# The Simulator's graph layer: three views, one set of ids (#1309)

> **Status: implemented.** Models in [`src/social_sim/graphs.py`](../../src/social_sim/graphs.py), fixtures in
> [`fixtures/`](fixtures/), operational rules in [`../Rulebook/GRAPHS_1309.md`](../Rulebook/GRAPHS_1309.md), tests in
> [`tests/test_simulator_graphs_1309.py`](../../tests/test_simulator_graphs_1309.py).

This page is the map: what the three views are, where their truth lives, how they are versioned, and how they relate to
the RPG's graph contract without becoming a fifth family.

## 1. The three views

| view | file format | source of truth | what it answers |
|---|---|---|---|
| **Social** | `noopunk.simulator.social` v1 | `Graphs/fixtures/social_graph_1309.json`; Paper: [`../Paper/SOCIAL_GRAPH.md`](../Paper/SOCIAL_GRAPH.md) | who knows whom, who belongs to what, who is allied and who is not |
| **Ideology** | `noopunk.simulator.ideology` v1 | `Graphs/fixtures/ideology_graph_1309.json`; theory: the LaclauGPT Phase 1 paper and `THEORY.md` | what each actor is coded as claiming, and where two actors disagree |
| **Physical** | `noopunk.simulator.physical` v1 | `Graphs/fixtures/physical_graph_1309.json`; Paper: [`../Paper/PHYSICAL_GRAPH.md`](../Paper/PHYSICAL_GRAPH.md) | where places are, how they connect, which locations open a sub-graph |
| **World** | `noopunk.simulator.world` v1 | assembled from the three at load time | the joins: every stance actor is a social actor, every `graph_ref` names a place |

## 2. Ids

* **Actors** follow Paper's convention: `person_mars_eldrich`, `organization_quiet_correspondence`,
  `institution_europol_field_office`, `faction_accelerationist_circle`.
* **Places** follow Paper's convention: `location_ratakatu_12`.
* **Concepts** are stable slugs: `signifier_disclosure`, `demand_machine_restraint`, `frame_human_continuity`.
* **Stances** carry the statement they were coded from (`stmt-001`), so a claim can be traced back to its evidence.

The shared RPG contract uses dotted ids (`social.…`, `loc.…`). `shared_id()` maps between the conventions and refuses a
token it cannot classify; **the fixtures do not switch conventions**, and the choice of canonical one is an open
author decision recorded in the Rulebook page.

## 3. Versioning and change policy

* Each file carries `format` and `version`; a loader refuses an unknown format. Adding an optional field is a **minor**
  change; changing what an existing field means is a new version and a migration note in the Rulebook.
* Fixtures are **data, not code**: they may grow as cases need them, and a fixture is never "edited to make a test pass"
  — the test asserts a property, not a snapshot of every value.
* The three views are separate files on purpose: a case can ship a social graph without ideology, or a city graph
  without either.

## 4. Relationship to the RPG graph contract

`docs/architecture/SHARED_TAG_GRAPH_CONTRACTS_1295.md` defines four world-graph families — **Physical, Cyber, Social,
Story** — with dotted ids and `noopunk.world.graphs` serialization. This layer does **not** add a fifth family:

* **Social** here is a Simulator view whose actor ids can be mapped onto the RPG's `social.` ids.
* **Physical** here is the Simulator's city graph; the RPG's Physical family remains its own navigable map, and an
  adapter between them is future work, not a silent merge.
* **Ideology** is explicitly a **projection** of coded discourse over social actors. It is not in the RPG contract and
  does not pretend to be.

Where the two ever disagree, the RPG contract governs the RPG's ids and this layer governs the Simulator's; the adapter
is where they meet, and it must be a documented translation with tests.

## 5. What loads today

```
PYTHONPATH=src python -c "from social_sim.graphs import load_world; print(load_world('NooPunk-Simulator/Graphs/fixtures').cross_reference())"
# {'actors': 6, 'concepts': 3, 'stances': 6, 'places': 5, 'routes': 3, 'external_graph_refs': 0}
```

## 6. Limits, stated here so nobody has to rediscover them

* **No faction mechanics**, no ideological transition rules: the issue defers them until the social foundation is
  tested.
* **No UI.** A Streamlit view was named as a *later* possibility, not a deliverable.
* **No nested Location Graphs.** Rooms and doors are represented only by a `graph_ref`; the inner graph is not built.
* **No Helsinki map.** Three routes and five places, none with coordinates, because a small correct fixture is worth
  more than an invented city.
