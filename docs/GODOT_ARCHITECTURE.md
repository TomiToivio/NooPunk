# Godot RPG Architecture

This document describes only the current technical scaffold. It does **not** define NoöPunk mechanics or lore.

## Runtime

- `project.godot` defines a minimal Godot 4 project.
- `scenes/main.tscn` is the bootstrap scene.
- The bootstrap scene displays only a neutral project-status message.

There is currently no gameplay code.

## Separation of concerns

### `src/godot/`

Reserved for future Godot-specific controllers, adapters, scene glue, and engine integration.

Canonical rules should not live here.

### `src/rules/`

Reserved for future engine-independent RPG rule logic.

This directory is intentionally empty because the core mechanic, attributes, skills, combat, psionics, and other rules have not yet been specified.

### `src/world/`

Reserved for future world/domain logic after the author defines the relevant setting structures.

It must not be populated by inferred lore.

### `src/simulation/`

Reserved for future simulation logic.

No agent behavior, equations, causal model, or simulation assumptions are currently defined.

### `data/rules/`

Reserved for author-defined machine-readable rule data that can correspond to human-readable material in `RULEBOOK.md`.

### `data/world/`

Reserved for author-defined canonical world/content data.

### `data/simulation/`

Reserved for author-defined simulation parameters and data.

## Tabletop ↔ Godot contract

The long-term goal is for the tabletop RPG and Godot RPG to share the same conceptual rules.

When rules are eventually specified:

1. `RULEBOOK.md` remains the human-readable rules reference.
2. Engine-independent rule concepts should live in `src/rules/` and/or `data/rules/`.
3. Godot scenes and UI should consume those concepts through adapters rather than redefine them.
4. World content and simulation logic should remain separate from presentation code.

This is an architectural direction, not a current rules implementation.

## Intentionally undefined

The scaffold does not choose:

- dice or randomization system
- attributes
- skills
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
