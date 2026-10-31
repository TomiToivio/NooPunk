# Design: GUMSHOE SRD (OGL) investigation mod for CWN — rookie UNSA agent

> **Status: design deliverable. Implementation requires its own follow-up.** This issue records the
> proposal and a reviewed conversion reference; **no new core or Godot mechanic is authorised here.**
>
> **Foundational invariant:** *Cities Without Number* (CWN) remains the ONLY core RPG rules engine.
> *Stars Without Number*, *Worlds Without Number* and *Ashes Without Number* can contribute compatible
> optional rules. GUMSHOE is an **investigation procedure and scenario-design mod**, NOT a second set of
> statistics or an alternative resolution engine. Follows foundational lock #897.
>
> **Rules source:** the **GUMSHOE SRD, OGL version** — <https://pelgranepress.com/gumshoe/files/GUMSHOE%20SRD%20OGL%20version.pdf>,
> 68 pages, © 2013 Pelgrane Press, published under the **Open Game License v1.0**. Open content: the
> whole document except the declared Product Identity (the trademarked game-line names, which this
> document therefore never uses as NoöPunk vocabulary). Page numbers below are that PDF's.
>
> **Campaign framing:** *NoöPunk's own*. The rookie UNSA agent, the NHI threat, containment, evidence
> security and the recurring Helsinki base are invented here — no commercial roleplaying book is a
> source, and none of its institutions, entities or adventures is adapted.

## 1. Goals / non-goals

- Enable genuinely satisfying **X-Files / Nordic psychiatric-horror investigations** starring a
  **player-created, tabula-rasa rookie UNSA agent** whose personality and investigative identity emerge
  from the player's choices. **Inspector Dr. Harri S. Romppainen is an NPC supervisor**, not the PC; he
  may join the field party occasionally when a mission warrants it.
- Preserve the original CWN character sheet, skills, 2d6 attribute + skill checks, saves, hacking, combat,
  Edges/Foci, equipment, leveling and compatible Without Number modules.
- Preserve GUMSHOE's breakthrough: **a mystery cannot stop because someone missed a roll for essential
  information**. Finding clues and interpreting them are different actions.
- Preserve the subtly uncanny NoöPunk tone; do not make NHI explanations automatically conclusive, or
  define anomalous reports as true in real life.
- **Not now:** implement in Godot, add a second skill tree, replace CWN, introduce GUMSHOE d6 general
  tests, duplicate Stability/Stress, or import any commercial game's setting, creatures or adventures.

## 2. GUMSHOE SRD digest (OGL version, 68 pp.)

**Licence first, because it decides what may be written down** (p. 1): every page is **open content**
except the declared Product Identity, which is a list of **trademarked game-line names** — this licence
does not grant them, and neither does the GUMSHOE logo. Obligations when NoöPunk ships something based on
it: carry the OGL, keep the Section 15 copyright notice, declare open content and product identity, use
no withheld mark as our own vocabulary (§9).

### The two ability classes (pp. 2, 5, 6, 19–26)
- Abilities are **investigative** (three families: Academic, Interpersonal, Technical — 52 of them in the
  SRD) or **general** (24 of them, `Stability` among them). The SRD gives them **different mechanics on
  purpose**: "general abilities introduce the possibility of failure" and that is exactly what "can stop
  a mystery story dead if applied to the collection of information" (p. 5's reasoning, restated at p. 11
  of the commercial edition the author supplied as inspiration; the OGL SRD carries the same division).
- **Rating vs pool** (p. 2): the rating is static competence; the pool is spent down. The SRD is explicit
  that the distinction is crucial.
- **A rating of at least 1 is needed to get useful information** (p. 5). NoöPunk diverges here on
  purpose — see §4.1.

### Clue acquisition (pp. 32–33)
- **Core clue** (p. 32): the fact you need to reach the next scene. The GM avoids gating it behind an
  obscure ability, and the listed ability is *"just one possibility, not a straight jacket"* — a plausible
  alternative method gets the information out.
- **Passive clues** (p. 32): obvious to a trained investigator on entering, given without prompting.
- **Inconspicuous clues** (p. 33): noticed in a place the party is only passing through. The GM asks
  **which character has the highest current pool** in the ability in question; ties go to the highest
  rating. Nobody declares a search.
- **Simple searches** (p. 33): an ordinary person could credibly find it, so it is found — no ability
  required, no roll.
- **Special benefits** (p. 32): spend pool points for an advantage — tactical preparation, NPC goodwill,
  an earlier insight. Spends buy advantages, **not** the clue the case needs.

### Scenario structure (pp. 56–60)
- **Clue types**: floating core clues (p. 56 — one clue, several possible scenes, used to control pacing),
  leveraged clues (p. 56 — a fact put to a resistant witness), pipe clues (p. 57 — significant later),
  restricted clues (p. 57 — obscure knowledge held by one character, chosen for spotlight and background),
  timed results (pp. 57–58 — a lab or support analysis that arrives later and can carry a core clue).
- **Scene types** (pp. 58–60): introductory, core, alternate, antagonist reaction, hazard, conclusion and
  hybrid scenes, with scene diagrams on p. 61 — and the explicit design rule that alternate routes and
  redundant leads are how a case avoids becoming a corridor.
- The SRD's own italic bracketed notes are designer guidance addressed to people writing games with it;
  they are not rules text and none of them is reproduced here.

### What the SRD does not contain
It is a systems reference, not a setting: no institutions, no antagonist cosmology, no campaign framing.
Everything in §5 is therefore **NoöPunk's own** and needs no permission from anyone.

## 3. Proposed NoöPunk GUMSHOE mod v0.1

### Inviolable order of precedence
1. **CWN** rules determine character build, mechanical challenges and consequences.
2. Compatible **SWN/WWN/AWN** additions as previously agreed (e.g. existing Stress).
3. **GUMSHOE SRD procedure** determines clue classification and flow only.
4. **NoöPunk's own setting** supplies institutions, situations and inspiration — never a mandatory
   metaphysical truth, and never GUMSHOE's combat, health or Stability rules.

### Proposed rules, all subject to tabletop playtest
**I1. Core clue guarantee.** For each scene, the GM writes the essential fact(s), plausible investigative
approaches and lead destinations. If an investigator reaches the relevant scene and makes a credible
attempt, they obtain the core clue **without rolling**. No resource spend, no narrowly unique skill
prerequisite. Provide alternate approaches when a specialist is absent. Automatic *access to information*
is not automatic access to a locked or hostile site.

**I2. Core-clue access vs dangerous method.** Roll normal CWN only for meaningful risk and uncertainty:
entering a guarded site, escaping, hacking under pressure, seizing evidence, winning a hostile
confrontation. If that check fails, do not erase the essential lead: give it by another credible route,
with time, alarm, exposure or other consequences. Never guarantee survival or mission success.

**I3. Expertise tags (descriptive, not scores).** Use CWN background/profession, Foci, trained skills and
narrated prior experience to infer 2–4 optional investigative expertise tags (e.g. forensic psychiatry,
police procedure, Finnish folklore, data forensics). Tags add no dice, points or progression. The SRD's
52-ability inventory is the vocabulary the GM maps *from*, not a list the player buys.

**I4. Extra discoveries.** Optional bonus information may be awarded for thoughtful questions, appropriate
expertise, good investigation, or CWN checks where uncertainty matters. These must not be necessary to
identify the next lead. **Default: no investigative pool.** SWN Effort is the one spendable currency and a
CWN rank is training, not fuel (#704 already enforces this). A later, separately approved optional variant
could add a small case-level resource, but not at this stage.

**I5. Evidence vs interpretation.** Record observed fact, reliability/provenance, investigator
interpretation and alternative hypotheses separately. A clue may be real even if the team's explanation of
NHI/PSI/noösphere phenomena is mistaken. Encourage conflicting testimony, institutional uncertainty and the
grounded-to-uncanny gradient.

**I6. Investigation types.** Support passive, inconspicuous, core, optional, floating, leveraged, pipe,
restricted and timed clues, alternate scenes and multiple leads (SRD pp. 32–33, 56–58). The soft "three
plausible routes" heuristic is welcome, not compulsory.

**I7. Skill usage.** CWN's nineteen broad skills plus backgrounds govern expertise. Do not import the SRD's
investigative ratings or translate pool spends into modifiers. Use CWN skill checks only for actions, not
to notice essential facts.

**I8. Stress and ethics.** Apply the existing NoöPunk Stress module (#928) when conditions warrant it, and
the existing social/reputation and faction overlays for consequences. **No second Stability track** — the
SRD's Stability is a general ability, i.e. a full system with tests, recovery and episode carry-over, and
importing it would contradict the one mental-cost track NoöPunk already runs. No uncritical real-world
psychiatric claims.

**I9. Open-ended players and LLM GM.** Accept a plausible method not written in the scenario data and
provide the clue through it. Never require the player to name a GUMSHOE ability or click every hotspot.
Never secretly alter standard CWN check odds.

**I10. Conversion mode.** When converting any published GUMSHOE case, keep its clue/scene map, translate
its *general* actions into CWN checks, convert its NPCs into CWN-compatible stats separately, and mark
unsupported mechanics for GM judgement. This is a **semantic** conversion, not a one-to-one numeric
formula — and it applies to the open SRD's own example material only.

## 4. Three points a reviewer should decide on purpose

### 4.1 Rank 0 counts as trained — more generous than the SRD
The SRD requires a rating of at least 1 to get useful information (p. 5). CWN says rank 0 is trained
(`untrained_check: -1`, `skills.min: 0`), and the implemented layer treats competence as **presence**
(`Investigator.is_competent`). So NoöPunk hands over core clues to a character the SRD would refuse. That
is deliberate — it stops character creation from gating the first scene — and it is recorded as **G1**.

### 4.2 Passive clues are allocated, not merely named
Highest current pool, ties by highest rating (p. 33). `inconspicuous_finder()` implements an allocation;
whoever changes it should first read which rule it encodes.

### 4.3 Stability is refused because it is a system
A general ability with recovery, episode carry-over and its own consequences (p. 25 and the surrounding
general-ability rules). Refusing it is structural, not stylistic.

## 5. Crosswalk: GUMSHOE SRD abilities → CWN approaches (GM reference only)

**CWN skills are suggested approaches, never gates.** A specific expertise comes from background,
profession and fiction; `Work` denotes a relevant professional specialty, `Know` covers scholarly fields,
and `Program` is the computer/data skill (actual intrusion uses the established CWN hacking procedure).

### 5.1 Investigative abilities (52: 19 Academic · 16 Interpersonal · 17 Technical)

| SRD ability | Family | Suggested CWN approaches |
| --- | --- | --- |
| Anthropology | Academic | Know (anthropology), Connect |
| Archaeology | Academic | Know, Work (archaeologist) |
| Architecture | Academic | Know, Fix, Work |
| Art History | Academic | Know, Work |
| Botany | Academic | Know, Survive |
| Comparative Religion | Academic | Know |
| Forensic Accounting | Academic | Administer, Trade |
| Forensic Psychology | Academic | Heal, Know, Notice |
| Geology | Academic | Know, Survive |
| History | Academic | Know |
| Languages | Academic | Know, Connect (track languages descriptively; no free fluency from rank) |
| Law | Academic | Administer, Know |
| Linguistics | Academic | Know |
| Natural History | Academic | Know, Survive |
| Occult Studies | Academic | Know (folklore and esotericism — never proof of a paranormal claim) |
| Pathology | Academic | Heal, Know, Work |
| Research | Academic | Know, Administer |
| Textual Analysis | Academic | Know, Administer |
| Trivia | Academic | Know |
| Bullshit Detector | Interpersonal | Notice, Talk (notices inconsistency; never supernatural truth-detection) |
| Bureaucracy | Interpersonal | Administer, Connect |
| Cop Talk | Interpersonal | Talk, Connect (law-enforcement background) |
| Flattery | Interpersonal | Talk |
| Flirting | Interpersonal | Talk, Perform |
| High Society | Interpersonal | Connect, Perform |
| Impersonate | Interpersonal | Perform, Talk, Sneak |
| Inspiration | Interpersonal | Lead (rallies the team under pressure) |
| Interrogation | Interpersonal | Talk, Notice |
| Intimidation | Interpersonal | Talk (physical coercion is a normal CWN action) |
| Negotiation | Interpersonal | Talk, Trade |
| Oral History | Interpersonal | Connect, Know |
| Reassurance | Interpersonal | Talk, Heal |
| Respect | Interpersonal | Lead, Connect |
| Streetwise | Interpersonal | Connect, Survive |
| Tradecraft | Interpersonal | Sneak, Notice, Counterintelligence |
| Astronomy | Technical | Know (astronomy, UAP/optical analysis) |
| Ballistics | Technical | Know, Fix, Work |
| Camping | Technical | Survive, Exert |
| Chemistry | Technical | Know, Heal, Work |
| Craft | Technical | Fix, Work |
| Cryptography | Technical | Program, Know |
| Data Retrieval | Technical | Program |
| Document Analysis | Technical | Know, Administer, Work |
| Electronic Surveillance | Technical | Program, Fix, Notice |
| Evidence Collection | Technical | Notice, Work |
| Explosive Devices | Technical | Fix, Know (disarming is a risky CWN action) |
| Fingerprinting | Technical | Notice, Work |
| Forensic Anthropology | Technical | Heal, Know, Work (remains and autopsy) |
| Forensic Entomology | Technical | Know, Work |
| Locksmith | Technical | Fix, Sneak |
| Photography | Technical | Know, Fix, Work (image analysis) |
| Traffic Analysis | Technical | Program, Notice, Administer |

### 5.2 General abilities (24) — these are **not** converted into CWN skills

The SRD's general abilities are the half NoöPunk refuses: uncertain action is CWN's `2d6` check and
conflict is CWN combat. The mapping below says only *which CWN procedure a GM reaches for* when a
converted case calls for one of them.

| SRD general ability | CWN procedure |
| --- | --- |
| Athletics, Fleeing, Scuffling, Shooting | the matching CWN combat/action check, with CWN damage |
| Health, Stability | CWN hit points and saves; mental cost through the Stress module (#928), never a second meter |
| Conceal, Disguise, Filch, Infiltration, Surveillance, Sense Trouble | a Notice/Sneak/Deceive check where the outcome is genuinely uncertain |
| Driving, Piloting, Riding | the matching vehicle/Drive procedure in CWN |
| Explosives, Mechanics, Preparedness | a Fix/Work check; equipment comes from CWN gear, not from a prepared-kit ability |
| Business Affairs, Public Relations | Administer/Connect/Trade checks plus the faction and reputation overlays |
| Gambling | an opposed check where the table wants one |
| Hypnosis | **not converted** — there is no CWN-equivalent; if a case needs it, the GM rules it, and PSI remains the Psyche overlay's business |
| Medic, Shrink | Heal checks; psychological care is narrative, not a separate ability |

## 6. Setting: what NoöPunk invents (no external source)

| NoöPunk element | What it is |
| --- | --- |
| UNSA NHI investigation apparatus | the agency the rookie PC joins; case files, support stations, containment authority |
| The investigation team | the rookie player-agent plus colleagues; the supervisor is NPC Dr. Romppainen |
| Situation room, lab, forensic-psychiatric support | where timed results and institutional pressure come from |
| Recurring Helsinki base | neighbourhoods, hospital and university networks, standing local contacts — a *station* in the procedural sense, used across cases |
| Human collaborators, hostile factions, cults, opportunists, disinformation operators | the antagonist space, chosen per case |
| NHI / noetic / anomalous manifestations | never pre-classified: some cases are hoaxes, misidentified phenomena, institutional malfeasance, rogue-AGI activity, human conspiracy, or genuinely inexplicable |
| Containment and evidence security | counter-intelligence, tactical intervention, public information and the ethical dilemma of the cover story |
| Stress, reputation, factions | the existing NoöPunk overlays, unchanged |

**Principle:** the characters' beliefs are never evidence. A case can end with the anomaly unexplained and
the case still closed.

## 7. Protagonist and campaign guardrails (author corrections, 2026-10-31)

- **PC:** a tabula-rasa rookie UNSA field agent, not Dr. Romppainen or a prewritten veteran detective. The
  player's decisions build the protagonist's personality, investigative style, professional loyalties,
  interpersonal reputation, priorities and beliefs. CWN mechanical backgrounds/skills still exist, but
  identity develops through play.
- **Dr. Inspector Harri S. Romppainen:** established **NPC**, the protagonist's boss and briefing/mentor
  authority; potentially recruitable **as an occasional temporary party member**. Never the default
  protagonist, permanent mandatory companion, or the character making the player's decisive choices.
- **Lakkahaltia:** a **minor comic detail within the main plot**, not a scenario, adventure outline, test
  case or mission authored under this issue.
- **Tone:** grounded Helsinki/Nordic reality with an unsettling pharmaceutical/identity/paranoia
  atmosphere, institutional psychiatry/experimentation weirdness, and hospital-based tragicomic
  supernatural ambiguity. Influences are thematic; no scene or plot is copied.
- **PC agency:** clues reveal possibilities, never dictate that the PC must embrace an ideology, believe a
  particular ontology, or obey Romppainen. Institutional pressure produces consequences and choices.
- **Generic rules demonstration (no named scenario):** a rookie agent examines accessible UNSA intake
  records (`Administer`/`Know`) and receives an essential discrepancy without a roll; optionally risks a
  CWN `Program` check to retrieve a protected metadata copy, with alert/time costs on failure. Existing
  Stress resolves any genuinely disturbing later encounter.

### Tabula-rasa personality as a separate narrative layer

Track *choices and their consequences* through the existing dialogue, relations, reputation and faction
systems — without replacing CWN attributes or inventing a GUMSHOE personality score. Candidate descriptive
axes for **later design**, never mandatory statistics: skeptical ↔ open-minded, empathic ↔ detached,
lawful ↔ improvisational, institutional ↔ independent. Different decisions unlock dialogue and
interpersonal affordances, not core clues or "correct" conclusions.

## 8. Future implementation concept (NOT authorised by this issue)

A GM-facing `investigation` object holding scenes, `core_clues`, `optional_discoveries`, `approaches`,
`leads_to`, evidence provenance, `reveal_state`, NPC reactions and fallback paths. Independent of
`core/cwn`; risky actions invoke standard CWN resolution. Visual case boards and natural-language handling
for an LLM GM **only after rules signoff**. What already exists must not be rebuilt — see the acceptance
record for which of I1–I10 are code today.

## 9. Design-stage checklist / acceptance criteria

- [ ] Agree CWN is unchanged and always primary.
- [ ] Review the GUMSHOE SRD digest against **SRD pp. 2, 5, 19–26, 32–33, 56–60**.
- [ ] Approve/tweak the full 52 + 24 crosswalk (GM reference, not new player skills).
- [ ] Agree expertise tags as optional descriptors, not a second character-builder economy.
- [ ] Agree core clues never hinge on failed skill rolls or expenditure, while risky ACTIONS still use CWN.
- [ ] Decide whether optional special discoveries are freely adjudicated (recommended) or receive a
      **separately proposed** resource rule.
- [ ] Align psychological horror with existing Stress rather than adding Stability.
- [ ] Approve the NoöPunk institution mapping and the rookie-PC/Romppainen guardrail.
- [ ] Review a **generic, scenario-independent** multi-scene investigation graph for loops, bottlenecks and
      alternative clue routes; author no Lakkahaltia scenario.
- [ ] Record licensing/attribution boundaries: OGL obligations, open content vs product identity, no
      withheld mark as vocabulary.
- [ ] **Stop at written rules proposal.** No implementation PR, code or Godot changes until separately
      requested.

## 10. Licensing boundary

- **Source used:** GUMSHOE SRD, **OGL version**, 68 pp., © 2013 Pelgrane Press, **Open Game License v1.0**.
  Open content: everything except the declared Product Identity (trademarked game-line names) — and the
  licence grants **none** of those marks, nor the GUMSHOE logo.
- **Obligations if anything ships:** include the OGL text, keep the Section 15 copyright notice, declare
  open content and product identity, and invent our own vocabulary for everything a withheld mark would
  name.
- **Not used, not adapted:** any commercial GUMSHOE game line, its setting, its institutions, its
  creatures and its adventures. The author's commercial copy was read as **inspiration** about tone; it
  is not a source for this repository, and none of its text, tables or page images is committed.
- **The SRD's bracketed designer notes** are guidance addressed to implementers, not material we carry.

## Design deliverable
`docs/design/ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md` (this document) plus
`docs/design/ISSUE_932_ACCEPTANCE.md`. No Godot or Python code modified.

## Source / related
- Rules: **GUMSHOE SRD, OGL version** — <https://pelgranepress.com/gumshoe/files/GUMSHOE%20SRD%20OGL%20version.pdf>.
- Implementation already on `main`: `src/rules/investigation.py`, `src/rules/anomaly_gate.py`,
  `data/scenarios/lakkahaltia/case_graph.json` (#704, #707); `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md`.
- NoöPunk rule foundation: #897. Stress module: #928.
