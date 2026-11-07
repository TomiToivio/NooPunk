# Shared Tag/Graph contracts (#1295)

> **Status: minimal contract, version 1.** Three subprojects consume these shapes; changing them needs
> a cross-project review, not a silent edit in whichever subproject needed it first.

The rule that keeps the pivot from becoming a fourth rules system: **the contract is the smallest set
of facts that all three consumers already agree on.** Everything else stays in its own subproject.

---

## 1. Identifiers

Stable, human-readable, dotted:

| Prefix | Meaning | Example |
| --- | --- | --- |
| `series.` | a Story series | `series.europol01` |
| `episode.` | an episode within a series | `episode.first_day` |
| `scene.` | a Scene node | `scene.briefing` |
| `pc.` / `npc.` | characters | `pc.rookie`, `npc.falk` |
| `loc.` | a physical or astral location | `loc.ratakatu_12` |
| `cyber.` | a device, host or service | `cyber.camera` |
| `clue.` / `goal.` / `social.` / `personality.` | the four tag families | `clue.warehouse_log` |

Rules: lowercase, `snake_case` after the prefix, no spaces, no reuse after deletion (a retired id is
retired, not recycled), and **one id means one thing across all three subprojects**.

## 2. Graph families

Four, and only four (`src/world/graphs.py`):

| Family | Nodes | Edges | Occupancy |
| --- | --- | --- | --- |
| **Physical** | locations | routes (`directed` optional, `kind`) | `occupants: actor → loc` |
| **Cyber** | devices/hosts/services | links | `avatars: actor → cyber node` |
| **Social** | characters, factions | relationships, `score` −4…+4, `kind` | — |
| **Story** | series, episode, scene | transitions, prerequisites | — |

An **Astral** family does not exist. Astral scenes are non-navigable (`run_astral_scene`), and adding a
fifth family is a schema change, not a convenience.

## 3. Serialised form

```json
{ "format": "noopunk.world.graphs", "version": 1,
  "physical": {...}, "cyber": {...}, "social": {...}, "story": {...} }
```

- `format` and `version` are **required**; a reader refuses an unknown version rather than guessing.
- Enums are serialised as their string values.
- Two serialisations of the same data must be byte-identical after sorting keys.

## 4. Tags

Four families (`src/world/narrative_tags.py`), and they stay apart:

- **SocialTag** — holder, target, fact, polarity, source
- **GoalTag** — owner, text, state, blockers
- **ClueTag** — clue id, holder, fact, route, reliability, `bears_on`
- **PersonalityTag** — NPC, trait, lever, under pressure, taboo

A tag is a **fact, not a modifier**. Nothing in the contract adds a number to a roll.

## 5. Scene types

`Social`, `Investigation`, `Exploration`, `Action`, `Cyber`, `Astral` (`src/world/scenes.py`).

A scene declares its type honestly; the type is an interface shape, never a resolution rule. CWN
remains the action authority for anything with a check in it.

## 6. Direction of travel

```
Tomi's Story  →  Story Graph  →  RPG narrative
LaclauGPT-informed Simulator  ↔  Tag/Graph state  →  RPG social world
```

- **Story → Graph is one-way.** Agents convert; they do not write back.
- **Simulator ↔ Graph is a synchronisation**, not a merge: each side keeps provenance.
- **RPG consumes.** It never owns the manuscript or the simulation.

## 7. Compatibility

A change is **breaking** if it renames an id prefix, removes a field, changes a node kind, changes the
meaning of `score`, or alters version. Breaking changes need:

1. a new `version`,
2. an adapter or migration for existing data,
3. a cross-project review recorded on the issue,
4. a test that the old data still loads or fails with a clear message.

## 8. What this contract deliberately does not define

- character sheets (CWN owns them)
- how a scene resolves (CWN owns that)
- simulation internals (the Simulator owns them)
- UI or rendering (each interface owns its own)
