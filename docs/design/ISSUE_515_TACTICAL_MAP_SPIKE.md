# #515 — Optional retro tactical map: implementation spike

**Status:** future-layer technical proposal, not an approved tactical ruleset or an MVP dependency. **Track:** NoöPunk × LaclauGPT crossover `strategy_game/`; the legacy Godot RPG is a separate implementation.

## Architectural decision for review

**Recommended first renderer:** Python/Pygame for a deliberately small, optional 2D frontend attached to the existing Python crossover engine. Godot 2D remains an alternative for a larger art/UI pipeline; Tiled JSON can be an optional editor interchange later. Neither engine should own the game rules. This is a recommendation, not a final author selection.

- Keep all authoritative state and action resolution in the existing Python Fate RPG/mission model. Renderer consumes a projection and emits intents; it never changes stress, resources, success or faction standings directly.
- Use a 20×20, orthogonal square tile map as the **prototype target** explicitly requested by #515, not a universal map-size rule.
- Rendering: walls, floors, doors, interactive objects, four selectable agent tokens, hover/selection, unobtrusive Physical / Cyber / Astral indicators.
- Movement: request a path only through currently traversable cells; no move-through-walls; optional click-to-move. The resolver decides whether the action is permitted and what it costs once author-approved action economy exists.
- A single mission scene supports conversations, evidence, terminals, stealth and (later) hostile encounters. Every goal should admit noncombat resolution where the authored mission supports it.
- Four agents deploy from the existing five-seat roster: the *leader stays the player's character and faction leader*. Do not silently place the leader in a fifth squad slot or replace the four agents.

## Cross-layer contract (proposed)

`MissionMap`: map_id, dimensions, tiles, entity_refs, interactable_refs, overlays (display only), objective_refs.

`MissionIntent`: actor_id, scene_id, declared_action, target_ref, path_cells when relevant, optional chosen approach (Physical/Cyber/Astral).

`MissionEvent`: resolved_action_ref, observed_change, evidence_refs, consequence_refs; the authoritative engine produces it.

`MissionOutcome`: mission_id, involved_agents, evidence/reputation/resource/injury consequences and provenance; records one event for persistence in the #502 shared world model. **Magnitude and transition algorithms remain unapproved.**

These are proposed data contracts, **not implemented or frozen schemas**. A social tie on the strategy graph does not create network connectivity on a tactical map. Cyber access should consult `strategy_game/cyber.py` before offering any intrusion.

## Incremental milestones and gates

1. **Spike:** choose renderer, input surface, tile data and action adapter through author review. No game rules added.
2. **Movement demo:** one map, four selectable roster agents, click-to-move path preview, doors and blockers. Movement cost/action permission awaits approved core mechanics.
3. **Investigation demo:** evidence inspection, dialogue, local terminal and noncombat mission completion using the same RPG resolver.
4. **Optional combat demo:** cover and line-of-sight previews; *do not invent* attacks, action points, damage or enemy AI until #516 and related combat decisions are approved.
5. **Integration demo:** persist wounds/intelligence/political consequences through the #502 single-world interface without mirroring state in UI.
6. **Polish:** tiny sprite sheet / iconography, keyboard accessibility fallback, text-mode equivalence; save and reload mid-mission.

## Acceptance scenario (future, not yet completed)

Four agents enter a 20×20 municipal archive. The mission can end through conversation plus clue recovery; if a security encounter occurs, the player can choose an alternate route. The same map handles a local computer and optional Astral clue, without treating PSI as a hacking backdoor. The encounter returns an inspectable MissionOutcome consumed once by the faction view.

## Comparison

| Option | Benefit | Cost / warning | Verdict |
| --- | --- | --- | --- |
| Pygame | Fast Python prototype; easiest connection to crossover | Bespoke input/UI, more manual tile tooling | Preferred spike |
| Godot 2D | TileMap, built-in scene/editor/UI | Python-to-Godot bridge and two state owners risk | Reevaluate for production |
| Tiled | Dedicated authoring/export | Separate editor and import validation | Optional map authoring only |

**Non-goals:** isometric/3D, cinematic animation, an autonomous combat engine, mandatory battles, exact mission economy, or changes to the legacy RPG. Related: #502, #516, #517, #344, #461.

## Milestone 1 executed (2026-10-19): the grid/tile format and the mission-data schema

Milestone 1 of this issue is *"Technical spike: choose renderer, grid/tile format and mission-data schema."* The renderer remains an author choice (the recommendation above is unchanged), but the other two halves are now artefacts rather than intentions, and they are renderer-neutral by construction: a data boundary that Pygame, Godot or a Tiled export can all consume.

| Artefact | Path | What it settles |
| --- | --- | --- |
| Mission-map module | `strategy_game/mission_map.py` | reader, validator and four-neighbour breadth-first pathfinder; stdlib only |
| Schema instance | `strategy_game/data/mission_map_municipal_archive.json` | one 20×20 municipal archive implementing this document's acceptance scenario |
| Executable contracts | `strategy_game/tests/test_mission_map.py` | 27 checks; the spike's evidence, not a prose claim |

### What the schema declares

Format `noopunk.strategy_game.mission_map`, version `1`, in the house data style (`format`, `version`, `status`, `sources`, `provenance`, `consumes`). A rectangular grid (`rows` of single-character tiles), a **closed tile vocabulary** (`wall`, `floor`, `door`, `terminal`, `evidence`, `person`, `obstacle`, `exit`), door records carrying state, four agent placements, one `leader_ref`, interactables (person / terminal / evidence), objectives, and display-only overlays.

Two boundaries are stated in the data itself rather than left to convention:

- **A terminal is a physical fact, not a network fact.** Its `network_ref` names a connectivity class; whether a path exists in the current era is `strategy_game/cyber.py`'s answer (#344). No floor plan asserts reachability.
- **The strategic map is not replaced.** `strategy_game/map_spec.py`'s eight-node graph remains the strategic layer; a mission happens *inside one* of its locations. This grid is the tactical layer that module explicitly declined to provide.

### What the validator enforces

1. A rectangular grid whose declared size matches its rows.
2. A **sealed boundary** — the perimeter is wall, so no route leaves the map.
3. A **closed vocabulary** — every character is declared; an unknown tile is reported, never guessed.
4. **Doors are state, not scenery** — a door cell is traversable only when its record says open, every door cell has exactly one record, and every record sits on a door cell.
5. **Four deployed agents and no leader** — #515's squad, with the leader remaining the faction leader instead of silently taking a fifth slot; agents are on distinct walkable cells.
6. **Interactables match their tile and can be approached** — a person, terminal or evidence record must sit on its own kind of cell and have at least one walkable neighbour.
7. **The mission is completable** — every objective resolves to an interactable (or the exit) that some deployed agent can actually reach. A map that cannot be finished is a defect, not a difficulty setting.
8. **Overlays are display-only** — Physical / Cyber / Astral markers may sit on any cell, and `walkable()` never consults them.
9. **No mechanic smuggled in as data** — keys such as `damage`, `hit_points`, `initiative`, `action_points`, `difficulty`, `modifier`, `morale`, `cover` or `line_of_sight` are reported wherever they appear in the received payload.

### What the pathfinder deliberately does not do

`path(start, goal)` returns the cells a shortest four-neighbour route crosses, inclusive of both ends, or `()` when there is no route. It does **not** say what the route costs, how long it takes, whether the agent is permitted to take it, or what happens on arrival. There is no cover, line of sight, initiative, action economy, damage or enemy behaviour in the module — the issue's non-goals and the repository's gates keep those for approved rules (#516). A test parses the module and scans its **identifiers** for rule vocabulary, because the prohibition may be stated in prose but must not appear as code.

### How to run it

```bash
python -m unittest discover -s strategy_game/tests -p "test_mission_map.py"
python -c "from strategy_game.mission_map import load_mission_map; m = load_mission_map(); print(m.problems(), len(m.path((2,18),(4,4))))"
```

On `main` the first command reports 27 passing tests and the second prints `() 23` — no defects, and a 23-cell route from the entrance to the west wing.

### Acceptance status: the issue stays open

This completes **milestone 1 only**. The issue's own acceptance criterion — *"a four-agent squad can finish a short tile-based mission featuring movement, at least one investigation/dialogue interaction and optional tactical combat; its outcome is reflected in persistent character/faction state"* — is **not** met, and cannot be met by a data schema. Milestones 2-6 (movement demo, investigation demo, optional combat, integration, polish) remain, and the combat half is gated on #516's approved mechanics. What this section changes is that the next milestone now has a schema to build against instead of a paragraph.
