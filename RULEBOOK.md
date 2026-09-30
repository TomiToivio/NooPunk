# NoöPunk Rulebook

> **Status:** foundation / intentionally incomplete.
>
> This document is the **canonical design source for NoöPunk game rules**. The tabletop RPG is designed and stabilized here first; Godot and Concordia are later ports of stable tabletop systems. Undefined sections are reserved for later author specification. Do not fill them automatically from genre conventions or other RPG systems.

## 1. Design goal

NoöPunk is one RPG rules model with three runtimes, developed **tabletop first**:

- **Tabletop RPG:** human-readable rules usable with players, a game master, character sheets, and ordinary tabletop procedures.
- **Godot RPG:** the same concepts represented in software and data.
- **Concordia RPG / simulation:** the same canonical mechanics exposed to deterministic simulation logic and LLM agents.

Where practical, canonical game rules remain independent of runtime-specific UI, scenes, prompts, animation, rendering, or input code.

The development sequence is:

1. define the tabletop rule in human-readable form;
2. make it coherent and playable at the table;
3. resolve important ambiguities and edge cases;
4. derive a digital specification;
5. port that specification to Godot and Concordia.

If software exposes an unclear rule, the correction belongs here first.

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
3d6 + relevant attribute modifier + skill modifier + other applicable modifiers
~~~

Compare the final total against a difficulty rating. A check succeeds when the final total **meets or exceeds** the target.

| Difficulty | Target |
|---|---:|
| Easiest | 3 |
| Easier | 6 |
| Easy | 9 |
| Normal | 12 |
| Hard | 15 |
| Impossible | 18 |

Additional modifiers may later come from advantages, disadvantages, cybernetics, equipment, conditions, circumstances, or other author-defined systems. Positive and negative modifiers are summed normally.

The **skill modifier** is determined by the character's skill level — see section 4.3. Skill levels are now canonical; the *list* of which skills exist is not (section 5.3).

"Impossible" is the canonical name for target 18. It is still a numeric difficulty, not a prohibition on attempting the check. There is no automatic failure on a natural 3 and no automatic success on a natural 18.

These names supersede the earlier labels `Hard = 12`, `Harder = 15`, and `Hardest = 18`. The current mapping is `Normal = 12`, `Hard = 15`, and `Impossible = 18`. At the time of this rename there was no canonical save-data schema or runtime caller persisting the old difficulty names, so no legacy aliases are retained. In particular, old `Hard` must not silently continue to mean target 12.

### 4.1 Opposed checks

For opposed actions, each side rolls:

~~~text
3d6 + attribute modifier + other applicable modifiers
~~~

The side with the higher final total wins.

If the final totals are tied, the result is explicitly unresolved. No tie-breaker rule is currently canonical.

### 4.3 Skill levels

Skill competence has exactly **four** levels:

| Level | Name | Modifier | Meaning |
|---:|---|---:|---|
| 0 | Unskilled | special | The character does **not have** the skill. See the two cases below. |
| 1 | Basic | +1 | Basic competence in the skill. |
| 2 | Advanced | +2 | Advanced competence in the skill. |
| 3 | Expert | +3 | Expert competence in the skill. |

**Level 0 means no skill.** It is not a low grade of trained competence, and it does not mean "beginner" — the character simply does not possess the skill. Levels 1–3 contribute their listed positive modifier to the check.

These are the only ordinary skill levels. No further ordinary levels are canonical, and no skill catalog, rating scale, or progression rule is defined here (section 5.3).

Interaction with the check formula:

~~~text
total = 3d6 + relevant attribute modifier + skill modifier + other applicable modifiers
~~~

- level 1 → **+1**
- level 2 → **+2**
- level 3 → **+3**
- level 0 → either **-1** (if unskilled use is allowed) or **blocked** (if the skill is required)

### 4.4 Unskilled and trained-only checks

Level 0 has two distinct cases. Which case applies is a property of the *action*, not of the character:

1. **Unskilled attempt allowed:** a character at level 0 may attempt the action, with an additional **-1 unskilled modifier**. The penalty is applied **exactly once**.
2. **Skill required / trained-only:** a character at level 0 cannot attempt the action. This is a **blocked attempt**, not a failed roll. No dice are rolled and additional modifiers cannot bypass the requirement.

The -1 is the level-0 contribution to the check formula, so it is not added on top of a skill modifier — a level-0 character has no skill modifier, only this penalty or a block.

Which skills and actions use which category is **not yet specified** (section 5.3).

### 4.5 Worked checks

These examples are normative examples of the same check formula used by Tabletop, Godot, and Concordia:

- **Easiest, no modifiers:** a raw check roll of 3 against target 3 totals 3 and succeeds.
- **Easiest, -1 modifier:** a raw check roll of 3 with a -1 modifier totals 2 and fails.
- **Impossible:** a raw check roll of 18 with no modifiers against target 18 totals 18 and succeeds. "Impossible" therefore does not mean "unrollable."
- **Unskilled allowed:** a raw check roll of 10 with no attribute modifier and the -1 unskilled modifier totals 9, succeeding against Easy (9). The unskilled penalty is applied exactly once.

Skill levels in the same formula:

- **Basic (level 1):** a raw check roll of 10 with no attribute modifier and a +1 skill modifier totals 11, failing against Normal (12) and succeeding against Easy (9).
- **Advanced (level 2):** the same roll with +2 totals 12, succeeding against Normal (12) on the boundary.
- **Expert (level 3):** the same roll with +3 totals 13, succeeding against Normal (12).
- **Unskilled (level 0), unskilled use allowed:** the same roll with the -1 unskilled modifier totals 9, failing against Normal (12).
- **Unskilled (level 0), skill required:** the attempt is blocked. No dice are rolled, there is no total, and no combination of modifiers permits the attempt.

The level-1/2/3 examples differ from each other by exactly the skill modifier, which is the property that makes the four levels a ladder of competence rather than a second attribute.

## 5. Characters

Most character systems remain unspecified. The six canonical attributes and ordinary-human attribute generation are now defined.

### 5.1 Attributes

The canonical attributes are:

- **Fitness (FIT):** your health, fitness and constitution.
- **Reflexes (REF):** your dexterity, agility and coordination.
- **Intelligence (INT):** how smart, educated and knowledgeable you are.
- **Charisma (CHA):** your social skills, attractiveness and leadership skills.
- **Cybernetics (CYB):** your cyborg side; how technical you are; your proficiency in cyberspace, programming and cybernetics.
- **Psyche (PSY):** your consciousness, intuition, empathy and psionics. Used in astral projection and for psionics.

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

- +3 is the ordinary human upper end represented by this generation table.
- Values above +3 are **transhuman**.
- Values below -3 are **basically dead**.

These statements describe attribute modifiers, not raw 3d6 generation rolls. They do not define any additional death, injury, augmentation, resurrection, or recovery mechanic.

The data model must permit values outside the ordinary-human -3..+3 range. Future transhumans, AI entities, NHI, cybernetic beings, injuries, or other cases may use explicitly assigned values when their rules are later defined.

Where useful, preserve both the raw 3d6 generation roll and the resulting modifier.

### 5.3 Skills

**Skill levels are canonical; the skill list is not.**

The four canonical skill levels are defined in section 4.3: 0 Unskilled, 1 Basic (+1), 2 Advanced (+2), 3 Expert (+3).

Still **UNSPECIFIED**:

- the skill list — which skills exist;
- which skills are unskilled-allowed versus skill-required;
- any skill's governing attribute;
- skill progression, XP costs, training time, specialties, prerequisites, skill groups, or defaulting chains;
- any skill ratings beyond the four levels above.

The four levels are a *scale*. A character's sheet has a level per skill; what skills the character may have is not yet defined.

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

The three supported forms are tabletop RPG, Godot RPG, and Concordia RPG / simulation. The tabletop form is the canonical first implementation and design authority; digital runtimes follow after the relevant tabletop system is stable enough to port.

They use the same canonical attribute identifiers, human-generation table, difficulty targets, check semantics, skill levels and their modifiers, unskilled penalty, trained-only representation, and opposed-check semantics.

Runtime-specific adapters may differ, but they must not redefine canonical rules.

**Digital skill-level implementation is deferred.** Skill levels are canonical in the tabletop rules (sections 4.3–4.4) but are **not** implemented in Godot or Concordia by this rulebook change, and `data/rules/core.json` does not yet carry a skill-level table. Porting them is a separate, later task once the tabletop rule is stable; a digital runtime must not invent a skill-level representation of its own in the meantime.

## 18. Canon and change control

A rule becomes canonical only when explicitly specified by the author or incorporated into this rulebook through an author-approved task.

Examples, prototypes, test values, genre conventions, and temporary implementation details are **not canon**.

## 19. Future design sections

The following remain intentionally unresolved:

- skill list (which skills exist), and which of them are unskilled-allowed vs skill-required
- skill progression / training / advancement mechanics (the four skill *levels* are canonical; how a character reaches them is not)
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
