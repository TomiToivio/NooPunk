# Attributes

> **Status: NOÖPUNK NATIVE — issue #131 supersedes issue #113.**
>
> NoöPunk uses an independent **1–10 STAT** model. Six universal base STATs —
> **FIT / REF / INT / SOC / CYB / PSY** — describe the character. They are organized
> by four ontological layers: **Physical, Social, Psychic, and Cybernetic**. These
> layers describe different modes of participation in the world. They are not four
> skills and they do not collapse into a generic "Mental" or "Ego" layer.

## Core principles

- **Physical** is embodied material and biological capability.
- **Social** is language, symbolic reasoning, communication, identity, institutions,
  discourse, and understanding other agents.
- **Psychic** is phenomenal consciousness, self-directed awareness, intuition, PSI, and
  Noetic capability.
- **Cybernetic** is direct functional coupling to computation, AI, BCI, networks, and
  machines.
- **Language is Social.**
- **Psychic and Social are distinct.**
- **Cybernetic is not intelligence.**
- **Density is not IQ.**
- **Polarization is not alignment.**

## Why six base STATs

An earlier draft (issue #113) grew to twelve STATS. That made every interesting concept
its own universal dial and left the character sheet hard to read. The author's direction
on issue #131 is the opposite: **keep the universal layer small and put complexity into
the domain layers.**

- The base STATs cover only what *every* character needs a universal, rolled number for.
- The **Social Systems** layer carries social complexity: Affect, Factions, Motivations,
  Reputation, Contacts, reputation networks, and persuasion procedures.
- The **Psychic Systems** layer carries psychic complexity: PSI domains, awakening, the
  seven energy centers, Noetic techniques, Density and Polarization.
- **Cybernetics keeps one base STAT (CYB).** Hardware and system properties — processing,
  bandwidth, storage, hardening, interfaces — are statistics of the *equipment and agents*
  a character controls (decks, implants, devices, software, AIs), not character attributes.
  See *Cybernetic hardware statistics* below.

Ordinary human STAT ratings use **1–10** when a STAT is operative. A missing layer is
represented as **N/A** in human-readable sheets and **null** in machine-readable data.
**0 is not used for absence**, because 0 would blur the difference between "this layer
does not operate for this entity" and "this entity operates in the layer but is extremely
poor at it."

## The six base STATS

| Layer | STAT | Code | Covers |
| --- | --- | --- | --- |
| Physical | Fitness | FIT | strength, stamina, exertion, gross motor power |
| Physical | Reflexes | REF | speed, coordination, reaction time, dexterity, balance |
| Social | Intelligence | INT | reasoning, learning, knowledge, language-mediated cognition |
| Social | Social | SOC | communication, charisma, projection, persuasion, empathy |
| Cybernetic | Cybernetics | CYB | cyberspace/cyborg-native aptitude; direct coupling to machines |
| Psychic | Psyche | PSY | consciousness, willpower, psychic resilience, psionics |

### Fitness (FIT)
Strength, stamina, gross motor capability, exertion, lifting, climbing, running, and
sustained physical output.

### Reflexes (REF)
Reaction speed, balance, agility, dexterity, fine bodily timing, hand-eye coordination,
and rapid physical response. **Dexterity** is the fine-motor reading of Reflexes;
**movement** is a derived value produced from Reflexes and Fitness together with
morphology, rather than a separate STAT.

### Intelligence (INT)
General cognitive ability: reasoning, learning, memory, knowledge, analysis, abstraction,
interpretation, planning, formal logic, and scientific reasoning.

Intelligence belongs to the Social layer because NoöPunk treats human symbolic cognition
as inseparable from language, communication, institutions, and accumulated culture. This
does **not** mean that non-human or non-linguistic consciousness lacks cognition.

### Social (SOC)
Aptitude for other agents and social space: communication, charisma, expression,
composure, projection, authority, persuasion, performance, leadership, intimidation,
reciprocity, interpersonal attunement, and management of one's public role.

Social can make Service-to-Others choices easier to perceive or enact, but **high Social
does not make a character StO**.

The finer distinctions an earlier draft split into separate *Empathy*, *Presence* and
*Reason* STATS — reading another mind versus projecting one's own, feeling with others
versus commanding them — are **Social Systems** mechanics. They are expressed through
that layer's Affect, Faction, Motivation, Reputation and Contact model plus learned
skills, not through additional base STATs.

### Cybernetics (CYB)
Cyberspace/cyborg-native technical aptitude and the depth of a character's **direct
coupling** to machine systems: BCI coherence, sensorimotor incorporation, implant
coordination, machine embodiment, command and control through cybernetic systems, and the
ability to treat technological components as part of the acting self.

A biological human who uses ordinary external tools but has no meaningful cybernetic
interface may have this layer as **N/A** while still using computers through Intelligence
and learned skills. Cybernetics measures the coupling, not learned hacking technique and
not general reasoning.

### Psyche (PSY)
The base STAT for consciousness, willpower, psychic resilience, psionics, and related
inner capacities: self-direction, concentration, intentional control, persistence,
psychic resistance, awareness and depth of consciousness, and PSI/Noetic potential.

Psyche measures a general capacity, not spiritual worth or Density. A powerful psychic can
be immature, unpolarized, destructive, confused, or ethically ordinary. A contemplative
character may have a deep, well-integrated Psyche with little usable PSI; a naturally
gifted but chaotic psychic may show the reverse. Characters with psychic awareness or
awakened abilities get their actual psionic capabilities — the PSI domains, techniques and
awakening mechanics — modelled in the **Psychic Systems** layer, and a Sleeper may carry
latent Psyche that mostly manifests as luck, intuition and weak anomalous effects.

## Cybernetic hardware statistics

Hardware and system properties are **not character attributes**. They are statistics of
the equipment, implants, devices, agents and decks a character has access to — the same
way a firearm has statistics that are not the character's STATS:

- **processing** — parallel computation, inference, simulation, cryptographic workload,
  running agents and processes;
- **bandwidth** — concurrent connections, throughput, remote presence, latency, routing,
  distributed and swarm operation;
- **storage** — datasets, model weights, exploit libraries, cached knowledge, archives,
  backups;
- **hardening** — isolation, sandboxing, authentication, exploit resistance, redundancy,
  compartmentalization, integrity protection.

Offensive hacking is learned technique and stays a **Skill**; defensive hardening is a
property of the target system. A check therefore reads as `INT or CYB + Hacking Skill`
rolled against a target's hardening rating, not `Attack stat` versus `Defence stat`.
Exact hardware statistics, their ranges and their conversion are deferred to the
Cybernetic Systems and equipment passes.

## Skills remain separate

Cross-system conversion tables for Cyberpunk RED, Eclipse Phase 2E, and Cities Without Number are maintained in [`docs/design/RPG_CONVERSION_REFERENCE.md`](../docs/design/RPG_CONVERSION_REFERENCE.md). They are interoperability aids only and do not expand the canonical six-STAT model or import another game's skill catalogue.

NoöPunk keeps the rule established in #111:

```text
STAT + Skill + 1d10
```

A skill describes learned practice. A STAT describes the capability through which that
practice is being expressed.

The same skill may sometimes pair with different STATS when the fictional method changes.
Examples:

- ordinary network research may use **INT + Research**;
- reading a witness may use **SOC + Kinesics**;
- coercive command may use **SOC + Persuade/Provoke**;
- resisting psychic intrusion may use **PSY + Psi** or a future resistance skill;
- receiving an anomalous impression may use **PSY + Psi**;
- direct BCI machine control may use **CYB + Interface/Pilot**;
- brute physical work may use **FIT + Athletics**.

Exact pairings belong to the skill-design and playtest passes. The attribute model should
not silently turn skills back into fixed aptitude aliases.

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
| non-conscious software AI | N/A | operative | N/A | operative |
| conscious AGI | platform-dependent | operative | operative | operative |
| non-conscious robot | operative | possibly operative | N/A | operative |
| Noetic entity | possibly N/A | possibly operative | operative | possibly N/A |
| animal | operative | limited/nonhuman | operative | usually N/A |

"No human-compatible language" does not imply "no Social layer." A nonhuman entity may
participate socially through telepathy, chemical signaling, machine protocols, collective
signaling, symbolic geometry, or other media.

## Cybernetic augmentation and the 1–10 human scale

For biological humans, the unaugmented/base STAT remains on the **1–10** scale.

Cybernetics can later affect a STAT in three ways:

1. **unlock** an otherwise unavailable Cybernetic STAT;
2. provide a **situational modifier** to an existing STAT + Skill check;
3. produce an **effective STAT above 10** when an augmentation genuinely exceeds ordinary
   human capacity.

Keep base and augmentation visible separately. For example:

```text
REF 8
augmentation: +3 reflex accelerator
effective REF: 11 when the accelerator applies
```

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
- PSY, and the psychic techniques built on it, may affect how a character experiences or
  handles awakening, but none of them determines Density.

## 3D → 4D awakening

A 3D PC may have a **six-segment Awakening Clock**.

Advance the clock only for major fictional developments involving sustained integration
of consciousness, catalyst, PSI/Noetic experience, energy-center development, or
polarization. Do not award segments for ordinary XP, successful skill checks, or merely
having high Psychic STATS.

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

Do **not** map the seven energy centers one-to-one onto the six STATS.

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

The **Cybernetic layer sits outside the chakra map**. Technology can nevertheless affect
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
- the six base STATS above;
- separate 1–10 skills;
- PSI;
- Density;
- Polarization;
- Contacts / Factions / Motivations;
- UNSA field agents.

Defer until this model is stable:

- cortical-stack continuity mechanics;
- full resleeving;
- morph switching/catalogs;
- forks and backups;
- infomorph edge cases.

Later transhuman rules must map onto the four-layer ontology rather than replacing it.
