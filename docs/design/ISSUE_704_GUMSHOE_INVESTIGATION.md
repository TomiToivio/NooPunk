# CWN-first investigation system: GUMSHOE research and NoöPunk design proposal

**Issue:** [#704](https://github.com/TomiToivio/NooPunk/issues/704) · **Status:** tabletop-first proposal, not approved canon or implemented engine.

## 1. Authority and existing implementation

Read [the authoritative Without Number baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md) first. The 2026-10-26 ruling adopts CWN's STR/DEX/CON/INT/WIS/CHA, 2d6 skills, d20 attacks/saves, and source-specific CWN/SWN/AWN/WWN procedures. The former FIT/REF/INT/SOC/PSY/CYB system is **legacy**, not presently canonical, despite appearances in `rulebook/00_START_HERE.md`. Renaming attributes remains a **future proposal** and must not silently change the baseline.

Existing digital layers are **not yet converted uniformly**: `src/rules/wn_core.py` and `data/rules/wn_core.json` carry the WN baseline; `src/rules/swn_psionics.py` is a SWN-inspired effort implementation; `strategy_game/rpg/investigation.py` is a *separate crossover game's* Fate-based demo with branching stages; older `src/rules/core.py` retains an independent d10 kernel. Do not import the crossover Fate implementation into the primary RPG by accident.

The following is an **original investigation procedure inspired by the GUMSHOE design literature**, with CWN retaining authority over uncertain consequential actions. It introduces no new dice, currency, skill ranks, or automatic psychic powers.

## 2. GUMSHOE research

**Primary source:** Pelgrane Press, [GUMSHOE System Reference Document, version 3](https://pelgranepress.com/2013/10/24/the-gumshoe-system-reference-document/) (PDF linked on the official page; CC BY 3.0). Source version 3 was released February 2020 and includes material from GUMSHOE One-2-One and QuickShock. See also [GUMSHOE design overview](https://pelgranepress.com/2018/02/14/gumshoe/) and [design guidance](https://pelgranepress.com/2020/10/16/see-page-xx-how-to-design-for-gumshoe/).

Concepts worth adapting:
1. **Investigative abilities vs general abilities:** knowing how and where to look for information is distinct from winning a contest under pressure. Rather than cloning GUMSHOE's ability lists or spends, map investigation domains onto existing CWN skills.
2. **Core clues:** an indispensable fact or viable lead is provided when players have appropriate fictional access, bring relevant expertise, and undertake a sensible action. Do not roll to decide if the scenario can continue.
3. **Additional information:** deeper context, corroboration, strategic advantage and optional discoveries may require resource costs, additional actions, special access, or checks.
4. **Scene/lead design:** clues point to locations, persons, events, contradictions or investigative actions, not a single compulsory next scene. Multiple routes support open-ended play.
5. **Failure is consequential:** use the existing CWN system to decide exposure, restricted access, interference, hazards, deadlines, negotiations, or whether optional advantages are obtained. Avoid 'roll again until clue appears'.
6. **Unreliable inferences:** guaranteed *observations* are not guaranteed *interpretations*. A genuine anomaly is not automatically proof of extraterrestrials, psionics or a specific psychiatric diagnosis.

**Not recommended:** replace CWN's 2d6 resolution with GUMSHOE's general-ability rules; transplant investigative point-spend economies; bypass physical access or ethics; turn SWN psychic powers into free truth detection; require players to solve the mystery by guessing which prewritten skill to name.

### CWN skill crosswalk (proposed, no new skills)

| Inquiry | CWN competence and fictional prerequisites | Risky action remains under CWN |
| --- | --- | --- |
| Trace physical evidence, reconstruction, observation | Notice; Know for specialist science; Fix for technical artefacts | Seizing guarded evidence, preserving chain of custody under pressure |
| Psychiatry, treatment records, clinical anomalies | Heal plus appropriate professional background; Know for research | Access to private records, patient trust, time-sensitive treatment |
| Interviews, motive, testimony | Talk, Connect, Lead and contextual familiarity | Coercion, deception, persuasion, surveillance or resistance |
| Archives, bureaucracy, institutional records | Administer, Know, Connect | Unauthorized access, deadlines, concealment |
| Digital forensics | Program, Fix, Notice; authenticated reachable devices | Intrusion, countermeasures, limited resources, air gaps |
| Noetic evidence | Ordinary Notice/Know for observable signs; SWN psychic skill only with a legitimate psychic package | SWN Effort/technique rules and CWN consequences where applicable |

**Permission first:** qualifications alone do not grant access to locked rooms, classified files, privately held medical information, unreachable servers, or another person's thoughts. A core clue must have at least one reachable, fair path, potentially involving meaningful access challenges; if that path can fail, offer another independent path or an attainable consequence-based route.

## 3. Proposed tabletop procedure

Before play the referee writes a small **case graph** with nodes (scenes, witnesses, records), edges (leads), facts (observations), and hypotheses (inferences). Mark each clue as **core** or **optional**, and note its evidence provenance, access condition, method and recipient. At least two independent leads should sustain each crucial progression whenever feasible. Do not preselect a single correct explanation if the case is deliberately unresolved.

During play:
1. Player states an investigative intention and method, naming their character's plausible access or expertise. Referee may suggest fitting CWN skill; no keyword guessing.
2. If the investigator has credible competence and access, reveal the **core observation** without rolling. If they lack either, describe the missing prerequisite and leave accessible alternatives.
3. If circumstances create a materially uncertain *consequential* action, use normal CWN resolution with announced difficulty, risks and resources. The result affects cost, optional evidence, speed, safety, credibility or access, not whether an already legitimately found core observation disappears.
4. Record **who asserted what**, the source and medium, time, physical/cyber/psychic channel, reliability, and whether evidence is observation, inference or testimony. A psychic impression is a reported experience, not confirmed objective history.
5. Allow characters to reason incorrectly. Different leads may conflict. No roll dictates what a player must believe.
6. Clock/faction consequences are GM-authored events or existing source procedures, not a new free-floating PbtA economy. Failure may close *one* route, but not every route to a required fact.

### Example: *Etsivä Romppainen ja Lakkahaltian Salaisuus*

**Illustrative investigation only, not setting canon or a claim about mental illness or paranormal events.**

| Node | Core observation available with relevant access and method | Leads onward | Optional action/risk |
| --- | --- | --- | --- |
| A. Ward interview | Patient and nurse independently describe an incident occurring during an unscheduled blackout | Security log (B); pharmacy records (C) | Talk check for willingness to testify publicly |
| B. Camera/security room | Time-stamped gap overlaps a local system restart; logs cannot by themselves establish a supernatural cause | Technician (D); power meter (E) | CWN Program/hacking to access protected backups |
| C. Medication audit | A treatment entry was amended after the reported event | Prescriber (F); archive (E) | Administer/Heal expertise to contextualize drugs and records |
| D. Technician | Work order documents an unexplained maintenance request | Power meter (E); staff rota (F) | Social pressure or threatened job security |
| E. Archive and meter | Discrepancy between official outage time and recorded power use | Compare with A/B/C; independent inquiry | Concealment, privacy obligations, time pressure |
| F. Staff and prescriber | Conflicting accounts remain plausible; neither conclusively establishes an NHI or PSI event | Follow-up witnesses and corroboration | Consequences for trust and reputation |

A patient can be accurately describing an experience without the explanation being established. The referee should not treat psychiatric care as evidence of unreliability or illness as a paranormal diagnostic category.

**Example play:** A qualified investigator inspects an accessible ward register: provide the amended-record clue. Roll only if they try to remove it unseen before security arrives, or access a protected off-site original. A trained SWN telepath may use a source-defined technique if permitted and pay its real Effort; the result has that technique's actual limits, not author-granted omniscience.

## 4. Narrative overlays: optional, subordinate

- **Fate-style aspects:** record descriptive situational tags such as *Staff Fear Retaliation* or *Inconsistent Timestamps*. Do not introduce Fate points or free rerolls without a separately approved migration.
- **PbtA-style consequences:** prepare choices such as delay, exposure, strained relationships, damaged equipment or advancing adversary response. Apply them through ordinary CWN referee adjudication; do not turn a CWN 2d6 into a PbtA move roll.
- **Eclipse Phase:** use its treatment of forks, testimony by alternate selves, memory provenance and psychological stakes as *design prompts*. No new sanity or identity currency without further review.
- **SWN psionics:** use the existing source psychic package, skills, Effort commitment, technique restrictions and recovery. BCI, psychotronic tools and natural PSI are distinct access channels; none bypasses the investigative process automatically.

## 5. Attribute reskin options (decision pending)

| Candidate | Scope | Compatibility |
| --- | --- | --- |
| A. **Keep CWN codes**, add NoöPunk-specific explanatory descriptions/examples | Presentation only | No numeric changes; safest now |
| B. **Alias only** (e.g., STR=Body Power, DEX=Coordination, CON=Resilience, INT=Reason, WIS=Awareness, CHA=Presence) | Character-sheet labels | Maintain canonical STR/DEX/CON/INT/WIS/CHA identifiers in data, saves and rules references |
| C. **Design six new NoöPunk attributes** including reconsideration of FIT/REF/SOC/PSY/CYB | Mechanical replacement | Requires explicit mapping and revised saves, psychics, progression, equipment, skills, NPCs, character creation and migrations |

Recommended **now: A or B** as a nonbreaking first step; C is a separate, deliberately larger author decision. Cybernetics is currently equipment under CWN, and psychic capability is a SWN specialist package, so conflating either with a universal innate attribute has substantial mechanical costs.

## 6. Source, rights and implementation guardrails

- Cite the GUMSHOE SRD under **CC BY 3.0** if incorporating its licensed expression; give credit, source link, licence link and note modifications. This document uses original paraphrase and procedures inspired by general concepts, not copied source prose.
- CWN's SRD [https://cwn.quadrifons.com/](https://cwn.quadrifons.com/) is not proof that **all** text in the commercial CWN/SWN/AWN/WWN books can be reproduced. See repository rights audit [#569](https://github.com/TomiToivio/NooPunk/issues/569).
- Keep the primary game's case data separated from the independent crossover game's `strategy_game/rpg/investigation.py` Fate demo.
- **Tabletop-first:** test the case graph at a table before adding any Python, Godot or CI code. Automated tests, when added, should test executable behavior rather than prose.
- Do not modify the authoritative baseline until the attribute reskin and clue procedure receive explicit sign-off.

## 7. Acceptance / playtest checklist

- [ ] Playtest interviews, cyber-forensics, clinical records and optional PSI using existing CWN/SWN character sheets.
- [ ] Verify that missing a skill or failing a roll never makes *all* core lead paths inaccessible.
- [ ] Verify that players can pursue misleading hypotheses, that claims retain provenance, and that no core clue asserts an unsupported paranormal conclusion.
- [ ] Verify hacking permissions, medical-record privacy and SWN Effort expenditures remain binding.
- [ ] Decide A/B/C attribute reskin policy; then update only approved rulebook material and follow with a versioned digital migration.
- [ ] Compare paper case execution against a future Godot implementation and add runtime tests only after code exists.

## 8. The anomaly gate: keeping uncertainty after the clues are free

Making clues automatic removes the stalled-plot failure mode and introduces its opposite: a table that
collects every fact and then treats the strangest reading as established, because it is the most
memorable. The gate is the discipline that prevents it, and it is implemented in
`src/rules/anomaly_gate.py`.

**Every core clue carries four things**: the fact, the ordinary reading, the anomalous reading, and —
named *in advance* — the **discriminator**, the test that would separate them. A discriminator that is
blank, or a pair of readings that are identical, is refused when the dossier is built: one reading
dressed twice cannot preserve uncertainty.

**A case may not conclude as anomalous while any core discriminator is unrun.** `require_open()` names
the outstanding tests. Failure to *think of* an ordinary explanation is not a discriminator; a test must
actually be attempted and its result recorded. `tally()` returns counts only — there is no verdict
function, because the module does not believe anything.

Two authoring notes, recorded rather than enforced: a discriminator should be **possible** for the
characters (a wall is not a test) and should **cost something** (a formality is not a test).

Applied to *Etsivä Romppainen ja Lakkahaltian Salaisuus*: the future-tense files have both a template
artifact reading and a precognitive reading, and the separating test is the template deployment history
against the file timestamps. Until that test runs, both hypotheses stay live and the table may act only
on what is common to them — protecting the remaining patients and securing the files.
