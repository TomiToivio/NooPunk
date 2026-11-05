# Graph implementation v1: four layers first (#1178)

> **AUTHOR DECISION (2026-11-05):** [issue #1178](https://github.com/TomiToivio/NooPunk/issues/1178) supersedes the conflicting portions of draft [#1164](DRAFT_GRAPH_SCENES_1164.md) and [the earlier PSI proposal](DRAFT_ASTRAL_GRAPH_SWN_PSI_1164.md). The v1 Python adapter is in `src/rules/four_graphs.py`. The Astral Graph **is deferred**, and spontaneous sleeping OOBEs, NDEs and Monroe-inspired technology initiate **scripted Story scenes**, not player-selected Astral navigation.

## Canonical distinction

| Family | What is a node? | What is an edge? | Where are characters? |
|---|---|---|---|
| Physical | World, city, district, location or room, at the appropriate map resolution | Physical route / door | Positions/occupants stored **outside** node records |
| Cyber | Device or service, such as a computer, camera or turret. It can act **and** host hacker avatars | Network link | A hacker avatar occupies a Cyber node; its operator remains at a Physical node |
| Social | Character or faction | Social relationship with score −4..+4 | Characters themselves are nodes; this is **not** a movement graph |
| Story | Series, Episode, Scene | Contains / conditional transition | Scenes reference locations/entities and participants, but are not locations |
| Astral (later) | **Astral locations**, not conscious agents | Astral route | Projected agents occupy Astral locations; do not implement until Projection scenes need navigation |

The author-owned `design/graphs/README.md` and `design/graphs/RULES.md` remain unchanged. Their earlier shorthand about agents in a graph is interpreted using **occupancy**, not character-as-spatial-node.

## Current gameplay scope

- `SpatialGraph` allows `enter`, `move` and `occupants` with explicit routes and story flags for door/access gating. The caller runs normal **CWN** movement/combat and permissions. Passing a gate flag never grants a skill bonus or a turn.
- `Cyber` uses the **same topology adapter**, except each node is a service/device that may list device actions and a `physical_ref`. The existing CWN hacking subsystem must decide whether the flag granting entry is earned. `FourGraphs.move_avatar` changes only Cyber positions.
- `SocialGraph` stores edges distinct from positions, with directed/asymmetric ties. **Missing** means unknown rather than relationship score zero. Persona/goal/reputation systems own the underlying data, not this graph.
- `StoryGraph` contains Series → Episode → Scene; branches through flags and goal IDs. Query existing `GoalLog` for completion and pass IDs into `available`. Existing investigation core clues remain accessible through authorized inquiry.
- `FourGraphs` checks Cyber->Physical references and Story->Physical/Cyber/Social references. Snapshots are versioned UTF-8 JSON, keeping one canonical actor record elsewhere. `networkx_view` optionally derives a NetworkX `MultiDiGraph`. NetworkX is **not a dependency** of the resolver.

### Author-friendly Markdown/YAML

The `graph_authoring.read_record` loader accepts a Markdown file with YAML frontmatter and descriptive prose. Python users can install PyYAML for conventional YAML, or use JSON object frontmatter (a YAML subset) without any dependency. `compile_graphs` validates four records with stable `record_id` and corresponding `graph_type`; it does **not** execute prose or allow Python snippets in authored data. Source is Markdown; Python NetworkX views are derived.

Example of a **Physical domain record** with JSON-as-YAML frontmatter (the same keys work with ordinary YAML and PyYAML):

```markdown
---
{
  "record_id": "graph.helsinki.physical.v1",
  "graph_type": "physical",
  "data": {
    "graph_type": "physical", "version": 1,
    "nodes": [
      {"id": "physical.kurvi.home", "label": "Europol company housing"},
      {"id": "physical.ratakatu", "label": "Federal office"}
    ],
    "edges": [
      {"id": "route.kurvi.ratakatu",
       "source": "physical.kurvi.home",
       "target": "physical.ratakatu",
       "directed": false}
    ],
    "positions": {"pc.tony": "physical.kurvi.home"}
  }
}
---

# Helsinki: introductory locations

The rookie leaves the apartment. Normal CWN travel resolves arrival.
```

To bind an authored Cyber avatar to a physical operator, add an `avatar_operators` mapping inside Cyber `data` (for example, `{"avatar.tony": "pc.tony"}`), and list the avatar in Cyber `positions` and the operator in Physical `positions`. The validator checks both.

For the other three files replace `graph_type`/data with `cyber` (devices, links, avatar positions), `social` (character/faction entities, relationships) and `story` (Series/Episode/Scene nodes and `contains`/`transition` edges). The adapter currently compiles *one domain record per family*; future multi-record ingestion must explicitly merge and validate stable IDs before use. The existing [authoring templates](../graphs/templates/) remain usable inspiration, but they are not automatically compiled if their frontmatter lacks `data` and `record_id`.

### Existing systems remain authoritative

`src/rules/cwn_hacking.py`, `cwn_combat.py`, `goals.py`, `investigation.py` and `swn_psionics.py` are not replaced. The new adapter **does not automatically wire** the existing console/Evennia runtime into these graph views: integration is a subsequent targeted task with an explicit actor-ID mapping and CWN action authority.

## Psionics and later character options

- Player-selectable SWN disciplines are **Telepathy and Telekinesis only**, trained using the published **SWN Psychic Training Focus** (published edition verification required).
- Other psychic effects belong to NPCs, scripted Story scenes, or named equipment (psychotronic cyberware and devices).
- **Astral Projection is scripted** during dreams/OOBEs, NDEs and Monroe-like technical sessions. No freeform Astral Graph player traversal in v1.
- The AWN Mutant Edge becomes a human–alien Hybrid Edge. Pseudo-Psychic Mutations are genuinely psychic in fiction. The author requires a selected positive mutation, a randomly rolled additional positive mutation, and alternative recognizable-hybrid Stigma/Negative Mutation options. **Do not implement tables until the selection/roll paths are clarified and editions checked.**
- AWN Mentalist and CWN Spellcaster/Summoner Edges are allowed as separate published options. **PSI = Magick** in ontology, not unrestricted cross-system access.
- Existing drafts granting free selectable Psychic Defence or Astral Projection are **superseded**. Defensive equipment remains possible; NPC/scripted abilities remain possible. No silent seventh SWN discipline.

## Verification

`tests/test_four_graphs_1178.py` checks occupancy, gated route navigation, co-location, asymmetric Social scores, story gates, cross-reference validation, roundtrip persistence and optional NetworkX projection. `tests/test_graph_authoring_1178.py` checks Markdown record validation.

**Status note:** the graph adapter is an executable first slice; full CWN/Evennia integration is not claimed. No Astral graph feature has been added as part of #1178.
