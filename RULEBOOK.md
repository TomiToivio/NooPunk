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

NoöPunk uses the **Cities Without Number SRD skill-check engine**, modified for NoöPunk's own six attributes and wider ordinary-human attribute range.

The basic skill check is:

~~~text
total = 2d6 + relevant skill level + relevant attribute modifier
success = total >= difficulty
~~~

Roll two six-sided dice and add the character's relevant trained skill level and the attribute modifier that best fits the action. A level-0 skill contributes +0, level-1 contributes +1, and so on through level-4 at +4. A character with no relevant skill is **unskilled**, which is outside the numbered skill levels and uses section 4.2.

NoöPunk keeps its own attribute modifiers, including the ordinary-human **-3..+3** range in section 5.2. This is an intentional divergence from the narrower CWN attribute range.

The GM calls for a skill check when the outcome is meaningfully uncertain and beyond ordinary routine competence. Anything easier than difficulty 6 generally should not require a roll.

| Difficulty | Meaning |
|---:|---|
| **6** | Relatively simple task that is still beyond ordinary routine |
| **8** | Significant challenge to a competent professional |
| **10** | Difficult task expected mainly of a skilled expert |
| **12** | Master-level challenge |
| **14+** | Extreme task where even a true master will probably fail |

These five ratings replace the earlier NoöPunk ladder `Easiest 3 / Easier 6 / Easy 9 / Normal 12 / Hard 15 / Impossible 18`, which is **no longer canonical for skill checks**. The old difficulty names are **not retained as aliases**: the old `Hard` must not silently continue to mean 15, and old `Easy` must not mean 9. Difficulty **6** keeps its number but changes its meaning — under the old ladder it was the second-easiest rung, and it is now the hardest task still not worth rolling for. There is **no automatic failure on a natural 2** and **no automatic success on a natural 12**; a 2 or a 12 is only ever a low or high die result.

The player describes what the character is doing. The GM selects the relevant skill and attribute from that description. Skills are **not** permanently bound to one attribute. If more than one combination is genuinely plausible, the player may use a plausible favorable combination. A combination that is only marginally relevant may take a **-1 or -2** penalty at the GM's discretion.

Helpful or hostile circumstances generally produce a combined situational modifier within **-2..+2**. Exceptional subsystem-specific equipment, cyberware, software, or other effects may later define their own rules. Do not assign modifiers to every fictional detail.

This section supersedes the earlier NoöPunk **3d6 skill-check engine** and its **3 / 6 / 9 / 12 / 15 / 18** difficulty ladder. The old numbers remain relevant only to historical repository versions and to the still-unported digital runtime described in section 17.

### 4.1 Opposed skill checks

For an opposed skill check, both sides roll:

~~~text
2d6 + relevant skill level + relevant attribute modifier
~~~

The side with the higher total wins.

If a player character is involved and the totals tie, **the player character wins the tie**.

A general tie procedure for opposed tests that involve no player character is not defined here. Do not invent an additional subsystem for it.

### 4.2 Unskilled and trained-only checks

These two cases apply to a character who **does not possess** the relevant skill. Unskilled is not a skill level: it is the absence of one (section 5.3).

1. **Unskilled attempt allowed:** apply **-1** to the skill check.
2. **Training required:** sufficiently technical or esoteric tasks may be impossible to attempt without the relevant skill. This is a **blocked attempt**, not a failed roll. No dice are rolled.

A character who possesses the skill uses the numbered level normally, from level-0 (+0) through level-4 (+4).

Which tasks require training remains contextual unless a later subsystem specifies it.

### 4.3 Aiding another character

A character may help another character when the fiction makes the assistance plausible.

1. The helper explains how they are helping.
2. The helper rolls a relevant skill + attribute check against the same difficulty.
3. On success, the acting character receives **+1**.
4. On failure, there is normally no additional penalty.
5. Multiple helpers may roll when plausible, but the total aid bonus is capped at **+1**.

### 4.4 NPC skill checks

Ordinary NPCs use the lightweight CWN-derived approach:

- for something they should reasonably be competent at, roll **2d6 + the NPC's listed or relevant skill modifier**;
- use **+0** for ordinary unrelated competence;
- use **-1** when the NPC is particularly bad at the task;
- unusually detailed NPCs that actually have attributes and skill levels may use the full player-character procedure.

This is not a complete NPC-generation system.

### 4.5 Worked checks

- **Difficulty 6, level-0, attribute +0:** a roll of 6 totals 6 and succeeds.
- **Difficulty 8, unskilled, attribute +1:** a roll of 8 with +1 attribute and -1 unskilled totals 8 and succeeds.
- **Difficulty 10, level-2, attribute +1:** a roll of 7 +2 +1 totals 10 and succeeds.
- **Difficulty 12, level-4, attribute -1:** a roll of 9 +4 -1 totals 12 and succeeds.
- **Training required, unskilled:** the attempt is blocked before rolling.

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
2d6 + relevant skill level + relevant attribute modifier
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

Skill levels have **no numeric representation in `data/rules/core.json`** yet. The current runtime data and adapters still implement the superseded pre-#25 3d6 check engine; they are retained temporarily as digital-port debt and are **not** the tabletop source of truth. Skill levels and the skill list are tabletop-first and not yet ported (section 17).

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

**Hacking / cyberspace is DEFERRED.**

The earlier tabletop experiment from issue #17 introduced separate **BCI, Compute, Connection, and Infosec defence modifiers** for human cyberspace users. Those modifiers are now **withdrawn from active canon** while NoöPunk's hacking subsystem is reconsidered against the Cities Without Number SRD.

The concepts are not rejected. BCI quality, local compute, connection quality, and infosec hardening may return later inside a redesigned CWN-derived hacking/cyberspace system.

For now:

- CYB remains the canonical attribute for cybernetic, technical, programming, and cyberspace aptitude where relevant;
- **Program** remains a skill in section 5.3, but this section does not declare that every cyberspace action uses Program;
- no BCI / Compute / Connection / Infosec modifier tables are active rules;
- no hacking subsystem, cyberdeck rules, ICE, tracing, target-security model, brain-hacking consequences, or AI-native cyberspace mechanics are defined;
- AI-native entities, uploaded humans, and autonomous software agents remain a separate later design problem.

The next hacking/cyberspace task should review the CWN SRD hacking subsystem under the KEEP / MODIFY / REPLACE / OMIT / DEFER process before restoring or replacing any of the earlier modifier concepts.

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

### 17.1 Known port debt: the digital runtimes still implement the superseded 3d6 system

The **tabletop skill-check canon is now the 2d6 CWN-derived engine in section 4**. The existing `data/rules/core.json`, shared Python rules, Godot adapter, and Concordia adapter still implement the superseded 3d6 check engine and old difficulty ladder. They are retained temporarily as **explicit digital-port debt**, not as competing canon. Where a runtime and this rulebook disagree, **this rulebook is authoritative** and the runtime is wrong. `data/rules/core.json` carries a `_superseded_note` key recording this in the runtime data itself.

A later porting task must convert the stable tabletop rule into a shared digital specification and then update Godot and Concordia consistently. Until that task is done, runtime tests may verify the legacy implementation as legacy behavior, but documentation must not describe it as the current canonical tabletop mechanic.

The skill list and the level-0..4 trained skill scale in section 5.3 are also tabletop-first and not yet ported.

The attribute identifiers, ordinary-human 3d6 generation, the -3..+3 modifier range, the unskilled penalty, and the trained-only representation are **unchanged** by section 4 and remain shared between tabletop and the runtimes.

The former issue #17 BCI / Compute / Connection / Infosec modifier framework is no longer an active tabletop rule and must not be ported. Hacking/cyberspace is DEFERRED pending a later CWN-based subsystem review.

Runtime-specific adapters may differ in plumbing, but once ported they must not redefine canonical rules.

## 18. Canon and change control

A rule becomes canonical only when explicitly specified by the author or incorporated into this rulebook through an author-approved task.

Examples, prototypes, test values, genre conventions, and temporary implementation details are **not canon**.

### 18.1 Open mechanical chassis

NoöPunk's main open mechanical starting point is the **Cities Without Number SRD**. This rulebook describes NoöPunk's own tabletop rules. Where a subsystem is still unresolved, the CWN SRD is the reference point for *reviewing* that subsystem, not an automatic source of the rule.

Every CWN subsystem gets one explicit author decision: **KEEP**, **MODIFY**, **REPLACE**, **OMIT**, or **DEFER**. Nothing is assumed to survive unchanged, and an unresolved subsystem stays **DEFER** (see section 19). Existing NoöPunk rules in this rulebook take precedence over CWN defaults.

Only material actually present in the CWN **SRD** may be directly reused. NoöPunk's core tabletop mechanics are derived from and substantially modify the Cities Without Number SRD, released under CC0. NoöPunk is an independent project and is not affiliated with or endorsed by Sine Nomine Publishing. See [docs/CWN_CHASSIS.md](docs/CWN_CHASSIS.md) for the detailed policy, legal boundary, and subsystem review order.

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
- hacking / cyberspace rules, including whether any BCI, Compute, Connection, or Infosec modifiers return in the later CWN-derived design
- cyberspace rules for AI-native entities, uploaded humans and autonomous agents
- detailed network topology, bandwidth and latency models
- psionic powers
- astral projection mechanics beyond PSY being its future governing attribute
- detailed social subsystem mechanics
- AI / NHI mechanical differences
- transhuman augmentation rules
- equipment and economy
- world building
- factions
- simulation model

This list is a roadmap of questions, not a specification.

Any subsystem that the Cities Without Number SRD also covers is additionally subject to the chassis review in section 18.1 and stays **DEFER** until the author decides it.
