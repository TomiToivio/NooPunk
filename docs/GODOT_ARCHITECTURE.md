# Godot RPG Architecture

This document describes only the current technical scaffold. It does **not** define NoöPunk mechanics or lore.

## Runtime

- `project.godot` defines a minimal Godot 4 project.
- `scenes/main.tscn` is the bootstrap scene.
- The bootstrap scene displays only a neutral project-status message.

The first canonical gameplay layer is now implemented: the six attributes and core 3d6 check mechanics. No UI or broader gameplay subsystem has been added.

## Separation of concerns

### `src/godot/`

Reserved for future Godot-specific controllers, adapters, scene glue, and engine integration.

Canonical rules should not live here.

### `src/rules/`

Contains the engine-independent Python reference implementation of the author-specified attribute and core 3d6 rules. Canonical numeric data is loaded from data/rules/core.json.

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

## Tabletop ↔ Godot contract

The long-term goal is for the tabletop RPG and Godot RPG to share the same conceptual rules.

The core resolution mechanic and the six canonical attributes are now specified. The contract they follow:

1. `RULEBOOK.md` remains the human-readable rules reference.
2. The canonical constants live once in `data/rules/core_rules.json`, generated from the shared Python layer in `src/rules/core_rules.py`.
3. The Godot runtime reads that data through `src/rules/core_rules.gd`; scenes and UI should consume those concepts through adapters rather than redefine them.
4. World content and simulation logic remain separate from presentation code.
5. Nothing outside the specified mechanic and attributes may be added without explicit author instruction.

### Parity and permitted divergence

NoöPunk's design principles require **the same world, same rules, same mechanics** across Tabletop, Godot, and Concordia (see [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) §2). For this runtime that means:

- **Shared (must not diverge):** attributes, skills, dice/probability model, combat, hacking, psionics, cybernetics, progression, equipment logic, world assumptions, terminology, and core balance values.
- **May diverge:** scenarios, missions, maps, encounters, presentation, UI, pacing, procedural generation, and implementation details required by the medium.

A presentation difference between the tabletop and Godot versions of a scenario is expected. A **rule** difference is a defect: extract or extend the shared specification rather than forking the rule in GDScript.

## Intentionally undefined

The scaffold now implements the author-specified attributes and core 3d6 resolution only. It still does not choose:

- skills or a skill list
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
