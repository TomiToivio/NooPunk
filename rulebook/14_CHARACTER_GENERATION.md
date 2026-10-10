# Character Generation

> **Status: NOÖPUNK NATIVE. Author directive, 2026-10-07.** This chapter is the **character
> generation section** the author asked for. It is a **companion and index** to the
> canonical chargen rules, not a replacement for them.
>
> **The canonical framework lives in `RULEBOOK.md` §9** (issue #144: the Lifepath sequence,
> multiple faction membership, the 10-point Faction Reputation pool, the default Helsinki
> campaign, and the UNSA Police Academy package). **This chapter consumes it and does not
> restate or re-derive it.**
>
> **No new numbers are defined here.** Per `AGENTS.md` §4, the STAT/Skill generation
> procedure, starting skill counts and levels, classes/archetypes and equipment statistics
> were reserved. The author's 2026-10-07 directive opens the **section and its descriptive
> lists** — the *shape* of a character and the paths through it — and does not open new
> arithmetic (§13.11).

---

## 13.1 What character generation is

**A NoöPunk character is an assemblage, not a class.**

The setting's own theory of mind (`rulebook/10_SINGULARITY_CRISIS.md` §9.7, §9.10) says
intelligence emerges from a **human + machine + cultural assemblage**, and that the
meaningful unit of intelligence is **the assemblage, not the isolated human or machine.**
Character generation is therefore the procedure for describing *one such assemblage*: a
person, their factions, their augmentation, their training and their place in a network.

**The canonical procedure is a Lifepath** (`RULEBOOK.md` §9.1), and the canonical default
campaign is **Helsinki / UNSA** (§9.3), whose graduates receive a defined universal Skill
package, a capability-level augmentation package and a stat-free rookie field kit
(`data/rules/unsa_academy.json`).

---

## 13.2 The Lifepath, as an index

**Canonical sequence: `RULEBOOK.md` §9.1.** Reproduced here only as a map of which chapter
supplies the setting content for each stage — **not** as a second copy of the rule.

| Lifepath stage | Setting content supplied by |
| --- | --- |
| 1. Origin / place of birth | §13.4 (Helsinki default, `RULEBOOK.md` §9.3) |
| 2. Family and social background | §13.4; the class-conflict frame in `rulebook/12_BEINGS.md` §11.10 |
| 3. Education | §13.5 (training tracks) |
| 4. Childhood / youth events | §13.4 |
| 5. Political, religious, cultural influences | `rulebook/6_PSYCHIC.md` §6.10.4 (**no universal paradigm shift**) and §6.10.2 (the occult archive) |
| 6. Early faction ties | `rulebook/4_SOCIAL.md`, `rulebook/8_FACTIONS.md` |
| 7. Motivations | `rulebook/4_SOCIAL.md` (Motivation edges) |
| 8. Friends, allies, Contacts | `rulebook/4_SOCIAL.md` (Contact edges) |
| 9. Rivals and enemies | `rulebook/4_SOCIAL.md`, `rulebook/12_BEINGS.md` §11.4 |
| 10. Romance / relationships | `rulebook/4_SOCIAL.md` |
| 11. Major life events and crises | `rulebook/10_SINGULARITY_CRISIS.md`; `rulebook/7_TIMELINE.md` |
| 12. Recruitment into UNSA or alternative employer | `RULEBOOK.md` §38 (UNSA), §9.3 |
| 13. Police Academy basic training | `data/rules/unsa_academy.json`; `rulebook/12_BEINGS.md` §11.9 |
| 14. Specialist academy / track | §13.5 |
| 15. Starting assignment | `rulebook/12_BEINGS.md` §11.4's factions; `docs/design/GAMEPLAY_LOOP.md` |
| 16. Starting Reputation allocation | `RULEBOOK.md` §9.2 (10 points, two or three factions) |
| 17. Starting equipment/resources | `rulebook/13_EQUIPMENT.md` (§12.9 defines the limits) |
| 18. Final character summary | §13.6 |

**Stages may be chosen, rolled or mixed** (`RULEBOOK.md` §9.1). This chapter adds no tables.

---

## 13.3 The six STATs and the four layers

**Canonical: six base STATs — FIT / REF / INT / SOC / CYB / PSY — on a 1–10 scale**
(`RULEBOOK.md` §9.2, issue #131; detail in `rulebook/2_ATTRIBUTES.md`).

**The four ontological layers — Physical / Social / Psychic / Cybernetic — are modes of
participation, not four skill groups and not four STATs** (`rulebook/2_ATTRIBUTES.md`).

**Character generation does not add STATs.** In particular:

- **Cybernetic hardware properties** (compute, interface, network, storage, bandwidth,
  hardening) are **properties of devices, implants and agents — not character STATs**
  (`rulebook/13_EQUIPMENT.md`).
- **Density is not IQ**; **Polarization is not alignment**; **Cybernetic is not
  intelligence** (`rulebook/2_ATTRIBUTES.md`).
- **EMP is not a STAT** and is not restored by this chapter
  (`rulebook/6_PSYCHIC.md` §6.6.3).
- **Seity is not a STAT** and is not implemented (`rulebook/6_PSYCHIC.md` §6.6).

---

## 13.4 Origins and backgrounds — the light list

**Names and light descriptions; no tables, no numbers.**

### 13.4.1 Where a character comes from

| Origin | Light description |
| --- | --- |
| **Helsinki / Uusimaa** | The default campaign ground; Finnish/Nordic/EU institutional texture (`RULEBOOK.md` §9.3) |
| **Other Nordic / Baltic** | Close enough to matter, foreign enough to be useful |
| **EU core** | The bureaucratic and corporate centre |
| **US / China** | Where the Singularity Crisis happened; the two acceleration poles |
| **Corporate arcology / company town** | Raised inside a firm's jurisdiction |
| **Rural / periphery / post-industrial** | Where the networks are thinner and the state is more visible |
| **Orbital / off-world** | The transhuman backdrop (EP-level technology is canon) |
| **Undersea / maritime NHI-adjacent** | `RULEBOOK.md` §40.2's undersea NHI canon |
| **Mobile / stateless / nomadic** | Belonging to networks rather than places |

### 13.4.2 Social background

The setting's class axis is the one `rulebook/12_BEINGS.md` §11.10 makes
existential — **"the ruling class stopped dying."**

| Background | Light description |
| --- | --- |
| **Cybercapitalist / dynastic elite** | Access to resleeving, influence, deniability |
| **Corporate professional** | Inside the machine, with an exit cost |
| **State / public sector** | UNSA, Europol, national services |
| **Working / precarious** | The majority; the augmentation trade-off is most visible here |
| **Marginal / underground** | Networks of the common; the informal economy |
| **Rhizome / Noöspheric / psychedelic-church** | The setting's counter-cultural pole |
| **Confederation follower family** | §`rulebook/12_BEINGS.md` §11.4 — the "UFO religion" texture |
| **Orion-affected or purchased** | Raised inside an infiltration or bargain relationship |

### 13.4.3 Formative events (setting-grounded, light)

- The **Singularity Crisis** and Disclosure as background trauma
  (`rulebook/10_SINGULARITY_CRISIS.md`) — but **not everyone believes the same account**
  (`rulebook/6_PSYCHIC.md` §6.10.4);
- psychic awakening, or the failure to awaken;
- an encounter, a contact, or a **misattributed** one;
- augmentation debt, refusal or coercion (§9.11's political questions);
- a hybrid accusation (§`rulebook/12_BEINGS.md` §11.5 — **the injustice engine**);
- displacement, bereavement, or a resleeving in the family.

---

## 13.5 Training and role paths — the light list

**This is the "character generation" list the author asked for: the shape of a career, not
a class with fixed numbers.** Every path is compatible with the six STATs, the canonical
Skill vocabulary (`data/rules/skills.json`, `RULEBOOK.md` §4.1) and the four layers.

> **No archetype in this list defines a fixed Skill package, a STAT minimum, a bonus or a
> niche-protection rule.** The paths describe *what a character is for*; the canonical
> Lifepath and Skill rules supply the numbers.

### 13.5.1 The default: UNSA Police Academy graduate

The canonical entry point (`RULEBOOK.md` §38; `data/rules/unsa_academy.json`): a universally
trained investigator-officer with a forensic sensorium, psychotronic protection, an optional
augmentation package and a stat-free field kit. **The non-implant path is fully playable**
(§12.1's platform rule). Specialisation happens *after* the universal package.

### 13.5.2 Investigator paths

| Path | Light description |
| --- | --- |
| **Field investigator** | The default generalist; `Investigation`, interviews, scene work |
| **Forensic specialist** | Physical and cyber trace; the lab side |
| **Psionic investigator** | ESP and Psychic Defence; the aura-not-mind-reading archetype (`rulebook/6_PSYCHIC.md` §6.7.3) |
| **Verification officer** | The §11.9 protocol specialist — the setting's Blade Runner officer |
| **Counterintelligence officer** | Infiltration, hybrids, Men in Black (§`rulebook/12_BEINGS.md` §11.7) |
| **X-Risk / anomalies officer** | NHI and X-Risk containment (§38); the information-hazard specialist |
| **Occult-archive researcher** | Symbolic/discursive knowledge as an investigative domain (§6.10.2) |
| **OSINT / intelligence analyst** | The remote, network-side investigator |
| **Negotiator / interviewer** | `Talk`, `Kinesics`, `Deceive`, `Provoke` (canonical task mapping) |

### 13.5.3 Non-UNSA and non-investigator paths

The default campaign is UNSA-centred, but the setting's politics require alternatives:

| Path | Light description |
| --- | --- |
| **Corporate security / fixer** | The mirror image of UNSA, with a different master |
| **Journalist / disclosure researcher** | The Disclosure beat (`RULEBOOK.md` §41) |
| **Rhizome / movement organiser** | Anti-sovereign politics made professional (§9.14) |
| **Psychedelic-church / contemplative practitioner** | PSI training inside a tradition (§6.10.1) |
| **Smuggler / network runner** | The common's logistics |
| **AI-rights advocate / legal operator** | Panopticon, organoids and personhood (§9.11) |
| **Scientist / engineer** | Psychotronics, organoids, quantum interfaces (§9.9) |
| **Hybrid or infiltration-origin character** | **Played with the injustice caveat of §11.5** — the setting's hardest role |

### 13.5.4 How a path is recorded

A path is a **narrative + Faction + Skill-distribution** decision, expressed through the
canonical machinery: the Lifepath stages, the universal Skill package where applicable,
field specialisations (`RULEBOOK.md` §4.1's field model), and the 10-point Reputation pool
(`RULEBOOK.md` §9.2). **Nothing here overrides those rules.**

---

## 13.6 The character as an assemblage — the final sheet

**Not a new stat block — a checklist of what a NoöPunk character *is*, drawn from the
canonical components.** Useful for the Lifepath's stage 18 summary.

- **Identity** — name, pronouns, age, apparent age.
- **STATs** — FIT / REF / INT / SOC / CYB / PSY (1–10).
- **Skills and fields** — per `RULEBOOK.md` §4.1 and `data/rules/skills.json`.
- **Affect graph** — Faction Reputation, Motivations, Contacts, Rivals
  (`rulebook/4_SOCIAL.md`).
- **Augmentation** — implant, wearable, external or **none** (§12.1's platform rule).
- **Psychotronic gear** — Category A and B devices (`rulebook/13_EQUIPMENT.md` §12.4).
- **PSI** — the canonical PSY Skills, if any (`rulebook/6_PSYCHIC.md` §6.7.1).
- **Belief position** — where the character stands on PSI, NHI and AGI
  (§6.10.4: **there is no consensus**).
- **Legal and employment status** — UNSA affiliation, licences, warrants.
- **The assemblage** — what the character is *coupled to*: agents, LLM copilot, exocortex,
  BCI, partner, collective (§9.10's spectrum).
- **Open questions** — the identity and continuity questions the character embodies
  (§`rulebook/12_BEINGS.md` §11.11).

> **The last item is not decoration.** In NoöPunk, *which questions a character carries* is
> part of what the character is.

---

## 13.7 Chargen and the setting's constraints

Three setting rules bind character generation directly:

1. **Augmentation is optional, and refusing invasive cyberware is a valid character.**
   `data/rules/unsa_academy.json`'s platform rule and §12.1.
2. **Nobody agrees about the world.** No character, faction or template may assume a
   consensus ontology (`rulebook/6_PSYCHIC.md` §6.10.4).
3. **The class conflict is personal.** A character's access to augmentation, resleeving and
   legal personhood is a **political position before it is a stat**
   (`rulebook/12_BEINGS.md` §11.10, `rulebook/10_SINGULARITY_CRISIS.md` §9.11).

---

## 13.8 The default lifepath in five steps (issue #197)

The canonical Lifepath (`RULEBOOK.md` §9.1, issue #144) is a long sequence. For the default
UNSA campaign, issue #197 names its **five load-bearing steps** — the spine the setting
content hangs from:

1. **Childhood, social origins and formative experience.** Where they came from and what
   happened to them (§13.4).
2. **The experience that made UNSA recruit them.** Education, a first career, or an
   extraordinary event — the reason their file exists at all.
3. **UNSA Academy common training.** The **equalizing step**: the universal
   investigator-officer package every graduate receives (`data/rules/unsa_academy.json`,
   issue #158), regardless of where they came from. The Academy teaches baseline
   investigation, evidence handling, safety and fieldcraft, cyber hygiene, contact protocol
   and operational competency.
4. **Specialty.** An optional or defined Academy track (§13.5) that differentiates graduates
   *after* the common package.
5. **Graduation, relationships and first assignment.** Who they owe, who they know, and the
   posting they did not choose.

**What differentiates graduates is steps 1–2 and 4; what makes them a party is step 3.**
That is the design intent: prior careers and specializations supply variety, while the common
package guarantees the team can actually work together.

**Skills, packages and Edges are three different things** (issue #197; see the boundary notes
in §13.11): *Skills* are learned competencies (`data/rules/skills.json`, §4.1); the
*lifepath/career package* records professional history and recruitment rationale; *Edges* —
distinctive talents, cybernetic/PSI capabilities, professional advantages, connections or
formative experience, in the spirit of *Cities Without Number* — are a **separate mechanical
question that issue #197 does not settle**. Balance, eligibility and progression for Edges
belong to the rules issues, and this chapter deliberately locks nothing.

> **Related issues (coordinate, do not duplicate).** **#144** owns the Lifepath framework and
> the Reputation pool; **#158** owns the UNSA Academy universal package, the standard
> augmentations and the rookie field kit; **#159** owns the canonical Skill vocabulary, the
> field-specialization model and the default STAT bindings. This chapter consumes all three
> and restates none of them.

---

## 13.9 "Geeks, Jocks & Freaks" — student slang, not classes

**Issue #197 adds exactly one piece of chargen vocabulary, and it is deliberately informal:**
Academy students describe recruitment routes as **Geeks, Jocks & Freaks**. It is **student
slang, not an official or mandatory classification**, and it carries **no mechanical weight**.

| Slang | Recruited for | Typical prior life |
| --- | --- | --- |
| **Geeks** | scholarly or technical expertise | research, engineering, medicine, analysis, academia |
| **Jocks** | operational, military, intelligence, law-enforcement or rescue experience | service, policing, the field |
| **Freaks** | PSI, anomalous encounters, unusual augmentation or other exceptional characteristics | the setting's hardest backgrounds (§11.5) |

Two cautions are part of the term itself:

- **The categories overlap.** A hacker may be a Jock with a Geek's degree; a psi-capable
  recruit may also be the most rigorous analyst in the intake. Do not reduce every hacker to
  one type, or treat every unusual person as one archetype.
- **"Freak" is affectionate, impolite, and the setting knows it.** The word is the students'
  own. It must never license treating unusual people as **inherently pathological**; §11.10's
  class-and-personhood politics and §11.5's injustice engine are the corrective, and the
  Academy's whole point is that an anomalous recruit graduates as an officer like any other.

**The equalizing rule stands above the slang:** all graduates gain the common Academy package,
and prior careers and specializations differentiate them *without* creating character classes
or tiering one route above another. Multiple age and background paths stay viable.

---

## 13.10 Example new-graduate backgrounds (issue #197)

Four worked examples of **step 1 → step 2 → step 3 → step 5** — recruitment routes, not stat
blocks. Each shows a different road into the Academy and the same equalizing result. **They
define no numbers, no Skill packages and no mechanical bonuses**; they illustrate the shape
§13.9 describes.

**1 — The Geek who was already an expert.**
*Origins:* a corporate research arcology; comfortably inside the machine (§13.4.2).
*Recruited:* a published (and quietly suppressed) result in psychotronic signal analysis that
should not have been possible with the equipment she had. UNSA read the paper; her employer
read the security log. *Route:* **Geek**.
*Equalizer:* the Academy taught her to secure a scene, handle evidence and carry a warrant.
*First assignment:* a forensic-support posting she finds humiliatingly junior and privately
perfect — she can see in the data what the field team cannot.
*Parity note:* her technical advantage is a **career history**, not a bonus; the field
investigator beside her is not worse at the job.

**2 — The Jock who thought they were done with all this.**
*Origins:* working/precarious background, periphery post-industrial town (§13.4.2).
*Recruited:* twelve years in national tactical response, ending with an incident nobody will
write down involving something that was not, in the report, present. *Route:* **Jock**.
*Equalizer:* the Academy re-taught procedure he had been doing by instinct for a decade, and
made him articulate it.
*First assignment:* field lead for the new graduates — technically their peer, structurally
their adult.
*Parity note:* experience buys judgment, not immunity; the universal package is genuinely new
material for him too.

**3 — The Freak who never asked for this.**
*Origins:* a Rhizome / psychedelic-church household, or a Confederacy-follower family
(§13.4.2).
*Recruited:* measurable PSI under a screening she did not consent to, after an anomalous
encounter her own community reads as devotion and the state reads as a case. *Route:* **Freak**.
*Equalizer:* the Academy treated her as a **recruit, not a specimen** — the institution's best
face, and exactly the promise it does not always keep (§11.5's injustice engine).
*First assignment:* an investigation team where her partner's job includes noticing if she
stops being herself.
*Parity note:* PSI here is a **capability resolved with the existing Skill check**
(`rulebook/6_PSYCHIC.md` §6.7), not a new subsystem, and not a licence to treat her as damaged.

**4 — The one from the wrong side.**
*Origins:* raised inside an Orion-bargain or purchased relationship (§13.4.2); a hybrid
accusation in the family (§11.5).
*Recruited:* volunteered, which nobody expected, or was handed over, which is worse.
*Route:* readable as any of the three — which is precisely why the slang fails at the edges,
and why the Academy's equalizing rule exists.
*Equalizer:* graduation makes her a UNSA officer; it does not make anyone trust her, and it
does not settle what her background did to her.
*First assignment:* counterintelligence, where her knowledge is the most useful thing in the
room and her file is the most dangerous (§38's Cold War).
*Parity note:* the hardest background is **playable and not punished** — but §11.5's caveat
travels with it, and the campaign must not pretend the suspicion is unreasonable.

> **These are examples, not canon characters and not templates.** Per `AGENTS.md` §2, they
> illustrate the paths; they do not fix names, numbers, factions or outcomes.

---

## 13.11 What this chapter deliberately does NOT define

Binding, per `AGENTS.md` §4 and the author's "light description" instruction:

- **the STAT/Skill generation procedure** beyond the canonical Lifepath framework
  (`RULEBOOK.md` §9) — no new point-buy, no rolling method;
- **starting Skill counts or levels**, except the canonical UNSA package;
- **character classes or archetypes** — §13.5's paths are careers, **not classes**; they
  grant nothing mechanically;
- **derived statistics**;
- **starting equipment counts or prices** (`rulebook/13_EQUIPMENT.md` §12.9);
- **advancement / XP**;
- **an economy**;
- **EMP or Seity as stats** (§13.3).

**The deliverable is the section and its descriptive lists — the shape of a NoöPunk
character and the roads through it. A later character-design issue owns the arithmetic.**
