# NoöPunk Rulebook

> **Status:** foundation / intentionally incomplete.
>
> This document is the shared human-readable rules reference for the NoöPunk tabletop, Godot, and Concordia runtimes. Undefined sections are reserved for later author specification. Do not fill them automatically from genre conventions or other RPG systems.

## 1. Design goal

NoöPunk is one RPG rules model with three runtimes:

- **Tabletop RPG:** human-readable rules usable with players, a game master, character sheets, and ordinary tabletop procedures.
- **Godot RPG:** the same concepts represented in software and data.
- **Concordia RPG / simulation:** the same canonical mechanics exposed to deterministic simulation logic and LLM agents.

Where practical, canonical game rules remain independent of runtime-specific UI, scenes, prompts, animation, rendering, or input code.

## 2. Genre premise

**NoöPunk = Noösphere + Cyberpunk.**

The setting explores a cyberpunk technological and social transformation together with speculative paradigm shifts involving consciousness, psionics, non-human intelligence, and the emergence of a Noösphere.

The detailed setting is not defined in this document yet. See README.md and TIMELINE.md for the current high-level framing.

## 3. Time convention

Future dates are written as **20XX** unless explicitly specified otherwise.

The setting is approximately a 2045-like future extrapolated from 2026, without committing the fiction to an exact canonical year.

## 4. Core resolution system

The basic NoöPunk check is:

~~~text
3d6 + relevant attribute modifier + skill/advantage/disadvantage/cybernetic/situational modifiers
~~~

Compare the final total against a difficulty rating. A check succeeds when the final total **meets or exceeds** the target.

| Difficulty | Target | Meaning |
|---|---:|---|
| Easiest | 3 | Can only fail with negative modifiers. |
| Easier | 6 | Trivial for a capable character. |
| Easy | 9 | Routine. |
| Normal | 12 | The default challenge. |
| Hard | 15 | Demanding. |
| Impossible | 18 | The hardest target, resolved with the same formula. |

> **These labels supersede an earlier table.** In the previous version target 12 was
> named **Hard** and targets 15/18 were named **Harder/Hardest**. Under the
> author-specified table above, target 12 is **Normal**, the label **Hard** now means
> **15**, and **Harder/Hardest are no longer canonical names**.
>
> **Migration warning.** The string `Hard` has changed target from **12 to 15**. Any
> stored or external data that recorded the *label* rather than the number must be
> migrated deliberately. Neither rulebook nor runtimes may silently reinterpret an old
> `Hard` as 15; a saved artifact carrying `"Hard": 12` should be treated as an old
> **Normal**. The difficulty data is versioned in `data/rules/core.json`.

**"Impossible" is a name, not a prohibition.** It is the author's name for target 18
and is resolved with the same numeric formula as every other target. There is **no
automatic failure on a natural 3** and **no automatic success on a natural 18**.

Additional modifiers may later come from skills, advantages, disadvantages, cybernetics, equipment, conditions, circumstances, or other author-defined systems. Positive and negative contributions are summed; no values, catalogs or progression systems are defined here.

### 4.1 Opposed checks

For opposed actions, each side rolls:

~~~text
3d6 + attribute modifier + other applicable modifiers
~~~

The side with the higher final total wins.

If the final totals are tied, the result is explicitly unresolved. No tie-breaker rule is currently canonical.

### 4.2 Unskilled and trained-only checks

Skill use has two representable categories:

1. **Unskilled attempt allowed:** the action may be attempted without the skill, with an additional **-1 unskilled modifier**.
2. **Trained-only:** the action cannot be attempted without the required skill.

Which future skills use which category is not yet specified.

## 5. Characters

Most character systems remain unspecified. The six canonical attributes and ordinary-human attribute generation are now defined.

### 5.1 Attributes

The canonical attributes are:

- **Fitness (FIT):** your health, fitness, stamina, physical robustness, and constitution.
- **Reflexes (REF):** your dexterity, agility, coordination, reaction speed, and bodily precision.
- **Intelligence (INT):** how smart, educated, knowledgeable, analytical, and generally intellectually capable you are.
- **Charisma (CHA):** your social skills, attractiveness, presence, persuasion, and leadership ability.
- **Cybernetics (CYB):** your cyborg / technological side: technical aptitude, proficiency in cyberspace, programming, cybernetics, and related human-machine capabilities.
- **Psyche (PSY):** your consciousness, intuition, empathy, and psionic aptitude. PSY is used for consciousness-related and psionic actions, including astral projection when those systems are later defined.

Do not add alternate names or additional attributes without author specification.

### 5.2 Human attribute generation

For an ordinary human character, roll **3d6 independently for each of the six attributes**.

Convert each raw 3d6 result into an attribute modifier:

| 3d6 roll | Modifier |
|---|---:|
| 3 | -3 |
| 4-5 | -2 |
| 6-8 | -1 |
| 9-12 | 0 |
| 13-15 | +1 |
| 16-17 | +2 |
| 18 | +3 |

Interpretation:

- +3 is approximately the normal upper human limit.
- Values above +3 are transhuman / superhuman.
- Values below -3 represent an effectively nonfunctional or near-dead state.

These refer to **attribute modifiers**, not raw generation rolls. The data model must permit values outside the ordinary-human -3..+3 range, and explicitly assigned values are used as-is without clamping. This interpretation defines **no** death, injury, augmentation or resurrection mechanics; those remain reserved for later author specification.

Where useful, preserve both the raw 3d6 generation roll and the resulting modifier.

### 5.3 Skills

**UNSPECIFIED.**

No skill list, skill ratings, or skill progression rules are currently canonical. Only the unskilled/trained-only distinction in section 4.2 is defined.

### 5.4 Derived statistics

**UNSPECIFIED.**

### 5.5 Character creation

Only ordinary-human attribute generation in section 5.2 is currently defined. All other character-creation procedures are reserved for later specification.

### 5.6 Advancement

**UNSPECIFIED.**

## 6. Human, cyborg and AI characters

**UNSPECIFIED beyond the shared attribute container.**

The model permits attribute values outside ordinary-human limits, but playable categories, capabilities, limitations, embodiment, identity rules, and mechanical differences have not yet been defined.

## 7. Psionics and consciousness

**UNSPECIFIED beyond PSY as the governing attribute for future consciousness-related and psionic actions.**

No powers, schools, ratings, costs, risks, procedures, or metaphysical mechanics are defined yet.

## 8. Non-Human Intelligence

**UNSPECIFIED.**

NHI exists at the scenario level, but taxonomy, origins, forms, motivations, capabilities, game statistics, and player interaction rules are reserved for later worldbuilding.

## 9. Cybernetics and augmentation

**UNSPECIFIED beyond CYB as the canonical cybernetic/technical attribute.**

No cyberware catalog, augmentation economy, body-slot system, humanity cost, compatibility system, hacking subsystem, or attribute-modification rules are currently canonical.

## 10. Combat

**UNSPECIFIED.**

Reserved for later specification, including initiative, actions, attacks and defense, damage, armor, injury / wounds, recovery, ranged combat, and close combat.

## 11. Social interaction

**UNSPECIFIED beyond CHA as the relevant social attribute where appropriate.**

No detailed social subsystem is canonical yet.

## 12. Networks, hacking and AI systems

**UNSPECIFIED.**

CYB may be the relevant attribute for future technical, programming, cyberspace, cybernetics, or hacking actions, but no hacking or network subsystem is defined.

## 13. Equipment and economy

**UNSPECIFIED.**

## 14. Vehicles and mobility

**UNSPECIFIED.**

## 15. World building

**AUTHOR-DEFINED LATER.**

Agents must not populate missing setting categories without explicit author instruction.

## 16. Simulation layer

**UNSPECIFIED beyond use of the same deterministic rules model.**

Concordia may reason about context and describe outcomes, but dice, attribute values, numeric modifiers, and canonical mechanical resolution belong in code when deterministic game logic is available.

## 17. Runtime implementation contract

The three supported forms are tabletop RPG, Godot RPG, and Concordia RPG / simulation.

They use the same canonical attribute identifiers, human-generation table, difficulty targets, check semantics, unskilled penalty, trained-only representation, and opposed-check semantics.

Runtime-specific adapters may differ, but they must not redefine canonical rules.

## 18. Canon and change control

A rule becomes canonical only when explicitly specified by the author or incorporated into this rulebook through an author-approved task.

Examples, prototypes, test values, genre conventions, and temporary implementation details are **not canon**.

## 19. Future design sections

The following remain intentionally unresolved:

- skill list and skill progression
- derived statistics
- detailed character creation beyond ordinary-human attributes
- combat
- health / hit points / wounds
- initiative
- damage and armor
- advancement / XP
- cyberware rules and catalog
- hacking rules
- psionic powers
- astral projection mechanics beyond PSY being its future governing attribute
- detailed social subsystem mechanics
- AI / NHI mechanical differences
- transhuman augmentation rules
- opposed-check tie-breakers
- equipment and economy
- world building
- factions
- simulation model

This list is a roadmap of questions, not a specification.
