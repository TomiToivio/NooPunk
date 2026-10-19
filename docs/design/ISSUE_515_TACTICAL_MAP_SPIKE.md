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
