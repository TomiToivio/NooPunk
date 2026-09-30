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
modifier** is the character's skill level (section 5.3): **+0..+4** for a trained
skill at level-0 through level-4, and for a character with no skill either the
**unskilled -1** or a **blocked** attempt, per section 4.2.
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

These two cases apply to a character who **does not possess** the skill. Unskilled
is not a skill level: it is the absence of one (section 5.3).

1. **Unskilled attempt allowed:** the action may be attempted without the skill, with an additional **-1 unskilled modifier**, applied exactly once.
2. **Skill required / trained-only:** the action cannot be attempted without the required skill. This is a **blocked attempt**, not a failed roll. No dice are rolled and additional modifiers cannot bypass the requirement.

A character who possesses the skill is trained, and uses their skill level's
**+0..+4** modifier instead (section 5.3).

Which skills use which category is not yet specified.

### 4.3 Worked checks

These examples are normative examples of the same check formula used by Tabletop, Godot, and Concordia:

- **Easiest, no modifiers:** a raw check roll of 3 against target 3 totals 3 and succeeds.
- **Easiest, -1 modifier:** a raw check roll of 3 with a -1 modifier totals 2 and fails.
- **Impossible:** a raw check roll of 18 with no modifiers against target 18 totals 18 and succeeds. "Impossible" therefore does not mean "unrollable."
- **Unskilled allowed:** a raw check roll of 10 with no attribute modifier and the -1 unskilled modifier totals 9, succeeding against Easy (9). The unskilled penalty is applied exactly once.
- **Level-0 skill (+0):** a raw check roll of 9 with no attribute modifier and a level-0 skill totals 9, succeeding against Easy (9).
- **Level-2 skill (+2):** a raw check roll of 8 with no attribute modifier and a level-2 skill totals 10, succeeding against Easy (9).
- **Level-4 skill (+4):** a raw check roll of 9 with a -1 attribute modifier and a level-4 skill totals 12, succeeding against Normal (12).
- **Skill required, unskilled:** the attempt is blocked before rolling. No dice are rolled and no total is produced, however large the other modifiers are.

## 5. Characters

Most character systems remain unspecified. The six canonical attributes, ordinary-human attribute generation, the skill list, and the level-0..4 trained skill scale are now defined.

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

> **This section supersedes the earlier four-step skill model** in which level 0
> meant "unskilled" and levels 1–3 gave +1/+2/+3. That model is withdrawn. Under the
> Cities Without Number chassis (section 18.1), the decision for this subsystem is
> **MODIFY**, and NoöPunk now uses a **trained skill scale of level-0 through
> level-4**, with unskilled sitting **outside** the numbered levels.

**Unskilled is not level-0.** A character who does not possess a skill is
*unskilled*, which is not a numbered level at all. It has the two cases in section
4.2: an unskilled attempt is either allowed with **-1**, or **blocked** when training
is required.

A character who possesses a skill has exactly one level in it:

| Skill level | Meaning for now |
|---:|---|
| **Level-0** | Basic competence, such as an ordinary practitioner would have |
| **Level-1** | Experienced professional, clearly better than most |
| **Level-2** | Veteran expert, respected even by those with considerable experience |
| **Level-3** | Master of the skill, likely one of the best in the city |
| **Level-4** | Superlative expertise, one of the best in the world |

For now, a trained skill contributes its numeric level to a normal skill check:

~~~text
unskilled: -1 if the attempt is allowed, otherwise BLOCKED
level-0:   +0
level-1:   +1
level-2:   +2
level-3:   +3
level-4:   +4
~~~

So the normal check in section 4 stays conceptually:

~~~text
3d6 + relevant attribute modifier + relevant skill level + other applicable modifiers
~~~

This wording is deliberately provisional. The scale and the skill list are a first
pass under the chassis review; the author expects to revisit individual skills,
specialties, advancement, attribute interactions, and professions later.

#### Skill list

The initial NoöPunk skill list is the **Cities Without Number SRD standard skill
list** as a starting point, with two author-specified renames: **Heal → Medical**
and **Know → Science**.

- **Administer** — manage an organization, handle paperwork, analyze records, and keep an institution functioning. Bureaucratic expertise, organizational management, legal knowledge, government agencies, and how corporations really work.
- **Connect** — find people who can be helpful and get them to cooperate. Useful connections, people you know, where to get illicit goods and services, foreign cultures and languages. Can stand in for Talk when persuading people found through this skill.
- **Drive** — drive vehicles, sail ships, fly planes, pilot drones, and perform maintenance and basic repairs on such devices.
- **Exert** — apply trained speed, strength, or stamina: run, jump, lift, swim, climb, throw. Usable as a combat skill when throwing things, but not otherwise.
- **Fix** — create and repair devices both simple and complex; build things, fix things, and identify what something is supposed to do.
- **Medical** — medical and psychological treatment for the injured or disturbed. Cure diseases, stabilize the critically injured, treat psychological disorders, diagnose illnesses, and the medical care of cyberware where later rules make that relevant. Inherits the role of CWN **Heal**.
- **Science** — facts about academic or scientific fields. Understand academic topics, recall relevant history, solve science mysteries, and know basic facts about rare or esoteric topics. Inherits the role of CWN **Know**.
- **Lead** — convince others to do whatever it is you are trying to do, even when they think it is a bad idea. Lead troops in combat, inspire loyalty, maintain morale and discipline.
- **Notice** — spot anomalies or interesting facts about the environment. Search places, detect ambushes, spot things, and read the emotional state of other people.
- **Perform** — exhibit a performance skill: dance, sing, orate, act, or otherwise put on a convincing or emotionally moving performance.
- **Program** — operate or hack computing and communications hardware. Program or hack computers, control computer-operated hardware, operate communications tech, decrypt things.
- **Punch** — the combat skill for fighting unarmed.
- **Shoot** — the combat skill for ranged weaponry: thrown weapons, bows, gunlinked pistols, combat rifles, heavy artillery.
- **Sneak** — move without drawing notice. Stealth, disguise, infiltration, manual legerdemain, pickpocketing, and physically defeating security measures such as electronic locks.
- **Stab** — the combat skill for melee weapons, primitive or complex. Also usable when throwing weapons.
- **Survive** — street smarts and urban survival, or outlands bushcraft and wilderness living, depending on background. Practice can generalize it.
- **Talk** — convince other people of the facts you want them to believe: persuade, charm, or deceive others in conversation.
- **Trade** — find what you need on the market and sell what you have. Sell or buy things, find hard-to-get or illicit goods, deal with customs agents, run a business.
- **Work** — a catch-all for professions not represented by other skills. **The profession mechanism is not yet canonical NoöPunk specialization mechanics** (see below): for now this is a broad skill, and how it is narrowed is deferred.

Do **not** casually rename, split, merge, or add other skills. The author will review
the list bit by bit later.

#### Skills are not bound to a fixed attribute

Do not assign every skill to a fixed attribute. NoöPunk checks use the attribute
**relevant to the action** and to later rules, not a fixed skill-to-attribute table.

#### Not defined

The following are **not defined** and must not be inferred: which skills are
unskilled-allowed versus trained-only; a skill catalog beyond the list above;
per-skill attribute bindings; training time; prerequisites; skill groups;
defaulting chains; critical-success rules; and any advancement mechanic
(section 5.6).

Skill levels have **no numeric representation in `data/rules/core.json`** yet; that
file remains the canonical runtime data for the attributes, human generation,
difficulty targets, unskilled penalty, and opposed-check semantics. Skill levels and
the skill list are tabletop-first and not yet ported (section 17).

#### Specialties: deferred

The author expects some broad skills eventually to support specialties, such as
`Science (Biotech)` or `Work (Lawyer)`. This is **future design, not a rule**.

Explicitly **not** decided, and not to be inferred:

- whether specialties are mandatory or optional;
- whether they give modifiers;
- whether they restrict what a broad skill can do;
- whether Work always requires a profession;
- whether Science always requires a field;
- how specialties are bought or advanced;
- whether specialties have their own levels;
- whether other skills use specialties.

In particular, CWN's treatment of Work as *"pick a particular profession"* is **not**
automatically canonical NoöPunk specialization mechanics. The broad Work skill stands
for now, and the exact specialty/subtype mechanism is deferred until the author
decides it.

### 5.4 Derived statistics

**UNSPECIFIED.**

### 5.5 Character creation

Only ordinary-human attribute generation in section 5.2 and the skill list and levels in section 5.3 are currently defined. All other character-creation procedures, including how many skills a starting character has and at what levels, are reserved for later specification.

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

#### The relevant skill is not fixed

The **"relevant skill modifier"** term is the character's level in whatever skill
the action actually calls for (section 5.3). No skill is bound to cyberspace by
this framework.

**Program** is an obvious candidate for many computing and hacking actions, since it
has that role in the Cities Without Number SRD. That is an observation, not a rule:
this framework does **not** create a hacking subsystem and does **not** decide that
every cyberspace action uses Program. Which skill applies, and when, remains for
later author specification.

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

The skill list and the level-0..4 trained skill scale in section 5.3 are
**tabletop-first and not yet ported**. They are canonical tabletop rules; Godot and
Concordia do not implement them yet, and porting them is a separate later task after
the tabletop version is stable.

The cyberspace and hacking modifiers in section 12.1 are **tabletop-first and not
yet ported** in the same way. There is no runtime schema, modifier table or
`data/rules/core.json` entry for them, and Godot and Concordia do not implement
them. Porting them is a separate later task after the tabletop framework is stable.

Runtime-specific adapters may differ, but they must not redefine canonical rules.

## 18. Canon and change control

A rule becomes canonical only when explicitly specified by the author or incorporated into this rulebook through an author-approved task.

Examples, prototypes, test values, genre conventions, and temporary implementation details are **not canon**.

### 18.1 Open mechanical chassis

NoöPunk's main open mechanical starting point is the **Cities Without Number SRD**. This rulebook describes NoöPunk's own tabletop rules. Where a subsystem is still unresolved, the CWN SRD is the reference point for *reviewing* that subsystem, not an automatic source of the rule.

Every CWN subsystem gets one explicit author decision: **KEEP**, **MODIFY**, **REPLACE**, **OMIT**, or **DEFER**. Nothing is assumed to survive unchanged, and an unresolved subsystem stays **DEFER** (see section 19). Existing NoöPunk rules in this rulebook take precedence over CWN defaults.

Only material actually present in the CWN **SRD** may be directly reused. See [docs/CWN_CHASSIS.md](docs/CWN_CHASSIS.md) for the policy, the legal boundary, and the subsystem review order.

## 19. Future design sections

The following remain intentionally unresolved:

- skill specialties and skill progression
- skill-to-attribute bindings
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

Any subsystem that the Cities Without Number SRD also covers is additionally subject to the chassis review in section 18.1 and stays **DEFER** until the author decides it.
