# AGENTS.md

## NoöPunk agent rules

These rules are mandatory for coding and documentation agents working in this repository.

**Design invariants.** NoöPunk has three core design balances, documented once in
[`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md). They are project-level
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

A base RPG scaffold is not permission to create a game system.

### 3. Tabletop first; Godot and Concordia are later ports

The **tabletop RPG rules/worldbook are the canonical design source** for NoöPunk.

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

The six attributes (FIT, REF, INT, CHA, CYB, PSY), ordinary-human 3d6 attribute generation, the CWN-derived **2d6 skill-check engine**, CWN-style skill-check difficulties, opposed skill checks with player-character tie priority, unskilled -1 / trained-only blocking, the skill list, and the level-0..4 trained skill scale are now author-specified in RULEBOOK.md. Agents must preserve them exactly.

**The current skill list, level-0..4 scale, and 2d6 skill-check engine are tabletop-first.** The existing digital runtime still contains the superseded 3d6 check engine and old difficulty ladder. Treat that as explicit porting debt, not as competing canon. Do not partially port #25 into one runtime; a later task must derive the shared digital specification and update Godot and Concordia consistently.

The earlier issue #17 BCI / Compute / Connection / Infosec cyberspace modifier framework is **withdrawn from active canon**. Do not port it. Hacking / cyberspace is DEFERRED until a later CWN-based subsystem review.

Until explicitly specified, do not define:
- additional attributes or derived statistics
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


### 11. One RPG, three runtimes, developed in sequence

NoöPunk is one RPG rules/world model intended to run in three forms:

- tabletop RPG
- Godot RPG
- Concordia RPG / simulation

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

NoöPunk's canonical design invariants are documented once in [`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md). Every contributing agent must preserve them:

1. Preserve the **Gamism / Narrativism / Simulationism balance**.
2. Use **CY_BORG** (Gamism), **Cyberpunk 2020** (Simulationism), and **The Sprawl** (Narrativism) as the canonical reference poles.
3. Preserve **rules/mechanics parity** between Tabletop, Godot and Concordia wherever possible, while developing them in the order **Tabletop → Godot/Concordia** rather than in parallel.
4. Allow scenarios and medium-specific presentation to diverge.
5. Preserve the **Cyberpunk / Noösphere balance**.
6. Treat **UFO Disclosure, Psionics and Panpsychism** as the defining Noösphere paradigm shifts.
7. Treat **Shadowrun** and **Eclipse Phase** as comparative influences, not templates to copy.
8. Do not silently redesign these balances. If an implementation requires a departure, document the reason explicitly.
9. Treat the **Cities Without Number SRD** as the open mechanical chassis (see §15), reviewed and modified **subsystem by subsystem**, with existing NoöPunk author decisions taking precedence over CWN defaults.

Practical consequences:

- Prefer noösphere content that stays science-fictional, philosophical and speculative; do not let it become generic fantasy magic.
- Do not let one creative agenda become the default that overwhelms the other two, and do not add mechanics that only serve one of them.
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

### 15. Cities Without Number SRD is the open chassis

NoöPunk's main open mechanical starting point is the **Cities Without Number SRD**, documented once in [`docs/CWN_CHASSIS.md`](docs/CWN_CHASSIS.md). NoöPunk is **not** a CWN clone: it starts from that SRD and then modifies the system **subsystem by subsystem**.

When working on any subsystem that CWN also has:

1. review the CWN SRD version of it;
2. decide explicitly: **KEEP**, **MODIFY**, **REPLACE**, **OMIT**, or **DEFER**;
3. when the decision is missing, leave it **DEFER** — do not assume CWN's version survives, and do not assume it is dropped.

**NoöPunk decisions take precedence.** Existing author-specified NoöPunk rules are canonical and are not overridden by CWN defaults, and **do not redesign them back toward CWN**: the six attributes (FIT, REF, INT, CHA, CYB, PSY), 3d6 ordinary-human **attribute generation**, the −3..+3 ordinary-human modifier range, the CWN-derived **2d6 skill-check engine**, CWN-style skill-check difficulties, and the skill list and level-0..4 trained skill scale are all NoöPunk's own. Do not restore the superseded 3d6 skill-check engine or old difficulty ladder.

Where CWN is the starting point for a subsystem, NoöPunk's modification of it is the rule. The skills subsystem is **MODIFY**: NoöPunk adopts the CWN level-0..4 structure and standard list, but unskilled stays outside the numbered levels (at -1 or blocked), Heal is renamed **Medical**, Know is renamed **Science**, and specialization is deferred. The core skill-check subsystem is also **MODIFY**: NoöPunk adopts CWN's 2d6 + skill + attribute structure and difficulty ladder while retaining NoöPunk's six attributes and wider -3..+3 ordinary-human attribute range.

**Source boundary.** Direct reuse is limited to material actually present in the Cities Without Number **SRD**. Do not import setting material, megacorps, NPCs, places, or events from the full CWN book. Do not copy protected text, setting material, terminology, or faction content from Cyberpunk 2020, Eclipse Phase, Shadowrun, The Sprawl, or CY_BORG: those are **design references only**. When unsure whether something is in the SRD, treat it as not in the SRD and write original wording.

Adopting the chassis is a **policy and roadmap**, not a conversion. Do not mass-port CWN mechanics, and do not advance Godot or Concordia ahead of the tabletop rules.

Subsystem decisions belong to the author. A DEFER is an open question, not permission for an agent to choose.
