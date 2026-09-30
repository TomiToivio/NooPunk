# AGENTS.md

## NoöPunk agent rules

These rules are mandatory for coding and documentation agents working in this repository.

### 1. Author intent is canon

Do not invent NoöPunk rules, mechanics, lore, history, factions, technologies, metaphysics, organizations, locations, character classes, archetypes, species, NHI categories, psionic powers, skills, attributes, combat systems, progression systems, equipment lists, economies, or world events unless the author has explicitly specified them.

When a required design decision is missing, prefer:
- a neutral placeholder,
- a generic interface,
- an empty data structure,
- a TODO explicitly marked as requiring author specification,
- or no implementation at all.

Do not "helpfully" complete undefined worldbuilding.

### 2. Advance one layer at a time

NoöPunk is intentionally developed slowly.

For each task:
1. implement only what the issue or author explicitly requests;
2. preserve extension points for later design;
3. do not expand scope into adjacent systems;
4. do not turn examples into canon;
5. do not infer mechanics from genre conventions.

A base RPG scaffold is not permission to create a game system.

### 3. Godot and tabletop must share the same rules model

The intended RPG rules must be usable both:
- in the Godot computer RPG, and
- as a tabletop RPG.

Game logic should therefore be data-driven and engine-independent where practical.

Do not bury canonical rules inside scene scripts or UI code. Prefer separable domain data / rule definitions that can later be documented in RULEBOOK.md and represented in Godot.

Do not define those rules before the author specifies them.

### 4. Current reserved design areas

Until explicitly specified, do not define:
- attributes or derived statistics
- skills
- character creation
- character classes or archetypes
- combat resolution
- damage, health, wounds, armor, or initiative
- psionic powers or psionic mechanics
- NHI taxonomy or capabilities
- cyberware / augmentation rules
- equipment statistics
- economy
- advancement / XP
- factions
- professions
- detailed geography
- quests or canonical plot
- social mechanics
- hacking mechanics
- vehicles
- magic or supernatural systems
- detailed simulation mechanics

These may be represented only by clearly empty extension points when needed by the requested architecture.

### 5. Setting constraints

Treat NoöPunk as an original genre combining Noösphere + Cyberpunk.

The cyberpunk layer remains technological, political, economic, and social cyberpunk. Do not convert it into fantasy.

The speculative consciousness / NHI layer draws inspiration from sources identified by the author, including Teilhard de Chardin, Alexander Wendt, Jacques Vallée, Dean Radin, Federico Faggin, and Donald Hoffman.

Do not present speculative setting assumptions as established real-world scientific facts.

### 6. Time convention

Canonical future dates are written as **20XX** unless the author explicitly says otherwise.

The world is approximately a 2045-like extrapolation from the 2026 situation, but agents must not assign exact future dates on their own.

### 7. Retrocyberpunk tone is not a license to add lore

Recognized influences include old-school Cyberpunk, Shadowrun, Eclipse Phase, Philip K. Dick, Hawkwind, and 1970s space psychedelia.

Use these only as high-level tonal references. Do not copy protected setting material, terminology, characters, factions, mechanics, or text. Do not silently import assumptions from those games or works.

### 8. Minimal Godot foundation

When asked to create the initial Godot RPG base, build only generic infrastructure needed for later author-defined systems, such as:
- a valid Godot project
- minimal project structure
- a bootstrap/main scene
- generic navigation or test scene if necessary
- reusable data/resource architecture
- save/load interface skeleton if explicitly useful and still content-neutral
- tests or validation appropriate to the scaffold
- documentation of extension points

Do not implement speculative gameplay systems merely to demonstrate architecture.

### 9. RULEBOOK.md is intentionally incomplete

RULEBOOK.md is the source for tabletop-compatible game rules as they are specified.

Agents may improve its organization and add explicitly requested rules, but must preserve unresolved sections as unresolved.

Never fill a blank section using "standard RPG rules."

### 10. Prefer reversible architecture

At this stage:
- keep dependencies minimal;
- avoid premature frameworks;
- avoid deep inheritance trees;
- avoid hard-coded canon;
- keep content separate from engine plumbing;
- make changes easy to replace after later design decisions.

When uncertain, choose the smaller implementation.
