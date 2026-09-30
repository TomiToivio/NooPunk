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
total = 3d6 + relevant attribute modifier + skill modifier + other applicable modifiers
success = total >= difficulty target
~~~

A **3d6** roll is three six-sided dice summed, giving 3..18. The **skill
modifier** is the character's skill level modifier, defined in section 5.3; at
skill level 0 it is either the unskilled -1 or a blocked attempt, per section 4.2.
"Other applicable modifiers" are summed, whether positive or negative.

Compare the final total against a difficulty rating. A check succeeds when the final total **meets or exceeds** the target; a total one below the target fails.

| Difficulty | Target |
|---|---:|
| Easiest | 3 |
| Easier | 6 |
| Easy | 9 |
| Normal | 12 |
| Hard | 15 |
| Impossible | 18 |

Additional modifiers may later come from skills, advantages, disadvantages, cybernetics, equipment, conditions, circumstances, or other author-defined systems. Positive and negative modifiers are summed normally.

"Impossible" is the canonical name for target 18. It is still a numeric difficulty, not a prohibition on attempting the check. There is no automatic failure on a natural 3 and no automatic success on a natural 18.

These names supersede the earlier labels `Hard = 12`, `Harder = 15`, and `Hardest = 18`. The current mapping is `Normal = 12`, `Hard = 15`, and `Impossible = 18`. At the time of this rename there was no canonical save-data schema or runtime caller persisting the old difficulty names, so no legacy aliases are retained. In particular, old `Hard` must not silently continue to mean target 12.

### 4.1 Opposed checks

For opposed actions, each side rolls:

~~~text
3d6 + attribute modifier + other applicable modifiers
~~~

The side with the higher final total wins.

If the final totals are tied, the result is explicitly unresolved. No tie-breaker rule is currently canonical.

### 4.2 Unskilled and trained-only checks

Skill use has two representable categories. Both are the two cases of skill **level 0** (section 5.3):

1. **Unskilled attempt allowed:** the action may be attempted without the skill, with an additional **-1 unskilled modifier**, applied exactly once.
2. **Skill required / trained-only:** the action cannot be attempted without the required skill. This is a **blocked attempt**, not a failed roll. No dice are rolled and additional modifiers cannot bypass the requirement.

At skill levels 1–3 the character has the skill, so neither case applies; the
level's own **+1/+2/+3** modifier is used instead.

Which future skills use which category is not yet specified.

### 4.3 Worked checks

These examples are normative examples of the same check formula used by Tabletop, Godot, and Concordia:

- **Easiest, no modifiers:** a raw check roll of 3 against target 3 totals 3 and succeeds.
- **Easiest, -1 modifier:** a raw check roll of 3 with a -1 modifier totals 2 and fails.
- **Impossible:** a raw check roll of 18 with no modifiers against target 18 totals 18 and succeeds. "Impossible" therefore does not mean "unrollable."
- **Unskilled allowed:** a raw check roll of 10 with no attribute modifier and the -1 unskilled modifier totals 9, succeeding against Easy (9). The unskilled penalty is applied exactly once.
- **Basic skill (+1):** a raw check roll of 8 with no attribute modifier and a Basic skill totals 9, succeeding against Easy (9).
- **Expert skill (+3):** a raw check roll of 11 with a -1 attribute modifier and an Expert skill totals 13, succeeding against Normal (12).
- **Skill required, level 0:** the attempt is blocked before rolling. No dice are rolled and no total is produced, however large the other modifiers are.

## 5. Characters

Most character systems remain unspecified. The six canonical attributes, ordinary-human attribute generation, and the four canonical skill levels are now defined.

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

Skill **levels** are canonical. The skill **catalog** is not: no skill list,
skill names, or skill-to-attribute assignments are defined yet.

A character has exactly one of four levels in a given skill:

| Level | Name | Modifier | Meaning |
|---:|---|---:|---|
| 0 | Unskilled | special | The character does not possess the skill. |
| 1 | Basic | +1 | Basic competence in the skill. |
| 2 | Advanced | +2 | Advanced competence in the skill. |
| 3 | Expert | +3 | Expert competence in the skill. |

**Level 0 is the absence of the skill, not ordinary trained competence.** It has
two cases, taken from section 4.2:

1. **Unskilled allowed** — the action may be attempted with an additional **-1**, applied exactly once.
2. **Skill required / trained-only** — the attempt is **blocked before rolling**. No dice are rolled, and no modifier can bypass the requirement.

Levels 1–3 contribute their listed positive modifier to the check in section 4.

These are the only ordinary skill levels. There is no level above 3 and no
fractional or partial level. The level range is intentionally small: 0 = no
skill, 1 = basic, 2 = advanced, 3 = expert.

The following are **not defined** and must not be inferred: a skill catalog, which
skills are unskilled-allowed versus trained-only, XP costs, progression speed,
training time, specialties, prerequisites, skill groups, defaulting chains,
critical-success rules, and any advancement mechanic. See section 5.6.

Levels 1–3 have no numeric representation in `data/rules/core.json` yet; that
file remains the canonical runtime data for the attributes, human generation,
difficulty targets, unskilled penalty, and opposed-check semantics specified
above.

### 5.4 Derived statistics

**UNSPECIFIED.**

### 5.5 Character creation

Only ordinary-human attribute generation in section 5.2 and the four skill levels in section 5.3 are currently defined. All other character-creation procedures, including starting skill levels, are reserved for later specification.

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

**Hacking is UNSPECIFIED.** CYB is the governing attribute for technical, programming, cyberspace, cybernetics and hacking actions, and **section 12.1 defines the situational modifier framework** that applies to those actions. No hacking subsystem, tool catalog, target-security model, or cyberspace skill list is defined.

### 12.1 Cyberspace and hacking modifiers (human users)

This is the starting framework for **human characters operating in cyberspace**. It is deliberately small and simulationist: actual hardware, interface quality, compute, connectivity and defensive preparation matter mechanically, without becoming a bookkeeping system.

**The character assumption is a human user.** These modifiers are **not** generalized to AI-native entities, uploaded humans, other cyberspace-native beings, non-human intelligence, or autonomous software agents. Their relationship to interface, compute, embodiment and connectivity may be fundamentally different, and they need a separate design pass — see the deferral note at the end of this section.

The check structure:

~~~text
total = 3d6
      + CYB attribute modifier
      + relevant skill modifier
      + BCI modifier
      + Compute modifier
      + Connection modifier
      + Infosec modifier, where it applies
      + other future software / hardware / situational modifiers
success = total >= difficulty target
~~~

**Not every category applies to every check.** Each modifier is included only where it logically affects the action. A check made with no relevant equipment, for instance, simply has fewer terms — the framework describes what *can* apply, not a fixed sum.

All four categories use the same small scale, matching the rest of the system:

| Quality | Modifier |
|---|---:|
| Poor / obsolete | -1 |
| Standard | +0 |
| Advanced | +1 to +3 |

#### BCI modifier

The quality and immediacy of the human user's interface into cyberspace.

| Modifier | Interface |
|---:|---|
| **-1** | Legacy / non-BCI interface: keyboard and monitor, voice commands, mobile phone, or another slow or awkward conventional interface. Appropriate for people who refuse invasive or non-invasive brain-computer interfaces. |
| **+0** | Standard BCI: non-invasive or invasive, cheap and common. The baseline human cyberspace interface. |
| **+1 to +3** | Advanced invasive BCI: progressively more advanced state-of-the-art invasive interfaces. |

#### Compute modifier

Local or personal compute available for intelligence augmentation and cyberspace operations, whether integrated into an implant or carried in an external cyberdeck.

| Modifier | Compute |
|---:|---|
| **-1** | No meaningful augmentation compute: nothing useful in implant or deck for intelligence augmentation. |
| **+0** | Standard compute: normal consumer-grade personal compute, roughly the setting-equivalent of an ordinary cell phone or standard personal device. |
| **+1 to +3** | Advanced compute: progressively stronger intelligence augmentation or local compute. |

#### Connection modifier

The quality and proximity of the connection to the target system.

| Modifier | Connection |
|---:|---|
| **-1** | Global wireless / mobile-network connection: the ordinary wide-area mobile network. Poor bandwidth and latency for demanding cyberspace activity — enough for limited remote access, not ideal for heavy operations. |
| **+0** | Local WLAN / local network: suitable for augmented reality and for interacting with or hacking local IoT devices. |
| **+1** | Direct wired connection: physically wired into the target or target network, or a direct server/network connection. |

These are the only connection tiers. Fiber quality, satellite links, mesh relays, tactical radios, air-gapped bridging and quantum networking remain for later author specification.

#### Infosec defence modifier

Defensive hardening protecting the user, especially the BCI and connected personal systems. This matters because an invasive BCI creates the possibility that hostile cyberspace activity can threaten brain-connected systems — which is why this category exists from the beginning, and why it is primarily **defensive**: it is applied where it logically affects the action, not to every check.

| Modifier | Defence |
|---:|---|
| **-1** | Unhardened / disabled infosec: no meaningful firewall, hardening, filtering, sandboxing or equivalent defence, or protections are disabled for some reason. Especially dangerous when using an invasive BCI. |
| **+0** | Standard infosec: normal baseline defensive hardening, nothing exceptional. |
| **+1 to +3** | Advanced infosec: progressively stronger defensive hardening. |

#### Not defined here

Deliberately left undefined, and not to be inferred: named implants or brands, bandwidth or latency numbers, hardware tiers, FLOPS, model sizes, RAM, accelerators, power consumption, device catalogs, prices, surgery rules, costs, humanity mechanics, medical side effects, brain-damage mechanics, neural malware, intrusion tables, ICE catalogs, firewall product classes, mental-status consequences, a complete hacking subsystem, and a cyberspace skill list.

Those belong to later author specification. The framework above is a starting point; further modifier categories may be added later.

#### Deferred: non-human cyberspace participants

Cyberspace rules for **AI-native entities, uploaded humans, autonomous software agents and other non-human participants** are **explicitly deferred** to a separate future design task. They are not covered by, and must not be inferred from, the human-user modifiers in this section.

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

They use the same canonical attribute identifiers, human-generation table, difficulty targets, check semantics, unskilled penalty, trained-only representation, and opposed-check semantics.

The four skill levels in section 5.3 are **tabletop-first and not yet ported**. They
are canonical tabletop rules; Godot and Concordia do not implement them yet, and
porting them is a separate later task after the tabletop version is stable.

The cyberspace and hacking modifiers in section 12.1 are **tabletop-first and not
yet ported** in the same way. There is no runtime schema, modifier table or
`data/rules/core.json` entry for them, and Godot and Concordia do not implement
them. Porting them is a separate later task after the tabletop framework is stable.

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
- hacking rules (beyond the human-user situational modifier framework in section 12.1: tools, target security, ICE, tracing, stealth, brain-hacking consequences)
- cyberspace rules for AI-native entities, uploaded humans and autonomous agents
- detailed network topology, bandwidth and latency models
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
