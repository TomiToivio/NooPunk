# NoöPunk Rulebook

> **Status:** foundation / intentionally incomplete.
>
> This document will become the shared rules reference for both the NoöPunk tabletop RPG and the Godot computer RPG. Undefined sections are reserved for later author specification. Do not fill them automatically from genre conventions or other RPG systems.

## 1. Design goal

NoöPunk is designed as one rules model with two implementations:

- **Tabletop RPG:** human-readable rules usable with players, a game master, character sheets, and ordinary tabletop procedures.
- **Godot RPG:** the same concepts represented in software and data.

Where practical, canonical game rules should remain independent of Godot-specific UI, scenes, animation, rendering, or input code.

## 2. Genre premise

**NoöPunk = Noösphere + Cyberpunk.**

The setting explores a cyberpunk technological and social transformation together with speculative paradigm shifts involving consciousness, psionics, non-human intelligence, and the emergence of a Noösphere.

The detailed setting is not defined in this document yet. See README.md and TIMELINE.md for the current high-level framing.

## 3. Time convention

Future dates are written as **20XX** unless explicitly specified otherwise.

The setting is approximately a 2045-like future extrapolated from 2026, without committing the fiction to an exact canonical year.

## 4. Core resolution system

**UNSPECIFIED.**

To be defined by the author.

This section will later establish:
- dice / randomization model
- tests and difficulty
- opposed actions
- success and failure
- degrees of outcome, if any
- modifiers and situational rules

No default system is implied.

## 5. Characters

**UNSPECIFIED.**

### 5.1 Attributes
Reserved for later specification.

### 5.2 Skills
Reserved for later specification.

### 5.3 Derived statistics
Reserved for later specification.

### 5.4 Character creation
Reserved for later specification.

### 5.5 Advancement
Reserved for later specification.

## 6. Human, cyborg and AI characters

**UNSPECIFIED.**

The setting includes AI and cyborgification at the premise level, but playable categories, capabilities, limitations, embodiment, identity rules, and mechanical differences have not yet been defined.

## 7. Psionics and consciousness

**UNSPECIFIED.**

The setting premise may include scientifically validated psionic phenomena and consciousness-related technologies, but no powers, schools, ratings, costs, risks, procedures, or metaphysical mechanics are defined yet.

## 8. Non-Human Intelligence

**UNSPECIFIED.**

NHI exists at the scenario level, but taxonomy, origins, forms, motivations, capabilities, game statistics, and player interaction rules are reserved for later worldbuilding.

## 9. Cybernetics and augmentation

**UNSPECIFIED.**

No cyberware catalog, augmentation economy, body-slot system, humanity cost, compatibility system, or other mechanics are currently canonical.

## 10. Combat

**UNSPECIFIED.**

Reserved for later specification, including:
- initiative
- actions
- attacks and defense
- damage
- armor
- injury / wounds
- recovery
- ranged combat
- close combat

## 11. Social interaction

**UNSPECIFIED.**

Reserved for later specification.

## 12. Networks, hacking and AI systems

**UNSPECIFIED.**

Reserved for later specification.

## 13. Equipment and economy

**UNSPECIFIED.**

Reserved for later specification.

## 14. Vehicles and mobility

**UNSPECIFIED.**

Reserved for later specification.

## 15. World building

**AUTHOR-DEFINED LATER.**

This section will eventually contain or link to canonical material concerning:
- places
- institutions
- factions
- cultures
- corporations
- states and political entities
- technologies
- everyday life
- media
- economy
- conflicts
- NHI
- the Noösphere

Agents must not populate these categories without explicit author instruction.

## 16. Simulation layer

**UNSPECIFIED.**

NoöPunk is also intended as a simulation of interacting social and technological paradigm shifts. The simulation should eventually be compatible with the RPG's conceptual world model, but simulation entities, variables, causal rules, agent behavior, and calibration are not yet defined.

## 17. Runtime implementation contract

The Godot and Concordia implementations should eventually map the same author-defined rules into engine-independent data and logic.

The three supported forms are:

- tabletop RPG
- Godot RPG
- Concordia RPG / simulation

Runtime-specific adapters may differ, but they must not redefine canonical rules.

Initial implementations may create placeholders for:
- rule data
- character data
- world data
- simulation data
- serialization
- Godot UI / scene adapters
- Concordia GM / agent / human-player adapters
- LLM provider configuration

These placeholders must remain semantically empty until the corresponding rules are specified.

## 18. Canon and change control

A rule becomes canonical only when explicitly specified by the author or incorporated into this rulebook through an author-approved task.

Examples, prototypes, test values, genre conventions, and temporary implementation details are **not canon**.

When software needs a value before the rule exists, use a clearly marked temporary fixture that cannot be mistaken for a design decision.

## 19. Future design sections

The following are intentionally waiting for separate design steps:

- core mechanic
- attributes
- skills
- character creation
- combat
- psionics
- NHI
- cybernetics
- AI
- hacking / networks
- social interaction
- equipment
- advancement
- world building
- factions
- simulation model

This list is a roadmap of questions, not a specification.
