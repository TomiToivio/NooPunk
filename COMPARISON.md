# COMPARISON: candidate tabletop rule systems for NoöPunk

**Status: exploratory research, NOT canonical rules.** Tracked in [#255](https://github.com/TomiToivio/NooPunk/issues/255). This document does not change any approved rules, runtime implementation, or rulebook contents. Source of NoöPunk's actual vocabulary is [data/rules/skills.json](data/rules/skills.json) and `RULEBOOK.md` §4.1. Existing implementation epic [#200](https://github.com/TomiToivio/NooPunk/issues/200) still advocates an older **Fudge/Psi-Punk hybrid**. The author's new direction for #255 is **drop Fudge from the candidate foundations** and compare a **Fate Core / Transhumanity's Fate centered** approach. Reconcile the old epic before making any implementation change; preserve previous agents' work.

## 1. Design philosophy: GNS as an exploratory triangle

| Location in triangle | Game family | Strengths to examine | Main reservation |
|---|---|---|---|
| **Center** | Fate Core / Transhumanity's Fate | Aspects, Fate Points, Stunts, invokes/compels, stress, consequences, flexible action types | Fate Core has skills without separate attributes; Transhumanity's Fate cannot be copied directly into a commercial CC adaptation |
| **Simulationist corner** | Eclipse Phase 2E | Bodies, posthuman identity, psi, hacking, injury, gears and believable material constraints | Complexity, longer resolution and NC-licensed expression |
| **Gamist corner** | Cities Without Number / Stars Without Number | Quick rulings, jobs/foci, niches, challenges, tactical choices, GM prep and faction turns | D&D-derived class/level assumptions and uneven thematic fit |
| **Narrativist corner** | PbtA / The Veil | Fiction-first trigger/outcome moves, moral choices, relationships, emotional costs, snowballing complications | Not a unified rules system; playbooks/moves often replace generic skill lists |

**Caution:** GNS is a useful subjective design vocabulary rather than a verified taxonomy; these games do not cleanly occupy only one corner. “Narrativist” here means that a conflict's result changes relationships, commitments, ideology or narrative direction, not that character competency is irrelevant. Example: the players obtain evidence of an Orion proxy, but must decide whether revealing it will destabilize a friendly government.

**Non-negotiable:** NoöPunk keeps six **distinct** attributes `FIT / REF / INT / SOC / PSY / CYB` AND separately rated **skills**. Keep the canonical list without quietly rewriting it. The precise dice kernel, numeric scale, and difficulty targets remain **OPEN**.

## 2. Authorized reading material and rights/provenance

| Family | Reading links | Status / limitations |
|---|---|---|
| Fate Core | https://fate-srd.com/fate-core ; https://fate-srd.com/official-licensing-fate | Official SRD has a CC BY 3.0 route (attribution required); respect excluded brands/art |
| Transhumanity's Fate | https://legacy.eclipsephase.com/releases/transhumanitys-fate | Licensed CC BY-NC-SA; **not an unrestricted commercial reuse SRD** |
| Eclipse Phase 2E | https://eclipsephase.github.io/en/ ; https://eclipsephase.com/cclicense/ ; https://www.eclipsephase.com/wp-content/uploads/2021/12/EclipsePhaseSecondEdition_RulesPrimer.pdf | Online rules reference and free primer; full published work's CC BY-NC-SA restrictions apply |
| Apocalypse World / PbtA | https://lumpley.games/apocalypseworld/ ; https://lumpley.games/2023/11/22/what-is-pbta/ | PbtA is not one universal SRD or license; creator's official resources/policy |
| Worlds of Legacy SRD | https://ufopress.co.uk/wp-content/uploads/2020/03/Worlds-of-Legacy-SRD.pdf | PbtA-derived reference; inspect PDF license notice before copying |
| The Veil | Publisher/author authorized book and any quickstart **LINK TO VERIFY** | Do not conflate book availability with a general SRD; verify edition and license of passages used |
| Cities Without Number | https://cwn.quadrifons.com/ | Community-hosted browser; check **official CC0 SRD's exact scope**, not blanket license for whole published game |
| Stars Without Number Revised | https://www.drivethrurpg.com/en/product/230009/stars-without-number-revised-edition-free-version | Free full-featured rulebook, not automatically an official CC0 SRD |

**Reuse rule:** Independently rewrite high-level game concepts; do not transplant CC BY-NC-SA (Eclipse Phase / Transhumanity's Fate) expression into a commercially reusable CC release. Free access ≠ permission to reuse copyrighted text. Catalog any actual adapted Fate SRD expression and attribution. Preserve a per-section edition, URL, license, and verbatim/adapted/original provenance ledger before publication. This document paraphrases systems and makes analogies; it is not a license clearance certificate.

## 3. Attribute conversion table

A “counterpart” means analogous use, **not equivalent numbers or a fixed formula**. Fate Core has **skills**, not core attributes; EP uses **aptitudes**, with skills in addition; CWN/SWN have D&D-like attributes + skills; PbtA/The Veil usually roll moves using a broad stat or emotion, with no independent universal skill bonus.

| NoöPunk stat | Fate Core skills typically involved | Eclipse Phase 2E aptitude area (conceptual) | CWN / SWN attributes | PbtA / The Veil |
|---|---|---|---|---|
| **FIT** Fitness | Physique, Athletics, Fight | SOM (somatics) | Strength, Constitution | body-related stat / emotional condition depending on move |
| **REF** Reflexes | Athletics, Shoot, Drive | REF (reflexes) | Dexterity | action-based move with relevant stat/emotion |
| **INT** Intelligence | Lore, Investigate, Notice | COG (cognition), INT (intuition) | Intelligence, Wisdom | investigation move / relevant emotion |
| **SOC** Social | Rapport, Empathy, Deceive, Provoke | SAV (savvy) | Charisma | social move / emotional condition |
| **PSY** Psyche | Will plus supernatural Aspect/Stunt | WIL (willpower); psi uses additional game-specific systems | Wisdom/Charisma; SWN psychic class/powers separate | custom psychic move plus fictional permissions |
| **CYB** Cybernetics | Lore, Crafts, Burglary + gear/Aspect | COG/INT and Infosec/Interface/Programming; hardware is separate | Intelligence + Program/Fix; SWN technical skills | interface/hacking move, hardware narrative permission |

**Important:** NoöPunk CYB is a **character stat**, while `Interface / Network / Compute` are **hardware properties**, not extra character attributes. EP's aptitudes are not just “Fate stats” with the numbers changed. PbtA's triggers/procedures cannot be represented with a single numerical column.

## 4. Complete canonical skill vocabulary: cross-system *concept* mapping

This comparison enumerates **every** name from `data/rules/skills.json` at the time of drafting. **These are provisional analogies**, not confirmed identical official skill names: EP entries may vary by edition; Fate examples are from its broad skill model; CWN and SWN lists differ; PbtA examples are proposed possible *types of moves*, not official The Veil moves. “No direct match” must remain an explicit gap.

| NoöPunk skill | Stat | Fate analogue | Eclipse Phase analogue | Without Number analogue | PbtA / The Veil move analogy |
|---|---|---|---|---|---|
| Administrate | INT | Resources, Contacts | Administration | Administer | institutional move |
| Athletics | FIT | Athletics | Freerunning | Exert | act under fire |
| Connect | SOC | Contacts | Networking | Connect | relationship move |
| Counterintelligence | INT | Investigate, Notice | Infosec, Investigation | Notice, Connect | counterspy move |
| Deceive | SOC | Deceive | Deceive | Talk | deceive move |
| ESP | PSY | Notice + Stunt | Psi sleight | SWN psychic ability; CWN none | psychic move |
| Exotic Skill | Variable | Stunt / permission | Exotic Skill | Work / special skill | custom move |
| First Aid | INT | Lore + Stunt | Medicine | Heal (CWN) | healing move |
| Forensics | INT | Investigate | Investigation | Notice, Know | clue move |
| Fray | REF | Athletics, Fight | Fray | Exert, Punch | defend move |
| Free Fall | FIT | Athletics | Free Fall | Exert, Pilot | zero-g move |
| Guns | REF | Shoot | Guns | Shoot | combat move |
| Hardware | CYB | Crafts | Hardware | Fix | repair move |
| Infosec | CYB | Burglary, Lore | Infosec | Program | security move |
| Intelligence Analysis | INT | Investigate, Lore | Research, Investigation | Know, Notice | assess threat move |
| Interface | CYB | Lore + Stunt | Interface | Program | interface move |
| Investigation | INT | Investigate | Investigation | Notice, Know | investigate move |
| Kinesics | SOC | Empathy | Kinesics | Notice, Talk | read a person |
| Know | INT | Lore | Academics / skill field | Know (CWN) | expertise move |
| Lead | SOC | Rapport, Provoke | Persuasion / Leadership | Lead | lead move |
| Medicine | INT | Lore + Stunt | Medicine | Heal (CWN) | heal move |
| Melee | FIT | Fight | Melee | Stab | attack move |
| Noöspace | PSY | Aspect + Stunt | no direct match | no direct match | bespoke projection move |
| Perceive | PSY | Notice | Perception | Notice | read situation |
| Perform | PSY | Rapport + Stunt | Art | Perform | perform move |
| Pilot | REF | Drive | Pilot | Drive / Pilot (SWN) | vehicle move |
| Precognition | PSY | Stunt | precognition-related sleight | SWN psychic power analogy | premonition move |
| Program | CYB | Lore, Crafts | Programming | Program | hack move |
| Provoke | SOC | Provoke | Intimidation | Talk, Lead | apply pressure move |
| Psychic Defence | PSY | Will + Stunt | psi resistance | SWN psychic resistance | resist psi move |
| Psychokinesis | PSY | Stunt | psychokinetic sleight | SWN telekinesis power | psychic move |
| Research | INT | Investigate, Lore | Research | Know | research move |
| Sneak | REF | Stealth | Infiltration | Sneak | sneak move |
| Survival | INT | Survival | Survival | Survive | survive move |
| Tactics | INT | Lore, Notice | Tactics | Lead, Know | battle plan move |
| Talk | SOC | Rapport | Persuasion | Talk | persuade move |
| Telepathy | PSY | Stunt | telepathy-related sleight | SWN telepathy discipline | mind-contact move |
| Trade | SOC | Resources, Rapport | Networking / Profession | Trade | trade move |
| Unarmed | FIT | Fight | Unarmed Combat | Punch | attack move |
| Work | Variable | Lore, Crafts | Profession / field | Work | career move |

**Notes:** `Exotic Skill` and `Work` are fielded/variable; `Know`, `Medicine`, `Hardware`, `Pilot`, `Perform` have field specializations in the current catalog. Neither the Transhumanity's Fate, Eclipse Phase, nor CWN skill list is *literally identical* to the NoöPunk list: record nearest functional correspondence and mismatches. Exact page-by-page validation remains an explicit review task.

## 5. Dice, thresholds, degrees of success: conversion *framework*, not a conversion formula

| Topic | Fate Core | Eclipse Phase 2E | CWN / SWN | PbtA / The Veil | NoöPunk open design question |
|---|---|---|---|---|---|
| Randomizer | 4 Fate dice (`-1,0,+1`) | d100 roll-under | Commonly 2d6 skills and d20 attack rolls | Typically 2d6 + stat/emotion | One kernel across all subsystems? |
| Skills & attributes | Skill rating; no standard separate attribute | Aptitude + skill base/target; percentile resolution | Separate attribute modifier and skill rating | Usually no universal skill ratings | Preserve both, avoid runaway stacked bonuses |
| Difficulty | Ladder with opposition/target numbers, shifts | Target number, modifiers and success quality | 2d6 checks vs difficulty; combat differs | 6-/7–9/10+ bands (typical, game-specific) | Translate outcome *frequency*, not bare integers |
| Degrees | Fail, tie, succeed, succeed with style | Success/critical/superior result and failure gradations | Often binary checks, specific combat exceptions | Miss, mixed, strong hit | Which narrative costs can accompany success? |
| Assistance | Teamwork and advantages/aspects | Bonuses, assistance, gear, teamwork | Aid or modifier by edition and procedure | Aid/interfere move or fiction | Cap stacking and make collaboration meaningful |
| Metacurrency | Fate Points | Pools/moxie-like resources | Effort for some psychic systems; no universal Fate Points | Usually fictionally triggered moves, some playbook resources | Do resource pools overlap? |

**4dF exact distribution (81 equally likely combinations):**

| 4dF result | -4 | -3 | -2 | -1 | 0 | +1 | +2 | +3 | +4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Outcomes / 81 | 1 | 4 | 10 | 16 | 19 | 16 | 10 | 4 | 1 |

A Fate outcome of **+2 net modifier** has a higher success probability against the same target than +0; adding a second unrestricted +2 attribute would substantially change standard Fate target expectations. Do **not** equate EP “60% skill” to Fate “+3” or CWN “level 3”: these are different distributions and target settings.

### Two explicit Fate-first kernels to playtest (both DRAFT)

**Kernel A: bounded additive attributes + skills.** `4dF + A + S`; proposed example ranges `A ∈ [-2,+2]`, `S ∈ [0,3]`. Calibrate difficulty and cap stacked temporary bonuses. *Pros:* both matter every check. *Risk:* very large modifiers relative to 4dF spread, and over-specialization.

**Kernel B: skill-led with attribute edge.** `4dF + S + conditional A`; conditional attribute contribution is **capped** (e.g. +1/0/-1) when attribute especially helps or hinders the specific approach. All stats are rated separately and determine capacity, resistance, fictional access and bounded bonuses. *Pros:* closer to Fate core odds. *Risk:* attributes may feel underused if triggers unclear.

These are **hypotheses, not rules**. When stress-testing, vary target shifts, qualified opponent, gear, teamwork, Fate Point invokes, cyber/psi edge use, expert vs newcomer and PvP.

**Shared example for testing:** An UNSA academy graduate with INT +1, Research 2 examines an Orion-linked forensic dossier. Against a proposed target 3 with neutral dice: Kernel A total 3 = success/tie boundary depending chosen formal rules; Kernel B total 3 if conditional +1 applies. A senior analyst with INT +2 and Research 3 would gain +5 in A, versus at most +4 in B: compare rates of success at *all* difficulty tiers. Fate's real tie and style outcomes must be chosen explicitly before final odds tables.

## 6. Difficulty conversion by *task meaning* (illustrative)

| Fictional difficulty | Fate-style target example | EP2 approach | CWN/SWN approach | PbtA / The Veil approach |
|---|---|---|---|---|
| Routine for trained agent | +0 / +1 opposition | Easy threshold with beneficial modifiers | Lower skill-check DV | Usually no roll unless dramatic stakes |
| Professional challenge | +2 / +3 opposition | Ordinary test with relevant modifiers | Standard skill-check DV | Trigger a move, 7–9 has meaningful cost |
| Elite / resistant opponent | +4 / +5 opposition | Contest or penalty for difficult conditions | Higher DV or opposed check | Opponent/threat moves and snowball |
| Exceptional / NHI anomaly | +6+ if roll is allowed | Heavy penalty or impossible without permission | High DV / required specialist capacity | Fictional positioning or specialist move required |

This table deliberately avoids claiming numerical equivalence. Before implementing any conversion, calculate percentiles for typical beginner/competent/expert agents and verify plausible task permissions.

## 7. Subsystem comparisons and recommendations to investigate

| Subsystem | Fate / Transhumanity's Fate | Eclipse Phase | CWN / SWN | PbtA / The Veil | NoöPunk research hypothesis |
|---|---|---|---|---|---|
| **PSI** | Aspect for psychic identity/permissions; Stunt for a defined exception; stress/consequence costs | Separate psi abilities/sleights, aptitude/skill interactions, costs/risks | SWN disciplines/powers and Effort as explicit resource | A psychic Move triggers from a fictional action and determines 3-tier consequences | Separate **capability/permission**, **check** and **cost**; avoid psi = unrestricted bonus |
| **Combat** | Zones, four actions, stress/consequences and concession | More detailed action timing, injuries, range and gear | Clear rounds, attacks, damage and tactical choices | Harm, fiction-first threat and mixed-result escalation | Test meaningful tactics without EP tactical burden |
| **Social** | Rapport/Deceive/Provoke, aspects and social conflict | Networking, reputation, motivations and social skills | Talk, Connect, Lead and contacts/factions | Emotional stakes, debt/relationship and social moves | Model trust, warrants, diplomacy, obligation, ideology |
| **Factions** | Campaign aspects, extras, consequences and milestones | Organizational networks/reputations | Faction turn, assets, goals, actions | Fronts/threats/clocks, evolving relationships | Preserve existing NoöPunk faction/reputation rules; compare separately |
| **Cyberspace** | Advantage, contests, challenges with technical Stunts | Distinct mesh hacking, infosec, AI and network systems | CWN Program/Fix and hacking procedures; SWN technical actions | Fictional cyber move, costs and exposure | Explicit network topology, privileges and separate hardware Interface/Network/Compute |
| **Investigation** | Discover/create advantage; compel complications | Professional investigative skills/gear | Skill checks, GM procedures | Clue-revealing moves, partial hits and costs | Essential clues cannot disappear on one failed roll; maintain evidence chain |
| **Transhumanism** | Body/identity as Aspects/extras | Morphs/resleeving/augmentation identity | Cyberware and SWN optional AI/transhuman tech | Relationship/identity consequences | Emerging, uneven adoption; don't import whole Eclipse Phase setting |
| **Advancement** | Milestones, skill rearrangement, Stunts | Skills, pools, gear and bodily changes | XP and level advancement | End-of-session questions and playbook growth | Classless lifepath; both expertise and life-altering experiences |

### PSI power, Stunt and Move: important non-identity

An **Eclipse Phase psi sleight** or **Stars Without Number psychic power** typically establishes a concrete capability with eligibility/cost rules. A **Fate Stunt** is a narrowly framed exception or special bonus, often justified by an Aspect. A **PbtA Move** is a triggered procedure that says what happens when a player acts in specific circumstances, including mixed outcomes and GM reactions. They are *not interchangeable units*: one power might need an **Aspect (identity) + Stunt (permission) + skill test (ability) + move-like 7–9 consequence text (narrative price)**. This is a conceptual composition, not a suggestion to run four independent resolution rolls.

## 8. Specific scenarios for apples-to-apples playtests

1. **UNSA interview:** Friendly Confederacy contact offers vital intelligence only if the agents promise confidentiality that may constrain human sovereignty. Test social competency vs voluntary compromise and faction response.
2. **Orion proxy investigation:** Investigators track a donor network via interviews, open-source evidence, forensics and cyber intrusion. Core clue must be discoverable, with consequences escalating on risk.
3. **PSI incident:** Academy-trained psychic probes missing-time impressions; learn something partial and ambiguous without automatic mind-reading truth. Test stress, countermeasures and agency.
4. **Cybergraph operation:** Hacker penetrates one endpoint only where a real authorized/vulnerable technical path exists; compromise does not automatically grant brain access.
5. **Physical crisis:** Rescue civilians from a contaminated anomaly zone with limited rounds, gear constraints, teammates and negotiable risks.

Track median resolution time, number of rule lookups, tactical decisions, meaningful narrative choices, modifier stacks, success rates, safety/agency and GM improvisation burden.

## 9. Dependencies, coordination, deliverables

- [#200](https://github.com/TomiToivio/NooPunk/issues/200) is an existing parent *implementation* epic. Its Fudge/Psi-Punk center conflicts with #255's new author direction. **Do not destructively rewrite #200 or mass-delete implementation artifacts**; raise a resolution comment and use separate approved follow-up change.
- [#217–232](https://github.com/TomiToivio/NooPunk/issues/217), [#144](https://github.com/TomiToivio/NooPunk/issues/144), [#158](https://github.com/TomiToivio/NooPunk/issues/158), [#159](https://github.com/TomiToivio/NooPunk/issues/159) contain pre-existing work. Preserve valid contributions and flag conflicts with the latest decision.
- Candidate future *decision record* must pin: chosen kernel, trait/skill ranges, challenge ladder, stress handling, resources, Stunt and PSI mapping, advancement, and licensing; **none decided merely by this research**.
- Before merge verify: all **40** skills mapped; six attributes; four families; difficulty, PSI/combat/social/faction/cyberspace tables; sources and license caveats; no canonical rule changes.
