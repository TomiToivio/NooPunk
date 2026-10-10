# RPG conversion and correspondence reference

> **Status: conversion/reference appendix for issue #135.**
>
> NoöPunk is an independent system. These opt-in tables convert characters *from* other
> games *into* the native NoöPunk **1–10 STAT + 1–10 Skill + 1d10** rules, for
> interoperability only. No external system is a parent, a baseline or an implementation
> source for these rules, and nothing here imports another game's attribute or skill
> catalogue.

## Design rule

NoöPunk keeps the compact six-STAT model:

- **Fitness (FIT)**
- **Reflexes (REF)**
- **Intelligence (INT)**
- **Social (SOC)**
- **Cybernetics (CYB)**
- **Psyche (PSY)**

When a source game has several narrow skills that fit one NoöPunk skill, convert them
into the broad NoöPunk skill and preserve important detail as a specialization, trait,
piece of equipment, or subsystem feature.

```text
many source skills -> one broad NoöPunk skill
```

Do not create a new universal NoöPunk skill merely because a source game has one.

## STAT correspondence

| NoöPunk | Cyberpunk RED | Eclipse Phase 2E | Cities Without Number | Notes |
| --- | --- | --- | --- | --- |
| **Fitness (FIT)** | BODY; MOVE when speed matters | SOM | STR + CON | Strength, stamina and embodied exertion. For RED, BODY is the default source; MOVE is only relevant when the conversion is specifically about locomotion. For CWN, average STR and CON after converting each score. |
| **Reflexes (REF)** | REF + DEX | REF | DEX | RED splits reaction speed and fine coordination; average REF and DEX when both matter, otherwise use the most relevant one. |
| **Intelligence (INT)** | INT; TECH as a task-specific secondary reference | COG + INT | INT + WIS | NoöPunk INT is broad symbolic/analytic cognition. Average the paired source attributes when both clearly contribute. Learned technical practice remains a Skill. |
| **Social (SOC)** | EMP + COOL | SAV | CHA; WIS when reading a situation matters | RED splits interpersonal sensitivity and composure/presence. CWN CHA is the default; WIS is a situational secondary source for social perception. |
| **Cybernetics (CYB)** | No direct equivalent; TECH is only a rough proxy | No direct aptitude; COG plus Interface/Infosec/Program are useful references | No direct equivalent; INT plus Program/Fix are useful references | CYB measures cybernetic/cyberspace-native coupling, not general technical intelligence. If the source character has no meaningful direct cybernetic coupling, use **N/A** rather than inventing a score. |
| **Psyche (PSY)** | WILL; EMP may inform empathy but is not PSY | WIL; Psi skill describes trained psi use | WIS is only a rough proxy | PSY covers will, consciousness, psychic resilience and psionic potential. Do not infer active psionics solely from a high converted PSY. |

When two source attributes map to one NoöPunk STAT, convert both first, average them, and
round to the nearest whole number. If only one is fictionally relevant, use that one.

## Cyberpunk RED -> NoöPunk

Cyberpunk RED already uses a broadly comparable 1–10 STAT scale. Keep conversion simple.

### RED STATs

Default rule:

```text
NoöPunk STAT = closest semantically relevant RED STAT value
```

For split concepts:

- **REF**: average RED **REF + DEX** when both reaction and dexterity matter.
- **SOC**: average **EMP + COOL** when both social attunement and composure/presence matter.
- **FIT**: use **BODY** by default; consult **MOVE** only for locomotion-heavy conversions.
- **INT**: use **INT** by default. Do not automatically fold **TECH** into intelligence.
- **PSY**: use **WILL** by default.
- **CYB**: there is no direct RED character STAT equivalent. Assign a CYB score only if
  the fiction establishes genuine cybernetic/BCI/cyberspace-native coupling.

### RED skills

A close RED skill may carry its numeric rating across approximately **1:1** when a close
NoöPunk skill already exists.

Do not import the RED skill catalogue. If several RED skills fit one broad NoöPunk skill,
use the highest relevant source skill as the starting rating and preserve other meaningful
training as specializations.

Example:

```text
several narrow RED weapon/technical/social skills
        -> one broad NoöPunk skill
        + specializations where they matter
```

## Eclipse Phase 2E -> NoöPunk

Eclipse Phase separates **aptitudes** (0–30) from learned **skills** (0–100). They should
not use the same conversion table.

### EP2 aptitudes -> NoöPunk STATs

EP2 aptitude checks use **aptitude × 3**. Convert that normal check value into the same
decade bands used for percentile skills. This preserves EP2's own meaning of the aptitude
scale and is still table-fast.

| EP2 aptitude | Aptitude check | NoöPunk |
| ---: | ---: | ---: |
| 0–3 | 0–9 | 1 |
| 4–6 | 12–18 | 2 |
| 7–9 | 21–27 | 3 |
| 10–13 | 30–39 | 4 |
| 14–16 | 42–48 | 5 |
| 17–19 | 51–57 | 6 |
| 20–23 | 60–69 | 7 |
| 24–26 | 72–78 | 8 |
| 27–29 | 81–87 | 9 |
| 30+ | 90+ | 10 |

This means an EP2 aptitude of **15**, the ordinary transhuman baseline in EP2, becomes a
NoöPunk **5**. An unaugmented-human-style EP2 aptitude around **10** becomes **4**.

### EP2 learned skills -> NoöPunk Skills

| Eclipse Phase skill | NoöPunk Skill |
| ---: | ---: |
| 0–9 | 1 |
| 10–19 | 2 |
| 20–29 | 3 |
| 30–39 | 4 |
| 40–49 | 5 |
| 50–59 | 6 |
| 60–69 | 7 |
| 70–79 | 8 |
| 80–89 | 9 |
| 90+ | 10 |

Use the character's **final EP2 skill value** as the source number.

EP2 competence bands line up well with this intentionally coarse conversion: low values
remain rudimentary, the professional middle lands near the middle of NoöPunk's scale, and
expert/master values land in the upper bands.

### EP2 specializations

An EP2 specialization normally gives **+10** when applicable. After converting the base
skill, record the specialization by name and apply **+1** to the NoöPunk skill for that
specialized use, capped at 10.

```text
EP2 Guns 70 (Beam Weapons)
-> NoöPunk broad ranged-combat skill 8
-> Beam Weapons specialization: +1 when applicable
```

If the eventual NoöPunk skill design gives specializations a different native mechanic,
use that mechanic instead of permanently raising the base skill.

### EP2 values and bonuses above 100

NoöPunk's base Skill scale stops at **10**.

- Convert any EP2 final/effective value of **90+** to **10**.
- Do not turn temporary bonuses above 100 into permanent Skill levels.
- Preserve extraordinary source advantages as situational modifiers, traits, equipment,
  morph features, pools, or other subsystem effects when they matter.

### EP2 morph/body effects

Convert the **ego** first: aptitudes and learned skills belong to the character's
persistent identity. Then convert morph effects separately.

Morph-provided durability, pools, implants, movement modes, armor, body form, and similar
effects should become NoöPunk Physical/Cybernetic equipment, traits, statuses, derived
values, or explicit modifiers. Do not bake all of them permanently into the six base STATs.

## Eclipse Phase 2E skill reference

This is a **mapping worksheet**, not a NoöPunk skill list.

| Eclipse Phase 2E skill | Type / useful grouping | Proposed NoöPunk equivalent | Decision |
| --- | --- | --- | --- |
| Athletics | Physical | TBD | TBD |
| Deceive | Social | TBD | TBD |
| Exotic Skill: [Field] | Field / special | TBD | TBD |
| Fray | Combat / defense | TBD | TBD |
| Free Fall | Physical / microgravity | TBD | TBD |
| Guns | Combat | TBD | TBD |
| Hardware: [Field] | Technical / field | TBD | TBD |
| Infiltrate | Physical / stealth | TBD | TBD |
| Infosec | Technical / cyber | TBD | TBD |
| Interface | Technical / cyber | TBD | TBD |
| Kinesics | Social / perception | TBD | TBD |
| Know: [Field] | Knowledge / field | TBD | TBD |
| Medicine: [Field] | Technical / medical / field | TBD | TBD |
| Melee | Combat | TBD | TBD |
| Perceive | Mental / perception | TBD | TBD |
| Persuade | Social | TBD | TBD |
| Pilot: [Field] | Vehicle / field | TBD | TBD |
| Program | Technical / cyber | TBD | TBD |
| Provoke | Social | TBD | TBD |
| Psi | Psychic | TBD | TBD |
| Research | Technical / information | TBD | TBD |
| Survival | Physical / fieldcraft | TBD | TBD |

Open-ended EP2 field skills should normally become a broad NoöPunk skill plus a
specialization or domain rather than dozens of universal skills.

Common EP2 field examples include:

- **Hardware:** Aerospace, Armorer, Demolitions, Electronics, Groundcraft, Industrial,
  Nautical, Robotics.
- **Medicine:** Biotech, Forensics, Paramedic, Pharmacology, Psychosurgery.
- **Pilot:** Air, Ground, Nautical, Space.
- **Exotic Skill:** only use when the activity genuinely falls outside ordinary broad
  NoöPunk skills.
- **Know:** retain the field name as a knowledge domain/specialization rather than
  automatically creating a new universal skill.

## Cities Without Number -> NoöPunk

CWN attributes run from **3–18** and skills from **untrained / level 0–4**. Convert them by
competence band, not probability reconstruction.

### CWN attributes -> NoöPunk STATs

| CWN attribute score | CWN modifier | NoöPunk |
| ---: | ---: | ---: |
| 3 | -2 | 1 |
| 4–5 | -1 | 2 |
| 6–7 | -1 | 3 |
| 8–9 | +0 | 4 |
| 10–11 | +0 | 5 |
| 12–13 | +0 | 6 |
| 14–15 | +1 | 7 |
| 16 | +1 | 8 |
| 17 | +1 | 9 |
| 18+ | +2 or exceptional | 10 |

The CWN modifier remains a useful sanity check: negative modifiers map low, +0 occupies the
middle, +1 maps high, and +2 marks peak ordinary-human competence.

When a NoöPunk STAT uses two CWN attributes, convert each source attribute first, average
the converted values, then round normally.

### CWN skills -> NoöPunk Skills

| CWN skill level | Meaning for conversion | NoöPunk |
| ---: | --- | ---: |
| Untrained / no skill | lacks trained competence | 1 |
| 0 | basic trained competence | 2 |
| 1 | practiced | 4 |
| 2 | veteran / advanced | 6 |
| 3 | master-level | 8 |
| 4 | peak / legendary | 10 |

The spacing is deliberate. It leaves room inside the 1–10 NoöPunk scale for later
advancement, specializations, gear and situational modifiers instead of pretending CWN's
five trained levels contain ten distinct probability bands.

## Cities Without Number skill reference

This is a conversion worksheet only.

| Cities Without Number skill | Proposed NoöPunk equivalent | Decision |
| --- | --- | --- |
| Administer | TBD | TBD |
| Connect | TBD | TBD |
| Drive | TBD | TBD |
| Exert | TBD | TBD |
| Fix | TBD | TBD |
| Heal | TBD | TBD |
| Know | TBD | TBD |
| Lead | TBD | TBD |
| Notice | TBD | TBD |
| Perform | TBD | TBD |
| Program | TBD | TBD |
| Punch | TBD | TBD |
| Shoot | TBD | TBD |
| Sneak | TBD | TBD |
| Stab | TBD | TBD |
| Survive | TBD | TBD |
| Talk | TBD | TBD |
| Trade | TBD | TBD |
| Work | TBD | TBD |

## Conversion procedure

For any imported character:

1. Convert only the source attributes needed for the six canonical NoöPunk STATs.
2. Use **N/A** for CYB or another layer that genuinely is not operative rather than
   inventing a number.
3. Identify the source skills that actually matter to the character concept.
4. Map them into the **smallest reasonable set of broad NoöPunk skills**.
5. Preserve narrow expertise as specializations, traits, equipment or layer-specific
   mechanics.
6. Keep source-system body, cyberware, morph, psi, reputation and similar extras outside
   the six-STAT conversion unless they truly describe a base character capacity.
7. Re-read the resulting character as a NoöPunk character. Conversion should preserve the
   concept, not reproduce every source probability.

## Sources used to validate the scales

- Eclipse Phase 2E online rules: Character Stats, Skills, Active Skill List, and Total
  Skills.
- Cities Without Number SRD: Attributes, Skills, and Character Advancement.
- Cyberpunk RED is used only as a correspondence/reference scale here; its full STAT and
  skill catalog is intentionally not reproduced.
