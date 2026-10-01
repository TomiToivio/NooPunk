# Godot RPG Architecture

This document describes only the preserved technical scaffold. It does **not** define NoöPunk mechanics or lore.

> **Development status:** Godot is a later-stage port. Substantive gameplay work waits until the corresponding tabletop rules/world material are defined and stable in `RULEBOOK.md` and the canonical tabletop/world documentation. Existing Godot infrastructure is preserved rather than discarded.

## Runtime

- `project.godot` defines a minimal Godot 4 project.
- `scenes/main.tscn` is the bootstrap scene.
- The bootstrap scene displays only a neutral project-status message.

The first canonical gameplay layer is now implemented: the six attributes and a core check. **That check is the superseded 3d6 system** (RULEBOOK.md §17.1) — it has not yet been ported to the canonical legacy provisional **2d6 skill check**. No UI or broader gameplay subsystem has been added.

## Separation of concerns

### `src/godot/`

Reserved for future Godot-specific controllers, adapters, scene glue, and engine integration.

Canonical rules should not live here.

### `src/rules/`

Contains the engine-independent Python implementation of the canonical attributes plus a core check. **The check is the superseded 3d6 system and awaits the port** (RULEBOOK.md §17.1). Canonical numeric data is loaded from data/rules/core.json, which likewise still carries the withdrawn 3d6-era values and is marked `_superseded_note`.

### `src/world/`

Reserved for future world/domain logic after the author defines the relevant setting structures.

It must not be populated by inferred lore.

### `src/simulation/`

Reserved for future simulation logic.

No agent behavior, equations, causal model, or simulation assumptions are currently defined.

### `data/rules/`

Contains author-defined machine-readable rule data corresponding to RULEBOOK.md. data/rules/core.json is the canonical runtime data for attributes, human generation, difficulty targets, unskilled penalty, and opposed-check semantics.

### `data/world/`

Reserved for author-defined canonical world/content data.

### `data/simulation/`

Reserved for author-defined simulation parameters and data.

## Tabletop → Godot contract

The tabletop RPG is the canonical first implementation. Godot receives stable tabletop systems as a later conversion; it does not co-design unfinished rules.

The long-term goal is for the tabletop RPG and Godot RPG to share the same conceptual rules.

The core resolution mechanic and the six canonical attributes are now specified. The contract they follow:

1. `RULEBOOK.md` is the canonical human-readable rules source and is updated first.
2. The canonical constants live once in `data/rules/core.json` and are consumed by the shared Python layer in `src/rules/core.py`.
3. The Godot runtime reads that same data through `src/godot/core_rules.gd`; scenes and UI should consume those concepts through adapters rather than redefine them.
4. World content and simulation logic remain separate from presentation code.
5. Nothing outside the specified mechanic and attributes may be added without explicit author instruction.

### Parity and permitted divergence

NoöPunk's design principles require **the same world, same rules, same mechanics** across Tabletop, Godot, and Concordia (see [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) §2). For this runtime that means:

- **Shared (must not diverge):** attributes, skills, dice/probability model, combat, hacking, psionics, cybernetics, progression, equipment logic, world assumptions, terminology, and core balance values.
- **May diverge:** scenarios, missions, maps, encounters, presentation, UI, pacing, procedural generation, and implementation details required by the medium.

A presentation difference between the tabletop and Godot versions of a scenario is expected. A **rule** difference is a defect: extract or extend the shared specification rather than forking the rule in GDScript.

## Intentionally undefined

The scaffold implements the author-specified attributes and a core check only. The Godot adapter reads the difficulty names and targets directly from `data/rules/core.json`, and its check resolver accepts an optional deterministic dice-total override for parity tests. Production checks still roll 3d6 when no override is supplied.

**This is stale with respect to the canonical rule.** `RULEBOOK.md` §4 now specifies `2d6 + skill level + attribute modifier` against a `6 / 8 / 10 / 12 / 14+` ladder, with opposed ties won by the player character. The adapter has not been ported; doing so is a separate later task (RULEBOOK.md §17.1). Do not treat the adapter's behaviour as canon.

The difficulty names currently in `data/rules/core.json` are **Easiest 3, Easier 6, Easy 9, Normal 12, Hard 15, Impossible 18**. These are **superseded** — they are the withdrawn 3d6 ladder, not the canonical skill-check ladder (RULEBOOK.md §4, now `6 / 8 / 10 / 12 / 14+`). Earlier Hard/Harder/Hardest labels are not retained as runtime aliases because doing so would make `Hard` ambiguous after its target changed from 12 to 15. The legacy provisional ladder deliberately does **not** reuse the old names either: difficulty 6 keeps its number but changes meaning, so re-pointing a name would silently change what an old note meant.

It still does not choose:

- skill levels and the skill list (specified for tabletop in RULEBOOK.md §5.3; not yet ported)
- derived statistics
- character creation
- combat
- damage, wounds, armor, health, or initiative
- advancement
- psionics
- NHI taxonomy or mechanics
- cybernetics mechanics
- hacking
- social mechanics
- equipment or economy
- factions
- quests or plot
- detailed geography
- vehicles
- simulation variables, agents, equations, or causal rules

These are waiting for separate author-driven design steps.

## Current technical decisions

- **Godot generation:** Godot 4 project format (`config_version=5`).
- **Renderer:** `gl_compatibility` for a conservative, broadly compatible baseline.
- **Dependencies:** none.
- **Bootstrap resolution:** 1280×720 logical viewport.
- **Code architecture:** no framework, autoload, plugin, inheritance hierarchy, or gameplay singleton has been introduced.

These choices are intentionally easy to revise.


## Porting gate

Before adding a substantive Godot gameplay system:

1. confirm the tabletop rule/world concept exists;
2. confirm it is coherent enough for tabletop play;
3. resolve rule ambiguity in the tabletop source;
4. derive a digital specification;
5. implement the Godot adapter without redefining the rule.

The preferred path is **tabletop rule → digital specification → Godot**. Concordia follows the same shared specification later. Platform-specific presentation may differ, but a hidden rules fork is a defect.
