# GUMSHOE investigation overlay for CWN: UNSA design specification

**Status:** proposed rules only. **Issue:** #932. **Rules basis:** user-supplied *The Esoterrorists*, 2nd ed. (book pp. 8–34, 35–65, 66–77, 79–95). **Authority:** #897 CWN foundational lock.

## 1. Goals / non-goals

- Enable genuinely satisfying **X-Files / Esoterrorists / Nordic psychiatric-horror investigations** starring a **player-created, tabula-rasa rookie UNSA agent** whose personality and investigative identity emerge from the player's choices. **Inspector Dr. Harri S. Romppainen is an NPC supervisor**, not the PC; he may join the field party occasionally when a mission warrants it.
- Preserve the original CWN character sheet, skills, 2d6 attribute + skill checks, saves, hacking, combat, Edges/Foci, equipment, leveling and compatible Without Number modules.
- Preserve GUMSHOE's breakthrough: **a mystery cannot stop because someone missed a roll for essential information**. Finding clues and interpreting them are different actions.
- Let original *Esoterrorists* cases be translated/adapted scene-by-scene with a GM-only mapping table.
- Preserve the subtly uncanny NoöPunk tone; do not make NHI explanations automatically conclusive, or define anomalous reports as true in real life.
- **Not now:** implement in Godot, add second skill tree, replace CWN, introduce GUMSHOE d6 general tests, duplicate Stability/Stress, convert copyrighted creatures verbatim, or import the full Esoterrorists game.

## 2. GUMSHOE rules digest from the uploaded *The Esoterrorists*, 2nd Edition (Robin D. Laws; Gareth Ryder-Hanrahan)

**Source**: user-supplied PDF `Esoterrorists_2nd_Edition_linked.pdf` (2013 printing, 162 PDF pages). *Book page numbers* below, not PDF viewer numbering. This is an original operational summary, not replacement/reproduction of the book.

### Character / resolution division (book pp. 8–10, 19–34)
- GUMSHOE divides abilities into **Investigative** (Academic, Interpersonal, Technical) and **General** abilities. Investigative ratings are professional competence; investigative **pools** are separate, depletable points. General ability ratings/pools support uncertain action and conflict; the two categories have different mechanics.
- An appropriate investigative ability with a positive **rating** discovers essential clues **even if its pool is empty**. Spending investigative points gives **special benefits** (usually 1–2 pool points), never core clues. Relevant free information may also be **zero-point clues**.
- To discover a clue, the investigator must reach a relevant scene, bring suitable expertise, and investigate/indicate an appropriate approach. A plausible alternative to the listed ability works. Obvious/passive clues can be volunteered; players should actively pursue leads.
- **Core clue**: points the PCs onward, never hidden behind a die roll or spend. **Special benefit**: extra color, advantage, earlier insight, NPC goodwill or tactical preparation, not required to finish the case.
- **Inconspicuous clues** may be noticed without consciously investigating; **simple searches** cover ordinary searching without making the mystery hinge on dice.
- GUMSHOE's full general system includes simple tests, contests, spends, combat, Health, Stability, recovery and improvement. **Do not import these mechanics**; equivalent actions remain CWN.

### Mystery design (book pp. 20–24, 66–77)
- Design meaningful scenes and pathways between them. Distinguish core / optional / alternative scenes, antagonist reactions, hazardous scenes, conclusion, and running clocks. An investigation is not a railroad: many approaches and sequences can reach the essential information.
- **Floating core clue**: place an essential lead at any one of several credible scenes to keep momentum.
- **Leveraged clue**: a previously found fact is presented to a reluctant witness so they reveal further information.
- **Pipe clue**: planted information that becomes significant later when combined with new evidence.
- **Restricted clue**: obscure knowledge held by a particular investigator; choose narratively based on background, expertise and spotlight, without blocking progress.
- **Timed result**: a lab/UNSA support analysis arrives later (potentially bringing a core clue).
- Scenario structure should allow alternate methods, redundancy and sensible fallback leads. Distinguish discovery from figuring out motives, assembling theory and choosing actions.

### Esoterrorists institutional / horror components (book pp. 35–65, 79–95)
- **Ordo Veritatis** covert cells, briefings, support stations, deployment, investigation, counter-operations, neutralization, **veil-out**/containment, protocols and ethics → UNSA team and organizational play.
- **Esoterrorist** cells and **Outer Dark Entities**, with the **Membrane**/reality-breach ideas → NoöPunk NHI threats, human collaborators, noetic anomalies, disinformation and disputed in-world models.
- **Station Duty** supplies a small-area, ongoing investigation framework with local contacts, local knowledge, a standing station, recurring characters and town/city relationships; particularly relevant for Helsinki neighborhoods, hospitals, university and UNSA.
- The book has its own **Stability** and psychological horror system. Retain ONLY useful horror/storytelling principles; NoöPunk's existing CWN/AWN-derived Stress/ontological-shock module governs checks and consequences. Avoid two parallel mental-health meters. Do not treat real psychiatric diagnoses as evidence of NHI activity.

## 3. Proposed NoöPunk GUMSHOE mod v0.1

### Inviolable order of precedence
1. **CWN** rules determine character build, mechanical challenges and consequences.
2. Compatible **SWN/WWN/AWN** additions as previously agreed (e.g., existing Stress).
3. **GUMSHOE investigation mod** determines clue classification and flow only.
4. **Esoterrorists → UNSA/NHI** provides campaign institutions, situations and inspiration, not mandatory metaphysical truth or GUMSHOE combat rules.

### Proposed rules, all subject to tabletop playtest
**I1. Core clue guarantee.** For each scene, GM writes essential fact(s), plausible investigative approaches and lead destinations. If an investigator reaches the relevant scene and makes a credible attempt, they obtain the core clue **without rolling**. No resource spend or narrowly unique skill prerequisite. Provide alternate approaches if a specialist is absent. Automatic *access to information* is not automatic access to a locked/hostile site.

**I2. Core-clue access vs dangerous method.** Roll normal CWN only for meaningful risk and uncertainty: entering a guarded site, escaping, hacking under pressure, seizing evidence, winning a hostile confrontation. If that check fails, do not erase the essential lead: give it via another credible route, with time, alarm, exposure or other consequences. Never guarantee survival or mission success.

**I3. Expertise tags (descriptive, not scores).** Use CWN background/profession, Foci, trained skills and narrated prior experience to infer 2–4 optional investigative expertise tags (e.g., forensic psychiatry, police procedure, Finnish folklore, data forensics). Tags do not add dice, points or a progression system. A broadly relevant CWN skill/credible background is enough: tags are prompts, **not mandatory locks**.

**I4. Extra discoveries.** Optional bonus information can be awarded for thoughtful questions, appropriate expertise, good investigation or CWN checks where uncertainty matters. These must not be necessary to identify the next lead. **Default: no investigative pool.** A later, separately approved optional variant could add a tiny case-level resource, but not during this stage.

**I5. Evidence vs interpretation.** Record observed fact, reliability/provenance, investigator interpretation and alternative hypotheses separately. A clue may be real even if the team's explanation of NHI/PSI/noösphere phenomena is mistaken. Encourage conflicting testimony, institutional uncertainty and the NoöPunk grounded-to-uncanny gradient.

**I6. Investigation types.** Support passive, zero-point, core, optional, floating, leveraged, pipe, restricted and timed clues; alternate scenes and multiple leads. A soft "three plausible routes" design heuristic is welcome, not a compulsory rule.

**I7. Skill usage.** CWN's broad skills plus backgrounds govern expertise. Do not import the dozens of GUMSHOE ratings or translate numerical investigative spends to modifiers. Use CWN skill checks only if relevant to actions, not simply to notice essential facts.

**I8. Stress and ethics.** Apply existing NoöPunk AWN/CWN-based Stress/ontological shock when conditions warrant it, and existing social/reputation and faction overlays for consequences. No second Stability track or uncritical real-world psychiatric claims.

**I9. Open-ended players and LLM GM.** Accept a plausible method not written in scenario data; provide clues through that method. Never require the user to say a particular GUMSHOE ability name or click every hotspot. Avoid secretly altering standard CWN check odds.

**I10. Conversion mode.** When running an original GUMSHOE case, keep the clue/scene map; translate any GUMSHOE *general action* to CWN skills/checks, convert NPCs/threats separately into CWN-compatible stats, and mark unsupported mechanics for GM judgment. This is a **semantic** conversion, not an arbitrary numeric one-to-one formula.

## 4. GM-only crosswalk: Esoterrorists investigative abilities → CWN

**CWN skills below are suggested approaches, not strict replacements or compulsory gates.** Specific expertise comes from background, profession and fiction. `Work` denotes a relevant professional specialty. `Program` is the relevant computer/data skill; use established CWN hacking procedures for actual intrusion.

| GUMSHOE investigative ability | Proposed CWN mapping / expertise | Notes |
|---|---|---|
| Anthropology | Know, Connect | Cultural expertise |
| Archaeology | Know, Work | Archaeologist background |
| Architecture | Know, Fix, Work | Structural expertise |
| Art History | Know, Work | Art specialist |
| Astronomy | Know | Astronomy / UAP analysis |
| Ballistics | Know, Fix, Work | Firearms forensics |
| Bullshit Detector | Notice, Talk | Notice inconsistency; not supernatural truth-detection |
| Bureaucracy | Administer, Connect | Records, gatekeepers |
| Chemistry | Know, Heal, Work | Lab expertise as appropriate |
| Cop Talk | Talk, Connect | Law-enforcement background |
| Cryptography | Program, Know | Mathematical/historical cryptology also Know |
| Data Retrieval | Program | Disk, media, data analysis |
| Document Analysis | Know, Administer, Work | Authentication |
| Electronic Surveillance | Program, Fix, Notice | Electronic sensors, eavesdropping |
| Evidence Collection | Notice, Work | Crime-scene procedure |
| Explosive Devices | Fix, Know | **Actual disarming is a risky CWN action** |
| Fingerprinting | Notice, Work | Forensics specialist |
| Flattery | Talk | Interpersonal approach |
| Flirting | Talk, Perform | Interpersonal approach |
| Forensic Accounting | Administer, Trade | Follow funds |
| Forensic Anthropology | Heal, Know, Work | Human remains / autopsy expertise |
| Forensic Entomology | Know, Work | Specialized biology |
| Forensic Psychology | Heal, Know, Notice | Psychology background |
| History | Know | Historical research |
| Impersonate | Perform, Talk, Sneak | Context dependent |
| Interrogation | Talk, Notice | Formal police interviewing |
| Intimidation | Talk | If physical force, normal CWN action |
| Local Knowledge (Station Duty) | Connect, Know, Survive | Local Helsinki networks |
| Languages | Know, Connect | Track spoken languages descriptively; no free fluency from skill level |
| Law | Administer, Know | Legal background |
| Linguistics | Know | Language structures / discourse |
| Natural History | Know, Survive | Biological/environment expertise |
| Negotiation | Talk, Trade | Interpersonal process |
| Occult Studies | Know | Folklore/esotericism, NOT proof of paranormal claims |
| Pathology | Heal, Know, Work | Medical examiner |
| Photography | Know, Fix, Work | Image analysis |
| Reassurance | Talk, Heal | Clinical empathy where relevant |
| Research | Know, Administer | Archives/desk research |
| Streetwise | Connect, Survive | Local underworld |
| Textual Analysis | Know, Administer | Documents/discourse analysis |
| Trivia | Know | Specific cultural knowledge |

**Crosswalk treatment of GUMSHOE General abilities (NOT additive PC skills):**

| GUMSHOE general | CWN / Without Number ruling |
|---|---|
| Athletics | Exert |
| Driving | Drive |
| Filch | Sneak |
| Health | CWN HP and existing damage/recovery |
| Infiltration | Sneak; Program if digital; normal CWN security |
| Mechanics | Fix |
| Medic | Heal |
| Preparedness | CWN gear, inventory, contacts, procurement and GM judgment |
| Scuffling | Punch / stab as appropriate |
| Shooting | Shoot |
| Shrink | Heal, Talk, Know; psychological care as established |
| Stability | Existing NoöPunk Stress/ontological shock; NEVER a second meter |
| Surveillance | Notice, Sneak, Program, Drive as situational |

**Translation of published scenarios:** A GUMSHOE investigative rating requirement becomes “credible CWN skill/background/expertise”; a general test becomes “choose a fitting CWN check/difficulty”; GUMSHOE numerical pools/spends are **not** transferred. In genuine ambiguous cases the GM decides transparently. Do not grant a flat skill bonus solely because of the mapping.

## 5. Setting conversion: Esoterrorists → NoöPunk

| Esoterrorists | NoöPunk adaptation |
|---|---|
| Ordo Veritatis | UNSA, specifically its NHI investigation / containment apparatus |
| OV secret field cell | Rookie UNSA player-agent's investigation team, supervised by NPC Romppainen (occasional party companion) |
| OV briefing / analysis station | UNSA situation room, scientific lab, psychiatric/forensic support |
| OV Station Duty | Recurring Helsinki base, neighborhoods, local contacts and hospital networks, with the rookie PC leading investigations under NPC Romppainen |
| Esoterrorists | Human NHI collaborators, hostile clandestine factions, cults, opportunists and disinformation operators |
| Outer Dark Entities | NHI / noetic / anomalous manifestations; classify case-by-case |
| The Membrane | One **in-universe hypothesis** about noösphere, consensus reality or boundary phenomena; not settled cosmology |
| Counter-ops / neutralization | UNSA counterintelligence, containment, tactical intervention |
| Veil-out | UNSA evidence security, public information, cover story and ethical dilemma |
| Stability / traumatic encounters | Existing NoöPunk Stress and consequences |
| Esoterrorist cell worksheet / adversary record | UNSA case file, faction graph, suspects, contacts, adversary response |
| Clue maps | NoöPunk investigation board; optionally LaclauGPT-style actor/relationship links |

**Principle:** The team is not automatically fighting “occult terrorists” every time. Some cases are hoaxes, misidentified phenomena, institutional malfeasance, rogue AGI activity, human conspiracies or genuinely inexplicable events. Distinguish characters' beliefs from verified case evidence.

## 6. Protagonist and campaign guardrails (author corrections, 2026-10-31)

- **PC:** a tabula-rasa rookie UNSA field agent, not Dr. Romppainen or a prewritten veteran detective. The player's decisions build the protagonist's personality, investigative style, professional loyalties, interpersonal reputation, priorities, and beliefs. CWN mechanical backgrounds/skills still exist, but character identity develops through play rather than a scripted personality.
- **Dr. Inspector Harri S. Romppainen:** an established **NPC**, the protagonist's boss and briefing/mentor authority; potentially recruitable **as an occasional temporary party member** in suitable missions. Never make him the default protagonist, permanent mandatory companion, or the character making the player's decisive choices.
- **Lakkahaltia:** a **minor comic detail within the main plot**, not the name or center of a distinct scenario. No “Etsivä Romppainen ja Lakkahaltian Salaisuus” scenario, adventure outline, test case, or mission authored under this issue.
- **Campaign tone:** grounded Helsinki/Nordic reality with an unsettling pharmaceutical/identity/paranoia atmosphere akin to *A Scanner Darkly*, institutional psychiatry/experimentation weirdness akin to *Maniac*, and hospital-based tragicomic supernatural ambiguity akin to *Riget*. Influences are thematic, not a mandate to copy scenes or plots. Preserve humor as a counterpoint to horror.
- **PC agency:** investigation clues reveal possibilities, never dictate that the PC must embrace an ideology, believe a particular ontological explanation, or obey Romppainen. Supervisor/agency pressure produces consequences and choices.
- **Generic rules demonstration (no named scenario):** rookie agent examines accessible UNSA intake records (Administer/Know) and receives an essential discrepancy without a roll; optionally risks a CWN Program check to retrieve a protected metadata copy, with alert/time costs on failure. Existing Stress resolves any genuinely disturbing later encounter. No fixed case setting or plot is required.

### Tabula-rasa personality as a separate narrative layer

Track *choices and their consequences* through existing dialogue, relations, reputation and faction systems, without replacing CWN attributes or inventing a GUMSHOE personality score. Candidate descriptive axes for **later design**, not mandatory game statistics: skeptical ↔ open-minded, empathic ↔ detached, lawful ↔ improvisational, institutional ↔ independent. Different decisions unlock dialogue and interpersonal affordances, not core clues or “correct” story conclusions.

## 7. Future implementation concept (NOT authorized by this issue)

Potential later design: GM-facing `investigation` object containing scenes, `core_clues`, `optional_discoveries`, `approaches`, `leads_to`, evidence provenance, `reveal_state`, NPC reactions and fallback paths. Keep it independent from `core/cwn`; invoke standard CWN resolution for risky actions. Consider visual case boards and natural-language handling for LLM GM **only after rules signoff**.

## 8. Design-stage checklist / acceptance criteria

- [ ] Agree CWN is unchanged and always primary.
- [ ] Review and approve the GUMSHOE rules summary against uploaded Esoterrorists book pp. 8–34, 35–65, 66–77 and 79–95.
- [ ] Approve/tweak the full investigative + general crosswalk (GM reference, not new player skills).
- [ ] Agree on expertise tags as optional descriptors, not a second character-builder economy.
- [ ] Agree core clues never hinge on failed skill rolls or expenditure, while risky ACTIONS still use CWN.
- [ ] Decide whether optional special discoveries are freely adjudicated (recommended) or receive a **separately proposed** resource rule.
- [ ] Align psychological horror with existing Stress rather than adding Stability.
- [ ] Approve UNSA/Ordo, NHI/Esoterrorist, containment/veil-out and Station Duty conversions; preserve rookie-PC agency, Romppainen's NPC-supervisor role and occasional party availability.
- [ ] Review a **generic, scenario-independent** multi-scene investigation graph for loops, bottlenecks, and alternative clue routes; do not author a Lakkahaltia scenario.
- [ ] Record licensing/attribution boundaries: reference published book, do not copy copyrighted text or adventures wholesale.
- [ ] **Stop at written rules proposal**. No implementation PR, code or Godot changes until separately requested.

## Source / related
- Primary rules reference: **Robin D. Laws, with Gareth Ryder-Hanrahan, _The Esoterrorists_, 2nd ed.** User-uploaded `Esoterrorists_2nd_Edition_linked.pdf`. Key book sections: Your Character pp. 8–17; GUMSHOE Rules System pp. 19–34; Ordo Veritatis pp. 35–43; The Enemy pp. 44–65; Scenarios pp. 66–77; Station Duty pp. 79–95.
- NoöPunk rule foundation: #897.
