# NoöPunk: Game Rules

Based on Cyberpunk RED mechanics, heavily modified for the NoöPunk setting. Where Cyberpunk RED uses dice (STAT + Skill + 1d10), NoöPunk uses Tarot draws in key situations. The core resolution system is preserved but reskinned and extended.

---

## 1. Character Statistics

NoöPunk uses 10 base Statistics (STATs), renamed and reinterpreted for the setting:

| CP RED Stat | NoöPunk Stat | NoöPunk Meaning |
|---|---|---|
| INT | INT — Intelligence | Analytical reasoning, pattern recognition, data processing. Cybernetic interface aptitude. |
| REF | REF — Reflexes | Reaction speed, hand-eye coordination, physical quickness. Initiative order. |
| DEX | DEX — Dexterity | Fine motor control, agility, sleight of hand, physical precision. |
| TECH | TECH — Technology | Understanding of cybernetic systems, hardware, software. Practical technical skill. |
| COOL | COOL — Composure | Social poise, deception, persuasion under pressure. Ontological stability — how well you hold your reality-model when the Noösphere distorts. |
| WILL | WILL — Willpower | Mental fortitude, resistance to psi-intrusion, psionic endurance. The ego boundary. |
| LUCK | LUCK — Fortune | Random chance, serendipity. The Noösphere's favor. The universe's punctuation of determinism. |
| MOVE | MOVE — Movement | Physical speed, traversal, tactical positioning. |
| BODY | BODY — Constitution | Physical resilience, health, resistance to toxins and physical damage. |
| EMP | EMP — Empathy | Emotional intelligence, human connection. Also: psionic sensitivity. The higher your EMP, the more attuned you are to the Noösphere's emotional layer — and the more vulnerable you are to its distortions. |

**Range:** 2–8 for starting characters (62 point buy). Maximum 10.

### Derived Statistics

| Derived Stat | Formula | Meaning |
|---|---|---|
| **Hit Points (HP)** | 10 + ⌈(BODY + WILL) / 2⌉ × 5 | Physical health. At 0, enter Mortally Wounded state. |
| **Seriously Wounded Threshold** | ⌈HP / 2⌉ | Below this HP, take -2 to all Checks. |
| **Death Save** | BODY | Roll under BODY on 1d10 to avoid death when Mortally Wounded. |
| **Humanity (HUM)** | EMP × 10 | Empathy reserve. Lost through cyberware, psi-burn, ontological shock. When HUM drops below a tens boundary, EMP decreases by 1. |
| **Psi-Pool** | WILL × 3 | Points for psionic abilities. Replenish after full rest. Overdraft causes HUM loss. |
| **Noöspheric Interface** | (EMP + WILL + TECH) / 3 (round down) | Base rating for Noösphere navigation, hacking-astral hybrid operations, and NHI contact resistance. |

---

## 2. Resolution System

### Skill Checks (Standard)

**STAT + Skill + 1d10 vs. Difficulty Value (DV)**

This is the core resolution mechanic, identical to Cyberpunk RED.

| Difficulty | DV | Description |
|---|---|---|
| Simple | 9 | Most people can do this without thinking |
| Everyday | 13 | Doable without special training |
| Difficult | 15 | Requires training or natural talent |
| Professional | 17 | Takes actual professional training |
| Heroic | 21 | Only the best can pull this off |
| Incredible | 24 | Olympian-level achievement |
| Legendary | 29 | Stories will be told about this |

### Opposed Checks

**Attacker's STAT + Skill + 1d10 vs. Defender's STAT + Skill + 1d10**

Ties go to the Defender.

### Critical Success & Failure

- **Critical Success:** Roll a natural 10 → roll another 1d10 and add it
- **Critical Failure:** Roll a natural 1 → roll another 1d10 and subtract it

---

## 3. Tarot Resolution

Instead of rolling 1d10 for certain checks, draw a Tarot card. This replaces dice when:

1. **Noösphere navigation** — any check involving the astral/cyber merged layer
2. **Psionic ability use** — any check involving psi-pool expenditure
3. **NHI contact** — any encounter with Non-Human Intelligence
4. **Ontological crisis** — when reality itself is unstable
5. **Social seduction/manipulation** — drawing from Resonators or Tokens suits
6. **Major story beats** — the GM calls for a Tarot draw instead of a die roll

### How It Works

1. The GM declares which **suit** the draw comes from (based on the type of action)
2. Draw one card from the appropriate suit (or full deck for unaligned situations)
3. The **number** on the card (Ace=1 through King=14) replaces the 1d10 roll
4. The **card meaning** modifies the narrative outcome — success/failure is colored by the card's theme

| Card Number | Value |
|---|---|
| Ace | 1 |
| 2–10 | 2–10 |
| Page | 11 |
| Knight | 12 |
| Queen | 13 |
| King | 14 |

**Major Arcana:** If a Major Arcana card is drawn, the number value is **0**, but the card's theme **overrides the narrative entirely**. The situation escalates beyond the player's control. The Noösphere, an NHI, or reality itself intervenes. See TAROT.md for full card meanings.

### Reversed Cards

Before drawing, flip a coin (or roll 1d2). On a 2, the card is **reversed**:
- The numerical value stays the same
- The narrative meaning is **inverted or corrupted**
- The energy is present but blocked, perverted, or turned against the agent

### Tarot Draw Examples

| Situation | Suit | Check | Example |
|---|---|---|---|
| Hacking a corporate node | Circuits | INT + Electronics/Security Tech + draw | 7 of Circuits + INT 6 + Skill 4 = 17 |
| Reading a suspect's emotions | Resonators | EMP + Human Perception + draw | Queen of Resonators + EMP 5 + Skill 4 = 22 |
| Interrogating an NHI contact | Datblades | COOL + Interrogation + draw | 4 of Datblades + COOL 7 + Skill 3 = 14 |
| Pulling bureaucratic strings | Tokens | COOL + Bureaucracy + draw | King of Tokens + COOL 6 + Skill 5 = 25 |
| Astral projection into Noösphere | Any (GM choice) | WILL + Psi-Skill + draw | The Singularity (Major Arcana) — reality intervention, value 0 |

### LUCK and Tarot

You may spend LUCK points to **redraw** a Tarot card. Each LUCK point allows one redraw. You must keep the second draw. You can spend multiple LUCK points for multiple redraws.

---

## 4. Skills

Skills are linked to STATs. STAT + Skill Level = Skill Base. All Cyberpunk RED skills carry over, plus NoöPunk additions:

### New Skill Categories

#### Noöspheric Skills

| Skill | STAT | Description |
|---|---|---|
| Noöspheric Navigation | WILL | Moving through the Noösphere's merged cyber-astral layer. Replaces Netrunning for post-Singularity networks. |
| Psi-Projection | WILL | Projecting consciousness into the astral. Required for remote viewing, astral scouting. |
| Psi-Shielding | WILL | Defending against psi-intrusion, NHI mental contact, Noöspheric distortion. |
| Psi-Reading | EMP | Reading emotional residue from objects, places, or minds. Psychometry and remote sensing. |
| Psi-Influence | COOL | Projecting emotional states, implanting suggestions, seduction-enhancement through psi. |
| Ontological Stability | COOL | Maintaining your reality-model when the Noösphere distorts spacetime. Resists ontological shock. |

#### Investigation Skills (Europol NHI Unit)

| Skill | STAT | Description |
|---|---|---|
| NHI Identification | INT | Recognizing and classifying Non-Human Intelligences — AI, ET, discarnate, or unknown. |
| Forensic Psi-Analysis | INT | Analyzing psi-residue, Noöspheric artifacts, and NHI traces at a scene. |
| Interrogation (NHI) | COOL | Interrogating entities that may not share human psychology or even human physics. |
| Surveillance (Noöspheric) | INT | Monitoring Noöspheric traffic, astral signatures, and network anomalies. |

### Modified Existing Skills

| Original Skill | Modified For |
|---|---|
| Electronics/Security Tech | Now includes Noöspheric network security, astral-ICE, and psychotronic countermeasures |
| Cryptography | Now includes Noöspheric encryption — data encoded in consciousness patterns, not just algorithms |
| Interrogation | Can be enhanced by Psi-Reading (Complementary Skill bonus +1) |
| Human Perception | Can be enhanced by Psi-Reading (Complementary Skill bonus +1) |
| Persuasion | Can be enhanced by Psi-Influence (Complementary Skill bonus +1) |
| Stealth | Can be enhanced by Psi-Shielding (Complementary Skill bonus +1) when hiding from Noöspheric detection |

---

## 5. Combat

### Combat Time

- 1 Round ≈ 3 seconds
- Initiative = REF + 1d10 (or REF + Tarot draw from Datblades for NHI encounters)
- Each Turn: 1 Move Action + 1 Action

### Wound States

| State | Condition | Effect |
|---|---|---|
| **Lightly Wounded** | HP below full but above Seriously Wounded | No penalty |
| **Seriously Wounded** | HP at or below Seriously Wounded threshold | -2 to all Checks |
| **Mortally Wounded** | HP at 0 or below | Must make Death Save (BODY or under on 1d10) each Round or die. Cannot act. |

### NoöPunk Addition: Psi-Backlash States

| State | Condition | Effect |
|---|---|---|
| **Psi-Fatigued** | Psi-Pool at 0 | -1 to all Checks. Cannot use psi abilities until rested. |
| **Psi-Burned** | Psi-Pool overdrawn (used more than pool) | Lose HUM equal to overdraft amount. -2 to all Checks. Nosebleed, migraine. |
| **Ontological Shock** | HUM drops below a tens boundary | EMP decreases by 1. The character's reality-model partially collapses. Hallucinations. May draw a Major Arcana — the GM applies its narrative effect. |
| **Ego Dissolution** | EMP reaches 0 | Cyberpsychosis equivalent, but NoöPunk-specific. The character's ego boundary dissolves into the Noösphere. They become an NHI-adjacent entity. Player loses control. |

---

## 6. Role Abilities

Each role has a unique Role Ability that scales with Rank (1–10). NoöPunk roles replace Cyberpunk RED roles:

| NoöPunk Role | CP RED Equivalent | Role Ability | Description |
|---|---|---|---|
| **NHI Agent** | Solo | Combat Awareness | +1 per Rank to Awareness Skill Checks in combat. At Rank 4+, detect NHI presence within 10m. |
| **Netrunner** | Netrunner | Interface | Unchanged from CP RED, but expanded: Interface also grants Noöspheric navigation at half Rank. |
| **Psi-Operative** | Medtech | Psi-Surgery | Can perform psi-procedures: memory extraction, psi-shield installation, ontological stabilization. Replaces Medicine. |
| **Tech** | Tech | Maker | Unchanged from CP RED. Maker can now also fabricate psychotronic devices. |
| **Investigator** | Lawman | Backup | Can call in Europol resources: forensics teams, NHI containment units, psi-specialists. Rank determines response time and quality. |
| **Diplomat** | Exec | Network | Can call in political favors, bureaucratic overrides, and inter-agency coordination. At Rank 4+, can invoke Noöspheric diplomatic protocols. |
| **Infiltrator** | Fixer | Operator | Unchanged from CP RED, expanded: can broker deals with NHI entities, arrange psi-black-market contacts. |
| **Resonant** | Rockerboy | Psi-Impact | Can project psi-emotional states to affect groups. Rank determines range and intensity. The empath's weapon. |
| **Operator** | Nomad | Convoy | Unchanged from CP RED. Can now also coordinate drone swarms and psychotronic vehicle interfaces. |
| **Analyst** | Media | Credibility | Unchanged from CP RED. Can now also broadcast Noöspheric intelligence reports that shift public ontological frameworks. |

---

## 7. Humanity and Cyberpsychosis

### Humanity (HUM)

HUM = EMP × 10 (starting value). HUM is lost from:

| Source | HUM Loss |
|---|---|
| Cyberware installation | Per cyberware table (unchanged from CP RED) |
| Psi-burn (overdrafting psi-pool) | Equal to overdraft amount |
| Ontological shock (witnessing NHI reality distortion) | 2d6 per incident (GM discretion) |
| NHI mental contact (failed Psi-Shielding check) | 1d6–4d6 depending on entity power |
| Prolonged Noösphere immersion (unprotected) | 1d6 per hour |

When HUM crosses a tens boundary downward, EMP drops by 1. When HUM reaches 0, the character enters **Cyberpsychosis / Ego Dissolution**.

### Ego Dissolution (NoöPunk Cyberpsychosis)

When EMP hits 0, the character's ego boundary collapses. They merge with the Noösphere. This is not simple psychosis — it's ontological transformation. Options:

1. **Player loses the character.** The entity that was the character may return later as an NHI NPC.
2. **The character is contained.** Europol NHI unit has protocols for this: psi-restraining, ego-reconstruction therapy (slow, expensive, not always successful).
3. **The character becomes a Resonant Walker.** Partial dissolution. They can operate but must make WILL checks every session to maintain ego coherence. They are legally classified as NHI-adjacent.

---

## 8. Noösphere Mechanics

The Noösphere is the merged cyber-astral network. It has three layers that progressively reveal themselves through the game's acts. These map to Faggin's CIP framework: Cyber is technology inside P-Space (Physical), Astral is I-Space (the quantum information field), and Physical is P-Space (our spacetime). **C-Space (qualia) is not a game layer — it is what consciousness is.**

### Layer 1: Cyberspace (P-Space Technology, Early Game)

Functionally similar to CP RED Netrunning. Standard hacking, data theft, network manipulation. Interface ability governs. Cyber is physical infrastructure — computers, networks, code. The astral layer (I-Space) is present but dim.

### Layer 2: Cyber-Astral Merge (P-Space meets I-Space, Mid Game)

Cyberspace (P-Space technology) and astral space (I-Space) overlap. Hackers encounter non-physical entities. Psionic operators can navigate data structures. **Both Interface and psi-skills are relevant.** NHI encounters become common.

**New mechanics:**
- Noöspheric Navigation checks (WILL + Noöspheric Navigation + draw from Circuits)
- Psi-Shielding to protect against Noöspheric entities
- Data can now be encoded in consciousness patterns (Cryptography skill modified)
- Hacking an astral entity requires Psi-Reading as a Complementary Skill

### Layer 3: Spacetime Penetration (I-Space breaches P-Space, Late Game)

The Noösphere (I-Space) begins to affect physical reality (P-Space) directly. Code changes matter. Belief reshapes local physics. PKD's Ubik — consumer psionics, reality layers bleeding into each other.

**New mechanics:**
- Ontological Stability checks to resist reality distortion
- Physical actions can be modified by Noöspheric manipulation
- Belief and consensus become mechanical factors — the more people who believe something, the more real it becomes
- Major Arcana draws become mandatory for significant actions
- The GM may declare **Reality Shifts** (tarot: Wheel of Fortune / Reality Shift) where the constants of local physics temporarily change

---

## 9. Modifiers

### Standard Modifiers (from CP RED)

| Condition | Modifier |
|---|---|
| Night / low light | -1 |
| Never done this before | -1 |
| Complex task | -2 |
| Wrong tools | -2 |
| Uncomfortable / slept badly | -2 |
| Extreme stress | -2 |
| Exhausted | -4 |
| Extremely drunk / sedated | -4 |
| Performing task secretly | -4 |
| Obscured by smoke / darkness | -4 |

### NoöPunk Modifiers

| Condition | Modifier |
|---|---|
| NHI presence nearby (subtle) | -1 to all Checks, +1 to Psi-Reading |
| NHI presence nearby (manifest) | -2 to all Checks, +2 to Psi-Reading |
| Local Noöspheric distortion | -1 to -4 (severity-dependent) to physical Checks; +1 to +4 to Noöspheric Checks |
| Ontological shock threshold crossed | -2 to all Checks until stabilized |
| Psi-enhanced (Complementary) | +1 to linked Skill |
| Agent acting in accordance with Tarot draw's narrative | +1 to +3 (GM discretion) |
| Agent acting against Tarot draw's narrative | -1 to -3 (GM discretion) |

---

## 10. Character Advancement

### Improvement Points (IP)

Earned at the end of each session (unchanged from CP RED mechanics). IP can be spent on:

- Raising Skill Levels (cost varies by skill)
- Raising STATs (expensive — requires in-game justification: training, cyberware, psi-awakening)
- Learning new Skills
- Role Ability advancement

### Psi-Awakening

A character with EMP 6+ may undergo psi-awakening (in-game event, not just IP spend). This unlocks:

- Access to Psi-Pool
- Noöspheric Navigation and Psi-Skills
- Vulnerability to NHI mental contact, psi-burn, and ontological shock

Awakening costs 10 IP and requires a WILL check (DV 15). Failure means the awakening fails — try again next session. Critical failure means the character experiences a minor ontological shock (2d6 HUM loss).

---

## 11. Equipment: Psychotronic Technology

Psychotronic devices interface consciousness with technology. They replace some cyberware functions and add new capabilities:

| Device | Cost | HUM Loss | Function |
|---|---|---|---|
| Psi-Amplifier | 5,000€ | 2d6 | +2 to all psi-Skill Checks. Head-mounted cranial implant. |
| Noöspheric HUD | 2,000€ | 1d6 | Overlays Noöspheric data on visual field. Like a cybernetic HUD for the astral. |
| Psi-Shield Generator | 3,000€ | 1d6 | +2 to Psi-Shielding. Protects against NHI mental contact. |
| Psychotronic Lockpick | 500€ | 0 | Opens electronic locks through psi-pattern recognition. Requires Noöspheric Navigation. |
| Empathy Box | 1,000€ | 1d6 | PKD's Mercerism device. Allows voluntary shared consciousness with other users. +3 to Psi-Reading when connected to another Empathy Box user. |
| Ontological Anchor | 10,000€ | 4d6 | Stabilizes local reality. Grants +4 to Ontological Stability Checks within 10m radius. Military-grade. Restricted. |
| NHI Detector | 3,000€ | 1d6 | Detects NHI presence within 50m. Differentiates AI, ET, and discarnate signatures with a DV15 Noöspheric Navigation Check. |

---

## 12. Quick Reference: Tarot for Checks

| You Want To... | Check | Suit |
|---|---|---|
| Hack a system | INT + Electronics/Security Tech + draw | Circuits |
| Navigate the Noösphere | WILL + Noöspheric Navigation + draw | Circuits (or full deck if merged) |
| Read someone's mind | EMP + Psi-Reading + draw | Resonators |
| Project psi-emotion | COOL + Psi-Impact + draw | Resonators |
| Investigate a crime scene | INT + Deduction + draw | Datblades |
| Fight in melee | DEX + Brawling/Melee + draw | Datblades |
| Shoot someone | REF + Handgun/Shoulder Arms + draw | Datblades (or 1d10 for mundane combat) |
| Seduce or charm | COOL + Persuasion + draw | Tokens (or Resonators if psi-enhanced) |
| Navigate bureaucracy | COOL + Bureaucracy + draw | Tokens |
| Resist ontological shock | COOL + Ontological Stability + draw | Full deck (Major Arcana possible) |
| Contact an NHI | WILL + Psi-Projection + draw | Full deck (Major Arcana likely) |

---

*The dice are for the street. The cards are for the Noösphere. When reality itself is on the table, you don't roll — you draw.*