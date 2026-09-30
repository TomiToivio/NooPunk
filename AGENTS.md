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

The six attributes (FIT, REF, INT, CHA, CYB, PSY), ordinary-human 3d6 generation, core 3d6 checks, canonical difficulties, opposed comparison, unskilled -1, and trained-only blocking are now author-specified in RULEBOOK.md and data/rules/core.json. Agents must preserve them exactly.

Until explicitly specified, do not define:
- additional attributes or derived statistics
- skills or a skill list
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


### 11. One RPG, three runtimes

NoöPunk is one RPG rules/world model intended to run in three forms:

- tabletop RPG
- Godot RPG
- Concordia RPG / simulation

These are implementations of the same game, not separate rule systems.

Concordia-specific agents must not invent alternate mechanics, lore, statistics, or canonical facts to make simulation easier. If a shared rule or world concept is undefined, leave it undefined or use clearly non-canonical fixtures.

Godot and Concordia may have different adapters and runtime plumbing, but canonical rules/data should remain shared or convertible wherever practical.

### 12. Concordia and Ollama constraints

When implementing the Concordia runtime:

- use Google DeepMind Concordia as the agent-based simulation/RPG framework;
- design for local Ollama-served LLMs for GM and NPC agents;
- allow an optional human-controlled player to participate alongside LLM agents;
- keep the LLM provider behind a replaceable adapter/configuration boundary;
- do not hard-code a particular Ollama model as canon unless the author specifies one;
- do not create NPC personalities, factions, plots, psionic abilities, skills, additional attributes, or world facts unless explicitly specified;
- use deterministic shared code for dice and numeric resolution when available; never ask the LLM to invent dice outcomes or canonical numeric mechanics;
- do not let prompts silently become canon;
- keep prompts/configuration separate from canonical RPG rules and world data;
- preserve the same tabletop ↔ Godot ↔ Concordia rule semantics wherever practical.

The first Concordia implementation should be infrastructure only: runnable simulation plumbing, agent/GM interfaces, Ollama connection boundaries, optional human input, and empty world/rule hooks. Do not advance into substantive simulation design without a separate author task.

### 13. The three design balances are invariants

NoöPunk holds three balances deliberately. They are project-level invariants, not loose inspirations, and agents must preserve them. The full canonical explanation lives in [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md) — treat it as the source of truth and do not restate its reasoning elsewhere.

**Creative agenda balance — Gamism / Narrativism / Simulationism**

- **Gamism:** CY_BORG — challenge, danger, meaningful choices, resource pressure, emergent problem solving, fast playable rules.
- **Simulationism:** Cyberpunk 2020 — coherent world rules, material consequences, cybernetics and technology that matter mechanically.
- **Narrativism:** The Sprawl — fiction-forward consequences, relationships and factions, failures and partial successes that change the situation.

Do not let one agenda become the default that overwhelms the others. Gamism does not mean combat-focused or optimization-heavy: hacking, psionics, infiltration, investigation, social engineering and exploration are all gamist challenge spaces.

**Implementation balance — Tabletop / Godot / Concordia**

Same world, same rules, same mechanics wherever possible. All three runtimes share rules, mechanics, character model, world model, setting canon, core systems and balance. **Scenarios, missions, maps, encounters, presentation, UI, pacing, procedural generation and medium-specific implementation details may and probably should diverge.** See rule 11 and rule 3. Where duplicate rule implementations exist, prefer extracting a shared specification so divergence becomes easier to detect.

**Genre balance — Cyberpunk / Noösphere**

Neither half may swallow the other. The cyberpunk side stays technological, political, economic and social. The Noösphere is the anomalous layer and is based specifically on three speculative paradigm shifts: **UFO / UAP Disclosure**, **Psionics**, and **Panpsychism**. The Noösphere must not become generic fantasy magic.

**Comparative influences, not templates**

**Shadowrun** and **Eclipse Phase** are the nearest structural neighbours — Shadowrun for mixing cyberpunk with an anomalous layer, Eclipse Phase where cyberpunk and anomalous/posthuman themes meet. They are comparative influences only. NoöPunk must not be presented as an Eclipse Phase homebrew, expansion or rules variant, or as a Shadowrun derivative, and no protected setting material, terminology, characters, factions, mechanics or text may be copied.

**Changing a balance**

Do not silently redesign any of these balances. If an implementation appears to require a departure, document the reason explicitly in the issue or document that forced it, and prefer a neutral placeholder or TODO over a quiet reinterpretation. Examples, prototypes, test fixtures and genre convention are not authority to change a balance.

### 14. Keep design guidance in one place

Do not duplicate the three balances across documents. `docs/DESIGN_PRINCIPLES.md` is the canonical explanation; other documents carry short references to it. If a balance's meaning needs to change, change it there and nowhere else. If an existing design-principles document already covers a topic, extend it rather than creating a competing source of truth.
