# AGENTS.md

## NoöPunk agent rules

These rules are mandatory for coding and documentation agents working in this repository.

**Design invariants.** NoöPunk has three core design balances, documented once in
[`docs/archive/DESIGN_PRINCIPLES.md`](docs/archive/DESIGN_PRINCIPLES.md). They are project-level
invariants and are restated as binding rules in §13 below. Read that document
before changing rules, mechanics, or setting material.

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

The RPG scaffold and the reserved-area list are not permission to create a game system.

### 3. Tabletop first; Godot and Concordia are later ports

NoöPunk is **one computer RPG/simulation**, not separate tabletop, simulation and
videogame products ([`docs/archive/NOOPUNK_AS_ONE_GAME.md`](docs/archive/NOOPUNK_AS_ONE_GAME.md),
#48). The tabletop / Godot / Concordia distinction in this section is about notation
and runtime sequence, not about maintaining three products.

The **tabletop-style RPG rules/worldbook are the canonical design source** for NoöPunk.

Development order is binding:

1. define and refine the tabletop rule or world concept;
2. stabilize it through documentation and playtestable procedures;
3. only then convert it into a digital specification;
4. implement that specification in Godot and Concordia.

If a mechanic is unclear, incomplete, or internally inconsistent, fix the tabletop rule first. Do not let Godot, Concordia, UI code, prompts, or platform architecture accidentally invent the missing rule.

The intended RPG rules must ultimately be usable in tabletop, Godot, and Concordia. Game logic should therefore remain data-driven and engine-independent where practical.

Do not bury canonical rules inside scene scripts or UI code. Prefer separable domain data / rule definitions derived from RULEBOOK.md and the worldbook material.

Existing Godot and Concordia scaffolds must be preserved, not deleted, but they are later-stage implementation material until the relevant tabletop systems are stable.

### 4. Current reserved design areas

Issue #51 explicitly revises the earlier six-attribute reservation. The canonical character direction is now a **four-system unified tag model**: Physical / Social / Psychic / Cybernetic, with attributes represented as typed attribute tags rather than a separate subsystem. Ordinary-human attribute-tag values use the -3..+3 band, but the final attribute names/counts and generation procedure are not yet locked. The old FIT / REF / INT / CHA / CYB / PSY model and its 3d6 generator remain in the digital runtime only as documented porting debt.

The current provisional **2d6 skill-check engine**, its difficulty ladder, opposed skill checks with player-character tie priority, unskilled -1 / trained-only blocking, the skill list, and the level-0..4 trained skill scale remain author-specified in RULEBOOK.md for now. Agents must preserve them until the author explicitly revises them.

**The current skill list, level-0..4 scale, and 2d6 skill-check engine are tabletop-first.** The existing digital runtime still contains the superseded 3d6 check engine and old difficulty ladder. Treat that as explicit porting debt, not as competing canon. Do not partially port #25 into one runtime; a later task must derive the shared digital specification and update Godot and Concordia consistently.

The earlier issue #17 BCI / Compute / Connection / Infosec cyberspace modifier framework is **withdrawn from active canon**. Do not port it. Hacking / cyberspace is DEFERRED until the author defines an original NoöPunk subsystem.

Until explicitly specified, do not define:
- final attribute names/counts inside the four systems, or derived statistics
- additional skills, or a rename/split/merge of the ones in RULEBOOK.md §5.3
- which skills are unskilled-allowed versus trained-only
- skill specialties or the mechanism by which a broad skill is narrowed (the profession mechanism in particular is deferred)
- how many skills a starting character has, or at what levels
- skill-to-attribute bindings (checks use the attribute relevant to the action)
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
- hacking / cyberspace mechanics, including whether the withdrawn BCI / Compute / Connection / Infosec concepts return
- vehicles
- magic or supernatural systems
- detailed simulation mechanics

These may be represented only by clearly empty extension points when needed by the requested architecture.

### 5. Setting constraints

Treat NoöPunk as an **alternate Eclipse Phase timeline set before the Fall**, combining Noösphere + Cyberpunk inside that transhuman setting.

Canonical anchors are: **20XX**, **Earth still exists**, **the Fall has not happened**, and **the technology level is broadly Eclipse Phase-level**.

The cyberpunk layer remains technological, political, economic, and social cyberpunk. Do not convert it into fantasy.

The speculative consciousness / NHI layer draws inspiration from sources identified by the author, including Teilhard de Chardin, Alexander Wendt, Jacques Vallée, Dean Radin, Federico Faggin, and Donald Hoffman.

Do not present speculative setting assumptions as established real-world scientific facts.

### 6. Time convention

Canonical future dates are written as **20XX** unless the author explicitly says otherwise.

The world is approximately a 2045-like extrapolation from the 2026 situation, but agents must not assign exact future dates on their own.

### 7. Retrocyberpunk tone is not a license to add lore

Recognized influences include old-school Cyberpunk, Shadowrun, Philip K. Dick, Hawkwind, and 1970s space psychedelia.

Those remain tonal/comparative references. **Eclipse Phase is different:** it is now the licensed parent continuity, technology baseline, and EP2 mechanical foundation for NoöPunk. Use EP material only within the applicable licensing and attribution boundaries, and document timeline divergences rather than renaming concepts merely to appear original.

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


### 11. One RPG, three runtimes, developed in sequence

NoöPunk is one RPG rules/world model. It is developed as **one computer
RPG/simulation**, and the three headings below are notation/runtime choices within
that single game rather than three products to maintain
([`docs/archive/NOOPUNK_AS_ONE_GAME.md`](docs/archive/NOOPUNK_AS_ONE_GAME.md), #48):

- tabletop-style notation — how the rules are written and read
- Concordia — the generative-agent / Game Master runtime
- Godot — a possible *future* frontend, not a planned parallel runtime

These are implementations of the same game, not separate rule systems, but they are **not developed in parallel by default**. The tabletop version comes first and acts as the executable human specification. Godot and Concordia follow as staged conversions after the relevant tabletop systems are stable.

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

### 13. Preserve the three design balances

NoöPunk's canonical design invariants are documented once in [`docs/archive/DESIGN_PRINCIPLES.md`](docs/archive/DESIGN_PRINCIPLES.md). Every contributing agent must preserve them:

1. Preserve the **Gamism / Narrativism / Simulationism balance**, with issue #51's current priority: **Narrativist experience + Simulationist world + Gamist friction**.
2. Use **CY_BORG** (Gamism), **Cyberpunk 2020** (Simulationism), and **The Sprawl** (Narrativism) as the canonical reference poles; use **The Veil** as a complementary Narrativist reference.
3. Preserve **rules/mechanics parity** between Tabletop, Godot and Concordia wherever possible, while developing them in the order **Tabletop → Godot/Concordia** rather than in parallel.
4. Allow scenarios and medium-specific presentation to diverge.
5. Preserve the **Cyberpunk / Noösphere balance**.
6. Treat **UFO Disclosure, Psionics and Panpsychism** as the defining Noösphere paradigm shifts.
7. Treat **Shadowrun** as a comparative influence. Treat **Eclipse Phase** as the licensed parent continuity / technology baseline / EP2 rules foundation, subject to provenance and attribution.
8. Do not silently redesign these balances. If an implementation requires a departure, document the reason explicitly.
9. Treat **EP2 as the current mechanical chassis**. NoöPunk may simplify or replace subsystems deliberately, but agents must not revert the project to an original-rules-only premise unless the author explicitly changes direction again.

Practical consequences:

- Prefer noösphere content that stays science-fictional, philosophical and speculative; do not let it become generic fantasy magic.
- Do not collapse the game into a single creative agenda. Narrativism is the foreground experience, Simulationism supplies persistent causal grounding, and Gamism supplies pressure and consequential choice.
- A scenario, mission, map, or presentation difference between Tabletop, Godot and Concordia is expected and permitted. A **rules** difference is a defect: extract a shared specification rather than fork the rule.
- Where a shared specification already exists (for example `data/rules/core.json` over `src/rules/core.py`), consume it rather than re-declaring the same values in a second runtime.

`tests/test_design_principles.py` fails the build if these invariants, the canonical document, or the documents that reference it drift out of agreement.


### 14. Tabletop-first porting gate

Before implementing or extending a substantive Godot or Concordia gameplay system, agents must check:

1. Is the mechanic or world concept explicitly defined in the tabletop rules/worldbook?
2. Is its terminology and procedure coherent enough to play without software?
3. Are important edge cases documented or consciously left unresolved?
4. If not, stop at the tabletop layer and improve that source first.
5. If yes, convert it as **tabletop rule → digital specification → Godot implementation → Concordia implementation**.

Platform-specific differences must be documented as adaptations. They must not silently become new canonical rules.

Scenarios, UI, pacing, maps, presentation, automation, and other medium-specific features may diverge where appropriate. Core rules, mechanics, terminology, and world canon should not.

### 15. Eclipse Phase 2E chassis and alternate-timeline rule

**Eclipse Phase 2E is the current mechanical chassis and Eclipse Phase is the parent continuity.**

When adding or revising mechanics:

1. begin from the current author direction in issue #60 and `RULEBOOK.md`;
2. preserve EP2 mechanics and terminology when they work, rather than replacing them for originality's sake;
3. simplify or modify subsystems only when NoöPunk or Concordia has a clear reason;
4. connect NoöPunk additions to the project's theoretical sources where appropriate;
5. record whether material is EP-derived, modified EP, or NoöPunk-native, including licensing/provenance;
6. keep unresolved systems unresolved rather than inventing unsupported canon.

Setting work must preserve the anchors **20XX / pre-Fall / Earth intact / Eclipse Phase technology level** unless the author explicitly revises them.
