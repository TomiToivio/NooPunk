# Attributes

> **Status: NOÖPUNK NATIVE — author decision on issue #131**
>
> NoöPunk uses an independent **1–10 STAT** model with **six base STATS**:
> **FIT / REF / INT / SOC / CYB / PSY**.
>
> The base model is deliberately small. Deeper complexity lives in the **domain layers** —
> the Physical, Social, Psychic and Cybernetic systems — not in an enlarged universal
> attribute list.

## Core principles

- **Six base STATS, one universal sheet.** Every character-scale actor uses the same six.
- **Fitness (FIT)** is general physical capability.
- **Reflexes (REF)** is speed, coordination, reaction time and dexterity.
- **Intelligence (INT)** is general cognitive ability, reasoning, learning and knowledge.
- **Social (SOC)** is social skill, communication and charisma.
- **Cybernetics (CYB)** is cyberspace- and cyborg-native technical aptitude.
- **Psyche (PSY)** is consciousness, willpower, psychic resilience, psionics and related
  inner capacities.
- **Social and Psychic remain distinct.** Language and symbolic reasoning belong to the
  Social layer; phenomenal consciousness and Noetic capability belong to the Psychic layer.
- **There is no generic Mental/Ego layer.**
- **Cybernetic is not intelligence.**
- **Density is not IQ.**
- **Polarization is not alignment.**
- **Complexity is added in the domain layers, not multiplied into the base attributes.**

Ordinary human STAT ratings use **1–10**. A layer that does not operate for an entity is
**N/A** in human-readable sheets and **null** in machine-readable data.
**0 is not used for absence**, because 0 would blur the difference between "this layer
does not operate for this entity" and "this entity operates in the layer but is extremely
poor at it."

## The six base STATS

### Fitness (FIT)

General physical capability: strength, muscular power, endurance, exertion, lifting,
climbing, running, sustained physical output, and resistance to physical strain.

FIT is deliberately one stat rather than a strength/toughness pair. Where a scenario needs
to distinguish "strong" from "hardy", that distinction is expressed through **traits** or
**statuses** (or a scenario-local derived value), not by adding a seventh base STAT.

### Reflexes (REF)

Speed, coordination, reaction time, balance, agility, fine bodily timing, hand-eye
coordination, and rapid physical response.

Dexterity and Movement are both **readings of REF**, not separate attributes: "Dexterity" is
how REF expresses itself in fine-motor contexts, and movement rate is a **derived value**
influenced by REF, FIT and embodiment.

### Intelligence (INT)

General cognitive ability: reasoning, analysis, abstraction, interpretation, planning,
learning, memory, and the ability to work with knowledge.

INT belongs to the Social layer because NoöPunk treats human symbolic cognition as
inseparable from language, communication, institutions and accumulated culture. This does
**not** mean that non-human or non-linguistic consciousness lacks cognition.

INT is not a skill. Engineering, science, programming, medicine and similar learned
domains are **Skills** that pair with INT or another fitting STAT.

### Social (SOC)

Social skill, communication, and charisma: expression, composure, persuasion, performance,
leadership, intimidation, social perception, and the management of one's public role.

SOC is intentionally a single broad stat. The **Social Systems** layer carries the real
complexity: Affect, Contacts, Factions, Reputation, Motivations and the Social Network
Graph. Empathy, presence, deception and rhetoric are **Skills** used with SOC (or with
another STAT where the fictional method changes), not separate base attributes.

### Cybernetics (CYB)

Cyberspace- and cyborg-native technical aptitude: the character's facility with
computational systems, interfaces, and their own cybernetic extensions.

CYB becomes operative for a character with BCI, implants, a synthetic subsystem, direct
neural interfaces, machine embodiment, or an equivalent functional coupling. A biological
human who uses ordinary external tools may have the Cybernetic layer as **N/A** while still
using ordinary computers through INT and learned Skills.

> **CYB is a character stat. COMPUTE / INTERFACE / NETWORK are not.**
>
> The computational capacity of a deck, implant, agent or machine — throughput,
> interface quality, connectivity, storage — is a property of that **equipment**, and is
> recorded as **hardware/system statistics** with the device. A character's CYB rating and
> a deck's system ratings are different kinds of number and must not be collapsed into one.

### Psyche (PSY)

Consciousness, willpower, psychic resilience, psionics, and related inner capacities:
self-direction, concentration, intentional control, persistence, psychic resistance, and
the ability to maintain a chosen course under internal or Noetic pressure.

**PSY is a base capacity, not a full psionics subsystem.** Characters with psychic
awareness or awakened abilities get their actual psionic capabilities — powers, techniques,
their limits and their costs — modeled in the **Psychic Systems** layer. A Sleeper and an
adept differ in what the Psychic layer grants them, not in their base STAT list.

PSY measures capability, not spiritual worth or Density. A powerful psychic can be
immature, unpolarized, destructive, confused, or ethically ordinary.

## The four-layer ontology is unchanged

The six base STATS do not replace the four ontological layers. **Physical, Social, Psychic
and Cybernetic** remain the layers through which characters participate in the world, and
NoöPunk adds **Cybernetic** as its own extension rather than attributing it to Luhmann.
The layers describe *modes of participation*; the six STATS are the universal ratings that
sit across them.

| Layer | What it describes | Related base STATS |
| --- | --- | --- |
| Physical | embodied material and biological capability | FIT, REF |
| Social | language, communication, institutions, identity, discourse | INT, SOC |
| Psychic | phenomenal consciousness, Noetic capability, PSI | PSY |
| Cybernetic | direct functional coupling to machines and networks | CYB |

This mapping is a **reading of emphasis**, not a partition: the four layers are modes of
participation, and the six STATS are universal. An entity may be fully described by fewer
operative layers, and a STAT may serve more than one layer depending on the action.

## Skills remain separate

NoöPunk keeps the rule established in #111:

```text
STAT + Skill + 1d10
```

A skill describes learned practice. A STAT describes the capability through which that
practice is expressed. The same skill may pair with different STATS when the fictional
method changes. Examples:

- ordinary network research may use **INT + Research**;
- reading a witness may use **SOC + Kinesics**;
- coercive command may use **SOC + Persuade/Provoke**;
- an athletic feat may use **FIT + Athletics**;
- a delicate technical task may use **REF + Hardware**;
- resisting psychic intrusion may use **PSY + Psi** or a future resistance skill;
- direct BCI machine control may use **CYB + Interface/Pilot**;
- technical work on ordinary external computers may use **INT + Program** when no direct
  cybernetic coupling is involved.

Exact pairings belong to the skill-design and playtest passes. The attribute model should
not silently turn skills back into fixed aptitude aliases, and it should not multiply base
STATS to represent competence that a skill already covers.

## Derived values

Values calculated from other properties are **derived values**, not STATS. This includes
movement rate, carrying capacity, wound threshold, initiative, and similar outputs.
Cyberware, implants and decks may supply additional derived capacities such as bandwidth or
storage; those belong to the equipment's system statistics, not to the character's six
base STATS.

Do not promote a derived value to a base STAT merely because it is frequently used.

## Absent layers

Use three distinct states:

1. **N/A / null** — the layer or STAT is not meaningfully operative for this entity.
2. **1–10** — the layer is operative within the ordinary human-scale rating.
3. **11+ effective** — superhuman/transhuman/NHI performance, normally produced by
   augmentation, non-human embodiment, PSI, or another explicit exception.

Examples:

| Entity | Physical | Social | Psychic | Cybernetic |
| --- | --- | --- | --- | --- |
| ordinary biological human without direct cybernetics | 1–10 | 1–10 | 1–10 | N/A |
| cybernetically augmented human | 1–10 | 1–10 | 1–10 | 1–10 |
| animal | operative | limited/nonhuman | operative | usually N/A |
| non-conscious software AI | N/A | operative | N/A | operative |
| conscious AGI | platform-dependent | operative | operative | operative |
| non-conscious robot | operative | possibly operative | N/A | operative |
| Noetic entity | possibly N/A | possibly operative | operative | possibly N/A |

"No human-compatible language" does not imply "no Social layer." A nonhuman entity may
participate socially through telepathy, chemical signaling, machine protocols, collective
signaling, symbolic geometry, or other media.

## Cybernetic augmentation and the 1–10 human scale

For biological humans, the unaugmented/base STAT remains on the **1–10** scale.

Cybernetics can later affect a STAT in three ways:

1. **unlock** an otherwise unavailable Cybernetic capability;
2. provide a **situational modifier** to an existing STAT + Skill check;
3. produce an **effective** STAT above 10 when an augmentation genuinely exceeds ordinary
   human capacity.

Keep base and augmentation visible separately. For example:

```text
REF 8
augmentation: +3 reflex accelerator
effective REF: 11 when the accelerator applies
```

The same principle separates a character from their equipment: a deck's COMPUTE,
INTERFACE and NETWORK ratings are the **deck's** statistics, and they modify or enable
what the character can do without rewriting the character's own CYB.

Do not let routine gear permanently rewrite the biological base score. This keeps the
human 1–10 scale legible while leaving room for cyborgs, transhumans, NHI, and machine
entities.

# Density

> **Density is a developmental state of consciousness, not a STAT and not IQ.**

Represent Density as a **tier/state**, normally written **1D–7D** for NPC/world-model
purposes.

- PCs normally begin in **3D** or, with explicit campaign permission, **4D**.
- 5D–7D are not ordinary advancement tiers for player characters.
- A high-INT scientist can be 3D.
- A low-INT being can be 4D.
- PSY may affect how a character experiences or handles awakening, but it does not
  determine Density.

## 3D → 4D awakening

A 3D PC may have a **six-segment Awakening Clock**.

Advance the clock only for major fictional developments involving sustained integration
of consciousness, catalyst, PSI/Noetic experience, energy-center development, or
polarization. Do not award segments for ordinary XP, successful skill checks, or merely
having a high PSY.

When the sixth segment is filled, the character becomes **eligible** for a 4D transition.
The transition should occur through a significant story event, not automatically at the
instant the clock fills. It may involve a stable change in perception, identity,
relationships, PSI, or participation in the Noösphere.

A 4D transition does **not** grant blanket numerical superiority. Any mechanical benefits
must be explicit and narrow.

# Polarization

> **Polarization is a dynamic history of orientation expressed through sustained action,
> not a chosen good/evil alignment.**

Track Polarization on a separate scale:

```text
-100 ← Service to Self (StS) ... 0 ... Service to Others (StO) → +100
```

Characters normally begin near 0 unless their history clearly establishes otherwise.

Use the Law-of-One-inspired asymmetry as a setting rule:

- **+51 or higher**: clearly StO-polarized;
- **-95 or lower**: clearly StS-polarized;
- between those thresholds: mixed, developing, conflicted, or unpolarized.

These thresholds are not moral scores and do not replace roleplaying. They represent the
setting's metaphysical model of sustained orientation.

## How Polarization changes

Change Polarization because of **meaningful patterns of choice**, not isolated cosmetic
acts. A major action may shift the score by roughly **1–5 points**, with repeated
consistent behavior mattering more than one dramatic gesture.

Examples of StO-polarizing patterns include voluntary aid, solidarity, costly protection,
truthful cooperation, respect for agency, and building reciprocal capacity in others.

Examples of StS-polarizing patterns include domination, instrumentalization, coercive
control, deliberate hierarchy for personal power, and systematically converting other
agents into extensions of the self.

Context matters. Sacrifice can be manipulative. Self-interest can be healthy. Violence can
protect others. Cooperation can conceal domination. The GM/system should judge the
orientation of the sustained action, not match keywords.

## Social, Psyche, and Polarization

- **SOC** can help a character understand others and recognize opportunities for StO
  action. It does not award StO points by itself.
- **PSY** can help a character maintain self-directed control and execute StS strategies.
  It does not award StS points by itself.
- A low-SOC character may become strongly StO through principle, discipline, or chosen
  solidarity.
- A high-SOC character may use exquisite understanding of others for manipulation.
- A low-PSY character can still drift into selfishness without becoming strongly
  polarized.
- A high-PSY character can be a disciplined protector.

# Seven energy centers

The energy centers are **developmental states**, not extra STATS, and they are **not** a
one-to-one map of the six base STATS.

Treat them as **developmental states spanning layers**. Each center may be recorded as:

- **Blocked**
- **Active**
- **Balanced**
- **Integrated**

This vocabulary is developmental, not a second 1–10 competence scale.

| Center | Primary concerns | Strongest layer relationships |
| --- | --- | --- |
| Red | survival, embodiment, vitality, basic material existence | Physical |
| Orange | selfhood, intimacy, one-to-one relation, personal desire | Psychic + Social |
| Yellow | groups, roles, institutions, status, collective identity | Social |
| Green | compassion, reciprocity, care, opening beyond self-interest | Social + Psychic |
| Blue | communication, truthful expression, listening, shared meaning | Social |
| Indigo | disciplined consciousness, intuition, PSI, Noetic work | Psychic |
| Violet | whole-system signature / integration | derived from the whole character |

The **Cybernetic** layer sits outside the chakra map. Technology can nevertheless affect
conditions at any center: a BCI may aid communication, a psychotronic device may amplify
Indigo work, surveillance may distort Yellow-center relations, and cybernetic embodiment
may alter Red-center experience. Cybernetics does not become an eighth chakra.

Energy centers may later serve as prerequisites, permissions, risks, or modifiers for
specific PSI/awakening mechanics. Do not give automatic generic bonuses merely for marking
a center "Integrated."

# Biological-human-first kernel

Implement the first playable character kernel around:

- biological humans;
- optional cybernetic augmentation;
- the six base STATS;
- separate 1–10 skills;
- PSI via the Psychic Systems layer;
- Density;
- Polarization;
- Contacts / Factions / Motivations;
- UNHSS / Firewall field agents.

Defer until this model is stable:

- cortical-stack continuity mechanics;
- full resleeving;
- morph switching/catalogs;
- forks and backups;
- infomorph edge cases.

Later transhuman rules must map onto this model rather than replacing it.
