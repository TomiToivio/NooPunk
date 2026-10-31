# GUMSHOE investigation overlay for CWN: UNSA design specification

**Status:** proposed rules only. **Issue:** #932. **Rules basis:** the [GUMSHOE SRD (OGL version)](https://pelgranepress.com/gumshoe/files/GUMSHOE%20SRD%20OGL%20version.pdf), © Pelgrane Press — the open-licensed source, not any commercial GUMSHOE game. **Authority:** #897 CWN foundational lock.

> **Read with [`ISSUE_932_ACCEPTANCE.md`](ISSUE_932_ACCEPTANCE.md).** That record checks this digest
> claim by claim against the GUMSHOE SRD, corrects three points, and
> lists which of rules I1–I10 are **already implemented** in `src/rules/investigation.py` /
> `anomaly_gate.py`. Do not implement what is already code; the open surface is the five unrepresented
> clue types and the expertise tags, and neither is authorised. Approvals are queued as **D59–D60** in
> [`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md).

## 1. Goals / non-goals

- Enable genuinely satisfying **X-Files / investigative-horror / Nordic psychiatric-horror investigations** starring a **player-created, tabula-rasa rookie UNSA agent** whose personality and investigative identity emerge from the player's choices. **Inspector Dr. Harri S. Romppainen is an NPC supervisor**, not the PC; he may join the field party occasionally when a mission warrants it.
- Preserve the original CWN character sheet, skills, 2d6 attribute + skill checks, saves, hacking, combat, Edges/Foci, equipment, leveling and compatible Without Number modules.
- Preserve GUMSHOE's breakthrough: **a mystery cannot stop because someone missed a roll for essential information**. Finding clues and interpreting them are different actions.
- Let GUMSHOE SRD scenario structures be adapted scene-by-scene into CWN with a GM-only mapping table; no commercial adventure is reproduced.
- Preserve the subtly uncanny NoöPunk tone; do not make NHI explanations automatically conclusive, or define anomalous reports as true in real life.
- **Not now:** implement in Godot, add second skill tree, replace CWN, introduce GUMSHOE d6 general tests, duplicate Stability/Stress, copy proprietary monsters or settings, or import any full commercial GUMSHOE game.

## 2. GUMSHOE rules digest from the GUMSHOE SRD (OGL)

**Source**: [GUMSHOE SRD OGL Version](https://pelgranepress.com/gumshoe/files/GUMSHOE%20SRD%20OGL%20version.pdf), © Pelgrane Press. Sections are cited by name (*Investigative Abilities*, *Gathering Clues*, *Core Clues*, *Special Benefits*, *Tests*). This is an original operational summary of open game content; no commercial game's text, setting or adventures are reproduced.

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

### Campaign-framing components (GUMSHOE SRD: investigative scenario structure; NoöPunk original design)
- **Investigative agency**: briefings, support, deployment, counter-operations and containment → UNSA team and organisational play. The agency, its ethics and its jurisdiction are **NoöPunk's own invention**, not imported.
- **Organised adversaries and anomalous incidents** → human NHI collaborators, hostile clandestine factions, cults, opportunists, noetic anomalies and disinformation, all classified case by case.
- **A recurring local base** — one neighbourhood, its contacts, its institutions and its regulars — is NoöPunk design guidance for Helsinki, hospitals, the university and the UNSA field office; it follows the SRD's advice to keep investigations anchored in a place rather than inventing a setting.
- The SRD treats **Stability** as a general ability with its own recovery and carry-over. It is **not imported**: NoöPunk's existing CWN/AWN-derived Stress module is the single mental-cost track. Retain horror/storytelling principles only, and never treat real psychiatric diagnoses as evidence of NHI activity.

## 3. Proposed NoöPunk GUMSHOE mod v0.1

### Inviolable order of precedence
1. **CWN** rules determine character build, mechanical challenges and consequences.
2. Compatible **SWN/WWN/AWN** additions as previously agreed (e.g., existing Stress).
3. **GUMSHOE investigation mod** determines clue classification and flow only.
4. **NoöPunk's own UNSA/NHI setting** supplies campaign institutions and situations; GUMSHOE supplies investigation structure only, never metaphysical truth or combat rules.

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

## 4. GM-only crosswalk: GUMSHOE investigative abilities → CWN

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
| Local Knowledge | Connect, Know, Survive | Local Helsinki networks |
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

## 5. Setting conversion: GUMSHOE investigation model → NoöPunk

| GUMSHOE / generic investigative element | NoöPunk adaptation |
|---|---|
| Investigating agency | UNSA, specifically its NHI investigation and containment apparatus |
| Field investigation cell | Rookie UNSA player-agent's team, supervised by NPC Romppainen (occasional party companion) |
| Briefing and analysis support | UNSA situation room, scientific lab, psychiatric and forensic support |
| Recurring local base | Helsinki neighbourhoods, local contacts, hospital networks; the rookie PC leads under NPC Romppainen |
| Organised adversaries | Human NHI collaborators, hostile clandestine factions, cults, opportunists and disinformation operators |
| Anomalous phenomena | NHI / noetic / anomalous manifestations; classified case by case |
| Boundary phenomena | One **in-universe hypothesis** about noösphere, consensus reality or boundary phenomena; never settled cosmology |
| Counter-operations | UNSA counterintelligence, containment, tactical intervention |
| Evidence security | UNSA evidence handling, public information, cover story and its ethical dilemma |
| Psychological harm | Existing NoöPunk Stress and consequences |
| Case worksheet | UNSA case file, faction graph, suspects, contacts, adversary response |
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
- [ ] Review and approve the GUMSHOE rules summary against the GUMSHOE SRD (OGL) sections named in §2.
- [ ] Approve/tweak the full investigative + general crosswalk (GM reference, not new player skills).
- [ ] Agree on expertise tags as optional descriptors, not a second character-builder economy.
- [ ] Agree core clues never hinge on failed skill rolls or expenditure, while risky ACTIONS still use CWN.
- [ ] Decide whether optional special discoveries are freely adjudicated (recommended) or receive a **separately proposed** resource rule.
- [ ] Align psychological horror with existing Stress rather than adding Stability.
- [ ] Approve the UNSA agency, NHI adversary, containment and recurring-base conversions; preserve rookie-PC agency, Romppainen's NPC-supervisor role and occasional party availability.
- [ ] Review a **generic, scenario-independent** multi-scene investigation graph for loops, bottlenecks, and alternative clue routes; do not author a Lakkahaltia scenario.
- [ ] Record licensing/attribution boundaries: cite the GUMSHOE SRD under OGL v1.0, and do not copy text or adventures from any commercial game.
- [ ] **Stop at written rules proposal**. No implementation PR, code or Godot changes until separately requested.

## Source / related
- Primary rules reference: [**GUMSHOE SRD, OGL version**](https://pelgranepress.com/gumshoe/files/GUMSHOE%20SRD%20OGL%20version.pdf), © Pelgrane Press. Key sections: *Investigative Abilities*, *General Abilities*, *Gathering Clues*, *Core Clues*, *Special Benefits*, *Tests*, *Contests*, *Stability*.
- NoöPunk rule foundation: #897.
