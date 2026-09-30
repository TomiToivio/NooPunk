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

## 4. Core resolution system: skill checks

> **This section supersedes the earlier 3d6 core check and its
> `3 / 6 / 9 / 12 / 15 / 18` difficulty ladder.** NoöPunk's skill checks now use the
> **Cities Without Number SRD** model (section 18.1, decision **Core checks →
> MODIFY**), keeping NoöPunk's own six attributes and its wider **−3..+3**
> ordinary-human attribute range.

The basic NoöPunk skill check is:

~~~text
total = 2d6 + relevant skill level + relevant attribute modifier + other applicable modifiers
success = total >= difficulty
~~~

A **2d6** roll is two six-sided dice summed, giving 2..12. The **skill level** term
is the character's level in the relevant skill (section 5.3): **+0..+4** for a
trained skill at level-0 through level-4. A character who does not possess the skill
either takes the **unskilled -1** or is **blocked**, per section 4.2.

The **attribute modifier** is the modifier of whatever attribute is relevant to the
action (section 4.4). NoöPunk's ordinary-human range is **−3..+3** (section 5.2).

A check succeeds when the final total **meets or exceeds** the difficulty; a total
one below fails.

On a failure the character either cannot accomplish the feat at all, suffers bad
luck, or achieves it at the cost of a further complication. **The GM decides the
specific consequence of a failure.** No failure table is canonical.

### 4.1 Difficulty ladder

| Difficulty | Meaning |
|---:|---|
| **6** | A relatively simple task that is still more than the character would usually be expected to manage in their regular background. |
| **8** | A significant challenge to a competent professional, that they would still succeed at more often than not. |
| **10** | Something too difficult to be expected of anyone but a skilled expert, and even they might fail. |
| **12** | Only a true master could expect to carry this off with any degree of reliability. |
| **14+** | Only a true master has any chance of achieving this at all, and even they will probably fail. |

Anything easier than difficulty 6 **is not worth a skill check** and should be
resolved by ordinary competence or narrated directly.

These five ratings supersede the earlier NoöPunk ladder `Easiest 3, Easier 6,
Easy 9, Normal 12, Hard 15, Impossible 18`. That ladder is **no longer canonical for
skill checks**, and its names are not retained as aliases: the old `Easy 9` and the
new `6` or `8` are different questions, so silently re-pointing a name would change
what an old note meant. **Difficulty 6 keeps its number but changes meaning** — under
the old ladder it was the second-easiest rung (`Easier`); it is now the *hardest
thing still not worth rolling for*. There is no automatic failure on a natural 2 and
no automatic success on a natural 12.

### 4.2 Unskilled and trained-only checks

These two cases apply to a character who **does not possess** the skill. Unskilled
is not a skill level: it is the absence of one (section 5.3).

1. **Unskilled attempt allowed:** the action may be attempted without the skill, with an additional **-1 unskilled modifier**, applied exactly once.
2. **Skill required / trained-only:** the action cannot be attempted without the required skill. This is a **blocked attempt**, not a failed roll. No dice are rolled and additional modifiers cannot bypass the requirement.

A character who possesses the skill is trained, and uses their skill level's
**+0..+4** modifier instead (section 5.3).

Which skills use which category is not yet specified. The **technical or esoteric**
test is deliberately left to the GM and is not enumerated: some sufficiently
technical or esoteric tasks may be impossible to attempt untrained.

### 4.3 Opposed checks

For opposed **skill checks**, each side rolls:

~~~text
2d6 + relevant skill level + relevant attribute modifier
~~~

The side with the higher final total wins. **On a tie, the player character wins.**

This supersedes the earlier NoöPunk rule that an opposed tie is "unresolved". It
applies to opposed **skill checks**. Where an opposed test involves no player
character, use the smallest coherent reading — the GM resolves it as an ordinary
contest between two NPC totals (section 4.5) — and treat any deeper procedure as
future design. Do not invent an elaborate tie ladder.

### 4.4 Calling for a skill check

The GM calls for a skill check when the outcome is meaningfully uncertain **and**
beyond ordinary competence. The order is:

1. The player describes what the character attempts.
2. The GM names the skill and attribute combination to roll.
3. If more than one combination is genuinely plausible, **the player may pick the one most favourable to them.**
4. If a combination is only marginally relevant but still reasonably plausible, it may suffer a **−1 or −2** penalty, at the GM's discretion.

**Skill-to-attribute bindings are deliberately not fixed.** Do not build a table
mapping each skill to one attribute: the same skill may plausibly use different
attributes depending on what the character is actually doing (for example, a
technical action and a social one may both draw on CYB and CHA in different ways).
The relevant attribute comes from the described action, every time.

### 4.5 Situational modifiers, aid, and NPCs

**Helpful or hostile circumstances** modify a skill check by **−2 to +2**. Normally
no combination of situational modifiers should alter the roll by more than this, or
else it becomes a near-foregone conclusion. Do not turn every fictional detail into
a modifier. This band does **not** cover modifiers from gear mods, cyberware, or PC
aid, which may later have their own rules where explicitly defined.

**Aiding a skill check.** To aid a comrade:

1. The helper explains what their character is doing to help.
2. If the GM agrees it is plausible, the helper rolls a **relevant skill + attribute check against the same difficulty** as the check they are aiding.
3. On success, the acting character gains **+1**.
4. On failure there is normally no additional penalty.
5. Multiple characters may aid when their actions are plausible, but **the total aid bonus is capped at +1**.

Aiding is usually done in a way that lets the helper leverage their own talents: a
character with no Sneak might instead use Perform to create a distraction.

**NPC skill checks.** When an NPC needs a skill check, roll **2d6 + their listed
skill modifier** if the action is something they ought reasonably to be good at. If
it is not, use **+0**, or **−1** if it is something they would be particularly bad
at. An NPC detailed enough to have real attribute scores and skill levels uses those
normally instead. This is lightweight guidance, **not** an NPC-generation system.

### 4.6 Worked skill checks

These examples are normative examples of the same check formula used by Tabletop,
Godot, and Concordia:

- **Competent professional:** a raw 2d6 roll of 7 with a level-1 skill (+1) and a +1 attribute modifier totals 9, failing against difficulty 10 and succeeding against 8.
- **True master:** a raw 2d6 roll of 9 with a level-4 skill (+4) and a +1 attribute modifier totals 14, succeeding against 14+.
- **Wider NoöPunk attribute range:** a raw 2d6 roll of 6 with a level-2 skill (+2) and a **+3** attribute modifier totals 11, succeeding against 10. Under CWN's narrower attribute range the same character would have totalled less; NoöPunk keeps **−3..+3** deliberately (section 5.2).
- **Unskilled allowed:** a raw 2d6 roll of 8 with a +0 attribute modifier and the −1 unskilled modifier totals 7, succeeding against 6. The penalty is applied exactly once.
- **Level-0 skill:** a raw 2d6 roll of 6 with a +0 attribute modifier and a level-0 skill totals 6, succeeding against 6.
- **Marginally relevant combination:** a raw 2d6 roll of 8 with a +1 skill and a +0 attribute modifier, at the GM's −2 for marginal relevance, totals 7, failing against 8.
- **Aided check:** a raw 2d6 roll of 6 with a +1 skill and a +0 attribute modifier totals 7 and fails against 8; a successful aid from a comrade adds +1, making 8 and succeeding. A second successful aid does **not** add another +1.
- **Opposed, PC wins the tie:** the PC totals 9 and the NPC totals 9; the **player character wins**.
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

So the normal skill check in section 4 is:

~~~text
2d6 + relevant skill level + relevant attribute modifier + other applicable modifiers
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
difficulty targets, unskilled penalty, and opposed-check semantics — and, as section
17.1 records, it still carries the **superseded 3d6-era** values pending the port.
The skill list and levels are tabletop-first and not yet ported.

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

**Hacking is UNSPECIFIED and deferred.** CYB is the governing attribute for
technical, programming, cyberspace, cybernetics and hacking actions. No hacking
subsystem, tool catalog, target-security model, or cyberspace skill list is defined.

An earlier revision defined a situational modifier framework for cyberspace actions
(BCI, Compute, Connection, Infosec). **That framework has been withdrawn** and
hacking is now **DEFER** under the chassis policy; see section 12.1 for the
withdrawal and what it does and does not mean.

### 12.1 Cyberspace and hacking modifiers: withdrawn

> **The earlier BCI / Compute / Connection / Infosec modifier framework has been
> withdrawn from active canonical rules.**

An earlier revision of this section (issue #17) specified a stack of situational
modifiers for human cyberspace actions: **BCI** (interface quality), **Compute**
(local compute), **Connection** (link quality and proximity), and **Infosec**
(defensive hardening), applied on top of the core check.

That framework is **no longer canonical**. NoöPunk is now much closer to the Cities
Without Number mechanical chassis, and the hacking/cyberspace subsystem should be
reconsidered against **CWN's own hacking rules** rather than carrying an early
parallel modifier stack forward. See [docs/CWN_CHASSIS.md](docs/CWN_CHASSIS.md):
**Hacking / cyberspace is DEFER.**

**This is a withdrawal from active canon, not a rejection of the ideas.** BCI
quality, compute, connection quality, and infosec defence may return later inside a
redesigned, CWN-derived hacking/cyberspace system. They remain available as **future
design ideas**. The earlier wording is preserved in git history for reference; it is
not a rule and must not be applied to a check.

What this means in practice:

- Do **not** add BCI, Compute, Connection, or Infosec modifiers to a skill check.
- Do **not** reintroduce them into `data/rules/core.json` or any runtime adapter.
- Do **not** treat their withdrawal as an author decision that hacking is solved —
  hacking itself remains **UNSPECIFIED** and is deferred to its own future task.

CYB remains the governing attribute for technical, programming, cyberspace,
cybernetics and hacking actions, as stated at the head of this section. When hacking
is designed, it will follow this section's own guidance: the relevant attribute and
skill come from the described action (sections 4.4 and 5.3), not from a fixed table.

#### Deferred: non-human cyberspace participants

Cyberspace rules for **AI-native entities, uploaded humans, autonomous software
agents and other non-human participants** are **explicitly deferred** to a separate
future design task. They were never covered by the withdrawn human-user modifiers
and must not be inferred from them.

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

**The digital runtimes have not yet been ported to the 2d6 skill-check model in section 4.** As of this revision:

- `data/rules/core.json` still carries the **superseded** 3d6-era constants: the `3 / 6 / 9 / 12 / 15 / 18` `difficulties` map, the `opposed_tie` value `unresolved`, and the attribute-generation table.
- `src/rules/core.py`, `src/godot/core_rules.gd`, and `src/concordia_runtime/mechanics.py` still roll **3d6** and resolve against the old ladder.
- The Godot and Concordia scaffolds are therefore **stale with respect to section 4**, and the skill list and level-0..4 scale in section 5.3 remain unported.

**This is a known, deliberate, explicitly-tracked debt.** It is not a second canon: where a runtime and this rulebook disagree, **this rulebook is authoritative**, and the runtime is wrong. Porting is a separate later task after the tabletop rules are stable (section 14 of `AGENTS.md`). A runtime must not be extended to match the old rules, and a runtime must not invent the new ones either — the port is its own issue.

The attribute identifiers, the ordinary-human generation procedure, the `-3..+3` modifier range, the unskilled penalty, and the trained-only representation are **unchanged** by section 4 and remain shared between tabletop and the runtimes.

Runtime-specific adapters may differ, but they must not redefine canonical rules.

## 18. Canon and change control

A rule becomes canonical only when explicitly specified by the author or incorporated into this rulebook through an author-approved task.

Examples, prototypes, test values, genre conventions, and temporary implementation details are **not canon**.

### 18.1 Open mechanical chassis

NoöPunk's main open mechanical starting point is the **Cities Without Number SRD**. This rulebook describes NoöPunk's own tabletop rules. Where a subsystem is still unresolved, the CWN SRD is the reference point for *reviewing* that subsystem, not an automatic source of the rule.

Every CWN subsystem gets one explicit author decision: **KEEP**, **MODIFY**, **REPLACE**, **OMIT**, or **DEFER**. Nothing is assumed to survive unchanged, and an unresolved subsystem stays **DEFER** (see section 19). Existing NoöPunk rules in this rulebook take precedence over CWN defaults.

Only material actually present in the CWN **SRD** may be directly reused. See [docs/CWN_CHASSIS.md](docs/CWN_CHASSIS.md) for the policy, the legal boundary, and the subsystem review order.

### 18.2 Provenance

**NoöPunk's core tabletop mechanics are derived from and substantially modify the
Cities Without Number SRD, released under CC0. NoöPunk is an independent project and
is not affiliated with or endorsed by Sine Nomine Publishing.**

Provenance is kept short here **by design**. The licence, the exact reuse boundary,
what the CC0 waiver does and does not cover, and the authoritative source are all
explained once in [docs/CWN_CHASSIS.md](docs/CWN_CHASSIS.md) — do not restate the
full licensing argument in this rulebook or scatter legal boilerplate across the
docs.

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
- hacking rules (the withdrawn human-user cyberspace modifier framework is not a rule; the subsystem is **DEFER** and will be redesigned on CWN's hacking chassis — tools, target security, ICE, tracing, stealth, brain-hacking consequences)
- cyberspace rules for AI-native entities, uploaded humans and autonomous agents
- detailed network topology, bandwidth and latency models
- psionic powers
- astral projection mechanics beyond PSY being its future governing attribute
- detailed social subsystem mechanics
- AI / NHI mechanical differences
- transhuman augmentation rules
- opposed skill checks that involve no player character (the PC-wins-tie rule in section 4.3 covers opposed skill checks generally; a fuller procedure is future design)
- equipment and economy
- world building
- factions
- simulation model

This list is a roadmap of questions, not a specification.

Any subsystem that the Cities Without Number SRD also covers is additionally subject to the chassis review in section 18.1 and stays **DEFER** until the author decides it.
