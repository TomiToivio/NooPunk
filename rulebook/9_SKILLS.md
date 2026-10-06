# Skills

> **Status: NOÖPUNK NATIVE — issue #159 supersedes the deferred skill list.**
>
> NoöPunk uses an independent **1–10 Skill** scale to match the **1–10 STAT** scale
> (`rulebook/2_ATTRIBUTES.md`). This chapter defines the **canonical universal Skill list**,
> each Skill's governing attribute, whether it may be attempted untrained, and the
> specialization rule. It replaces the placeholder text "the final complete Skill list is
> still allowed to evolve" in `RULEBOOK.md` §4.
>
> The list is inspired especially by **Eclipse Phase** and **Cities Without Number**, but it
> is its own system. It is deliberately **smaller and flatter** than Cyberpunk RED's catalogue
> and carries **no Eclipse Phase numerical mechanics** — no linked aptitudes, no percentile
> values, no defaulting formula. Those belong to EP2 and are not NoöPunk rules.

## Core rule

Every Skill is based on one of the six NoöPunk attributes:

- **Fitness (FIT)** — athletic performance, physical strength, endurance, bodily effort.
- **Reflexes (REF)** — coordination, dexterity, agility, reaction speed, precise physical control.
- **Intelligence (INT)** — knowledge, reasoning, analysis, memory, research, cognitive tasks.
- **Social (SOC)** — charisma, communication, persuasion, leadership, social interaction, language.
- **Cybernetics (CYB)** — native cyborg and cyberspace technical ability (Infosec, Interface, Program, Hardware).
- **Psyche (PSY)** — consciousness-related tasks, intuition, perception, artistic and experiential abilities, and psionics.

A normal check is:

```text
Attribute + Skill + 1d10 vs Difficulty Value
```

The relevant attribute is fixed by the Skill's row below. A few broad Skills are marked
**flexible** and use different attributes depending on the task; the default is always stated.

## Untrained use

Some Skills may be attempted **untrained** with a **−1 modifier**. Others **require training**
and cannot be attempted at all by an untrained character. The **Trained?** column states this
for every Skill.

- Attemptable untrained at −1: broad, everyday physical, social and awareness actions.
- Trained only: anything requiring a field of knowledge, a technical discipline, a
  controlled skill such as piloting or surgery, or psionic capability.

The −1 is the only untrained penalty; there is no separate "defaulting" formula.

## Specialization model

Some broad Skills are **field Skills**: they require a **field** written on the sheet, e.g.
`Know (Sociology)`, `Medicine (Forensics)`, `Pilot (Space)`.

- A **related** field may substitute at a **−1 modifier**.
- An **unrelated** field cannot substitute at all.

Examples:

- `Know (Sociology)` may answer a **Political Science** question at −1.
- `Know (Sociology)` cannot answer a **Physics** question.
- `Pilot (Ground)` may drive a **watercraft** at −1; it cannot fly an **aircraft**.

Relatedness is judged sensibly at the table by the GM and the group. NoöPunk does not build
an exhaustive relatedness matrix; when two fields are obviously adjacent, allow −1, and when
they are obviously not, refuse.

The seven field Skills are **Exotic Skill, Hardware, Know, Medicine, Pilot, Perform, Work**.
A campaign exposes only the fields actual play needs (see `RULEBOOK.md` §39 and
`data/rules/campaign_skill_fields.json`).

## The canonical skill list

### Physical skills

| Skill | Attribute | Trained? | Summary |
| --- | --- | --- | --- |
| **Athletics** | FIT | untrained (−1) | Physical activity in gravity: climbing, running, swimming, jumping, gymnastics, throwing, winged flight, general athletic movement. |
| **Free Fall** | FIT | untrained (−1) | Physical activity in microgravity or free fall: maneuvering, orientation, EVA movement, spin recovery. |
| **Fray** | REF | untrained (−1) | Getting out of the way of danger: dodging, evasive movement, avoiding blasts and sudden hazards. Evasion only — the exact combat-defence procedure is a later subsystem. |
| **Melee** | FIT (finesse → REF) | untrained (−1) | Fighting with held or improvised melee weapons: clubs, blades, stun batons. Highly dexterous weapons may use REF instead. |
| **Sneak** | REF | untrained (−1) | Sneaking, hiding, stalking, concealing movement, escaping detection. |

### Combat skills

| Skill | Attribute | Trained? | Summary |
| --- | --- | --- | --- |
| **Guns** | REF | trained only | Aiming and shooting ranged weapons: beam, kinetic, seeker, spray, handguns, rifles. Unusual weapons use Exotic Skill. |
| **Unarmed** | FIT | untrained (−1) | Unarmed combat: striking, grappling, restraint, takedowns, holds, non-lethal subdual. |

### Social skills

| Skill | Attribute | Trained? | Summary |
| --- | --- | --- | --- |
| **Connect** | SOC | untrained (−1) | Finding and using social connections: locating contacts, networking, asking around, informal channels. Interacts with the Faction / Reputation / Contact system. |
| **Deceive** | SOC | untrained (−1) | Lying, bluffing, conning, fast talk, impersonation, acting, misrepresenting or hiding the truth with words and gestures. Opposed by Kinesics. |
| **Kinesics** | SOC | untrained (−1) | Reading people: body language, tells, facial expression, social cues, emotional signals, non-verbal communication. Opposes Deceive. |
| **Lead** | SOC | untrained (−1) | Leadership: command, motivating people, coordinating teams, combat, political and crisis leadership. |
| **Perform** | PSY (SOC when primarily social) | untrained (−1) | Performing art or expressive activity. Fields: Music, Dance, Acting, Visual Art, Ritual Performance, Performance Art. |
| **Provoke** | SOC | untrained (−1) | Moving someone emotionally: intimidation, taunting, seduction, agitation, emotional manipulation. Distinct from Talk. |
| **Talk** | SOC | untrained (−1) | Persuading through ordinary communication: persuasion, negotiation, diplomacy, rapport, explaining, convincing. |
| **Trade** | SOC | untrained (−1) | Buying and selling on markets: bargaining, valuation, negotiating prices, commercial dealing. |

### Investigative and social-science skills

NoöPunk keeps its **police, intelligence and investigative** competence in a small cluster
rather than a dozen near-duplicate skills. The dedicated skills are **Perceive**,
**Kinesics**, **Research** and **Connect**; the case-work *fields of knowledge* are carried
by **Know** fields (see below). This is the design rule the issue asks for: *avoid several
skills that all solve the same detective scene*.

| Skill | Attribute | Trained? | Summary |
| --- | --- | --- | --- |
| **Perceive** | PSY | untrained (−1) | Awareness through the senses: sight, hearing, smell, touch, situational awareness, noticing hidden detail, reading augmented sensory feeds. Perception sits under **PSY** because perception is an aspect of conscious experience. |
| **Research** | INT | untrained (−1) | Finding and synthesizing external information: online, library, archives, databases, public records, scientific literature, OSINT-style gathering. |

### Cognitive and knowledge skills

| Skill | Attribute | Trained? | Summary |
| --- | --- | --- | --- |
| **Know** (field) | INT | trained only | Academic, scientific, technical, cultural or theoretical knowledge of a field. Related fields may be used at −1. |
| **Administrate** | INT (SOC when it is leadership/politics) | untrained (−1) | Managing an organization: bureaucracy, logistics, budgets, project management, institutional procedure, coordinating personnel, running departments. |
| **Survival** | INT | untrained (−1) | Operating in hostile environments: wilderness and urban survival, navigation, shelter, food and water, hazard recognition, environmental adaptation. |
| **Work** (field) | variable | trained only | Broad practical occupational competence. The attribute depends on the Work: e.g. Construction → FIT, Precision Technician → REF, Researcher → INT, Politician → SOC, Cyber Operator → CYB, Meditation Teacher → PSY. |

### Technical and cybernetic skills

| Skill | Attribute | Trained? | Summary |
| --- | --- | --- | --- |
| **Hardware** (field) | CYB | trained only | Building, repairing, disabling, upgrading and physically hacking technological systems. Fields include Electronics, Cyberware, Robotics, Vehicles, Weapons, Drones, Sensors, Industrial systems, Psychotronics, Nanofabrication. |
| **Interface** | CYB | untrained (−1) | Operating and interacting with computers, devices, AR/VR, networks, cyberware and machine systems via keyboard, touch, AR, VR, neural interface or BCI. Interface **quality** modifies the roll (legacy gear penalises, advanced BCI bonuses). |
| **Infosec** | CYB | trained only | Hacking or protecting devices and networks: intrusion, exploitation, malware, defence, access control, credential attacks, hardening, compromise detection, counter-hacking. The main cyberwarfare skill. |
| **Program** | CYB | trained only | Writing and modifying software: scripting, application development, AI tool-building, nanofabrication programming, virtual environments, AR illusions, software-defined devices. |

**Boundary rule (Program / Infosec / Interface / Hardware):**

- **Program** *creates and modifies* software.
- **Infosec** *attacks and defends* systems.
- **Interface** *operates and interacts with* systems.
- **Hardware** *physically builds, repairs and modifies* devices.

### Vehicle and field skills

| Skill | Attribute | Trained? | Summary |
| --- | --- | --- | --- |
| **Pilot** (field) | REF | trained only | Piloting or driving vehicles. Fields: Ground Vehicles, Aircraft, Spacecraft, Drones, Watercraft, Exoskeletons/walkers, exotic vehicles. Related categories may be used at −1. |
| **Medicine** (field) | INT | trained only | Diagnosing and healing. Fields: Emergency Care, Surgery, Psychiatry, Neurology, Cybermedicine, Veterinary, Xenomedicine, Psychotronic Medicine, Forensics. |
| **Exotic Skill** (field) | variable | trained only | Unusual capabilities that fit nowhere else — exotic alien technologies, rare morph operation, unusual transhuman abilities. Used sparingly. |

**First Aid is not a separate Skill.** It is `Medicine (Emergency Care)`. This field is the
only Medicine field that a trained operator uses for immediate stabilisation; `Medicine
(Surgery)` and the advanced fields remain trained only and are never attempted untrained.

### Psionic skills

The generic **Psi** placeholder is **replaced** by a compact set of six disciplines. They
require an explicit source of psionic capability — natural PSI ability, psychotronic
augmentation, or another stated source — and are always **trained only**.

| Skill | Attribute | Summary |
| --- | --- | --- |
| **Telepathy** | PSY | Reading and transmitting thoughts, emotion and mental content; mind-to-mind contact and communication. |
| **Clairvoyance** | PSY | Anomalous and remote perception. *Remote Viewing* and *Psychometry* are techniques within this discipline. |
| **Psychokinesis** | PSY | Influencing physical systems and matter through PSI; the physical, potentially offensive PSI discipline. |
| **Noöspace** | PSY | Entering, navigating, perceiving and acting in Noöspace. *Noetic Projection* (OBE) and *Channeling/Mediumship* are techniques within this discipline. |
| **Precognition** | PSY | Anomalous perception of future probabilities. |
| **Psychic Defence** | PSY | Resisting and defending against telepathy, intrusion, possession, influence and noetic attack; it absorbs the former *Counter-Psi* domain. |

**Psychic attack** is performed *through* the disciplines — a hostile Telepathy contact or a
Psychokinesis strike — rather than as a separate skill. The specific sleights, their effects,
and their resolution belong to the Psychic Systems layer and remain a later increment; this
chapter fixes the **skill names and their attributes** only.

**Psychotronics is not a psionic skill.** The engineering of Noetic technology stays
`Hardware (Psychotronics)` (CYB), as established by issue #110.

## Overlap resolutions (the issue's own deltas)

The issue lists overlaps to resolve explicitly. The resolutions are:

| Overlap | Resolution |
| --- | --- |
| Talk / Provoke / Deceive / Kinesics / Connect / Lead | Distinct by *function*: **Talk** persuades by argument and rapport; **Provoke** moves emotion; **Deceive** misrepresents; **Kinesics** reads others; **Connect** finds people; **Lead** directs groups. Kinesics opposes Deceive. |
| Interface / Program / Infosec / Hardware | Split by *verb*: operate / create / attack–defend / build. See the boundary rule above. |
| Know / Research / Investigation / Intelligence Analysis | **Research** finds and verifies external info; **Know** holds domain understanding; investigation, law-enforcement, intelligence and counterintelligence work are **Know fields**, applied through Perceive, Kinesics, Research and Connect. |
| Work vs dedicated skills | Dedicated Skills **outperform** a broad Work for specialised tasks. Work covers practical occupations without a dedicated skill. |
| First Aid vs Medicine | Folded — `Medicine (Emergency Care)`. |
| Law | A **Know field**, `Know (Law)`, not a dedicated skill. |
| Tactics | Covered by **Lead** (command and crisis) plus a relevant **Know** field; **no** separate Tactics skill, to keep the list flat. |

## UNSA academy alignment (issue #158)

Issue #159 is asked to review issue #158 (UNSA Academy core training) for the police,
investigation and counterintelligence Skills it requires. The academy's needs map onto the
universal list **without adding a skill per need** — the specialist *knowledge* lives in
`Know` fields, and the rest is covered by the universal Skills:

| #158 need | NoöPunk representation |
| --- | --- |
| Firearms | **Guns** |
| Unarmed combat | **Unarmed** |
| Melee / stun baton | **Melee** |
| Athletics / fitness | **Athletics** |
| Room entry, cover, team movement | **Lead** + `Know (Law Enforcement)` (no separate Tactics skill) |
| First aid / trauma care | **Medicine (Emergency Care)** |
| Law / criminal procedure | `Know (Law)` |
| Investigation | `Know (Investigation)` |
| Interview / interrogation | **Talk**, **Provoke**, **Kinesics** |
| Forensics | `Medicine (Forensics)` |
| Observation / perception | **Perceive** |
| Surveillance / countersurveillance | **Sneak** + `Know (Counterintelligence)` |
| Police procedure / chain of custody | `Know (Law Enforcement)` |
| Intelligence analysis | `Know (Intelligence)` |
| Counterintelligence | `Know (Counterintelligence)` |
| HUMINT | **Connect**, **Talk** + `Know (Intelligence)` |
| OSINT | **Research** |
| Detect deception | **Kinesics** (opposes **Deceive**) |
| Secure communications / crypto | **Infosec**, **Program** |
| X-risk recognition | `Know (X-Risk Studies)` |
| NHI studies / anomalous phenomena | `Know (NHI Studies)` |

The machine-readable mapping is `unsa_academy_alignment` in [`data/rules/skills.json`](../data/rules/skills.json).
New `Know` fields are added only when a scenario or academy track actually needs them — the
campaign profile is not pre-populated (issue #110's rule, reaffirmed here).

## Attribute flexibility

Most Skills use a fixed attribute. The flexible Skills are **Administrate** (INT by default;
SOC when the task is leading people or institutional politics), **Work** (set by the field),
**Perform** (PSY by default; SOC when the performance is primarily social persuasion), and
**Melee** (FIT by default; REF for finesse weapons). The default is always the stated one; the
alternative applies only when the task clearly calls for it.

## What this chapter does not define

This chapter fixes the **skill list, attributes, trained/untrained status and specialization
rule** — nothing more. Specifically still deferred, and not to be inferred from this chapter:

- combat resolution, damage, defence procedure (Fray is named; its combat use is later);
- hacking / cyberspace procedures and whether the withdrawn BCI/Compute/Connection concepts return;
- psionic powers, sleights, their effects and resolution;
- the number of Skills a starting character has, and at what levels;
- advancement / XP;
- cyberware, augmentation and equipment statistics;
- the full campaign field catalogue (extend `data/rules/campaign_skill_fields.json` as play needs it).

## Machine-readable form

The canonical machine-readable list is [`data/rules/skills.json`](../data/rules/skills.json).
The universal `RULEBOOK.md` §4 summary and the campaign-scoped profile
[`data/rules/campaign_skill_fields.json`](../data/rules/campaign_skill_fields.json) both
derive from it.
